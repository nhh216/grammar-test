"""Analytics service: aggregate user performance stats per topic."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exam_session import ExamSession
from app.models.grammar_topic import GrammarTopic
from app.models.question import Question
from app.schemas.analytics import PerformanceResponse, TopicPerformance


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_performance(self) -> PerformanceResponse:
        """Aggregate per-topic performance stats from completed exam sessions."""
        # Fetch all topics for full coverage (including untested ones)
        topics_result = await self.db.execute(select(GrammarTopic).order_by(GrammarTopic.name))
        all_topics = list(topics_result.scalars().all())

        # Fetch all completed sessions
        sessions_result = await self.db.execute(
            select(ExamSession)
            .where(ExamSession.status == "completed")
            .order_by(ExamSession.topic_id, ExamSession.completed_at)
        )
        sessions = list(sessions_result.scalars().all())

        # Group sessions by topic_id
        sessions_by_topic: dict[int, list[ExamSession]] = {}
        for s in sessions:
            sessions_by_topic.setdefault(s.topic_id, []).append(s)

        # Aggregate per-topic correct answer counts from questions table
        correct_counts_result = await self.db.execute(
            select(
                ExamSession.topic_id,
                func.count(Question.id).label("total"),
                func.sum(func.cast(Question.is_correct, type_=__import__("sqlalchemy").Integer)).label("correct"),
            )
            .join(Question, Question.session_id == ExamSession.id)
            .where(ExamSession.status == "completed", Question.is_correct.isnot(None))
            .group_by(ExamSession.topic_id)
        )
        question_stats = {row.topic_id: row for row in correct_counts_result}

        topic_performances: list[TopicPerformance] = []
        total_sessions = 0
        total_questions_answered = 0
        total_correct_global = 0

        for topic in all_topics:
            topic_sessions = sessions_by_topic.get(topic.id, [])
            n = len(topic_sessions)
            total_sessions += n

            q_stats = question_stats.get(topic.id)
            total_q = int(q_stats.total) if q_stats else 0
            total_c = int(q_stats.correct or 0) if q_stats else 0
            total_questions_answered += total_q
            total_correct_global += total_c

            # Recent score percentages (last 5 sessions)
            recent_scores = [
                round((s.score / s.total * 100) if s.total else 0, 1)
                for s in topic_sessions[-5:]
            ]

            # Average score % per session
            avg_score_pct = round(sum(recent_scores) / len(recent_scores), 1) if recent_scores else 0.0

            # Overall accuracy for this topic
            accuracy_pct = round(total_c / total_q * 100, 1) if total_q > 0 else 0.0

            # Classify level
            level = _classify_level(accuracy_pct, n)

            # Trend: compare first half vs second half of recent scores
            trend = _compute_trend(recent_scores)

            topic_performances.append(TopicPerformance(
                topic_id=topic.id,
                topic_name=topic.name,
                slug=topic.slug,
                sessions_completed=n,
                total_questions=total_q,
                total_correct=total_c,
                accuracy_pct=accuracy_pct,
                avg_score_pct=avg_score_pct,
                level=level,
                trend=trend,
                recent_scores=recent_scores,
            ))

        overall_accuracy = (
            round(total_correct_global / total_questions_answered * 100, 1)
            if total_questions_answered > 0 else 0.0
        )

        return PerformanceResponse(
            topics=topic_performances,
            total_sessions=total_sessions,
            total_questions_answered=total_questions_answered,
            overall_accuracy=overall_accuracy,
            has_data=total_sessions > 0,
        )


def _classify_level(accuracy_pct: float, session_count: int) -> str:
    if session_count == 0:
        return "untested"
    if accuracy_pct >= 80:
        return "strong"
    if accuracy_pct >= 60:
        return "moderate"
    return "weak"


def _compute_trend(scores: list[float]) -> str:
    if len(scores) < 2:
        return "new"
    if len(scores) == 2:
        diff = scores[-1] - scores[0]
    else:
        mid = len(scores) // 2
        first_avg = sum(scores[:mid]) / mid
        second_avg = sum(scores[mid:]) / len(scores[mid:])
        diff = second_avg - first_avg

    if diff >= 5:
        return "improving"
    if diff <= -5:
        return "declining"
    return "stable"
