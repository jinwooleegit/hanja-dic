import sqlite3
import json
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def export_to_json():
    """데이터베이스의 내용을 JSON 파일로 내보내기"""
    try:
        # 데이터베이스 연결
        conn = sqlite3.connect('korean_dictionary.db')
        cursor = conn.cursor()

        # 단어 데이터 가져오기
        cursor.execute('''
            SELECT 
                target_code,
                word,
                word_unit,
                word_type,
                pronunciation,
                origin,
                pos_info,
                study_info,
                meaning,
                example
            FROM words
        ''')
        
        words = []
        for row in cursor.fetchall():
            word = {
                'target_code': row[0],
                'word': row[1],
                'word_unit': row[2],
                'word_type': row[3],
                'pronunciation': row[4],
                'origin': row[5],
                'pos_info': row[6],
                'study_info': row[7],
                'meaning': row[8],
                'example': row[9]
            }
            words.append(word)
        
        # JSON 파일로 저장
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        with open('data/words.json', 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        
        logger.info(f"총 {len(words)}개의 단어를 JSON 파일로 내보냈습니다.")
        
    except Exception as e:
        logger.error(f"JSON 파일 내보내기 중 오류 발생: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    export_to_json() 