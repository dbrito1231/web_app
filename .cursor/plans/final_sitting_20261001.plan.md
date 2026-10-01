# Final sitting: Q1 rewrite close-out (2026-10-01)

Author: Lead Developer. Status: **approved by the user 2026-10-01** (option 1; audit term `identity` option a; sweep date 2026-10-01; push straight to `main`).

Parent: `.cursor/plans/q1_remaining_budget_plan_20260926.plan.md` (Amendment 11, final-sitting list).

## Goal

Finish the Q1 rewrite cleanly: fix the last open content items, tidy the records, and run the project's definition-of-done checks.

## Items

| # | Item | Files | Learning content |
|---|---|---|---|
| 1 | **CR-0019:** verify in AWS docs whether AWS Glue for Ray is closed to new customers. If confirmed, label its status in lesson 3.5 (or drop it from the engine list), add it to the RULES closed list, and replace the four distractors with current options that are wrong for a taught reason. If not confirmed, report and change nothing. | `content/lessons/lesson-3-5.json`, `content/citations/cite-saa-3-5-glue-job-engines.json`, `q-saa-3-5-k04-mr`, `k07-mr`, `s01-mc`, `s04-mc`, `reports/fix-loop-r2/q1/RULES.md` | Yes |
| 2 | **CR-0021:** the tf-g4 Warnings bullet on `sensitive` cites "group 3's state-security guidance", which does not exist. Cite group 2's state-file note and group 6's Warnings instead. Wording only. | `content/lessons/lesson-tf-g4.json` | Yes |
| 3 | **D6-FU:** the 4.4 K05 lesson follow-up (both tunnels of one VPN connection carry traffic under ECMP), plus the three optional items (3.3 S01 replica-lag alarm; 4.4 Regional NAT gateway; 4.2-s05 r7 sets only a minimum) where the Teacher and the technical reviewer agree they are worth doing. | lessons 4.4, 3.3; exercise 4.2-s05 if needed | Yes |
| 4 | **LD-Qg7-002:** 7 Terraform stems that state a need without asking a question (tf-g1 1a/1b/1c-mr, tf-g2 2a/2b/2d-mr, tf-g4 4a-mc) get a short question. Wording only. | 7 question files | Yes (wording) |
| 5 | **Audit term `identity`:** remove it from `distractor_type_audit.py` TERMS (it is in one tf-g7 question only and makes closed task 1-1 fail on IAM "identity"). | `scripts/distractor_type_audit.py` | No |
| 6 | **Date sweep:** set every citation `accessed` and every question `reviewedOn` from `2026-09-26` to `2026-10-01` in one commit, and update the literal in `q1_batch_check.py`. Script-verified: only those fields change. | content (about 885 files), `scripts/q1_batch_check.py` | Dates only |
| 7 | **Register reconciliation:** close stale rows with a reason (L1, N8, R6/ISS-070, Q1-T2/T3/T4, ISS-010 and others superseded by the rewrite) and leave a true open list. | `reports/fix-loop/issue-register.md` | No |
| 8 | Update `docs/status.md`, `HANDOFF.md`, close CR-0019 and CR-0021 in `docs/change-requests.md`, and record Q1-STEM-Q / D6-FU as done. | docs | No |
| 9 | **User's local machine:** `python manage.py test workbook`, `npm run build`, `scripts/db_fingerprint.py backend/db.sqlite3`, and the browser smoke test (about 10 questions across 3.1 to tf-g8, then DB restore). These cannot run in the cloud session (no venv, no DB, no browser state). | none | No |

## Process

- Items 1–4 change learning content, so the Teacher validates the plan for them **before** the edits and the result **after**. The technical reviewer verifies the AWS fact for CR-0019 and any AWS claims in D6-FU, using docs.aws.amazon.com read with curl (no WebFetch). Closure rule: reporter and a second role both mark each item Gone.
- Subagents run Sonnet, at most 3 at a time, and run no git. The Lead Dev commits after each step and pushes straight to `main` (user decision).
- The date sweep runs **after** the content edits, so no file is edited twice in flight.

## Risks

- CR-0019 rests on an unverified AWS fact. If the docs do not confirm the closure, nothing changes and the CR is closed as not reproduced.
- The date sweep touches about 885 files. A script compares old and new JSON field by field and fails if anything other than `accessed`/`reviewedOn` changed.
- Pushing straight to `main` skips PR review. Each commit is small and the whole check chain runs before each push.

## Tests

After every step: `content_lint.py`, and for each task touched `q1_batch_check`, `distractor_type_audit`, `stem_echo_check`, `claim_prose_check`, plus `test_q1_letter.py`. Item 9 on the user's machine.

## Outcome (2026-10-01)

- Items 1–8 are done and pushed to `main`: `1d13468` (item 5), `65ac6ba` (items 1–4; Teacher and technical reviewer close), `a7a215b` (item 6), and the records commit (items 7–8).
- Item 3: the Regional NAT gateway was skipped on both reviewers' advice and is logged as optional in the register.
- Item 9 waits on the user's machine.
