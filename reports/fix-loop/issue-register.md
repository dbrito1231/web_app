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
| D6 | Dated prices and templated design exercises | Decided 2026-09-25: fix them. Work not started |
| D7 | Lab scanner skips `gl-01` | Done. Scanner includes GL-01. `PASS 42 labs scanned` |
