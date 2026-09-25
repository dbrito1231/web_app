# Workbook Django API (Phase 1)

Local JSON API for the AWS + Terraform workbook. Binds to **127.0.0.1** only.

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Content is read from `../content/`. SQLite database: `backend/db.sqlite3` (gitignored).

## Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py test workbook
```

## CORS

Only browser origins on localhost Vite ports **5173** and **5174** are allowed. POST endpoints require Django CSRF (`X-CSRFToken` after `GET /api/health` sets the cookie).
