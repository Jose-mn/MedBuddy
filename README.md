# MedBuddy

**MedBuddy** is an AI-assisted health consultation platform with a FastAPI backend and static HTML/CSS/JavaScript frontend. It provides symptom checking, user authentication with JWT tokens, health tips, and Stripe-based premium plans.

This README explains how to set up, run, and troubleshoot the project locally (Windows-focused).

---

## Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start (Windows)](#quick-start-windows)
- [Development Setup](#development-setup)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Quick Test with cURL](#quick-test-with-curl)
- [Helper Files](#helper-files)

---

## Features

- ✅ Symptom checker (rule-based analyzer)
- ✅ User signup/login with bcrypt password hashing and JWT tokens
- ✅ Health tips endpoint with random and all tips endpoints
- ✅ Premium plans with Stripe checkout integration
- ✅ MySQL database with SQLAlchemy ORM
- ✅ Auto-generated API documentation at `/docs`
- ✅ CORS configured for frontend access

---

## Tech Stack

- **Backend:** Python 3.11+ (FastAPI, SQLAlchemy)
- **Auth:** `bcrypt` for password hashing + JWT tokens
- **Database:** MySQL with `mysql-connector-python`
- **Frontend:** Static HTML/CSS/Vanilla JavaScript
- **Payments:** Stripe (server-side checkout sessions)
- **Config:** `python-dotenv` for environment variables

---

## Quick Start (Windows)

### 1. Clone and navigate to backend

```powershell
git clone https://github.com/yourusername/MedBuddy.git
cd MedBuddy\backend
```

### 2. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create `.env` file with database credentials

Copy `.env.example` to `.env` and fill in your MySQL credentials:

```powershell
copy .env.example .env
```

Edit `.env` with your database password and Stripe keys.

### 5. Create MySQL database

```sql
CREATE DATABASE medbuddy_db;
```

### 6. Initialize database tables

```powershell
python init_db.py
```

### 7. Start the backend server

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 8. Start the frontend

Open `frontend/index.html` with Live Server (VS Code extension) or any local server at `http://127.0.0.1:5500/`

---

## Development Setup

**Backend working directory:** `d:\Medbuddy\backend`  
**Frontend files:** `d:\Medbuddy\frontend`

### Virtual environment commands (Windows):

- Activate: `.\venv\Scripts\activate`
- Deactivate: `deactivate`
- Use venv Python directly: `.\venv\Scripts\python <script>.py`

⚠️ **Important:** Always run backend commands with the venv Python to ensure installed packages are available.

---

## Database Setup

The project uses SQLAlchemy models in `backend/models.py`. The `init_db.py` helper script initializes all tables.

### Steps:

1. **Ensure MySQL is running** and accessible

2. **Create the database:**

```sql
CREATE DATABASE medbuddy_db;
```

3. **Update credentials in `.env`:**

```
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=medbuddy_db
```

4. **Run the initialization script:**

```powershell
python init_db.py
```

⚠️ **Note:** `init_db.py` drops and recreates tables — use only in development.

---

## Environment Variables

Create a `.env` file in `backend/` based on `.env.example`:

```bash
# Database credentials (REQUIRED)
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=medbuddy_db

# Stripe API keys (get from https://dashboard.stripe.com/apikeys)
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_test_XXXXXXXXXXXXXXXX

# Stripe redirect URLs
STRIPE_SUCCESS_URL=http://127.0.0.1:5500/index.html
STRIPE_CANCEL_URL=http://127.0.0.1:5500/premium.html

# Optional: Frontend URL
FRONTEND_URL=http://127.0.0.1:5500
```

⚠️ **SECURITY:** Never commit `.env` to version control. The `.gitignore` file protects it.

---

## Running the Backend

From `d:\Medbuddy\backend` with venv activated:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### What to see:

- Server starts on `http://127.0.0.1:8000`
- API docs available at `http://127.0.0.1:8000/docs`
- Database tables created (if first run)
- CORS configured for frontend origin

---

## Running the Frontend

**Option A (Recommended):** Use Live Server (VS Code extension)

1. Right-click `frontend/` folder
2. Select "Open with Live Server"
3. Opens at `http://127.0.0.1:5500/`

**Option B:** Any local HTTP server

```powershell
# Python built-in server example
cd frontend
python -m http.server 5500
```

---

## API Endpoints

### Authentication

- **POST** `/auth/signup` — Create user
  - Body: `{ "username": "...", "email": "...", "password": "..." }`
  - Returns: `{ "id": 1, "username": "...", "email": "..." }`

- **POST** `/auth/login` — Login and get JWT token
  - Body: `{ "username": "...", "password": "..." }`
  - Returns: `{ "access_token": "...", "token_type": "bearer" }`

### Symptom Checker

- **POST** `/symptom/analyze` — Analyze symptoms
  - Body: `{ "symptoms": "fever, cough", "user_id": null }`
  - Returns: `{ "severity": "moderate", "recommendations": [...] }`

### Health Tips

- **GET** `/api/tips/random` — Get random health tip
  - Returns: `{ "id": 1, "title": "...", "content": "..." }`

- **GET** `/api/tips/all` — Get all health tips
  - Returns: `{ "tips": [...], "total": 5 }`

### Premium Plans

- **GET** `/premium/plans` — List all premium plans
  - Returns: `{ "plans": [...], "total": 3 }`

- **POST** `/premium/subscribe/{user_id}/{plan_id}` — Subscribe user to plan
  - Returns: `{ "user_id": 1, "plan_name": "Premium Monthly", "status": "subscribed" }`

- **GET** `/premium/status/{user_id}` — Get subscription status
  - Returns: `{ "is_premium": true, "plan_name": "Premium Monthly" }`

### Payments

- **POST** `/api/payments/create-checkout-session` — Create Stripe checkout
  - Body: `{ "user_id": 1, "plan_id": 1, "plan_name": "Premium Monthly", "amount": 999 }`
  - Returns: `{ "session_id": "...", "checkout_url": "...", "status": "success" }`

---

## Troubleshooting

### CORS blocked (browser error: No 'Access-Control-Allow-Origin' header)

- Ensure backend is running: `uvicorn main:app --reload`
- Hard-refresh frontend: `Ctrl+F5`
- Verify frontend is served from `http://127.0.0.1:5500`
- Check browser console for specific error

### 500 errors on signup

- Bcrypt has a 72-byte limit on passwords
- Backend automatically truncates passwords before hashing
- Use normal UTF-8 passwords shorter than ~72 bytes

### Missing Python packages (ImportError)

```powershell
# Activate venv
.\venv\Scripts\activate

# Install/reinstall requirements
pip install -r requirements.txt
```

### Stripe errors

- Ensure `.env` has `STRIPE_SECRET_KEY` set
- Use **test keys** for development (start with `sk_test_` and `pk_test_`)
- Visit https://dashboard.stripe.com/apikeys for your keys

### Database errors (unknown column, etc.)

```powershell
# Recreate tables (development only - deletes all data)
python init_db.py
```

---

## Quick Test with cURL

Use these commands from PowerShell to test endpoints. Replace `127.0.0.1:8000` if needed.

### Signup

```powershell
curl -X POST http://127.0.0.1:8000/auth/signup `
    -H "Content-Type: application/json" `
    -d '{"username":"testuser","email":"test@example.com","password":"passwd123"}'
```

### Login

```powershell
curl -X POST http://127.0.0.1:8000/auth/login `
    -H "Content-Type: application/json" `
    -d '{"username":"testuser","password":"passwd123"}'
```

### Get random health tip

```powershell
curl http://127.0.0.1:8000/api/tips/random
```

### Create Stripe checkout session

```powershell
curl -X POST http://127.0.0.1:8000/api/payments/create-checkout-session `
    -H "Content-Type: application/json" `
    -d '{"user_id":1,"plan_id":1,"plan_name":"Premium Monthly","amount":999}'
```

### Get subscription status

```powershell
curl http://127.0.0.1:8000/premium/status/1
```

---

## Helper Files

- **`.env.example`** — Template for environment variables. Copy to `.env` and fill in credentials.
- **`.gitignore`** — Prevents sensitive files (`.env`, `venv/`, `__pycache__/`) from being committed.
- **`init_db.py`** — Database initialization script. Creates and optionally seeds sample data.
- **`setup.ps1`** — PowerShell helper to automate setup (optional).
- **`CONTRIBUTING.md`** — Local development workflow and contribution guidelines.
- **`LICENSE`** — MIT license file.

---

## Security Notes

⚠️ **Before Production:**

1. ✅ Database credentials are read from `.env` (not hardcoded) — DONE
2. ✅ `.gitignore` prevents `.env` from being committed — DONE
3. ❌ Rotate exposed password if it was ever visible in git history
4. Use **strong** database passwords
5. Use **live** Stripe keys (not test keys)
6. Enable HTTPS on production
7. Run FastAPI behind a production WSGI server (e.g., Gunicorn)
8. Implement rate limiting and input validation for production

---

## Notes

- The backend is a prototype/demo and is **not production-hardened**.
- Always use the virtual environment Python to avoid missing package errors.
- CORS is configured to allow `http://127.0.0.1:5500` (Live Server) during development.
- The `.gitignore` file protects sensitive files from being committed.
