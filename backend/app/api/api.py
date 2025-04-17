from fastapi import APIRouter

from app.api.endpoints import hanja

api_router = APIRouter()
api_router.include_router(hanja.router, prefix="/hanja") 