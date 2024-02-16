import requests
from flask_socketio import SocketIO

def SQL_Payload_GET(url, param, socketio):
    with open("./flask_page/SQL_Payload.txt", 'r', encoding='utf-8') as SQL_Payload:
        Payload = SQL_Payload.read().split('\n\n')

    Payload_result = []

    for payload in Payload:
        full_url = f"{url}?{param}={payload}"
        r = requests.get(full_url)
        
        if r.status_code == 200:
            result = f"{payload} 통함"
            print(f"{payload} 통함")
            Payload_result.append(result)
            socketio.emit('sql_result', {'result': result})
        else:
            print(f"{payload} 안통함")

    return Payload_result

def SQL_Payload_POST(url, param, socketio):
    with open("./flask_page/SQL_Payload.txt", 'r', encoding='utf-8') as SQL_Payload:
        Payload = SQL_Payload.read().split('\n\n')

    Payload_result = []

    for payload in Payload:
        data = {param: payload}
        r = requests.post(url, data=data)
        
        if r.status_code == 200:
            result = f"{payload} 통함"
            print(f"{payload} 통함")
            Payload_result.append(result)
            socketio.emit('sql_result', {'result': result})
        else:
            print(f"{payload} 안통함")

    return Payload_result
