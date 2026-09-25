# Evidence log — ITMGR

| ID | Time | Type | Locator | Excerpt | Tool |
|----|------|------|---------|---------|------|
| EV-ITMGR-001 | 2026-09-25 | UI | `reports/evidence/ui/start.md` | A0 threat model, export/import/RESET, readiness insufficient_evidence | Browser text |
| EV-ITMGR-002 | 2026-09-25 | UI | `reports/evidence/ui/labs.md` | All 42 labs · 0%; cost/stop panels on GL cards | Browser text |
| EV-ITMGR-003 | 2026-09-25 | UI | `reports/evidence/ui/exam.md` | 429 drills; mock exam disabled "Phase 4 Locked" | Browser text |
| EV-ITMGR-004 | 2026-09-25 | UI | `reports/evidence/ui/coverage.md` | Registry drill-down; bootstrap loading pattern | Browser text |
| EV-ITMGR-005 | 2026-09-25 | file | `reports/evidence/app-map.md` | Four tabs; bootstrap loads summary/progress/readiness | Read |
| EV-ITMGR-006 | 2026-09-25 | API | `reports/evidence/api/progress.json` | attemptCounts total 0; labCheckpoints [] | GET snapshot |
| EV-ITMGR-007 | 2026-09-25 | API | `reports/evidence/api/metrics-readiness.json` | aws/terraform insufficient_evidence; missingPerBucket | GET snapshot |
| EV-ITMGR-008 | 2026-09-25 | API | `reports/evidence/api/coverage.json` | 189 rows; status implemented_unverified on samples | GET snapshot |
| EV-ITMGR-009 | 2026-09-25 | API | `reports/evidence/api/question-q-saa-1-1-k01-mc.json` | GET includes rationale field (no correctAnswerIds) | GET snapshot |
| EV-ITMGR-010 | 2026-09-25 | file | `frontend/src/hooks/useWorkbookBootstrap.ts:71-73` | catch sets error message; failed lab loads skipped | Read |
| EV-ITMGR-011 | 2026-09-25 | file | `frontend/src/App.tsx:60-64` | page-error: Start Django on 127.0.0.1:8000 | Read |
| EV-ITMGR-012 | 2026-09-25 | file | `frontend/src/api/client.ts:31-39` | non-2xx throws Error with JSON error field | Read |
| EV-ITMGR-013 | 2026-09-25 | file | `frontend/src/components/Header.tsx:42-50` | Saved in this browser; steps/labs percent header | Read |
| EV-ITMGR-014 | 2026-09-25 | file | `frontend/src/components/StartHereTab.tsx:85-100` | Readiness cards show missingPerBucket counts | Read |
| EV-ITMGR-015 | 2026-09-25 | file | `reports/evidence/intended-design.md:9-12` | Local-only; no login; SQLite progress | Read |
| EV-ITMGR-016 | 2026-09-25 | file | `reports/evidence/inventory.md` | 16 hourly lab IDs (gl/ul pairs) | Read |
| EV-ITMGR-017 | 2026-09-25 | file | `reports/evidence/content-scan.md` | 721 hits; 380 longest_correct; 21 missing_beforeYouStart | Read |
| EV-ITMGR-018 | 2026-09-25 | file | `reports/evidence/content-scan.json` | mcpStatus pending_recheck 427; UL-01…UL-21 missing_beforeYouStart | Read |
| EV-ITMGR-019 | 2026-09-25 | file | `docs/labs-and-safety.md:REQ-L06` | Cost-risk typing gate on GL-06/07/08/09/14/18/19/21 | Read |
| EV-ITMGR-020 | 2026-09-25 | cross | `reports/06-senior-python-developer.md` | PYTHON-001 Confirmed High rationale leak | Read |
| EV-ITMGR-021 | 2026-09-25 | cross | `reports/05-senior-fullstack-engineer.md` | FULLSTACK-001/002 cross-refs PYTHON-001 | Read |
| EV-ITMGR-022 | 2026-09-25 | file | `backend/workbook/progress.py:15-56` | export_progress schemaVersion attempts checkpoints | Read |
| EV-ITMGR-023 | 2026-09-25 | file | `backend/README.md:28` | localhost CORS 5173/5174; CSRF on POST | Read |
