from flask import Blueprint, render_template, request

from directory_parser import directory_listing

directory_bp = Blueprint("directory_bp", __name__, template_folder="templates")


@directory_bp.route("/directory", methods=["GET", "POST"])
def directory():
    if request.method == "POST":
        user_provided_url = request.form["url"]
        pages_info = directory_listing(user_provided_url)
        return render_template("directory_result.html", pages_info=pages_info)

    return render_template("directory.html")
