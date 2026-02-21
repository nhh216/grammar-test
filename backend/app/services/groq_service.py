"""Groq integration for question generation and answer grading."""

import json
import logging

from groq import AsyncGroq

from app.core.config import settings
from app.core.prompts import (
    GENERATION_SYSTEM_PROMPT,
    GENERATION_USER_PROMPT,
    GRADING_SYSTEM_PROMPT,
    GRADING_USER_PROMPT,
    INSIGHTS_SYSTEM_PROMPT,
    INSIGHTS_USER_PROMPT,
)

logger = logging.getLogger(__name__)


class GroqService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_questions(self, topic: str, num_questions: int) -> list[dict]:
        """Call Groq to generate TOEIC grammar questions for a topic."""
        user_prompt = GENERATION_USER_PROMPT.format(
            num_questions=num_questions,
            topic=topic,
        )
        response = await self._call_groq(GENERATION_SYSTEM_PROMPT, user_prompt)
        data = self._parse_json(response)
        questions = data.get("questions", [])
        if not questions or len(questions) != num_questions:
            raise ValueError(
                f"Groq returned {len(questions)} questions, expected {num_questions}"
            )
        return questions

    async def generate_insights(
        self,
        overall_accuracy: float,
        total_sessions: int,
        total_questions: int,
        topic_breakdown: str,
    ) -> dict:
        """Call Groq to generate personalized coaching insights in Vietnamese."""
        user_prompt = INSIGHTS_USER_PROMPT.format(
            overall_accuracy=overall_accuracy,
            total_sessions=total_sessions,
            total_questions=total_questions,
            topic_breakdown=topic_breakdown,
        )
        response = await self._call_groq(INSIGHTS_SYSTEM_PROMPT, user_prompt)
        return self._parse_json(response)

    async def grade_answers(self, questions_with_answers: list[dict]) -> list[dict]:
        """Call Groq to grade submitted answers and produce per-question explanations."""
        formatted = json.dumps(questions_with_answers, ensure_ascii=False, indent=2)
        user_prompt = GRADING_USER_PROMPT.format(questions_with_answers=formatted)
        response = await self._call_groq(GRADING_SYSTEM_PROMPT, user_prompt)
        data = self._parse_json(response)
        return data.get("results", [])

    async def _call_groq(self, system_prompt: str, user_prompt: str) -> str:
        """Make a single Groq chat completion call with JSON mode."""
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
            return completion.choices[0].message.content or ""
        except Exception as exc:
            logger.error("Groq API call failed: %s", exc)
            raise RuntimeError(f"Groq API error: {exc}") from exc

    def _parse_json(self, raw: str) -> dict:
        """Parse JSON response; raise ValueError on malformed output."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse Groq JSON response: %s", raw[:200])
            raise ValueError(f"Invalid JSON from Groq: {exc}") from exc


# Singleton instance
groq_service = GroqService()
