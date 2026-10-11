"""
Application Configuration Module.

Loads and validates environment variables and application runtime settings
using Pydantic BaseSettings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global system configuration settings."""

    PROJECT_NAME: str = "AI-Powered Personal Productivity Suite"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration (Defaults to SQLite for portable local execution; supports PostgreSQL)
    DATABASE_URL: str = "sqlite:///./productivity_suite.db"
    DB_ECHO: bool = False
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # AI Inference Settings
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.75
    DEFAULT_SCHEDULE_SLOT_DURATION_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

