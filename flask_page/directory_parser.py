from flask import Blueprint, render_template
import requests
import time

directory_bp = Blueprint("directory_bp", __name__)


@directory_bp.route("/directory")
def directory():
    url = "http://regs123.dothome.co.kr/shop/"
    cheatsheet_path = "C:/WVA/tools/directory_cheatsheet.txt"
    directory_found_list = []

    try:
        with open(cheatsheet_path, "r", encoding="utf-8") as directory_cheatsheet:
            directory_index = directory_cheatsheet.read().split("\n")
    except FileNotFoundError:
        return f"Error: File '{cheatsheet_path}' not found."

    try:
        total_directories = len(directory_index)
        for i, directory in enumerate(directory_index, 1):
            result = requests.get(url + directory)
            try:
                result.raise_for_status()
                directory_found_list.append(directory)
                print(f"[{i}/{total_directories}] Directory found: {directory}")
            except requests.exceptions.HTTPError as err:
                print(
                    f"[{i}/{total_directories}] HTTP error ({err.response.status_code}): {err.response.reason}"
                )
            time.sleep(1)
    except Exception as e:
        return f"Error: {e}"

    return render_template("directory.html", directory_found_list=directory_found_list)
