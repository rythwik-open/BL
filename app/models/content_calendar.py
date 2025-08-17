"""
Content calendar model for planning and scheduling content.
"""

from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ContentCalendarEntry(BaseModel):
    """Model for content calendar entries and scheduling."""
    
    __tablename__ = "content_calendar"
    
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    content_theme: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )  # system_critique, framework, community_spotlight
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), 
        default="planned",
        nullable=False
    )  # planned, generated, approved, published
    content_pillar: Mapped[str] = mapped_column(String(50), nullable=True)
    package_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("content_packages.id"),
        nullable=True
    )
    
    # Relationships
    package = relationship("ContentPackage", back_populates="calendar_entries")


# Add back reference to ContentPackage
from app.models.content_package import ContentPackage
ContentPackage.calendar_entries = relationship("ContentCalendarEntry", back_populates="package")