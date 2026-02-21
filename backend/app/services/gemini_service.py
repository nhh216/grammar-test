"""Google Gemini integration for question generation and answer grading."""

import json
import logging

import google.generativeai as genai

from app.core.config import settings
from app.core.prompts import (
    GENERATION_SYSTEM_PROMPT,
    GENERATION_USER_PROMPT,
    GRADING_SYSTEM_PROMPT,
    GRADING_USER_PROMPT,
)

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL

    def _get_model(self, system_prompt: str) -> genai.GenerativeModel:
        return genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt,
        )

    async def generate_questions(self, topic: str, num_questions: int) -> list[dict]:
        """Call Gemini to generate TOEIC grammar questions for a topic."""
        user_prompt = GENERATION_USER_PROMPT.format(
            num_questions=num_questions,
            topic=topic,
        )
        response = await self._call_gemini(GENERATION_SYSTEM_PROMPT, user_prompt)
        data = self._parse_json(response)
        questions = data.get("questions", [])
        if not questions or len(questions) != num_questions:
            raise ValueError(
                f"Gemini returned {len(questions)} questions, expected {num_questions}"
            )
        return questions

    async def grade_answers(self, questions_with_answers: list[dict]) -> list[dict]:
        """Call Gemini to grade submitted answers and produce per-question explanations."""
        formatted = json.dumps(questions_with_answers, ensure_ascii=False, indent=2)
        user_prompt = GRADING_USER_PROMPT.format(questions_with_answers=formatted)
        response = await self._call_gemini(GRADING_SYSTEM_PROMPT, user_prompt)
        data = self._parse_json(response)
        return data.get("results", [])

    async def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        """Make a single Gemini chat completion call with JSON mode."""
        try:
            model = self._get_model(system_prompt)
            response = await model.generate_content_async(
                user_prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                ),
            )
            return response.text or ""
        except Exception as exc:
            logger.error("Gemini API call failed: %s", exc)
            raise RuntimeError(f"Gemini API error: {exc}") from exc

    def _parse_json(self, raw: str) -> dict:
        """Parse JSON response; raise ValueError on malformed output."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse Gemini JSON response: %s", raw[:200])
            raise ValueError(f"Invalid JSON from Gemini: {exc}") from exc


# Singleton instance
gemini_service = GeminiService()
