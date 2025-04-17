import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 한자 테이블 조회
cursor.execute('SELECT traditional, korean_pronunciation, meaning FROM hanja')
rows = cursor.fetchall()

print('총 한자 수:', len(rows))
print('한자 목록:')
for row in rows:
    print(f'{row[0]} ({row[1]}) - {row[2]}')

# 연결 종료
conn.close() 