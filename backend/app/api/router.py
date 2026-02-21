from fastapi import APIRouter

from app.api import analytics, exams, topics

api_router = APIRouter(prefix="/api")
api_router.include_router(topics.router)
api_router.include_router(exams.router)
api_router.include_router(analytics.router)
