import requests
from bs4 import BeautifulSoup
import os

# 여기에 URL을 입력
user_provided_url = "김원태"

def save_input_tags_to_file(url, base_output_file):
    try:
        # URL에서 HTML 가져오기
        response = requests.get(url)
        response.raise_for_status()  # 에러가 있는 경우 예외 발생

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # <input> 태그 찾기
        input_tags = soup.find_all('input')

        # 결과를 txt파일에 저장하기
        output_file = base_output_file
        count = 1
        while os.path.exists(output_file + '.txt'):
            count += 1
            output_file = f"{base_output_file}_{count}"

        with open(output_file + '.txt', 'w', encoding='utf-8') as file:
            file.write(f"Input Tag Found at {url}:\n")
            for input_tag in input_tags:
                # <input> 태그의 속성과 값을 모두 기록해줌
                attributes = input_tag.attrs
                for attr, value in attributes.items():
                    file.write(f"  {attr}: {value}\n")
                file.write("\n")

        print(f"Input tags saved to {output_file}.txt")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

save_input_tags_to_file(user_provided_url, "input tag")
