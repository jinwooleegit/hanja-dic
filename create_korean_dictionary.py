import sqlite3
import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_database():
    """한국어 사전 데이터베이스 생성"""
    try:
        # 기존 데이터베이스 파일 삭제
        if os.path.exists('korean_dictionary.db'):
            os.remove('korean_dictionary.db')
            logging.info("기존 데이터베이스 파일을 삭제했습니다.")
            
        conn = sqlite3.connect('korean_dictionary.db')
        cursor = conn.cursor()

        # 단어 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_code TEXT,
            word TEXT NOT NULL,
            word_unit TEXT,
            word_type TEXT,
            pronunciation TEXT,
            origin TEXT,
            pos_info TEXT,
            study_info TEXT,
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
        
        # XML 파일에서 데이터 가져오기
        import_data_from_xml(conn)
        
    except Exception as e:
        logging.error(f"데이터베이스 생성 중 오류 발생: {str(e)}")
    finally:
        conn.close()

def extract_text_safely(elem, path):
    """XML 요소에서 안전하게 텍스트를 추출"""
    sub_elem = elem.find(path)
    return sub_elem.text.strip() if sub_elem is not None and sub_elem.text is not None else ''

def extract_meaning(elem):
    """의미 정보 추출"""
    meanings = []
    
    # pos_info에서 의미 추출
    pos_info = elem.find('pos_info')
    if pos_info is not None and pos_info.text:
        meanings.append(f"품사: {pos_info.text.strip()}")
    
    # study_info에서 의미 추출
    study_info = elem.find('study_info')
    if study_info is not None and study_info.text:
        meanings.append(f"학습 정보: {study_info.text.strip()}")
    
    # lexical_info에서 의미 추출
    lexical_info = elem.find('lexical_info')
    if lexical_info is not None and lexical_info.text:
        meanings.append(f"어휘 정보: {lexical_info.text.strip()}")
    
    # conju_info에서 의미 추출
    conju_info = elem.find('conju_info')
    if conju_info is not None and conju_info.text:
        meanings.append(f"활용 정보: {conju_info.text.strip()}")
    
    return ' | '.join(meanings) if meanings else ''

def extract_pronunciation(elem):
    """발음 정보 추출"""
    pronunciation_info = elem.find('pronunciation_info')
    if pronunciation_info is not None and pronunciation_info.text:
        return pronunciation_info.text.strip()
    return ''

def import_data_from_xml(conn):
    """XML 파일에서 데이터를 가져와 데이터베이스에 저장"""
    try:
        cursor = conn.cursor()
        data_dir = Path('data/raw')
        
        if not data_dir.exists():
            logging.error(f"데이터 디렉토리를 찾을 수 없습니다: {data_dir}")
            return
            
        xml_files = sorted(list(data_dir.glob('*.xml')))
        if not xml_files:
            logging.error("XML 파일을 찾을 수 없습니다.")
            return
            
        total_words = 0
        for xml_file in xml_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                words_data = []
                for item in root.findall('.//item'):
                    target_code = extract_text_safely(item, 'target_code')
                    word_info = item.find('word_info')
                    if word_info is None:
                        continue
                        
                    word = extract_text_safely(word_info, 'word')
                    word_unit = extract_text_safely(word_info, 'word_unit')
                    word_type = extract_text_safely(word_info, 'word_type')
                    pronunciation = extract_pronunciation(word_info)
                    origin = extract_text_safely(word_info, 'origin')
                    pos_info = extract_text_safely(word_info, 'pos_info')
                    study_info = extract_text_safely(word_info, 'study_info')
                    meaning = extract_meaning(word_info)
                    example = extract_text_safely(word_info, 'example')
                    
                    if word:  # 단어가 있는 경우만 저장
                        words_data.append((
                            target_code, word, word_unit, word_type, 
                            pronunciation, origin, pos_info, study_info,
                            meaning, example
                        ))
                
                if words_data:
                    # 배치 처리로 데이터 삽입
                    cursor.executemany('''
                        INSERT INTO words (
                            target_code, word, word_unit, word_type,
                            pronunciation, origin, pos_info, study_info,
                            meaning, example
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', words_data)
                    
                    conn.commit()
                    total_words += len(words_data)
                    logging.info(f"{xml_file.name}에서 {len(words_data)}개의 단어를 가져왔습니다.")
                
            except Exception as e:
                logging.error(f"{xml_file.name} 처리 중 오류 발생: {str(e)}")
                continue
                
        logging.info(f"총 {total_words}개의 단어를 데이터베이스에 저장했습니다.")
        
    except Exception as e:
        logging.error(f"데이터 가져오기 중 오류 발생: {str(e)}")
        conn.rollback()

if __name__ == '__main__':
    create_database() 