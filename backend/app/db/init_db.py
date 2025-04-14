from app.db.base import Base, engine
from app.models.hanja import Hanja

def init_db():
    # 테이블 생성
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("데이터베이스 테이블을 생성합니다...")
    init_db()
    print("데이터베이스 테이블 생성이 완료되었습니다.") 