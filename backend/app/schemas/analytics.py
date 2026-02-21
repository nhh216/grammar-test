"""Schemas for topic performance analytics and AI insights."""

from pydantic import BaseModel


class TopicPerformance(BaseModel):
    topic_id: int
    topic_name: str
    slug: str
    sessions_completed: int
    total_questions: int
    total_correct: int
    accuracy_pct: float          # 0-100
    avg_score_pct: float         # 0-100 (average per session)
    level: str                   # "weak" | "moderate" | "strong" | "untested"
    trend: str                   # "improving" | "declining" | "stable" | "new"
    recent_scores: list[float]   # last ≤5 session score percentages


class PerformanceInsight(BaseModel):
    overall_level: str           # overall rating label
    overall_accuracy: float      # global accuracy across all topics
    summary: str                 # 2-3 sentence overall assessment
    weak_topics: list[str]       # topic names needing focus
    strong_topics: list[str]     # topic names performing well
    recommendations: list[str]   # actionable bullet points (3-5 items)
    study_plan: str              # suggested study order


class PerformanceResponse(BaseModel):
    topics: list[TopicPerformance]
    total_sessions: int
    total_questions_answered: int
    overall_accuracy: float
    has_data: bool
