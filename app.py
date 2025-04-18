from flask import Flask, jsonify, request, render_template
import json
import os
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sqlite3
from contextlib import closing

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def init_db():
    """데이터베이스 초기화"""
    try:
        with closing(sqlite3.connect('korean_dictionary.db')) as conn:
            with closing(conn.cursor()) as cursor:
                # 단어 테이블 생성
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_code TEXT,
                        word TEXT,
                        word_unit TEXT,
                        word_type TEXT,
                        pronunciation TEXT,
                        origin TEXT,
                        pos_info TEXT,
                        study_info TEXT,
                        lexical_info TEXT,
                        conju_info TEXT,
                        example TEXT,
                        meaning TEXT
                    )
                ''')
                conn.commit()
    except Exception as e:
        logger.error(f"데이터베이스 초기화 중 오류 발생: {str(e)}")

def import_xml_to_db():
    """XML 파일에서 데이터베이스로 데이터 임포트"""
    try:
        data_dir = Path('data/raw')
        if not data_dir.exists():
            logger.error(f"데이터 디렉토리가 존재하지 않습니다: {data_dir}")
            return
            
        xml_files = sorted(list(data_dir.glob('*.xml')))
        if not xml_files:
            logger.error("XML 파일을 찾을 수 없습니다.")
            return
            
        with closing(sqlite3.connect('korean_dictionary.db')) as conn:
            with closing(conn.cursor()) as cursor:
                for xml_file in xml_files:
                    try:
                        logger.info(f"XML 파일 처리 중: {xml_file}")
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        
                        for item in root.findall('.//item'):
                            word_info = item.find('word_info')
                            if word_info is None:
                                continue
                                
                            word_data = {
                                'target_code': item.find('target_code').text if item.find('target_code') is not None else '',
                                'word': word_info.find('word').text if word_info.find('word') is not None else '',
                                'word_unit': word_info.find('word_unit').text if word_info.find('word_unit') is not None else '',
                                'word_type': word_info.find('word_type').text if word_info.find('word_type') is not None else '',
                                'pronunciation': word_info.find('pronunciation_info').text if word_info.find('pronunciation_info') is not None else '',
                                'origin': word_info.find('origin').text if word_info.find('origin') is not None else '',
                                'pos_info': word_info.find('pos_info').text if word_info.find('pos_info') is not None else '',
                                'study_info': word_info.find('study_info').text if word_info.find('study_info') is not None else '',
                                'lexical_info': word_info.find('lexical_info').text if word_info.find('lexical_info') is not None else '',
                                'conju_info': word_info.find('conju_info').text if word_info.find('conju_info') is not None else '',
                                'example': word_info.find('example').text if word_info.find('example') is not None else ''
                            }
                            
                            # 의미 정보 합치기
                            meaning_parts = []
                            if word_data['pos_info']:
                                meaning_parts.append(f"품사: {word_data['pos_info']}")
                            if word_data['study_info']:
                                meaning_parts.append(f"학습 정보: {word_data['study_info']}")
                            if word_data['lexical_info']:
                                meaning_parts.append(f"어휘 정보: {word_data['lexical_info']}")
                            if word_data['conju_info']:
                                meaning_parts.append(f"활용 정보: {word_data['conju_info']}")
                            
                            word_data['meaning'] = ' | '.join(meaning_parts) if meaning_parts else ''
                            
                            # 데이터베이스에 삽입
                            cursor.execute('''
                                INSERT INTO words (
                                    target_code, word, word_unit, word_type, pronunciation,
                                    origin, pos_info, study_info, lexical_info, conju_info,
                                    example, meaning
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                word_data['target_code'], word_data['word'], word_data['word_unit'],
                                word_data['word_type'], word_data['pronunciation'], word_data['origin'],
                                word_data['pos_info'], word_data['study_info'], word_data['lexical_info'],
                                word_data['conju_info'], word_data['example'], word_data['meaning']
                            ))
                            
                    except Exception as e:
                        logger.error(f"{xml_file.name} 처리 중 오류 발생: {str(e)}")
                        continue
                        
                conn.commit()
                logger.info("데이터베이스 임포트 완료")
                
    except Exception as e:
        logger.error(f"데이터베이스 임포트 중 오류 발생: {str(e)}")

def get_db():
    """데이터베이스 연결 반환"""
    db = sqlite3.connect('korean_dictionary.db')
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    try:
        logger.info("메인 페이지 접속")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"메인 페이지 렌더링 중 오류 발생: {str(e)}")
        return "오류가 발생했습니다. 관리자에게 문의하세요.", 500

@app.route('/api/words/search')
def search_words():
    try:
        query = request.args.get('q', '').lower()
        logger.info(f"검색 쿼리: {query}")
        
        if not query:
            return jsonify([])
        
        with closing(get_db()) as db:
            cursor = db.cursor()
            cursor.execute('''
                SELECT * FROM words 
                WHERE LOWER(word) LIKE ? OR LOWER(meaning) LIKE ?
            ''', (f'%{query}%', f'%{query}%'))
            
            results = [dict(row) for row in cursor.fetchall()]
            logger.info(f"검색 결과: {len(results)}개")
            return jsonify(results)
            
    except Exception as e:
        logger.error(f"검색 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/words/<word>')
def get_word(word):
    try:
        logger.info(f"단어 조회: {word}")
        with closing(get_db()) as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM words WHERE word = ?', (word,))
            result = cursor.fetchone()
            
            if result:
                return jsonify(dict(result))
            return jsonify({'error': 'Word not found'}), 404
            
    except Exception as e:
        logger.error(f"단어 조회 중 오류 발생: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # 데이터베이스 초기화 및 데이터 임포트
        if not os.path.exists('korean_dictionary.db'):
            logger.info("데이터베이스 초기화 및 데이터 임포트 시작")
            init_db()
            import_xml_to_db()
        
        logger.info("Flask 애플리케이션 시작")
        app.run(host='0.0.0.0', port=8000, debug=True)
    except Exception as e:
        logger.error(f"Flask 애플리케이션 시작 중 오류 발생: {str(e)}") 