from flask import Flask, jsonify, request, render_template
import json
import os
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# JSON 파일에서 데이터 로드
def load_words():
    with open('data/words.json', 'r', encoding='utf-8') as f:
        return json.load(f)

words_data = load_words()

@app.route('/')
def index():
    return render_template('index.html', analytics_script='''
        <script defer src="/_vercel/insights/script.js"></script>
    ''')

@app.route('/api/words/search')
def search_words():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for word in words_data:
        if query in word['word'].lower() or query in word['meaning'].lower():
            results.append(word)
    
    return jsonify(results)

@app.route('/api/words/<word>')
def get_word(word):
    for w in words_data:
        if w['word'] == word:
            return jsonify(w)
    return jsonify({'error': 'Word not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 