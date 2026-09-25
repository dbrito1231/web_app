# Evidence log — PYTHON (Phase 3 strict eval)

| ID | Time | Type | Locator | Excerpt | Tool |
|----|------|------|---------|---------|------|
| EV-GATE0-001 | 2026-09-25T18:00Z | UI | POST `/api/attempts` `q-a0-mc-001` | 403 — `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins` | browser + CDP fetch hook |
| EV-GATE0-002 | 2026-09-25T18:01Z | UI | POST `/api/labs/gl-01/checkpoints` | 403 — same CSRF origin failure as attempts | browser GL-01 checkpoint click |
| EV-PYTHON-201 | 2026-09-25 Phase 3 | command | `GET /api/questions/q-saa-1-1-k01-mc` | `Has rationale: True`; `Has correctAnswerIds: False` | Django `Client` (see EV-PYTHON-217) |
| EV-PYTHON-202 | 2026-09-25 Phase 3 | file | `backend/workbook/content_loader.py:45-48` | `public_question` pops `correctAnswerIds` only; rationale retained | Read |
| EV-PYTHON-203 | 2026-09-25 Phase 3 | command | `reports/evidence/PYTHON/test-workbook-output.txt` | `Ran 8 tests` … `OK`; `enforce_csrf_checks=False` in test client | `python manage.py test workbook` |
| EV-PYTHON-204 | 2026-09-25 Phase 3 | file | `backend/workbook/scoring.py:4-7` | `return selected == correct_ids` — all-or-nothing set equality | Read |
| EV-PYTHON-205 | 2026-09-25 Phase 3 | file | `backend/config/settings.py:18-23,35-44` | `CORS_ALLOWED_ORIGINS` lists Vite; **no** `CSRF_TRUSTED_ORIGINS`; `CsrfViewMiddleware` enabled | Read |
| EV-PYTHON-206 | 2026-09-25 Phase 3 | file | `backend/workbook/views.py:54-224` | Eight `@require_GET` views; five `@csrf_protect` + `@require_POST` mutators | Read |
| EV-PYTHON-207 | 2026-09-25 Phase 3 | file | `backend/workbook/tests/test_scoring_and_api.py:66-70` | `test_question_hides_answer_key` — `assertNotIn("correctAnswerIds")` only | Read |
| EV-PYTHON-208 | 2026-09-25 Phase 3 | file | `backend/workbook/readiness.py:182-221`; test L25-28 | Filters exam / non-assisted / first-attempt; empty DB → `insufficient_evidence` both tracks | Read + test |
| EV-PYTHON-209 | 2026-09-25 Phase 3 | file | `backend/workbook/middleware.py:5-43` | Vite CORS allowlist; non-local `Origin` on `/api/` → 403 `Origin not allowed` | Read |
| EV-PYTHON-210 | 2026-09-25 Phase 3 | command | `reports/evidence/lint-output-run3.txt` | `questions 429 aws 310 tf 119` … `PASS` | `python scripts/content_lint.py` |
| EV-PYTHON-211 | 2026-09-25 Phase 3 | file | `reports/evidence/content-scan.json` | `finding_count` 721 — 380 `heuristic_longest_correct`, 320 `has_cli_or_code_snippet`, 21 `missing_beforeYouStart` | JSON aggregate (script) |
| EV-PYTHON-212 | 2026-09-25 Phase 3 | file | `backend/workbook/views.py:85-132` | `create_attempt` validates mode/list; POST returns `rationale` after score | Read |
| EV-PYTHON-213 | 2026-09-25 Phase 3 | file | `backend/workbook/progress.py` | Import 2 MiB cap, `schemaVersion == 1`, atomic replace | Read |
| EV-PYTHON-214 | 2026-09-25 Phase 3 | API | `reports/evidence/api/lesson-unknown.json` | Unknown lesson id → HTTP 404 | Saved curl snapshot |
| EV-PYTHON-215 | 2026-09-25 Phase 3 | command | POST `/api/attempts` + `/api/labs/gl-01/checkpoints` | Status **403** with `Origin checking failed - http://127.0.0.1:5173` (matches Gate 0) | Django `Client(enforce_csrf_checks=True)` + `HTTP_ORIGIN` |
| EV-PYTHON-216 | 2026-09-25 Phase 3 | command | All read routes in `views.py` | POST to each GET-only path → **405**; GET to each POST-only path → **405** (no Origin header) | Django `Client(enforce_csrf_checks=False)` |
| EV-PYTHON-217 | 2026-09-25 Phase 3 | command | `GET /api/questions/q-saa-1-1-k01-mc` | Status 200; rationale present in JSON body | Django `Client` |
| EV-PYTHON-218 | 2026-09-25 Phase 3 | cross | `reports/evidence/gate0-save-failure.md` | Documents missing `CSRF_TRUSTED_ORIGINS` vs allowed CORS origin | Read (Gate 0 write-up) |
