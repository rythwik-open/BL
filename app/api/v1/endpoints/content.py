"""
Content generation and management API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import tempfile
import os

from app.core.database import get_db
from app.services.content_generator import ContentGeneratorService
from app.services.image_generator import ImageGeneratorService
from app.models.trend_opportunity import TrendOpportunity
from app.models.generated_content import GeneratedContent
from app.schemas.content import ContentGenerationRequest, ContentResponse

router = APIRouter()


@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentGenerationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate content from a trend opportunity."""
    # Get trend opportunity
    trend = await db.get(TrendOpportunity, request.trend_opportunity_id)
    if not trend:
        raise HTTPException(status_code=404, detail="Trend opportunity not found")
    
    # Generate content
    content_service = ContentGeneratorService()
    generated_content = await content_service.generate_content(
        trend, 
        request.content_type
    )
    
    # Save to database
    db.add(generated_content)
    await db.commit()
    await db.refresh(generated_content)
    
    return ContentResponse.from_orm(generated_content)


@router.post("/generate-image/{content_id}")
async def generate_image(
    content_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Generate image for content."""
    # Get content
    content = await db.get(GeneratedContent, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Generate image
    image_service = ImageGeneratorService()
    image = await image_service.generate_image_for_content(content)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        image.save(tmp_file.name, "PNG")
        
        return FileResponse(
            tmp_file.name,
            media_type="image/png",
            filename=f"content_{content_id}.png"
        )


@router.get("/", response_model=List[ContentResponse])
async def get_content(
    status: str = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get generated content."""
    query = db.query(GeneratedContent)
    
    if status:
        query = query.filter(GeneratedContent.status == status)
    
    content = await query.limit(limit).all()
    return [ContentResponse.from_orm(c) for c in content]


@router.put("/{content_id}/approve")
async def approve_content(
    content_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Approve content for publishing."""
    content = await db.get(GeneratedContent, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.status = "approved"
    await db.commit()
    
    return {"message": "Content approved"}


@router.put("/{content_id}/reject")
async def reject_content(
    content_id: str,
    feedback: str = "",
    db: AsyncSession = Depends(get_db)
):
    """Reject content with feedback."""
    content = await db.get(GeneratedContent, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.status = "rejected"
    # TODO: Store feedback for learning
    await db.commit()
    
    return {"message": "Content rejected", "feedback": feedback}