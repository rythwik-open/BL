"""
Application configuration settings.
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/content_pipeline"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Social Media APIs
    INSTAGRAM_ACCESS_TOKEN: str = ""
    LINKEDIN_ACCESS_TOKEN: str = ""
    
    # News APIs
    NEWS_API_KEY: str = ""
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    
    # Application
    DEBUG: bool = False
    SECRET_KEY: str
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Based Labs Brand Settings
    BRAND_PROVOCATIVE_LEVEL: int = 7
    DEFAULT_POSTING_TIMES_INSTAGRAM: List[str] = ["11:00", "14:00", "17:00"]
    DEFAULT_POSTING_TIMES_LINKEDIN: List[str] = ["08:00", "12:00", "18:00"]
    
    class Config:
        env_file = ".env"


settings = Settings()