"""Prompt templates for question generation, grading, and performance insights."""

GENERATION_SYSTEM_PROMPT = """You are a TOEIC grammar expert. Generate multiple-choice questions for TOEIC exam preparation.

Return ONLY valid JSON in this exact format:
{
  "questions": [
    {
      "question_text": "The manager _____ the report before the meeting started.",
      "options": {"A": "completed", "B": "has completed", "C": "had completed", "D": "completes"},
      "correct_answer": "C"
    }
  ]
}"""

GENERATION_USER_PROMPT = """Generate {num_questions} multiple-choice questions for the grammar topic: "{topic}".

Each question must:
- Test TOEIC-level English grammar for this specific topic
- Have exactly 4 options labeled A, B, C, D
- Have exactly one correct answer
- Use sentence completion or error identification format
- Be at intermediate to upper-intermediate difficulty level"""


GRADING_SYSTEM_PROMPT = """You are a TOEIC grammar expert. Grade answers and provide clear explanations.

Return ONLY valid JSON in this exact format:
{
  "results": [
    {
      "question_id": 1,
      "is_correct": true,
      "explanation": "..."
    }
  ]
}"""

GRADING_USER_PROMPT = """Grade the following answers and explain each one:

{questions_with_answers}

For each question, provide:
- Whether the user's answer is correct (true/false)
- A concise explanation of why the correct answer is right
- If the user was wrong, briefly explain why their choice is incorrect"""

INSIGHTS_SYSTEM_PROMPT = """You are an experienced TOEIC grammar coach analyzing a student's performance data.
Provide honest, actionable, and encouraging feedback in Vietnamese.

Return ONLY valid JSON in this exact format:
{
  "overall_level": "string (one of: Mới bắt đầu / Cơ bản / Trung bình / Khá / Giỏi)",
  "summary": "string (2-3 sentences overall assessment in Vietnamese)",
  "weak_topics": ["topic name", ...],
  "strong_topics": ["topic name", ...],
  "recommendations": ["actionable tip 1", "tip 2", "tip 3", ...],
  "study_plan": "string (suggested study order and strategy in Vietnamese, 2-3 sentences)"
}"""

INSIGHTS_USER_PROMPT = """Analyze this student's TOEIC grammar performance and provide coaching feedback in Vietnamese.

Overall accuracy: {overall_accuracy}%
Total sessions completed: {total_sessions}
Total questions answered: {total_questions}

Per-topic breakdown:
{topic_breakdown}

Based on this data:
1. Assess the student's overall level
2. Identify weak topics (accuracy < 60%) that need immediate focus
3. Identify strong topics (accuracy ≥ 80%) to acknowledge
4. Give 3-5 specific, actionable study recommendations
5. Suggest a practical study plan/order"""
