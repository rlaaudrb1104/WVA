import requests

def try_get_and_post(url):
    try:
        # GET 요청 시도
        response_get = requests.get(url)
        if response_get.status_code == 200:
            print("GET 메소드는 사용 가능합니다.")
        elif response_get.status_code == 405:
            raise requests.exceptions.HTTPError("405 Method Not Allowed")
        else:
            print("GET 메소드의 응답 상태 코드:", response_get.status_code)

        # POST 요청 시도
        response_post = requests.post(url)
        if response_post.status_code == 200:
            print("POST 메소드는 사용 가능합니다.")
        elif response_post.status_code == 405:
            raise requests.exceptions.HTTPError("405 Method Not Allowed")
        else:
            print("POST 메소드의 응답 상태 코드:", response_post.status_code)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 오류 발생: {e}")
    except requests.RequestException as e:
        print(f"기타 오류 발생: {e}")

if __name__ == "__main__":
    # 사용자로부터 URL 입력 받기
    user_url = input("URL을 입력하세요: ")

    # 함수 호출하여 GET 및 POST 요청 결과 출력
    try_get_and_post(user_url)
