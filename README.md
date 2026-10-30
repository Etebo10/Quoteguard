# QuoteGuard

QuoteGuard is a FastAPI-based quoting intelligence app for estimating quote viability, pricing, and commercial risk.

Visit at: https://quoteguard-1.onrender.com/app

## Features
- Deterministic pricing calculation engine
- Margin and cost-overrun risk detection
- Historical similarity and statistics analysis
- Optional Groq-backed AI assessment when an API key is configured
- Lightweight static web UI for quote entry and reporting

## Tech stack
- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Groq API (optional)

## Local setup
1. Create and activate a virtual environment.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Copy the environment template:
   copy .env.example .env
4. Add a valid Groq key to .env if you want AI analysis enabled:
   GROQ_API_KEY=your_key_here
5. Run the app:
   python -m uvicorn app.main:app --reload
6. Open the web app at:
   http://127.0.0.1:8000/app

## Tests
Run the suite with:
python -m pytest -q

## Notes
The AI layer gracefully falls back to local deterministic analysis when no Groq key is present, so the project remains usable offline.
