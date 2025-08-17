"""
Generated content model for AI-created content pieces.
"""

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class GeneratedContent(BaseModel):
    """Model for AI-generated content pieces."""
    
    __tablename__ = "generated_content"
    
    trend_opportunity_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("trend_opportunities.id"),
        nullable=False
    )
    content_type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )  # quote_minimal, long_form, carousel_series
    text: Mapped[str] = mapped_column(Text, nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), 
        default="generated",
        nullable=False
    )  # generated, approved, rejected, published
    package_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("content_packages.id"),
        nullable=True
    )
    
    # Relationships
    trend_opportunity = relationship("TrendOpportunity", back_populates="generated_content")
    content_package = relationship("ContentPackage", back_populates="generated_content")


# Add back reference to TrendOpportunity
from app.models.trend_opportunity import TrendOpportunity
TrendOpportunity.generated_content = relationship("GeneratedContent", back_populates="trend_opportunity")