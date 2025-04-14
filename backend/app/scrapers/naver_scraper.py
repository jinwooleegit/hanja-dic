from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re

class NaverScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://hanja.dict.naver.com/search?query="

    def extract_data(self, html_content: str) -> dict:
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}

        # 기본 정보 추출
        try:
            hanja_info = soup.select_one('.origin')
            if not hanja_info:
                return {}

            # 한자
            result['traditional'] = hanja_info.select_one('.hanja').text.strip()
            result['simplified'] = result['traditional']  # 네이버는 간체자를 따로 제공하지 않음

            # 발음
            pronunciation = hanja_info.select_one('.pronounce')
            if pronunciation:
                korean = pronunciation.select_one('.korean')
                chinese = pronunciation.select_one('.china')
                result['korean_pronunciation'] = korean.text.strip() if korean else ''
                result['chinese_pronunciation'] = chinese.text.strip() if chinese else ''

            # 부수와 획수
            radical_stroke = hanja_info.select_one('.sub_info')
            if radical_stroke:
                radical = radical_stroke.select_one('.radical')
                stroke = radical_stroke.select_one('.stroke')
                result['radical'] = radical.text.strip() if radical else ''
                result['stroke_count'] = int(re.search(r'\d+', stroke.text).group()) if stroke else 0

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
                        example_texts.append(f"{hanja.text.strip()}\n{korean.text.strip()}")
                result['examples'] = '\n\n'.join(example_texts)

            result['source'] = 'naver'
            return result

        except Exception as e:
            print(f"네이버 스크래핑 중 오류 발생: {str(e)}")
            return {} 