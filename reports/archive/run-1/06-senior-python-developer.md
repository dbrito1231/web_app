# Senior Python Developer Evaluation

## Evaluation Scope

- Backend modules: `backend/workbook/{views,scoring,progress,readiness,content_loader,middleware}.py`, `backend/config/settings.py`
- Tests: `backend/workbook/tests/test_scoring_and_api.py` (8 tests, all passed per EV-PYTHON-003)
- API GET samples: `reports/evidence/api/` (health, content-summary, coverage, progress, readiness, export, lesson/question/lab samples, unknown-ID errors)
- Content gates: `scripts/content_lint.py` output (`reports/evidence/lint-output.txt`) vs orchestrator content scan (`reports/evidence/content-scan.json`, `content-scan.md`)

## Finding template and confidence labels

Per evaluation plan §12, every finding uses this block:

- **Severity:** Critical / High / Medium / Low / Informational
- **Category:** one or more tags (`api`, `backend-bug`, `security-local`, `maintainability`, …)
- **Location:** file and symbol (prefer `file:function:line`)
- **Evidence:** EV-PYTHON-### row(s)
- **Description:** what the code does vs what product expects
- **Impact:** learner or product effect
- **Reproduction / Validation:** curl, test name, or code path
- **Recommended Improvement:** minimal fix or document-only action
- **Confidence:** Confirmed / Likely / Needs Verification / Subjective Observation
- **Related:** (optional) cross-agent finding IDs

Section placement: only **Confirmed** findings under **Confirmed Issues**; **Likely** under **Probable Concerns**; **Needs Verification** under **Items Requiring Verification**; **Subjective Observation** under **Subjective Observations** or non-defect notes.

## Backend mechanisms (review notes)

### HTTP method guards (`views.py`)

| Route | Decorators | Mutations |
|-------|------------|-----------|
| `/api/health` | `@ensure_csrf_cookie`, `@require_GET` | Sets CSRF cookie for SPA |
| `/api/content/summary`, `/api/coverage`, `/api/progress`, `/api/metrics/readiness` | `@require_GET` | Read-only |
| `/api/lessons/<id>`, `/api/questions/<id>`, `/api/labs/<id>` | `@require_GET` | Read-only; lab `?reveal=1` gates `solution` via `public_lab` |
| `/api/attempts`, `/api/labs/<id>/checkpoints`, `/api/export`, `/api/import`, `/api/reset` | `@csrf_protect`, `@require_POST` | State-changing |

Wrong methods receive Django **405** (not exercised in unit tests; standard `require_http_methods` behavior). Unknown content IDs return **404** with `{"error": "… not found"}` (EV-PYTHON-014).

### CSRF and CORS

- **Global:** `CsrfViewMiddleware` in `settings.MIDDLEWARE` (EV-PYTHON-005).
- **POST endpoints:** `@csrf_protect` on attempts, lab checkpoints, export, import, reset (EV-PYTHON-006).
- **Health:** `@ensure_csrf_cookie` so the Vite app can read `csrftoken` before POST (matches frontend `ensureSession()` pattern noted by Full-Stack agent).
- **Tests:** `Client(enforce_csrf_checks=False)` — CSRF behavior is not regression-tested (EV-PYTHON-003).
- **CORS:** `LocalhostCorsMiddleware` allows credentialed requests from Vite origins only; `LocalOriginGuardMiddleware` returns **403** for non-allowlisted `Origin` on `/api/*` (EV-PYTHON-009). Appropriate for localhost-only threat model.

### Question sanitization and attempt feedback

- `public_question` removes only `correctAnswerIds`; **stem, choices, and full `rationale` remain on GET** (EV-PYTHON-001, EV-PYTHON-002).
- `POST /api/attempts` validates `questionId`, `selectedIds` (must be a list), and `mode` ∈ `{practice, exam}`; scores server-side; returns `correct`, `rationale`, `objectiveIds` (EV-PYTHON-012).
- `is_first_exam_attempt` is set only when `mode == exam`, `assisted == false`, and no prior non-assisted exam attempt exists for that `question_id`.

### Scoring (`scoring.py`) — MC and MR

- Single function: **all-or-nothing set equality** between `selected_ids` and `correctAnswerIds` (EV-PYTHON-004).
- **Order independent** (sets). **Partial MR selections fail** (test `test_mr_all_or_nothing_partial_wrong`). **Extra selections fail** (superset ≠ correct set).
- **Not validated:** `selectedIds` membership in `choices`, duplicate entries in `selectedIds`, or `selectCount` vs selection length — garbage IDs can still produce a boolean via set compare (PYTHON-005).

### Progress import / reset (`progress.py`)

- Import: max **2 MiB**, JSON parse errors → `ValueError`; **only `schemaVersion == 1`** accepted (future or past versions rejected — test `test_import_rejects_future_schema`).
- Import **replaces** all progress tables inside `@transaction.atomic` (destructive merge).
- Reset requires JSON body `{"confirm": "RESET"}` (test `test_reset_requires_confirm_token`).

### Readiness (`readiness.py`) — edge cases

- Input attempts: `mode=exam`, `assisted=False`, `is_first_exam_attempt=True` only.
- **Default empty DB:** both tracks return `status: insufficient_evidence` (test `test_insufficient_evidence_by_default`, EV-PYTHON-008).
- **Thresholds:** AWS — ≥40 first attempts and ≥5 per domain `d1`–`d4`; Terraform — ≥30 attempts and ≥2 per group 1–8.
- **Unmapped objectives:** attempts still count toward `firstAttemptCount` but not toward domain/group buckets (`bucket is None`); can trigger `missingPerBucket` while total count looks high.
- **Track assignment:** `_attempt_track` uses objective id prefixes (`SAA-`, `tf.`), else `question_id.startswith("q-t")` → terraform, else **defaults to aws**.
- **Weighted accuracy:** domains with zero attempts are dropped from weight normalization; if no buckets have attempts, weighted accuracy is **0.0** (no division by zero).
- **Recent accuracy (14 days):** if fewer than 10 recent items, formula drops the 10% recent term and documents fold-in via `components.note`.
- **Objective coverage:** numerator is distinct objectives touched by filtered attempts; denominator fixed at 189 (AWS) or 37 (Terraform) — not weighted by registry completeness.

### Local-only settings rating (`settings.py`)

| Setting | Value | Local-only rating |
|---------|--------|-------------------|
| `DEBUG` | `True` | **Acceptable** for dev workbook; would expose stack traces if host binding ever widened |
| `SECRET_KEY` | hard-coded insecure string | **Acceptable** on loopback with no multi-user auth; **blocker** if deployed |
| `ALLOWED_HOSTS` | `127.0.0.1`, `localhost`, `testserver` | **Good** alignment with intended design |
| SQLite | `backend/db.sqlite3` | **By design** single-user store |

Overall: **appropriate for stated local-only product** (Subjective Observation PYTHON-006). Not a defect under `intended-design.md`.

### `content_lint.py` vs content-scan heuristics

| Aspect | `scripts/content_lint.py` (gate) | Content scan (triage, EV-PYTHON-011) |
|--------|----------------------------------|--------------------------------------|
| Purpose | CI-style **PASS/FAIL** (`lint-output.txt` → PASS) | **Signal only**; 721 hits on 429 questions |
| Question counts | Floors: AWS ≥210, TF ≥111; per-module ≥20 (except A0) | No count floors |
| Structural checks | `type` mc/mr, rationale required, objectives, MR `selectCount`, AKIA regex | `selectCount` vs correct count, stem wording, choice integrity, duplicates, template stems, rationale quality, citation/`mcpStatus` |
| Answer leakage | Not checked | **380×** `heuristic_longest_correct` |
| CLI/code in stems | Not checked | **320×** `has_cli_or_code_snippet` |
| Labs | Guided ≥15 steps, teardown fields, unguided criteria | Steps, backticks, commands extract, `beforeYouStart`, cost, pairId, variable order — **21×** `missing_beforeYouStart` |
| Registry | 189 ids, knowledge vs skill ref rules | Full bullet coverage, mock exam weights |
| Copy | Banned “pass probability” phrases | (partial overlap via scan text rules) |
| Lessons / exercises | Lessons loaded; exercises via banned copy scan | `drillIds` resolve, rubric sums, curriculum order |

**Conclusion:** Lint proves **minimum corpus shape**; scan finds **quality and leakage patterns** lint does not cover. Scan hits are not defects until human review (per plan §5.4). Backend does not run either script at runtime.

## Confirmed Issues

### PYTHON-001 — Question GET exposes rationales before attempt

- **Severity:** High
- **Category:** api, security-local
- **Location:** `content_loader.public_question`, `views.question_detail`
- **Evidence:** EV-PYTHON-001, EV-PYTHON-002, EV-PYTHON-012
- **Description:** `GET /api/questions/<id>` returns full `rationale` while omitting only `correctAnswerIds`. `public_question` is not symmetric with exam integrity expectations.
- **Impact:** Any client (browser DevTools, script on localhost) can prefetch explanations and defeat exam-mode practice integrity; amplifies Full-Stack N+1 fetch of all question payloads.
- **Reproduction / Validation:** `reports/evidence/api/question-q-saa-1-1-k01-mc.json` — body includes `"rationale": "Option A aligns…"`. Unit test asserts `correctAnswerIds` absent but **does not** assert rationale absent (EV-PYTHON-007).
- **Recommended Improvement:** Strip `rationale` (and any answer-key-adjacent fields) in `public_question`; keep rationale on `POST /api/attempts` only.
- **Confidence:** Confirmed
- **Related:** FULLSTACK-001 (XF-001)

### PYTHON-003 — No regression test for rationale leak

- **Severity:** Medium
- **Category:** maintainability, api
- **Location:** `backend/workbook/tests/test_scoring_and_api.py` (`test_question_hides_answer_key`)
- **Evidence:** EV-PYTHON-007, EV-PYTHON-003
- **Description:** Test checks `correctAnswerIds` not in GET payload but not `rationale`, so PYTHON-001 can regress silently.
- **Impact:** Drill integrity bugs ship despite green `manage.py test workbook`.
- **Reproduction / Validation:** Read test at lines 66–70; compare with EV-PYTHON-001.
- **Recommended Improvement:** Extend test: `assertNotIn("rationale", data)` for public question GET.
- **Confidence:** Confirmed
- **Related:** PYTHON-001

## Probable Concerns

### PYTHON-002 — MR scoring is strictly all-or-nothing (by design)

- **Severity:** Informational
- **Category:** backend-bug, consistency
- **Location:** `scoring.score_question`
- **Evidence:** EV-PYTHON-004, EV-PYTHON-003 (`test_mr_all_or_nothing_partial_wrong`)
- **Description:** Partial credit is impossible; matches SAA-style “select all that apply” grading when exam uses full-credit-only scoring.
- **Impact:** None for current product spec; document in API/architecture if stakeholders expect partial MR credit.
- **Reproduction / Validation:** Unit tests for MC and MR set equality.
- **Recommended Improvement:** Document in `docs/architecture.md`; no code change unless product requires partial credit.
- **Confidence:** Likely

### PYTHON-004 — Scoring does not validate `selectedIds` against choices

- **Severity:** Low
- **Category:** api, backend-bug
- **Location:** `views.create_attempt`, `scoring.score_question`
- **Evidence:** EV-PYTHON-004, EV-PYTHON-012
- **Description:** Unknown choice ids in `selectedIds` are scored purely by set equality to `correctAnswerIds`; duplicates in list collapse via `set()`. No check against `selectCount` or choice ids.
- **Impact:** Malformed client payloads get a score without 400 validation; unlikely from first-party UI.
- **Reproduction / Validation:** Code review; POST with `selectedIds: ["z"]` for a known question (not automated).
- **Recommended Improvement:** Optional 400 if any selected id ∉ choice ids or `len(selected_ids) != len(set(selected_ids))` when strict mode desired.
- **Confidence:** Likely

### PYTHON-005 — Corrupt content JSON may surface as 500

- **Severity:** Low
- **Category:** api, maintainability
- **Location:** `content_loader._read_json`, GET detail views
- **Evidence:** EV-PYTHON-002, EV-PYTHON-014
- **Description:** `json.load` failures are not caught in views; only missing files become 404 via `ContentNotFoundError`.
- **Impact:** Single bad file breaks lesson/question/lab GET with server error instead of 404/422.
- **Reproduction / Validation:** Needs Verification unless a corrupt file exists in repo (lint loads all JSON at CI — mitigates).
- **Recommended Improvement:** Catch `JSONDecodeError` in loader and map to 404 or 500 with clear error body.
- **Confidence:** Likely

## Items Requiring Verification

No findings in this category.

## Subjective Observations

### PYTHON-006 — DEBUG and SECRET_KEY fit local-only scope

- **Severity:** Informational
- **Category:** security-local
- **Location:** `backend/config/settings.py`
- **Evidence:** EV-PYTHON-005
- **Description:** Insecure defaults are intentional for a non-hosted workbook; combined with origin guard and loopback hosts, risk is contained to the learner machine.
- **Impact:** Would become High if the app is bound to `0.0.0.0` or placed behind a public URL without hardening.
- **Reproduction / Validation:** Static review against `intended-design.md`.
- **Recommended Improvement:** If packaging for wider use, env-driven `SECRET_KEY`, `DEBUG=False`, and deployment checklist.
- **Confidence:** Subjective Observation

## Strengths

- Clear split: `public_question` / `public_lab(reveal=…)` vs full content on disk; lab solution gating matches product rules.
- Readiness pipeline avoids divide-by-zero in weights; explicit `insufficient_evidence` path with `missingPerBucket` detail.
- Progress import size cap and schema version gate reduce accidental blob imports.
- Middleware enforces localhost browser origins on API routes — coherent with CSRF cookie model.
- Small, readable view layer with consistent `_json_error` helper and typed validation on attempt mode and lab checkpoint status.

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| PYTHON-001 | Confirmed High | XF-001 |
| PYTHON-002 | Informational (by design) | — |
| PYTHON-003 | Confirmed Medium | XF-001 |
| PYTHON-004 | Likely Low | — |
| PYTHON-005 | Likely Low | — |
| PYTHON-006 | Subjective (acceptable local) | — |
