import os
import sys
from pathlib import Path
import sqlite3
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 프로젝트 경로 설정
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# 데이터베이스 파일 경로
DB_PATH = os.path.join(project_root, "app.db")
logger.info(f"데이터베이스 파일 경로: {DB_PATH}")

# 샘플 한자 데이터
SAMPLE_HANJA = [
    {
        "traditional": "一",
        "simplified": "一",
        "korean_pronunciation": "일",
        "chinese_pronunciation": "yī",
        "radical": "一",
        "stroke_count": 1,
        "meaning": "하나 일",
        "examples": "一日(일일): 하루\n一年(일년): 일 년",
        "frequency": 500
    },
    {
        "traditional": "二",
        "simplified": "二",
        "korean_pronunciation": "이",
        "chinese_pronunciation": "èr",
        "radical": "二",
        "stroke_count": 2,
        "meaning": "두 이",
        "examples": "二月(이월): 2월\n二人(이인): 두 사람",
        "frequency": 450
    },
    {
        "traditional": "三",
        "simplified": "三",
        "korean_pronunciation": "삼",
        "chinese_pronunciation": "sān",
        "radical": "一",
        "stroke_count": 3,
        "meaning": "셋 삼",
        "examples": "三國(삼국): 세 나라\n三角(삼각): 삼각형",
        "frequency": 430
    },
    {
        "traditional": "四",
        "simplified": "四",
        "korean_pronunciation": "사",
        "chinese_pronunciation": "sì",
        "radical": "囗",
        "stroke_count": 5,
        "meaning": "넉 사",
        "examples": "四月(사월): 4월\n四角(사각): 네모",
        "frequency": 400
    },
    {
        "traditional": "五",
        "simplified": "五",
        "korean_pronunciation": "오",
        "chinese_pronunciation": "wǔ",
        "radical": "二",
        "stroke_count": 4,
        "meaning": "다섯 오",
        "examples": "五月(오월): 5월\n五感(오감): 다섯 가지 감각",
        "frequency": 380
    },
    {
        "traditional": "六",
        "simplified": "六",
        "korean_pronunciation": "육",
        "chinese_pronunciation": "liù",
        "radical": "八",
        "stroke_count": 4,
        "meaning": "여섯 육",
        "examples": "六月(육월): 6월\n六角(육각): 육각형",
        "frequency": 350
    },
    {
        "traditional": "七",
        "simplified": "七",
        "korean_pronunciation": "칠",
        "chinese_pronunciation": "qī",
        "radical": "一",
        "stroke_count": 2,
        "meaning": "일곱 칠",
        "examples": "七月(칠월): 7월\n七色(칠색): 일곱 가지 색",
        "frequency": 330
    },
    {
        "traditional": "八",
        "simplified": "八",
        "korean_pronunciation": "팔",
        "chinese_pronunciation": "bā",
        "radical": "八",
        "stroke_count": 2,
        "meaning": "여덟 팔",
        "examples": "八月(팔월): 8월\n八角(팔각): 팔각형",
        "frequency": 320
    },
    {
        "traditional": "九",
        "simplified": "九",
        "korean_pronunciation": "구",
        "chinese_pronunciation": "jiǔ",
        "radical": "乙",
        "stroke_count": 2,
        "meaning": "아홉 구",
        "examples": "九月(구월): 9월\n九分(구분): 아홉 부분",
        "frequency": 310
    },
    {
        "traditional": "十",
        "simplified": "十",
        "korean_pronunciation": "십",
        "chinese_pronunciation": "shí",
        "radical": "十",
        "stroke_count": 2,
        "meaning": "열 십",
        "examples": "十月(시월): 10월\n十年(십년): 십 년",
        "frequency": 300
    },
    {
        "traditional": "水",
        "simplified": "水",
        "korean_pronunciation": "수",
        "chinese_pronunciation": "shuǐ",
        "radical": "水",
        "stroke_count": 4,
        "meaning": "물 수",
        "examples": "水洗(수세): 물로 씻다\n水上(수상): 물 위",
        "frequency": 280
    },
    {
        "traditional": "火",
        "simplified": "火",
        "korean_pronunciation": "화",
        "chinese_pronunciation": "huǒ",
        "radical": "火",
        "stroke_count": 4,
        "meaning": "불 화",
        "examples": "火山(화산): 화산\n火災(화재): 화재",
        "frequency": 270
    },
    {
        "traditional": "山",
        "simplified": "山",
        "korean_pronunciation": "산",
        "chinese_pronunciation": "shān",
        "radical": "山",
        "stroke_count": 3,
        "meaning": "메 산",
        "examples": "山水(산수): 산과 물\n登山(등산): 등산",
        "frequency": 250
    },
    {
        "traditional": "風",
        "simplified": "风",
        "korean_pronunciation": "풍",
        "chinese_pronunciation": "fēng",
        "radical": "風",
        "stroke_count": 9,
        "meaning": "바람 풍",
        "examples": "風景(풍경): 풍경\n風車(풍차): 풍차",
        "frequency": 230
    },
    {
        "traditional": "雨",
        "simplified": "雨",
        "korean_pronunciation": "우",
        "chinese_pronunciation": "yǔ",
        "radical": "雨",
        "stroke_count": 8,
        "meaning": "비 우",
        "examples": "雨水(우수): 빗물\n大雨(대우): 큰 비",
        "frequency": 220
    }
]

def add_sample_data():
    """샘플 한자 데이터를 데이터베이스에 추가합니다."""
    logger.info("샘플 데이터 추가 시작...")
    
    # 데이터베이스 파일 존재 확인
    if not os.path.exists(DB_PATH):
        logger.error(f"데이터베이스 파일이 존재하지 않습니다: {DB_PATH}")
        logger.error("먼저 init_db.py 스크립트를 실행해 데이터베이스를 초기화해주세요.")
        return False
    
    try:
        # SQLite 연결
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 기존 데이터 확인
        cursor.execute("SELECT COUNT(*) FROM hanja")
        count = cursor.fetchone()[0]
        logger.info(f"현재 데이터베이스에 {count}개의 한자가 있습니다.")
        
        # 데이터 삽입
        added_count = 0
        skipped_count = 0
        
        for hanja in SAMPLE_HANJA:
            # 이미 존재하는지 확인
            cursor.execute("SELECT COUNT(*) FROM hanja WHERE traditional = ?", (hanja["traditional"],))
            exists = cursor.fetchone()[0] > 0
            
            if exists:
                logger.info(f"'{hanja['traditional']}' 이미 존재합니다. 건너뜁니다.")
                skipped_count += 1
                continue
            
            # 필드 목록과 값 목록 생성
            fields = hanja.keys()
            values = [hanja[field] for field in fields]
            
            # SQL 쿼리 생성
            placeholders = ", ".join(["?"] * len(fields))
            field_names = ", ".join(fields)
            
            # 삽입 쿼리 실행
            sql = f"INSERT INTO hanja ({field_names}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            
            logger.info(f"'{hanja['traditional']}' 추가 완료!")
            added_count += 1
        
        # 변경사항 커밋
        conn.commit()
        
        # 결과 확인
        cursor.execute("SELECT COUNT(*) FROM hanja")
        new_count = cursor.fetchone()[0]
        
        logger.info(f"샘플 데이터 추가 완료!")
        logger.info(f"추가됨: {added_count}, 건너뜀: {skipped_count}")
        logger.info(f"전체 한자 수: {new_count}")
        
        return True
    
    except Exception as e:
        logger.error(f"샘플 데이터 추가 중 오류 발생: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = add_sample_data()
    if success:
        logger.info("샘플 데이터 추가 성공!")
    else:
        logger.error("샘플 데이터 추가 실패.")
        sys.exit(1) 