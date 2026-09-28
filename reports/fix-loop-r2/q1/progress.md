# Q1 lesson-first rewrite: progress tracker

Plan: `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`, Amendment 3. The rules and the pipeline are defined there. Update this file after every step.

Pipeline per task:
1. **LW:** lesson written (Sonnet writer).
2. **LR:** lesson reviewed by Teacher + AWS (for TF lessons, the Teacher checks against HashiCorp docs and AWS checks only the AWS-provider parts).
3. **LF:** lesson fixes, repeated until both approve.
4. **QW:** questions written (tasks with more than 25 questions are split into two writer agents).
5. **QR:** questions reviewed by Teacher + AWS + Student (Student fairness must be at least 90%).
6. **QF:** question fixes, repeated until all three approve.
7. **Closed:** DB restored, register updated.

| # | Lesson | Questions | LW | LR | LF | QW | QR | QF | Closed |
|---|---|---:|---|---|---|---|---|---|---|
| 0 | lesson-1-1 (pilot) | 19 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ 2026-09-26 |
| 1 | lesson-1-2 | 16 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ 2026-09-26 |
| 2 | lesson-1-3 | 20 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ 2026-09-26 |
| 3 | lesson-2-1 | 35 | ✔ | ✔ | ✔ | ✔ | ✔ AWS 35/35, Teacher close, Student 9/10 | ✔ (3 key-wording trims after Student note; Teacher approved 4e58e56) | ✔ 2026-09-26 |
| 4 | lesson-2-2 | 32 | ✔ | ✔ | ✔ | ✔ | ✔ AWS (after s07-mc fix), Teacher close, Student 10/10 | ✔ | ✔ 2026-09-26 |
| 5 | lesson-3-1 | 8 | ✔ | ✔ | ✔ | ✔ | ✔ AWS (1 diversity fix), Teacher close, Student packet 7/7 | ✔ | ✔ 2026-09-26 |
| 6 | lesson-3-2 | 16 | ✔ | ✔ | ✔ | ✔ | ✔ AWS (1 diversity fix + K05 timeout sentence), Teacher close, Student packet 8/8 | ✔ | ✔ 2026-09-26 |
| 7 | lesson-3-3 | 21 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 8/8 blind | ✔ (AWS-Q33-001, TEACHER-Q33-001) | ✔ 2026-09-26 |
| 8 | lesson-3-4 | 13 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 13/13 | ✔ (AWS-Q34-001–003, TEACHER-Q34-001) | ✔ 2026-09-26 |
| 9 | lesson-3-5 | 24 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 24/24 | ✔ (DataBrew diversity, TEACHER-Q35-001) | ✔ 2026-09-26 |
| 10 | lesson-4-1 | 35 | ✔ | ✔ | ✔ | ✔ (2 writers) | ✔ AWS close, Teacher close, Student packet 35/35 | ✔ (AWS-Q41-001/002) | ✔ 2026-09-26 |
| 11 | lesson-4-2 | 24 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 24/24 | ✔ (AWS-Q42-001, TEACHER-Q42-001–003; Lead Dev pre-check: recycled Outposts phrasing + s06-mr strawman) | ✔ 2026-09-26 |
| 12 | lesson-4-3 | 22 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 22/22 | ✔ (TEACHER-Q43-001–004; Lead Dev: read replica 6→3 and snapshot 4→3 after fixing a plural-matching bug in distractor_type_audit.py) | ✔ 2026-09-26 |
| 13 | lesson-4-4 | 23 | ✔ | ✔ | ✔ | ✔ | ✔ AWS close, Teacher close, Student packet 23/23 | ✔ (AWS-L44-001–003, TEACHER-L44-001–003 + 2 lesson additions; AWS-Q44-001; TEACHER-Q44-001–003 stem echoes; Lead Dev: s06-mr strawman + absolutism tell, 2 avoidable stem leaks after Student) | ✔ 2026-09-27 |
| 14 | lesson-tf-g1 | 9 | ✔ | ✔ | ✔ | ✔ | ✔ Tech close, Teacher close, Student packet 9/9 | ✔ (AWS-Qg1-001/TEACHER-Qg1-001 false CloudFormation serial claim; Lead Dev pre-check rejected 9 caricature distractors) | ✔ 2026-09-27 |
| 15 | lesson-tf-g2 | 12 | ✔ | ✔ | ✔ | ✔ | ✔ Tech close, Teacher close, Student packet 12/12 | ✔ (TEACHER-Lg2-001–003, AWS-Lg2-001/002, TEACHER-Qg2-001 over-trimmed quote, AWS-Qg2-001 -upgrade untaught, exam tip + claim row 8b/8c) | ✔ 2026-09-27 |
| 16 | lesson-tf-g3 | 21 | ✔ | ✔ | ✔ | ✔ | ✔ Tech close, Teacher close, Student packet 21/21 | ✔ (AWS-Lg3-001 fabricated quote, AWS-Lg3-002 version boundary, TEACHER-Lg3-001–004, TEACHER-Qg3-001; Lead Dev pre-check: 3f dependents contradiction, 2 self-explaining choices, 2 match-the-flag reworks; 3 freebie distractors after Student) | ✔ 2026-09-27 |
| 17 | lesson-tf-g4 | 24 | ✔ | ✔ | ✔ | ✔ | ✔ Tech close, Teacher close, Student packet 24/24 | ✔ (AWS-Lg4-001/002, TEACHER-Lg4-001/002; Lead Dev pre-check 12 incl. 10 rationales with shifted letter refs, a sort() distractor that worked, stale nonsensitive() claim; AWS-Qg4-001–010, AWS-Lg4-013, TEACHER-Qg4-001–011; three fix passes, round 2c) | ✔ 2026-09-28 |
| 18 | lesson-tf-g5 | 12 | | | | | | | |
| 19 | lesson-tf-g6 | 12 | | | | | | | |
| 20 | lesson-tf-g7 | 9 | | | | | | | |
| 21 | lesson-tf-g8 | 20 | | | | | | | |

Other approved work running alongside:
- **O9** (lab sidecar templates and lab-specific s12–s15 steps). Status: **closed 2026-09-26** (AWS: AWS-O9.md, AWS-O9-recheck.md; Student: STUDENT-O9.md, STUDENT-O9-recheck.md).
