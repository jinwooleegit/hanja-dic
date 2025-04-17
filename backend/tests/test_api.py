import pytest
import logging
from unittest import mock
from app.core.cache import redis_cache

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_read_main(client):
    """기본 API 엔드포인트 테스트"""
    response = client.get("/")
    logger.debug(f"응답: {response.status_code} - {response.text}")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to HanjaDB API"}

@pytest.fixture
def mock_redis_cache():
    """Redis 캐시 모킹 픽스처"""
    with mock.patch.object(redis_cache, 'clear_cache') as mock_clear_cache:
        mock_clear_cache.return_value = True
        yield mock_clear_cache

def test_clear_cache(client, mock_redis_cache):
    """캐시 초기화 API 테스트 (Redis 모킹)"""
    response = client.post("/clear-cache")
    logger.debug(f"응답: {response.status_code} - {response.text}")
    
    # API 호출 성공 검증
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Redis 모킹 함수 호출 검증
    mock_redis_cache.assert_called_once()

@pytest.mark.parametrize("route,status_code", [
    ("/search", 200),
    ("/details/試", 404),
])
def test_api_routes_exist(client, route, status_code):
    """API 라우트 존재 테스트 - 데이터베이스 연결이 되어 있어도 API 엔드포인트는 올바르게 응답해야 함"""
    if "/search" in route:
        response = client.post(route, json={"query": "test"})
    else:
        response = client.get(route)
        
    logger.debug(f"API 라우트 테스트 - {route}: {response.status_code}")
    
    # 올바른 상태 코드 확인
    assert response.status_code == status_code

def test_create_hanja(client, db_session):
    """한자 생성 API 테스트"""
    # 테스트용 한자 데이터
    hanja_data = {
        "traditional": "道",
        "simplified": "道",
        "korean_pronunciation": "도",
        "chinese_pronunciation": "dào",
        "radical": "辶",
        "stroke_count": 12,
        "meaning": "길, 도리, 방법",
        "examples": "道路(도로): 길, 도로",
        "frequency": 750
    }
    
    # 한자 생성 API 호출
    response = client.post("/", json=hanja_data)
    logger.debug(f"한자 생성 응답: {response.status_code} - {response.text}")
    
    # 응답 검증
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["traditional"] == hanja_data["traditional"]
    assert data["meaning"] == hanja_data["meaning"]
    
    # DB에 저장되었는지 확인
    from app.models.hanja import Hanja
    saved_hanja = db_session.query(Hanja).filter(Hanja.traditional == "道").first()
    assert saved_hanja is not None
    assert saved_hanja.korean_pronunciation == "도"
    
    # 검색 API를 통해 찾을 수 있는지 확인
    search_response = client.post("/search", json={"query": "도"})
    assert search_response.status_code == 200
    search_results = search_response.json()
    assert len(search_results) >= 1
    assert any(item["traditional"] == "道" for item in search_results)
    
    # 상세 정보 API를 통해 조회할 수 있는지 확인
    details_response = client.get(f"/details/道")
    assert details_response.status_code == 200
    details = details_response.json()
    assert details["traditional"] == "道"
    assert details["meaning"] == "길, 도리, 방법" 