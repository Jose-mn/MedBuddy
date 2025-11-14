# Contributing to MedBuddy

Thank you for your interest in contributing! This file covers how to set up a local development environment, coding conventions, and how to add new routes or models.

## Local dev workflow (Windows)

1. Clone the repository and open PowerShell in the repo root.
2. Backend development:

```powershell
cd d:\Medbuddy\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file based on `backend/.env.example` and fill in the test Stripe keys and DB details.
4. Create the MySQL database (e.g., `medbuddy_db`) and run `python init_db.py` to create tables.
5. Start the backend server: `uvicorn main:app --reload`.

## Code style & tests
- Follow standard Python practices (PEP8). Use meaningful variable names and keep functions small.
- If adding new routes or models, include small unit tests where practical.

## Adding a route
1. Create a new file in `backend/routes/` (or add to an existing router).
2. Use `APIRouter` and include your router in `main.py`.
3. Add pydantic request/response schemas to `backend/schemas.py`.
4. Register the route in `main.py` (use appropriate prefix).

## Database migrations
- This project currently uses `init_db.py` (development convenience). For production or collaborative development, add Alembic and migration scripts.

## Submitting a PR
- Fork the repo, create a feature branch, commit changes with clear messages, and open a pull request describing the change.
- Include steps to reproduce and any API changes in the PR description.

Thanks for helping improve MedBuddy!