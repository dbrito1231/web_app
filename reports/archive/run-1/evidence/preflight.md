# Pre-flight (Phase 1)

Recorded: 2026-09-25 (orchestrator, before UI interaction)

## Listening ports

| Address | Port | PID |
|---------|------|-----|
| 127.0.0.1 | 8000 | 20200 |
| 127.0.0.1 | 5173 | 28264 |

## Health

```json
{"status": "ok"}
```

Source: `GET http://127.0.0.1:8000/api/health`

## DB baseline

- Backup: `C:\Users\dbadmin\Desktop\GitServ\ccna\eval-baseline\db.sqlite3.bak`
- Fingerprint file: `eval-baseline/db-fingerprint-before.txt`
- Taken **before** any evaluation UI interaction or POST attempts.

## Lint / scan

- `python scripts\content_lint.py` → PASS (see `lint-output.txt`)
- `python scripts\scan_lab_placeholders.py` → PASS, 41 labs scanned (see `scan-lab-placeholders-output.txt`)
