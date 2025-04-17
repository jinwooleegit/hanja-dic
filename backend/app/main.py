from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import hanja
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to HanjaDB API"}

# 루트 경로에 라우터 등록 (프리픽스 제거)
app.include_router(hanja.router)

# 캐시 초기화 엔드포인트를 메인 애플리케이션에 추가
@app.post("/clear-cache")
async def clear_cache():
    """캐시를 초기화합니다."""
    from app.core.cache import redis_cache
    try:
        await redis_cache.clear_cache("*")
        return {"message": "캐시가 초기화되었습니다."}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e)) 