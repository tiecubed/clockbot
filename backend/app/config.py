"""Backend configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    DATABASE_URL: str = "sqlite:///./data/timetracker.db"
    SHARED_TOKEN: str = "change-me-in-production"
    HEALTH_THRESHOLD_SECONDS: int = 90
    SCREENSHOT_DIR: str = "./screenshots"
    SCREENSHOT_MAX_WIDTH: int = 1920
    SCREENSHOT_QUALITY: int = 70
    DISCORD_CLIENT_ID: Optional[str] = None
    DISCORD_CLIENT_SECRET: Optional[str] = None
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
