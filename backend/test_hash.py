from routes.auth import get_password_hash

try:
    print(get_password_hash('889900'))
    print('Hashing succeeded')
except Exception as e:
    print('Hashing error:', type(e).__name__, e)
