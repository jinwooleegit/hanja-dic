# backend/scripts/populate_db.py
import asyncio
import logging
import sys
import os
import sqlite3
from pathlib import Path
import time

# --- 로깅 설정 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 프로젝트 경로 설정 --- 
project_root = Path(__file__).resolve().parents[1] 
backend_root = project_root
if str(backend_root) not in sys.path:
    sys.path.append(str(backend_root))
logger.info(f"프로젝트 경로 추가: {backend_root}")

# --- 데이터베이스 파일 경로 ---
DB_PATH = os.path.join(project_root, "app.db")
logger.info(f"데이터베이스 파일 경로: {DB_PATH}")

# --- 필요한 모듈 임포트 시도 --- 
try:
    from app.scrapers.scraper_manager import scraper_manager # 싱글톤 인스턴스
    # tqdm 임포트 시도 (선택 사항)
    try:
        from tqdm import tqdm
    except ImportError:
        tqdm = None
        logger.info("tqdm 라이브러리가 설치되지 않았습니다. 진행률 표시줄 없이 실행됩니다.")
        logger.info("진행률 표시줄을 보려면 'pip install tqdm'을 실행하세요.")
except ImportError as e:
     logger.error(f"모듈 임포트 오류: {e}. 가상환경이 활성화되었는지, 스크립트 실행 위치가 올바른지 확인하세요.")
     logger.error(f"현재 sys.path: {sys.path}")
     sys.exit(1)
except Exception as e:
    logger.error(f"모듈 임포트 중 예상치 못한 오류: {e}")
    sys.exit(1)


# --- 스크레이핑 대상 한자 목록 --- 
# 한국어 교육용 한자 1800자 중 일부 (여기서는 예시로 10자만 포함)
HANJA_TO_SCRAPE = [
    # 기초 한자
    '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'
]

# --- 설정 --- 
REQUEST_DELAY = 1 # 각 한자 스크레이핑 사이의 지연 시간 (초). 웹사이트 부하 감소 목적.

def get_db_connection():
    """SQLite 데이터베이스 연결을 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 결과를 딕셔너리 형태로 반환
    return conn

async def populate_single_hanja(character: str, pbar=None):
    """단일 한자를 처리하는 비동기 함수"""
    current_task_desc = f"처리 중: {character}"
    if pbar: pbar.set_description(current_task_desc)
    else: logger.info(current_task_desc)

    try:
        # 1. 데이터베이스에서 존재 여부 확인
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM hanja WHERE traditional = ?", (character,))
            existing_hanja = cursor.fetchone()
            if existing_hanja:
                logger.info(f"'{character}' DB에 이미 존재. 건너뜁니다.")
                if pbar: pbar.update(1)
                return 'skipped'
        finally:
            conn.close()

        # 2. 스크레이핑 실행
        logger.info(f"'{character}' 데이터 스크레이핑 시작...")
        # 비동기 검색 호출
        scraped_data = await scraper_manager.search_hanja_async(character)

        # 3. 데이터 검증 및 저장
        if scraped_data and 'traditional' in scraped_data:
            logger.info(f"'{character}' 데이터 수집 완료. DB 저장 시도...")
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # 필수 필드 확인
                required_fields = ['traditional', 'korean_pronunciation', 'meaning']
                if not all(field in scraped_data and scraped_data[field] for field in required_fields):
                    logger.warning(f"'{character}' 필수 데이터 부족: {scraped_data}. 저장하지 않습니다.")
                    if pbar: pbar.update(1)
                    return 'error_validation'
                
                # 데이터베이스에 저장할 필드와 값 준비
                fields = [
                    'traditional', 'simplified', 'korean_pronunciation', 'chinese_pronunciation',
                    'radical', 'stroke_count', 'meaning', 'examples', 'frequency'
                ]
                
                # 없는 필드는 None으로 설정
                values = [scraped_data.get(field) for field in fields]
                
                # SQL 쿼리 준비
                placeholders = ', '.join(['?'] * len(fields))
                field_names = ', '.join(fields)
                
                # 삽입 쿼리 실행
                query = f"INSERT INTO hanja ({field_names}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
                
                logger.info(f"'{character}' DB 저장 성공.")
                if pbar: pbar.update(1)
                return 'added'
            except Exception as db_err:
                logger.error(f"'{character}' DB 저장 오류: {db_err}")
                conn.rollback()
                if pbar: pbar.update(1)
                return 'error_db'
            finally:
                conn.close()
        else:
            logger.warning(f"'{character}' 데이터 수집 실패 또는 유효하지 않음.")
            if pbar: pbar.update(1)
            return 'error_scrape'

    except Exception as e:
        logger.error(f"'{character}' 처리 중 예상치 못한 오류: {e}")
        if pbar: pbar.update(1)
        return 'error_unknown'
    finally:
        # 다음 요청 전 지연
        logger.debug(f"'{character}' 처리 완료. 다음 요청까지 {REQUEST_DELAY}초 대기...")
        await asyncio.sleep(REQUEST_DELAY)

async def process_batch(batch, results_summary):
    """배치로 한자를 처리하는 함수"""
    tasks = [populate_single_hanja(char) for char in batch]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in results:
        if isinstance(result, str) and result in results_summary:
            results_summary[result] += 1
        elif isinstance(result, Exception):
            logger.error(f"한자 처리 중 예외 발생: {result}")
            results_summary['error_unknown'] += 1
        else:
            results_summary['error_unknown'] += 1
            logger.error(f"처리 중 예상치 못한 결과: {result}")

async def main():
    logger.info("===== 한자 데이터베이스 채우기 스크립트 시작 =====")
    start_time = time.time()

    # 데이터베이스 파일 존재 확인
    if not os.path.exists(DB_PATH):
        logger.error(f"데이터베이스 파일이 존재하지 않습니다: {DB_PATH}")
        logger.error("먼저 init_db.py 스크립트를 실행해 데이터베이스를 초기화해주세요.")
        return

    hanja_list = HANJA_TO_SCRAPE
    total_hanja = len(hanja_list)
    logger.info(f"총 {total_hanja}개의 한자를 처리합니다.")

    results_summary = {'added': 0, 'skipped': 0, 'error_validation': 0, 'error_db': 0, 'error_scrape': 0, 'error_unknown': 0}

    # 배치 크기 설정 (동시에 처리할 최대 한자 수)
    batch_size = 5
    
    # 한자 목록을 배치로 분할
    for i in range(0, total_hanja, batch_size):
        batch = hanja_list[i:i+batch_size]
        batch_start = i + 1
        batch_end = min(i + batch_size, total_hanja)
        logger.info(f"배치 처리 중: {batch_start}-{batch_end}/{total_hanja}")
        
        # 배치 처리
        await process_batch(batch, results_summary)
        
        # 배치 처리 결과 중간 보고
        logger.info(f"현재까지 처리 결과: 추가됨={results_summary['added']}, 건너뜀={results_summary['skipped']}, 오류={results_summary['error_validation'] + results_summary['error_db'] + results_summary['error_scrape'] + results_summary['error_unknown']}")

    end_time = time.time()
    duration = end_time - start_time
    logger.info("===== 데이터베이스 채우기 완료 =====")
    logger.info(f"총 처리 시간: {duration:.2f} 초")
    logger.info(f"처리 결과: 추가됨={results_summary['added']}, 건너뜀={results_summary['skipped']}, 유효성오류={results_summary['error_validation']}, DB오류={results_summary['error_db']}, 스크랩오류={results_summary['error_scrape']}, 기타오류={results_summary['error_unknown']}")

if __name__ == "__main__":
    # Windows에서 asyncio 정책 설정 (필요한 경우)
    if sys.platform == "win32" and sys.version_info >= (3, 8):
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main()) 