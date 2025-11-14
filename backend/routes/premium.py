from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, PremiumPlan
import logging

router = APIRouter(prefix="/premium", tags=["premium"])

logger = logging.getLogger(__name__)


@router.post("/create")
def create_premium_plan(name: str, price: float, duration_days: int, db: Session = Depends(get_db)):
    """
    Create a new premium plan.
    
    Query parameters:
    - name: Plan name (e.g., "Monthly Premium")
    - price: Price in USD
    - duration_days: Duration of the plan in days
    """
    try:
        existing = db.query(PremiumPlan).filter(PremiumPlan.name == name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Premium plan '{name}' already exists"
            )
        
        plan = PremiumPlan(
            name=name,
            price=price,
            duration_days=duration_days,
            description=f"{name} - ${price:.2f} for {duration_days} days"
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        logger.info(f"Premium plan created: {plan.name} (ID: {plan.id})")
        
        return {
            "id": plan.id,
            "name": plan.name,
            "price": plan.price,
            "duration_days": plan.duration_days,
            "description": plan.description
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating premium plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating premium plan: {str(e)}"
        )


@router.get("/plans")
def get_premium_plans(db: Session = Depends(get_db)):
    """
    Get all available premium plans.
    """
    try:
        plans = db.query(PremiumPlan).all()
        
        return {
            "plans": [
                {
                    "id": plan.id,
                    "name": plan.name,
                    "price": plan.price,
                    "duration_days": plan.duration_days,
                    "description": plan.description
                }
                for plan in plans
            ],
            "total": len(plans)
        }
    except Exception as e:
        logger.error(f"Error fetching premium plans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching premium plans: {str(e)}"
        )


@router.post("/subscribe/{user_id}/{plan_id}")
def subscribe_to_plan(user_id: int, plan_id: int, db: Session = Depends(get_db)):
    """
    Subscribe a user to a premium plan.
    
    Path parameters:
    - user_id: ID of the user
    - plan_id: ID of the premium plan
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        plan = db.query(PremiumPlan).filter(PremiumPlan.id == plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Premium plan with ID {plan_id} not found"
            )
        
        # Update user's premium plan
        user.premium_plan_id = plan_id
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user_id} subscribed to plan {plan_id}")
        
        return {
            "user_id": user.id,
            "plan_id": plan.id,
            "plan_name": plan.name,
            "status": "subscribed",
            "message": f"Successfully subscribed to {plan.name}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error subscribing user to plan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error subscribing to plan: {str(e)}"
        )


@router.get("/status/{user_id}")
def get_subscription_status(user_id: int, db: Session = Depends(get_db)):
    """
    Get premium subscription status for a user.
    
    Path parameters:
    - user_id: ID of the user
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        if not user.premium_plan_id:
            return {
                "user_id": user.id,
                "premium_plan_id": None,
                "is_premium": False,
                "message": "User is not subscribed to a premium plan"
            }
        
        plan = db.query(PremiumPlan).filter(PremiumPlan.id == user.premium_plan_id).first()
        
        return {
            "user_id": user.id,
            "premium_plan_id": plan.id if plan else None,
            "plan_name": plan.name if plan else None,
            "is_premium": True,
            "message": f"User is subscribed to {plan.name if plan else 'Unknown plan'}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching subscription status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscription status: {str(e)}"
        )
