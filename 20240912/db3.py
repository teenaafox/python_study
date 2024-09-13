import mysql.connector

# MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost", user="root", password="p0o9i8", database="sakila"
)

# 커서 생성
cursor = db.cursor()

#테이블 생성 함수
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
    
