from flask import Blueprint, render_template, request
from XSS_parser import XSS_Bypass

XSS_Bypass_bp = Blueprint('XSS_Bypass_bp', __name__, template_folder='templates')

@XSS_Bypass_bp.route('/XSS', methods=['GET','POST'])
def XSS():
  if request.method == 'POST':
    user_provided_url = request.form['url']
    user_provided_cookies_name = request.form['cookies_name']
    user_provided_cookies_value = request.form['cookies_value']
    user_provided_params = request.form['params']
    user_provided_cookies = {
      user_provided_cookies_name : user_provided_cookies_value
    }
    
    result_html = XSS_Bypass(user_provided_url,user_provided_cookies,user_provided_params)
    return render_template('XSS_Bypass_result.html',result_html=result_html)
  return render_template('XSS.html')


