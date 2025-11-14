from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import PaymentRequest
import stripe
import os
import logging

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Initialize Stripe with API key from environment
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

logger = logging.getLogger(__name__)


@router.post("/create-checkout-session")
def create_checkout_session(request: PaymentRequest, db: Session = Depends(get_db)):
    """
    Create a Stripe checkout session for premium plan subscription.
    
    Expected request body:
    {
        "user_id": 1,
        "plan_id": 1,
        "plan_name": "Premium Monthly",
        "amount": 999
    }
    """
    try:
        # Validate the payment request
        if not request.user_id or not request.plan_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id and plan_id are required"
            )

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": request.plan_name or "Premium Plan",
                            "description": f"Premium plan for user {request.user_id}",
                        },
                        "unit_amount": int(request.amount),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=os.getenv("STRIPE_SUCCESS_URL", "http://127.0.0.1:5500/index.html"),
            cancel_url=os.getenv("STRIPE_CANCEL_URL", "http://127.0.0.1:5500/premium.html"),
            metadata={
                "user_id": request.user_id,
                "plan_id": request.plan_id,
            }
        )

        logger.info(f"Checkout session created: {session.id} for user {request.user_id}")
        
        return {
            "session_id": session.id,
            "checkout_url": session.url,
            "status": "success"
        }

    except stripe.error.CardError as e:
        logger.error(f"Card error: {e.user_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Card error: {e.user_message}"
        )
    except stripe.error.StripeException as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment processing error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating checkout session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating checkout session: {str(e)}"
        )

