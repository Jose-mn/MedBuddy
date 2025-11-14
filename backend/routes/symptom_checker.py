from fastapi import APIRouter, HTTPException
from schemas import SymptomRequest, SymptomResponse

router = APIRouter(prefix="/symptom", tags=["symptom_checker"])

@router.post("/analyze", response_model=SymptomResponse)
def analyze_symptoms(symptom_request: SymptomRequest):
    symptoms = symptom_request.symptoms.lower().strip()
    
    if not symptoms:
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    
    # Simple AI-like symptom analysis
    if any(word in symptoms for word in ["cough", "flu", "cold", "sneeze", "congestion", "runny nose"]):
        return SymptomResponse(
            analysis="Mild respiratory symptoms detected",
            recommendation="Rest well, drink plenty of fluids, and consider over-the-counter cold medicine. If symptoms persist for more than 3 days or you develop a high fever, consult a doctor.",
            severity="mild"
        )
    elif any(word in symptoms for word in ["stomach", "vomit", "nausea", "diarrhea", "indigestion", "abdominal"]):
        return SymptomResponse(
            analysis="Digestive system symptoms detected",
            recommendation="Stay hydrated with water or electrolyte solutions. Eat bland foods like bananas, rice, applesauce, and toast. Avoid spicy or fatty foods. If symptoms persist for more than 24 hours, seek medical attention.",
            severity="moderate"
        )
    elif any(word in symptoms for word in ["headache", "migraine"]):
        return SymptomResponse(
            analysis="Headache symptoms detected",
            recommendation="Rest in a quiet, dark room. Stay hydrated and consider over-the-counter pain relief. If headache is severe or accompanied by vision changes, seek immediate medical care.",
            severity="mild"
        )
    elif any(word in symptoms for word in ["fever", "high temperature", "chills"]):
        return SymptomResponse(
            analysis="Fever detected",
            recommendation="Rest, stay hydrated, and monitor your temperature. Use fever-reducing medication as directed. If fever is above 103°F (39.4°C) or persists for more than 3 days, consult a doctor.",
            severity="moderate"
        )
    elif any(word in symptoms for word in ["chest pain", "shortness of breath", "difficulty breathing"]):
        return SymptomResponse(
            analysis="Serious symptoms detected",
            recommendation="These symptoms require immediate medical attention. Please seek emergency care or call your local emergency number immediately.",
            severity="severe"
        )
    else:
        return SymptomResponse(
            analysis="General symptoms reported",
            recommendation="Please consult a healthcare professional for accurate diagnosis and treatment. Monitor your symptoms and seek immediate care if they worsen.",
            severity="unknown"
        )