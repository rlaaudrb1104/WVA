import requests



def XSS(url):
  #필터링
  XSS_Bypass = open("XSS_Bypass.txt",'r', encoding='utf-8')
  Bypass = XSS_Bypass.read().split('\n')
  #페이로드
  XSS_Payload = open("XSS_Payload.txt", 'r', encoding='utf-8')
  Payload = XSS_Payload.read().split('\n')

  Bypass_result = []
  Payload_result = []
  
  #필터링 확인
  for i in Bypass:
    r = requests.get(f"{url}{Bypass[i]}")
    
    if r.text in Bypass[i] :
      print(Bypass[i], "통함")
      Bypass_result = Bypass[i]
    else:
      print(Bypass[i],"안통함")

  #페이로드 넣기
  for i in Payload:
    r = requests.get(f"{url}{Payload[i]}")
    
    if r.text in Payload[i] :
      print(Payload[i], "통함")
      Payload_result = []
    else:
      print(Payload[i],"안통함")

XSS("https://example.com")