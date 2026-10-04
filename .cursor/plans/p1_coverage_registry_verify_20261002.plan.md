# Plan P1: Verify the coverage registry (R6 / ISS-070 remainder)

Author: Lead Developer. Status: **approved by the user 2026-10-04 (recommended option).** Phase 3 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-02)

- All 189 rows of `content/coverage/saa_registry.json` have `status: "implemented_unverified"`, `gap: "MCP re-check and Phase 6 verification pending"`, `next_action: "Phase 6 verify"` and empty `validation_refs`.
- The Coverage tab shows **0/189 "verified with evidence"** (`CoverageTab.tsx` counts `status === 'verified'`). The learner sees a gap that no longer exists: every lesson and question behind these rows was rewritten and closed through the Q1 pipeline.
- All 189 rows have `lesson_refs` and `drill_refs`; no drill ref is dangling.
- **Demo drills in two rows:** `SAA-1.1-K04` lists `q-a0-mr-001`, and `SAA-1.1-K05` lists `q-a0-mc-001` and `q-a0-mr-001`. These are the two demo questions, which have no `mcpStatus` and no citations. (Teacher correction: these rows do not drift; their `drill_refs` match the questions' `objectiveIds`.)
- `docs/coverage-and-metrics.md` is still the Phase-0 skeleton. Its gap report says every row is `missing` and shows "0 / 189", so it contradicts the registry (CR-0022).
- `docs/coverage-and-metrics.md` allows `missing | planned | partial | implemented_unverified | verified` and defines "Verified atomic = verified / 189".

## Options (KISS)

1. **Evidence-based flip (recommended).** A read-only script checks each row:
   - the lesson in `lesson_refs` is a closed Q1 lesson;
   - `drill_refs` equals the set of questions whose `objectiveIds` name the row;
   - every such question is `mcpStatus: verified` with citations, excluding the demo `q-a0-*` questions;
   - the task's `distractor_type_audit` result has no real-reuse FAIL. This is why Phase 1 (P2) runs first;
   - every `validation_refs` path exists. The 1-1 pilot's evidence is a line in `progress.md`, so cite that line, not missing files.

   Rows that pass get `status: "verified"`, `validation_refs` pointing to the Q1 reports for that task (`reports/fix-loop-r2/q1/progress.md` plus the task's Student and review files), and `gap`/`next_action` cleared. Rows that fail stay `implemented_unverified` with the reason in `gap`. Demo drills: remove `q-a0-*` from `drill_refs` in K04 and K05, so the rows rest on real verified drills. If a row would then have no drill, keep it unverified and flag it. Single-drill rows (69) count if their one drill is verified, cited and not a demo; the Teacher confirms this in the spot-check.
2. **Status-only flip.** Set all 189 to `verified` in one edit and cite `progress.md`. This is faster, but it skips the per-row check, so a broken row could be marked verified.
3. **Change the label, not the data.** Leave the statuses and change the Coverage tab text to explain that they are pending. This hides the problem, and the metric stays 0%.

## Recommended approach (option 1)

1. Write `scripts/registry_verify.py`. It is read-only by default and prints a per-row PASS/FAIL table; `--write` applies the changes.
2. Run it read-only and hand the output to the Teacher. The Teacher spot-checks about 20 rows across all 4 domains, including K04, K05, a single-drill row, a `design_exercise` row and several `live_aws` rows: does the lesson really teach the bullet, and do the drills really test it?
3. After the Teacher approves, run `--write` once. Then refresh `docs/coverage-and-metrics.md`: replace the stale Phase-0 gap report, rollup and skeleton text, and define "verified" narrowly: "the lesson and drills were reviewed on paper by a technical reviewer, the Teacher and a blind Student, with official citations." It must not say "tested", "exam-ready" or "run in AWS". For the 25 `live_aws` rows, write "paper review only; not run in AWS (decision D5)" in each row's `gap` or `validation_refs`, not only in the doc. Check that the Coverage tab caption still says this is not a pass probability.
4. The Teacher re-validates the written file against the spot-check sample.

## Files

`scripts/registry_verify.py` (new), `content/coverage/saa_registry.json`, `docs/coverage-and-metrics.md`, the register and status docs.

## Risks

- "Verified" could overclaim. Rows with live-AWS practice (`practice_mode: live_aws`, 25 rows) are verified on paper only: labs are never run against AWS (decision D5). The script must not claim a live run; `validation_refs` will cite paper reviews.
- `content_lint.py` checks the registry. Run it after `--write`.

## Tests

`content_lint.py`; `manage.py test workbook` (the coverage endpoint); `npm run build`; a smoke check that the Coverage tab shows the new count.

## Teacher pre-validation (2026-10-02)

Concerns, folded in above: the demo-drill correction replaces the false drift claim; the audit result and `validation_refs` path checks are pass criteria; the live_aws paper-review wording is added; the stale doc is refreshed. See `reports/open-items/TEACHER-plans.md`.

## Learning content affected

Yes (`content/coverage/**` and `docs/coverage-and-metrics.md`). The Teacher validates before and after.
