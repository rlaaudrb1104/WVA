import requests

def try_request(url):
    try:
        # GET 요청 시도
        response_get = requests.get(url)
        print(f"GET 요청 성공 - 상태 코드: {response_get.status_code}")

        # 메모장 파일에 저장
        with open("response_output.txt", "a", encoding="utf-8") as file:
            file.write("GET 요청 결과:\n")
            file.write(f"URL: {url}\n")
            file.write(f"HTTP 메소드: GET\n")
            file.write(f"상태 코드: {response_get.status_code}\n")
            file.write(f"응답 내용:\n{response_get.text}\n\n")

    except requests.RequestException as e:
        print(f"GET 요청 실패 - 오류 발생: {e}")

    try:
        # POST 요청 시도
        response_post = requests.post(url)
        print(f"POST 요청 성공 - 상태 코드: {response_post.status_code}")

        # 메모장 파일에 저장
        with open("response_output.txt", "a", encoding="utf-8") as file:
            file.write("POST 요청 결과:\n")
            file.write(f"URL: {url}\n")
            file.write(f"HTTP 메소드: POST\n")
            file.write(f"상태 코드: {response_post.status_code}\n")
            file.write(f"응답 내용:\n{response_post.text}\n\n")

    except requests.RequestException as e:
        print(f"POST 요청 실패 - 오류 발생: {e}")

if __name__ == "__main__":
    # 사용자로부터 URL 입력 받기
    user_url = input("URL을 입력하세요: ")

    # 함수 호출하여 GET 및 POST 요청 시도 및 결과 출력
    try_request(user_url)

    print("결과가 'response_output.txt' 파일에 저장되었습니다.")
