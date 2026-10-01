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
| ISS-080 | ITMGR-205, AWS-210, TEACHER-211 | WP11 | **Closed 2026-09-30** | Sandbox note Closed (IT Manager Gone). D6 fix complete (plan `d6_iss080_pricing_and_exercises_20260929`). **AWS-210:** 16 hourly labs carry a dated us-east-1 cost basis, with the 24 h figure in the stop panel. NAT, WAF, RDS storage, EFS and CloudWatch alarm rates are still unverified and marked in the labs. **TEACHER-211:** all 60 exercises are rewritten as case studies with stakeholder constraints and outcome rubrics (0 template scenarios left). The exercise card now shows constraints, deliverable and rubric. Tech and Teacher closed every batch; Student 12/12 designs match, fair | CR-0016 |
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
| R1 | GL-17 DDL matches the CSV, the query, and cleanup | Closed. Teacher recheck Pass (2026-09-25): real newline CSV; Athena drop table then drop database in s09 and teardown, before S3 deletes |
| R2 | GL-08 `user-data.sh` is LF, no BOM, and readable on the Labs screen | Closed. Teacher recheck Pass (2026-09-25): `WriteAllText` with UTF-8 no BOM and `` `n ``; `Set-Content` gone; still `file://user-data.sh` |
| R3 | Eight stem openings | Not a fix. Teacher and Student agree. Covered by Q1 |
| R4 | All 23 Start here titles; keyboard and screen-reader labels | Pass. Full-Stack and Student agree. Closed |
| R5 | `/exam?q=` opens that question; a bad id is clear; back works | Agreed Fail (Full-Stack, Student). Fixed after review: unknown id shows a message; “Back to Start here” when opened with `?q=`. Awaiting a new review |
| R6 | Each domain-4 bullet cites the official doc for its topic | Fail. AWS and Teacher agree. Fix not started |

## Round-2 open items (not started)

| ID | Issue | WP | Status |
|----|-------|----|--------|
| O1 | Lab details and header progress (FS-FINAL-001) | WP8b | Fixed. Header uses summary step counts (630 steps, 42 labs) before lab bodies load. Labs still load when the Labs tab opens |
| O2 | Lab card accessible name (FS-FINAL-002) | WP8b | Fixed. Card name is `GL-07 details`. Checked in the browser |
| O3 | Tab ARIA: tablist, selected, controls, arrow keys | WP8b | Fixed. ArrowRight moves from Exam drills to Coverage and focuses that tab |
| O4 | Markdown helper misses some lesson and lab constructs | WP8b | Fixed for `###` and `####` headings used in lessons. Checked on lesson 1.1 |
| O5 | Exam layout at 375px | WP8b | Fixed. One column, no horizontal scroll at 375px |
| O6 | Each drill links back to its lesson | WP7b | Fixed. `Study:` link on `q-saa-1-1-k01-mc` opens lesson 1.1 |
| O7 | Each lesson links to its labs and design exercises | WP7b | Fixed. Matched on objective ids. Lab links open `/labs?lab=`. Exercises show on the lesson |
| O8 | GL-07 says EFS but has no EFS steps; GL-21 title says HCP | WP5b | Fixed. GL-07 is “EC2 and EBS” and points at UL-07 for EFS. GL-21 is “ElastiCache tradeoffs” |
| O9 | Missing sidecar templates; s12–s15 boilerplate | WP5b | Reported. Not started |
| O10 | Corrupt content JSON returns a clear JSON 500 | WP9b | Fixed. Loader raises ContentParseError; question GET returns JSON 500. 13 Django tests OK |
| Q1 | Rewrite the practice-question bank | WP4b | Reported. Blocked until the pilot batch is approved |

O1–O8 and O10 were committed on 2026-09-26 (`609182f`, `37e0a95`, `b0ed883`). Team round-2 review is in progress (`reports/fix-loop-r2/round-2/`). None of them is Closed until two roles mark it Gone.

## Amendment 1 items (logged 2026-09-26, CR-0017)

| ID | Issue | Source | Severity | Status |
|----|-------|--------|----------|--------|
| N1 | GL-08 internet-facing ALB created with one subnet; AWS needs two AZs | AWS round-1 new issue (was not logged) | Medium | Valid. Design awaiting Teacher and AWS verdicts |
| N2a | GL-01 teardown sets `$BoundaryArn = $null` before `delete-policy`; the boundary policy is never deleted | Lead Dev script | Medium | Valid. Awaiting verdicts |
| N2b | 10 unguided labs reset every ID to `$null` at the top of Stop charges; nothing gets deleted | Lead Dev script (register ISS-030 residual) | High | Valid. Awaiting verdicts |
| N2c | GL-06/GL-08 dead `$null` and guarded delete lines; GL-06 NAT/EIP lines duplicated | Lead Dev script | Low | Valid. Awaiting verdicts |
| N3 | UL-07 (EFS lab) teardown never deletes EFS | Lead Dev review | Medium | Valid. Awaiting verdicts |
| N4 | Start here lists drills by raw question ID | FS-R2-R1-001 | Low | Valid. Deferred to Q1 |
| N5 | Scanner counts teardown `$null` lines as "assigned" | Lead Dev review | Medium | Valid. Awaiting verdicts |
| N6 | 14 labs append `-ErrorAction SilentlyContinue` to native `aws` commands. PowerShell passes these words to `aws` as arguments (confirmed locally with `cmd /c echo`), so the cleanup command likely fails; this includes the GL-19 EKS and GL-21 ElastiCache deletes | Lead Dev review | High (Likely until AWS confirms CLI behaviour) | Validating (AWS) |
| N7 | 11 unguided labs' teardowns hard-code guided-lab names (`workbook-glNN`) | Lead Dev review | Medium | Valid (AWS confirmed). Revised design awaiting user approval |
| T1 | UL-05/08/10/14/16 teardowns miss resources their criteria create | Teacher + AWS amendment review | High/Medium | Valid. Awaiting user approval |
| T2 | UL-19 never deletes node group / Fargate profile; cluster delete fails | AWS amendment review | High | Valid. Awaiting user approval |
| T3 | UL-03 GuardDuty, UL-04 KMS/secret/SSM, GL-16 Route 53 record not deleted | AWS amendment review | Medium | Valid. Awaiting user approval |
| T4 | GL-14 `$DbId` / `$SubnetGroup` never set | AWS amendment review | Medium | Valid. Awaiting user approval |
| T5 | GL-11 s08 `"…:$AccountId:$ApiId/*/*"` is a PowerShell parse error | AWS (Needs Verification) → Lead Dev reproduced | Medium | Valid. Awaiting user approval |
| T6 | GL-08 untagged resources and `curl` alias; GL-10 unsubscribe line; UL-18 task check | AWS amendment review | Low | Valid. Awaiting user approval |

| N8 | **152 of 429 rationales refer to choices by letter ("A and B are sound…")**, and the letters don't match the key. Pass-1 rotated the keys without updating the rationales. The UI also shuffles choice order (`ExamDrillsTab.tsx` `shuffle`), so any letter reference is wrong for learners | Lead Dev script 2026-09-26 | **High** (explanations teach the wrong answer) | Valid. Q1 pilot rule: no letter references. Remaining batches fix it as they are rewritten. An interim fix for the rest needs your decision |
| N9 | Exam tab renders all ~430 drill cards above the question; page is ~117,000 px tall in a narrow window | Lead Dev browser check | Low | Reported (FS-R2-2-001 fix scrolls to the question; layout itself unchanged) |

FS-R2-2-001 and FS-R2-2-002 fixed in `740efd0`; awaiting re-review. Scanner rewrite N5 is in `bbb05de`, with 6 fixture tests.

N6 is now Valid and High: the AWS reviewer confirmed with the CLI docs that AWS CLI v2 rejects unknown arguments.

## Round-2 team review results so far (2026-09-26)

**Full-Stack** (`reports/fix-loop-r2/round-2/FULLSTACK.md`):
- Gone: O1, O2, O3, O4, O5, O7, R5.
- **Still present:** O6. The Study link is missing on 193 of 429 drills, including all MR variants and all 74 Terraform questions, because it only uses lesson `drillIds`.
- Each item still needs a second role (Student) before it closes.
- No drill was submitted, so the save flow was not re-tested this round.

New items from Full-Stack:

| ID | Issue | Sev | Status |
|----|-------|-----|--------|
| FS-R2-2-001 | `/exam?q=` opens the question far down the page with no scroll or focus, so the link looks broken | Medium | Valid (reported). Fix is in approved O6/R5 scope |
| FS-R2-2-002 | Study link only uses lesson `drillIds`, so 193 drills lack it (same root as O6) | Medium | Valid. Fix is in O6 scope: fall back to objective-id match |
| FS-R2-2-003 | Sticky header covers the linked lab card head | Low | Reported |
| FS-R2-2-004 | Lab filter stays after returning to plain `/labs` | Low | Reported |
| FS-R2-2-005 | Start here scrolls sideways at 375px | Low | Reported |
| FS-R2-2-006 | Lesson picker doesn't update `?lesson=` | Low | Reported |
| FS-R2-2-007 | `?q=` not updated after picking another drill | Low | Reported |
| FS-R2-2-008 | Import/Reset confirmation lost after reload (code reading only) | Low | Reported (Likely) |

**Python** (`reports/fix-loop-r2/round-2/PYTHON.md`): PY-R2-2-003/004/005 are folded into N5 (scanner). PY-R2-2-006/008/009/010 are Low and reported.

**ISS-060 / O10:** Python round-2 found non-UTF-8 and wrong-type files still gave an HTML 500 (PY-R2-2-001/002). Fixed in `1c68079` with real-file route tests. Awaiting Python re-check.

## Decisions

| ID | Decision | Status |
|----|----------|--------|
| D1 | Git baseline | Decided 2026-09-25: commit on `main`, not `fix/run2-round2` |
| D2 | WP4–WP11 after the fact | Decided 2026-09-25: approve as-is. See `reports/fix-loop-r2/retro-approval.md` |
| D3 | ISS-061 debug mode and local secret key | Decided 2026-09-25: accept for this local-only app |
| D4 | ISS-081 audit-grade manager metrics | Decided 2026-09-25: leave it out |
| D5 | ISS-090 live AWS lab runs | Decided 2026-09-25: paper checks only |
| D6 | Dated prices and templated design exercises | Decided 2026-09-25: fix them. **Done 2026-09-30.** Part A closed 2026-09-29; Part B batches 1–3 closed; Student fair |
| D7 | Lab scanner skips `gl-01` | Done. Scanner includes GL-01. `PASS 42 labs scanned` |

## Round 3 results (2026-09-26)

Reports: `reports/fix-loop-r2/round-3/` (AWS, Teacher, Student, Python, Full-Stack) and `reports/fix-loop-r2/q1-pilot/` (AWS, Teacher, Student). DB restored to baseline after the round (fingerprint `930f0e72…` matches; 8 attempt rows from reviewer drills removed).

### Closed this round (original reporter + a second role marked Gone)

| ID | Gone by |
|----|---------|
| N1, N2a, N2b, N2c, N3, N6, N7, T1–T6 (lab cleanup, CR-0017) | AWS; Teacher (approve on all 12 GL and most UL); Student (7 labs followed) |
| R1 GL-17, R2 GL-08 | AWS, Student |
| N5 scanner loophole, PY-R2-2-001/002/003/004/005/007 | Python; AWS (scanner PASS on 42 labs) |
| O1, O5, O7, R5 | Full-Stack (round 2), Student |
| O6 / FS-R2-2-002 Study link (429/429 drills) | Full-Stack, Student |

### Still open, or new

| ID | Issue | Sev | Source |
|----|-------|-----|--------|
| L1 | **Lessons don't teach.** SAA lessons are ~50% boilerplate plus the objective text; Terraform lessons are 96–242 words, mostly boilerplate. No pilot question passes teach-before-test | **High** | Teacher pilot T1; Lead Dev measured all 23 lessons |
| N8 | 133 rationales outside the pilot still name wrong letters | **High** | Lead Dev (pilot fixed 19) |
| FS-R3-001 | `?q=` / card scroll: 80px margin < wrapped header (115px at 1024, 176px at 375), so the heading is hidden | Medium | Full-Stack |
| AWS-R3-002 | GL-14/19/21 subnet lookup returns one tab-joined string; subnet group / cluster create fails | Medium | AWS (reproduced in PS 5.1) |
| TEACHER-R3-001 | UL-15 duplicate criterion; CloudTrail criterion lost | Medium | Teacher, AWS |
| TEACHER-R3-002 | UL-01 teardown policy names not in criteria | Medium | Teacher |
| TEACHER-R3-003 | UL-02 `$Bucket` comment contradicts next line; name not in criteria | Medium | Teacher |
| PY-R3-002/003 | Scanner still foolable (text-only guard check; `''`/`$NULL` resets; empty teardown) | Medium | Python |
| Q1-T2 | `de-federation` exercise lacks SAML / AD FS / AD Connector / Identity Center | Medium | Teacher pilot |
| Q1-T3 | Pilot fixes: k04-mr (non-existent features), s02-mr (key looks already done), s06-mr (choice cross-reference, retired Simple AD) | Low | Teacher pilot |
| Q1-T4 | Lesson 1.1 `drillIds` omit the 8 MR questions | Low | Teacher, Student pilot |
| Q1-M | Distractor reuse ("IAM user with keys" 8/19, "boundary" 6/19) | Low | Teacher pilot |
| AWS-R3-001 | `| [0]` lookups with text output per page (UL-10/11/12/17) | Low | AWS |
| AWS-R3 Lows | GL-17 async DROP race; GL-19 us-east-1e subnets; GL-19 panel SG wording; UL-04 C16 vs pending-deletion key; UL-16 default VPC; UL-09 `None`; UL-08/11 `curl`; UL-18 untagged SG lookup | Low | AWS |
| TEACHER-R3-004…015 | Wording, teachability, criterion-duplication nits across UL labs | Low | Teacher |
| STUDENT-R3-004 | UL-07/UL-08 lack the `workbook-ulNN` naming criterion | Low | Student |
| FS-R3-002 | Clicking the selected card leaves the scroll flag set; next module click jumps | Low | Full-Stack |
| FS-R2-2-003…008, FS-R3-003/004 | Older screen Lows and notes | Low / Info | Full-Stack |
| PY-R3-001, 004–006 | Inner-shape HTML 500; scanner case and false-positive gaps | Low | Python |

Pilot verdicts: AWS **approve** (19/19 exam-realistic and correct); Student **approve** (7/7 fair, 7/7 correct); Teacher **concerns** (16 approve, 3 small fixes, and lessons don't teach).

## Status after round 6 (2026-09-26)

Rule: an item closes only when its original reporter and a second role mark it Gone. Every closure below meets that. Rows above keep their history; this section is the current state.

### Closed

| Area | Items | Closed by |
|---|---|---|
| D6-FU | Lesson follow-ups found during D6 (none blocking): 4.4 K05, both tunnels of one VPN connection carry traffic under ECMP (Student, E4); 3.3 S01, "raise an alarm on the replica-lag metric" (TEACHER-DE2-003, optional); 4.4, Regional NAT gateway (AWS-DE3-015, optional); 4.2-s05 r7 sets only a minimum (AWS-DE3-021, optional). Also CR-0019 (Glue for Ray) | Low | Final sitting |
| Saves, explanations, lesson-drill links | ISS-001, 002, 003, 004 | earlier rounds (see above) |
| Lab cleanup (CR-0017, Amendments 1 and 2) | N1, N2a–c, N3, N5, N6, N7, T1–T6, R1, R2, AWS-R3-001–011, AWS-R4L-001–006, TEACHER-R3-001–015, STUDENT-R3-004, STUDENT-R4-001–004, STUDENT-R5-001 | AWS (`round-5/AWS-labs.md`, `round-6/AWS-ul11.md`) + Student (`round-5/STUDENT.md`) |
| Screens | O1–O7, R4, R5, FS-FINAL-001/002, FS-R2-2-001–008, FS-R3-001–004, FS-R4-001–005 | Full-Stack (`round-5/FULLSTACK.md`) + Student (`round-5/STUDENT.md`) |
| Backend robustness | O10, ISS-060, PY-R2-2-*, PY-R3-001–006, PY-R4-001–004, 010, 011 | Python (`round-5/PYTHON.md`) + AWS/Teacher (checks pass on all content) |
| Lab scanner (N5 and follow-ups) | "Scanner/loader work: close" | Python round 5 |
| Wrong-letter rationales | N8 (interim fix, 185 files) | Teacher (all 185 by script + 20 read) |
| Lesson 1.1 + SAA task 1.1 questions (Q1 pilot) | L1 for lesson 1.1; Q1-T1–T4; TEACHER-R4-001–008; TEACHER-R5-001–008; AWS-R4-001–009; AWS-R5-001/002 | Teacher, AWS, Student (`round-6/`), fairness 10/10 |
| de-federation exercise | Q1-T2, AWS-R4-009, TEACHER-R4-008 | Teacher + AWS |
| Lesson 1.2 + SAA task 1.2 questions (Q1) | L1 for lesson 1.2; lesson and question findings in `reports/fix-loop-r2/q1/*1-2*` | Teacher, AWS, Student (`fix-loop-r2/q1/`) |
| Lesson 1.3 + SAA task 1.3 questions (Q1) | L1 for lesson 1.3; AWS-L13-001–004; TEACHER-L13-001; TEACHER-Q13-001; AWS-Q13-001 | Teacher + AWS re-checks, Student 10/10 (`fix-loop-r2/q1/`) |
| Lesson 2.1 + SAA task 2.1 questions (Q1) | L1 for lesson 2.1; AWS-L21-*, TEACHER-L21-001–004; LD-Q21-001–003; AWS-Q21-001/002 | AWS 35/35, Teacher close, Student 9/10 (`fix-loop-r2/q1/`) |
| Lesson 2.2 + SAA task 2.2 questions (Q1) | L1 for lesson 2.2; AWS-L22-001–003; TEACHER-L22-001; AWS-Q22-001–003; TEACHER-Q22-001 | AWS, Teacher close, Student 10/10 (`fix-loop-r2/q1/`) |
| Lessons 3.1 + 3.2 and SAA tasks 3.1/3.2 questions (Q1) | L1 for lessons 3.1/3.2; AWS-L31-001–005, TEACHER-L31-001–003; AWS-L32-001–003, TEACHER-L32-001; AWS-Q31-001, AWS-Q32-001 | AWS, Teacher close, Student text packet 15/15 (`fix-loop-r2/q1/`) |
| Lesson 3.3 + SAA task 3.3 questions (Q1) | L1 for lesson 3.3; AWS-L33-001–005, TEACHER-L33-001; AWS-Q33-001/002, TEACHER-Q33-001 | AWS, Teacher close, Student text packet 8/8 (`fix-loop-r2/q1/`) |
| Lesson 3.4 + SAA task 3.4 questions (Q1) | L1 for lesson 3.4; AWS-L34-001, TEACHER-L34-002 (checker fix); AWS-Q34-001–003, TEACHER-Q34-001 | AWS, Teacher close, Student text packet 13/13 (`fix-loop-r2/q1/`) |
| Lesson 3.5 + SAA task 3.5 questions (Q1) | L1 for lesson 3.5; writer diversity fix (DataBrew); TEACHER-Q35-001 | AWS, Teacher close, Student text packet 24/24 (`fix-loop-r2/q1/`) |
| Lesson 4.1 + SAA task 4.1 questions (Q1) | L1 for lesson 4.1; TEACHER-L41-001–003; AWS-Q41-001/002 | AWS, Teacher close, Student text packet 35/35 (`fix-loop-r2/q1/`) |
| Lesson 4.2 + SAA task 4.2 questions (Q1) | L1 for lesson 4.2; AWS-L42-001/002/004, TEACHER-L42-001/002/003/004/006; AWS-Q42-001, TEACHER-Q42-001–003; Lead Dev pre-check (recycled Outposts distractor, s06-mr strawman) | AWS close, Teacher close, Student text packet 24/24 (`fix-loop-r2/q1/`). AWS-L42-003 / TEACHER-L42-005 (`##` lesson title) rejected by Lead Dev and accepted as resolved by both reporters; `RULES.md` amended to document the pattern used by all 22 lessons |
| Lesson 4.3 + SAA task 4.3 questions (Q1) | L1 for lesson 4.3; AWS-L43-001, TEACHER-L43-001/002/003/004; TEACHER-Q43-001 (k07-mc tested S02's engine fact instead of its own K07 migration-type objective, leaving K07 untested), TEACHER-Q43-002/003 (duplicated prose in S02/S05, plus a K05 triple-repeat neither reviewer reported), TEACHER-Q43-004 (s03-mc strawman); Lead Dev pre-check (~24 category-error strawmen, MR key sets); Lead Dev round 2 (distractor_type_audit plural-matching bug hid read replica at 6/22 and snapshot at 4/22, both cut under cap; two k08 snapshot distractors were themselves strawmen) | AWS close, Teacher close, Student text packet 22/22 (`fix-loop-r2/q1/`). Student flagged 9 of 22 stems as keyword-guessable; not reworked, see L1/Q1 note |
| Lesson 4.4 + SAA task 4.4 questions (Q1) | L1 for lesson 4.4; AWS-L44-001/002/003 (citation sourcing), TEACHER-L44-001 (Origin Shield in claim table but not prose) /002/003 + 2 lesson additions; AWS-Q44-001 (CloudFront intro page does not assert the "only" exclusivity); TEACHER-Q44-001/002/003 (stem/key keyword echoes under the new paraphrase rule); Lead Dev (s06-mr strawman + "as the only" tell that all three reviewers passed; two avoidable stem leaks found via the Student) | AWS close, Teacher close, Student text packet 23/23 (`fix-loop-r2/q1/`). First task under the stem-paraphrase rule |
| Terraform g1 + g2 lessons and questions (Q1) | L1 for both lessons; TEACHER-Lg2-001/002/003, AWS-Lg2-001/002 (both reviewers found the same wrong citation URL and named different replacement pages; Lead Dev fetched both and the Teacher's was right); AWS-Qg1-001/TEACHER-Qg1-001 (a distractor claiming native template tools provision serially -- false, CloudFormation parallelises); TEACHER-Qg2-001 (a quote trimmed until it asserted more than its source); AWS-Qg2-001 (a real, true distractor resting on a fact the lesson never taught); Lead Dev pre-check rejected 9 caricature distractors in g1; Student found 2 more in g2 that Lead Dev had noted and not acted on | Tech close, Teacher close, Student text packets 9/9 and 12/12 (`fix-loop-r2/q1/`). First tasks under the stem-echo gate and the split Student count: 0 keyword-guessable defects, 8 structural |
| Terraform g3 lesson and questions (Q1) | L1 for lesson tf-g3; **AWS-Lg3-001 a fabricated quote** -- text presented as verbatim that is not on the cited page, a new defect class for this project; AWS-Lg3-002 version boundary (HashiCorp's own plan and destroy pages contradict each other, 0.15 vs 0.15.2; resolved to 0.15.2 on the authoritative page); TEACHER-Lg3-001–004 including 3f too thin for three questions; TEACHER-Qg3-001 a rationale asserting an untaught fact; Lead Dev pre-check found a contradiction inside the lesson carried into a key (destroy -target dependents), 2 self-explaining choices and 2 match-the-flag reworks; 3 freebie distractors replaced after the Student, 1 of my 4 candidates rejected by the Teacher as a fair distractor | Tech close, Teacher close, Student text packet 21/21 (`fix-loop-r2/q1/`). Split count: 1 keyword-guessable, 10 structural, **no untaught facts** |
| Terraform g4 lesson and questions (Q1) | L1 for lesson tf-g4; AWS-Lg4-001/002 (citation page, version floors), TEACHER-Lg4-001/002; **Lead Dev pre-check found 10 rationales citing choices by letter, shifted after a key-balance reorder, two of them calling a correct key "wrong"**; a `sort()` distractor that was actually a working answer; a `nonsensitive()` rationale true only for v1.2-1.5 (current docs say it is a no-op); `ignore_changes = [all]` invalid syntax; a self-justifying key; duplicate keyed facts on 4a; lesson miscounts (three vs four condition mechanisms; write-only listed as an ephemeral source). Round-2 fixes then introduced an MR distractor off both stem needs and a refutation taught only in the claim table; both caught in round 2b. AWS-Qg4-001-010, AWS-Lg4-013, TEACHER-Qg4-001-011 | Tech close, Teacher close, Student text packet 24/24 (Sonnet). Split count: 0 keyword-guessable, 10 structural, no untaught facts |
| Terraform g5 lesson and questions (Q1) | L1 for lesson tf-g5. **Round 1:** a false cross-reference ("the methods 4c covered") and a branch described as a pin. **Lead Dev pre-check:** `distractor_type_audit` was blind for g5 (no TERMS); once the terms were added it showed one misconception reused in 3 questions and a 5d fact tested in 5a. **Round 2:** a pair tell in 5c-mc2 (only the key said "kept out"); an untaught "apply does not install" fact behind a 5c-mr distractor (fixed with a quoted lesson sentence); a form tell in 5c-mr (only the keys lacked "Running"). The Lead Dev's "version on non-registry errors" was from memory, unsupported by the docs, and not used | Tech close, Teacher close, Student 12/12. Split count: 0 keyword-guessable, 10 structural |
| Terraform g6 lesson and questions (Q1) | L1 for lesson tf-g6. **Round 1:** the `removed` block page contradicts itself (intro vs lifecycle default); the lesson shows the required `lifecycle { destroy = false }` nesting. The 1.7 floor is scoped to remove-and-import. The import block vs command and `moved` vs `state mv` contrasts were missing. **Quote sourcing:** 5 proposed sentences were dropped as unsupported; 3 of them were later found on the import **overview** page, not the command page, and restored with verified rows. **Round 2:** an untaught "one object per run" refutation (6d-mc2) and an untaught locking claim (6a-mc2). **Student:** justification clauses appeared only on distractors (6c-mr, 6c-mc2, 6b-mr, 6d-mr), plus one echo. A repair then introduced a new echo, caught by `stem_echo_check`. A g4 overclaim was found and logged as CR-0021 | Tech close, Teacher close, Student 12/12. Split count: 1 keyword-guessable (fixed), 11 structural |
| Shortest-is-key reopen of 4-3, 4-1, 1-3 (user decision 2026-09-28) | 11 MC keys were conspicuously the shortest option (57/48/45%). They were rebalanced by wording only and are now 29/29/18%. `q1_batch_check` letter-reference check rewritten: it had passed "c is wrong because…" (all 10 tf-g4 shifted-letter rationales) and false-flagged "answer a different question" in 1-3. Reviewer fixes: 4-3 s02 names Aurora PostgreSQL; 4-3 k09 lost the "non-relational" echo; 1-3 s01 lost the "on demand" hint. **Recorded, not fixed:** 3-1 shortest-is-key 60% (5 MC) and 3-5 36%, left closed by the user; 4-3 s04 "column/columnar" stem-key match (the Student's only keyword-guessable stem, a closed task written before the paraphrase rule); 4-1 k05 key is the only option with a "with…" qualifier (mild) | Tech close, Teacher close, Student 15/15 (`fix-loop-r2/q1/reopen-shortest-key-*.md`) |

### Still open

| ID | Item | Sev | Notes |
|---|---|---|---|
| L1 / Q1 | Lessons 4.3–4.4 and TF g1–g8 (10 lessons) not yet closed; ~142 questions still template-style | **High** | Lesson-first method (Amendment 2/3). Tasks 1.1–4.4 and Terraform g1–g3 closed (2026-09-27; budget plan in effect); next: Terraform g4. Open method-wide observation: Students scored 100% on 3.5, 4.1, 4.2 and 4.3, and on 4.3 reported 9 of 22 stems answerable by matching wording between stem and key. Making stems paraphrase rather than reuse lesson keywords would be a RULES change applying from 4.4 onward, not a reopen of closed tasks -- user decision pending |
| ISS-010 | Template question wording | High | Closes as Q1 batches complete |
| O9 | Lab sidecar-file templates missing; repeated s12–s15 boilerplate steps | Medium | **Closed 2026-09-26.** AWS and Student approved, including the follow-up fixes (GL-10 handler, GL-12 logging, step titles) |
| R6 / ISS-070 | Per-bullet official citations in lessons 4.2–4.4; coverage registry `implemented_unverified`; `mcpStatus: pending_recheck` on non-pilot questions | Medium | Folded into the lesson and question rewrites |
| N9 | Exam tab renders all ~430 drill cards above the question | Low | Scroll-to-question works; layout unchanged |
| N4 | Start here lists drills by raw ID | Low | Deferred to Q1 |
| STUDENT-R6 notes | Lesson 1.1 has no in-lesson section links; S06/K04 dense on first read | Low | New, non-blocking |
| PY-R5-001–003 | Scanner bypasses needing deliberate obfuscation (`iex`, aws via variable, Unicode dash) | Low | Python says close is fine; formal won't-fix needs your approval |
| PY-R4-005/008/009, PY-R5-004/005 | Documented KISS trade-offs / info | Low/Info | As above |
| Lab cosmetic | UL-21 comment dash encoding; UL-02 bucket-name echo quirk | Info | From AWS round 5 |

DB fingerprint after round 6: `930f0e72…` (matches baseline).
