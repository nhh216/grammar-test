from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.grammar_topic import GrammarTopic
from app.schemas.topic import TopicResponse

router = APIRouter(tags=["topics"])


@router.get("/topics", response_model=list[TopicResponse])
async def list_topics(db: AsyncSession = Depends(get_db)):
    """Return all available grammar topics."""
    result = await db.execute(select(GrammarTopic).order_by(GrammarTopic.name))
    return result.scalars().all()
