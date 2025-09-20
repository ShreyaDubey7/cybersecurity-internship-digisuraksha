# Secure Password Strength Checker & Authentication System

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
2.	Initialize DB:
python init_db.py
3.	Run the app:
python app.py
4.	Run tests:
pytest -q
Notes & next steps
•	Replace app.secret_key with a secure random key or configure via environment variable.
•	For production: use HTTPS, a real rate-limiter (Redis), and stronger logging/rotating logs.
•	Optionally connect to HaveIBeenPwned API for breached-password checks. ```

