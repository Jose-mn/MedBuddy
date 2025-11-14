from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, LoginRequest, Token
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

SECRET_KEY = "medconsult_secret_key_12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    # Ensure input is bytes and truncate to 72 bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    truncated = plain_password[:72]
    try:
        return bcrypt.checkpw(truncated, hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password):
    # Ensure input is bytes and truncate to 72 bytes before hashing
    if isinstance(password, str):
        password = password.encode('utf-8')
    truncated = password[:72]
    hashed = bcrypt.hashpw(truncated, bcrypt.gensalt())
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    print(f"[DEBUG] Signup called for user: {user.username}")
    # Check if user exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"[DEBUG] Signup successful for user: {user.username}")
    
    return db_user

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    print(f"[DEBUG] Login called for user: {login_data.username}")
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    print(f"[DEBUG] Login successful for user: {login_data.username}")
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username
    )