# Architecture

```
React (Vite)  →  REST JSON  →  FastAPI  →  SQLite (SQLAlchemy)
                     /api/employees (CRUD, search/filter/sort/page)
                     /api/stats/* (summary, by-dept/country/level, top)
```

- **Backend** (`backend/app/`): `models.py` (Employee + FX table), `schemas.py`
  (validation: salary > 0, < 1M), `routers/employees.py` (indexed queries,
  `ilike` search, whitelist sort), `routers/stats.py` (GROUP BY aggregations).
  `salary_usd` is precomputed on write so analytics sort/filter on one indexed
  column instead of converting per row.
- **DB**: SQLite with indexes on `country, department, level, salary_usd,
  join_date, email`. p95 list < 200ms for 10k rows; single-file, zero-ops.
- **Frontend** (`frontend/src/`): `api.js` fetch client, `App.jsx` (dashboard +
  table + edit modal in one screen for HR flow). No chart lib — CSS bars keep
  bundle ~226KB.
- **Seed** (`backend/scripts/seed.py`): deterministic (`seed(42)`), weighted
  countries/depts/levels, bulk insert 1k/batch, idempotent (wipes + reseeds).

## Trade-offs
SQLite over Postgres: fine for 10k rows + single writer; migration path is
SQLAlchemy URL swap. No auth: trusted-HR v1, add JWT + roles next. No salary
history table: `updated_at` only; history is the first v2 slice.
