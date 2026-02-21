"""Analytics API: topic performance stats and AI coaching insights."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.analytics import PerformanceInsight, PerformanceResponse
from app.services.analytics_service import AnalyticsService
from app.services.groq_service import groq_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/performance", response_model=PerformanceResponse)
async def get_performance(db: AsyncSession = Depends(get_db)):
    """Return per-topic performance stats aggregated from completed sessions."""
    service = AnalyticsService(db)
    return await service.get_performance()


@router.get("/insights", response_model=PerformanceInsight)
async def get_insights(db: AsyncSession = Depends(get_db)):
    """Generate AI coaching feedback based on current performance data."""
    service = AnalyticsService(db)
    perf = await service.get_performance()

    if not perf.has_data:
        return PerformanceInsight(
            overall_level="Chưa có dữ liệu",
            overall_accuracy=0.0,
            summary="Bạn chưa hoàn thành bài thi nào. Hãy làm ít nhất một bài để nhận đánh giá!",
            weak_topics=[],
            strong_topics=[],
            recommendations=[
                "Hãy bắt đầu với chủ đề bạn cảm thấy tự tin nhất.",
                "Mỗi bài thi khoảng 10 câu là đủ để thu thập dữ liệu đánh giá.",
            ],
            study_plan="Làm bài thi trên nhiều chủ đề khác nhau để hệ thống có thể phân tích điểm mạnh và điểm yếu của bạn.",
        )

    # Build topic summary text for AI prompt
    lines = []
    for t in perf.topics:
        if t.sessions_completed == 0:
            lines.append(f"- {t.topic_name}: chưa làm bài")
        else:
            lines.append(
                f"- {t.topic_name}: {t.sessions_completed} bài, "
                f"độ chính xác {t.accuracy_pct}% ({t.level}), "
                f"xu hướng: {t.trend}"
            )
    topic_breakdown = "\n".join(lines)

    raw = await groq_service.generate_insights(
        overall_accuracy=perf.overall_accuracy,
        total_sessions=perf.total_sessions,
        total_questions=perf.total_questions_answered,
        topic_breakdown=topic_breakdown,
    )

    return PerformanceInsight(
        overall_level=raw.get("overall_level", "Trung bình"),
        overall_accuracy=perf.overall_accuracy,
        summary=raw.get("summary", ""),
        weak_topics=raw.get("weak_topics", []),
        strong_topics=raw.get("strong_topics", []),
        recommendations=raw.get("recommendations", []),
        study_plan=raw.get("study_plan", ""),
    )
