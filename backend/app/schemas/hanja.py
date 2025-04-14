from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
import re

class HanjaBase(BaseModel):
    traditional: str = Field(..., min_length=1, max_length=5, description="전통 한자")
    simplified: Optional[str] = Field(None, max_length=5, description="간체자")
    korean_pronunciation: str = Field(..., min_length=1, max_length=10, description="한국어 발음")
    chinese_pronunciation: Optional[str] = Field(None, max_length=10, description="중국어 발음")
    radical: Optional[str] = Field(None, max_length=5, description="부수")
    stroke_count: Optional[int] = Field(None, ge=1, le=64, description="획수")
    meaning: str = Field(..., min_length=1, max_length=500, description="의미")
    examples: Optional[str] = Field(None, max_length=1000, description="예문")
    frequency: Optional[int] = Field(0, ge=0, description="검색 빈도")
    
    @field_validator('traditional', 'simplified', 'radical')
    @classmethod
    def validate_chinese_chars(cls, v, info):
        if not v:
            return v
        # 한자 및 CJK 문자 검증
        if not re.match(r'^[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf]+$', v):
            raise ValueError(f"{info.field_name}은(는) 유효한 한자 문자여야 합니다")
        return v

class HanjaCreate(HanjaBase):
    """한자 생성을 위한 스키마"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "traditional": "水",
                "simplified": "水",
                "korean_pronunciation": "수",
                "chinese_pronunciation": "shuǐ",
                "radical": "水",
                "stroke_count": 4,
                "meaning": "물 수",
                "examples": "水泳(수영): 수영",
                "frequency": 100
            }
        }
    )

class HanjaUpdate(BaseModel):
    """한자 업데이트를 위한 스키마"""
    traditional: Optional[str] = Field(None, min_length=1, max_length=5, description="전통 한자")
    simplified: Optional[str] = Field(None, max_length=5, description="간체자")
    korean_pronunciation: Optional[str] = Field(None, min_length=1, max_length=10, description="한국어 발음")
    chinese_pronunciation: Optional[str] = Field(None, max_length=10, description="중국어 발음")
    radical: Optional[str] = Field(None, max_length=5, description="부수")
    stroke_count: Optional[int] = Field(None, ge=1, le=64, description="획수")
    meaning: Optional[str] = Field(None, min_length=1, max_length=500, description="의미")
    examples: Optional[str] = Field(None, max_length=1000, description="예문")
    frequency: Optional[int] = Field(None, ge=0, description="검색 빈도")
    
    model_config = ConfigDict(json_schema_extra={"example": {"meaning": "물 수", "frequency": 200}})

class HanjaResponse(HanjaBase):
    """API 응답용 한자 스키마"""
    id: Optional[int] = Field(None, description="고유 ID")
    created_at: Optional[datetime] = Field(None, description="생성 시간")
    updated_at: Optional[datetime] = Field(None, description="마지막 업데이트 시간")

    model_config = ConfigDict(from_attributes=True)

class HanjaSearchRequest(BaseModel):
    """한자 검색 요청 스키마"""
    query: str = Field(..., min_length=1, max_length=50, description="검색어")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "수"
            }
        }
    )

class HanjaListResponse(BaseModel):
    """페이지네이션된 한자 목록 응답"""
    items: List[HanjaResponse]
    total: int
    page: int
    page_size: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "traditional": "水",
                        "simplified": "水",
                        "korean_pronunciation": "수",
                        "chinese_pronunciation": "shuǐ",
                        "radical": "水",
                        "stroke_count": 4,
                        "meaning": "물 수",
                        "examples": "水泳(수영): 수영",
                        "frequency": 100,
                        "id": 1,
                        "created_at": "2023-06-01T12:00:00",
                        "updated_at": "2023-06-01T12:00:00"
                    }
                ],
                "total": 1,
                "page": 1,
                "page_size": 20
            }
        }
    ) 