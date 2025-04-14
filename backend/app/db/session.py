from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# 데이터베이스 연결 설정
def get_connection_args():
    """데이터베이스 유형에 따른 연결 인자 설정"""
    if "sqlite" in settings.DATABASE_URL:
        return {
            "check_same_thread": False,
            "isolation_level": "SERIALIZABLE"
        }
    elif "postgresql" in settings.DATABASE_URL:
        return {
            "connect_timeout": 10,
            "client_encoding": "utf8"
        }
    return {}

# 엔진 생성
if "sqlite" in settings.DATABASE_URL:
    # SQLite용 엔진 설정
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=get_connection_args(),
        echo=settings.is_testing()  # 테스트 환경에서만 SQL 로깅
    )
    
    # SQLite 최적화
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging 모드
        cursor.execute("PRAGMA synchronous=NORMAL")  # 동기화 모드 조정
        cursor.execute("PRAGMA cache_size=10000")   # 캐시 크기 증가
        cursor.execute("PRAGMA foreign_keys=ON")    # 외래 키 제약 조건 활성화
        cursor.close()
else:
    # PostgreSQL/MySQL 등 다른 DB용 엔진 설정
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # 연결이 유효한지 확인
        pool_recycle=3600,   # 1시간마다 연결 재활용
        pool_size=5,         # 연결 풀 크기
        max_overflow=10,     # 최대 추가 연결 수
        connect_args=get_connection_args(),
        echo=settings.is_testing()  # 테스트 환경에서만 SQL 로깅
    )

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 수동 세션 관리를 위한 컨텍스트 매니저
@contextmanager
def get_db_session():
    """수동 세션 관리를 위한 컨텍스트 매니저

    Example:
        with get_db_session() as session:
            results = session.query(Model).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"데이터베이스 세션 오류: {e}")
        raise
    finally:
        session.close()

# FastAPI 의존성 주입을 위한 함수
def get_db():
    """FastAPI 의존성 주입을 위한 함수

    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 오류: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# 재시도 로직이 있는 데이터베이스 작업 실행
def execute_with_retry(func, max_retries=3, retry_delay=0.5):
    """데이터베이스 작업을 재시도 로직과 함께 실행

    Args:
        func: 실행할 함수 (세션을 인자로 받아야 함)
        max_retries: 최대 재시도 횟수
        retry_delay: 재시도 간 지연시간(초)

    Returns:
        함수 실행 결과
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            with get_db_session() as session:
                result = func(session)
                return result
        except SQLAlchemyError as e:
            last_error = e
            logger.warning(f"데이터베이스 작업 실패 (시도 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    # 모든 재시도 실패
    logger.error(f"데이터베이스 작업이 {max_retries}번의 시도 후 실패했습니다: {last_error}")
    raise last_error 