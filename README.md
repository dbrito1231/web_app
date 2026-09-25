# AWS Solutions Architect + Terraform Lab Workbook

Local learning app for **SAA-C03** (189 atomic objective bullets from the supplied exam guide) and **Terraform Associate 004**.

## Stack

- Frontend: Vite + React + TypeScript (`frontend/`)
- Backend: Django 6.1.1 on `127.0.0.1:8000` (`backend/`)
- Progress: SQLite `backend/db.sqlite3` (gitignored)
- Specs: `docs/` (markdown)

Agents never call AWS. You run labs in your own terminal. Agent roles (Teacher is read-only; Lead Developer is the only writer) are in `AGENTS.md`.

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173 — four tabs: Labs | Exam drills | Coverage | Start here.

## Tests and lint

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py test workbook

cd ..
python scripts\content_lint.py

cd frontend
npm run build
```

Terraform fixture (no credentials / no apply):

```powershell
cd lab-fixtures\gl-20
terraform fmt -check
terraform init -backend=false
terraform validate
```

## Content floors

- ≥210 AWS MC/MR questions, ≥111 Terraform questions
- 21 guided + 21 unguided labs (≥15 steps / ≥15 criteria)
- 189-row coverage registry in `content/coverage/saa_registry.json`

## Safety

- $10 is a warning, not a stop
- Teardown on every lab; stopping an instance is not teardown
- Hourly labs require typing `I ACCEPT THE COST RISK`
- HCP Terraform hands-on only on a no-charge plan

## MCP note

Phase 6 sample re-check (2026-09-24) used AWS Knowledge MCP and Terraform registry MCP (docs only). Evidence: `docs/citation-recheck.md`. Agents never use AWS API MCP or provision resources. The drill bank remains largely `pending_recheck` until per-item polish.
