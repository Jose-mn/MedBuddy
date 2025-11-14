# Make `routes` a package so imports like `from routes import auth` work
from . import auth, symptom_checker, tips, premium, payments
