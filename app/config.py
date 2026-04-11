"""
Application configuration settings.
Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    
    # Application metadata
    APP_NAME: str = "Data Listing API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database configuration
    # SQLite by default for development, PostgreSQL URL can be provided for production
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React/Next.js
        "http://localhost:5173",  # Vite
        "http://localhost:8080",  # Vue
    ]
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-long-random-string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance to avoid reloading on each request.
    Uses LRU cache for performance.
    """
    return Settings()
