# AI Lead Qualification & Outreach Agent

Hackathon project for the Nebius x NVIDIA Global AI Hackathon.

## Purpose

Turn raw lead data into qualified, prioritized, human-approved outreach actions.

Core loop:

**Import → Qualify → Score → Prioritize → Recommend → Draft → Approve → Execute → Verify → Report**

## Current status

- Product scope: locked
- PRD: locked
- Technical specification: locked v0.1
- M2 backend lead engine: implemented
- AI qualification, outreach, approvals, frontend and deployment: not implemented
- Deployment: not started

## Local setup

Python 3.10 or newer is required.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cp .env.example .env
cd backend
../.venv/bin/uvicorn app.main:app --reload
```

The API initializes the SQLite schema on startup. By default the database is
`backend/app.db`; set `DATABASE_URL` in `.env` to select another SQLAlchemy URL.
Nebius settings are optional until the AI integration milestone and are never
sent to the frontend.

## M2 API

- `GET /health`
- `POST /api/leads/import` with a multipart `file` containing UTF-8 CSV
- `GET /api/leads` with optional `q`, `company`, `industry`, `sort_by`, `sort_order`, `limit` and `offset`
- `POST /api/leads`, `GET /api/leads/{id}`, `PATCH /api/leads/{id}`, `DELETE /api/leads/{id}`
- `POST /api/leads/{id}/score` with five integer factor values from 0 to 100

CSV headers use the lead field names (`name`, `company`, `role`, `email`,
`website`, `industry`, `company_size`, `source`, `notes`). A complete file is
validated before any rows are persisted. Scoring is deterministic and uses the
weights and tiers in `docs/technical-spec.md`.

Run backend tests from the repository root:

```bash
.venv/bin/python -m pip install -r backend/requirements-dev.txt
cd backend
../.venv/bin/python -m unittest discover -s tests -v
```

See `docs/` for the product and engineering contracts.
