import chardet

def detect_encoding(file_path):
    # 파일의 처음 1000바이트를 읽어서 인코딩 감지
    with open(file_path, 'rb') as f:
        raw_data = f.read(1000)
        result = chardet.detect(raw_data)
        print(f"파일: {file_path}")
        print(f"감지된 인코딩: {result['encoding']}")
        print(f"신뢰도: {result['confidence']}")
        print("첫 100바이트:", raw_data[:100])
        print("-" * 80)

# 첫 번째 파일의 인코딩 확인
detect_encoding('data/raw/1435291_5000.xml') 