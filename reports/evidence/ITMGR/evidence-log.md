# Evidence log — ITMGR

| ID | Time | Type | Locator | Excerpt | Tool |
|----|------|------|---------|---------|------|
| EV-ITMGR-201 | 2026-09-25 | UI | `reports/evidence/ui/start.md` | A0 threat model, export/import/RESET, readiness insufficient_evidence | Browser text |
| EV-ITMGR-202 | 2026-09-25 | UI | `reports/evidence/ui/labs.md` | All 42 labs · 0%; cost/stop panels on GL cards | Browser text |
| EV-ITMGR-203 | 2026-09-25 | UI | `reports/evidence/ui/exam.md` | 429 drills; mock exam disabled "Phase 4 Locked" | Browser text |
| EV-ITMGR-204 | 2026-09-25 | UI | `reports/evidence/ui/coverage.md` | Registry drill-down; bootstrap loading pattern | Browser text |
| EV-ITMGR-205 | 2026-09-25 | file | `reports/evidence/app-map.md` | Four tabs; bootstrap loads summary/progress/readiness | Read |
| EV-ITMGR-206 | 2026-09-25 | API | `reports/evidence/api/progress.json` | attemptCounts total 0; labCheckpoints [] | GET snapshot |
| EV-ITMGR-207 | 2026-09-25 | API | `reports/evidence/api/metrics-readiness.json` | aws/terraform insufficient_evidence; missingPerBucket | GET snapshot |
| EV-ITMGR-208 | 2026-09-25 | API | `reports/evidence/api/coverage.json` | 189 rows; status implemented_unverified on samples | GET snapshot |
| EV-ITMGR-209 | 2026-09-25 | API | `reports/evidence/api/question-q-saa-1-1-k01-mc.json` | GET includes rationale field (no correctAnswerIds) | GET snapshot |
| EV-ITMGR-210 | 2026-09-25 | file | `frontend/src/hooks/useWorkbookBootstrap.ts:71-73` | catch sets error message; failed lab loads skipped | Read |
| EV-ITMGR-211 | 2026-09-25 | file | `frontend/src/App.tsx:60-64` | page-error: Start Django on 127.0.0.1:8000 | Read |
| EV-ITMGR-212 | 2026-09-25 | file | `frontend/src/api/client.ts:31-39` | non-2xx throws Error with JSON error field | Read |
| EV-ITMGR-213 | 2026-09-25 | file | `frontend/src/components/Header.tsx:42-50` | Saved in this browser; steps/labs percent header | Read |
| EV-ITMGR-214 | 2026-09-25 | file | `frontend/src/components/StartHereTab.tsx:85-100` | Readiness cards show missingPerBucket counts | Read |
| EV-ITMGR-215 | 2026-09-25 | file | `reports/evidence/intended-design.md:9-12` | Local-only; no login; SQLite progress | Read |
| EV-ITMGR-216 | 2026-09-25 | file | `reports/evidence/inventory.md` | 16 hourly lab IDs (gl/ul pairs) | Read |
| EV-ITMGR-217 | 2026-09-25 | file | `reports/evidence/content-scan.md` | 721 hits; 380 longest_correct; 21 missing_beforeYouStart | Read |
| EV-ITMGR-218 | 2026-09-25 | file | `reports/evidence/content-scan.json` | pending_recheck 427; UL-01…UL-21 missing_beforeYouStart | Read |
| EV-ITMGR-219 | 2026-09-25 | file | `docs/labs-and-safety.md:REQ-L06` | Cost-risk typing gate on GL-06/07/08/09/14/18/19/21 | Read |
| EV-ITMGR-220 | 2026-09-25 | cross | `reports/06-senior-python-developer.md` | PYTHON-201 Confirmed High rationale leak | Read |
| EV-ITMGR-221 | 2026-09-25 | cross | `reports/05-senior-fullstack-engineer.md` | FULLSTACK-201/230 cross-refs PYTHON-201 | Read |
| EV-ITMGR-222 | 2026-09-25 | file | `backend/workbook/progress.py:15-56` | export_progress schemaVersion attempts checkpoints | Read |
| EV-ITMGR-223 | 2026-09-25 | file | `backend/README.md:28` | localhost CORS 5173/5174; CSRF on POST | Read |
| EV-ITMGR-224 | 2026-09-25 | cross | `reports/01-college-it-student.md` | STUDENT-211 Confirmed Forbidden on exam submit | Read |
| EV-ITMGR-225 | 2026-09-25 | cross | `reports/03-senior-aws-solutions-architect.md` | AWS-201–203 Confirmed High lab defects | Read |
| EV-GATE0-001 | 2026-09-25T18:00Z | UI | POST /api/attempts q-a0-mc-001 | 403 CSRF Origin checking failed http://127.0.0.1:5173 | browser click + CDP fetch hook |
| EV-GATE0-002 | 2026-09-25T18:01Z | UI | POST gl-01/checkpoints | 403 same CSRF origin failure | browser click GL-01 step |
