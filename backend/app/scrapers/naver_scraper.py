from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class NaverScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://hanja.dict.naver.com/search?query="

    def search(self, hanja: str) -> Dict:
        """동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}{hanja}"
            logger.info(f"네이버 사전 검색: {url}")
            soup = self.get_soup(url)
            if not soup:
                logger.warning(f"네이버 사전에서 '{hanja}' 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"네이버 사전 검색 중 오류: {e}")
            return {}

    async def search_hanja_async(self, hanja: str) -> Dict:
        """비동기적으로 한자를 검색합니다."""
        try:
            url = f"{self.base_url}{hanja}"
            logger.info(f"네이버 사전 비동기 검색: {url}")
            soup = await self.get_soup_async(url)
            if not soup:
                logger.warning(f"네이버 사전에서 '{hanja}' 비동기 검색 결과 없음")
                return {}
            return self.extract_hanja_info(soup)
        except Exception as e:
            logger.error(f"네이버 사전 비동기 검색 중 오류: {e}")
            return {}

    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        """HTML에서 한자 정보를 추출합니다."""
        result = {}

        # 기본 정보 추출
        try:
            hanja_info = soup.select_one('.origin')
            if not hanja_info:
                return {}

            # 한자
            hanja_element = hanja_info.select_one('.hanja')
            if hanja_element:
                result['traditional'] = hanja_element.text.strip()
                result['simplified'] = result['traditional']  # 네이버는 간체자를 따로 제공하지 않음

            # 발음
            pronunciation = hanja_info.select_one('.pronounce')
            if pronunciation:
                korean = pronunciation.select_one('.korean')
                chinese = pronunciation.select_one('.china')
                if korean:
                    result['korean_pronunciation'] = korean.text.strip()
                if chinese:
                    result['chinese_pronunciation'] = chinese.text.strip()

            # 부수와 획수
            radical_stroke = hanja_info.select_one('.sub_info')
            if radical_stroke:
                radical = radical_stroke.select_one('.radical')
                stroke = radical_stroke.select_one('.stroke')
                if radical:
                    result['radical'] = radical.text.strip()
                if stroke:
                    stroke_match = re.search(r'\d+', stroke.text)
                    if stroke_match:
                        result['stroke_count'] = int(stroke_match.group())

            # 의미
            meaning = soup.select_one('.meaning')
            if meaning:
                result['meaning'] = meaning.text.strip()

            # 예문
            examples = soup.select('.example_item')
            if examples:
                example_texts = []
                for example in examples[:3]:  # 최대 3개의 예문만 가져옴
                    hanja = example.select_one('.hanja')
                    korean = example.select_one('.korean')
                    if hanja and korean:
                        example_texts.append(f"{hanja.text.strip()}: {korean.text.strip()}")
                if example_texts:
                    result['examples'] = '\n'.join(example_texts)

            # 출처 정보 추가
            result['source'] = 'naver'
            logger.info(f"네이버 사전에서 '{result.get('traditional', '')}' 정보 추출 성공")
            return result

        except Exception as e:
            logger.error(f"네이버 사전 정보 추출 중 오류: {str(e)}")
            return {} 