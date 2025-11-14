from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
try:
    print('about to hash')
    h = pwd_context.hash('889900')
    print('hash ok', h)
except Exception as e:
    print('error:', type(e).__name__, e)
