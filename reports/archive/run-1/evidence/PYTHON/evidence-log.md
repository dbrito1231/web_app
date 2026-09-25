# Evidence log — PYTHON

| ID | Time | Type | Locator | Excerpt | Tool |
|----|------|------|---------|---------|------|
| EV-PYTHON-001 | 2026-09-25 | API | `reports/evidence/api/question-q-saa-1-1-k01-mc.json` | GET body includes `"rationale": "Option A aligns…"` while no `correctAnswerIds` | Saved curl response |
| EV-PYTHON-002 | 2026-09-25 | file | `backend/workbook/content_loader.py:45-48` | `public_question`: `payload.pop("correctAnswerIds", None)` only; rationale retained | Read |
| EV-PYTHON-003 | 2026-09-25 | command | `python manage.py test workbook` | 8 tests OK (scoring, readiness default, import schema, reset confirm, API hide key, attempt rationale, lab reveal) | Django test (user-confirmed) |
| EV-PYTHON-004 | 2026-09-25 | file | `backend/workbook/scoring.py:4-7` | `return selected == correct_ids` — all-or-nothing, order-independent | Read |
| EV-PYTHON-005 | 2026-09-25 | file | `backend/config/settings.py:10-14,35-44` | `SECRET_KEY` insecure string; `DEBUG=True`; middleware stack incl. CSRF | Read |
| EV-PYTHON-006 | 2026-09-25 | file | `backend/workbook/views.py:54-223` | `@require_GET` on reads; `@csrf_protect` + `@require_POST` on attempts, checkpoints, export, import, reset; `@ensure_csrf_cookie` on health | Read |
| EV-PYTHON-007 | 2026-09-25 | file | `backend/workbook/tests/test_scoring_and_api.py:66-70` | `test_question_hides_answer_key` asserts missing `correctAnswerIds` only | Read |
| EV-PYTHON-008 | 2026-09-25 | file | `backend/workbook/readiness.py:104-221`; test line 25-28 | Empty objectives map → both tracks `insufficient_evidence`; filters `is_first_exam_attempt=True`, `assisted=False` | Read + test |
| EV-PYTHON-009 | 2026-09-25 | file | `backend/workbook/middleware.py:5-43` | CORS allowlist for Vite; `LocalOriginGuardMiddleware` 403 on bad Origin for `/api/` | Read |
| EV-PYTHON-010 | 2026-09-25 | file | `reports/evidence/lint-output.txt` | `questions 429 aws 310 tf 119` … `PASS` | content_lint output |
| EV-PYTHON-011 | 2026-09-25 | file | `reports/evidence/content-scan.json` | `finding_count`: 721 — 380 `heuristic_longest_correct`, 320 `has_cli_or_code_snippet`, 21 `missing_beforeYouStart` | JSON aggregate |
| EV-PYTHON-012 | 2026-09-25 | file | `backend/workbook/views.py:85-132` | `create_attempt` validates mode/list; returns `rationale` after score | Read |
| EV-PYTHON-013 | 2026-09-25 | file | `backend/workbook/progress.py:66-116,136-139` | Import atomic replace; `schemaVersion` must equal 1; 2 MiB cap | Read |
| EV-PYTHON-014 | 2026-09-25 | API | `reports/evidence/api/lesson-unknown.json`, `question-bad.json` | Unknown ids → HTTP 404, empty body in snapshot | Saved curl response |
