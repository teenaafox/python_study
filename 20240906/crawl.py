import requests     # pip install requests 필요 # pip - 파이썬에서 외부 패키지 관리 
from bs4 import BeautifulSoup  # pip install bs4  # 문서 읽고 특정 위치 내용을 끄집어 내는 역할

# 웹 서버에 요청을 보낼 때 사용할 HTTP 헤더를 정의
# User-Agent 값을 지정해 브라우저(Chrome)로부터 요청이 온 것처럼 속인다.
# 웹 서버는 User-Agent 값을 기반으로 요청을 구분할 수 있으며, 이를 통해 스크래핑을 방지하거나 허용
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

# requests.get()을 사용해 네이버 메인 페이지(https://www.naver.com)의 HTML 데이터를 가져온다
# 여기서 headers를 함께 사용해 서버가 정상적인 브라우저 요청으로 인식하도록 한다
data = requests.get("https://www.naver.com", headers=headers)

# 가져온 HTML 데이터를 BeautifulSoup을 통해 파싱
# data.text는 웹 페이지의 HTML 소스 코드이고, "html.parser"는 HTML을 파싱할 때 사용할 파서(분석기)
soup = BeautifulSoup(data.text, "html.parser")                        # 자바스크립트는 실행 못함

# soup.select()는 CSS 선택자를 사용하여 HTML 요소를 선택
# 여기서는 body 안에 있는 .blind 클래스를 가진 모든 요소를 선택하여 리스트로 저장 .blind == (class = blind)   id 관련한 것은 #blind 클래스 관련 .blind
# .blind는 클래스 이름을 의미하며, 웹 페이지 내에서 스크린 리더를 위한 텍스트 정보가 주로 포함
blind = soup.select("body .blind")

# 결과를 파일로 저장
# scraping_results.txt라는 파일을 열거나 생성하여, 데이터를 추가할 수 있는 append 모드('a')로 연다
with open("scraping_results.txt", "a", encoding="utf-8") as file:
    # .blind 클래스를 가진 모든 요소를 순회합니다. blind는 리스트이므로 각 요소를 하나씩 꺼내서 처리
    for b in blind:
        # b.text는 각 .blind 요소의 텍스트 내용을 추출한 것. 이를 파일에 기록하는데, 각 줄마다 개행(\n)
        file.write(b.text + "\n")
