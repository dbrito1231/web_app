# Plan P1: Verify the coverage registry (R6 / ISS-070 remainder)

Author: Lead Developer. Status: **draft, awaiting user approval.** Phase 3 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-02)

- All 189 rows of `content/coverage/saa_registry.json` have `status: "implemented_unverified"`, `gap: "MCP re-check and Phase 6 verification pending"`, `next_action: "Phase 6 verify"` and empty `validation_refs`.
- The Coverage tab shows **0/189 "verified with evidence"** (`CoverageTab.tsx` counts `status === 'verified'`). The learner sees a gap that no longer exists: every lesson and question behind these rows was rewritten and closed through the Q1 pipeline.
- All 189 rows have `lesson_refs` and `drill_refs`; no drill ref is dangling.
- **2 rows drift:** `SAA-1.1-K04` and `SAA-1.1-K05` list `drill_refs` that differ from the questions whose `objectiveIds` name them.
- `docs/coverage-and-metrics.md` allows `missing | planned | partial | implemented_unverified | verified` and defines "Verified atomic = verified / 189".

## Options (KISS)

1. **Evidence-based flip (recommended).** A read-only script checks each row:
   - the lesson in `lesson_refs` is a closed Q1 lesson;
   - `drill_refs` equals the set of questions whose `objectiveIds` name the row;
   - every such question is `mcpStatus: verified` with citations.

   Rows that pass get `status: "verified"`, `validation_refs` pointing to the Q1 reports for that task (`reports/fix-loop-r2/q1/progress.md` plus the task's Student and review files), and `gap`/`next_action` cleared. Rows that fail stay `implemented_unverified` with the reason in `gap`. The 2 drifting rows are fixed by regenerating `drill_refs` from question `objectiveIds`.
2. **Status-only flip.** Set all 189 to `verified` in one edit and cite `progress.md`. This is faster, but it skips the per-row check, so a broken row could be marked verified.
3. **Change the label, not the data.** Leave the statuses and change the Coverage tab text to explain that they are pending. This hides the problem, and the metric stays 0%.

## Recommended approach (option 1)

1. Write `scripts/registry_verify.py`. It is read-only by default and prints a per-row PASS/FAIL table; `--write` applies the changes.
2. Run it read-only and hand the output to the Teacher. The Teacher spot-checks about 20 rows across all 4 domains: does the lesson really teach the bullet, and do the drills really test it?
3. After the Teacher approves, run `--write` once. Then update `docs/coverage-and-metrics.md` to say what "verified" means: a closed Q1 lesson plus matching verified drills plus reviewer evidence.
4. The Teacher re-validates the written file against the spot-check sample.

## Files

`scripts/registry_verify.py` (new), `content/coverage/saa_registry.json`, `docs/coverage-and-metrics.md`, the register and status docs.

## Risks

- "Verified" could overclaim. Rows with live-AWS practice (`practice_mode: live_aws`, 25 rows) are verified on paper only: labs are never run against AWS (decision D5). The script must not claim a live run; `validation_refs` will cite paper reviews.
- `content_lint.py` checks the registry. Run it after `--write`.

## Tests

`content_lint.py`; `manage.py test workbook` (the coverage endpoint); `npm run build`; a smoke check that the Coverage tab shows the new count.

## Learning content affected

Yes (`content/coverage/**` and `docs/coverage-and-metrics.md`). The Teacher validates before and after.
