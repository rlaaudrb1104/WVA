from flask import Blueprint, request, jsonify, render_template
import html
from SQL_parser import SQL_Payload_GET
from SQL_parser import SQL_Payload_POST


SQL_Payload_GET_bp = Blueprint('SQL_Payload_GET_bp', __name__, template_folder='templates')
SQL_Payload_POST_bp = Blueprint('SQL_Payload_POST_bp', __name__, template_folder='templates')

@SQL_Payload_GET_bp.route('/SQL', methods=['GET','POST'])
def SQL_G():
    if request.method == 'POST':
        user_provided_url = request.form['url']
        
        user_provided_cookies = [
                {
                    'name': request.form.get('cookie_name1', ''),
                    'value': request.form.get('cookie_value1', '')
                },
                {
                    'name': request.form.get('cookie_name2', ''),
                    'value': request.form.get('cookie_value2', '')
                }
            ]
            
        user_provided_params = request.form['params']
        
        result = SQL_Payload_GET(user_provided_url,user_provided_params)
        SQL_result = html.escape(result)
        return render_template('SQL_Payload.html', SQL_result=SQL_result)
    return render_template('SQL.html')

@SQL_Payload_POST_bp.route('/SQL', methods=['GET', 'POST'])
def SQL_P():
    if request.method == 'POST':
        user_provided_url = request.form['url']
        user_provided_params = request.form['params']
        
        result = SQL_Payload_POST(user_provided_url, user_provided_params)
        # 결과 문자열을 HTML 엔티티로 이스케이프 처리
        SQL_result = html.escape(result)
        # 결과를 JSON 형태로 클라이언트에 반환
        return render_template('SQL_Payload.html', SQL_result=SQL_result)
    # GET 요청 시, SQL 테스트 폼을 포함한 HTML 페이지 렌더링
    return render_template('SQL.html')