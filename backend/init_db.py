"""
Database initialization script to create/recreate tables
Run this once to set up the database schema
"""
from database import engine, Base
from models import User, HealthTip, PremiumPlan

# Drop all existing tables and recreate them
print("Dropping existing tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("✓ Database tables created successfully!")
print("Tables created:")
print("  - users")
print("  - health_tips")
print("  - premium_plans")
