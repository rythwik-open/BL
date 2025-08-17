"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import trends, content, review, analytics

api_router = APIRouter()

api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(review.router, prefix="/review", tags=["review"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])