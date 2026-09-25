# Workbook Multi-Agent Evaluation Summary

**Date:** 2026-09-25  
**Scope:** SAA-C03 + Terraform 004 local workbook (`web_app`)  
**Mode:** Read-only app; evidence under `reports/`; DB restored after eval.

## Executive summary

The workbook delivers a coherent four-tab learning shell, broad content coverage (429 drills, 42 labs, 23 lessons), and passing structural lint/Terraform fixture checks. Three **Confirmed High** app/content themes dominate: (1) **exam drill integrity** — rationale on question GET (XF-001); (2) **lesson ↔ drill linkage** — dot/hyphen mismatch on **20** SAA lessons (Teacher **F-01**, XF-010); (3) **assessment quality** — ~227 template MC stems (Teacher **F-02**, XF-003). **Confirmed High lab commands** (post–CR-0005): GL-08 Linux user data (AWS-001), GL-05 NACL semantics (AWS-002), GL-17 missing Athena DDL (AWS-003). **Confirmed Medium:** GL-07/UL-07 EFS gap (AWS-004), teardown scanner gap + meg-scripts (AWS-005). CR-0005: placeholder scan PASS; **AWS + Teacher** validation **concerns** — not full sign-off.

## Finding counts

| Severity | Count |
|----------|------:|
| Critical | 0 |
| High | 8 (XF-001, F-01, F-02, AWS-001–003, ITMGR-001, ITMGR-005 org/policy) |
| Medium | 9 |
| Low | 3 |
| Informational | 1 |

| Confidence | Count |
|------------|------:|
| Confirmed | 5 |
| Likely | 7 |
| Needs Verification | 3 |
| Subjective Observation | 3 |

## Top confirmed issues

1. **XF-001 / PYTHON-001 / FULLSTACK-001 / ITMGR-001** — Rationale leak on question GET; not audit-grade for L&D attestation (High).
2. **XF-010 / Teacher F-01** — Dotted `drillIds` on 20 SAA lessons vs hyphenated question files (High; CR-0001 regression).
3. **XF-003 / Teacher F-02 / ITMGR-003** — Template MC bank (~227 stems; ~380 longest-choice heuristics) (High).
4. **XF-011 / AWS-001–003** — GL-08 user data, GL-05 NACL, GL-17 Athena sequence (Confirmed High lab).
5. **AWS-004 / AWS-005** — GL-07 EFS gap; teardown var scan no-op (Confirmed Medium).
6. **Teacher F-03–F-06** — GL-20/21 copy, UL preflight, lesson links (Medium).
7. **STUDENT-001** — UL-01 criterion references GL-03 bucket not taught on lesson path (Confirmed Medium).
8. **STUDENT-002** — Permissions boundary in GL-01 not taught in lessons (Confirmed Low).
9. **ITMGR-005 / XF-006** — Live hourly labs; GL-08-style failures increase spend while debugging (organizational High).
10. **ITMGR-004 / XF-007** — Coverage `implemented_unverified` (Medium).
11. **ITMGR-002 / XF-008** — Bootstrap lab load + silent skip (Likely Medium).
12. **FULLSTACK-002 / XF-002**, **XF-009**, **PYTHON-003** — Mock UI, MR count, rationale test (Medium/Likely).

## Agent disagreements preserved

- **UL labs missing `beforeYouStart`:** Teacher F-05 Confirmed Medium vs optional pair-design — add UL preflight or explicit GL link in UI.
- **CR-0005 closure:** Status log says done; Teacher **concerns** + **AWS-005** (scan var check disabled; 16 labs with unset teardown vars) — partial paper verification only (V-01); GL-05/08/17 blockers confirmed without live AWS.
- **Old “AWS-003 teardown” label:** Superseded — finding ID **AWS-003** is now GL-17 Athena DDL (see `03-senior-aws-solutions-architect.md`).

## Strengths

- Locked safety narrative (no app AWS calls, teardown emphasis, GL-01 baseline).
- Content lint PASS; lab placeholder scan PASS; `terraform validate` PASS on GL-20 fixture.
- Honest readiness messaging (no fake pass probability).

## Recommended next actions (product)

1. Strip rationales from public question API; add regression test (PYTHON-003) — **block compliance use until done** (ITMGR-001).
2. **F-01:** Hyphenate `drillIds` on 20 lessons + lint rule (priority; CR-0001 regression).
3. **F-02:** Phased drill rewrite; MCP recheck (`pending_recheck` on 427 items).
4. **AWS-001–003:** Fix GL-08 user data, GL-05 NACL, GL-17 DDL (blocking labs).
5. **AWS-004/005:** GL-07 EFS alignment; enable strict teardown var checks in `scan_lab_placeholders.py`.
6. **F-03/F-04/F-05/F-06:** Teacher lab/lesson fixes (see `02-teacher.md` draft CRs).
7. **STUDENT-001/002:** UL-01 GL-03 prerequisite; teach permissions boundary before GL-01.
8. Corporate rollout: sandbox OU/SCP + billing policy (ITMGR-005); prioritize fixing hourly labs with AWS-001/002 defects.
9. Engineering: bootstrap/lab load, mock UI, MR count, rationale API/test (FULLSTACK/PYTHON items).
10. Transcribe Teacher + AWS draft CRs via approved Lead Dev plan (`02-teacher.md`, `03-senior-aws-solutions-architect.md`).
11. Optional live GL spot-runs (Teacher V-01) for AWS-006/007 after JSON fixes.

## Source reports

- [Student](01-college-it-student.md)
- [Teacher](02-teacher.md)
- [AWS Architect](03-senior-aws-solutions-architect.md)
- [IT Manager](04-it-manager.md)
- [Full-Stack](05-senior-fullstack-engineer.md)
- [Python](06-senior-python-developer.md)

## Evaluation Integrity

| Check | Result |
|-------|--------|
| DB fingerprint after restore | **Match** — re-restored after [Student](c855fe33-55e1-4480-bcc0-c1f737fbb726) batch (~28 `POST /api/attempts`); fingerprint equals baseline (`eval-baseline/db-fingerprint-after.txt`) |
| Student UI re-review (2026-09-25) | Tab `b56e36`; journeys in `reports/evidence/STUDENT/ui-journey/`; **Check answers** clicked for 15+ loads; **0** SQLite rows (Forbidden POST in MCP browser). Prior API-only Student batch **void**. Re-verify 30 persisted attempts in standard Chrome if needed. |
| File manifest diff | **Empty diff** — `manifest-before.txt` equals `manifest-after.txt` (5556 files; excludes `reports/` and `db.sqlite3`) |
| Server PIDs 5173/8000 | **Unchanged** — 28264 (5173), 20200 (8000) |
| Forbidden commands | None (no npm build/dev, migrate, terraform apply, git writes) |
| MCP | Terraform provider version 6.66.0 OK; AWS Knowledge MCP used for S3 bucket doc sample |
| Commands run | `content_lint.py`, `scan_lab_placeholders.py`, `manage.py test workbook`, `terraform fmt -check` + `validate`, `eslint src`, GET APIs |
