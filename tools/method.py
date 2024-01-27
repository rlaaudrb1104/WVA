import requests
from bs4 import BeautifulSoup

def parse_forms_and_test(url):
    try:
        # 주어진 URL에 대한 GET 요청을 보냄
        response = requests.get(url)
        response.raise_for_status()  # 요청이 실패한 경우 예외를 발생시킴
        soup = BeautifulSoup(response.text, 'html.parser')  # 응답을 BeautifulSoup으로 파싱
    except requests.exceptions.RequestException as e:
        print(f"오류: {e}")
        return None

    forms = soup.find_all('form')  # 웹 페이지에서 모든 폼을 찾음
    if not forms:
        print("\n폼을 찾을 수 없습니다.")
        return None

    # 각 폼에 대해 GET 및 POST 요청을 보내고 결과를 저장
    results_from_method_exploration = method_exploration(forms, url)
    save_results_to_txt(results_from_method_exploration)
    print("\n테스트 결과는 method_exploration.txt 파일에 저장되었습니다.")

def method_exploration(forms, base_url):
    results = {}

    for form in forms:
        action = form.get('action', '')
        form_url = requests.compat.urljoin(base_url, action)

        # ID와 name을 찾아 결과에 추가
        form_id = form.get('id', '')
        form_name = form.get('name', '')

        # GET 메소드에 대한 요청
        try:
            response_get = requests.get(form_url)
            response_get.raise_for_status()

            result_get = {
                'url': form_url,
                'methods': ['GET'],
                'status_code': response_get.status_code,
                'form_id': form_id,
                'form_name': form_name,
            }
            key = (result_get['url'], result_get['status_code'], result_get['form_id'], result_get['form_name'])
            results[key] = results.get(key, []) + result_get['methods']

        except requests.exceptions.RequestException as e:
            result_get = {
                'url': form_url,
                'methods': ['GET'],
                'error': str(e),
                'form_id': form_id,
                'form_name': form_name,
            }
            key = (result_get['url'], result_get['status_code'], result_get['form_id'], result_get['form_name'])
            results[key] = results.get(key, []) + result_get['methods']

        # POST 메소드에 대한 요청
        try:
            response_post = requests.post(form_url)
            response_post.raise_for_status()

            result_post = {
                'url': form_url,
                'methods': ['POST'],
                'status_code': response_post.status_code,
                'form_id': form_id,
                'form_name': form_name,
            }
            key = (result_post['url'], result_post['status_code'], result_post['form_id'], result_post['form_name'])
            results[key] = results.get(key, []) + result_post['methods']

        except requests.exceptions.RequestException as e:
            result_post = {
                'url': form_url,
                'methods': ['POST'],
                'error': str(e),
                'form_id': form_id,
                'form_name': form_name,
            }
            key = (result_post['url'], result_post['status_code'], result_post['form_id'], result_post['form_name'])
            results[key] = results.get(key, []) + result_post['methods']

    return results

def save_results_to_txt(results):
    # 폼 테스트 결과를 파일에 저장
    with open('method_exploration.txt', 'w', encoding='utf-8') as file:
        # 같은 URL, 상태 코드, 폼 ID, 폼 이름에 대한 결과를 하나로 출력
        for i, (key, methods) in enumerate(results.items()):
            url, status_code, form_id, form_name = key
            file.write(f"\n{i+1}.\nURL: {url}\n")
            file.write(f"상태 코드: {status_code}\n")
            file.write(f"폼 ID: {form_id}\n")
            file.write(f"폼 이름: {form_name}\n")
            file.write(f"메소드: {', '.join(methods)}\n")

if __name__ == "__main__":
    user_provided_url = "URL 입력란"
    parse_forms_and_test(user_provided_url)