import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def save_input_tags_to_file(url, output_file, max_depth):
    visited_urls = set()

    def dfs(current_url, depth):
        nonlocal visited_urls

        if current_url in visited_urls or '#' in current_url or depth > max_depth:
            return

        try:
            # URL에서 HTML 가져오기
            response = requests.get(current_url)
            response.raise_for_status()  # 에러 예외 처리

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # <input> 태그 찾기
            input_tags = soup.find_all('input')

            # 결과를 텍스트 파일에 저장
            output_file = base_output_file
            count = 1
            while os.path.exists(output_file + '.txt'):
                count += 1
                output_file = f"{base_output_file}_{count}"

            with open(output_file + '.txt', 'a', encoding='utf-8') as file:
                file.write(f"Input Tag Found at {current_url}:\n")
                for input_tag in input_tags:
                    # <input> 태그의 속성과 값 저장
                    attributes = input_tag.attrs
                    for attr, value in attributes.items():
                        file.write(f"  {attr}: {value}\n")
                    file.write("\n")

            print(f"Input tags saved to {output_file}.txt")

            # 현재 URL을 방문한 것으로 표시
            visited_urls.add(current_url)

            # 현재 페이지에서 모든 링크 추출
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
    user_provided_url = "https://www.naver.com/"

    # 결과를 저장할 텍스트 파일의 이름
    base_output_file = "url"

    # 함수 호출 및 탐색 깊이 정해주기
    save_input_tags_to_file(user_provided_url, base_output_file, max_depth=3)
