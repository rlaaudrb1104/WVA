from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def XSS_Payload(url, name, cookies):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화

    # ChromeDriverManager를 사용하여 브라우저 드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # 웹 페이지에 접근하기 전에 쿠키 추가
    driver.get(url)  # 쿠키를 추가하기 전에 도메인에 최소 한 번은 접근해야 함
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    # 쿠키 추가 후 페이지 재로드
    driver.get(url)

    # 페이로드 파일 읽기
    with open("XSS_Payload.txt", 'r', encoding='utf-8') as file:
        payloads = file.read().split('\n')
    
    for payload in payloads:
        target_url = f"{url}?{name}={payload}"
        driver.get(target_url)
        
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(payload, "통함")
            alert.accept()
        except (NoAlertPresentException, TimeoutException):
            pass

    driver.quit()

# 쿠키 예시 (사용할 쿠키 정보에 맞게 수정)
cookies = [
    {'name' : 'security', 'value': 'impossible'},
    {'name' : 'PHPSESSID', 'value' : 'kkh7u94lq4s1998i1gglnhfske'}
]

# 함수 호출 (URL, 파라미터 이름, 쿠키)
XSS_Payload("http://localhost/DVWA/vulnerabilities/xss_r", "name", cookies)