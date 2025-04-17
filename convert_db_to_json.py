import sqlite3
import json
import os

def convert_db_to_json():
    if not os.path.exists('korean_dictionary.db'):
        print("데이터베이스 파일이 존재하지 않습니다.")
        return
    
    conn = sqlite3.connect('korean_dictionary.db')
    cursor = conn.cursor()
    
    # words 테이블의 모든 데이터 가져오기
    cursor.execute("SELECT * FROM words")
    words = []
    
    for row in cursor.fetchall():
        word = {
            'id': row[0],
            'word': row[1],
            'word_unit': row[2],
            'word_type': row[3],
            'pronunciation': row[4],
            'origin': row[5],
            'meaning': row[6],
            'example': row[7]
        }
        words.append(word)
    
    # JSON 파일로 저장
    with open('data/words.json', 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    
    print(f"총 {len(words)}개의 단어를 JSON 파일로 변환했습니다.")
    conn.close()

if __name__ == "__main__":
    convert_db_to_json() 