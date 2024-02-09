import requests
import time


def directory_listing(url):
    cheatsheet_path = "C:/Users/skawl/OneDrive/바탕 화면/WVA/tools/directory_cheatsheet.txt"
    directory_index = []

    try:
        with open(cheatsheet_path, "r", encoding="utf-8") as directory_cheatsheet:
            directory_index = directory_cheatsheet.read().split("\n")
    except FileNotFoundError:
        print(f"Error: File '{cheatsheet_path}' not found.")
        return

    directory_found_list = []

    try:
        total_directories = len(directory_index)
        for i in range(total_directories):
            result = requests.get(str(url) + directory_index[i])
            try:
                result.raise_for_status()
                directory_found_list.append(directory_index[i])
                print(
                    f"[{i + 1}/{total_directories}] Directory found: {directory_index[i]}"
                )
            except requests.exceptions.HTTPError as err:
                print(
                    f"[{i + 1}/{total_directories}] HTTP error ({err.response.status_code}): {err.response.reason}"
                )

            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

    save_to_file(
        "C:/Users/skawl/OneDrive/바탕 화면/WVA/tools/directory_found_list.txt",
        directory_found_list,
    )


def save_to_file(file_path, data_list):
    with open(file_path, "w", encoding="utf-8") as output_file:
        for item in data_list:
            output_file.write(item + "\n")


# Example usage:
result = directory_listing("http://regs123.dothome.co.kr/shop/")
print(result)
