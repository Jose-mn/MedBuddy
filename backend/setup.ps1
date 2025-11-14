<#
Simple Windows PowerShell setup script for MedBuddy backend (development only)
- Creates virtual environment (if missing)
- Activates venv for the current session
- Installs requirements
- Copies .env.example -> .env if .env missing (will not overwrite)
- Runs DB init script (init_db.py) - ensure your MySQL DB exists and credentials in database.py are correct
- Starts uvicorn

Usage: run from `d:\Medbuddy\backend` in PowerShell
PS> .\setup.ps1
#>

Set-StrictMode -Version Latest

$here = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $here

# 1) Create venv if it doesn't exist
if (-Not (Test-Path -Path .\venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
} else {
    Write-Host "Virtual environment already exists."
}

# 2) Activate venv in this session
Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# 3) Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4) Copy .env.example -> .env if missing
if (-Not (Test-Path -Path .\.env)) {
    if (Test-Path -Path .\.env.example) {
        Copy-Item .\.env.example .\.env
        Write-Host "Created .env from .env.example. Edit .env to add secrets (Stripe keys, DB connection if needed)."
    } else {
        Write-Host "No .env.example found. Create a .env file in the backend folder with required variables."
    }
} else {
    Write-Host ".env already exists."
}

# 5) Run DB init (developer caution)
Write-Host "Running DB initialization (drops & recreates tables). Ensure DB exists and database.py has correct credentials..."
python init_db.py

# 6) Start backend (uvicorn)
Write-Host "Starting backend (uvicorn). Press Ctrl+C to stop."
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
