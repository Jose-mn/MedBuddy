from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class HealthTip(Base):
    __tablename__ = "health_tips"

    id = Column(Integer, primary_key=True, index=True)
    tip_text = Column(Text, nullable=False)
    category = Column(String(50), default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())