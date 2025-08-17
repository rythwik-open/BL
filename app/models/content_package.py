"""
Content package model for grouping related content pieces.
"""

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import BaseModel


class ContentPackage(BaseModel):
    """Model for content packages that group related content pieces."""
    
    __tablename__ = "content_packages"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), 
        default="draft",
        nullable=False
    )  # draft, review, approved, published, archived
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    generated_content = relationship("GeneratedContent", back_populates="content_package")