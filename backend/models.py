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
    premium_status = Column(String(20), default="free")  # free, active, expired
    plan_id = Column(Integer, nullable=True)
    plan_expiry = Column(DateTime, nullable=True)

    
class HealthTip(Base):
    __tablename__ = "health_tips"

    id = Column(Integer, primary_key=True, index=True)
    tip_text = Column(Text, nullable=False)
    category = Column(String(50), default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PremiumPlan(Base):
    __tablename__ = "premium_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
