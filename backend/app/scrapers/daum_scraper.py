from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re
import logging

logger = logging.getLogger(__name__)

class DaumScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://dic.daum.net/search.do"
    
    def search(self, hanja: str) -> Dict:
        """동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}?q={hanja}&dic=hanja"
            logger.info(f"다음 사전 검색: {url}")
            soup = self.get_soup(url)
            if not soup:
                logger.warning(f"다음 사전에서 '{hanja}' 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"다음 사전 검색 중 오류: {e}")
            return {}
    
    async def search_hanja_async(self, hanja: str) -> Dict:
        """비동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}?q={hanja}&dic=hanja"
            logger.info(f"다음 사전 비동기 검색: {url}")
            soup = await self.get_soup_async(url)
            if not soup:
                logger.warning(f"다음 사전에서 '{hanja}' 비동기 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"다음 사전 비동기 검색 중 오류: {e}")
            return {}
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        """HTML에서 한자 정보를 추출합니다."""
        result = {}
        
        try:
            # 한자 정보 추출
            hanja_info = soup.find('div', class_='card_word')
            if not hanja_info:
                logger.warning("다음 사전에서 한자 정보를 찾을 수 없음")
                return {}
                
            # 한자 추출
            hanja_elem = hanja_info.find('span', class_='txt_hanzi')
            if hanja_elem:
                result['traditional'] = hanja_elem.text.strip()
            else:
                logger.warning("다음 사전에서 한자를 찾을 수 없음")
                return {}
            
            # 간체자 처리 (다음은 보통 제공하지 않음)
            result['simplified'] = result['traditional']
            
            # 한글 발음
            pronunciation = hanja_info.find('span', class_='txt_pronounce')
            if pronunciation:
                result['korean_pronunciation'] = pronunciation.text.strip()
            
            # 중국어 발음
            pinyin = hanja_info.find('span', class_='txt_pinyin')
            if pinyin:
                result['chinese_pronunciation'] = pinyin.text.strip()
            
            # 부수 (다음은 부수 정보를 제공하지 않을 수 있음)
            # 실제 HTML을 확인하여 부수 클래스를 찾아야 함
            
            # 획수
            stroke_count_elem = hanja_info.find('span', string=re.compile(r'획수'))
            if stroke_count_elem:
                count_match = re.search(r'\d+', stroke_count_elem.text)
                if count_match:
                    result['stroke_count'] = int(count_match.group())
            
            # 뜻
            meaning_elem = hanja_info.find('span', class_='txt_mean')
            if meaning_elem:
                result['meaning'] = meaning_elem.text.strip()
            
            # 예문
            examples = []
            for example in hanja_info.find_all('div', class_='txt_example'):
                examples.append(example.text.strip())
            if examples:
                result['examples'] = '\n'.join(examples)
                
            # 출처 정보 추가
            result['source'] = 'daum'
            logger.info(f"다음 사전에서 '{result.get('traditional', '')}' 정보 추출 성공")
            
        except Exception as e:
            logger.error(f"다음 사전 정보 추출 중 오류: {str(e)}")
            
        return result 