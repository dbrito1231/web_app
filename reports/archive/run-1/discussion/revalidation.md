# Phase 13 — Revalidation

## Queue (Critical/High)

| Item | Verifier action | Verdict |
|------|-----------------|---------|
| PYTHON-001 / FULLSTACK-001 rationale leak | Re-GET `http://127.0.0.1:8000/api/questions/q-saa-1-1-k01-mc`; inspect `public_question` | **Confirmed** — rationale in GET body; keys stripped only |
| PYTHON-003 missing rationale test | Read `test_scoring_and_api.py` `test_question_hides_answer_key` | **Confirmed** — asserts only `correctAnswerIds` absent |
| FULLSTACK-002 mock UI | `ExamDrillsTab.tsx` + `ui/exam.md` | **Confirmed** — disabled Phase 4 copy vs shipped mock content |
| Teacher F-01 drill IDs | `lesson-1-2.json` vs `q-saa-1-2-k01-mc` on disk | **Confirmed** — dots in lesson, hyphens in filenames (20 lessons) |
| Teacher F-02 template stems | Read `q-saa-1-1-k01-mc`, `q-saa-2-1-k01-mc`, `q-saa-3-1-k01-mc` | **Confirmed** — shared stem/distractor pattern (~227 MC) |
| Teacher F-03 GL-20 s03 | `gl-20.json` step s03 | **Confirmed** — Terraform “not required” contradicts later steps |

## Outcomes

- XF-001 (API leak): Confirmed High — fix before trusting exam-mode metrics.
- XF-010 (F-01 drill IDs): Confirmed High — CR-0001 regression on 20 lessons.
- XF-003 (F-02 drill templates): Confirmed High — content rewrite required for learning effectiveness.
- XF-011 AWS-001: `gl-08.json` s08 PowerShell user-data on AL2023 — **Confirmed** (EV-AWS-008, MCP EV-AWS-052).
- XF-011 AWS-002: `gl-05.json` s10 NACL protocol -1 deny — **Confirmed** (EV-AWS-005, MCP EV-AWS-051).
- XF-011 AWS-003: `gl-17.json` s07–s08 missing Athena DDL — **Confirmed** (EV-AWS-017).
- XF-005 AWS-005: `scan_lab_placeholders.py` L66 `pass` + `_var_scan.py` 16 labs — **Confirmed** (EV-AWS-043/044).
