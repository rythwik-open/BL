"""
Trend monitoring service for identifying content opportunities.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod

from app.models.trend_opportunity import TrendOpportunity


class TrendSource(ABC):
    """Abstract base class for trend sources."""
    
    @abstractmethod
    async def fetch_trends(self) -> List[Dict[str, Any]]:
        """Fetch trends from the source."""
        pass


class TrendMonitorService:
    """Service for monitoring trends and identifying content opportunities."""
    
    def __init__(self):
        self.sources: List[TrendSource] = []
        self.scoring_weights = {
            "brand_alignment": 0.4,
            "timeliness": 0.3,
            "engagement_potential": 0.2,
            "uniqueness": 0.1,
        }
    
    def add_source(self, source: TrendSource):
        """Add a trend source."""
        self.sources.append(source)
    
    async def monitor_trends(self) -> List[TrendOpportunity]:
        """Monitor all sources and return scored opportunities."""
        all_trends = []
        
        for source in self.sources:
            trends = await source.fetch_trends()
            all_trends.extend(trends)
        
        # Score and filter trends
        opportunities = []
        for trend in all_trends:
            score = self._score_trend(trend)
            if score > 0.6:  # Minimum threshold
                opportunity = self._create_opportunity(trend, score)
                opportunities.append(opportunity)
        
        # Sort by score and return top opportunities
        opportunities.sort(key=lambda x: x.score, reverse=True)
        return opportunities[:10]
    
    def _score_trend(self, trend: Dict[str, Any]) -> float:
        """Score a trend based on Based Labs criteria."""
        # Placeholder scoring logic
        # TODO: Implement actual scoring based on:
        # - System friction points
        # - Permission barriers
        # - Gatekeeping mechanisms
        # - Individual workarounds
        return 0.7
    
    def _create_opportunity(self, trend: Dict[str, Any], score: float) -> TrendOpportunity:
        """Create a TrendOpportunity from trend data."""
        return TrendOpportunity(
            title=trend.get("title", ""),
            description=trend.get("description", ""),
            source=trend.get("source", ""),
            url=trend.get("url", ""),
            score=score,
            metadata=trend,
        )