from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

webdriver_options = webdriver.ChromeOptions()
# webdriver_options.add_argument("--headless")
webdriver_options.add_argument("--no-sandbox")
webdriver_options.add_argument("--disable-dev-shm-usage")
webdriver_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
)

driver = webdriver.Chrome(options=webdriver_options)
driver.implicitly_wait(1)

url = "https://github.com/"
driver.get(url)

# 이메일 입력 필드 찾기
email_field = driver.find_element(By.ID, "hero_user_email")

# 이메일 입력 및 엔터 키 입력
email_field.send_keys("안녕하세요")
# email_field.send_keys(Keys.RETURN)  # 엔터 키 입력

# 입력된 내용 확인
entered_email = email_field.get_attribute("value")
print(f"입력된 이메일: {entered_email}")

# 페이지 소스 출력 (디버깅 목적)
# print(driver.page_source)

# 브라우저 종료
# driver.quit()
time.sleep(100)  # 5초 대기