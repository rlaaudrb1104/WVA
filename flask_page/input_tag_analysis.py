from flask import Blueprint, render_template, request

from input_tag_parser import save_input_tags_to_html

input_tag_bp = Blueprint('input_tag_bp', __name__, template_folder='templates')

@input_tag_bp.route('/input_tag', methods=['GET', 'POST'])
def input_tag():
    if request.method == 'POST':
        user_provided_url = request.form['url']
        result_html = save_input_tags_to_html(user_provided_url, max_depth=3)
        return render_template('input_tag_result.html', result_html=result_html)

    return render_template('input_tag.html')