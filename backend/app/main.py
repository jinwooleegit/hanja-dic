from fastapi import FastAPI
from app.api.endpoints import hanja
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

@app.get("/")
def read_root():
    return {"message": "Welcome to HanjaDB API"}

# 라우터를 직접 등록 (API_V1_STR 프리픽스 사용하지 않음)
app.include_router(hanja.router) 