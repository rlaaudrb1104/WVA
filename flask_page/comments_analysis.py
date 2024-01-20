from flask import Blueprint, render_template, request

from comments_parser import save_comments_to_html

comments_bp = Blueprint('comments_bp', __name__, template_folder='templates')

@comments_bp.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        user_provided_url = request.form['url']
        result_html = save_comments_to_html(user_provided_url, max_depth=3)
        return render_template('comments_result.html', result_html=result_html)

    return render_template('comments.html')
