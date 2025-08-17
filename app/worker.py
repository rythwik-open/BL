"""
Celery worker configuration for background tasks.
"""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "content_pipeline",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.trend_monitoring", "app.tasks.content_generation"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "monitor-trends": {
            "task": "app.tasks.trend_monitoring.monitor_trends_task",
            "schedule": 3600.0,  # Run every hour
        },
        "generate-content": {
            "task": "app.tasks.content_generation.generate_content_task", 
            "schedule": 7200.0,  # Run every 2 hours
        },
    },
)