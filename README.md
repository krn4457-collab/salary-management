# ACME Salary Management

Web-based salary management for 10,000 employees across multiple countries.
Replaces spreadsheet-based HR workflow.

**Stack:** FastAPI (Python) + SQLite · React (Vite) + plain CSS

## Quick start

Backend:

```bash
cd backend
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -r requirements.txt
python scripts/seed.py            # seeds 10,000 employees into salary.db
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

API docs: http://localhost:8000/docs

## Repo layout

```
docs/         requirements, architecture, AI usage log
backend/      FastAPI app, SQLite, seed script, pytest suite
frontend/     React Vite HR UI
```

See `docs/REQUIREMENTS.md` for scope and out-of-scope decisions.
