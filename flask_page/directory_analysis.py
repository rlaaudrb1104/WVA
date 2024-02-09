from flask import Blueprint, render_template, request

from directory_parser import save_directory_to_html

directory_bp = Blueprint("directory_bp", __name__, template_folder="templates")


@directory_bp.route("/directory", methods=["GET", "POST"])
def directory():
    if request.method == "POST":
        user_provided_url = request.form["url"]
        result_html = save_directory_to_html(user_provided_url, max_depth=3)
        return render_template("directory_result.html", result_html=result_html)

    return render_template("directory.html")
