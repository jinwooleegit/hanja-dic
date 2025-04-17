from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(title="한자 사전 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 메인 라우트
@app.get("/")
async def root():
    return {"message": "한자 사전 API에 오신 것을 환영합니다"}

# 한자 모듈 라우터
from app.models.hanja import Hanja
from app.api.endpoints import hanja as hanja_router

# API 라우터 등록
app.include_router(hanja_router.router, prefix="/hanja", tags=["hanja"])

# 캐시 초기화 라우트
@app.post("/clear-cache")
async def clear_cache():
    """캐시를 초기화합니다."""
    try:
        from app.core.cache import redis_cache
        redis_cache.clear_cache()
        return {"message": "캐시가 초기화되었습니다."}
    except Exception as e:
        logger.error(f"캐시 초기화 중 오류 발생: {str(e)}")
        return {"message": "캐시 기능이 비활성화되어 있습니다."} 