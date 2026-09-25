# Workbook Multi-Agent Evaluation Summary (run-2)

**Date:** 2026-09-25  
**Scope:** SAA-C03 + Terraform 004 local workbook (`web_app`)  
**Plan:** `.cursor/plans/eval_redo_extensive_20260925.plan.md`  
**Mode:** Read-only app (no fixes); paper-feedback after Gate 0; DB restored.

## Executive summary

**Corporate training (strict IT Manager pass):** **No-Go** for mandatory completion tracking and compliance-style drill reporting until **ITMGR-230** and **ITMGR-201** are fixed; **Conditional Go** for optional sandbox-governed self-study after CSRF fix (see `reports/04-it-manager.md`).

Run-2 re-verified the workbook with **Gate 0** evidence: **POST `/api/attempts` and lab checkpoints fail with Django CSRF origin rejection** (`CSRF_TRUSTED_ORIGINS` missing). That is a **Critical** blocker for progress, UI feedback, and manager attestation (**FULLSTACK-230**, **PYTHON-230**, **ITMGR-230**). Separately, **GET question payloads still leak rationales** (**FULLSTACK-201 / PYTHON-201**). Content themes from run-1 largely hold after re-check: **13** (not 20) SAA lessons with broken `drillIds` linkage (**Teacher F-201**), template MC bank (**F-202**), and confirmed lab command issues (**AWS-201–203**). **Strict Phase 3–5 complete:** six role reports (Teacher 97 EV / 26 TF doc lookups; Student 60 paper drills; AWS 42 lab command rows / 52 doc lookups), Round B + `group-discussion.md` + `revalidation.md`. **Phase 4 gate:** **PASS** (`report-gate-run2.txt`). — see `reports/evidence/report-gate-run2.txt`. Six Phase 3 role agents + paper-feedback drill log (`reports/evidence/STUDENT/paper-drill-log.md`, 60 IDs) completed in strict follow-up.

## Finding counts

Counts copied from `reports/evidence/summary-counts.json` (script-computed).

| Severity | Count |
|----------|------:|
| Critical | 3 |
| High | 10 |
| Medium | 27 |
| Low | 17 |
| Informational | 5 |

| Confidence | Count |
|------------|------:|
| Confirmed | 23 |
| Likely | 25 |
| Needs Verification | 7 |
| Subjective Observation | 4 |
| Unknown (parser) | 3 |

**Total findings parsed:** 62

## Top confirmed issues

1. **FULLSTACK-230 / PYTHON-230 / ITMGR-230** — CSRF trusted-origin failure blocks all learner POSTs (Critical; Gate 0).
2. **FULLSTACK-201 / PYTHON-201** — Rationale on question GET before submit (High).
3. **Teacher F-201** — Dot/hyphen `drillIds` mismatch on **13** SAA lessons (High; count from `lesson-drillids-run2.md`).
4. **Teacher F-202** — Template MC stems (~227 cluster; scan heuristics).
5. **AWS-201–203** — GL-08 user data, GL-05 NACL, GL-17 Athena sequence (High lab commands).
6. **AWS-204–205** — GL-07 EFS gap; teardown var scan gaps (Medium).
7. **ITMGR-201** — Metrics not audit-grade even after save fix (High; rationale leak).

## Changes since run 1

| ID | Change |
|----|--------|
| FULLSTACK-230, PYTHON-230, ITMGR-230 | **New** Critical — save failure root cause confirmed with network HTML (run-1 blamed browser). |
| Teacher F-201 / XF-210 | **Re-rated scope:** 13 lessons with missing drill files (run-1 summary incorrectly said 20). |
| Summary counts | **Computed** from reports via `summary-counts.json` (run-1 hand counts wrong). |
| Student drills | **Paper-feedback mode** — no UI scoring until CSRF fix. |
| Run-1 reports | Archived under `reports/archive/run-1/`; hypotheses re-used only with `Prior:` where noted. |

## Agent disagreements preserved

See `reports/discussion/group-discussion.md` (Round A remapped to 2xx IDs). UL `beforeYouStart` optional vs required; CR-0005 partial verification; mock exam UI vs delivered `mock-saa-50.json`.

## Strengths

- Safety narrative and local-only AWS posture unchanged.
- `content_lint.py` PASS; placeholder scan PASS; Terraform fixture validate PASS (run-1 evidence).
- Readiness API honest about `insufficient_evidence` at baseline.

## Recommended next actions (product)

1. **Add `CSRF_TRUSTED_ORIGINS`** for Vite origins — unblocks all learner writes (blocks everything else for eval browser).
2. Strip rationales from public question GET + regression test (**PYTHON-203**).
3. **F-201:** Fix remaining 13 lesson `drillIds` + lint rule.
4. **F-202 / AWS-201–203:** Content fixes per Teacher/AWS reports (approved Lead Dev plans).
5. Corporate rollout: IT Manager **No-Go** until ITMGR-230 + ITMGR-201; sandbox policy for ITMGR-205.

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
| Gate 0 recorded | Yes — `reports/evidence/gate0-save-failure.md` |
| DB fingerprint after restore | **Match** — `eval-baseline/run-2/db-fingerprint-after.txt` |
| Repo manifest (excl. reports) | **Match** — `run-2/manifest-before.txt` vs `manifest-after.txt` |
| Server PIDs | 5173 → **28264**, 8000 → **20200** (unchanged) |
| Phase 4 report gate | **PASS** (strict follow-up) |
| Forbidden commands | None in orchestrator logs |
| MCP Terraform | `hashicorp/aws` provider **6.66.0** |
