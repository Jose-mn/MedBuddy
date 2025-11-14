from fastapi import APIRouter
from schemas import TipResponse
import random

router = APIRouter(prefix="/tips", tags=["health_tips"])

HEALTH_TIPS = [
    {"tip": "Health is wealth — take care of your body, it's your only home.", "category": "motivation"},
    {"tip": "Drink at least 8 glasses of water daily to stay properly hydrated.", "category": "nutrition"},
    {"tip": "A 30-minute walk can significantly improve your mood and cardiovascular health.", "category": "exercise"},
    {"tip": "Sleep is the best meditation - aim for 7-9 hours of quality sleep each night.", "category": "sleep"},
    {"tip": "Practice deep breathing exercises to reduce stress and improve mental clarity.", "category": "mental_health"},
    {"tip": "Eat a rainbow of fruits and vegetables to get diverse nutrients.", "category": "nutrition"},
    {"tip": "Take regular breaks from screens to protect your eye health and mental wellbeing.", "category": "digital_health"},
    {"tip": "Wash your hands regularly to prevent the spread of germs and infections.", "category": "hygiene"},
    {"tip": "Practice gratitude daily - it can improve your mental and physical health.", "category": "mental_health"},
    {"tip": "Stretch daily to maintain flexibility and prevent muscle stiffness.", "category": "exercise"},
    {"tip": "Limit processed foods and focus on whole, natural ingredients.", "category": "nutrition"},
    {"tip": "Stay connected with loved ones - social connections are vital for wellbeing.", "category": "mental_health"},
    {"tip": "Get regular health check-ups - prevention is better than cure.", "category": "prevention"},
    {"tip": "Practice good posture to prevent back and neck pain.", "category": "posture"},
    {"tip": "Spend time in nature to reduce stress and boost your immune system.", "category": "mental_health"}
]

@router.get("/random", response_model=TipResponse)
def get_random_tip():
    tip = random.choice(HEALTH_TIPS)
    return TipResponse(tip=tip["tip"], category=tip["category"])

@router.get("/all")
def get_all_tips():
    return [TipResponse(tip=tip["tip"], category=tip["category"]) for tip in HEALTH_TIPS]