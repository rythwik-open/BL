"""
Post metrics model for tracking social media performance.
"""

from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class PostMetrics(BaseModel):
    """Model for tracking social media post performance metrics."""
    
    __tablename__ = "post_metrics"
    
    post_id: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    saves: Mapped[int] = mapped_column(Integer, default=0)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    reach: Mapped[int] = mapped_column(Integer, default=0)
    click_through_rate: Mapped[float] = mapped_column(Float, default=0.0)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)