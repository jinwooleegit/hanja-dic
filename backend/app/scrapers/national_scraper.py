from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from typing import Dict, Optional

class NationalScraper(BaseScraper):
    BASE_URL = "https://stdict.korean.go.kr/search/searchResult.do"
    
    def search_hanja(self, hanja: str) -> Dict:
        params = {
            'searchKeyword': hanja,
            'searchType': 'hanja'
        }
        
        soup = self.get_soup(self.BASE_URL, params=params)
        if not soup:
            return {}
            
        return self.extract_hanja_info(soup)
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        result = {}
        
        try:
            # 한자 정보 추출
            hanja_info = soup.find('div', class_='hanja_info')
            if hanja_info:
                result['traditional'] = hanja_info.find('span', class_='hanja').text.strip()
                result['korean_pronunciation'] = hanja_info.find('span', class_='pronunciation').text.strip()
                result['meaning'] = hanja_info.find('span', class_='meaning').text.strip()
                
                # 부수와 획수 정보
                radical_info = hanja_info.find('div', class_='radical_info')
                if radical_info:
                    result['radical'] = radical_info.find('span', class_='radical').text.strip()
                    result['stroke_count'] = int(radical_info.find('span', class_='stroke_count').text.strip())
                
                # 예문
                examples = []
                for example in hanja_info.find_all('div', class_='example'):
                    examples.append(example.text.strip())
                result['examples'] = '\n'.join(examples)
                
        except Exception as e:
            print(f"Error extracting hanja info: {str(e)}")
            
        return result 