import sqlite3

def count_hanja():
    # 데이터베이스 연결
    conn = sqlite3.connect('data/processed/hanja_dictionary.db')
    cursor = conn.cursor()
    
    # 한자 수 확인
    cursor.execute('SELECT COUNT(*) FROM hanja')
    total_hanja = cursor.fetchone()[0]
    
    # 한자-단어 관계 수 확인
    cursor.execute('SELECT COUNT(*) FROM hanja_word')
    total_words = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"총 한자 수: {total_hanja}")
    print(f"총 단어 수: {total_words}")

if __name__ == "__main__":
    count_hanja() 