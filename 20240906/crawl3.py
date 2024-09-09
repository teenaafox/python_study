from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver 설정
webdriver_options = webdriver.ChromeOptions()
# webdriver_options.add_argument("--headless")
webdriver_options.add_argument("--no-sandbox")
webdriver_options.add_argument("--disable-dev-shm-usage")
webdriver_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
)

driver = webdriver.Chrome(options=webdriver_options)


def get_active_content():
    # .group_type .is_active 클래스를 가진 요소 찾기
    active_element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.group_type.is_active"))
    )
    print("Active content:", active_element.text)

    # .tbl_home 클래스를 가진 요소 찾기
    tbl_home = active_element.find_element(By.CLASS_NAME, "tbl_home")
    print("Table content:", tbl_home.text)


try:
    # 웹페이지 접속
    url = "https://finance.naver.com/"
    driver.get(url)

    get_active_content()

    # li.tab4 요소 클릭
    tab4 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.tab4"))
    )
    tab4.click()

    get_active_content()

finally:
    time.sleep(100)     # 5초 대기
    driver.quit()