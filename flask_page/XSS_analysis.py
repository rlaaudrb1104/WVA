from flask import Blueprint, request, jsonify, render_template
import html
from XSS_parser import XSS_Bypass
from XSS_parser import XSS_Payload

XSS_Bypass_bp = Blueprint('XSS_Bypass_bp', __name__, template_folder='templates')
XSS_Payload_bp = Blueprint('XSS_Payload_bp', __name__, template_folder='templates')
@XSS_Bypass_bp.route('/XSS', methods=['GET','POST'])
def XSS():
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
    
    result = XSS_Bypass(user_provided_url,user_provided_params)
    Bypass_result = html.escape(result)
    return render_template('XSS_Bypass_result.html', Bypass_result=Bypass_result)
  return render_template('XSS.html')

@XSS_Payload_bp.route('/XSS', methods=['GET', 'POST'])
def XSS_P():
    if request.method == 'POST':
        user_provided_url = request.form['url']
        user_provided_params = request.form['params']
        
        result = XSS_Payload(user_provided_url, user_provided_params)
        # 결과 문자열을 HTML 엔티티로 이스케이프 처리
        Payload_result = html.escape(result)
        # 결과를 JSON 형태로 클라이언트에 반환
        return jsonify({'Payload_result': Payload_result})
    # GET 요청 시, XSS 테스트 폼을 포함한 HTML 페이지 렌더링
    return render_template('XSS.html')