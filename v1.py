import http.client
import json

conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
payload = json.dumps({
  "action": "allow",
  "application": [
    "youtube"
  ],
  "category": [
    "adult"
  ],
  "description": "It's upto you!!",
  "destination": [
    "any"
  ],
  "destination_hip": [
    "any"
  ],
  "disabled": False,
  "from": [
    "any"
  ],
  "name": "Testing",
 
  "service": [
    "service-http"
  ],
  "source": [
    "192.168.20.0/29"
  ],
  "source_hip": [
    "any"
  ],
  "source_user": [
    "john"
  ],
  "tag": [
    "test-one"
  ],
 "to": [
    "any"
   ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiNTY4YjlmOGMtNDk4NC00NDgyLWIyNTgtNzM0ZmYzNzA1MDI4LTE1NDM1MzIxMSIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiNzhYZTNvSk5RRmxLUWFwXy0yNlRWN1Q3NmdJIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNjM0NzI4LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNjM0NzI4LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA2MzU2MjgsImlhdCI6MTc0MDYzNDcyOCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJFc05lNGlJLWYtTl93N01aWVFwRlVXRXJuVWsiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.J20fOOS1VhFmz6M8IpfCFfd6NLEsgQmEUlqAeqnNcVC9FzAOPHaqXTF9wIDpcS66FG1dj5JOcjJCxcZMQPGl2cZ4pHrzQE6b4Zz4eM-oujIqGvVNN9_nAymz-JwAFMqkvZo6v_mNOv_tOacJrExH754aD35QmAeio1Q_DhwOaJ5VNP5Og40E-PiNHdXnddAf_QiL1K_JSKID4bCqdfUpqUobS5dSo0mnRhRRSWO_AJmH1TFRNrwjWFuBB62qUt_vZAGwBej4permAVpM4YoAp1L9bI3C8vWsBFmp0kJ1_eiY1JFinq1OzwkqcnC_CP13qZZJYbnac2TxvHMPsTvCTg'
}
conn.request("POST", "/sse/config/v1/security-rules?position=pre&folder=Remote%20Networks", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))