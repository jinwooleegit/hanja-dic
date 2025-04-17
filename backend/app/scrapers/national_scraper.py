from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import Dict
import re
import logging

logger = logging.getLogger(__name__)

class NationalScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://stdict.korean.go.kr/search/searchResult.do"
    
    def search(self, hanja: str) -> Dict:
        """동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}?searchKeyword={hanja}&searchType=hanja"
            logger.info(f"국립국어원 사전 검색: {url}")
            soup = self.get_soup(url)
            if not soup:
                logger.warning(f"국립국어원 사전에서 '{hanja}' 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"국립국어원 사전 검색 중 오류: {e}")
            return {}
    
    async def search_hanja_async(self, hanja: str) -> Dict:
        """비동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}?searchKeyword={hanja}&searchType=hanja"
            logger.info(f"국립국어원 사전 비동기 검색: {url}")
            soup = await self.get_soup_async(url)
            if not soup:
                logger.warning(f"국립국어원 사전에서 '{hanja}' 비동기 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"국립국어원 사전 비동기 검색 중 오류: {e}")
            return {}
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        """HTML에서 한자 정보를 추출합니다."""
        result = {}
        
        try:
            # 검색 결과 항목 찾기
            search_result = soup.find('dl', class_='search_list')
            if not search_result:
                logger.warning("국립국어원 사전에서 검색 결과를 찾을 수 없음")
                return {}
            
            # 한자 추출
            hanja_elem = search_result.find('a', class_='on')
            if hanja_elem:
                result['traditional'] = hanja_elem.text.strip()
            else:
                logger.warning("국립국어원 사전에서 한자를 찾을 수 없음")
                return {}
            
            # 간체자는 일반적으로 제공되지 않음
            result['simplified'] = result['traditional']
            
            # 한글 발음
            pron_elem = search_result.find('span', class_='search_sub')
            if pron_elem:
                result['korean_pronunciation'] = pron_elem.text.strip()
            
            # 의미
            mean_elem = search_result.find('span', class_='search_sub')
            if mean_elem and mean_elem.next_sibling:
                result['meaning'] = mean_elem.next_sibling.strip()
            
            # 부수 및 획수 (검색 결과 페이지에서는 제공하지 않을 수 있음)
            # 기본값 설정
            result['radical'] = '部'  # 기본 부수 (이후 데이터 병합 과정에서 덮어씌워질 것)
            result['stroke_count'] = 0  # 기본 획수 (이후 데이터 병합 과정에서 덮어씌워질 것)
            
            # 예문 (검색 결과 페이지에서는 제공하지 않을 수 있음)
            # 이 페이지에서 예문을 추출하려면 상세 페이지로 이동해야 할 수 있음
            
            # 출처 정보 추가
            result['source'] = 'national'
            logger.info(f"국립국어원 사전에서 '{result.get('traditional', '')}' 정보 추출 성공")
            
        except Exception as e:
            logger.error(f"국립국어원 사전 정보 추출 중 오류: {str(e)}")
            
        return result 