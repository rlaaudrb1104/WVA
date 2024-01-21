import requests



def SQL_Injection(url):
  #필터링
  SQL_Bypass = open("SQL_Bypass.txt",'r', encoding='utf-8')
  Bypass = SQL_Bypass.read().split('\n\n')
  #페이로드
  SQL_Payload = open("SQL_Payload.txt", 'r', encoding='utf-8')
  Payload = SQL_Payload.read().split('\n\n')

  Bypass_result = []
  Payload_result = []

  #필터링 확인
  for i in Bypass:
    r = requests.get(f"{url}{Bypass[i]}")
    
    if r.status_code == 500 :
      print(Bypass[i], "통함")
      Bypass_result = []
    else:
      print(Bypass[i],"안통함")

  #페이로드 넣기
  for i in Payload:
    r = requests.get(f"{url}{Payload[i]}")
    
    if r.status_code == 500 :
      print(Payload[i], "통함")
      Payload_result = []
    else:
      print(Payload[i],"안통함")

SQL_Injection("https://example.com")