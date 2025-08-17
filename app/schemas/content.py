"""
Schemas for content generation and management.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ContentGenerationRequest(BaseModel):
    """Schema for content generation requests."""
    trend_opportunity_id: str
    content_type: Optional[str] = None
    platform: str = "instagram"


class ContentResponse(BaseModel):
    """Schema for content responses."""
    id: str
    trend_opportunity_id: str
    content_type: str
    text: str
    platform: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True