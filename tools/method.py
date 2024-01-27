import requests
from bs4 import BeautifulSoup

url = input("URL을 입력하세요: ")  # URL 입력

# HTML 파싱
try:
    response = requests.get(url)
    response.raise_for_status()  # 오류 예외처리
    soup = BeautifulSoup(response.text, 'html.parser')
except requests.exceptions.RequestException as e:
    print(f"오류 : {e}")
    exit()

# GET, POST 요청 보내고 응답 txt로 저장
elements = soup.find_all(['a', 'form', 'button'])

form_data = {''}

for element in elements:
    method = element.name.upper()  # 대문자로 전환 후 메소드 구분
    element_text = element.get_text().strip()  # HTML 요소의 텍스트 추출

    try:
        if method == 'FORM':
            # POST 요청
            response = requests.get(element['href'])
            print(f"{method} 요청 - 응답: {response.text}")

            response = requests.post(element['action'], data=form_data)
            response.raise_for_status()
            print(f"{method} 요청 - 응답: {response.text}")
            # 성공한 응답을 기록
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{method} 요청 성공 - {element_text}\n")

        elif method == 'A':
            # GET 요청 보내기
            response = requests.get(element['href'])
            print(f"{method} 요청 - 응답: {response.text}")

            response = requests.post(element['action'], data=form_data)
            response.raise_for_status()
            print(f"{method} 요청 - 응답: {response.text}")
            # 성공한 응답을 기록
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{method} 요청 성공 - {element_text}\n")

        elif method == 'BUTTON':
            # POST 요청 보내기
            response = requests.get(element['href'])
            print(f"{method} 요청 - 응답: {response.text}")

            response = requests.post(url, data=form_data)
            response.raise_for_status()
            print(f"{method} 요청 - 응답: {response.text}")
            # 성공한 응답을 기록
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{method} 요청 성공 - {element_text}\n")

        else:
            print(f"그 외의 요소 : {method}")

    except requests.exceptions.RequestException as e:
        print(f"오류 : {e}")
        with open('error_log.txt', 'a') as error_log:
            error_log.write(f"{method} 요청 실패 - {element_text}\n")


print("작업 완료")