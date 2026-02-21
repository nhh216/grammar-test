"""
Shared test fixtures.
Uses the real PostgreSQL database (running in Docker).
- NullPool engine: each request gets a fresh connection (avoids asyncpg pool conflicts)
- Session-scoped setup for efficiency; cleanup via docker exec at the end
- OpenAI calls mocked for deterministic, cost-free tests
"""

import logging
import subprocess
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from unittest.mock import AsyncMock, patch

from app.main import app
from app.core.database import get_db
from app.core.config import settings

# ---------------------------------------------------------------------------
# Mock payloads
# ---------------------------------------------------------------------------

MOCK_QUESTIONS_5 = [
    {
        "question_text": f"The manager _____ the report before the meeting. (Q{i})",
        "options": {"A": "completed", "B": "has completed", "C": "had completed", "D": "completes"},
        "correct_answer": "C",
    }
    for i in range(1, 6)
]


_log = logging.getLogger(__name__)


def _cleanup_exam_data() -> None:
    """Delete exam data synchronously via docker exec (avoids asyncpg loop issues)."""
    result = subprocess.run(
        [
            "docker", "exec", "toeic-exercise-db-1",
            "psql", "-U", "toeic", "-d", "toeic_exercise",
            "-c", "DELETE FROM questions; DELETE FROM exam_sessions;",
        ],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        _log.warning("DB cleanup failed (rc=%d): %s", result.returncode, result.stderr.decode())


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(scope="session")
async def client():
    """
    Session-scoped HTTP test client.
    Uses NullPool so each request creates a fresh DB connection (no pool state issues).
    """
    # NullPool: each connection is created fresh and discarded after use
    test_engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    test_session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with test_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
    await test_engine.dispose()
    _cleanup_exam_data()


@pytest.fixture
def mock_generate():
    """Patch generate_questions to return 5 deterministic questions."""
    with patch(
        "app.services.exam_service.openai_service.generate_questions",
        new_callable=AsyncMock,
        return_value=MOCK_QUESTIONS_5,
    ) as m:
        yield m


@pytest.fixture
def mock_grade():
    """Patch grade_answers to return all-correct results."""
    async def _grade(questions_with_answers: list[dict]) -> list[dict]:
        return [
            {
                "question_id": q["question_id"],
                "is_correct": True,
                "explanation": "Past perfect is correct here.",
            }
            for q in questions_with_answers
        ]

    with patch(
        "app.services.exam_service.openai_service.grade_answers",
        side_effect=_grade,
    ) as m:
        yield m
