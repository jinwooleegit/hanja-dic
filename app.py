from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    """데이터베이스 연결 생성"""
    db_path = Path('data/processed/hanja_dictionary.db')
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 한자 검색
    cursor.execute('''
    SELECT h.*, GROUP_CONCAT(hw.word) as related_words
    FROM hanja h
    LEFT JOIN hanja_word hw ON h.id = hw.hanja_id
    WHERE h.character LIKE ? OR h.korean_pronunciation LIKE ?
    GROUP BY h.id
    ''', (f'%{query}%', f'%{query}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in results])

@app.route('/hanja/<int:hanja_id>')
def get_hanja(hanja_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 한자 상세 정보 조회
    cursor.execute('''
    SELECT h.*, GROUP_CONCAT(hw.word) as related_words
    FROM hanja h
    LEFT JOIN hanja_word hw ON h.id = hw.hanja_id
    WHERE h.id = ?
    GROUP BY h.id
    ''', (hanja_id,))
    
    hanja = cursor.fetchone()
    conn.close()
    
    if hanja:
        return jsonify(dict(hanja))
    return jsonify({'error': '한자를 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    app.run(debug=True) 