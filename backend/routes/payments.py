from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/payments", tags=["Payments"])

# Request model for payment
class PaymentRequest(BaseModel):
    plan: str

# Stripe secret key (add yours in .env)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
async def create_checkout_session(request: PaymentRequest):
    plan = request.plan
    prices = {
        "Bronze": 49900,    # Amount in cents
        "Gold": 99900,
        "Diamond": 199900
    }
    if plan not in prices:
        raise HTTPException(status_code=400, detail="Invalid plan")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'kes',
                    'product_data': {'name': f'{plan} Plan'},
                    'unit_amount': prices[plan],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=os.getenv("STRIPE_SUCCESS_URL", "http://127.0.0.1:8000/success.html"),
            cancel_url=os.getenv("STRIPE_CANCEL_URL", "http://127.0.0.1:8000/premium.html")
        )

        return JSONResponse({"url": session.url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

