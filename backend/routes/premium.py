from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, PremiumPlan
from datetime import datetime, timedelta

router = APIRouter(prefix="/premium", tags=["Premium Plans"])

# Create available premium plans
@router.post("/create")
def create_plan(name: str, price: int, duration_days: int, description: str, db: Session = Depends(get_db)):
    plan = PremiumPlan(name=name, price=price, duration_days=duration_days, description=description)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {"message": "Premium plan created", "plan": plan}

# List all available plans
@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    plans = db.query(PremiumPlan).all()
    return plans

# Subscribe user to a plan
@router.post("/subscribe/{user_id}/{plan_id}")
def subscribe_user(user_id: int, plan_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    plan = db.query(PremiumPlan).filter(PremiumPlan.id == plan_id).first()

    if not user or not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Plan not found")

    expiry_date = datetime.utcnow() + timedelta(days=plan.duration_days)
    user.premium_status = "active"
    user.plan_id = plan.id
    user.plan_expiry = expiry_date

    db.commit()
    db.refresh(user)
    return {"message": f"{user.username} subscribed to {plan.name} plan", "expiry": expiry_date}

# Check subscription status
@router.get("/status/{user_id}")
def check_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    status_msg = {
        "username": user.username,
        "premium_status": user.premium_status,
        "plan_id": user.plan_id,
        "plan_expiry": user.plan_expiry
    }
    return status_msg
