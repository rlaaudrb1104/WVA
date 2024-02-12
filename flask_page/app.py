
from input_tag_analysis import input_tag_bp
from XSS_analysis import XSS_Bypass_bp
from XSS_analysis import XSS_Payload_bp
from flask_socketio import SocketIO,emit
import threading
from XSS_parser import XSS_Payload
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
socketio = SocketIO(app)


# 블루프린트 등록
app.register_blueprint(input_tag_bp)
app.register_blueprint(XSS_Bypass_bp)
app.register_blueprint(XSS_Payload_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/XSS_Payload', methods=['GET'])
def xss_payload_form():
    return render_template('XSS_Payload.html')

@socketio.on('test_xss')
def handle_test_xss(json):
    # 별도의 스레드에서 XSS 테스트 실행
    thread = threading.Thread(target=XSS_Payload, args=(json['url'], json['param'], socketio))
    thread.start()
    
if __name__ == '__main__':
    socketio.run(app, debug=True)