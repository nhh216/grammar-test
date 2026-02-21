# Phase 2: Backend Implementation

## Context
- [plan.md](./plan.md)
- Depends on: [Phase 1](./phase-01-setup.md) completed

## Overview
- **Priority:** P1
- **Status:** complete
- **Effort:** 6h
- Implement database models, API endpoints, and OpenAI integration for question generation/grading.

## Key Insights
- GPT-4o-mini is cost-effective (~$0.15/1M input tokens) and fast enough for this use case
- Structured JSON output via system prompt + `response_format={"type": "json_object"}` ensures parseable responses
- Async SQLAlchemy avoids blocking during OpenAI API calls
- Keep OpenAI prompts in dedicated constants file for easy tuning

## Requirements

### Functional
- CRUD for grammar topics (seeded, read-only for users)
- Generate exam questions via OpenAI for a given topic + question count
- Grade submitted answers via OpenAI with per-question explanations
- Persist exam sessions and questions to PostgreSQL
- Retrieve exam history and review wrong answers

### Non-Functional
- OpenAI calls must have timeout (30s) and retry (1x)
- API responses under 500ms (excluding OpenAI latency)
- Input validation on all endpoints

## Architecture

```
Request Flow:
  Client -> FastAPI Router -> Service Layer -> OpenAI / Database
                                |
                          Pydantic Schema validation
```

## Related Code Files

### Files to Create
- `backend/app/models/__init__.py`
- `backend/app/models/grammar-topic.py` - GrammarTopic model
- `backend/app/models/exam-session.py` - ExamSession model
- `backend/app/models/question.py` - Question model
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/topic.py` - Topic response schemas
- `backend/app/schemas/exam.py` - Exam request/response schemas
- `backend/app/schemas/question.py` - Question schemas
- `backend/app/services/__init__.py`
- `backend/app/services/openai-service.py` - OpenAI integration
- `backend/app/services/exam-service.py` - Exam business logic
- `backend/app/api/__init__.py`
- `backend/app/api/router.py` - Main API router
- `backend/app/api/topics.py` - Topics endpoints
- `backend/app/api/exams.py` - Exams endpoints
- `backend/app/core/prompts.py` - OpenAI prompt templates
- `backend/seed.py` - Database seeder for grammar topics

### Files to Modify
- `backend/app/main.py` - Include API router
- `backend/alembic/env.py` - Import all models for autogenerate

## Implementation Steps

### 1. Database Models (45 min)

#### `backend/app/models/grammar-topic.py`
```python
class GrammarTopic(Base):
    __tablename__ = "grammar_topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)

    sessions: Mapped[list["ExamSession"]] = relationship(back_populates="topic_rel")
```

#### `backend/app/models/exam-session.py`
```python
class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("grammar_topics.id"))
    topic: Mapped[str] = mapped_column(String(100))  # denormalized for convenience
    num_questions: Mapped[int]
    score: Mapped[int | None]  # null until graded
    total: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="in_progress")  # in_progress | completed
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    completed_at: Mapped[datetime | None]

    topic_rel: Mapped["GrammarTopic"] = relationship(back_populates="sessions")
    questions: Mapped[list["Question"]] = relationship(back_populates="session", cascade="all, delete-orphan")
```

#### `backend/app/models/question.py`
```python
class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("exam_sessions.id"))
    question_number: Mapped[int]
    question_text: Mapped[str] = mapped_column(Text)
    options: Mapped[dict] = mapped_column(JSON)  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: Mapped[str] = mapped_column(String(1))  # A, B, C, or D
    user_answer: Mapped[str | None] = mapped_column(String(1))
    is_correct: Mapped[bool | None]
    explanation: Mapped[str | None] = mapped_column(Text)

    session: Mapped["ExamSession"] = relationship(back_populates="questions")
```

### 2. Create and Run Migration (15 min)

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

### 3. Seed Grammar Topics (15 min)

Create `backend/seed.py` to insert predefined topics:
- Tenses (Present Simple, Past Simple, Future, Present Perfect, Past Perfect)
- Articles (A/An/The)
- Prepositions
- Modal Verbs
- Conditionals (Type 0, 1, 2, 3)
- Passive Voice
- Relative Clauses
- Subject-Verb Agreement
- Gerunds & Infinitives
- Comparatives & Superlatives
- Conjunctions & Connectors
- Word Forms (noun/verb/adj/adv)

### 4. Pydantic Schemas (30 min)

#### `backend/app/schemas/topic.py`
```python
class TopicResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    model_config = ConfigDict(from_attributes=True)
```

#### `backend/app/schemas/exam.py`
```python
class ExamGenerateRequest(BaseModel):
    topic_id: int
    num_questions: int = Field(default=10, ge=5, le=20)

class QuestionResponse(BaseModel):
    id: int
    question_number: int
    question_text: str
    options: dict[str, str]
    correct_answer: str | None = None  # hidden during exam
    user_answer: str | None = None
    is_correct: bool | None = None
    explanation: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ExamSessionResponse(BaseModel):
    id: int
    topic: str
    num_questions: int
    score: int | None
    total: int
    status: str
    created_at: datetime
    completed_at: datetime | None
    questions: list[QuestionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class ExamSubmitRequest(BaseModel):
    answers: dict[int, str]  # {question_id: "A"|"B"|"C"|"D"}

class ExamHistoryResponse(BaseModel):
    id: int
    topic: str
    score: int | None
    total: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### 5. OpenAI Service (1h)

#### `backend/app/core/prompts.py`
Define two prompt templates:

**Generation Prompt:**
```
You are a TOEIC grammar expert. Generate {num_questions} multiple-choice questions
for the grammar topic: "{topic}".

Each question must:
- Test TOEIC-level English grammar
- Have exactly 4 options (A, B, C, D)
- Have exactly one correct answer
- Be a sentence completion or error identification format

Return JSON:
{
  "questions": [
    {
      "question_text": "The manager _____ the report before the meeting started.",
      "options": {"A": "completed", "B": "has completed", "C": "had completed", "D": "completes"},
      "correct_answer": "C"
    }
  ]
}
```

**Grading Prompt:**
```
You are a TOEIC grammar expert. Grade these answers and explain each one.

Questions and user answers:
{questions_with_answers}

For each question, provide:
- Whether the user's answer is correct
- A clear, concise explanation of WHY the correct answer is correct
- If wrong, explain why the user's chosen answer is incorrect

Return JSON:
{
  "results": [
    {
      "question_id": 1,
      "is_correct": true/false,
      "explanation": "..."
    }
  ]
}
```

#### `backend/app/services/openai-service.py`
```python
class OpenAIService:
    def __init__(self, settings: Settings):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate_questions(self, topic: str, num_questions: int) -> list[dict]:
        """Call GPT to generate TOEIC grammar questions."""
        # Use response_format={"type": "json_object"}
        # Parse and validate response
        # Retry once on parse failure

    async def grade_answers(self, questions_with_answers: list[dict]) -> list[dict]:
        """Call GPT to grade answers and provide explanations."""
        # Similar structure with grading prompt
```

### 6. Exam Service (1h)

#### `backend/app/services/exam-service.py`
```python
class ExamService:
    def __init__(self, db: AsyncSession, openai_service: OpenAIService):
        self.db = db
        self.openai = openai_service

    async def generate_exam(self, topic_id: int, num_questions: int) -> ExamSession:
        """Generate exam: call OpenAI, persist session + questions."""
        # 1. Fetch topic from DB
        # 2. Call openai_service.generate_questions()
        # 3. Create ExamSession record
        # 4. Create Question records
        # 5. Return session with questions

    async def submit_exam(self, session_id: int, answers: dict[int, str]) -> ExamSession:
        """Grade exam: save answers, call OpenAI for grading, update records."""
        # 1. Fetch session + questions
        # 2. Update user_answer on each question
        # 3. Build grading payload
        # 4. Call openai_service.grade_answers()
        # 5. Update is_correct + explanation on each question
        # 6. Calculate score, update session status to "completed"
        # 7. Return updated session

    async def get_history(self, limit: int = 20, offset: int = 0) -> list[ExamSession]:
        """Fetch past sessions ordered by created_at desc."""

    async def get_session(self, session_id: int) -> ExamSession:
        """Fetch single session with all questions."""

    async def get_review(self, session_id: int) -> list[Question]:
        """Fetch only incorrect questions for a session."""
```

### 7. API Endpoints (1h)

#### `backend/app/api/topics.py`
```python
@router.get("/topics", response_model=list[TopicResponse])
async def list_topics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GrammarTopic).order_by(GrammarTopic.name))
    return result.scalars().all()
```

#### `backend/app/api/exams.py`
```python
@router.post("/exams/generate", response_model=ExamSessionResponse)
async def generate_exam(req: ExamGenerateRequest, ...):
    # Hide correct_answer in response (exam in progress)

@router.post("/exams/{session_id}/submit", response_model=ExamSessionResponse)
async def submit_exam(session_id: int, req: ExamSubmitRequest, ...):
    # Return full results with correct answers + explanations

@router.get("/exams/history", response_model=list[ExamHistoryResponse])
async def exam_history(limit: int = 20, offset: int = 0, ...):

@router.get("/exams/{session_id}", response_model=ExamSessionResponse)
async def get_exam(session_id: int, ...):

@router.get("/exams/{session_id}/review", response_model=list[QuestionResponse])
async def review_exam(session_id: int, ...):
```

#### `backend/app/api/router.py`
```python
api_router = APIRouter(prefix="/api")
api_router.include_router(topics.router)
api_router.include_router(exams.router)
```

### 8. Wire Up and Test (30 min)

1. Update `main.py` to include `api_router`
2. Test each endpoint manually with `curl` or API client
3. Verify OpenAI integration with a real API call
4. Check DB records are persisted correctly

## Todo List

- [ ] Create GrammarTopic SQLAlchemy model
- [ ] Create ExamSession SQLAlchemy model
- [ ] Create Question SQLAlchemy model
- [ ] Generate and run Alembic migration
- [ ] Create seed script for grammar topics
- [ ] Define Pydantic schemas (topic, exam, question)
- [ ] Implement OpenAI prompt templates
- [ ] Implement OpenAIService (generate + grade)
- [ ] Implement ExamService (generate, submit, history, review)
- [ ] Implement GET /api/topics endpoint
- [ ] Implement POST /api/exams/generate endpoint
- [ ] Implement POST /api/exams/{id}/submit endpoint
- [ ] Implement GET /api/exams/history endpoint
- [ ] Implement GET /api/exams/{id} endpoint
- [ ] Implement GET /api/exams/{id}/review endpoint
- [ ] Wire router into main.py
- [ ] Manual integration test with real OpenAI call

## Success Criteria
- All 6 API endpoints return correct responses
- Questions generated by GPT parse into valid Pydantic models
- Grading returns explanations for each question
- Exam sessions persist correctly in PostgreSQL
- Review endpoint returns only incorrect answers

## Risk Assessment
| Risk | Mitigation |
|------|------------|
| GPT returns malformed JSON | Use `response_format=json_object`, validate with Pydantic, retry once |
| GPT generates wrong correct_answer | Accept for MVP; can add validation heuristics later |
| Slow OpenAI response (>10s) | Set 30s timeout, show loading on frontend |
| DB connection pool exhaustion | Use async sessions, set pool size in config |

## Security Considerations
- Validate all input with Pydantic (field constraints, type checks)
- Never expose OPENAI_API_KEY to frontend
- Sanitize GPT output before storing (strip HTML/scripts)
- Rate limit exam generation (prevent API abuse) - consider adding in v2

## Next Steps
- Proceed to [Phase 3: Frontend Implementation](./phase-03-frontend.md)
