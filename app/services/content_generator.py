"""
AI-powered content generation service with Based Labs brand voice.
"""

from typing import Dict, Any, Optional
import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.models.trend_opportunity import TrendOpportunity
from app.models.generated_content import GeneratedContent


class ContentGeneratorService:
    """Service for generating content using AI with brand voice consistency."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.provocative_level = settings.BRAND_PROVOCATIVE_LEVEL
        
        # Based Labs hook formulas
        self.hook_formulas = [
            "You're waiting for permission that will never come",
            "This rule made sense in 1950. It's destroying you in 2025",
            "Everyone does X, but here's why Y works better",
            "If [system] can replace you, it's not your fault—it's the system you were trained for",
        ]
    
    async def generate_content(
        self, 
        opportunity: TrendOpportunity,
        content_type: Optional[str] = None
    ) -> GeneratedContent:
        """Generate content from a trend opportunity."""
        
        # Determine content type if not specified
        if not content_type:
            content_type = self._determine_content_type(opportunity)
        
        # Generate content using AI
        content_text = await self._generate_text(opportunity, content_type)
        
        # Validate content quality
        if not self._validate_content(content_text):
            # Regenerate if quality check fails
            content_text = await self._generate_text(opportunity, content_type)
        
        return GeneratedContent(
            trend_opportunity_id=opportunity.id,
            content_type=content_type,
            text=content_text,
            platform="instagram",  # Default platform
            status="generated",
        )
    
    def _determine_content_type(self, opportunity: TrendOpportunity) -> str:
        """Determine content type based on opportunity characteristics."""
        # Simple logic based on description length
        desc_length = len(opportunity.description)
        
        if desc_length < 100:
            return "quote_minimal"
        elif desc_length < 800:
            return "long_form"
        else:
            return "carousel_series"
    
    async def _generate_text(self, opportunity: TrendOpportunity, content_type: str) -> str:
        """Generate text content using OpenAI."""
        
        system_prompt = self._build_system_prompt(content_type)
        user_prompt = self._build_user_prompt(opportunity)
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=500,
        )
        
        return response.choices[0].message.content.strip()
    
    def _build_system_prompt(self, content_type: str) -> str:
        """Build system prompt with Based Labs brand voice."""
        base_prompt = f"""
        You are a content creator for Based Labs, generating {content_type} content.
        
        Brand Voice:
        - Provocative level: {self.provocative_level}/10
        - Challenge systems and structures, not individuals
        - Direct, confident, slightly rebellious, empathetic
        - Focus on agency over permission, system inefficiencies, gatekeeping
        
        Content Requirements:
        - Clear value proposition for the reader
        - Specific next action or call-to-action
        - Connection to Based Labs philosophy (agency, systems, decentralization)
        
        Hook Formulas to Use:
        {chr(10).join(f'- {hook}' for hook in self.hook_formulas)}
        """
        
        if content_type == "quote_minimal":
            base_prompt += "\nKeep under 100 characters. Focus on a single powerful insight."
        elif content_type == "long_form":
            base_prompt += "\nKeep between 100-800 characters. Explain a framework or concept."
        else:
            base_prompt += "\nCreate multi-slide content over 800 characters."
        
        return base_prompt
    
    def _build_user_prompt(self, opportunity: TrendOpportunity) -> str:
        """Build user prompt from trend opportunity."""
        return f"""
        Create content based on this trend opportunity:
        
        Title: {opportunity.title}
        Description: {opportunity.description}
        Source: {opportunity.source}
        
        Focus on:
        - What system or rule is causing friction?
        - Who benefits from the current system?
        - How could individuals work around this?
        - What would a decentralized alternative look like?
        """
    
    def _validate_content(self, content: str) -> bool:
        """Validate content against Based Labs quality standards."""
        # Basic validation checks
        if len(content.strip()) < 10:
            return False
        
        # Check for value proposition indicators
        value_indicators = ["you", "your", "how to", "why", "what", "when"]
        has_value = any(indicator in content.lower() for indicator in value_indicators)
        
        # Check for call-to-action indicators
        cta_indicators = ["?", "what", "how", "which", "try", "start", "stop"]
        has_cta = any(indicator in content.lower() for indicator in cta_indicators)
        
        return has_value and has_cta