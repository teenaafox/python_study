import mysql.connector  # pip install mysql-connector-python

def connect_and_query():
    try:
        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host="localhost", port=3306, user="root", password="p0o9i8", database="sakila"
        )

        # 커서 생성
        cursor = connection.cursor()

        # SQL 쿼리 실행 (예: 모든 테이블 목록 조회)
        cursor.execute("SHOW TABLES")

        # 결과 가져오기
        tables = cursor.fetchall()

        # 결과 출력
        print("데이터베이스의 테이블 목록:")
        for table in tables:
            print(table[0])

        # dictionary=True 옵션으로 커서 생성
        cursor = connection.cursor(dictionary=True)

        # 특정 테이블의 데이터 조회 예시
        table_name = "actor"
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")

        rows = cursor.fetchall()

        print(f"\n{table_name} 테이블의 데이터:")
        for row in rows:
            last_update = row["last_update"].strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
            print(
                f'{row["actor_id"]} | {row["last_name"]} | {row["first_name"]} | {last_update}'
            )

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        # 연결 종료
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 연결이 종료되었습니다.")


if __name__ == "__main__":
    connect_and_query()