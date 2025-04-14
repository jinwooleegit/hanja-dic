from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional
import time
import random

class BaseScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """웹사이트에 과도한 부하를 주지 않기 위한 지연"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def extract_hanja_info(self, soup: BeautifulSoup) -> Dict:
        """각 사이트별로 구현해야 하는 메서드"""
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def search_hanja(self, hanja: str) -> Dict:
        """각 사이트별로 구현해야 하는 메서드"""
        raise NotImplementedError("This method must be implemented by subclasses") 