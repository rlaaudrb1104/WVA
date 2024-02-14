from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_socketio import SocketIO

def XSS_Bypass(url, name):
  # Chrome 옵션 설정
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
  chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화

  # ChromeDriverManager를 사용하여 브라우저 드라이버 설정
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

  # 웹 페이지에 접근하기 전에 쿠키 추가
  # driver.get(url)  # 쿠키를 추가하기 전에 도메인에 최소 한 번은 접근해야 함
  # for cookie in cookies:
  #     driver.add_cookie(cookie)

  # 쿠키 추가 후 페이지 재로드
  driver.get(url)

  # 페이로드 파일 읽기
  with open("./flask_page/XSS_Bypass.txt", 'r', encoding='utf-8') as file:
    Bypasss = file.read().split('\n')
  Bypass_result_T = ""
  Bypass_result_F = ""
  for Bypass in Bypasss:
    target_url = f"{url}?{name}={Bypass}"

    driver.get(target_url)
    
    if Bypass not in driver.page_source:
      Bypass_result_T += Bypass + "|"
    else:
      Bypass_result_F += Bypass + "|"
  Bypass_result = f"필터링O : {Bypass_result_T} \n필터링X : {Bypass_result_F}"
  driver.quit()
  return Bypass_result

def XSS_Payload(url, name, socketio):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화

    # ChromeDriverManager를 사용하여 브라우저 드라이버 설정
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 웹 페이지에 접근하기 전에 쿠키 추가
    # driver.get(url)  # 쿠키를 추가하기 전에 도메인에 최소 한 번은 접근해야 함
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # 쿠키 추가 후 페이지 재로드
    driver.get(url)

    # 페이로드 파일 읽기
    with open("./flask_page/XSS_Payload.txt", 'r', encoding='utf-8') as file:
        payloads = file.read().split('\n')

    Payload_results = []

    try:
        for payload in payloads:
            target_url = f"{url}?{name}={payload}"
            driver.get(target_url)

            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(payload, "통함")
                result = f"{payload}:통함"
                alert.accept()
                # 성공한 경우에만 emit 호출
                Payload_results.append(result)
                socketio.emit('xss_result', {'result': result})
            except (NoAlertPresentException, TimeoutException):
                pass

        driver.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # 오류가 발생했을 경우 빈 리스트 반환
        Payload_results = []

    return Payload_results
