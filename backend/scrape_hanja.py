import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random
import logging

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 스크래핑할 한자 수준별 목록 URL (예: 한국어 기초 한자)
SCRAPE_URLS = [
    "https://hanja.dict.naver.com/level/1",  # 초등 1~2학년
    "https://hanja.dict.naver.com/level/2",  # 초등 3~4학년
    "https://hanja.dict.naver.com/level/3",  # 초등 5~6학년
    "https://hanja.dict.naver.com/level/4",  # 중학교
    "https://hanja.dict.naver.com/level/5",  # 고등학교
]

# 한자 상세 정보 URL 포맷
DETAIL_URL = "https://hanja.dict.naver.com/hanja?q={}"

# User-Agent 목록 (차단 방지)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def create_db_connection():
    """SQLite 데이터베이스 연결 생성"""
    try:
        conn = sqlite3.connect('app.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"데이터베이스 연결 오류: {e}")
        raise

def get_existing_hanja():
    """데이터베이스에 있는 한자 목록 가져오기"""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT traditional FROM hanja")
    results = cursor.fetchall()
    conn.close()
    return [row['traditional'] for row in results]

def scrape_hanja_list(url):
    """한자 목록 페이지에서 한자 링크 추출"""
    headers = {'User-Agent': get_random_user_agent()}
    
    try:
        logger.info(f"URL 요청 중: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        hanja_links = soup.select('.hanja_list a')
        
        hanja_chars = []
        for link in hanja_links:
            hanja_char = link.text.strip()
            if hanja_char and len(hanja_char) == 1:
                hanja_chars.append(hanja_char)
        
        logger.info(f"{len(hanja_chars)}개 한자 찾음")
        return hanja_chars
    
    except requests.exceptions.RequestException as e:
        logger.error(f"URL 요청 오류: {e}")
        return []

def scrape_hanja_details(hanja_char):
    """한자 상세 정보 페이지에서 데이터 추출"""
    headers = {'User-Agent': get_random_user_agent()}
    url = DETAIL_URL.format(hanja_char)
    
    try:
        logger.info(f"한자 상세 정보 요청 중: {hanja_char}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 기본 정보 섹션 찾기
        info_section = soup.select_one('.hanja_mean')
        if not info_section:
            logger.warning(f"한자 정보를 찾을 수 없음: {hanja_char}")
            return None
        
        # 한자 데이터 추출
        data = {
            'traditional': hanja_char,
            'simplified': None,
            'korean_pronunciation': None,
            'chinese_pronunciation': None,
            'japanese_pronunciation': None,
            'meaning': None,
            'radical': None,
            'stroke_count': None,
            'examples': None,
            'frequency': random.randint(1, 100)  # 임의의 빈도수 (실제로는 더 정확한 정보 필요)
        }
        
        # 발음 정보
        pronunciation_section = soup.select_one('.pronunciation')
        if pronunciation_section:
            korean_pron = pronunciation_section.select_one('.korean')
            if korean_pron:
                data['korean_pronunciation'] = korean_pron.text.strip()
            
            chinese_pron = pronunciation_section.select_one('.chinese')
            if chinese_pron:
                data['chinese_pronunciation'] = chinese_pron.text.strip()
        
        # 뜻 정보
        meaning_section = soup.select_one('.mean_list')
        if meaning_section:
            meanings = meaning_section.select('li')
            if meanings:
                data['meaning'] = ', '.join([m.text.strip() for m in meanings])
        
        # 부수 및 획수 정보
        info_items = soup.select('.sub_h_list li')
        for item in info_items:
            text = item.text.strip()
            if '부수' in text:
                data['radical'] = text.split('：')[-1].strip()
            elif '총획' in text:
                try:
                    data['stroke_count'] = int(text.split('：')[-1].strip())
                except ValueError:
                    pass
        
        # 예문 정보
        example_section = soup.select('.example .example_mean')
        if example_section:
            examples = []
            for ex in example_section[:3]:  # 최대 3개 예문만 가져오기
                examples.append(ex.text.strip())
            if examples:
                data['examples'] = '\n'.join(examples)
        
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"한자 상세 정보 요청 오류: {e}")
        return None

def save_hanja_to_db(hanja_data):
    """한자 데이터를 데이터베이스에 저장"""
    if not hanja_data:
        return False
    
    conn = create_db_connection()
    cursor = conn.cursor()
    
    try:
        # 이미 존재하는지 확인
        cursor.execute("SELECT COUNT(*) FROM hanja WHERE traditional = ?", (hanja_data['traditional'],))
        count = cursor.fetchone()[0]
        
        if count > 0:
            logger.info(f"한자 업데이트: {hanja_data['traditional']}")
            
            # 업데이트 쿼리 구성
            update_fields = []
            update_values = []
            
            for key, value in hanja_data.items():
                if key != 'traditional' and value is not None:
                    update_fields.append(f"{key} = ?")
                    update_values.append(value)
            
            if update_fields:
                update_values.append(hanja_data['traditional'])
                cursor.execute(
                    f"UPDATE hanja SET {', '.join(update_fields)} WHERE traditional = ?",
                    update_values
                )
        else:
            logger.info(f"새 한자 추가: {hanja_data['traditional']}")
            
            # 필드 및 값 구성
            fields = []
            placeholders = []
            values = []
            
            for key, value in hanja_data.items():
                if value is not None:
                    fields.append(key)
                    placeholders.append('?')
                    values.append(value)
            
            cursor.execute(
                f"INSERT INTO hanja ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                values
            )
        
        conn.commit()
        return True
    
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"데이터베이스 저장 오류: {e}")
        return False
    
    finally:
        conn.close()

def main():
    """한자 스크래핑 메인 함수"""
    logger.info("한자 스크래핑 시작")
    
    # 이미 있는 한자 목록 가져오기
    existing_hanja = get_existing_hanja()
    logger.info(f"기존 한자 수: {len(existing_hanja)}")
    
    # 목표 한자 수를 1800으로 설정
    target_count = 1800
    current_count = len(existing_hanja)
    
    for url in SCRAPE_URLS:
        if current_count >= target_count:
            break
        
        # 한자 목록 스크래핑
        hanja_chars = scrape_hanja_list(url)
        
        # 중복 제거
        hanja_chars = [char for char in hanja_chars if char not in existing_hanja]
        
        for hanja_char in hanja_chars:
            if current_count >= target_count:
                break
            
            # 한자 상세 정보 스크래핑
            hanja_data = scrape_hanja_details(hanja_char)
            
            # 데이터베이스에 저장
            if hanja_data and save_hanja_to_db(hanja_data):
                current_count += 1
                logger.info(f"진행 상황: {current_count}/{target_count} ({(current_count/target_count*100):.1f}%)")
                
                # 서버 부하 방지를 위한 대기 시간 (0.5초)
                time.sleep(0.5)
    
    logger.info("한자 스크래핑 완료")
    logger.info(f"최종 한자 수: {current_count}")

if __name__ == "__main__":
    main() 