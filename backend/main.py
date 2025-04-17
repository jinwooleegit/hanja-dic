from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from app.models.hanja import Hanja
from app.db.base import get_db
from app.scrapers.scraper_manager import scraper_manager
from app.core.cache import redis_cache
from app.api.endpoints import hanja

# 앱 임포트 (현재 디렉토리의 app.py 파일에서 app 변수 임포트)
from app import app

app = FastAPI(title="한자 사전 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(hanja.router, prefix="/hanja", tags=["hanja"])

@app.get("/")
async def root():
    return {"message": "한자 사전 API에 오신 것을 환영합니다"}

@app.post("/clear-cache")
async def clear_cache():
    """캐시를 초기화합니다."""
    try:
        redis_cache.clear_cache()
        return {"message": "캐시가 초기화되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 