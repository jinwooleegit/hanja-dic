import sqlite3
import logging
import random

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 추가할 한자 데이터 목록
ADDITIONAL_HANJA = [
    # 시간 관련 한자
    {
        'traditional': '時', 'korean_pronunciation': '시', 
        'meaning': '때 시', 'stroke_count': 10, 
        'examples': '時間(시간): 시간\n時計(시계): 시계\n時代(시대): 시대'
    },
    {
        'traditional': '間', 'korean_pronunciation': '간', 
        'meaning': '사이 간', 'stroke_count': 12, 
        'examples': '時間(시간): 시간\n人間(인간): 인간\n中間(중간): 중간'
    },
    {
        'traditional': '日', 'korean_pronunciation': '일', 
        'meaning': '날 일', 'stroke_count': 4, 
        'examples': '日本(일본): 일본\n今日(금일): 오늘\n日曜日(일요일): 일요일'
    },
    {
        'traditional': '月', 'korean_pronunciation': '월', 
        'meaning': '달 월', 'stroke_count': 4, 
        'examples': '月曜日(월요일): 월요일\n今月(금월): 이번 달\n月光(월광): 달빛'
    },
    {
        'traditional': '年', 'korean_pronunciation': '년', 
        'meaning': '해 년', 'stroke_count': 6, 
        'examples': '今年(금년): 올해\n年齡(연령): 연령\n少年(소년): 소년'
    },
    
    # 방향 관련 한자
    {
        'traditional': '東', 'korean_pronunciation': '동', 
        'meaning': '동녘 동', 'stroke_count': 8, 
        'examples': '東洋(동양): 동양\n東方(동방): 동방\n東海(동해): 동해'
    },
    {
        'traditional': '西', 'korean_pronunciation': '서', 
        'meaning': '서녘 서', 'stroke_count': 6, 
        'examples': '西洋(서양): 서양\n東西(동서): 동서\n西海(서해): 서해'
    },
    {
        'traditional': '南', 'korean_pronunciation': '남', 
        'meaning': '남녘 남', 'stroke_count': 9, 
        'examples': '南方(남방): 남방\n南北(남북): 남북\n南美(남미): 남미'
    },
    {
        'traditional': '北', 'korean_pronunciation': '북', 
        'meaning': '북녘 북', 'stroke_count': 5, 
        'examples': '北方(북방): 북방\n南北(남북): 남북\n北韓(북한): 북한'
    },
    
    # 자연 관련 한자
    {
        'traditional': '天', 'korean_pronunciation': '천', 
        'meaning': '하늘 천', 'stroke_count': 4, 
        'examples': '天氣(천기): 날씨\n天國(천국): 천국\n天然(천연): 천연'
    },
    {
        'traditional': '地', 'korean_pronunciation': '지', 
        'meaning': '땅 지', 'stroke_count': 6, 
        'examples': '地球(지구): 지구\n地方(지방): 지방\n地下(지하): 지하'
    },
    {
        'traditional': '人', 'korean_pronunciation': '인', 
        'meaning': '사람 인', 'stroke_count': 2, 
        'examples': '人間(인간): 인간\n人類(인류): 인류\n他人(타인): 타인'
    },
    {
        'traditional': '木', 'korean_pronunciation': '목', 
        'meaning': '나무 목', 'stroke_count': 4, 
        'examples': '木材(목재): 목재\n樹木(수목): 수목\n木曜日(목요일): 목요일'
    },
    {
        'traditional': '金', 'korean_pronunciation': '금', 
        'meaning': '쇠 금', 'stroke_count': 8, 
        'examples': '金曜日(금요일): 금요일\n金屬(금속): 금속\n黃金(황금): 황금'
    },
    {
        'traditional': '土', 'korean_pronunciation': '토', 
        'meaning': '흙 토', 'stroke_count': 3, 
        'examples': '土曜日(토요일): 토요일\n國土(국토): 국토\n土地(토지): 토지'
    },
    
    # 동물 관련 한자
    {
        'traditional': '馬', 'korean_pronunciation': '마', 
        'meaning': '말 마', 'stroke_count': 10, 
        'examples': '馬車(마차): 마차\n競馬(경마): 경마\n馬場(마장): 마장'
    },
    {
        'traditional': '牛', 'korean_pronunciation': '우', 
        'meaning': '소 우', 'stroke_count': 4, 
        'examples': '牛肉(우육): 쇠고기\n牛乳(우유): 우유\n牧牛(목우): 소 치기'
    },
    {
        'traditional': '羊', 'korean_pronunciation': '양', 
        'meaning': '양 양', 'stroke_count': 6, 
        'examples': '羊肉(양육): 양고기\n牧羊(목양): 양 치기\n山羊(산양): 산양'
    },
    {
        'traditional': '鳥', 'korean_pronunciation': '조', 
        'meaning': '새 조', 'stroke_count': 11, 
        'examples': '鳥類(조류): 조류\n小鳥(소조): 작은 새\n家鳥(가조): 집새'
    },
    {
        'traditional': '魚', 'korean_pronunciation': '어', 
        'meaning': '물고기 어', 'stroke_count': 11, 
        'examples': '魚類(어류): 어류\n金魚(금어): 금붕어\n海魚(해어): 바다고기'
    },
    
    # 식물 관련 한자
    {
        'traditional': '花', 'korean_pronunciation': '화', 
        'meaning': '꽃 화', 'stroke_count': 7, 
        'examples': '花園(화원): 화원\n開花(개화): 개화\n花瓶(화병): 화병'
    },
    {
        'traditional': '草', 'korean_pronunciation': '초', 
        'meaning': '풀 초', 'stroke_count': 9, 
        'examples': '草原(초원): 초원\n草木(초목): 초목\n雜草(잡초): 잡초'
    },
    {
        'traditional': '米', 'korean_pronunciation': '미', 
        'meaning': '쌀 미', 'stroke_count': 6, 
        'examples': '米飯(미반): 밥\n白米(백미): 백미\n玄米(현미): 현미'
    },
    {
        'traditional': '菜', 'korean_pronunciation': '채', 
        'meaning': '나물 채', 'stroke_count': 11, 
        'examples': '野菜(야채): 야채\n菜園(채원): 채소밭\n青菜(청채): 푸른 채소'
    },
    
    # 생활 관련 한자
    {
        'traditional': '家', 'korean_pronunciation': '가', 
        'meaning': '집 가', 'stroke_count': 10, 
        'examples': '家族(가족): 가족\n家庭(가정): 가정\n我家(아가): 우리 집'
    },
    {
        'traditional': '門', 'korean_pronunciation': '문', 
        'meaning': '문 문', 'stroke_count': 8, 
        'examples': '門戶(문호): 문호\n校門(교문): 교문\n開門(개문): 개문'
    },
    {
        'traditional': '路', 'korean_pronunciation': '로', 
        'meaning': '길 로', 'stroke_count': 13, 
        'examples': '道路(도로): 도로\n路地(로지): 골목\n一路(일로): 한길'
    },
    {
        'traditional': '車', 'korean_pronunciation': '차', 
        'meaning': '수레 차', 'stroke_count': 7, 
        'examples': '自動車(자동차): 자동차\n車道(차도): 차도\n電車(전차): 전차'
    },
    {
        'traditional': '食', 'korean_pronunciation': '식', 
        'meaning': '먹을 식', 'stroke_count': 9, 
        'examples': '食事(식사): 식사\n食物(식물): 식물\n食堂(식당): 식당'
    },
    {
        'traditional': '水', 'korean_pronunciation': '수', 
        'meaning': '물 수', 'stroke_count': 4, 
        'examples': '水曜日(수요일): 수요일\n水泳(수영): 수영\n飲水(음수): 음료수'
    }
]

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

def save_hanja_to_db(hanja_data):
    """한자 데이터를 데이터베이스에 저장"""
    conn = create_db_connection()
    cursor = conn.cursor()
    
    try:
        # 이미 존재하는지 확인
        cursor.execute("SELECT COUNT(*) FROM hanja WHERE traditional = ?", (hanja_data['traditional'],))
        count = cursor.fetchone()[0]
        
        # 없으면 추가, 있으면 건너뛰기 (덮어쓰지 않음)
        if count == 0:
            # 빈도수 추가 (1-100 사이 랜덤값)
            if 'frequency' not in hanja_data:
                hanja_data['frequency'] = random.randint(1, 100)
            
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
            
            logger.info(f"새 한자 추가: {hanja_data['traditional']}")
            conn.commit()
            return True
        else:
            logger.info(f"한자 '{hanja_data['traditional']}' 이미 존재하여 건너뜀")
            return False
    
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"데이터베이스 저장 오류 ({hanja_data['traditional']}): {e}")
        return False
    
    finally:
        conn.close()

def main():
    """추가 한자 데이터 저장 메인 함수"""
    logger.info("추가 한자 데이터 저장 시작")
    
    # 이미 있는 한자 목록 가져오기
    existing_hanja = get_existing_hanja()
    logger.info(f"기존 한자 수: {len(existing_hanja)}")
    
    # 추가할 한자 목록에서 중복 제거
    new_hanja_list = [h for h in ADDITIONAL_HANJA if h['traditional'] not in existing_hanja]
    logger.info(f"추가할 한자 수: {len(new_hanja_list)}")
    
    # 한자 데이터 저장
    added_count = 0
    for hanja_data in new_hanja_list:
        if save_hanja_to_db(hanja_data):
            added_count += 1
    
    logger.info(f"추가 한자 데이터 저장 완료. {added_count}개 한자 데이터 추가됨.")
    logger.info(f"총 한자 수: {len(existing_hanja) + added_count}개")

if __name__ == "__main__":
    main() 