# 한자 사전 데이터베이스

한국인을 위한 포괄적인 한자 사전 데이터베이스입니다.

## 주요 기능

- 번체자 기반 한자 검색
- 간체자 병기
- 한글/중국어 발음 제공
- 부수, 획수 정보
- 예문 제공
- 빠른 검색 속도

## 프로젝트 구조

```
hanjaDB/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── scrapers/
│   └── main.py
├── frontend/
│   ├── public/
│   └── src/
├── requirements.txt
└── README.md
```

## 설치 및 실행

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 데이터베이스 설정
```bash
# PostgreSQL 데이터베이스 생성 및 설정
```

4. 백엔드 서버 실행
```bash
cd backend
uvicorn main:app --reload
```

5. 프론트엔드 실행
```bash
cd frontend
npm install
npm start
``` 