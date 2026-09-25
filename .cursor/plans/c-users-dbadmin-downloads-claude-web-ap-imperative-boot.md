---
name: Lead Dev fix loop (run-2 evaluation findings)
overview: "Planning only. The Lead Developer (AGENTS.md) validates every run-2 evaluation finding against the current code, fixes the validated ones in approved work packages, self-reviews, then has the same six-agent team re-review. The cycle Review → Validate → Fix → Lead Dev review → Team review repeats until the issue register has no open valid issues and a full regression round finds nothing new."
todos:
  - id: approve-master
    content: User approves this master plan (process + register + work packages). Editing is not approval.
    status: pending
  - id: phase-0
    content: Setup — save plan to .cursor/plans, git baseline decision, DB baseline, register built, CRs recorded
    status: pending
  - id: phase-1-validate
    content: Validate every register item (valid / invalid / duplicate / by-design / needs-user)
    status: pending
  - id: phase-2-wp-plans
    content: Per-WP fix design + Teacher pre-validation (content WPs) + user approval
    status: pending
  - id: phase-3-loop
    content: Fix → Lead Dev review → Teacher re-validation → six-agent team review, repeated per WP until clean
    status: pending
  - id: phase-4-final
    content: Full regression round with all six agents; exit criteria met; CRs closed; status.md updated
    status: pending
isProject: false
---

# Lead Dev fix loop: run-2 evaluation findings

> **Where this file goes.** Plan mode only lets me write to this scratch location. The first step after approval (Phase 0.1) copies it to `.cursor/plans/lead_dev_fix_loop_20260925.plan.md`, where AGENTS.md says Lead Dev plans live.

## Context

Run 2 (`reports/`, plan `.cursor/plans/eval_redo_extensive_20260925.plan.md`) produced 62 findings plus several evaluation-process gaps. You want the **Lead Developer** role from `AGENTS.md` to fix them. The rules:
- Each issue is proven real **before** it is fixed.
- The same six-role team re-reviews every fix.
- The loop repeats until nothing valid is left and no new issues appear.

AGENTS.md rules that apply throughout:
- Lead Dev is the only writer.
- Every change needs a user-approved plan. Approving one plan does not cover later changes.
- Content-affecting changes need a **Teacher** verdict before the plan goes to you and again after the fix.
- Change requests are recorded in `docs/change-requests.md`.
- The definition of done is: `python manage.py test workbook`, `python scripts\content_lint.py`, `npm run build`, Terraform `fmt`/`validate` when `lab-fixtures/**` changes, and a `docs/status.md` update.
- No AWS calls, and no credentialed Terraform.

## 1. Roles in this plan

| Role | Job in the loop | Writes files? |
|---|---|---|
| **Lead Developer** (AGENTS.md) | Validates issues, designs fixes, implements, self-reviews, records CRs, updates status | Yes (only writer) |
| **Teacher** (AGENTS.md) | Pre-validates content fix designs, re-validates content results, owns Terraform accuracy | No |
| **Team reviewers** (same six personas as the run-2 plan §6: Student, Teacher, AWS Architect, IT Manager, Full-Stack, Python) | Confirm each fixed issue is gone; hunt for regressions and new issues | Only `reports/fix-loop/**` |
| **You** | Approve the master plan, each work-package design, and any "by design / won't fix" call; break ties | — |

## 2. Issue register (single source of truth)

Phase 0 creates `reports/fix-loop/issue-register.md`, one row per issue. Columns:
- `ISS-###` and the source IDs (all reporter IDs, e.g. `FULLSTACK-230, PYTHON-230, ITMGR-230, STUDENT-211`)
- title, severity, and the WP it belongs to
- **validation status** and **fix status**
- CR ID, and evidence links for validation, fix, and review

**Status flow:** `Reported → Validated: {Valid | Invalid | Duplicate-of | By-design (needs user) | Needs-user-decision} → Fix designed → Approved → Fixed → Lead-Dev-verified → Teacher-verified (content only) → Team-verified → Closed`
- Any failure sends the issue back to `Fixed`, with the failing round noted (**Reopened**).
- New issues found in a review join as `Reported (round N)`.

### Initial register contents, grouped into work packages (WPs)

| WP | Theme | Source findings | Proposed solution (confirmed or adjusted after validation) |
|---|---|---|---|
| **WP1** | Saves fail (Critical) | FULLSTACK-230, PYTHON-230, ITMGR-230, STUDENT-211, TEACHER-212 | `backend/config/settings.py`: add `CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS`. Add a Django test that POSTs `/api/attempts` and `/api/labs/<id>/checkpoints` **with `HTTP_ORIGIN='http://127.0.0.1:5173'`** plus a valid CSRF cookie and token (this closes the test blind spot). `frontend/src/api/client.ts`: when a non-JSON 403 comes back, show a plain message ("Your answer couldn't be saved — the app's server refused the request") instead of the bare "Forbidden". |
| **WP2** | Explanations leak early (High) | FULLSTACK-201, PYTHON-201, PYTHON-203, ITMGR-201 (part) | `backend/workbook/views.py` question GET (`public_question`): strip `rationale` as well as `correctAnswerIds`. Return the rationale only in the `POST /api/attempts` response. Update `ExamDrillsTab.tsx` to show the rationale from the attempt result. Extend `test_question_hides_answer_key` to assert that `rationale` is absent. |
| **WP3** | Lesson→drill links (High) | F-201, TEACHER-214 | Change the dotted `drillIds` in the 13 SAA lessons to hyphens. Add a `content_lint.py` rule: every `drillIds` entry must match an existing question file. No backend normalisation; lint prevents the mismatch instead. |
| **WP4** | Drill bank quality (High) | F-202, AWS-211, STUDENT-204, TEACHER-208, TEACHER-215, ITMGR-203, plus answer-position bias (choice `a` was correct in 40 of 41 sampled MCs) | (a) Script the key-position distribution over all 429 questions to validate the bias. (b) Shuffle choices at presentation (the `presentedOrder` field already exists; confirm it is used). (c) Add lint rules: key positions balanced per module; longest-choice-is-key rate under a threshold; no stem skeleton repeated more than N times. (d) Rewrite template questions in **batches per SAA task** (14 batches) and per TF group. Each rewrite is scenario-based, with plausible distractors and a rationale that explains every distractor. AWS facts are checked with the AWS docs MCP and Terraform facts with the Terraform MCP or HashiCorp docs. `mcpStatus` and `reviewedOn` are updated. |
| **WP5** | Broken or confusing labs | AWS-201 (GL-08 user data → bash `#!/bin/bash` + `python3 -m http.server 80`), AWS-202 (GL-05 NACL → `--protocol 6 --port-range From=22,To=22`), AWS-203 (GL-17 → add the full `CREATE EXTERNAL TABLE` step), AWS-204 (GL-07 EFS steps, or retitle; align with UL-07), AWS-206 (GL-19 subnet list comma-joined), AWS-207 (GL-18 PowerShell-safe `--network-configuration` via a JSON file), AWS-208 (GL-07 volume AZ taken from the instance), AWS-209 (UL-05 tag `ul-05`), F-203 (GL-20 s03 wording), F-204 (GL-21 title vs content), F-205 / ITMGR-206 (UL `beforeYouStart`), TEACHER-209 (sidecar file templates), TEACHER-210 (s12–s15 boilerplate), STUDENT-201 (UL-01 prerequisite on GL-03), STUDENT-208 | JSON edits in `content/labs/*.json`. Each command is checked against the AWS CLI reference. Nothing is ever run. |
| **WP6** | Cleanup safety check | AWS-205 | `scripts/scan_lab_placeholders.py`: replace the `pass` at about line 66 with a real check that every cleanup variable was set in an earlier step. Fix the 16 labs it flags. |
| **WP7** | Lessons reachable and connected | STUDENT-203 (22 lessons not in app navigation), STUDENT-205, F-206, STUDENT-202 | Add lesson navigation in the existing tabs (`curriculum.ts`, `LabsTab`/`StartHereTab`). Validate the exact gap first, and follow the locked layout plan `ccna_layout_replica_160c046c`. Link exam drills to their lesson, and lessons to their labs and design exercises. Add a permissions-boundary explanation to the lesson that comes before GL-01. |
| **WP8** | Front-end quality | FULLSTACK-202 (mock exam card), 203 (N+1 fetch), 204 (bad URL → redirect to `/labs`), 205 (MR must match `selectCount`), 206 (tab ARIA), 207 (best scores from API), 208/ITMGR-202 (lazy lab load plus a visible load error), 209 (duplicate GET), 210 (accessible names), 211 (`aria-live` feedback), 212 (markdown coverage), 213 (mobile exam grid) | React changes in `frontend/src/**`. Each one is reproduced first. |
| **WP9** | Back-end robustness | PYTHON-204 (validate `selectedIds` against the choices → 400), PYTHON-205 (corrupt JSON → clean 500/404 plus a log entry), PYTHON-202 and PYTHON-206 (by design: need your call) | `scoring.py`, `content_loader.py`, `views.py`, plus tests. |
| **WP10** | Coverage and citations | F-207 (wrong citation URL reused), ITMGR-204 (every registry row is `implemented_unverified`), about 427 items at `mcpStatus: pending_recheck` | Fix the citation mapping. Recheck with MCP in batches alongside WP4. Promote registry rows only with evidence. |
| **WP11** | Program and docs | ITMGR-205 (sandbox/SCP guidance), AWS-210 (dated pricing snapshot), TEACHER-211 (templated design exercises), ITMGR-201 (audit-grade metrics) | Update the docs (`docs/labs-and-safety.md`). ITMGR-201 may break the KISS rule (multi-user, audit), so you decide scope. |
| **WP12** | Not verifiable by agents | TEACHER-213 (live-run all 21 guided labs), FULLSTACK-213 if not reproducible | Agents never call AWS. These go to you as optional manual checks and are marked `Needs-user-decision`. |

## 3. Phase 0: Setup (Lead Dev)

1. Copy this plan to `.cursor/plans/lead_dev_fix_loop_20260925.plan.md`.
2. **Git baseline (your decision).** The repo has no commits; everything is untracked. Recommended: with your OK, make one baseline commit on a new branch `fix/run2-findings` so every fix is a reviewable diff, and commit each WP separately. Without git, Lead Dev keeps a SHA-256 manifest per round instead.
3. Pre-flight: record the existing servers (5173 → PID 28264, 8000 → PID 20200 at plan time).
   - Settings and code changes rely on Django autoreload and Vite HMR.
   - **Never start a second instance.** If a reload fails, ask you to restart.
4. DB: take a baseline backup and fingerprint (same method as run 2) into `eval-baseline/fix-loop/`. Every team review round starts from the baseline and restores to it afterwards, because once WP1 lands, UI use will write progress.
5. Build `issue-register.md` from the table above, reading each item's source report text.
6. Record one CR per WP in `docs/change-requests.md` using the template, with the issue IDs listed inside.

## 4. Phase 1: Validate every issue (Lead Dev, checked by Teacher for content)

For each `ISS`:
1. **Reproduce against the current tree**, not the report's quote:
   - Content: open the JSON and quote the field.
   - Code: file:line, plus a GET call or UI steps.
   - Tests: a failing test written first, but only once the WP is approved.
2. Choose a status:
   - **Valid:** reproduced, with evidence linked.
   - **Invalid:** does not reproduce; say why.
   - **Duplicate-of ISS-x.**
   - **By-design:** conflicts with a locked decision in `aws_terraform_workbook_92c3d04f.plan.md` or AGENTS.md; goes to you.
   - **Needs-user-decision.**
3. Counts must be recomputed by script, never copied from a report. Example: the 13 lessons are re-counted, and so are the key positions across all 429 questions.
4. The **Teacher** must agree on every content item's validation. Disagreements go to you, and both views are recorded.

Output: `reports/fix-loop/validation.md`. Only **Valid** items move on.

## 5. Phase 2: Work-package fix design and approval

For each WP, Lead Dev writes an inline design section in this plan file covering:
- goal, and the exact files touched
- the solution for each valid ISS
- risks and tests
- whether learning content is affected, and the rollback approach

Then:
- Content-affecting WPs (3, 4, 5, 6, 7, 10, 11) need a **Teacher pre-validation** verdict (approve / concerns), recorded in the section.
- **You approve each WP design.** Recommended order, by impact and dependency: WP1 → WP2 → WP3 → WP9 → WP8 → WP7 → WP5 → WP6 → WP10 → WP4 (largest; runs in batches) → WP11.
- WP1 goes first because the saves must work before anyone can review the feedback flow.

## 6. Phase 3: The loop (per WP; WP4 per batch)

```
┌─► 1 Review    — team findings for this WP (round 0 = run-2 reports)
│   2 Validate  — Lead Dev reproduces each (Phase 1 rules); Teacher agrees for content
│   3 Fix       — Lead Dev implements the approved design; tests written first where possible
│   4 Lead Dev review — definition-of-done checks + self-verification of every ISS (see below)
│   5 Teacher re-validation (content WPs)
│   6 Team review — six agents verify fixes + hunt regressions/new issues
│   7 Triage   — new/reopened issues → register (status Reported, round N)
└── if any Valid issue open or new issue found → back to 1 with only those items
    else → WP closed (CR closed, status.md updated)
```

**Step 4, Lead Dev review (must pass before the team sees anything):**
- Run `python manage.py test workbook`, `python scripts\content_lint.py`, `python scripts\scan_lab_placeholders.py`, `npm run build`, and `npx eslint src`.
- Run `terraform fmt -check` and `validate` if `lab-fixtures/**` changed.
- For each fixed ISS, re-run the exact reproduction from validation and show that it now passes. Evidence goes in `reports/fix-loop/round-N/leaddev.md`.
- Show the diff (git, or the manifest delta), and confirm that nothing outside the approved file list changed.

**Step 6, Team review (thorough by design):**
- **Fix verification.** Each ISS is re-checked by its **original reporter role and one other role**. Both must mark it `Gone`, with evidence. A `Still present` from either reopens it.
- **Regression sweep, every round, not just for the WP:**
  - all automated checks
  - the full content scan (the run-2 scan script, extended with the new lint rules)
  - a UI pass over all four tabs at desktop and mobile sizes
  - one real drill answered **by reading** and one lab checkpoint, now that saves work
  - a console and network check
- **New-issue hunt.** Each role spends part of the round on its own area, looking outside the changed files for anything the change could have affected: imports, shared components, content that references edited IDs.
- **Content accuracy (WP4, 5, 10):**
  - The AWS Architect checks every changed AWS fact and CLI command against AWS docs (MCP or the CLI reference).
  - The Teacher checks every changed Terraform item against the registry MCP or HashiCorp docs.
  - Model memory alone cannot close an item.
- Evidence rules follow run 2 (EV rows with the real tool call; "Confirmed" requires direct observation). Each round's reports go to `reports/fix-loop/round-N/<ROLE>.md`.
- For each finding, a disputed verdict goes to a neutral verifier agent. If the dispute is still unresolved, it goes to you. No majority votes.

**Guardrails:**
- DB restore and fingerprint match at the end of every team round.
- Server PIDs unchanged.
- No AWS calls, and no direct `curl` POSTs.
- If an issue is reopened **3 times**, Lead Dev stops that item and brings you options. The loop keeps going on everything else.
- A **new** issue that needs a change outside an approved WP gets a design amendment and your approval before it is fixed. AGENTS.md says approval does not carry over.

## 7. Phase 4: Final regression round and exit criteria

When every WP is closed, all six agents run one **full** evaluation round. It covers the run-2 plan's scope and sample method, with a fresh seed, plus every register item. The work is done when all of these hold:
1. The register has **zero** items in any open state. Every item is Closed, Invalid, Duplicate, or By-design/Won't-fix **approved by you**.
2. The final round reports **no new issues** at Low or above. Informational items are listed but do not block.
3. The run-2 regression tests pass: the CSRF test with an Origin header, the rationale-absent test, and the lint rules for `drillIds`, key balance, template stems, and cleanup variables.
4. The definition of done is all green: Django tests, `content_lint`, lab scan, build, eslint, and Terraform `fmt`/`validate`.
5. Every CR is closed in `docs/change-requests.md`. `docs/status.md` has one row per WP with evidence. Teacher sign-off is recorded for every content WP.
6. The DB is restored to its baseline fingerprint, and no stray files are left outside the approved paths.

If the final round finds anything, go back to Phase 3 for those items only, then run the final round again.

## 8. Recommended models

The same plan works in either tool. Use the strongest model where judgement or accuracy matters, and a cheaper one for repetitive work.

| Job | Claude Code | Cursor |
|---|---|---|
| **Lead Developer: validation and fix design** | **Claude Opus 5.5** (`claude-opus-5-5`) | **Grok 4.7** |
| **Lead Developer: implementing code and JSON edits** | **Claude Opus 5.5** | **Composer 2.5** (Cursor's coding model). Grok 4.7 re-checks the diff in the Lead Dev review step |
| **AWS Architect, Teacher, verifiers** (fact checks, adjudication) | **Claude Opus 5.5**. Claude Fable 5.1 (`claude-fable-5-1`) is an option for the hardest rulings; try it on one batch first | **Grok 4.7**, the strongest reasoning option of the two families |
| **Full-Stack, Python reviewers** | **Claude Opus 5.5** | **Grok 4.7** |
| **Student, IT Manager reviewers** | **Claude Sonnet 5** (`claude-sonnet-5`) | **Grok 4.6** |
| **Bulk WP4 question rewrites** (drafts; every batch is still reviewed by the AWS Architect and Teacher) | **Claude Sonnet 5** drafts, **Opus 5.5** reviews | **Grok 4.7 (Fast)** drafts, **Grok 4.7** reviews |
| **Scripts: scans, lint runs, counts, register upkeep** | **Claude Haiku 4.5** (`claude-haiku-4-5-20251001`) | **Composer 2.5 (Fast)** |

Notes:
- **Claude Code:**
  - Run the six-agent team rounds as a Workflow, with a per-agent `model` set as above.
  - The main session (Lead Dev) stays on Opus 5.5.
  - Because of the AGENTS.md single-writer rule, reviewer agents get no edit permission outside `reports/fix-loop/**`.
- **Cursor:**
  - AGENTS.md is picked up automatically.
  - Run each reviewer persona as a separate Agent chat (or background agent) so their context stays independent.
  - Paste the persona text word for word.
  - Keep the Lead Dev chat as the only chat that edits files.
- **Cursor is limited to Composer and Grok models** (your choice).
  - Grok 4.7 is billed at 2× above 256k input tokens, up to 500k. Keep each review agent's context focused (one WP or batch plus the regression pack) and avoid loading the whole repo.
  - Composer 2.5 does the actual edits, so the model that writes a fix is different from the one that reviews it.
- The Cursor model names come from `cursor.com/docs/models` as of 2026-09-25, and the list changes often. If a name above isn't in your picker, use the closest newer Grok or Composer model.

## 9. Files most likely to change (confirmed per WP in Phase 2)

- `backend/config/settings.py`
- `backend/workbook/{views,scoring,content_loader}.py`
- `backend/workbook/tests/test_scoring_and_api.py`
- `frontend/src/api/client.ts`
- `frontend/src/components/{ExamDrillsTab,LabsTab,LabCard,StartHereTab,Header}.tsx`
- `frontend/src/data/curriculum.ts`
- `frontend/src/utils/markdown.tsx`
- `scripts/{content_lint,scan_lab_placeholders}.py`
- `content/lessons/lesson-*.json` (13)
- `content/questions/q-*.json` (WP4 batches)
- `content/labs/{gl,ul}-*.json`
- `content/citations/*`
- `content/coverage/saa_registry.json`
- `docs/{labs-and-safety,change-requests,status}.md`

## 10. Verification summary

- Each WP closes only after the Lead Dev review evidence, the Teacher verdict (content WPs), and `Gone` from two team roles per issue.
- The whole plan closes only after the Phase 4 exit criteria.
- Every loop's evidence stays under `reports/fix-loop/`, so every closure can be audited.
