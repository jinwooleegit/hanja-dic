from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# SQLite 사용 시 추가 설정
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 모델 클래스 생성
Base = declarative_base()

# 모든 모델 임포트
from app.models.hanja import Hanja

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 의존성 주입은 session.py에서 관리
from app.db.session import get_db 