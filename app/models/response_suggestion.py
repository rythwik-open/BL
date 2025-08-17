"""
Response suggestion model for community engagement assistance.
"""

from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ResponseSuggestion(BaseModel):
    """Model for AI-generated response suggestions to community interactions."""
    
    __tablename__ = "response_suggestions"
    
    comment_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("comments.id"),
        nullable=False
    )
    suggested_response: Mapped[str] = mapped_column(Text, nullable=False)
    response_type: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )  # educational, engagement, redirect
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    template_used: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relationships
    comment = relationship("Comment", back_populates="response_suggestions")


# Add back reference to Comment
from app.models.comment import Comment
Comment.response_suggestions = relationship("ResponseSuggestion", back_populates="comment")