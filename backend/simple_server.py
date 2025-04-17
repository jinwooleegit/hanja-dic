import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Path as FastAPIPath, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
import os
from pathlib import Path

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(title="한자 사전 API")

# CORS 설정 - 모든 오리진 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 템플릿 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 정적 파일 마운트 (필요시 사용)
# app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 데이터베이스 연결 함수
def get_db_connection():
    try:
        conn = sqlite3.connect("app.db")
        conn.row_factory = sqlite3.Row
        logger.info("SQLite DB 연결 성공")
        return conn
    except Exception as e:
        logger.error(f"SQLite DB 연결 오류: {str(e)}")
        raise

# Pydantic 모델
class HanjaBase(BaseModel):
    traditional: str
    simplified: Optional[str] = None
    korean_pronunciation: Optional[str] = None
    chinese_pronunciation: Optional[str] = None
    japanese_pronunciation: Optional[str] = None
    meaning: str
    stroke_count: Optional[int] = None
    radical: Optional[str] = None
    examples: Optional[str] = None
    frequency: Optional[int] = None

class HanjaCreate(HanjaBase):
    pass

class HanjaResponse(HanjaBase):
    id: Optional[int] = None
    favorite: Optional[bool] = False

class HanjaSearchRequest(BaseModel):
    query: str
    sort_by: Optional[str] = "frequency"  # frequency, strokes

# 웹 인터페이스 라우트
@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    """웹 인터페이스를 제공하는 HTML 페이지"""
    return templates.TemplateResponse("index.html", {"request": request})

# 루트 경로 API
@app.get("/api")
async def root():
    return {"message": "한자 사전 API에 오신 것을 환영합니다"}

# 한자 검색 엔드포인트
@app.post("/hanja/search")
async def search_hanja(search_request: HanjaSearchRequest):
    """한자 검색 API"""
    try:
        logger.info(f"검색 요청: {search_request.query}, 정렬: {search_request.sort_by}")
        conn = get_db_connection()
        search_term = f"%{search_request.query}%"
        
        query = """
        SELECT * FROM hanja 
        WHERE traditional LIKE ? 
        OR simplified LIKE ? 
        OR korean_pronunciation LIKE ? 
        OR meaning LIKE ?
        """
        
        # 정렬 조건 추가
        if search_request.sort_by == "frequency":
            query += " ORDER BY frequency DESC"
        elif search_request.sort_by == "strokes":
            query += " ORDER BY stroke_count ASC"
            
        cursor = conn.cursor()
        cursor.execute(query, (search_term, search_term, search_term, search_term))
        rows = cursor.fetchall()
        
        logger.info(f"검색 결과: {len(rows)}개 항목 찾음")
        
        result = []
        for row in rows:
            item = dict(row)
            # SQLite는 boolean을 지원하지 않으므로 변환 필요
            item['favorite'] = bool(item.get('favorite', 0))
            result.append(item)
            
        conn.close()
        return result
        
    except Exception as e:
        logger.error(f"한자 검색 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"한자 검색 중 오류: {str(e)}")

# 한자 상세 정보 조회 엔드포인트
@app.get("/hanja/details/{hanja_char}")
async def get_hanja_details(hanja_char: str = FastAPIPath(..., description="상세 정보 조회할 한자")):
    """한자 상세 정보 조회 API"""
    try:
        logger.info(f"한자 상세 정보 요청: {hanja_char}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hanja WHERE traditional = ?", (hanja_char,))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"한자 '{hanja_char}'를 찾을 수 없음")
            conn.close()
            raise HTTPException(status_code=404, detail=f"한자 '{hanja_char}'를 찾을 수 없습니다")
        
        item = dict(row)
        # SQLite는 boolean을 지원하지 않으므로 변환 필요
        item['favorite'] = bool(item.get('favorite', 0))
        conn.close()
        
        logger.info(f"한자 상세 정보 반환: {hanja_char}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"한자 상세 정보 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"한자 상세 정보 조회 중 오류: {str(e)}")

# 즐겨찾기 토글 엔드포인트
@app.post("/hanja/favorite/{hanja_char}")
async def toggle_favorite(hanja_char: str = FastAPIPath(..., description="즐겨찾기 토글할 한자")):
    """한자 즐겨찾기 토글 API"""
    try:
        logger.info(f"즐겨찾기 토글 요청: {hanja_char}")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 현재 즐겨찾기 상태 조회
        cursor.execute("SELECT * FROM hanja WHERE traditional = ?", (hanja_char,))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"한자 '{hanja_char}'를 찾을 수 없음")
            conn.close()
            raise HTTPException(status_code=404, detail=f"한자 '{hanja_char}'를 찾을 수 없습니다")
        
        # 현재 상태 반전
        current_favorite = bool(row['favorite'])
        new_favorite = not current_favorite
        
        # 상태 업데이트
        cursor.execute(
            "UPDATE hanja SET favorite = ? WHERE traditional = ?", 
            (int(new_favorite), hanja_char)
        )
        conn.commit()
        
        # 업데이트된 정보 조회
        cursor.execute("SELECT * FROM hanja WHERE traditional = ?", (hanja_char,))
        updated_row = cursor.fetchone()
        item = dict(updated_row)
        item['favorite'] = bool(item.get('favorite', 0))
        
        conn.close()
        logger.info(f"즐겨찾기 상태 변경: {hanja_char} -> {new_favorite}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"즐겨찾기 토글 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"즐겨찾기 토글 중 오류: {str(e)}")

# 즐겨찾기 목록 조회 엔드포인트
@app.get("/hanja/favorites")
async def get_favorites():
    """즐겨찾기 한자 목록 조회 API"""
    try:
        logger.info("즐겨찾기 목록 요청")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hanja WHERE favorite = 1")
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            item = dict(row)
            item['favorite'] = bool(item.get('favorite', 0))
            result.append(item)
            
        conn.close()
        logger.info(f"즐겨찾기 목록 반환: {len(result)}개 항목")
        return result
        
    except Exception as e:
        logger.error(f"즐겨찾기 목록 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"즐겨찾기 목록 조회 중 오류: {str(e)}")

# 서버 시작
if __name__ == "__main__":
    # 템플릿 디렉토리 확인
    template_dir = BASE_DIR / "templates"
    if not template_dir.exists():
        logger.warning(f"템플릿 디렉토리가 없습니다. 생성: {template_dir}")
        template_dir.mkdir(exist_ok=True)
    
    logger.info(f"서버 시작: localhost:8000")
    uvicorn.run("simple_server:app", host="localhost", port=8000, reload=True) 