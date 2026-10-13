# Requirements — ACME Salary Management (one page)

## Goal
Replace spreadsheet-based salary tracking for 10,000 employees across multiple
countries with a web app that lets one HR Manager browse, update, and answer
pay questions (total payroll, averages by dept/country/level, distribution)
quickly and without errors.

## Users
Single persona for v1: HR Manager (trusted internal user, one role, no
self-service employees, no approval workflow).

## Scope & features (v1)
1. **Employee directory** — paginated table of 10k employees: name, email,
   country, department, job level, base salary, currency, join date. Search by
   name/email, filter by country/department/level, sort by salary/join date.
2. **Employee detail + salary edit** — view one record, update base salary with
   validation (positive, < 1M) and audit timestamp. Single-writer assumption,
   last-write-wins.
3. **Payroll dashboard** — answers "how do we pay people?": headcount, total
   payroll (USD-normalized), avg/median salary, avg by department, avg by
   country, headcount by level, top-10 earners.
4. **Seed + reset** — deterministic script seeds 10,000 realistic employees
   (12 countries, 8 departments, 5 levels) in < 30s; idempotent re-run.
5. **API + docs** — REST JSON API with OpenAPI/Swagger; frontend consumes only
   this API (no direct DB access).

Non-functional: p95 list response < 200ms on SQLite with indexes; tests fast
and deterministic (in-memory DB); runs locally with 2 commands; no secrets.

## Deliberately out of scope
- **Auth/RBAC, SSO** — single trusted HR user for assessment; adding login
  adds noise without product signal. Noted as next step.
- **Multi-currency payroll execution / tax / payslips** — we store currency +
  USD-normalized figure for comparison only; real payroll compliance is a
  separate domain.
- **Salary history / audit trail / approvals** — only `updated_at` is kept;
  full history table is the obvious v2.
- **Bulk CSV import/export** — spreadsheets are the problem, not the
  interface; export-CSV (one button) is the only v2 concession planned.
- **i18n, mobile app, notifications** — desktop-first HR tool.

## Reasoning
Optimize for correctness, clarity, and demo-ability over completeness. A small,
well-tested CRUD + analytics surface proves engineering judgment; every
excluded item is a known, separable v2 slice that would bloat v1 without
changing the core HR workflow.
