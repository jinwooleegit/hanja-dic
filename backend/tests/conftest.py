import pytest
import os
import logging
from typing import Generator, Dict, Any
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.base_class import Base
from app.models.hanja import Hanja  # Hanja 모델 불러오기

# 테스트용 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 테스트용 엔진 생성
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# 테스트용 세션 팩토리
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def db_engine():
    # 테스트 전에 테이블 생성
    Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    # 테스트 후 테이블 삭제
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    # FastAPI의 의존성 주입 오버라이드
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # 테스트 데이터 추가
    test_hanja = Hanja(
        id=1,
        traditional="道",
        simplified="道",
        meaning="길, 도리, 방법",
        korean_pronunciation="도",
        chinese_pronunciation="dào",
        stroke_count=12,
        radical="辶",
        frequency=750,
        examples="道路(도로): 길, 도로"
    )
    db_session.add(test_hanja)
    db_session.commit()
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 테스트 후 의존성 주입 원복
    app.dependency_overrides.clear() 