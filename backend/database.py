from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Get database credentials from environment variables
# Railway provides DATABASE_URL, but we support both that and individual vars
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Railway provides a full DATABASE_URL
    # Convert from postgres format if needed, or use as-is for mysql
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # Fallback to individual environment variables (local development)
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "medbuddy_db")
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY", "sG7!9k2Qx#L8pW4vZ6eR")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    print("[DEBUG] Creating DB session")
    db = SessionLocal()
    try:
        print("[DEBUG] Yielding DB session")
        yield db
    finally:
        print("[DEBUG] Closing DB session")
        db.close()