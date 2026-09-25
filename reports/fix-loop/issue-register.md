# Fix-loop issue register (run-2, reconciled 2026-09-25)

Round-2 plan: `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`.

Git baseline: decision D1 recorded 2026-09-25 — commit on `main` (not `fix/run2-round2`). SHA fingerprint: `eval-baseline/fix-loop-r2/db-fingerprint-before.txt` (`930f0e72…`). Round-final "after" fingerprint: **not taken**.

`docs/status.md` row `fix-loop-wp4-11` means the pass-1 edits landed. It does not mean these rows are Closed. CR-0009–CR-0016 are marked done in the change log for the same reason.

Team checklist `reports/fix-loop/round-final/` did run. It was not the full regression in the original fix-loop plan. Edits after that checklist are not closed by the "Lead Dev follow-up" lines in those reports.

Only a user decision can set By-design or won't-fix (D3, D4, D5, D6).

## Pass-1 issues

| ISS | Sources | WP | Validation | Fix status | CR |
|-----|---------|----|------------|------------|----|
| ISS-001 | FULLSTACK-230, PYTHON-230, ITMGR-230, STUDENT-211 | WP1 | Valid | Closed. Gone: Student, Full-Stack, Python, IT Manager | CR-0006 |
| ISS-002 | TEACHER-212 | WP1 | Duplicate-of ISS-001 | Closed | CR-0006 |
| ISS-003 | FULLSTACK-201, PYTHON-201, PYTHON-203, ITMGR-201 | WP2 | Valid | Closed. Gone: Student, Full-Stack, Python, IT Manager | CR-0007 |
| ISS-004 | F-201, TEACHER-214 | WP3 | Valid (13 lessons) | Closed. Gone: Teacher, Student | CR-0008 |
| ISS-010 | F-202, AWS-211, STUDENT-204 | WP4 / Q1 | Valid. Disagreement | Open. Teacher: banned stem Gone, leftover wording Informational. Student: Still present. Stays open for Q1 | CR-0009 |
| ISS-020 | AWS-201–209, F-203–205, STUDENT-201, STUDENT-208 | WP5 | Valid, partial | Open. AWS command checklist Gone. Teacher GL-20 and UL `beforeYouStart` Gone. Student: GL-08 Still present, then the file changed (R2). GL-07 EFS and GL-21 title are O8. Sidecars and s12–s15 are O9 | CR-0010 |
| ISS-030 | AWS-205 | WP6 | Valid | Team-verified for the scanner (AWS Gone). Residual: some teardowns assign `$null` and never create the resource. Not a user by-design close | CR-0011 |
| ISS-040 | STUDENT-203, STUDENT-205, F-206, STUDENT-202 | WP7 | Valid, partial | Open. Start-here list Gone (Student, IT Manager). Drill-to-lesson is O6. Lesson-to-lab links are O7. Title and `/exam?q=` edits await R4 and R5 | CR-0012 |
| ISS-050 | FULLSTACK-202–213, ITMGR-202 | WP8 | Valid, partial | Open. Round-final checklist Gone. FS-FINAL-001 and FS-FINAL-002 were patched after the review (O1, O2) and are not re-checked. O3–O5 not closed | CR-0013 |
| ISS-060 | PYTHON-204, PYTHON-205 | WP9 | Valid, partial | Open. Unknown choice → 400 is Gone (Python). Corrupt JSON → bare 500 is O10 | CR-0014 |
| ISS-061 | PYTHON-202, PYTHON-206 | WP9 | By-design | Closed 2026-09-25. You accepted debug mode and the local secret key for this local-only app (D3) | CR-0014 |
| ISS-070 | F-207, ITMGR-204, pending_recheck | WP10 | Valid, partial | Open. The domain-4 citation sentence was replaced after review (R6, not accepted as Gone). Unique official URLs and `implemented_unverified` remain. Fact recheck is part of Q1 | CR-0015 |
| ISS-080 | ITMGR-205, AWS-210, TEACHER-211 | WP11 | Partial | Sandbox note Closed (IT Manager Gone). You chose to fix the dated price snapshot and templated design exercises (D6, 2026-09-25). That fix is not started | CR-0016 |
| ISS-081 | ITMGR-201 audit-grade metrics | WP11 | By-design | Closed 2026-09-25. You left audit-grade manager metrics out (D4) | CR-0016 |
| ISS-090 | TEACHER-213 live labs | WP12 | By-design | Closed 2026-09-25. Paper checks only. Agents do not call AWS (D5) | — |

## Found in round-final, then edited without a new review

| ID | Source | Validation | Fix status |
|----|--------|------------|------------|
| FS-FINAL-001 | Full-Stack. All labs fetched on cold start. Same as O1 | Valid at review time | Patched after review (`ensureLabs` on the Labs tab). Awaiting re-check. Not Closed |
| FS-FINAL-002 | Full-Stack. Lab card had no concise name. Same as O2 | Valid at review time | Patched after review (`aria-label` on the card). Awaiting re-check. Not Closed |
| STUDENT-picker | Student Low. Start here showed raw lesson ids. Same as R4 | Valid at review time | Patched after review (titles). Awaiting R4. Not Closed |
| STUDENT-drill-links | Student Low. Lessons did not deep-link drills. Related to R5 and O6 | Valid at review time | Links to `/exam?q=` added after review. Awaiting R5. "Study this lesson" on the drill is still O6 |
| GL-17-ddl | AWS Low. Second DDL bullet disagreed with the CSV. Same as R1 | Valid at review time | Second bullet removed after review. Awaiting R1. Not Closed |

## Round-2 re-checks (not started)

| ID | What | Status |
|----|------|--------|
| R1 | GL-17 DDL matches the CSV, the query, and cleanup | Reported |
| R2 | GL-08 `user-data.sh` is LF, no BOM, and readable on the Labs screen. Current step still says `Set-Content` | Reported |
| R3 | Eight stem openings | Recorded as not a fix. Covered by Q1 |
| R4 | All 23 Start here titles; keyboard and screen-reader labels | Reported |
| R5 | `/exam?q=` opens that question; a bad id is clear; back works | Reported |
| R6 | Each domain-4 bullet cites the official doc for its topic | Reported |

## Round-2 open items (not started)

| ID | Issue | WP | Status |
|----|-------|----|--------|
| O1 | Lab details and header progress (FS-FINAL-001) | WP8b | Reported. Partial patch exists; validate first |
| O2 | Lab card accessible name (FS-FINAL-002) | WP8b | Reported. Partial patch exists; validate first |
| O3 | Tab ARIA: tablist, selected, controls, arrow keys | WP8b | Reported |
| O4 | Markdown helper misses some lesson and lab constructs | WP8b | Reported |
| O5 | Exam layout at 375px | WP8b | Reported |
| O6 | Each drill links back to its lesson | WP7b | Reported |
| O7 | Each lesson links to its labs and design exercises | WP7b | Reported |
| O8 | GL-07 says EFS but has no EFS steps; GL-21 title says HCP | WP5b | Reported |
| O9 | Missing sidecar templates; s12–s15 boilerplate | WP5b | Reported |
| O10 | Corrupt content JSON returns a clear JSON 500 | WP9b | Reported |
| Q1 | Rewrite the practice-question bank | WP4b | Reported. Blocked until the pilot batch is approved |

## Decisions

| ID | Decision | Status |
|----|----------|--------|
| D1 | Git baseline | Decided 2026-09-25: commit on `main`, not `fix/run2-round2` |
| D2 | WP4–WP11 after the fact | Decided 2026-09-25: approve as-is. See `reports/fix-loop-r2/retro-approval.md` |
| D3 | ISS-061 debug mode and local secret key | Decided 2026-09-25: accept for this local-only app |
| D4 | ISS-081 audit-grade manager metrics | Decided 2026-09-25: leave it out |
| D5 | ISS-090 live AWS lab runs | Decided 2026-09-25: paper checks only |
| D6 | Dated prices and templated design exercises | Decided 2026-09-25: fix them. Work not started |
| D7 | Lab scanner skips `gl-01` | Decided 2026-09-25: include GL-01. Code change not started |
