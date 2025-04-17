import sqlite3
import os

def reset_database():
    # 데이터베이스 파일 경로
    db_path = 'data/processed/hanja_dictionary.db'
    
    # 데이터베이스 파일이 있으면 삭제
    if os.path.exists(db_path):
        os.remove(db_path)
        print("기존 데이터베이스가 삭제되었습니다.")
    
    # 새 데이터베이스 생성
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 한자 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character TEXT NOT NULL UNIQUE,
        korean_pronunciation TEXT,
        meaning TEXT,
        stroke_count INTEGER,
        radical TEXT,
        level TEXT,
        examples TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 한자-단어 관계 테이블 생성
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja_word (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hanja_id INTEGER,
        word TEXT NOT NULL,
        pronunciation TEXT,
        meaning TEXT,
        FOREIGN KEY (hanja_id) REFERENCES hanja(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("새 데이터베이스가 생성되었습니다.")

if __name__ == "__main__":
    reset_database() 