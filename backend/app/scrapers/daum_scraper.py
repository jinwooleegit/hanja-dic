from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class DaumScraper(BaseScraper):
    BASE_URL = "https://dic.daum.net/search.do"
    
    def search_hanja(self, hanja: str) -> Dict:
        params = {
            'q': hanja,
            'dic': 'hanja'
        }
        
        soup = self.get_soup(self.BASE_URL, params=params)
        if not soup:
            return {}
            
        return self.extract_hanja_info(soup)
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        result = {}
        
        try:
            # 한자 정보 추출
            hanja_info = soup.find('div', class_='search_hanja')
            if not hanja_info:
                return {}
                
            # 한자
            result['traditional'] = hanja_info.find('span', class_='hanja').text.strip()
            
            # 간체자
            simplified = hanja_info.find('span', class_='simplified')
            if simplified:
                result['simplified'] = simplified.text.strip()
            
            # 한글 발음
            pronunciation = hanja_info.find('span', class_='pronunciation')
            if pronunciation:
                result['korean_pronunciation'] = pronunciation.text.strip()
            
            # 중국어 발음
            pinyin = hanja_info.find('span', class_='pinyin')
            if pinyin:
                result['chinese_pronunciation'] = pinyin.text.strip()
            
            # 부수
            radical = hanja_info.find('span', class_='radical')
            if radical:
                result['radical'] = radical.text.strip()
            
            # 획수
            stroke_count = hanja_info.find('span', class_='stroke_count')
            if stroke_count:
                count = re.search(r'\d+', stroke_count.text)
                if count:
                    result['stroke_count'] = int(count.group())
            
            # 뜻
            meaning = hanja_info.find('div', class_='meaning')
            if meaning:
                result['meaning'] = meaning.text.strip()
            
            # 예문
            examples = []
            for example in hanja_info.find_all('div', class_='example'):
                examples.append(example.text.strip())
            if examples:
                result['examples'] = '\n'.join(examples)
                
        except Exception as e:
            print(f"Error extracting hanja info from Daum: {str(e)}")
            
        return result 