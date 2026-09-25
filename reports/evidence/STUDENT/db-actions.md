# DB actions — STUDENT (Phase 3, paper-feedback mode)

**Session:** 2026-09-25 strict eval Phase 3  
**Mode:** Gate 0 Result A (`reports/evidence/gate0-save-failure.md`) — UI saves blocked; drills graded on paper from `content/questions/*.json`.

## Baseline (pre-session)

| Table | Count | Tool |
|-------|------:|------|
| `workbook_attempt` | 0 | `backend/.venv` sqlite3 on `backend/db.sqlite3` |
| `workbook_labcheckpoint` | 0 | same |

## Actions attempted

| # | Time | Action | Endpoint / UI | Expected | Observed |
|---|------|--------|---------------|----------|----------|
| 1 | T+18m | Select answer on `q-a0-mc-001`, click **Check answers** | `POST /api/attempts` from `/exam` workflow | 200 + rationale | **403 Forbidden** (Gate 0: CSRF trusted-origin mismatch) |
| 2 | T+19m–T+95m | Repeat **Check answers** for all **60** drill IDs in `drill-60-ids.txt` | Same | Persist + UI feedback | **403 Forbidden** each attempt (curl POST without session: 403; UI per EV-GATE0-001) |
| 3 | T+25m | Paper lab checkpoint tick (not persisted) | `POST /api/labs/gl-01/checkpoints` | 200 | **403** per Gate 0 EV-GATE0-002 |

## Post-session

| Table | Count | Delta |
|-------|------:|------|
| `workbook_attempt` | 0 | 0 |
| `workbook_labcheckpoint` | 0 | 0 |

## Notes

- `GET /api/progress` after drill batch: `attemptCounts` remain empty (EV-STUDENT-220).
- Normal Chrome at `127.0.0.1:5173` with CSRF cookie may differ — not verified this session (MCP browser unavailable).
