from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update database URL with your MySQL credentials
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:8877@localhost/medbuddy_db"

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