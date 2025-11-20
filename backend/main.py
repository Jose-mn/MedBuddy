from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.auth import router as auth_router
from routes.symptom_checker import router as symptom_router
from routes.tips import router as tips_router
from routes.premium import router as premium_router
from routes.payments import router as payments_router
import logging
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

logging.basicConfig(level=logging.DEBUG)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("[DEBUG] Database tables created successfully")
except Exception as e:
    print(f"[DEBUG] Database error: {e}")

app = FastAPI(
    title="MedBuddy",
    description="AI-powered health consultation platform aligned with SDG 3",
    version="1.0.0"
)

# Configure CORS - MUST be added as middleware BEFORE routing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://med-buddy-delta.vercel.app",
        "https://medbuddy-ks9e.onrender.com",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Add global exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"[ERROR] {type(exc).__name__}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"{type(exc).__name__}: {str(exc)}"}
    )

# Include routers
print("[DEBUG] Including routers...")
app.include_router(auth_router, tags=["auth"])
app.include_router(symptom_router, tags=["symptom"])
app.include_router(tips_router, prefix="/api", tags=["tips"])
app.include_router(premium_router, tags=["premium"])
app.include_router(payments_router, tags=["payments"])


@app.get("/")
def read_root():
    return {
        "message": "Welcome to MedBuddy - Your Health Assistant",
        "sdg": "SDG 3: Good Health and Well-being",
        "status": "API is running",
        "docs": "Visit /docs for API documentation"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MedBuddy"}


if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)