from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# ===== DATABASE CONNECTION =====

# Railway provides DATABASE_URL or you can use individual env vars
DATABASE_URL = os.getenv("DATABASE_URL")

# If no DATABASE_URL is provided in the environment, fall back to the Render
# Postgres URL you supplied. This makes local testing and deployments easier
# (you can override with an env var). Replace this with your own URL if you
# want it hidden.
if not DATABASE_URL:
    DATABASE_URL = (
        "postgresql://medbuddy_db_7968_user:"
        "l0sxJILpuHWh6C2BIAfpgQXfBgF4GyEA@dpg-d4flhqlrnu6s73e75fvg-a.oregon-postgres.render.com/medbuddy_db_7968"
    )

if DATABASE_URL:
    # Normalize provider URLs to use psycopg2 explicitly for SQLAlchemy.
    # Handle both `postgres://` and `postgresql://` prefixes.
    if isinstance(DATABASE_URL, str) and DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql+psycopg2://", 1
        )
    elif isinstance(DATABASE_URL, str) and DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )
    else:
        SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # Fallback to individual env vars for local dev
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "medbuddy_db")
    DB_PORT = os.getenv("DB_PORT", "3306")  # default MySQL port

    # Build a MySQL connection string for local development
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


# ===== ENGINE & SESSION =====
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ===== SECRET KEY =====
SECRET_KEY = os.getenv("SECRET_KEY", "sG7!9k2Qx#L8pW4vZ6eR")

# ===== DB DEPENDENCY =====
def get_db():
    print("[DEBUG] Creating DB session")
    db = SessionLocal()
    try:
        print("[DEBUG] Yielding DB session")
        yield db
    finally:
        print("[DEBUG] Closing DB session")
        db.close()
