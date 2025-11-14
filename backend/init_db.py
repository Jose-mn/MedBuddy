"""
Database initialization script - creates all tables in the database.
Run this once after creating the MySQL database to set up the schema.

Usage:
    cd backend
    python init_db.py
"""

from database import engine, Base
from models import User, HealthTip, PremiumPlan
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database by creating all tables."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully!")
        logger.info("Tables created:")
        logger.info("  - users")
        logger.info("  - health_tips")
        logger.info("  - premium_plans")
        
    except Exception as e:
        logger.error(f"✗ Error creating database tables: {e}")
        raise


def seed_sample_data():
    """Optional: Add sample premium plans and health tips."""
    from database import SessionLocal
    
    try:
        db = SessionLocal()
        
        # Check if data already exists
        existing_plans = db.query(PremiumPlan).count()
        if existing_plans == 0:
            logger.info("Seeding sample premium plans...")
            plans = [
                PremiumPlan(
                    name="Monthly",
                    price=9.99,
                    duration_days=30,
                    description="Monthly Premium Plan - Access all features for 30 days"
                ),
                PremiumPlan(
                    name="Quarterly",
                    price=24.99,
                    duration_days=90,
                    description="Quarterly Premium Plan - Access all features for 90 days"
                ),
                PremiumPlan(
                    name="Annual",
                    price=99.99,
                    duration_days=365,
                    description="Annual Premium Plan - Access all features for 365 days"
                ),
            ]
            db.add_all(plans)
            db.commit()
            logger.info(f"✓ Added {len(plans)} premium plans")
        
        # Check and seed health tips
        existing_tips = db.query(HealthTip).count()
        if existing_tips == 0:
            logger.info("Seeding sample health tips...")
            tips = [
                HealthTip(
                    title="Stay Hydrated",
                    content="Drink at least 8 glasses of water daily to maintain proper hydration and support body functions."
                ),
                HealthTip(
                    title="Regular Exercise",
                    content="Aim for at least 150 minutes of moderate-intensity exercise per week to improve cardiovascular health."
                ),
                HealthTip(
                    title="Balanced Diet",
                    content="Eat a variety of fruits, vegetables, whole grains, and lean proteins for optimal nutrition."
                ),
                HealthTip(
                    title="Quality Sleep",
                    content="Get 7-9 hours of quality sleep each night to support immune function and mental health."
                ),
                HealthTip(
                    title="Stress Management",
                    content="Practice meditation, yoga, or deep breathing exercises to reduce stress and improve mental well-being."
                ),
            ]
            db.add_all(tips)
            db.commit()
            logger.info(f"✓ Added {len(tips)} health tips")
        
        db.close()
        
    except Exception as e:
        logger.error(f"✗ Error seeding sample data: {e}")
        raise


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("MedBuddy Database Initialization")
    logger.info("=" * 50)
    
    # Create tables
    init_db()
    
    # Seed sample data (optional)
    seed_sample_data()
    
    logger.info("=" * 50)
    logger.info("Database initialization complete!")
    logger.info("=" * 50)
