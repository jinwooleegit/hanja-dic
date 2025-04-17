# 한자 사전 데이터베이스 (Hanja Dictionary)

한국인을 위한 포괄적인 한자 사전 데이터베이스입니다. 이 프로젝트는 한자의 검색, 학습, 그리고 이해를 돕기 위한 도구를 제공합니다.

## 🌟 주요 기능

* **한자 검색**
  * 번체자 기반 검색
  * 간체자 병기
  * 부수, 획수로 검색
  * 한글/중국어 발음으로 검색

* **상세 정보**
  * 한자의 의미와 용례
  * 부수와 획수 정보
  * 한글/중국어 발음
  * 관련 예문 제공

* **학습 도구**
  * 자주 사용되는 한자 목록
  * 학습 진도 추적
  * 퀴즈 기능

## 🚀 시작하기

### 필수 요구사항

* Python 3.8 이상
* PostgreSQL 12 이상
* Node.js 14 이상

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/jinwooleegit/hanja-dic.git
cd hanja-dic
```

2. **가상환경 설정**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **데이터베이스 설정**
```bash
# PostgreSQL 데이터베이스 생성
createdb hanja_db

# 데이터베이스 마이그레이션
python create_db.py
```

5. **데이터 가져오기**
```bash
python import_hanja.py
```

6. **서버 실행**
```bash
# 백엔드 서버 실행
cd backend
uvicorn main:app --reload

# 프론트엔드 실행 (새 터미널에서)
cd frontend
npm install
npm start
```

## 📚 사용 방법

1. 웹 브라우저에서 `http://localhost:3000` 접속
2. 검색창에 한자, 부수, 획수 등을 입력하여 검색
3. 검색 결과에서 원하는 한자를 클릭하여 상세 정보 확인
4. 학습 기능을 활용하여 한자 학습 진행

## 🛠 기술 스택

* **백엔드**
  * Python
  * FastAPI
  * PostgreSQL
  * SQLAlchemy

* **프론트엔드**
  * React
  * TypeScript
  * Tailwind CSS

## 🤝 기여하기

1. 이슈 생성
2. Fork 후 개발
3. Pull Request 생성

## 📝 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 문의

* 이슈 생성
* 이메일: [이메일 주소]

## 🙏 감사의 말

이 프로젝트는 다음과 같은 오픈소스 프로젝트의 도움을 받았습니다:
* [FastAPI](https://fastapi.tiangolo.com/)
* [React](https://reactjs.org/)
* [PostgreSQL](https://www.postgresql.org/) 