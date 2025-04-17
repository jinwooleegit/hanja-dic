import requests
import json

# API 엔드포인트
BASE_URL = "http://127.0.0.1:8000/api"

# 테스트 단어 추가
def test_add_word():
    word_data = {
        "word": "사랑",
        "pronunciation": "sa-rang",
        "part_of_speech": "명사",
        "meaning": "남을 아끼고 귀여워하는 마음",
        "example": "사랑은 아름다운 감정이다."
    }
    
    response = requests.post(f"{BASE_URL}/words/", json=word_data)
    print("단어 추가 응답:", response.json())
    return response.json().get("word_id")

# 테스트 단어 검색
def test_search_word(word):
    response = requests.get(f"{BASE_URL}/words/{word}")
    print("검색 결과:", response.json())

if __name__ == "__main__":
    # 단어 추가 테스트
    word_id = test_add_word()
    
    # 단어 검색 테스트
    test_search_word("사랑") 