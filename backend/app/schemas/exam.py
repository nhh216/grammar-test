from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExamGenerateRequest(BaseModel):
    topic_id: int
    num_questions: int = Field(default=10, ge=5, le=20)


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_number: int
    question_text: str
    options: dict[str, str]
    # Omitted during active exam, revealed after grading
    correct_answer: str | None = None
    user_answer: str | None = None
    is_correct: bool | None = None
    explanation: str | None = None


class ExamSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    num_questions: int
    score: int | None
    total: int
    status: str
    created_at: datetime
    completed_at: datetime | None
    questions: list[QuestionResponse] = []


class ExamHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    score: int | None
    total: int
    status: str
    created_at: datetime


class ExamSubmitRequest(BaseModel):
    # {question_id: "A"|"B"|"C"|"D"}
    answers: dict[int, str]
