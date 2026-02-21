"""Exam business logic: generate, submit, history, review."""

import random
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.exam_session import ExamSession
from app.models.grammar_topic import GrammarTopic
from app.models.question import Question
from app.models.question_bank import QuestionBank
from app.services.groq_service import groq_service as ai_service


class ExamService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_bank_questions(self, topic_id: int, num_questions: int) -> list[dict]:
        """Pull random questions from the question bank for a topic."""
        # Get total available
        count_result = await self.db.execute(
            select(func.count()).where(QuestionBank.topic_id == topic_id)
        )
        total = count_result.scalar_one()
        if total == 0:
            return []

        # Fetch all for the topic, then sample randomly in Python
        result = await self.db.execute(
            select(QuestionBank).where(QuestionBank.topic_id == topic_id)
        )
        bank_items = list(result.scalars().all())
        sample = random.sample(bank_items, min(num_questions, len(bank_items)))
        random.shuffle(sample)

        return [
            {
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
            }
            for q in sample
        ]

    async def generate_exam(self, topic_id: int, num_questions: int) -> ExamSession:
        """Generate exam from question bank (instant); fall back to AI if bank is short."""
        topic = await self.db.get(GrammarTopic, topic_id)
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")

        # Try question bank first
        raw_questions = await self._get_bank_questions(topic_id, num_questions)

        # If bank doesn't have enough, top up with AI-generated questions
        if len(raw_questions) < num_questions:
            ai_count = num_questions - len(raw_questions)
            ai_questions = await ai_service.generate_questions(topic.name, ai_count)
            raw_questions.extend(ai_questions)

        # Persist exam session
        session = ExamSession(
            topic_id=topic_id,
            topic=topic.name,
            num_questions=num_questions,
            total=num_questions,
            status="in_progress",
        )
        self.db.add(session)
        await self.db.flush()

        # Persist questions
        for idx, q in enumerate(raw_questions, start=1):
            question = Question(
                session_id=session.id,
                question_number=idx,
                question_text=q["question_text"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                # Pre-fill explanation from bank; AI questions won't have it yet
                explanation=q.get("explanation"),
            )
            self.db.add(question)

        await self.db.flush()
        await self.db.refresh(session)

        result = await self.db.execute(
            select(ExamSession)
            .options(selectinload(ExamSession.questions))
            .where(ExamSession.id == session.id)
        )
        return result.scalar_one()

    async def submit_exam(self, session_id: int, answers: dict[int, str]) -> ExamSession:
        """Grade exam: save user answers, call OpenAI for explanations, update records."""
        result = await self.db.execute(
            select(ExamSession)
            .options(selectinload(ExamSession.questions))
            .where(ExamSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise LookupError(f"Session {session_id} not found")
        if session.status == "completed":
            raise ValueError("Exam already submitted")

        # Save user answers
        for question in session.questions:
            question.user_answer = answers.get(question.id)

        # Build grading payload for OpenAI
        questions_payload = [
            {
                "question_id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "user_answer": q.user_answer or "No answer",
            }
            for q in session.questions
        ]

        grading_results = await ai_service.grade_answers(questions_payload)

        # Map results by question_id
        results_by_id = {r["question_id"]: r for r in grading_results}

        score = 0
        for question in session.questions:
            graded = results_by_id.get(question.id, {})
            question.is_correct = graded.get("is_correct", False)
            question.explanation = graded.get("explanation", "")
            if question.is_correct:
                score += 1

        # Update session
        session.score = score
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

        await self.db.flush()

        # Reload fresh
        result = await self.db.execute(
            select(ExamSession)
            .options(selectinload(ExamSession.questions))
            .where(ExamSession.id == session_id)
        )
        return result.scalar_one()

    async def get_history(self, limit: int = 20, offset: int = 0) -> list[ExamSession]:
        """Fetch past sessions ordered newest first."""
        result = await self.db.execute(
            select(ExamSession)
            .order_by(ExamSession.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_session(self, session_id: int) -> ExamSession:
        """Fetch a single session with all questions."""
        result = await self.db.execute(
            select(ExamSession)
            .options(selectinload(ExamSession.questions))
            .where(ExamSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError(f"Session {session_id} not found")
        return session

    async def get_review(self, session_id: int) -> list[Question]:
        """Fetch only incorrectly answered questions for review."""
        result = await self.db.execute(
            select(Question)
            .where(Question.session_id == session_id, Question.is_correct == False)  # noqa: E712
            .order_by(Question.question_number)
        )
        return list(result.scalars().all())
