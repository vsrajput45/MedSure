import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

    PROJECT_NAME: str = "MEDSURE"
    TAGLINE: str = "Know the Fair Price. Verify Every Bill."
    HINDI_TAGLINE: str = "सही दाम जानो। हर बिल जांचो।"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "medsure-super-secret-production-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Database - Default to SQLite for zero-friction setup, PostgreSQL ready
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'medsure.db'}")
    
    # Upload limits & storage
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    REPORTS_DIR: Path = BASE_DIR / "generated_reports"
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: list[str] = [".pdf", ".png", ".jpg", ".jpeg"]
    
    # External AI / LLM optional integration
    AI_API_KEY: str | None = os.getenv("AI_API_KEY", None)
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock_rule_based")
    
    # Demo configuration
    DEMO_MODE_ENABLED: bool = True

settings = Settings()

# Ensure required private directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
