from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        # Check if password exceeds 72 bytes when encoded
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError('Password is too long (max 72 bytes)')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class SymptomRequest(BaseModel):
    symptoms: str
    user_id: Optional[int] = None

class SymptomResponse(BaseModel):
    analysis: str
    recommendation: str
    severity: str

class TipResponse(BaseModel):
    tip: str
    category: str


class PaymentRequest(BaseModel):
    user_id: Optional[int]
    plan_id: Optional[int]
    plan_name: Optional[str] = None
    amount: int  # amount in cents (integer)

    class Config:
        from_attributes = True