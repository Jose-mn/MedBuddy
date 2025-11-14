import requests
import json

url = 'http://127.0.0.1:8000/auth/signup'
payload = {
    'username': 'test_user_debug',
    'email': 'debug@example.com',
    'password': '889900'
}

try:
    resp = requests.post(url, json=payload, timeout=5)
    print('STATUS:', resp.status_code)
    try:
        print('BODY:', resp.json())
    except Exception:
        print('BODY TEXT:', resp.text)
except Exception as e:
    print('REQUEST ERROR:', e)
