import mysql.connector
from mysql.connector import Error
from tabulate import tabulate  # pip install tabulate


def connect_and_query():
    try:
        # 데이터베이스 연결 설정
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database="sakila",
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

        # 특정 테이블의 데이터 조회 예시
        table_name = "actor"
        columns_to_select = [
            "actor_id",
            "last_name",
            "first_name",
            "last_update",
        ]  # 원하는 컬럼 이름을 지정

        # 선택한 컬럼으로 쿼리 생성
        query = f"SELECT {', '.join(columns_to_select)} FROM {table_name}"
        cursor.execute(query)

        # 컬럼 이름 가져오기
        column_names = [i[0] for i in cursor.description]

        # 결과 가져오기
        rows = cursor.fetchall()

        print(f"\n{table_name} 테이블의 데이터:")
        # tabulate를 사용하여 테이블 형식으로 출력
        print(tabulate(rows, headers=column_names, tablefmt="pretty"))
    except Error as e:
        print(f"Error: {e}")

    finally:
        # 연결 종료
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 연결이 종료되었습니다.")


if __name__ == "__main__":
    connect_and_query()