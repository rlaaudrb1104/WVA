from flask import Blueprint, render_template, request

from directory_parser import directory_listing

directory_bp = Blueprint("directory_bp", __name__, template_folder="templates")


@directory_bp.route("/directory", methods=["GET", "POST"])
def directory():
    if request.method == "POST":
        user_provided_url = request.form["url"]
        cheatsheet_path = "flask_page/directory_cheatsheet.txt"  # 디렉토리 목록 파일 경로
        directory_found_list = directory_listing(user_provided_url, cheatsheet_path)
        return render_template("directory_result.html", directory_found_list=directory_found_list)

    return render_template("directory.html")
