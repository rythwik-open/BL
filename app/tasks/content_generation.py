"""
Celery tasks for content generation.
"""

from celery import current_app as celery_app
from app.services.content_generator import ContentGeneratorService
from app.services.image_generator import ImageGeneratorService


@celery_app.task
def generate_content_task():
    """Background task for content generation."""
    # TODO: Implement automated content generation
    print("Content generation task executed")
    return "Content generation completed"


@celery_app.task
def generate_image_task(content_id: str):
    """Background task for image generation."""
    # TODO: Implement automated image generation
    print(f"Image generation task executed for content {content_id}")
    return f"Image generated for content {content_id}"