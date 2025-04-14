from pydantic_settings import BaseSettings
from typing import Optional
import os
from sqlalchemy.orm import Session

class Settings(BaseSettings):
    PROJECT_NAME: str = "HanjaDB"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 데이터베이스 설정
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "hanja_db")
    
    @property
    def DATABASE_URL(self) -> str:
        if os.getenv("TESTING") == "true":
            return "sqlite:///:memory:"
        return os.getenv(
            "DATABASE_URL",
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    # Redis 설정
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )
    CACHE_TTL: int = 3600  # 1시간
    
    # 테스트 모드 확인
    def is_testing(self) -> bool:
        return "sqlite" in self.DATABASE_URL

    def get_db(self) -> Session:
        from app.db.session import SessionLocal
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings() 