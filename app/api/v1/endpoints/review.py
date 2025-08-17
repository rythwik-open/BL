"""
Content review and approval API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.content import ContentResponse

router = APIRouter()


@router.get("/queue", response_model=List[ContentResponse])
async def get_review_queue(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get content pending review."""
    # TODO: Implement review queue logic
    return []


@router.get("/dashboard")
async def get_review_dashboard(
    db: AsyncSession = Depends(get_db)
):
    """Get review dashboard data."""
    return {
        "pending_reviews": 0,
        "approved_today": 0,
        "rejected_today": 0,
        "average_review_time": 0
    }