from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
from typing import Dict, Optional
import time
import random
import logging

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self._session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """비동기 HTTP 세션을 반환합니다."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self.headers)
        return self._session
    
    async def close(self):
        """세션을 닫습니다."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    # 기존 동기식 메서드 (하위 호환성을 위해 유지)
    def get_soup(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """URL에서 HTML을 가져와 BeautifulSoup 객체를 반환합니다."""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"URL {url} 가져오기 오류: {str(e)}")
            return None
    
    # 비동기 메서드
    async def get_soup_async(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """비동기적으로 URL에서 HTML을 가져와 BeautifulSoup 객체를 반환합니다."""
        try:
            session = await self.get_session()
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                html = await response.text()
                return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logger.error(f"비동기 URL {url} 가져오기 오류: {str(e)}")
            return None
    
    async def delay_async(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """비동기 지연 함수"""
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))
    
    def delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """웹사이트에 과도한 부하를 주지 않기 위한 지연"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        """각 사이트별로 구현해야 하는 메서드"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다")
    
    def search(self, hanja: str) -> Dict:
        """각 사이트별로 구현해야 하는 메서드"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다")
    
    async def search_hanja_async(self, hanja: str) -> Dict:
        """각 사이트별로 구현해야 하는 비동기 검색 메서드"""
        raise NotImplementedError("이 메서드는 하위 클래스에서 구현해야 합니다") 