"""
Comment model for community engagement tracking.
"""

from datetime import datetime
from sqlalchemy import String, Text, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Comment(BaseModel):
    """Model for tracking comments and community interactions."""
    
    __tablename__ = "comments"
    
    post_id: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )  # question, feedback, spam, engagement
    sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)