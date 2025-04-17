from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import logging
import os

app = FastAPI(title="한국어 사전 API")

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Pydantic 모델 정의
class Word(BaseModel):
    word: str
    pronunciation: Optional[str] = None
    part_of_speech: Optional[str] = None
    meaning: Optional[str] = None
    example: Optional[str] = None

class RelatedWord(BaseModel):
    word_id: int
    related_word: str
    relation_type: str

# 데이터베이스 연결
def get_db():
    conn = sqlite3.connect('korean_dictionary.db')
    conn.row_factory = sqlite3.Row
    return conn

# 웹 인터페이스 라우트
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API 엔드포인트
@app.post("/api/words/", response_model=dict)
async def add_word(word: Word):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO words (word, pronunciation, part_of_speech, meaning, example)
        VALUES (?, ?, ?, ?, ?)
        ''', (word.word, word.pronunciation, word.part_of_speech, word.meaning, word.example))
        word_id = cursor.lastrowid
        conn.commit()
        return {"message": "단어가 성공적으로 추가되었습니다.", "word_id": word_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/api/related-words/", response_model=dict)
async def add_related_word(related_word: RelatedWord):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO related_words (word_id, related_word, relation_type)
        VALUES (?, ?, ?)
        ''', (related_word.word_id, related_word.related_word, related_word.relation_type))
        conn.commit()
        return {"message": "관련 단어가 성공적으로 추가되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/words/{word}", response_model=List[dict])
async def search_word(word: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT * FROM words WHERE word LIKE ?
        ''', (f'%{word}%',))
        words = [dict(row) for row in cursor.fetchall()]
        
        for word_data in words:
            cursor.execute('''
            SELECT related_word, relation_type FROM related_words WHERE word_id = ?
            ''', (word_data['id'],))
            related_words = cursor.fetchall()
            word_data['related_words'] = [dict(row) for row in related_words]
        
        return words
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/words/", response_model=List[dict])
async def get_all_words():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM words')
        words = [dict(row) for row in cursor.fetchall()]
        return words
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 