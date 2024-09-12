
import mysql.connector

# MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="sakila"
)

# 커서 생성
cursor = db.cursor()


# 테이블 생성 함수
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
    )
    """
    cursor.execute(sql)
    print("Users 테이블이 생성되었습니다.")


# 테이블 삭제 함수
def drop_table():
    sql = "DROP TABLE IF EXISTS users"
    cursor.execute(sql)
    print("Users 테이블이 삭제되었습니다.")


# INSERT 예제
def insert_data(name, age):
    sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
    values = (name, age)
    cursor.execute(sql, values)
    db.commit()
    print(f"{cursor.rowcount} record inserted. (name: {name}, age: {age})")


# UPDATE 예제
def update_data(id, new_age):
    sql = "UPDATE users SET age = %s WHERE id = %s"
    values = (new_age, id)
    cursor.execute(sql, values)
    db.commit()
    print(f"{cursor.rowcount} record(s) affected. Updated age to {new_age} for id {id}")


# DELETE 예제
def delete_data(id):
    sql = "DELETE FROM users WHERE id = %s"
    value = (id,)
    cursor.execute(sql, value)
    db.commit()
    print(f"{cursor.rowcount} record(s) deleted. (id: {id})")


# SELECT 및 출력 함수
def select_and_print():
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    results = cursor.fetchall()

    print("\n현재 users 테이블 내용:")
    if not results:
        print("테이블이 비어 있습니다.")
    else:
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    print()  # 빈 줄 추가


# 메인 프로그램
def main():
    try:
        # 테이블 생성
        create_table()

        # INSERT 작업 및 결과 출력
        insert_data("John Doe", 30)
        select_and_print()

        insert_data("Jane Smith", 25)
        select_and_print()

        # UPDATE 작업 및 결과 출력
        update_data(1, 31)
        select_and_print()

        # DELETE 작업 및 결과 출력
        delete_data(2)
        select_and_print()

    finally:
        # 프로그램 종료 시 테이블 삭제
        # drop_table()

        # 연결 종료
        db.close()


if __name__ == "__main__":
    main()
