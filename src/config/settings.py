"""
Application configuration and settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AniList GPT"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # AniList OAuth
    ANILIST_CLIENT_ID: str = ""
    ANILIST_CLIENT_SECRET: str = ""
    ANILIST_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/anilist_gpt"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Cache
    CACHE_TTL_DEFAULT: int = 3600
    CACHE_TTL_TRENDING: int = 1800
    CACHE_TTL_USER_LIST: int = 300

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 90
    RATE_LIMIT_WINDOW: int = 60

    # MCP
    MCP_TRANSPORT: str = "sse"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Observability
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
