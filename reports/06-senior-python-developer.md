# Senior Python Developer Evaluation (Phase 3 strict eval)

**Run:** 2026-09-25 Phase 3 — PYTHON role re-verification (no `archive/run-1` read for this draft).

## Evaluation Scope

- Backend: `backend/workbook/{views,scoring,progress,readiness,content_loader,middleware}.py`, `backend/config/settings.py`
- Tests: `python manage.py test workbook` → **PASS** (8 tests) — `reports/evidence/PYTHON/test-workbook-output.txt`
- Gate 0: `reports/evidence/gate0-save-failure.md`, EV-GATE0-001/002
- API samples: `reports/evidence/api/` (question GET includes rationale)
- Content gates: `scripts/content_lint.py` (`reports/evidence/lint-output-run3.txt` PASS) vs orchestrator scan (`reports/evidence/content-scan.json`, 721 heuristic hits)

## Finding template (nine fields)

- **Severity:** Critical / High / Medium / Low / Informational
- **Category:** tags (`api`, `backend-bug`, `security-local`, `maintainability`, …)
- **Location:** file and symbol
- **Evidence:** EV-PYTHON-### / EV-GATE0-###
- **Description:** behavior vs expectation
- **Impact:** learner or product effect
- **Reproduction / Validation:** command, test, or Gate 0
- **Recommended Improvement:** minimal fix
- **Confidence:** Confirmed / Likely / Needs Verification / Subjective Observation
- **Related:** (optional) cross-agent IDs

**Confirmed** findings appear only when backed by command output or Gate 0 (Phase 3 rule).

## Backend mechanisms (review notes)

### HTTP method guards — all `views.py` endpoints (EV-PYTHON-216)

| View | Route | Allowed | Wrong method (Phase 3) |
|------|-------|---------|-------------------------|
| `health` | `/api/health` | GET | POST → **405** |
| `content_summary_view` | `/api/content/summary` | GET | POST → **405** |
| `coverage_registry` | `/api/coverage` | GET | POST → **405** |
| `progress_view` | `/api/progress` | GET | POST → **405** |
| `readiness_metrics` | `/api/metrics/readiness` | GET | POST → **405** |
| `lesson_detail` | `/api/lessons/<id>` | GET | POST → **405** |
| `question_detail` | `/api/questions/<id>` | GET | POST → **405** |
| `lab_detail` | `/api/labs/<id>` | GET | POST → **405** |
| `create_attempt` | `/api/attempts` | POST | GET → **405** |
| `lab_checkpoint` | `/api/labs/<id>/checkpoints` | POST | GET → **405** |
| `export_view` | `/api/export` | POST | GET → **405** |
| `import_view` | `/api/import` | POST | GET → **405** |
| `reset_view` | `/api/reset` | POST | GET → **405** |

Unknown content IDs still return **404** with `{"error": "… not found"}` (EV-PYTHON-214).

### CSRF and CORS (EV-PYTHON-205, EV-PYTHON-209, EV-PYTHON-215)

- `CsrfViewMiddleware` is active; mutating views use `@csrf_protect` (EV-PYTHON-206).
- `CORS_ALLOWED_ORIGINS` includes `http://127.0.0.1:5173`; **`CSRF_TRUSTED_ORIGINS` is unset** (EV-PYTHON-205, EV-PYTHON-218).
- **Gate 0 + Phase 3 command:** POST `/api/attempts` and POST `/api/labs/gl-01/checkpoints` with `Origin: http://127.0.0.1:5173`, valid CSRF cookie/token → **403** — `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins` (EV-GATE0-001/002, EV-PYTHON-215). This is Django CSRF origin checking, not `LocalOriginGuardMiddleware` (`Origin not allowed`).
- Unit tests use `Client(enforce_csrf_checks=False)` and omit `Origin`, so they stay green while the Vite stack cannot save (EV-PYTHON-203).

### Question sanitization and attempts (EV-PYTHON-201, EV-PYTHON-202, EV-PYTHON-212)

- `public_question` strips only `correctAnswerIds`; **GET still returns full `rationale`** (EV-PYTHON-201, EV-PYTHON-217).
- `POST /api/attempts` scores server-side and returns `correct`, `rationale`, `objectiveIds` after submit (EV-PYTHON-212).

### Scoring (`scoring.py`) — EV-PYTHON-204

- All-or-nothing set equality for MC/MR; partial MR fails (covered by unit tests in EV-PYTHON-203).
- No server-side validation that `selectedIds` ⊆ choice ids or matches `selectCount` (PYTHON-204, Likely).

### Readiness (`readiness.py`) — EV-PYTHON-208

- Uses first non-assisted exam attempts only; empty DB → both tracks `insufficient_evidence` (test in EV-PYTHON-203).

### Middleware — EV-PYTHON-209

- Localhost CORS + API origin guard aligned with single-user dev threat model.

### `content_lint.py` vs content-scan — EV-PYTHON-210, EV-PYTHON-211

| Aspect | `content_lint.py` (gate) | Content scan (triage) |
|--------|--------------------------|------------------------|
| Outcome | **PASS** — 429 questions, floors met | **721** findings on 429 questions (not a fail gate) |
| Answer leakage heuristics | Not checked | 380× `heuristic_longest_correct` |
| CLI/code in stems | Not checked | 320× `has_cli_or_code_snippet` |
| Lab `beforeYouStart` | Partial structural rules | 21× `missing_beforeYouStart` |
| Runtime | CI/manual script | Orchestrator JSON; backend does not run either |

Lint proves **minimum corpus shape**; scan surfaces **quality patterns** lint does not enforce.

## Confirmed Issues

### PYTHON-230 — Missing CSRF_TRUSTED_ORIGINS breaks browser POSTs; tests miss Origin

- **Severity:** Critical
- **Category:** backend-bug, api
- **Location:** `backend/config/settings.py`; `CsrfViewMiddleware`; `test_scoring_and_api.py` (`enforce_csrf_checks=False`)
- **Evidence:** EV-GATE0-001, EV-GATE0-002, EV-PYTHON-205, EV-PYTHON-215, EV-PYTHON-203
- **Description:** Vite sends `Origin: http://127.0.0.1:5173` on POST. Django 6.1 rejects CSRF when that origin is not in `CSRF_TRUSTED_ORIGINS`. Tests POST without Origin and disable CSRF enforcement.
- **Impact:** All mutating learner APIs fail from the shipped dev stack; false confidence from green unit tests.
- **Reproduction / Validation:** Gate 0 save flow; Phase 3 Django client POST with `HTTP_ORIGIN` → 403 (EV-PYTHON-215).
- **Recommended Improvement:** Add `CSRF_TRUSTED_ORIGINS` matching Vite origins; add regression test POST with Origin + CSRF token.
- **Confidence:** Confirmed
- **Related:** FULLSTACK-230, ITMGR-230

### PYTHON-201 — Question GET exposes rationales before attempt

- **Severity:** High
- **Category:** api, security-local
- **Location:** `content_loader.public_question`; `views.question_detail`
- **Evidence:** EV-PYTHON-201, EV-PYTHON-202, EV-PYTHON-217; `reports/evidence/api/question-q-saa-1-1-k01-mc.json`
- **Description:** `GET /api/questions/<id>` returns full `rationale` while omitting only `correctAnswerIds`.
- **Impact:** Clients can prefetch explanations and undermine exam-mode integrity.
- **Reproduction / Validation:** Phase 3 GET `q-saa-1-1-k01-mc` → `Has rationale: True` (EV-PYTHON-217); saved API snapshot.
- **Recommended Improvement:** Strip `rationale` in `public_question`; keep on POST attempt response only.
- **Confidence:** Confirmed
- **Related:** FULLSTACK-201 (XF-201)

### PYTHON-203 — No regression test for rationale leak

- **Severity:** Medium
- **Category:** maintainability, api
- **Location:** `backend/workbook/tests/test_scoring_and_api.py` (`test_question_hides_answer_key`)
- **Evidence:** EV-PYTHON-207, EV-PYTHON-203
- **Description:** Test asserts `correctAnswerIds` absent on GET but not `rationale`, so PYTHON-201 can regress silently.
- **Impact:** Drill integrity bugs ship despite passing `manage.py test workbook`.
- **Reproduction / Validation:** Read test L66–70; contrast EV-PYTHON-217.
- **Recommended Improvement:** `assertNotIn("rationale", data)` on public question GET.
- **Confidence:** Confirmed
- **Related:** PYTHON-201

## Probable Concerns

### PYTHON-202 — MR scoring is strictly all-or-nothing (by design)

- **Severity:** Informational
- **Category:** consistency
- **Location:** `scoring.score_question`
- **Evidence:** EV-PYTHON-204, EV-PYTHON-203
- **Description:** Partial MR credit is impossible; matches full-credit SAA-style MR grading.
- **Impact:** None for current spec unless partial credit is requested.
- **Reproduction / Validation:** `test_mr_all_or_nothing_partial_wrong` in EV-PYTHON-203.
- **Recommended Improvement:** Document in architecture if stakeholders need partial MR.
- **Confidence:** Likely

### PYTHON-204 — Scoring does not validate `selectedIds` against choices

- **Severity:** Low
- **Category:** api, backend-bug
- **Location:** `views.create_attempt`; `scoring.score_question`
- **Evidence:** EV-PYTHON-204, EV-PYTHON-212
- **Description:** Unknown choice ids are scored by set equality only; duplicates collapse via `set()`.
- **Impact:** Malformed payloads get a score without 400; unlikely from first-party UI.
- **Reproduction / Validation:** Code review; no automated negative test.
- **Recommended Improvement:** Optional 400 when ids ∉ choices or selection length violates `selectCount`.
- **Confidence:** Likely

### PYTHON-205 — Corrupt content JSON may surface as 500

- **Severity:** Low
- **Category:** api, maintainability
- **Location:** `content_loader._read_json`; GET detail views
- **Evidence:** EV-PYTHON-202
- **Description:** `json.load` errors are not mapped to 404/422; only missing files raise `ContentNotFoundError`.
- **Impact:** One bad file breaks a GET endpoint with 500.
- **Reproduction / Validation:** Not executed in Phase 3 (no corrupt fixture in repo; lint loads all JSON — mitigates).
- **Recommended Improvement:** Catch decode errors in loader; return structured error.
- **Confidence:** Likely

## Subjective Observations

### PYTHON-206 — DEBUG and SECRET_KEY fit local-only scope

- **Severity:** Informational
- **Category:** security-local
- **Location:** `backend/config/settings.py`
- **Evidence:** EV-PYTHON-205
- **Description:** Insecure defaults are acceptable for loopback-only workbook per intended design.
- **Impact:** Becomes High if bound publicly without hardening.
- **Reproduction / Validation:** Static review vs `reports/evidence/intended-design.md`.
- **Recommended Improvement:** Env-driven secrets if packaging beyond localhost.
- **Confidence:** Subjective Observation

## Strengths

- Consistent `@require_GET` / `@require_POST` split across all thirteen view functions (EV-PYTHON-216).
- Lab `public_lab(reveal=…)` gates solutions; readiness avoids divide-by-zero in weights.
- Progress import schema version and size cap; localhost origin guard complements CSRF cookie model.

## Phase 3 summary

| Check | Result |
|-------|--------|
| `python manage.py test workbook` | **PASS** (8/8) |
| Gate 0 CSRF save failure | **Confirmed** |
| Rationale on question GET | **Confirmed** |
| GET-only POST → 405 (8 routes) | **Confirmed** |
| `content_lint.py` | **PASS** |
| PYTHON-2xx finding blocks | **7** (3 Confirmed issues, 3 Probable, 1 Subjective) |

## Post-discussion status

Run-2 strict Phase 5–6 (see `reports/discussion/round-b/PYTHON.md`, `revalidation.md`).

| Finding ID | Pre-discussion confidence | Final status | Notes |
|------------|---------------------------|--------------|-------|
| PYTHON-230 | Confirmed | **Confirmed Critical** | Gate 0 CSRF; tests miss Origin |
| PYTHON-201 | Confirmed | **Confirmed High** (XF-201) | GET rationale |
| PYTHON-203 | Confirmed | **Confirmed Medium** | Test gap; ship with XF-201 fix |
| PYTHON-202 | Likely | **Informational** (by design) | MR all-or-nothing |
| PYTHON-204 | Likely | **Likely Low** | selectedIds validation |
| PYTHON-205 | Likely | **Likely Low** | Corrupt JSON → 500 |
| PYTHON-206 | Subjective Observation | **Subjective Observation** | Localhost DEBUG scope |
