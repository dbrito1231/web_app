# Task status ledger

| task_id | role | spec_id | allowed_paths | dependency | status | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| phase-0-specs | implementer | REQ-P/A/C/L | `docs/**`, `content/coverage/**`, `content/objectives/**` | none | completed | five markdown specs + 189-row registry |
| phase-1-slice | implementer | REQ-A10–A16 | `frontend/**`, `backend/**`, slice content | phase-0 | completed | Django 8 tests OK; `npm run build` OK; Playwright 5 passed |
| phase-3-curriculum | implementer | REQ-P02, REQ-C* | `content/lessons/**`, `content/citations/**` | phase-1 | completed | 23 lessons; citations MCP sample-checked 2026-09-24 |
| phase-4-drills | implementer | REQ-P10–P12 | `content/questions/**`, `content/exercises/**`, registry | phase-3 | completed | 429 questions; 60 DEs; mock-50; lint PASS |
| phase-5-labs | implementer | REQ-L* | `content/labs/**`, `lab-fixtures/**` | phase-4 | completed | 21+21 labs; terraform validate OK |
| phase-6-signoff | orchestrator | section 14 | read-only + status | phase-5 | completed | delivery-report + Playwright + MCP citation-recheck 2026-09-24 |
| cr-0001-drill-ids | Lead Developer | CR-0001 | `content/lessons/lesson-1-1.json` | phase-6 | completed | 11 `drillIds` dots changed to hyphens; match question files |
| cr-0002-gl01 | Lead Developer | CR-0002 | `frontend/src/components/LabCard.tsx`, `content/labs/gl-*.json` | phase-6 | completed | Guided lab steps render as nested bullets |
| cr-0003-unguided | Lead Developer | CR-0003 | `frontend/src/data/curriculum.ts`, `frontend/src/components/LabCard.tsx` | cr-0002-gl01 | completed | UL-01 through UL-21 listed beside guided pairs; criteria, hints, and rubric render |
| cr-0004-batch1 | Lead Developer | CR-0004 | `LabCard.tsx`, `content/labs/*.json` | cr-0003 | completed | Cost from sameHourEstimateUsd; catalog minutes/modules/difficulty; UL teardown uses ul-NN tags |
| cr-0004-batches2-4 | Lead Developer | CR-0004 | `content/labs/gl-02.json`–`gl-21.json`, `ul-01.json`–`ul-21.json` | cr-0004-batch1 | superseded | Replaced by CR-0005 end-to-end lab rewrites |
| cr-0005-batch-a | Lead Developer | CR-0005 | `gl-02`–`gl-05`, `ul-02`–`ul-05` | cr-0004-batches2-4 | completed | Runnable steps/teardown; scan PASS |
| cr-0005-batch-b | Lead Developer | CR-0005 | `gl-06`–`gl-09`, `ul-06`–`ul-09` | cr-0005-batch-a | completed | Hourly s05 cost-risk; full VPC/NAT/ALB/ASG teardown |
| cr-0005-batch-c | Lead Developer | CR-0005 | `gl-10`–`gl-13`, `ul-10`–`ul-13` | cr-0005-batch-b | completed | IAM roles in steps; Lambda/SFN/API/DDB teardown |
| cr-0005-batch-d | Lead Developer | CR-0005 | `gl-14`–`gl-17`, `ul-14`–`ul-17` | cr-0005-batch-c | completed | RDS, CloudTrail, Route53, Athena commands |
| cr-0005-batch-e | Lead Developer | CR-0005 | `gl-18`–`gl-21`, `ul-01`, `ul-18`–`ul-21`, `scripts/scan_lab_placeholders.py` | cr-0005-batch-d | completed | GL-20 terraform workflow; UL-01 criteria fix; lint/tests/build/tf validate PASS |
| eval-run-2 | Lead Developer | eval_redo_extensive_20260925 | `reports/**`, `eval-baseline/run-2/**` | none | completed | Strict Phases 3–5 done; gate PASS (62 findings); Teacher/AWS/Student volumes met; DB+manifest integrity OK |
| fix-loop-wp1 | Lead Developer | CR-0006 | `backend/config/settings.py`, `frontend/src/api/client.ts`, tests | eval-run-2 | completed | CSRF_TRUSTED_ORIGINS; Origin POST test; plain 403 text; 9 Django tests OK |
| fix-loop-wp2 | Lead Developer | CR-0007 | `content_loader.py`, tests | fix-loop-wp1 | completed | GET omits rationale; attempt POST still returns it |
| fix-loop-wp3 | Lead Developer | CR-0008 | `content/lessons/lesson-1-2.json`–`lesson-4-4.json`, `scripts/content_lint.py` | fix-loop-wp2 | completed | 13 lessons hyphenated; lint PASS; Teacher approved |
| fix-loop-wp4-11 | Lead Developer | CR-0009–CR-0016 | questions, labs, frontend, scripts, docs | fix-loop-wp3 | completed | Pass-1 edits landed (stems, lint, lab commands, catalog, picker; tests, lint, scan, build OK). Round-final was a checklist, not a full regression. Register rows are not all Closed. See `reports/fix-loop/issue-register.md`. |
| fix-loop-r2-phase0 | Lead Developer | lead_dev_fix_loop_round2_20260926 | `reports/fix-loop/issue-register.md`, `reports/fix-loop-r2/**`, `eval-baseline/fix-loop-r2/` | fix-loop-wp4-11 | completed | Baseline on `main` (`925b619`). D1–D7 recorded. |
| fix-loop-r2-o | Lead Developer | lead_dev_fix_loop_round2_20260926 | frontend, content_loader, views, gl-07, gl-21, scanner | fix-loop-r2-phase0 | in progress | O1–O8 and O10 and D7 done. 13 Django tests OK. Lab scan PASS 42. O9, R6, D6, and Q1 still open. |

Rules: one writer, one path set. Agents never touch AWS. Roles: **Teacher** is read-only and owns learning-content correctness; **Lead Developer** is the only writer (the implementer) and needs an approved plan before any change. See `AGENTS.md`.
