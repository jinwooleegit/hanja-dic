import pytest
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# 테스트용 환경 변수 설정
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def setup_test_db():
    """테스트 DB 설정"""
    # 필요한 모듈을 내부에서 임포트 (순환 참조 방지)
    from app.db.base import Base
    
    # 인메모리 SQLite DB 설정
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 테이블 목록 확인
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"테이블 생성 완료: {tables}")
    
    return engine

@pytest.fixture
def db_session(setup_test_db):
    """테스트용 DB 세션"""
    connection = setup_test_db.connect()
    transaction = connection.begin()
    
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    
    # 외래 키 제약 조건 활성화
    session.execute(text("PRAGMA foreign_keys=ON"))
    session.commit()
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    """테스트 클라이언트"""
    from app.main import app
    from app.db.session import get_db
    
    # 의존성 오버라이드
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 의존성 복원
    app.dependency_overrides.clear() 