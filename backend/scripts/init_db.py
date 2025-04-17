import os
import sys
import logging
from pathlib import Path
import sqlite3

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 프로젝트 경로 설정
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
    
logger.info(f"프로젝트 경로 추가: {project_root}")

# SQLite 데이터베이스 파일 경로
DB_PATH = os.path.join(project_root, "app.db")

def init_db():
    logger.info(f"데이터베이스 파일 경로: {DB_PATH}")
    
    # 이미 존재하는 경우 삭제
    if os.path.exists(DB_PATH):
        logger.info(f"기존 데이터베이스 파일 삭제: {DB_PATH}")
        os.remove(DB_PATH)
    
    # SQLite 연결 및 테이블 생성
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 한자 테이블 생성
        logger.info("한자 테이블 생성 중...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hanja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            traditional TEXT NOT NULL UNIQUE,
            simplified TEXT,
            korean_pronunciation TEXT NOT NULL,
            chinese_pronunciation TEXT,
            radical TEXT,
            stroke_count INTEGER,
            meaning TEXT NOT NULL,
            examples TEXT,
            frequency INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 인덱스 생성
        logger.info("인덱스 생성 중...")
        cursor.execute('CREATE INDEX idx_traditional ON hanja(traditional)')
        cursor.execute('CREATE INDEX idx_simplified ON hanja(simplified)')
        cursor.execute('CREATE INDEX idx_korean_pronunciation ON hanja(korean_pronunciation)')
        cursor.execute('CREATE INDEX idx_chinese_pronunciation ON hanja(chinese_pronunciation)')
        cursor.execute('CREATE INDEX idx_radical ON hanja(radical)')
        cursor.execute('CREATE INDEX idx_stroke_count ON hanja(stroke_count)')
        cursor.execute('CREATE INDEX idx_frequency ON hanja(frequency)')
        cursor.execute('CREATE INDEX idx_pronunciation_search ON hanja(korean_pronunciation, chinese_pronunciation)')
        cursor.execute('CREATE INDEX idx_radical_stroke ON hanja(radical, stroke_count)')
        cursor.execute('CREATE INDEX idx_hanja_search ON hanja(traditional, simplified, korean_pronunciation)')
        cursor.execute('CREATE INDEX idx_frequency_created ON hanja(frequency, created_at)')
        
        # 테이블 생성 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"생성된 테이블: {tables}")
        
        conn.commit()
        logger.info("데이터베이스 초기화 완료!")
        return True
        
    except Exception as e:
        conn.rollback()
        logger.error(f"데이터베이스 초기화 중 오류 발생: {e}")
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = init_db()
    if success:
        logger.info("데이터베이스 초기화 성공!")
    else:
        logger.error("데이터베이스 초기화 실패.")
        sys.exit(1) 