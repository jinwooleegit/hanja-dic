import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
from unidecode import unidecode
import json
from functools import lru_cache

# 데이터 저장 디렉토리
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 캐시 파일 경로
CACHE_FILE = os.path.join(DATA_DIR, 'hanja_cache.json')

# 캐시 로드
try:
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

@lru_cache(maxsize=1000)
def fetch_hanja_data(hanja):
    """한자 데이터를 가져오는 함수"""
    # 캐시 확인
    if hanja in cache:
        return cache[hanja]
    
    url = f"https://hanja.dict.naver.com/api3/ccko/search?query={hanja}&mode=pc&hanja_reading=asseum&hanjaId=0&user_id=&m31Shn=false&shouldSearchOnlineDict=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://hanja.dict.naver.com/',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 한자 정보 추출
        hanja_info = {
            '한자': hanja,
            '음': '',
            '훈': '',
            '부수': '',
            '총획수': '',
            '설명': ''
        }
        
        if data and 'searchResultMap' in data:
            result = data['searchResultMap']
            if 'searchResultListMap' in result and result['searchResultListMap']:
                items = result['searchResultListMap'].get('items', [])
                if items:
                    item = items[0]  # 첫 번째 결과 사용
                    
                    # 음과 훈 추출
                    if 'reading' in item:
                        reading = item['reading']
                        if 'sound' in reading:
                            hanja_info['음'] = reading['sound']
                        if 'meaning' in reading:
                            hanja_info['훈'] = reading['meaning']
                    
                    # 부수와 총획수 추출
                    if 'radical' in item:
                        hanja_info['부수'] = item['radical']
                    if 'stroke_count' in item:
                        hanja_info['총획수'] = str(item['stroke_count'])
                    
                    # 설명 추출
                    if 'meaning' in item:
                        meanings = item.get('meaning', [])
                        if meanings:
                            hanja_info['설명'] = ' '.join(meanings)
        
        # 캐시에 저장
        cache[hanja] = hanja_info
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        
        return hanja_info
    
    except Exception as e:
        print(f"Error fetching data for {hanja}: {str(e)}")
        # 디버깅을 위해 응답 저장
        if hasattr(response, 'text'):
            with open(os.path.join(DATA_DIR, f'debug_{hanja}.json'), 'w', encoding='utf-8') as f:
                f.write(response.text)
        return None

def main():
    # 한자 목록 파일 읽기
    with open('hanja_list.txt', 'r', encoding='utf-8') as f:
        hanja_list = f.read().strip()
    
    # 데이터 저장할 리스트
    data = []
    
    # 각 한자에 대해 데이터 수집
    for hanja in hanja_list:
        if hanja.strip():  # 빈 줄 건너뛰기
            print(f"Fetching data for {hanja}...")
            hanja_data = fetch_hanja_data(hanja)
            if hanja_data:
                data.append(hanja_data)
            time.sleep(2)  # 서버 부하 방지
    
    # 데이터프레임 생성 및 저장
    if data:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, 'hanja_data.csv'), index=False, encoding='utf-8-sig')
        print("Data collection completed!")
        print(f"Total characters processed: {len(data)}")
    else:
        print("No data was collected!")

if __name__ == "__main__":
    main() 