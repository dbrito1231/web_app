---
name: Lead Dev fix loop — round 2 (close remaining issues)
overview: "Planning only. Finish the run-2 fix loop properly: set a git baseline, reconcile records, get the user decisions that were skipped, re-verify changes made after the last review, do a real rewrite of the practice-question bank, close the remaining open items, then run the full final regression review the original fix-loop plan requires. Follows AGENTS.md (Lead Dev is the only writer; Teacher validates content; user approves each work package)."
todos:
  - id: approve-plan
    content: User approves this plan (editing this file is not approval)
    status: completed
  - id: phase-0-baseline
    content: Git baseline commit (with user OK), DB fingerprint, server PIDs, register reconciled
    status: completed
  - id: phase-1-decisions
    content: User decisions D1–D6 recorded
    status: completed
  - id: phase-2-reverify
    content: Team re-verifies every change made after round-final (R1–R6)
    status: completed
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

## Amendment 1 (2026-09-26): new lab issues N1–N4

**Approval.** You asked Lead Dev to "run the next steps" (log the GL-08 bug, re-check GL-17/GL-08, commit and review O1–O10, fix the empty cleanup values). This amendment is the written plan for those fixes. AGENTS.md says Teacher validates it before any implementation. The Teacher and AWS verdicts are recorded below.

Each issue was validated by Lead Dev against commit `8789bf5`, using read-only scripts over `content/labs/*.json`.

| ID | Issue | Evidence | Severity | Fix |
|---|---|---|---|---|
| N1 | GL-08 creates the internet-facing ALB with one subnet. AWS requires subnets in at least two Availability Zones, so `create-load-balancer` fails (AWS round-1, not logged at the time) | `gl-08.json` s06 creates only `$SubnetPub` (us-east-1a); s09 passes `--subnets $SubnetPub` | Medium | s06: add `$SubnetPub2` (10.80.2.0/24, us-east-1b) and associate it with the public route table (`$RtAssocPub2`). s09: pass `--subnets $SubnetPub $SubnetPub2`. Teardown: disassociate `$RtAssocPub2` and delete `$SubnetPub2` before the route table and VPC. Tag both subnets `LabId=gl-08` |
| N2a | GL-01 cleanup sets `$BoundaryArn = $null` and then runs `delete-policy --policy-arn $BoundaryArn`. The boundary policy is never deleted, and the value from s06 is wiped | `gl-01.json` teardown lines 1 and 7 | Medium | Replace with `$AccountId = aws sts get-caller-identity --query Account --output text` and `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"` |
| N2b | 10 unguided labs (UL-05, 06, 07, 08, 09, 10, 11, 12, 14, 16) start Stop charges with `$X = $null` for every resource. That wipes the IDs the learner set while building, so every guarded delete is skipped and nothing is deleted. UL-06 and UL-08 include hourly NAT and ALB | Script: every teardown var in these labs is reset to `$null` before use | **High** (cost risk; only the tag-search check would catch leftovers) | Remove all `= $null` lines. Start each UL teardown with one PowerShell comment naming the variables it uses: `# Uses the IDs you set while building: $VpcId, $SubnetPub, …. Set any you named differently. Unset ones are skipped.` |
| N2c | GL-06 and GL-08 carry `$null` lines plus guarded deletes for resources those labs never create. GL-06 repeats the NAT and EIP lines twice | Script: 10 dead lines in GL-06 and 11 in GL-08 | Low | Delete the dead lines and the duplicate NAT/EIP pair. Keep only deletes for resources the lab's steps create |
| N3 | UL-07 is the EFS lab, but its cleanup never deletes the EFS mount targets or file system | `ul-07.json` teardown has only instance, volume and snapshot | Medium | Add `$FileSystemId` deletes: list and delete the mount targets, wait until none remain, then run `delete-file-system`. All of it goes before the instance and security group, following the criteria order |
| N4 | Start here lists a lesson's drills by raw question ID, not by question text (FS-R2-R1-001) | `StartHereTab.tsx:224` | Low | Logged only. Fixed together with Q1, when stems change |

**Scanner hardening** (`scripts/scan_lab_placeholders.py`), which closes the loophole behind N2:
- Count as "assigned" only variables set in the lab's **steps**, never in the teardown itself.
- Fail on any `= $null` line in a teardown.
- For `ul-*` labs, every teardown variable must be named in the leading `# Uses …` comment.

**Files touched:**
- `content/labs/{gl-01,gl-06,gl-08}.json`
- `content/labs/ul-{05,06,07,08,09,10,11,12,14,16}.json`
- `scripts/scan_lab_placeholders.py`
- records: `issue-register.md`, `docs/change-requests.md` (CR-0017), `docs/status.md`

**Risks:**
- A wrong CLI flag or delete order. Mitigation: the AWS reviewer checks every changed command against the AWS CLI reference.
- The comment-header approach relies on learners keeping their shell variables. Mitigation: the tag-search verification step stays, and the comment says what to do if the shell was closed.

**Tests:** scanner PASS on all 42 labs; content lint PASS; Django tests; a Lead Dev script showing zero `= $null` teardown lines; AWS and Student round-2 review.

**Learning content affected:** yes (labs). It needs Teacher validation before and after.

**Pre-implementation verdicts (2026-09-26):**
- Teacher: **concerns** (`reports/fix-loop-r2/amendment-1/TEACHER.md`)
- AWS: **concerns** (`reports/fix-loop-r2/amendment-1/AWS.md`)

Both confirm that N1–N3 are real and approve the N1, N2a, N2c and N3 fixes. Both found that the original design was not enough, and they found more cleanup bugs. The revised design below replaces the table above. **It needs your approval before any lab file changes**, because it is much larger than the original "fix the empty cleanup values" step.

### Amendment 1, revised: every lab's Stop charges must run and delete what the lab creates

| ID | Issue | Labs | Sev | Fix (commands taken from the AWS report, doc-cited) |
|---|---|---|---|---|
| N1 | Internet-facing ALB with one subnet | GL-08, **UL-08** | Medium | Add a second tagged public subnet in us-east-1b and associate it with the public route table; pass `--subnets $SubnetPub $SubnetPub2`; add `aws elbv2 wait target-in-service` before the HTTP check. Teardown order: ALB (and wait) → target group → instance → both route-table associations → route table → both subnets → IGW → SG → VPC. Update s06 success text and s13 order text |
| N2a | `$BoundaryArn = $null` before `delete-policy` | GL-01 | Medium | `$AccountId = aws sts get-caller-identity --query Account --output text`; `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"` |
| N2b | UL teardowns reset every ID to `$null`, so nothing is deleted | UL-05, 06, 07, 08, 09, 10, 11, 12, 14, 16 | **High** | Remove the `$null` lines. Wrap **every** UL delete in `if ($Var) { … }`. Start the teardown with one comment naming only that lab's real resource variables, plus how to recover a lost ID: `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=ul-NN` |
| N2c | Dead guarded lines and duplicate NAT/EIP pairs | GL-06, GL-08, UL-06, UL-08 | Low | Delete the dead and duplicate lines (line list in the AWS report) |
| N3 | EFS never deleted | UL-07 | Medium | Delete the mount targets → poll `describe-mount-targets` until 0 (EFS has no waiter) → `delete-file-system`, then the mount-target SG before the instance SG. Add an unmount note and a `describe-file-systems` check |
| N6 | `-ErrorAction SilentlyContinue` appended to native `aws` commands; the CLI rejects it, so the delete never runs | 16 lines in 12 labs (incl. GL-19 EKS, GL-21 ElastiCache, UL-14 RDS, UL-09 ASG) | **High** | Remove the flag from every `aws` line (keep it on real cmdlets such as `Remove-Item`). Add the missing waits: `eks wait nodegroup-deleted` / `cluster-deleted`, `elasticache wait cache-cluster-deleted`, `rds wait db-instance-deleted` before subnet-group deletes |
| N7 | UL teardowns hard-code guided names `workbook-glNN` that UL learners never create | UL-03, 04, 10, 11, 12, 13, 15, 17, 18, 19, 21 | Medium | Add an acceptance criterion "Name resources `workbook-ulNN`" and use those names, or variables, in the teardown |
| T1 | UL teardowns that don't match their own criteria | UL-05 (2 of 4 subnets), UL-08 (no WAF web ACL delete), UL-10 (no DLQ or event mapping delete), UL-14 (no restored-copy or snapshot delete, no waits), UL-16 (zone records not deleted → HostedZoneNotEmpty) | High (UL-08, UL-14), Medium (rest) | Add the missing deletes and waits in dependency order |
| T2 | EKS extras never deleted, so delete-cluster fails | UL-19 | **High** | `delete-nodegroup` + `wait nodegroup-deleted` and/or `delete-fargate-profile` + `wait fargate-profile-deleted`, then `delete-cluster` + `wait cluster-deleted` |
| T3 | Missing deletes | UL-03 (GuardDuty detector), UL-04 (KMS key deletion not scheduled; secret and SSM parameter kept), GL-16 (record not deleted → zone delete fails) | Medium | Add `guardduty delete-detector`, `kms schedule-key-deletion --pending-window-in-days 7`, `secretsmanager delete-secret`, `ssm delete-parameter`, and a Route 53 DELETE change batch before the zone delete |
| T4 | Variables used but never set | GL-14 (`$DbId`, `$SubnetGroup`) | Medium | Set them in s06 |
| T5 | PowerShell parse error in a lab step: `"…:$AccountId:$ApiId/*/*"` (Lead Dev reproduced "Variable reference is not valid") | GL-11 s08 | Medium | `"arn:aws:execute-api:us-east-1:$($AccountId):$($ApiId)/*/*"` |
| T6 | Low polish | GL-08 (untagged target group, subnet and route table; `curl` is an alias for Invoke-WebRequest in PS 5.1, reproduced → use `curl.exe`), GL-10 (unsubscribe line gets tab-joined ARNs), UL-18 (no running-task check before delete-cluster) | Low | As listed in the AWS report |
| N5 | Scanner loopholes | `scripts/scan_lab_placeholders.py` | High (it hid all of the above) | Rules: assignments count only from steps **or** from teardown lookup lines (`$X = aws …` or a string built from other vars), never `= $null`; UL labs are checked against their `# Uses` comment; fail on `-ErrorAction` in an `aws` line, `workbook-gl` names in `ul-*` teardowns, unguarded UL deletes, and duplicate teardown lines; per-lab whitelist instead of a global one. Add a small fixture test for the scanner |

**Files:**
- about 26 files in `content/labs/*.json`
- `scripts/scan_lab_placeholders.py`
- a new `backend/workbook/tests/test_lab_scan.py`, or `tests/unit/`
- records

**Method:** AWS reviewer's exact commands; every changed command checked against the CLI reference; batches by lab group, one commit each.

**Review:** AWS and Student check every changed lab (Student follows the Stop charges text literally); Teacher checks wording and ordering against each lab's "Order the deletes" step; Python checks the scanner and its test.

**Learning content affected:** yes.

**Status: approved by you on 2026-09-26, all items.** On the same day you also approved:
- fixing FS-R2-2-001 and FS-R2-2-002 now (within O6/R5);
- drafting the Q1 pilot batch (SAA task 1.1) for review.

The Teacher re-validates the finished lab changes (AGENTS.md "after implementation").

## Learning content impact

Yes, and it is large. Q1 rewrites most of the SAA and TF question bank, and O6–O9 plus R1, R2 and R6 change labs and lessons. Every content WP needs a Teacher verdict before your approval and again after the fix.
