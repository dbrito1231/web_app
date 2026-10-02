# Final sitting item 9 — checks run in the cloud session (2026-10-02)

The user chose option 2: run the Django tests and the build in the cloud, plus a browser smoke test against a throwaway database. This was a one-off exception to the HANDOFF rule "No servers, no Playwright". The DB fingerprint stays local, because it checks the user's own `backend/db.sqlite3`, which is not in git.

| Check | How | Result |
|---|---|---|
| `python manage.py test workbook` | Python 3.12 venv (Django 6.1.1 failed to install on the 3.11 default), `pip install -r requirements.txt` | **Ran 91 tests, OK** |
| `npm run build` | `npm ci`, then `tsc -b && vite build` | **Built OK** (224 kB JS, 23 kB CSS) |
| Browser smoke test | A fresh `db.sqlite3` from `migrate`; Django on 127.0.0.1:8000; `vite preview` on 127.0.0.1:5173; Playwright with the pre-installed Chromium (script: `smoke.cjs`) | **16 pass, 0 fail, 0 page errors** |
| DB fingerprint | — | **Local only** (user's machine) |

Smoke test detail:
- **Grading:** 10 questions across 3.1 to tf-g8 were answered through the UI with their keys, and all were graded Correct. They were 3-1 k01-mc, 3-3 k01-mr, 3-5 k07-mr and s04-mc (both edited this sitting), 4-2 k01-mc, 4-4 k05-mc, tf 1a-mr and 4a-mc (stems edited this sitting), 7b-mc2 and 8b-mc (edited after the Copilot review). A wrong answer on 8c-mc2 was graded Incorrect.
- **Lesson content:** the API serves the new lesson text: 3.5 "one of two engines" with no "Glue for Ray", 4.4 "ECMP enabled", and 3.3 "ReplicaLag". Start here renders lesson tf-g8.
- **Progress:** progress recorded the 11 attempts.

Cleanup: both servers were stopped and the throwaway `db.sqlite3` was deleted. Nothing from the run is committed except this report and the script.
