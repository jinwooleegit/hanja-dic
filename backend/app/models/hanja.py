from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.base_class import Base

class Hanja(Base):
    __tablename__ = "hanja"

    id = Column(Integer, primary_key=True, index=True)
    traditional = Column(String, unique=True, index=True, nullable=False)
    simplified = Column(String, index=True)
    korean_pronunciation = Column(String, index=True, nullable=False)
    chinese_pronunciation = Column(String, index=True)
    radical = Column(String, index=True)
    stroke_count = Column(Integer, index=True)
    meaning = Column(String, nullable=False)
    examples = Column(String)
    frequency = Column(Integer, default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 복합 인덱스
    __table_args__ = (
        # 발음 검색을 위한 인덱스
        Index('idx_pronunciation_search', 'korean_pronunciation', 'chinese_pronunciation'),
        # 부수와 획수 검색을 위한 인덱스
        Index('idx_radical_stroke', 'radical', 'stroke_count'),
        # 자주 사용되는 검색 패턴을 위한 인덱스
        Index('idx_hanja_search', 'traditional', 'simplified', 'korean_pronunciation'),
        # 정렬을 위한 인덱스
        Index('idx_frequency_created', 'frequency', 'created_at'),
    ) 