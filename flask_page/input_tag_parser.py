import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def save_input_tags_to_html(url, max_depth=3):
    print("now parsing...")
    visited_urls = set()
    input_tags_content = ""

    def dfs_crawl(current_url, depth):
        nonlocal input_tags_content, visited_urls

        if current_url in visited_urls or '#' in current_url or depth > max_depth:
            return

        try:
            # URL에서 HTML 가져오기
            response = requests.get(current_url)
            # 에러 예외 처리
            response.raise_for_status()
            
            # 현재 URL을 방문한 것으로 표시
            visited_urls.add(current_url)

            # 현재 페이지에서 모든 링크 추출
            links = parse_and_save_tags(current_url, response)  # response를 사용하도록 수정
            for link in links:
                next_url = urljoin(current_url, link['href'])

                # 절대 URL로 변환
                next_url = urlparse(next_url)._replace(query='').geturl()

                # 다음 페이지로 이동 (재귀 호출)
                dfs_crawl(next_url, depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")

    def parse_and_save_tags(url, response):
        nonlocal input_tags_content

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # <input> 태그 찾기
        input_tags = soup.find_all('input')

        # <input> 태그가 없는 페이지 필터링하기
        if input_tags:
            # 현재 페이지 HTML에 기록하기
            input_tags_content += "<hr />"
            post_response = requests.post(url)
            if response.status_code == 200:
                if post_response.status_code != 405:
                    input_tags_content += f"<details><summary><strong>[GET][POST]</strong>"
                else :
                    input_tags_content += f"<details><summary><strong>[GET]</strong>"
            elif post_response.status_code != 405:
                input_tags_content += f"<details><summary><strong>[POST]</strong>"
            input_tags_content += f"<strong>{url}:</strong></summary>"
            input_tags_content += "<hr />"
            for input_tag in input_tags:
                # <input> 태그의 속성과 값 기록하기
                attributes = input_tag.attrs
                for attr, value in attributes.items():
                    input_tags_content += f"  {attr}: {value}<br>"
                input_tags_content += "<br>"
            input_tags_content += "</details>"
            input_tags_content += "<hr />"

        return soup.find_all('a', href=True)

    # 최초의 URL에서 시작
    dfs_crawl(url, 0)

    return input_tags_content if input_tags_content else "Input 태그가 없습니다."
