"""Tests for exam endpoints (generate, submit, history, get, review)."""

import pytest
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _get_first_topic_id(client) -> int:
    resp = await client.get("/api/topics")
    return resp.json()[0]["id"]


async def _generate_exam(client, mock_generate, num_questions: int = 5) -> dict:
    topic_id = await _get_first_topic_id(client)
    resp = await client.post(
        "/api/exams/generate",
        json={"topic_id": topic_id, "num_questions": num_questions},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_generate_exam_returns_session(client, mock_generate):
    data = await _generate_exam(client, mock_generate)

    assert data["status"] == "in_progress"
    assert data["num_questions"] == 5
    assert len(data["questions"]) == 5


@pytest.mark.asyncio
async def test_generate_exam_hides_correct_answers(client, mock_generate):
    data = await _generate_exam(client, mock_generate)
    for q in data["questions"]:
        assert q.get("correct_answer") is None, "correct_answer must be hidden during exam"


@pytest.mark.asyncio
async def test_generate_exam_invalid_topic(client, mock_generate):
    resp = await client.post(
        "/api/exams/generate",
        json={"topic_id": 99999, "num_questions": 5},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_generate_exam_validates_num_questions(client, mock_generate):
    topic_id = await _get_first_topic_id(client)
    # Too few
    resp = await client.post(
        "/api/exams/generate",
        json={"topic_id": topic_id, "num_questions": 3},
    )
    assert resp.status_code == 422
    # Too many
    resp = await client.post(
        "/api/exams/generate",
        json={"topic_id": topic_id, "num_questions": 25},
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Submit
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_submit_exam_returns_completed_session(client, mock_generate, mock_grade):
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]
    answers = {str(q["id"]): "A" for q in session["questions"]}

    resp = await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "completed"
    assert data["score"] is not None
    assert data["completed_at"] is not None


@pytest.mark.asyncio
async def test_submit_exam_reveals_correct_answers(client, mock_generate, mock_grade):
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]
    answers = {str(q["id"]): "A" for q in session["questions"]}

    resp = await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})
    data = resp.json()

    for q in data["questions"]:
        assert q["correct_answer"] is not None
        assert q["explanation"] is not None


@pytest.mark.asyncio
async def test_submit_exam_double_submit_returns_400(client, mock_generate, mock_grade):
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]
    answers = {str(q["id"]): "A" for q in session["questions"]}

    await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})
    resp = await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_submit_exam_not_found(client, mock_grade):
    resp = await client.post("/api/exams/99999/submit", json={"answers": {}})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_history_returns_list(client, mock_generate):
    await _generate_exam(client, mock_generate)
    resp = await client.get("/api/exams/history")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_history_schema(client, mock_generate):
    await _generate_exam(client, mock_generate)
    resp = await client.get("/api/exams/history")
    item = resp.json()[0]
    for field in ("id", "topic", "score", "total", "status", "created_at"):
        assert field in item


@pytest.mark.asyncio
async def test_history_pagination(client, mock_generate):
    # limit=1 should always return exactly 1 item (sessions from other tests are fine)
    await _generate_exam(client, mock_generate)
    resp = await client.get("/api/exams/history?limit=1&offset=0")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


# ---------------------------------------------------------------------------
# Get session detail
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_exam_returns_session_with_questions(client, mock_generate):
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]

    resp = await client.get(f"/api/exams/{session_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == session_id
    assert len(data["questions"]) == 5


@pytest.mark.asyncio
async def test_get_exam_not_found(client):
    resp = await client.get("/api/exams/99999")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Review (wrong answers only)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_review_returns_only_wrong_answers(client, mock_generate):
    """With all-correct mock grading, review should return empty list."""
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]
    answers = {str(q["id"]): "A" for q in session["questions"]}

    # Submit with all-correct mock
    async def all_correct(questions_with_answers):
        return [
            {"question_id": q["question_id"], "is_correct": True, "explanation": "Correct!"}
            for q in questions_with_answers
        ]

    with patch("app.services.exam_service.openai_service.grade_answers", side_effect=all_correct):
        await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})

    resp = await client.get(f"/api/exams/{session_id}/review")
    assert resp.status_code == 200
    assert resp.json() == []  # no wrong answers


@pytest.mark.asyncio
async def test_review_returns_wrong_questions(client, mock_generate):
    """With all-wrong mock grading, review should return all questions."""
    session = await _generate_exam(client, mock_generate)
    session_id = session["id"]
    answers = {str(q["id"]): "B" for q in session["questions"]}

    async def all_wrong(questions_with_answers):
        return [
            {"question_id": q["question_id"], "is_correct": False, "explanation": "Wrong!"}
            for q in questions_with_answers
        ]

    with patch("app.services.exam_service.openai_service.grade_answers", side_effect=all_wrong):
        await client.post(f"/api/exams/{session_id}/submit", json={"answers": answers})

    resp = await client.get(f"/api/exams/{session_id}/review")
    assert resp.status_code == 200
    assert len(resp.json()) == 5
