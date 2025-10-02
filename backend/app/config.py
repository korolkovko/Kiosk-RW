from functools import lru_cache
from typing import List
from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Загружаем переменные из .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(env_path),
        env_file_encoding="utf-8",
        extra="ignore"  # ← 🔧 позволяет игнорировать лишние переменные в .env
    )

    # Application Settings
    PROJECT_NAME: str = "KIOSK Application"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., description="Secret key for the application")

    # Database Settings
    DATABASE_URL: str = Field(..., description="Database connection URL")

    # Redis Settings
    REDIS_URL: str = Field(..., description="Redis connection URL")

    # Authentication Settings
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Settings (disabled for Railway deployment)
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_PATH: str = "./uploads"  # Not used in Railway

    # Logging Settings (Railway uses stdout/stderr)
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs/app.log"  # Not used in Railway

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]

    # External Integrations
    POS_API_URL: str = ""
    POS_API_KEY: str = ""
    PAYMENT_API_URL: str = ""
    PAYMENT_API_KEY: str = ""


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print("✅ Loaded .env — SECRET_KEY:", os.getenv("SECRET_KEY"))
    return settings