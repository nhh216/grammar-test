from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.exam import (
    ExamGenerateRequest,
    ExamHistoryResponse,
    ExamSessionResponse,
    ExamSubmitRequest,
    QuestionResponse,
)
from app.services.exam_service import ExamService

router = APIRouter(tags=["exams"])


def _hide_answers(session_response: ExamSessionResponse) -> ExamSessionResponse:
    """Strip correct_answer from questions during active exam."""
    for q in session_response.questions:
        q.correct_answer = None
    return session_response


@router.post("/exams/generate", response_model=ExamSessionResponse)
async def generate_exam(req: ExamGenerateRequest, db: AsyncSession = Depends(get_db)):
    """Generate a new exam session using ChatGPT."""
    try:
        service = ExamService(db)
        session = await service.generate_exam(req.topic_id, req.num_questions)
        response = ExamSessionResponse.model_validate(session)
        # Don't reveal answers during the exam
        return _hide_answers(response)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/exams/{session_id}/submit", response_model=ExamSessionResponse)
async def submit_exam(
    session_id: int,
    req: ExamSubmitRequest,
    db: AsyncSession = Depends(get_db),
):
    """Submit answers, grade via ChatGPT, return results with explanations."""
    try:
        service = ExamService(db)
        session = await service.submit_exam(session_id, req.answers)
        return ExamSessionResponse.model_validate(session)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/exams/history", response_model=list[ExamHistoryResponse])
async def exam_history(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List past exam sessions, newest first."""
    service = ExamService(db)
    sessions = await service.get_history(limit=limit, offset=offset)
    return sessions


@router.get("/exams/{session_id}/review", response_model=list[QuestionResponse])
async def review_exam(session_id: int, db: AsyncSession = Depends(get_db)):
    """Return only incorrectly answered questions for review practice."""
    try:
        service = ExamService(db)
        questions = await service.get_review(session_id)
        return questions
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/exams/{session_id}", response_model=ExamSessionResponse)
async def get_exam(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific exam session with all questions and results."""
    try:
        service = ExamService(db)
        session = await service.get_session(session_id)
        return ExamSessionResponse.model_validate(session)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
