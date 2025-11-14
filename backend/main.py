from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.auth import router as auth_router
from routes.symptom_checker import router as symptom_router
from routes.tips import router as tips_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedConsult AI",
    description="AI-powered health consultation platform aligned with SDG 3",
    version="1.0.0"
)

# Add global exception handler for debugging
import logging
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"[ERROR] {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)}
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(symptom_router)
app.include_router(tips_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MedConsult AI - Your Health Assistant",
        "sdg": "SDG 3: Good Health and Well-being",
        "status": "API is running",
        "docs": "Visit /docs for API documentation"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MedConsult AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)