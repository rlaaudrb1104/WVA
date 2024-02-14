from flask import Flask, render_template
from input_tag_analysis import input_tag_bp
from comments_analysis import comments_bp
from directory_analysis import directory_bp

app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(input_tag_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(directory_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
