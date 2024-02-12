from flask import Blueprint, render_template, request
from XSS_parser import XSS_Bypass
import html
XSS_Bypass_bp = Blueprint('XSS_Bypass_bp', __name__, template_folder='templates')

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