# MedConsult AI

A simple full-stack health assistant aligned with **SDG 3 (Good Health & Well‑Being)**.

Tech stack:
- Backend: FastAPI (Python), SQLAlchemy
- Database: MySQL
- Frontend: HTML, CSS, JavaScript (Tailwind CDN + custom CSS)

API base URL: `http://127.0.0.1:8000`

## Features
- User Sign Up and Login (bcrypt hashed passwords)
- Symptom Checker with keyword-based insights
- Daily Health Tip and rotating motivational quotes
- Responsive, calming health-themed UI with animated gradients

---

## Local Development (no Docker)
1) Create MySQL database:
```
CREATE DATABASE medconsult_db;
```
2) Optionally copy `.env.example` to `.env` and set your values, or rely on defaults in `backend/database.py`.
3) Install Python deps:
```
pip install -r requirements.txt
```
4) Run the API:
```
uvicorn backend.main:app --reload
```
5) Open the frontend:
   - Use a local static server (e.g. VS Code Live Server) and open `frontend/index.html`
   - The frontend calls `http://127.0.0.1:8000`

---

## Docker Setup
This repository includes a `Dockerfile` for the API and a `docker-compose.yml` to run both MySQL and the API.

### 1) Create an `.env` file
Copy `.env.example` to `.env` and adjust values as desired:
```
cp .env.example .env
```

### 2) Start services
```
docker compose up -d --build
```
This will:
- Start `mysql` (with persistent volume `medconsult_mysql`)
- Build and start `api` at `http://127.0.0.1:8000`

The API will auto-create tables in `medconsult_db` on first run.

### 3) Stopping
```
docker compose down
```
To remove volumes too:
```
docker compose down -v
```

---

## Environment Variables
The API uses the following environment variables for DB connectivity:
- `MYSQL_USER` (default: `root`)
- `MYSQL_PASSWORD` (default: `password`)
- `MYSQL_HOST` (default: `127.0.0.1`)
- `MYSQL_PORT` (default: `3306`)
- `MYSQL_DATABASE` (default: `medconsult_db`)

When running via Docker Compose, these are set so the API connects to the `mysql` container by service name.

---

## Project Structure
```
backend/
  main.py
  database.py
  models.py
  schemas.py
  routes/
    auth.py
    symptom_checker.py
    tips.py
frontend/
  index.html
  signup.html
  login.html
  symptom.html
  style.css
  script.js
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

---

## Notes
- Default DB credentials are for quick local testing only. Change for production.
- No tokens/sessions are implemented; login responds with user info for demo purposes.
- Frontend calls are CORS-enabled from common local origins. Adjust in `backend/main.py` if necessary.


