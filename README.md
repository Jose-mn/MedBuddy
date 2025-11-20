# MedBuddy

MedBuddy is an AI-assisted health consultation platform with a FastAPI backend and static HTML/CSS/JavaScript frontend. It provides symptom checking, user authentication with JWT tokens, health tips, and Stripe-based premium plans.

View the project online:

Frontend: med-buddy-delta.vercel.app

Backend: https://medbuddy-ks9e.onrender.com

Contents

Features

Tech Stack

Quick Start (Windows)

Development Setup

Database Setup

Environment Variables

Running the Backend

Running the Frontend

API Endpoints

Troubleshooting

Quick Test with cURL

Helper Files

Features

✅ Symptom checker (rule-based analyzer)

✅ User signup/login with bcrypt password hashing and JWT tokens

✅ Health tips endpoint (random & all tips)

✅ Premium plans with Stripe checkout integration

✅ MySQL database with SQLAlchemy ORM

✅ Auto-generated API documentation at /docs

✅ CORS configured for frontend access

Tech Stack

Backend: Python 3.11+ (FastAPI, SQLAlchemy)

Auth: bcrypt for password hashing + JWT tokens

Database: MySQL with mysql-connector-python

Frontend: Static HTML/CSS/Vanilla JavaScript

Payments: Stripe (server-side checkout sessions)

Config: python-dotenv for environment variables

Quick Start (Windows)
1. Clone and navigate to backend
git clone https://github.com/yourusername/MedBuddy.git
cd MedBuddy\backend

2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Create .env file with database credentials
copy .env.example .env


Edit .env with your database password and Stripe keys.

5. Create MySQL database
CREATE DATABASE medbuddy_db;

6. Initialize database tables
python init_db.py

7. Start the backend server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload


Visit http://127.0.0.1:8000/docs
 for interactive API documentation.

8. Start the frontend

Open frontend/index.html with Live Server (VS Code extension) or any local server at http://127.0.0.1:5500/

Development Setup

Backend working directory: d:\Medbuddy\backend
Frontend files: d:\Medbuddy\frontend

Virtual environment commands (Windows):

Activate: .\venv\Scripts\activate

Deactivate: deactivate

Use venv Python directly: .\venv\Scripts\python <script>.py

⚠️ Important: Always run backend commands with the venv Python to ensure installed packages are available.

Database Setup

Ensure MySQL is running

Create the database:

CREATE DATABASE medbuddy_db;


Update credentials in .env:

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=medbuddy_db


Run the initialization script:

python init_db.py


⚠️ init_db.py drops and recreates tables — use only in development.

Environment Variables

Create a .env file in backend/ based on .env.example:

# Database credentials
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=medbuddy_db

# Stripe API keys
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_test_XXXXXXXXXXXXXXXX

# Stripe redirect URLs
STRIPE_SUCCESS_URL=http://127.0.0.1:5500/index.html
STRIPE_CANCEL_URL=http://127.0.0.1:5500/premium.html

# Optional: Frontend URL
FRONTEND_URL=http://127.0.0.1:5500


⚠️ SECURITY: Never commit .env to version control.

Running the Backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload


Server starts on http://127.0.0.1:8000

API docs available at http://127.0.0.1:8000/docs

Database tables created if first run

CORS configured for frontend origin

Running the Frontend

Option A: Live Server (VS Code)

Right-click frontend/ → Open with Live Server → Opens at http://127.0.0.1:5500/

Option B: Python built-in server

cd frontend
python -m http.server 5500

API Endpoints
Authentication

POST /auth/signup — Create user

POST /auth/login — Login and get JWT token

Symptom Checker

POST /symptom/analyze — Analyze symptoms

Health Tips

GET /api/tips/random

GET /api/tips/all

Premium Plans

GET /premium/plans

POST /premium/subscribe/{user_id}/{plan_id}

GET /premium/status/{user_id}

Payments

POST /api/payments/create-checkout-session — Create Stripe checkout

Troubleshooting

CORS issues: Ensure backend is running and frontend served from correct origin

500 errors: Check password length (<72 bytes), or missing packages

Stripe errors: Check .env keys and use test mode cards

Database errors: Run python init_db.py to recreate tables

Quick Test with cURL
# Signup
curl -X POST http://127.0.0.1:8000/auth/signup -H "Content-Type: application/json" -d '{"username":"testuser","email":"test@example.com","password":"passwd123"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username":"testuser","password":"passwd123"}'

# Random health tip
curl http://127.0.0.1:8000/api/tips/random

# Stripe checkout session
curl -X POST http://127.0.0.1:8000/api/payments/create-checkout-session -H "Content-Type: application/json" -d '{"user_id":1,"plan_id":1,"plan_name":"Premium Monthly","amount":999}'

# Get subscription status
curl http://127.0.0.1:8000/premium/status/1

Helper Files

.env.example — Template for environment variables

.gitignore — Protects sensitive files

init_db.py — Database initialization script

setup.ps1 — Optional PowerShell helper

CONTRIBUTING.md — Development workflow guide

LICENSE — MIT License

Security Notes

⚠️ Before Production:

Database credentials from .env

.gitignore prevents .env from being committed

Rotate passwords if exposed

Use strong database passwords

Use live Stripe keys

Enable HTTPS

Run FastAPI behind production server

Input validation & rate limiting

- The backend is a prototype/demo and is **not production-hardened**.
- Always use the virtual environment Python to avoid missing package errors.
- CORS is configured to allow `http://127.0.0.1:5500` (Live Server) during development.
- The `.gitignore` file protects sensitive files from being committed.
