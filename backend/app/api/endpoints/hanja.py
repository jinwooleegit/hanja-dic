from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging
from typing import List, Optional

from app.api.deps import get_db
from app.models.hanja import Hanja
from app.schemas.hanja import HanjaCreate, HanjaResponse, HanjaSearchRequest, HanjaListResponse
from app.core.cache import redis_cache as cache

# 로거 설정
logger = logging.getLogger(__name__)

# 라우터 초기화
router = APIRouter(tags=["hanja"])

@router.post("/", response_model=HanjaResponse, status_code=status.HTTP_201_CREATED)
async def create_hanja(
    hanja_data: HanjaCreate,
    db: Session = Depends(get_db)
):
    """
    한자 생성 또는 업데이트하는 엔드포인트
    """
    try:
        # 이미 존재하는 한자인지 확인
        existing_hanja = db.query(Hanja).filter(Hanja.traditional == hanja_data.traditional).first()
        
        if existing_hanja:
            # 기존 한자 업데이트
            for key, value in hanja_data.model_dump().items():
                if value is not None:
                    setattr(existing_hanja, key, value)
            db.commit()
            return HanjaResponse.model_validate(existing_hanja)
        else:
            # 새 한자 생성
            new_hanja = Hanja(**hanja_data.model_dump())
            db.add(new_hanja)
            db.commit()
            db.refresh(new_hanja)
            return HanjaResponse.model_validate(new_hanja)
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"한자 생성 중 무결성 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"한자 생성 실패: {str(e)}"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"한자 생성 중 데이터베이스 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"한자 생성 중 데이터베이스 오류: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"한자 생성 중 예기치 않은 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"한자 생성 중 예기치 않은 오류: {str(e)}"
        )

@router.post("/search", response_model=List[HanjaResponse])
async def search_hanja(search_request: HanjaSearchRequest, db: Session = Depends(get_db)):
    """한자 검색"""
    try:
        query = db.query(Hanja)
        
        if search_request.query:
            search_term = f"%{search_request.query}%"
            query = query.filter(
                (Hanja.traditional.contains(search_request.query)) |
                (Hanja.simplified.contains(search_request.query)) |
                (Hanja.korean_pronunciation.contains(search_request.query)) |
                (Hanja.meaning.contains(search_request.query))
            )
        
        # 정렬 기준 적용
        if search_request.sort_by == "frequency":
            query = query.order_by(Hanja.frequency.desc())
        elif search_request.sort_by == "strokes":
            query = query.order_by(Hanja.stroke_count.asc())
        
        results = query.limit(100).all()
        return results
    except Exception as e:
        logger.error(f"한자 검색 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"한자 검색 중 오류가 발생했습니다: {str(e)}")

@router.get("/details/{hanja_char}", response_model=HanjaResponse)
async def get_hanja_details(
    hanja_char: str = Path(..., description="상세 정보를 조회할 한자"),
    db: Session = Depends(get_db)
):
    """
    특정 한자의 세부 정보를 조회하는 엔드포인트
    """
    try:
        # 캐시 확인
        cache_key = f"hanja:{hanja_char}"
        cached_data = await cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # 데이터베이스에서 한자 정보 조회
        hanja = db.query(Hanja).filter(Hanja.traditional == hanja_char).first()
        
        if not hanja:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"한자 '{hanja_char}'를 찾을 수 없습니다"
            )
        
        # 결과를 HanjaResponse로 변환
        response = HanjaResponse.model_validate(hanja)
        
        # 캐시에 저장
        await cache.set(cache_key, response.model_dump())
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"한자 세부 정보 조회 중 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"한자 세부 정보 조회 중 오류: {str(e)}"
        )

@router.post("/favorite/{hanja_char}", response_model=HanjaResponse)
async def toggle_favorite(
    hanja_char: str = Path(..., description="즐겨찾기 상태를 변경할 한자"),
    db: Session = Depends(get_db)
):
    """한자 즐겨찾기 상태 토글 엔드포인트"""
    try:
        hanja = db.query(Hanja).filter(Hanja.traditional == hanja_char).first()
        
        if not hanja:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 한자를 찾을 수 없습니다: {hanja_char}"
            )
        
        # 즐겨찾기 상태 토글
        hanja.favorite = not hanja.favorite
        db.commit()
        db.refresh(hanja)
        
        # 캐시 업데이트
        await cache.delete(f"hanja:detail:{hanja_char}")
        await cache.delete("hanja:favorites")
        
        return hanja
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"즐겨찾기 토글 중 DB 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"즐겨찾기 토글 중 DB 오류: {str(e)}"
        )
    except Exception as e:
        logger.error(f"즐겨찾기 토글 중 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"즐겨찾기 토글 중 오류: {str(e)}"
        )

@router.get("/favorites", response_model=List[HanjaResponse])
async def get_favorites(db: Session = Depends(get_db)):
    """즐겨찾기한 한자 목록 조회 엔드포인트"""
    try:
        # 캐시 확인
        cached_data = await cache.get("hanja:favorites")
        if cached_data:
            logger.info("캐시에서 즐겨찾기 목록 가져옴")
            return cached_data
        
        # DB에서 조회
        favorites = db.query(Hanja).filter(Hanja.favorite == True).all()
        
        # 캐시 저장
        await cache.set("hanja:favorites", favorites)
        
        return favorites
    
    except Exception as e:
        logger.error(f"즐겨찾기 목록 조회 중 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"즐겨찾기 목록 조회 중 오류: {str(e)}"
        )

@router.post("/clear-cache", status_code=status.HTTP_200_OK)
async def clear_cache():
    """
    캐시를 초기화하는 엔드포인트
    """
    try:
        await cache.clear_cache("*")
        return {"message": "캐시가 성공적으로 초기화되었습니다"}
    except Exception as e:
        logger.error(f"캐시 초기화 중 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"캐시 초기화 중 오류: {str(e)}"
        ) 