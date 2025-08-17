"""
Schemas for trend opportunity data.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel


class TrendOpportunityBase(BaseModel):
    """Base schema for trend opportunities."""
    title: str
    description: str
    source: str
    url: Optional[str] = None
    score: float
    metadata: Dict[str, Any] = {}


class TrendOpportunityCreate(TrendOpportunityBase):
    """Schema for creating trend opportunities."""
    pass


class TrendOpportunityResponse(TrendOpportunityBase):
    """Schema for trend opportunity responses."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True