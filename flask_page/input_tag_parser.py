import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse

def save_input_tags_to_html(url, max_depth=3):
    print("now parsing...")
    visited_urls = set()
    content = []

    def dfs_crawl(current_url, depth):
        nonlocal content, visited_urls

        if current_url in visited_urls or '#' in current_url or depth > max_depth:
            return

        try:
            # URL에서 HTML 가져오기
            response = requests.get(current_url)
            # 에러 예외 처리
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # <input> 태그 찾기
            input_tags = soup.find_all('input')

            # HTML 주석 찾기
            html_comments = soup.find_all(string=lambda text: isinstance(text, Comment))

            # 현재 페이지 정보 추가
            page_info = {
                'url': current_url,
                'input_tags': input_tags,
                'comments': html_comments
            }

            content.append(page_info)

            # 현재 URL을 방문한 것으로 표시
            visited_urls.add(current_url)

            # 현재 페이지에서 모든 링크 추출
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(current_url, link['href'])

                # 절대 URL로 변환
                next_url = urlparse(next_url)._replace(query='').geturl()

                # 다음 페이지로 이동 (재귀 호출)
                dfs_crawl(next_url, depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")

    # 최초의 URL에서 시작
    dfs_crawl(url, 0)

    return content
