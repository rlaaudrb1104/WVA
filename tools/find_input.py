import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def save_input_tags_to_html(url, output_file, max_depth=3):
    print("now parsing...")
    visited_urls = set()

    def dfs_crawl(current_url, depth, html_content):
        nonlocal visited_urls

        if current_url in visited_urls or '#' in current_url or depth > max_depth:
            return html_content

        try:
            # URL에서 HTML 가져오기
            response = requests.get(current_url)
            # 에러 예외 처리
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # <input> 태그 찾기
            input_tags = soup.find_all('input')

            # <input> 태그가 없는 페이지 필터링하기
            if not input_tags:
                return html_content

            # 현재 페이지 HTML에 기록하기
            html_content += "<hr />"
            html_content += f"<div><strong>Input Tags Found at {current_url}:</strong><br>"
            html_content += "<hr />"
            for input_tag in input_tags:
                # <input> 태그의 속성과 값 기록하기
                attributes = input_tag.attrs
                for attr, value in attributes.items():
                    html_content += f"  {attr}: {value}<br>"
                html_content += "<br>"

            html_content += "</div>"
            html_content += "<hr />"

            # 현재 URL을 방문한 것으로 표시
            visited_urls.add(current_url)

            # 현재 페이지에서 모든 링크 추출
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(current_url, link['href'])

                # 절대 URL로 변환
                next_url = urlparse(next_url)._replace(query='').geturl()

                # 다음 페이지로 이동 (재귀 호출)
                html_content = dfs_crawl(next_url, depth + 1, html_content)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")

        return html_content

    # 최초의 URL에서 시작
    result_html = dfs_crawl(url, 0, "")

    # 결과를 HTML로 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("<!DOCTYPE html><html><head><title>Input Tags Report</title></head><body>")
        file.write(result_html)
        file.write("</body></html>")

    print(f"Input tags saved to {output_file}")

if __name__ == "__main__":
    # 여기에 URL을 입력
    user_provided_url = "ㅁㄴㅇㄹ"

    # 결과를 저장할 HTML 파일 이름
    output_html_file = "input_tags.html"

    # 함수 호출 및 탐색 깊이 정해주기
    save_input_tags_to_html(user_provided_url, output_html_file, max_depth=3)
