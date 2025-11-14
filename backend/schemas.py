from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

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