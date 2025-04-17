import sqlite3
import os

def check_database():
    if not os.path.exists('korean_dictionary.db'):
        print("데이터베이스 파일이 존재하지 않습니다.")
        return
    
    conn = sqlite3.connect('korean_dictionary.db')
    cursor = conn.cursor()
    
    # 테이블 구조 확인
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\n=== 테이블 목록 ===")
    for table in tables:
        print(f"테이블: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print("컬럼:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    # words 테이블의 데이터 수 확인
    cursor.execute("SELECT COUNT(*) FROM words;")
    count = cursor.fetchone()[0]
    print(f"\nwords 테이블의 총 레코드 수: {count}")
    
    # 샘플 데이터 확인
    if count > 0:
        print("\n=== 샘플 데이터 (최대 5개) ===")
        cursor.execute("SELECT * FROM words LIMIT 5;")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}")
            print(f"단어: {row[1]}")
            print(f"단어 단위: {row[2]}")
            print(f"단어 유형: {row[3]}")
            print(f"발음: {row[4]}")
            print(f"어원: {row[5]}")
            print(f"의미: {row[6]}")
            print(f"예문: {row[7]}")
            print("---")
    
    # 특정 단어 검색 테스트
    print("\n=== 검색 테스트 ===")
    test_words = ['빠르다', '빨리', '국어', '발음']
    for word in test_words:
        cursor.execute("SELECT COUNT(*) FROM words WHERE word = ?", (word,))
        count = cursor.fetchone()[0]
        print(f"'{word}' 검색 결과: {count}개")
        
        if count > 0:
            cursor.execute("SELECT * FROM words WHERE word = ? LIMIT 1", (word,))
            row = cursor.fetchone()
            print(f"  - 단어: {row[1]}")
            print(f"  - 의미: {row[6]}")
    
    conn.close()

if __name__ == "__main__":
    check_database() 