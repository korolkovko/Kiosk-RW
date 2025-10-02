from functools import lru_cache
from typing import List
from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Загружаем переменные из .env конкретно для backend-приложения
# По умолчанию используем backend/.env; путь можно переопределить через BACKEND_ENV_FILE
env_path = Path(__file__).resolve().parents[1] / ".env"
env_file = os.getenv("BACKEND_ENV_FILE", str(env_path))
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(env_file),
        env_file_encoding="utf-8",
        extra="ignore"  # ← 🔧 позволяет игнорировать лишние переменные в .env
    )

    HOST: str = Field(default="0.0.0.0", description="Bind address for the FastAPI server")
    PORT: int = Field(default=8000, description="Port for the FastAPI server")

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

    # Refresh token expiry in days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Kiosk Authentication Settings - Extended JWT for self-service kiosks
    KIOSK_JWT_SECRET_KEY: str = Field(default="", description="Kiosk JWT secret key for long-lived tokens")
    KIOSK_JWT_ALGORITHM: str = "HS256"
    KIOSK_ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    KIOSK_REFRESH_TOKEN_EXPIRE_DAYS: int = 90
    KIOSK_JWT_KEY_ID: str = Field(default="kiosk-v1", description="Key identifier for kiosk JWT tokens")

    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_PATH: str = "./uploads"

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs/app.log"

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
    print("✅ Settings loaded from:", env_file)
    print("✅ Loaded .env — SECRET_KEY:", os.getenv("SECRET_KEY"))
    return settings