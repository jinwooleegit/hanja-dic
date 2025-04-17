import sqlite3
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_database():
    """한국어 사전 데이터베이스 생성"""
    try:
        conn = sqlite3.connect('korean_dictionary.db')
        cursor = conn.cursor()

        # 단어 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            pronunciation TEXT,
            part_of_speech TEXT,
            meaning TEXT,
            example TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # 관련 단어 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS related_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER,
            related_word TEXT,
            relation_type TEXT,
            FOREIGN KEY (word_id) REFERENCES words (id)
        )
        ''')

        # 인덱스 생성
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON words (word)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_related_word ON related_words (word_id)')

        conn.commit()
        logging.info("데이터베이스가 성공적으로 생성되었습니다.")
        
    except Exception as e:
        logging.error(f"데이터베이스 생성 중 오류 발생: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    create_database() 