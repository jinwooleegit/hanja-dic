import os
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables(conn):
    """데이터베이스 테이블 생성"""
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja (
        id INTEGER PRIMARY KEY,
        character TEXT UNIQUE,
        meaning TEXT,
        reading TEXT,
        radical TEXT,
        stroke_count INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hanja_words (
        id INTEGER PRIMARY KEY,
        hanja_id INTEGER,
        word TEXT,
        meaning TEXT,
        FOREIGN KEY (hanja_id) REFERENCES hanja (id)
    )
    ''')
    conn.commit()

def insert_hanja_batch(conn, hanja_data, words_data):
    """한자 데이터를 일괄 삽입"""
    if not hanja_data:
        return 0
        
    cursor = conn.cursor()
    try:
        # 한자 데이터 삽입
        cursor.executemany('''
        INSERT OR IGNORE INTO hanja (character, meaning, reading, radical, stroke_count)
        VALUES (?, ?, ?, ?, ?)
        ''', hanja_data)
        
        # 삽입된 한자의 ID 조회
        placeholders = ','.join('?' * len(hanja_data))
        cursor.execute(f'''
        SELECT id, character FROM hanja WHERE character IN ({placeholders})
        ''', [h[0] for h in hanja_data])
        
        hanja_ids = {row[1]: row[0] for row in cursor.fetchall()}
        
        # 단어 데이터 삽입
        word_data_with_ids = []
        for word in words_data:
            hanja_id = hanja_ids.get(word[0])
            if hanja_id:
                word_data_with_ids.append((hanja_id, word[1], word[2]))
        
        if word_data_with_ids:
            cursor.executemany('''
            INSERT INTO hanja_words (hanja_id, word, meaning)
            VALUES (?, ?, ?)
            ''', word_data_with_ids)
        
        conn.commit()
        return len(hanja_data)
    except Exception as e:
        logging.error(f"데이터 삽입 중 오류 발생: {str(e)}")
        conn.rollback()
        return 0

def extract_text_safely(element, path, default=''):
    """XML 요소에서 안전하게 텍스트 추출"""
    try:
        found = element.find(path)
        if found is not None and found.text:
            return found.text.strip()
    except Exception:
        pass
    return default

def extract_hanja_from_text(text):
    """텍스트에서 한자 추출 (한글(한자) 형식)"""
    if not text:
        return None
    
    # 한글(한자) 패턴 매칭 - 더 유연한 패턴
    patterns = [
        r'[가-힣]+\(([一-龥]+)\)',  # 기본 패턴
        r'[가-힣]+[（(]([一-龥]+)[)）]',  # 다양한 괄호 지원
        r'[가-힣]+[（(]([一-龥]+)[)）]',  # 전각 괄호 지원
        r'[가-힣]+[（(]([一-龥]+)[)）]',  # 반각 괄호 지원
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # 괄호 없이 한자만 있는 경우
    hanja_pattern = r'[一-龥]+'
    match = re.search(hanja_pattern, text)
    if match:
        return match.group(0)
    
    return None

def parse_xml_file(file_path):
    """XML 파일에서 한자 데이터 추출"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        hanja_data = []
        words_data = []
        
        # XML 구조 분석
        logging.info(f"XML 루트 태그: {root.tag}")
        for child in root:
            logging.info(f"자식 태그: {child.tag}")
            if child.tag == 'item':
                for subchild in child:
                    logging.info(f"  - item 자식 태그: {subchild.tag}")
                    if subchild.tag == 'word_info':
                        for info in subchild:
                            logging.info(f"    - word_info 자식 태그: {info.tag}")
        
        # 모든 item 태그를 찾아서 처리
        items = root.findall('.//item')
        logging.info(f"총 {len(items)}개의 item 태그 발견")
        
        for item in items:
            try:
                # word_info 태그에서 단어 정보 추출
                word_info = item.find('word_info')
                if word_info is None:
                    continue
                
                # 단어 추출
                word_text = extract_text_safely(word_info, 'word')
                if not word_text:
                    continue
                
                # 한자 추출
                hanja = extract_hanja_from_text(word_text)
                if not hanja:
                    # word_info의 다른 태그에서 한자 찾기
                    for child in word_info:
                        if child.text:
                            hanja = extract_hanja_from_text(child.text)
                            if hanja:
                                break
                
                if not hanja:
                    continue
                
                # 의미 추출
                meanings = []
                for sense_info in word_info.findall('.//sense_info'):
                    definition = extract_text_safely(sense_info, 'definition')
                    if definition:
                        meanings.append(definition)
                
                meaning = '; '.join(meanings) if meanings else ''
                
                # 발음 추출
                reading = ''
                for pron_info in word_info.findall('.//pronunciation_info/pronunciation'):
                    if pron_info is not None and pron_info.text:
                        reading = pron_info.text.strip()
                        break
                
                # 부수와 획수 정보 추출
                radical = ''
                stroke_count = 0
                
                for info in word_info.findall('.//info'):
                    info_text = info.text if info.text else ''
                    if '부수' in info_text:
                        try:
                            radical = info_text.split('：')[-1].strip()
                            break
                        except:
                            pass
                    elif '획수' in info_text:
                        try:
                            stroke_count = int(info_text.split('：')[-1].strip())
                            break
                        except:
                            pass
                
                # 한자 데이터 추가
                hanja_data.append((
                    hanja,
                    meaning,
                    reading,
                    radical,
                    stroke_count
                ))
                
                # 예문 추출
                for sense_info in word_info.findall('.//sense_info'):
                    for example_info in sense_info.findall('.//example_info/example'):
                        example_text = example_info.text
                        if example_text:
                            example_hanja = extract_hanja_from_text(example_text)
                            if example_hanja:
                                words_data.append((hanja, example_hanja, meaning))
            
            except Exception as e:
                logging.error(f"항목 파싱 중 오류 발생: {str(e)}")
                continue
        
        if hanja_data:
            logging.info(f"{file_path}에서 {len(hanja_data)}개의 한자와 {len(words_data)}개의 단어 추출됨")
        
        return hanja_data, words_data
    except Exception as e:
        logging.error(f"XML 파싱 오류: {file_path} - {str(e)}")
        return [], []

def process_file(file_path):
    """개별 파일 처리"""
    try:
        logging.info(f"파일 처리 중: {file_path}")
        
        # 각 스레드마다 새로운 데이터베이스 연결 생성
        conn = sqlite3.connect('hanja.db')
        create_tables(conn)
        
        hanja_data, words_data = parse_xml_file(file_path)
        processed_count = 0
        
        if hanja_data:
            processed_count = insert_hanja_batch(conn, hanja_data, words_data)
            if processed_count > 0:
                logging.info(f"{file_path}에서 {processed_count}개의 한자 처리됨")
        
        conn.close()
        return processed_count
    except Exception as e:
        logging.error(f"파일 처리 중 오류 발생: {file_path} - {str(e)}")
        return 0

def main():
    data_dir = Path('data/raw')
    if not data_dir.exists():
        logging.error("데이터 디렉토리를 찾을 수 없습니다.")
        return
    
    xml_files = list(data_dir.glob('*.xml'))
    total_files = len(xml_files)
    total_hanja = 0
    processed_files = 0
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_file = {
            executor.submit(process_file, str(file)): file 
            for file in xml_files
        }
        
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                hanja_count = future.result()
                total_hanja += hanja_count
                processed_files += 1
                logging.info(f"처리된 파일 수: {processed_files}/{total_files} (총 {total_hanja}개 한자)")
            except Exception as e:
                logging.error(f"파일 처리 중 오류 발생: {file} - {str(e)}")
    
    logging.info(f"총 {total_hanja}개의 한자 데이터가 처리되었습니다.")

if __name__ == '__main__':
    main() 