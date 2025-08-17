"""
Celery tasks for trend monitoring.
"""

from celery import current_app as celery_app
from app.services.trend_monitor import TrendMonitorService


@celery_app.task
def monitor_trends_task():
    """Background task for trend monitoring."""
    # TODO: Implement automated trend monitoring
    print("Trend monitoring task executed")
    return "Trend monitoring completed"