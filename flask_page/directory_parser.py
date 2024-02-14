from flask import Blueprint, render_template, request
import requests
import time

directory_bp = Blueprint("directory_bp", __name__)


def directory_listing(url):
    cheatsheet_path = "./tools/directory_cheatsheet.txt"
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

            # time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

    return render_template("directory.html", directory_found_list=directory_found_list)
