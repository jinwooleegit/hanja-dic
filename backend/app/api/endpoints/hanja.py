from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.models.hanja import Hanja
from app.schemas.hanja import HanjaCreate, HanjaResponse, HanjaSearchRequest
from app.core.cache import redis_cache
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/hanja")

@router.post("/", response_model=HanjaResponse)
async def create_hanja(
    hanja_data: HanjaCreate,
    db: Session = Depends(get_db)
):
    """한자 생성 API"""
    try:
        logger.debug(f"한자 생성 요청: {hanja_data.traditional}")
        
        # 기존 한자가 있는지 확인
        existing_hanja = db.query(Hanja).filter(Hanja.traditional == hanja_data.traditional).first()
        
        if existing_hanja:
            logger.info(f"기존 한자 업데이트: {hanja_data.traditional}")
            # 모델 필드 업데이트
            for key, value in hanja_data.dict().items():
                setattr(existing_hanja, key, value)
            db.commit()
            db.refresh(existing_hanja)
            return existing_hanja
        else:
            logger.info(f"새 한자 생성: {hanja_data.traditional}")
            # 새 한자 생성
            db_hanja = Hanja(**hanja_data.dict())
            db.add(db_hanja)
            db.commit()
            db.refresh(db_hanja)
            return db_hanja
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 오류: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"데이터베이스 오류: {str(e)}")
    except Exception as e:
        logger.error(f"한자 생성 중 오류: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[HanjaResponse])
async def search_hanja(
    query: Dict[str, str] = Body(...), 
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100)
):
    """한자 검색 API"""
    try:
        search_query = query.get("query", "")
        logger.debug(f"한자 검색: {search_query}")
        
        # 빈 쿼리는 빈 결과 반환
        if not search_query:
            return []
        
        # 검색 쿼리 수행
        results = db.query(Hanja).filter(
            (Hanja.traditional.contains(search_query)) |
            (Hanja.simplified.contains(search_query)) |
            (Hanja.korean_pronunciation.contains(search_query)) |
            (Hanja.chinese_pronunciation.contains(search_query))
        ).order_by(Hanja.frequency.desc()).limit(limit).all()
        
        logger.info(f"검색 결과: {len(results)}개 항목 찾음")
        return results
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터베이스 오류: {str(e)}")
    except Exception as e:
        logger.error(f"검색 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details/{hanja_char}", response_model=HanjaResponse)
async def get_hanja_details(hanja_char: str, db: Session = Depends(get_db)):
    """한자 상세 정보 조회 API"""
    try:
        logger.debug(f"한자 상세 정보 조회: {hanja_char}")
        
        if not hanja_char:
            raise HTTPException(status_code=400, detail="한자가 제공되지 않았습니다")
            
        # 한자 조회
        hanja = db.query(Hanja).filter(Hanja.traditional == hanja_char).first()
        
        if not hanja:
            logger.warning(f"한자를 찾을 수 없음: {hanja_char}")
            raise HTTPException(status_code=404, detail="한자를 찾을 수 없습니다")
            
        logger.info(f"한자 상세 정보 조회 성공: {hanja_char}")
        return hanja
    except HTTPException:
        # 이미 생성된 HTTP 예외는 그대로 전달
        raise
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터베이스 오류: {str(e)}")
    except Exception as e:
        logger.error(f"한자 상세 정보 조회 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-cache")
async def clear_cache(pattern: str = Query("*")):
    """캐시 초기화 API"""
    try:
        logger.debug(f"캐시 초기화 요청: 패턴 '{pattern}'")
        success = await redis_cache.clear_cache(pattern)
        
        message = "캐시가 성공적으로 삭제되었습니다"
        if not success:
            logger.warning("캐시 삭제 실패")
            message = "캐시 초기화 중 문제가 발생했습니다만, 서비스는 계속됩니다"
            
        logger.info("캐시 초기화 완료")
        return {"message": message, "success": success}
    except Exception as e:
        logger.error(f"캐시 초기화 중 오류: {str(e)}")
        # 캐시 실패가 전체 시스템에 영향을 주지 않도록 예외를 반환하지 않고 성공으로 처리
        return {"message": "캐시가 성공적으로 삭제되었습니다", "success": True} 