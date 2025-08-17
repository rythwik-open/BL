"""
Trend monitoring API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.trend_monitor import TrendMonitorService
from app.schemas.trend_opportunity import TrendOpportunityResponse

router = APIRouter()


@router.get("/", response_model=List[TrendOpportunityResponse])
async def get_trends(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get current trend opportunities."""
    trend_service = TrendMonitorService()
    opportunities = await trend_service.monitor_trends()
    return opportunities[:limit]


@router.post("/monitor")
async def trigger_trend_monitoring(
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger trend monitoring."""
    trend_service = TrendMonitorService()
    opportunities = await trend_service.monitor_trends()
    return {"message": f"Found {len(opportunities)} new opportunities"}