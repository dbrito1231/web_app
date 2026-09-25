---
name: Lead Dev fix loop — round 2 (close remaining issues)
overview: "Planning only. Finish the run-2 fix loop properly: set a git baseline, reconcile records, get the user decisions that were skipped, re-verify changes made after the last review, do a real rewrite of the practice-question bank, close the remaining open items, then run the full final regression review the original fix-loop plan requires. Follows AGENTS.md (Lead Dev is the only writer; Teacher validates content; user approves each work package)."
todos:
  - id: approve-plan
    content: User approves this plan (editing this file is not approval)
    status: completed
  - id: phase-0-baseline
    content: Git baseline commit (with user OK), DB fingerprint, server PIDs, register reconciled
    status: pending
  - id: phase-1-decisions
    content: User decisions D1–D6 recorded
    status: pending
  - id: phase-2-reverify
    content: Team re-verifies every change made after round-final (R1–R6)
    status: pending
  - id: phase-3-open-items
    content: Validate and fix remaining open items (O1–O10)
    status: pending
  - id: phase-4-question-bank
    content: Real rewrite of the drill bank (Q1), batch by batch, with AWS/Teacher/Student review
    status: pending
  - id: phase-5-final
    content: Full final regression review by all six agents; exit criteria met; CRs closed
    status: pending
isProject: false
---

# Lead Dev fix loop, round 2: close the remaining issues

**Planning only.** Nothing changes until you approve this plan. Every work package (WP) below also needs its own approval and, for content, a Teacher verdict (AGENTS.md).

This plan continues `.cursor/plans/lead_dev_fix_loop_20260925.plan.md` ("fix-loop plan"). That plan's roles, register, loop, evidence rules and model table all still apply. This plan adds the fixes and the stricter rules below.

## Context

The first fix pass really fixed:
- the answer-saving bug
- the early explanations
- the lesson-to-question links
- the broken lab commands
- lesson navigation
- several screen problems

My review of `reports/fix-loop/` on 2026-09-26 found work still open:
- **The practice-question bank was disguised, not fixed.** 263 questions still use "Apply the objective directly: …" as the right answer. The right answer is the longest choice in 223 of 272 single-answer questions. The stems were only reworded into 8 openings.
- **The "final" round was only a checklist.** It was not the full regression review the plan requires. The plan's own tracker shows Phase 3 in progress and Phase 4 pending.
- **Changes were made after the reviewers finished,** and nobody re-checked them.
- **Records don't match.** The issue register still shows WP4–WP11 as "Reported", while `docs/status.md` says they are complete.
- **Decisions reserved for you were taken by agents:** the by-design calls and the WP4–WP11 design approvals, for which I found no record.
- **There's no git baseline and no end-of-round DB fingerprint,** and the Student used Playwright.

## Stricter rules added in this round

1. **Freeze rule.** Once a team review starts on a WP, Lead Dev changes nothing in that WP's files until the review ends. Any later change, however small, needs a new review of that change. "Lead Dev follow-up" edits written into reviewer reports are not allowed.
2. **Disagreements go to you.** If any reviewer says `Still present` and another says `Gone`, the issue stays open and goes to you with both views. Lead Dev may not settle it by making a tweak.
3. **Lint is not acceptance for content quality.** A lint rule can guard against regressions, but content issues close only when reviewers judge a stratified sample as good (Q1 acceptance).
4. **Only you can approve a by-design or won't-fix status.** An agent may propose it; the register records your decision with a date.
5. **Browser tools.** Use only the built-in browser (Claude Code) or Cursor's browser, against the servers already running. No Playwright, and no new server instances.
6. **Integrity every round.**
   - Take a DB fingerprint before and after each round and restore it.
   - Record server PIDs before and after.
   - Commit per WP with the git diff attached to the Lead Dev review.

## Phase 0: Baseline and records (Lead Dev)

| ID | Task | Done when |
|---|---|---|
| B1 | **Git baseline.** With your OK, create branch `fix/run2-round2` and commit the current tree as "baseline after fix pass 1". The pre-fix state can't be recovered from git; `reports/archive/**` and `reports/evidence/**` stay as the record of it | Commit exists; `git status` is clean apart from ignored files |
| B2 | **DB.** Take a fingerprint of the current `backend/db.sqlite3` into `eval-baseline/fix-loop-r2/db-fingerprint-before.txt`. Record the missing round-final "after" as *not taken* in the register | File exists |
| B3 | **Servers.** Record the PIDs for 5173 and 8000 | Recorded in `reports/fix-loop-r2/preflight.md` |
| B4 | **Reconcile the register** (`reports/fix-loop/issue-register.md`). Bring every ISS row in line with reality, using the round-final reports and `docs/status.md`. Add the new items (FS-FINAL-001/002, the Student's new Low items, the GL-17 leftover) and every item in this plan (R, O, Q and D IDs) | No row contradicts status.md or the reports |
| B5 | **Approval record.** List every file changed in WP4–WP11 (from the status log, the reports and the manifest) in `reports/fix-loop-r2/retro-approval.md` so you can approve them after the fact or ask for rework | You sign off, or rework items are added to this plan |

## Phase 1: Decisions only you can make

| ID | Decision | Options |
|---|---|---|
| D1 | Git baseline and branch (B1) | Yes, or no (fall back to manifests) |
| D2 | WP4–WP11 changes made without a recorded approval (B5) | Approve as-is / rework listed items |
| D3 | ISS-061: `DEBUG=True` and the hard-coded `SECRET_KEY` | Accept for local-only use / move to an env var |
| D4 | ISS-081: audit-grade progress tracking for managers | Out of scope under the KISS rule / scope a small feature |
| D5 | ISS-090: live AWS runs of the 21 guided labs (agents are never allowed to call AWS) | You run some yourself / accept paper checks only |
| D6 | ISS-080 remainder: dated pricing snapshot (AWS-210), templated design exercises (TEACHER-211) | Fix / accept as-is |
| D7 | Lab scanner skips `gl-01` (`scan_lab_placeholders.py:84`) | Keep the skip (intended) / include GL-01 |

## Phase 2: Re-verify changes made after round-final

Each item is checked by the reviewer role named plus one other role. Evidence goes in `reports/fix-loop-r2/round-1/`.

| ID | Change made after review | Check | Roles |
|---|---|---|---|
| R1 | GL-17: second DDL bullet removed; table columns changed | The DDL columns match the CSV uploaded in s06, the query uses them, and cleanup drops the table and database | AWS, Student |
| R2 | GL-08 user data: PowerShell here-string → `user-data.sh` → `file://` | **Line endings:** Windows PowerShell `Set-Content`/`Out-File` writes CRLF, and `#!/bin/bash\r` fails on Linux, so the step must write LF (for example `[IO.File]::WriteAllText` with `` "`n" ``). Also check the encoding (no BOM) and that the Labs screen shows the step readably | AWS, Student |
| R3 | 226 stems split across 8 openings | Covered by Q1; recorded as *not a fix* | Teacher, Student |
| R4 | Start here picker shows lesson titles | All 23 titles are correct; keyboard and screen-reader labels work | Student, Full-Stack |
| R5 | Lesson drill links go to `/exam?q=<id>` | `ExamDrillsTab` actually opens that question from the `q` parameter; a bad ID shows a clear message; the back button works | Full-Stack, Student |
| R6 | ISS-070 citation sentence replacement in lessons 4.2–4.4 | Each bullet cites the correct official doc for its topic | Teacher, AWS |

## Phase 3: Remaining open items (validate first, then fix)

Every item is first reproduced against the current tree, per the fix-loop plan §4. Items that don't reproduce are marked Invalid with evidence.

| ID | Issue (source) | Proposed fix | WP |
|---|---|---|---|
| O1 | All 42 labs fetched at every start (FS-FINAL-001, FULLSTACK-208) | Fetch a lab's details when its card is opened, or when the Labs tab first opens; the header progress uses the summary endpoint | WP8b |
| O2 | Lab card button has no concise accessible name (FS-FINAL-002, FULLSTACK-210) | Add `aria-label="GL-05 details"` or similar | WP8b |
| O3 | Tab ARIA pattern incomplete (FULLSTACK-206) | Complete it: `role=tablist/tab/tabpanel`, `aria-selected`, `aria-controls`, arrow-key moves | WP8b |
| O4 | Markdown helper too limited (FULLSTACK-212) | Check which lesson and lab constructs render wrongly; support only those | WP8b |
| O5 | Mobile exam layout at 375px (FULLSTACK-213) | Reproduce at 375×812; fix the layout if it's confirmed | WP8b |
| O6 | Exam drills don't link back to their lesson (STUDENT-205) | Show a "Study: <lesson title>" link on each drill, built from the lesson `drillIds` | WP7b |
| O7 | Lessons don't link to labs or design exercises (F-206) | Add lab and exercise links per lesson, matching on `objectiveIds` | WP7b |
| O8 | GL-07 says EFS but has no EFS steps (AWS-204); GL-21 title promises HCP (F-204) | Add the EFS steps or retitle GL-07 so it lines up with UL-07; retitle GL-21 or add the content | WP5b |
| O9 | Sidecar files with no templates (TEACHER-209); repeated s12–s15 boilerplate (TEACHER-210) | Provide the templates inline in the steps; make s12–s15 lab-specific | WP5b |
| O10 | Corrupt content JSON surfaces as a 500 (PYTHON-205) | Loader catches the parse error, logs it, and returns a clear 500 JSON error; add a test | WP9b |

## Phase 4: Q1, a real rewrite of the practice-question bank (WP4b)

**Problem (checked on the 2026-09-26 tree):**
- 263 question files use "Apply the objective directly: …" as the keyed choice.
- In single-answer questions, the right answer is the longest choice in **223 of 272**.
- Distractors are generic safety mistakes (root user, no teardown, budget alerts).
- Multiple-answer stems share one frame (about 156 "Select TWO actions that support this requirement").
- About 427 items are still `mcpStatus: pending_recheck`.

**Goal:** questions that test the SAA-C03 and Terraform 004 objectives the way the real exams do.

**Method, batch by batch** (14 SAA task batches, then 8 TF groups; each batch covers about 20–35 questions):
1. **Lead Dev drafts.** Each question gets:
   - a short scenario with a concrete requirement
   - 4 choices (MC) or 5–6 (MR), all of them real, plausible AWS services or approaches from the same area
   - only one choice that is best for the stated constraint
   - a rationale explaining the key **and** why each distractor is wrong
   - objective IDs kept as they are
   - a citation to an official AWS or HashiCorp doc
2. **Fact check.**
   - The AWS Architect checks every AWS claim through the AWS docs MCP (or `docs.aws.amazon.com`).
   - The Teacher checks every Terraform claim through the Terraform MCP or HashiCorp docs.
   - Then set `mcpStatus: verified` and `reviewedOn`, and add `citationIds`.
3. **Teacher pedagogy review.** Does the question test the objective? Is the difficulty right? Is the rationale useful?
4. **Student fairness review.** The Student answers a 30% sample **by reading**, writing down its choice and reasoning before seeing the key, then marks each question fair or unfair (and why).
5. **Your approval** of each batch before the next one starts. The first batch is the pilot and may change the method.

**Acceptance, measured per batch and over the whole bank.** Scripted checks, which also become lint rules:
- 0 choices contain the objective text word for word, and 0 contain "Apply the objective"
- the right answer is the longest choice in **≤ 35%** of MC questions
- key position is balanced within ±10% per module
- no stem opening (first 6 words) is used more than 5 times per module
- every question has ≥ 1 valid `citationId`, `mcpStatus: verified`, and a non-empty rationale that mentions every distractor
- `selectCount` matches the key length, and the MR stem states the number to pick

Judgement checks (these are what close Q1, not the lint):
- The AWS Architect and Teacher rate a 30% stratified sample: **≥ 95% "exam-realistic and correct"**, with no factual errors left.
- The Student's sample is **≥ 90% "fair"**, and no question can be answered from its wording alone.

## Phase 5: Full final regression review

This runs only when every earlier item is Closed or has your decision. It is the fix-loop plan's Phase 4 in full, not a checklist:
- **All six roles**, using the run-2 evaluation plan's scope and sample method with a fresh seed, plus every register item.
- **Every role re-tests the whole app in its own area:**
  - all four tabs at desktop and mobile sizes
  - real answers submitted by reading
  - lab checkpoints ticked and saved
  - export
  - console and network clean
- **Two discussion rounds.** Disagreements go to you.
- **Exit criteria:**
  - zero open register items
  - no new issues at Low or above (Informational may be listed)
  - all checks green: Django tests, `content_lint`, the lab scan, the build, eslint, and Terraform `fmt`/`validate`
  - CRs closed and `docs/status.md` updated
  - DB restored with a matching fingerprint, and server PIDs unchanged
  - the git diff reviewed
- If anything is found, those items go back through Phases 2–4 and the final review runs again.

## Order of work

B1–B5 → D1–D7 → R1–R6 → O10 → O1–O5 → O6–O7 → O8–O9 → Q1 (pilot batch, then the rest) → Phase 5.

The small, safe items go first so the long Q1 rewrite runs on a stable app.

## Recommended models (same as the fix-loop plan)

| Job | Claude Code | Cursor |
|---|---|---|
| Lead Dev: validation and design | Claude Opus 5.5 | Grok 4.7 |
| Lead Dev: code and JSON edits | Claude Opus 5.5 | Composer 2.5 (Grok 4.7 checks the diff) |
| AWS Architect, Teacher, verifiers | Claude Opus 5.5 (Fable 5.1 optional for hard rulings) | Grok 4.7 |
| Full-Stack, Python | Claude Opus 5.5 | Grok 4.7 |
| Student, IT Manager | Claude Sonnet 5 | Grok 4.6 |
| Q1 question drafting | Sonnet 5 drafts, Opus 5.5 reviews | Grok 4.7 (Fast) drafts, Grok 4.7 reviews |
| Scripts, scans, counts | Claude Haiku 4.5 | Composer 2.5 (Fast) |

Q1 fact-checking must use the MCP or doc tools. A model's memory never closes a content item.

## Files most likely to change

- `content/questions/*.json` (Q1)
- `content/labs/{gl-07,gl-08,gl-17,gl-21}.json` and other labs (O8, O9, R1, R2)
- `content/lessons/*.json` (O6, O7, R6)
- `content/citations/*`
- `frontend/src/components/{ExamDrillsTab,LabsTab,LabCard,StartHereTab,Header}.tsx`
- `frontend/src/hooks/useWorkbookBootstrap.ts`
- `frontend/src/utils/markdown.tsx`
- `frontend/src/App.tsx`
- `backend/workbook/content_loader.py` and its tests
- `scripts/content_lint.py`
- `docs/{change-requests,status,labs-and-safety}.md`
- `reports/fix-loop/issue-register.md`
- `reports/fix-loop-r2/**`

## Learning content impact

Yes, and it is large. Q1 rewrites most of the SAA and TF question bank, and O6–O9 plus R1, R2 and R6 change labs and lessons. Every content WP needs a Teacher verdict before your approval and again after the fix.
