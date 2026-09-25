# Pre-flight (fix-loop round 2, Phase 0)

Recorded: 2026-09-25. Lead Dev. No second server was started.

## Listening ports

| Address | Port | PID now | PID at run-2 preflight |
|---------|------|---------|------------------------|
| 127.0.0.1 | 8000 | 46208 (`python`, pyenv 3.12.1) | 20200 |
| 127.0.0.1 | 5173 | 28264 (`node`) | 28264 |

Django's listener PID changed since `reports/evidence/preflight.md`. Vite's PID did not. Health: `GET /api/health` → `{"status":"ok"}`. Frontend `GET /` → 200.

## DB

- Before fingerprint: `C:\Users\dbadmin\Desktop\GitServ\ccna\eval-baseline\fix-loop-r2\db-fingerprint-before.txt`
- SHA-256 of `iterdump()`: `930f0e721ae50453637b2eafc2900a458add7a1447ebdac9c01ff9852f7c0d86`
- Matches `eval-baseline/fix-loop/db-fingerprint-before.txt` and `eval-baseline/run-2/db-fingerprint-before.txt`
- Progress tables are empty (`workbook_attempt` 0, `workbook_labcheckpoint` 0)
- Round-final "after" fingerprint: **not taken**. There is no file from the end of that review.

## Git

- Branch `master` has **no commits**. The whole tree is untracked.
- Baseline commit (B1) is **not done**. It waits on decision D1.
- `backend/db.sqlite3` is gitignored.

## What this round has not started

R1–R6, O1–O10, Q1, and Phase 5 wait until D1–D7 are recorded.
