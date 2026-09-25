# Phase 1 validation (2026-09-25)

## ISS-001 / WP1 — CSRF saves

- **Valid.** `backend/config/settings.py` had `CORS_ALLOWED_ORIGINS` and no `CSRF_TRUSTED_ORIGINS`. Gate 0 recorded 403 `Origin checking failed` for `http://127.0.0.1:5173`.
- **Fix applied:** `CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)`. Test `test_post_with_vite_origin_and_csrf` POSTs attempts and a GL-01 checkpoint with `HTTP_ORIGIN` and a CSRF token. `client.ts` maps a non-JSON 403 to a plain sentence.

## ISS-003 / WP2 — rationale on GET

- **Valid.** `public_question` previously popped only `correctAnswerIds`. UI already renders `result.rationale` from the attempt response (`ExamDrillsTab.tsx`).
- **Fix applied:** also pop `rationale`. `test_question_hides_answer_key` asserts rationale absent. Attempt POST still returns rationale.

## ISS-004 / WP3 — drillIds

- **Valid.** Recount: 13 lesson files (`lesson-1-2` through `lesson-4-4`) used `q-saa-N.N-` IDs. Question files use hyphens. Terraform lessons already matched.
- **Teacher (content):** approve — hyphen-only alignment, same pattern as CR-0001; no lesson prose changed.
- **Fix applied:** regex replace in those 13 files. `content_lint.py` fails if any `drillIds` entry has no question file. Lint **PASS**.

## Not fixed this pass

WP4–WP12 stay open. Content rewrites (drill bank, labs, citations) need per-WP Teacher review and your approval before implementation, per the plan §5. PYTHON-202/206 and ITMGR-201/205 stay needs-user-decision.
