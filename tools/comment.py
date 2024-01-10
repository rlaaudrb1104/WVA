import requests
import re
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def save_comments_to_file(url, base_output_file, max_depth):
    visited_urls = set()

    def dfs(current_url, depth):
        nonlocal visited_urls

        if current_url in visited_urls or '#' in current_url or depth > max_depth:
            return

        try:
            # URL에서 HTML 가져오기
            response = requests.get(current_url)
            response.raise_for_status()  # 에러 예외 처리

            # HTML 주석 찾기
            comments = re.findall(r'<!--(.*?)-->', response.text, re.DOTALL)

            # 결과를 텍스트 파일에 저장
            output_file_path = f"{base_output_file}_{len(visited_urls)}.txt"
            with open(output_file_path, 'a', encoding='utf-8') as file:
                file.write(f"Comments Found at {current_url}:\n")
                for comment in comments:
                    file.write(f"{comment}\n")
            print(f"Comments saved to {output_file_path}")

            # 현재 URL을 방문한 것으로 표시
            visited_urls.add(current_url)

            # 현재 페이지에서 모든 링크 추출
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(current_url, link['href'])

                # 절대 URL로 변환
                next_url = urlparse(next_url)._replace(query='').geturl()

                # 다음 페이지로 이동 (재귀 호출)
                dfs(next_url, depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")

    # 최초의 URL에서 시작
    dfs(url, 0)

if __name__ == "__main__":
    # 여기에 URL을 입력
    user_provided_url = "http://localhost/g5/"

    # 결과를 저장할 텍스트 파일의 기본 이름
    base_output_file = "comments"

    # 함수 호출 및 탐색 깊이 정해주기
    save_comments_to_file(user_provided_url, base_output_file, max_depth=3)

