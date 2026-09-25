# Pre-flight (run-2, Phase 0)

Recorded: 2026-09-25 (orchestrator, before run-2 UI interaction)

## Listening ports

| Address | Port | PID |
|---------|------|-----|
| 127.0.0.1 | 8000 | 20200 |
| 127.0.0.1 | 5173 | 28264 |

## Health

```json
{"status":"ok"}
```

Source: `Invoke-RestMethod http://127.0.0.1:8000/api/health`

## DB baseline (run-2)

- Reused backup: `C:\Users\dbadmin\Desktop\GitServ\ccna\eval-baseline\db.sqlite3.bak`
- Fingerprint: `eval-baseline/run-2/db-fingerprint-before.txt`
- Live `backend/db.sqlite3` iterdump SHA-256 matches backup before Gate 0 clicks.

## MCP

- Terraform registry MCP: `get_latest_provider_version(hashicorp, aws)` → **6.66.0**
- AWS Knowledge MCP: not enabled (WebFetch fallback per plan §11).

## Lint / scan

- `python scripts\content_lint.py` → see `lint-output.txt`
- `python scripts\scan_lab_placeholders.py` → see `scan-lab-placeholders-output.txt`

## Run-1 archive

Previous deliverables moved to `reports/archive/run-1/` (not deleted).
