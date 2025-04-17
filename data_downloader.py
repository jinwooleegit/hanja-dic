import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def download_data():
    # 데이터 저장 디렉토리 확인
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 데이터 포털 API URL (예시)
    # 실제 API URL과 인증키는 data.go.kr에서 발급받아야 합니다
    api_url = "https://api.data.go.kr/..."
    
    try:
        # API 호출 및 데이터 다운로드
        response = requests.get(api_url)
        response.raise_for_status()
        
        # CSV 파일로 저장
        output_file = os.path.join(data_dir, 'korean_culture_encyclopedia.csv')
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"데이터가 성공적으로 다운로드되었습니다: {output_file}")
        
        # 데이터 확인
        df = pd.read_csv(output_file)
        print(f"다운로드된 데이터 크기: {df.shape}")
        print("\n데이터 미리보기:")
        print(df.head())
        
    except Exception as e:
        print(f"데이터 다운로드 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    download_data() 