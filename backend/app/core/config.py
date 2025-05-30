import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings#, AnyUrl, validator
from pydantic import AnyUrl, validator


class Settings(BaseSettings):
    # Application Config
    APP_NAME: str = "Polyglot API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Database Config (SQLite)
    DATABASE_URL: str = "sqlite:///./polyglot.db"
    SYNC_DATABASE_URL: Optional[str] = None
    
    # SQLite-specific settings
    SQLITE_DB_PATH: Path = Path("sqlite.db")
    
    # Whisper Config
    WHISPER_MODEL: str = "base"  # Possible values: tiny, base, small, medium, large
    
    # OCR Config
    OCR_DEFAULT_LANGUAGES: list[str] = ["en"]
    
    # File Storage
    UPLOAD_DIR: Path = Path("uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    class Config:
        case_sensitive = True
        env_file = ".env"
    
    @validator("DATABASE_URL", pre=True)
    def set_sqlite_database_url(cls, v: Optional[str], values: dict[str, any]) -> str:
        if v is not None:
            return v
        return f"sqlite:///{values.get('SQLITE_DB_PATH', 'polyglot.db')}"
    
    @validator("SYNC_DATABASE_URL", pre=True)
    def set_sync_database_url(cls, v: Optional[str], values: dict[str, any]) -> str:
        if v is not None:
            return v
        return values["DATABASE_URL"].replace("sqlite:///", "sqlite:///")
    
    @validator("UPLOAD_DIR")
    def create_upload_dir(cls, v: Path) -> Path:
        v.mkdir(exist_ok=True, parents=True)
        return v
    
    @validator("SQLITE_DB_PATH")
    def create_sqlite_parent_dir(cls, v: Path) -> Path:
        v.parent.mkdir(exist_ok=True, parents=True)
        return v


settings = Settings()


# Database setup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite requires this for foreign key support
sqlite_engine_args = {
    "connect_args": {"check_same_thread": False},
    "echo": settings.DEBUG
}

engine = create_engine(
    settings.SYNC_DATABASE_URL,
    **sqlite_engine_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()