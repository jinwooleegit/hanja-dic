from typing import Generator
from sqlalchemy.orm import Session
from app.db.base import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션을 제공하는 의존성 함수입니다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 