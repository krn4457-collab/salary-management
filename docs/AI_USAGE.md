# AI usage log

Built with agentic AI (OpenCode + Muse Spark). AI accelerated scaffolding;
all design decisions and verification are human-reviewed.

- Prompt 1: "Scaffold FastAPI + SQLite with employee CRUD, pagination, search" → reviewed, added whitelist sort + `salary_usd` index.
- Prompt 2: "Seed 10k deterministic employees across 12 countries" → reviewed distribution weights, verified < 30s.
- Prompt 3: "React table with filters + dashboard" → cut chart dependency, used CSS bars for bundle size.
- Prompt 4: "pytest suite, fast + deterministic" → in-memory SQLite, 12 tests, 0.24s.

Kept: validation bounds, 409 on duplicate email, 404 handling. Rejected: AI-suggested Postgres + Docker default (overkill for assessment).
