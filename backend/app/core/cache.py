from functools import wraps
import redis
import json
import logging
import time
from typing import Any, Callable, Optional, Dict, List, Union
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, retry_attempts: int = 3, retry_delay: float = 1.0):
        """Redis 캐시 초기화

        Args:
            retry_attempts: 연결 재시도 횟수
            retry_delay: 재시도 사이의 지연 시간(초)
        """
        self.redis_client = None
        self.enabled = True
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self._connect()

    def _connect(self) -> bool:
        """Redis 서버에 연결을 시도합니다.

        Returns:
            bool: 연결 성공 여부
        """
        for attempt in range(self.retry_attempts):
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_timeout=2.0,  # 타임아웃 설정
                    socket_connect_timeout=2.0
                )
                # 간단한 연결 확인
                self.redis_client.ping()
                logger.info("Redis 연결 성공")
                return True
            except redis.ConnectionError as e:
                logger.warning(f"Redis 연결 실패 (시도 {attempt+1}/{self.retry_attempts}): {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                logger.error(f"Redis 초기화 중 예상치 못한 오류: {e}")
                self.enabled = False
                break
        
        logger.warning("Redis 캐시 비활성화됨: 모든 캐싱 작업이 무시됩니다")
        self.enabled = False
        return False

    def cache_decorator(self, expire_time: int = 3600, key_prefix: str = ""):
        """함수 결과를 캐싱하는 데코레이터

        Args:
            expire_time: 캐시 만료 시간(초)
            key_prefix: 캐시 키 접두사
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # 캐시가 비활성화되었거나 클라이언트가 없는 경우 캐싱 없이 함수 실행
                if not self.enabled or not self.redis_client:
                    return await func(*args, **kwargs)

                # 캐시 키 생성
                cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args))}{hash(str(kwargs))}"
                
                try:
                    # 캐시된 데이터 확인
                    cached_data = self.redis_client.get(cache_key)
                    if cached_data:
                        logger.debug(f"캐시 적중: {cache_key}")
                        return json.loads(cached_data)

                    # 함수 실행
                    result = await func(*args, **kwargs)

                    # 결과 캐싱
                    if result:
                        try:
                            serialized = json.dumps(result)
                            self.redis_client.setex(
                                cache_key,
                                expire_time,
                                serialized
                            )
                            logger.debug(f"캐시 저장: {cache_key}, 만료 시간: {expire_time}초")
                        except (TypeError, json.JSONDecodeError) as e:
                            logger.warning(f"캐시 저장 실패 (직렬화 오류): {e}")
                        except redis.RedisError as e:
                            logger.warning(f"캐시 저장 실패 (Redis 오류): {e}")

                    return result

                except Exception as e:
                    logger.error(f"캐시 작업 중 오류 발생: {e}")
                    return await func(*args, **kwargs)

            return wrapper
        return decorator

    async def clear_cache(self, pattern: str = "*") -> bool:
        """지정된 패턴과 일치하는 모든 캐시를 삭제합니다.

        Args:
            pattern: 삭제할 캐시 키 패턴
            
        Returns:
            bool: 삭제 성공 여부
        """
        if not self.enabled:
            logger.warning("캐시가 비활성화되어 있어 캐시 삭제를 건너뜁니다")
            return True
            
        try:
            if not self.redis_client:
                logger.warning("Redis 클라이언트가 초기화되지 않았습니다")
                return True  # 캐시가 없는 경우 성공으로 간주

            # 패턴이 없으면 모든 키를 삭제
            if not pattern or pattern == "*":
                logger.info("모든 캐시 키를 삭제합니다")
            else:
                logger.info(f"패턴 '{pattern}'과 일치하는 캐시 키를 삭제합니다")

            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"{len(keys)}개의 캐시 항목이 삭제되었습니다.")
            else:
                logger.info("삭제할 캐시 키가 없습니다")
                
            return True
            
        except redis.RedisError as e:
            logger.error(f"캐시 삭제 중 Redis 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"캐시 삭제 중 예상치 못한 오류: {e}")
            return False

    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 키에 해당하는 값을 가져옵니다."""
        if not self.enabled or not self.redis_client:
            return None
            
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"캐시 조회 중 오류: {e}")
            return None
            
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """값을 캐시에 저장합니다."""
        if not self.enabled or not self.redis_client:
            return False
            
        try:
            serialized = json.dumps(value)
            self.redis_client.setex(key, expire, serialized)
            return True
        except Exception as e:
            logger.error(f"캐시 저장 중 오류: {e}")
            return False

# 싱글톤 인스턴스 생성
redis_cache = RedisCache() 