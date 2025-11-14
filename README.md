# MedBuddy

**MedBuddy** is a web-based AI-powered medical consultation platform designed to help users assess symptoms, receive personalized health advice, and access premium health services online. The project aligns with **SDG 3: Good Health and Well-being** and aims to make healthcare more accessible and convenient through technology.

---

## Table of Contents

1. [Features](#features)  
2. [Tech Stack](#tech-stack)  
3. [Architecture](#architecture)  
4. [Getting Started](#getting-started)  
 # MedBuddy

MedBuddy is a small AI-assisted health consultation prototype: a FastAPI backend + static frontend (HTML/CSS/JS). It provides a symptom checker, user authentication, health tips, and Stripe-based premium plans.

This README explains how to set up, run and troubleshoot the project locally (Windows-focused), and documents the main API endpoints used by the frontend.

---

## Contents

- Features
- Tech stack
- Quick start (Windows)
- Development setup (detailed)
- Database setup
- Environment variables (.env)
- Running the backend
- Running the frontend
- API endpoints (paths)
- Troubleshooting
- Notes & tips

---

## Features

- Symptom checker (simple rule-based analyzer)
- User signup/login with password hashing and JWT token generation
- Health tips endpoint and a floating quotes widget on the frontend
- Premium plans powered by Stripe checkout sessions
- MySQL + SQLAlchemy models for users, tips and premium plans

---

## Tech stack

- Backend: Python 3.11+ (FastAPI, SQLAlchemy)
- Auth: `bcrypt` for password hashing + JWT tokens
- Database: MySQL (tested with `mysql-connector-python`)
- Frontend: Static HTML/CSS/Vanilla JS
- Payments: Stripe (server-side checkout sessions)
- Config: `python-dotenv` for local environment variables

---

## Quick start (Windows)

1. Open PowerShell and clone the repo:

```powershell
git clone https://github.com/yourusername/MedBuddy.git
cd MedBuddy\backend
```

2. Create and activate a virtual environment (Windows):

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` folder (see "Environment variables" section below).

5. Create the MySQL database (example name: `medbuddy_db`) and run the DB init script:

```powershell
# Make sure your MySQL server is running and credentials in database.py match
python init_db.py
```

6. Start the backend server:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

7. Open the frontend static files with Live Server (VS Code extension) or any static server that serves files from the `frontend/` folder, or just open the files in your browser. If using Live Server, it commonly serves at `http://127.0.0.1:5500/`.

---

## Development setup (details)

- Backend working directory: `d:\Medbuddy\backend`
- Frontend files: `d:\Medbuddy\frontend` (open the .html files directly or use a static server)
- Virtual environment commands (Windows):
    - Activate: `.\venv\Scripts\activate`
    - Use the venv Python explicitly if not activated: `.\venv\Scripts\python <script>.py`

Important: run backend commands using the venv Python to ensure installed packages are available.

---

## Database setup

The project uses SQLAlchemy models in `backend/models.py`. A helper `init_db.py` drops and recreates tables for development.

1. Ensure MySQL is running and `backend/database.py` connection string (`SQLALCHEMY_DATABASE_URL`) matches your user/password and database name.
2. Create the database in MySQL (example):

```sql
CREATE DATABASE medbuddy_db;
```

3. Run the initialization script to create tables:

```powershell
cd d:\Medbuddy\backend
.\venv\Scripts\python init_db.py
```

Note: `init_db.py` will drop existing tables. Use with care and only during development.

---

## Environment variables (.env)

Create a `.env` file in `backend/` with the following (example):

```
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXX
STRIPE_PUBLISHABLE_KEY=pk_test_XXXXXXXXXXXXXXXX
STRIPE_SUCCESS_URL=http://127.0.0.1:5500/success.html
STRIPE_CANCEL_URL=http://127.0.0.1:5500/premium.html
# Optionally add a JWT secret if you want to override the default
# JWT_SECRET_KEY=your_jwt_secret
```

The project also reads database credentials from `database.py` directly (update `SQLALCHEMY_DATABASE_URL` if needed).

---

## Running the backend

From `d:\Medbuddy\backend` with venv activated:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Visit `http://127.0.0.1:8000/docs` to view the auto-generated API docs.

---

## Running the frontend

- Option A (recommended during development): Install Live Server (VS Code) and "Open with Live Server" the `frontend` folder root. It usually serves at `http://127.0.0.1:5500/`.
- Option B: Right-click each `.html` file and open in browser (some features expect the site to be served from a local server for CORS/preflight behavior).

---

## API endpoints (important routes)

These are the endpoints the frontend expects (relative to the backend base `http://127.0.0.1:8000`):

- POST `/auth/signup` — Create user. JSON body: `{ "username": "...", "email": "...", "password": "..." }`
- POST `/auth/login` — Login. JSON body: `{ "username": "...", "password": "..." }`
- POST `/symptom/analyze` — Symptom analysis. JSON: `{ "symptoms": "...", "user_id": <int or null> }`
- GET `/api/tips/random` — Returns a random health tip (used on the home page)
- GET `/api/tips/all` — Returns all tips
- POST `/api/payments/create-checkout-session` — Create Stripe checkout session. JSON: `{ "plan": "Gold" }`
- Premium admin endpoints: `/premium/*` (create/list/subscribe/status) — used by server-side admin flows

Open `/docs` for a browsable set of API schemas when server is running.

---

## Troubleshooting

Common issues and fixes:

- CORS blocked requests (browser error: **No 'Access-Control-Allow-Origin' header**):
    - Ensure the backend is running and did not crash (a 500 will cause the browser to receive no CORS headers).
    - Start the backend from the project's venv: `.\venv\Scripts\activate` then `uvicorn main:app --reload`.
    - Hard-refresh the frontend (Ctrl+F5) after restarting backend.

- 500 errors on signup (bcrypt / password length):
    - `bcrypt` has a 72-byte limit. The backend truncates passwords to 72 bytes before hashing. If you hit an error, make sure your password is a normal UTF-8 string and shorter than ~72 bytes.

- Missing Python packages (ImportError):
    - Activate venv before running code: `.\venv\Scripts\activate`.
    - Install requirements: `pip install -r requirements.txt`.

- Stripe issues:
    - Ensure `STRIPE_SECRET_KEY` is set in `.env` and that test keys are used for development.

- Database errors (unknown column etc.):
    - Run `init_db.py` to recreate tables if models changed during development. This will drop and recreate tables — only do this in development.

---

## Quick test with curl (examples)

Use these commands from a shell on the machine that can reach the backend (or use WSL/PowerShell). Replace `127.0.0.1:8000` if your backend uses a different host/port.

- Signup (create user):

```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","email":"test@example.com","password":"passwd123"}'
```

- Login (get token):

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"passwd123"}'
```

- Get a random tip:

```bash
curl http://127.0.0.1:8000/api/tips/random
```

- Create Stripe checkout session (example):

```bash
curl -X POST http://127.0.0.1:8000/api/payments/create-checkout-session \
    -H "Content-Type: application/json" \
    -d '{"plan":"Gold"}'
```

Note: cURL requests bypass browser CORS limitations and are useful for debugging server-side behavior.

---

## Added helper files

- `backend/.env.example` — template env vars to copy into `backend/.env`.
- `backend/setup.ps1` — PowerShell helper to create venv, install deps, copy `.env.example` -> `.env`, run `init_db.py`, and start the server (development only). Edit DB credentials in `database.py` or set env vars before running.
- `CONTRIBUTING.md` — local dev workflow and guidelines.
- `LICENSE` — MIT license file.


## Notes & tips

- Always run backend with the virtual environment Python to avoid missing package issues.
- Use `http://127.0.0.1:5500` (Live Server) as the frontend origin during development — CORS is configured to allow this.
- The repository is a prototype/demo; it is not production hardened.

---

If you'd like, I can:
- Add a small `Makefile` / PowerShell script to automate venv setup, install and run
- Add a minimal `.env.example` file in `backend/` listing the env vars to copy
- Add a CONTRIBUTING.md with instructions for adding new routes or models

 Tell me which of those you'd like me to add next.