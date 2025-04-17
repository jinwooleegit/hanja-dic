import sqlite3
import os

def create_database():
    # 데이터베이스 파일 경로
    db_path = 'data/processed/hanja_dictionary.db'
    
    # 디렉토리 생성
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 한자 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character TEXT NOT NULL UNIQUE,  -- 한자
        korean_pronunciation TEXT,       -- 한글 발음
        meaning TEXT,                    -- 뜻
        stroke_count INTEGER,            -- 획수
        radical TEXT,                    -- 부수
        level TEXT,                      -- 난이도 (초급/중급/고급)
        examples TEXT,                   -- 예문
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 한자-단어 관계 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja_word (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hanja_id INTEGER,
        word TEXT NOT NULL,              -- 단어
        pronunciation TEXT,              -- 발음
        meaning TEXT,                    -- 뜻
        FOREIGN KEY (hanja_id) REFERENCES hanja(id)
    )
    ''')
    
    # 변경사항 저장
    conn.commit()
    conn.close()
    
    print("데이터베이스가 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    create_database() 