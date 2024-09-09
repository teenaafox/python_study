# GitHub 홈페이지에 접속하여 이메일 입력 필드에 특정 이메일 주소를 입력한 후, 입력된 값을 확인하는 자동화 스크립트

from selenium import webdriver   # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Chrome 웹드라이버에 대한 옵션 객체를 생성
# 이 객체를 통해 브라우저의 동작을 customizing할 수 있다
webdriver_options = webdriver.ChromeOptions()

# GUI 없이 백그라운드에서 브라우저를 실행하는 방식
# webdriver_options.add_argument("--headless")     # 저사양 옵션에서 화면은 띄우지 않고 실행해 볼때

# Chrome의 샌드박스 보안 기능을 비활성화
# 주로 리눅스 환경에서 root 권한으로 Chrome을 실행할 때 필요
webdriver_options.add_argument("--no-sandbox")

# /dev/shm 파티션 사용을 비활성화하고 대신 임시 디렉토리를 사용
# 일부 Linux 시스템에서 메모리 부족 문제를 해결하는 데 도움
webdriver_options.add_argument("--disable-dev-shm-usage")

# 웹드라이버의 User-Agent 문자열을 설정
# 웹드라이버가 특정 브라우저와 운영 체제를 사용하는 것처럼 웹사이트에 자신을 식별
# 여기서는 Windows 10에서 실행되는 Chrome 97 버전으로 설정
webdriver_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
)

# 앞서 설정한 옵션들을 사용하여 Chrome 웹드라이버 인스턴스를 생성
driver = webdriver.Chrome(options=webdriver_options)
# 웹드라이버가 요소를 찾을 때 최대 1초간 기다리도록 설정합니다. 페이지 로딩 지연에 대비
driver.implicitly_wait(1)

# GitHub 홈페이지 URL을 정의하고, 웹드라이버를 사용해 해당 페이지로 이동
url = "https://github.com/"
driver.get(url)

# 이메일 입력 필드 찾기
# 페이지에서 ID가 "hero_user_email"인 요소(이메일 입력 필드)를 찾아 변수에 저장
email_field = driver.find_element(By.ID, "hero_user_email")
                                  
# 이메일 입력 및 엔터 키 입력
# 찾은 이메일 필드에 "teenaafox"라는 텍스트를 입력
email_field.send_keys("안녕하세요")
# email_field.send_keys(Keys.RETURN)   # 엔터 키 입력

# 입력된 내용 확인
# 이메일 필드의 현재 값을 가져와서 출력. 이는 입력이 제대로 되었는지 확인하는 용도
entered_email = email_field.get_attribute("value")
print(f"입력된 이메일: {entered_email}")

# 페이지 소스 출력 (디버깅 목적)
# 현재 페이지의 HTML 소스를 출력하는 코드
# print(driver.page_source)

# 브라우저 종료    웹드라이버를 종료하는 코드
# driver.quit()
# 작업 결과를 확인하거나 다음 작업을 위한 대기 시간을 제공. 프로그램을 100초간 일시 정지
time.sleep(100)   # 100초 대기