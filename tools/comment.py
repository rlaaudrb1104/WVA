import requests
import re

def save_website_comments_with_cookies(url, file_name):
    # requests 세션 생성
    session = requests.Session()

    # 웹사이트의 첫 번째 요청을 보내어 쿠키를 얻음
    session.get(url)

    # 세션을 사용하여 같은 웹사이트에 다시 요청을 보내어 쿠키를 포함시킴
    response = session.get(url)
    content = response.text

    # HTML 주석 찾기
    comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL)

    # 주석을 파일에 저장
    with open(file_name, 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + '\n\n')

# 사용 예제
url = 'https://evc.kepco.co.kr:4445/main.do'  # 분석하고자 하는 웹사이트의 URL
file_name = 'comments.txt'  # 저장할 파일 이름
save_website_comments_with_cookies(url, file_name)
