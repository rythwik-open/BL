"""
Trend opportunity model for storing identified content opportunities.
"""

from typing import Dict, Any
from sqlalchemy import String, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class TrendOpportunity(BaseModel):
    """Model for trend opportunities identified by the monitoring system."""
    
    __tablename__ = "trend_opportunities"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(
        String(20), 
        default="identified",
        nullable=False
    )  # identified, processed, archived