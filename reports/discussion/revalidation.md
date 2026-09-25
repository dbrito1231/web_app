# Phase 13 — Revalidation (Run-2 strict, post Round B)

Neutral verifier posture: evidence cited in run-2 reports and Gate 0 artifacts; no fix applied during eval.

## Critical / High — Confirmed items (Round B closed)

| ID | Topic | Verifier action | Neutral verdict |
|----|--------|-----------------|-----------------|
| **PYTHON-230** / **FULLSTACK-230** / **ITMGR-230** | CSRF `CSRF_TRUSTED_ORIGINS` vs Vite `Origin` | Re-read `gate0-save-failure.md`, EV-GATE0-001/002, EV-PYTHON-215; Round B role quotes | **Confirmed Critical** — POST `/api/attempts` and lab checkpoints return **403** with Django origin-check message for `http://127.0.0.1:5173`. Unit tests omit Origin and disable CSRF enforcement; green tests do not contradict browser failure. |
| **STUDENT-211** | Exam/lab UI `Forbidden` on submit | Align with CSRF cluster in Round B (FULLSTACK **WITHDRAW** MCP-only narrative) | **Confirmed** (symptom) — same root cause as ITMGR-230; not a distinct middleware class defect. |
| **PYTHON-201** / **FULLSTACK-201** / **ITMGR-201** (XF-201) | Rationale on `GET /api/questions/<id>` | Re-GET sample / read `question-q-saa-1-1-k01-mc.json`; `public_question` in report | **Confirmed High** — full `rationale` present on GET; `correctAnswerIds` stripped only. Independent of CSRF (prefetch remains while POST blocked). |
| **PYTHON-203** | Regression test gap | Read `test_question_hides_answer_key` | **Confirmed Medium** (blocking for XF-201 closure) — asserts keys only, not rationale. |
| **Teacher F-201** (XF-210) | Lesson `drillIds` dot vs hyphen | `lesson-drillids-run2.md` vs filenames | **Confirmed High** — mismatch class verified; **13** lessons affected (count refined from 20 in Round B, defect unchanged). |
| **Teacher F-202** (XF-203) | Template MC stems | Sample questions + content scan attribution | **Confirmed High** — pedagogic defect; AWS role correctly treats as non-factual (AWS-211 separate). |
| **AWS-201** | GL-08 user-data on AL2023 | `gl-08.json` s08 + EV-AWS-208, MCP EV-AWS-252 | **Confirmed High** — PowerShell-wrapped user data incompatible with AL2023 cloud-init expectation. |
| **AWS-202** | GL-05 NACL semantics | `gl-05.json` s10 + EV-AWS-251 | **Confirmed High** — protocol `-1` deny on ingress blocks all traffic, not SSH-only as implied. |
| **AWS-203** | GL-17 Athena DDL | `gl-17.json` s07–s08 + EV-AWS-217 | **Confirmed High** — SELECT without prior CREATE EXTERNAL TABLE in lab steps. |

## Related Confirmed (Medium) — noted for closure context

| ID | Neutral verdict |
|----|-----------------|
| **FULLSTACK-202** (XF-202) | **Confirmed Medium** — disabled mock exam UI vs shipped mock content. |
| **AWS-204** | **Confirmed Medium** — GL-07 / UL-07 EFS gap (XF-211 bundle). |
| **AWS-205** (XF-205) | **Confirmed Medium** — teardown var symmetry check disabled in scanner; CR-0005 teardown claim partially verified only. |
| **ITMGR-204** (XF-207) | **Confirmed Medium** — learner-facing `implemented_unverified` registry comms risk. |
| **STUDENT-201** | **Confirmed Medium** — UL-01 / GL-03 sequencing (AWS factual **REFINE** accepted). |

## Downgraded / withdrawn after Round B

| ID | Neutral verdict |
|----|-----------------|
| **ITMGR-205** | **Subjective Observation** — organizational sandbox policy requirement; **not** a software defect (Round B **WITHDRAW** product-bug label). |

## Outcomes summary

- **Gate 0 CSRF cluster:** **Confirmed Critical** — settings + Origin-aware tests required before trusting any POST-backed progress or UI scored feedback.
- **XF-201 rationale leak:** **Confirmed High** — server-side strip on GET; **PYTHON-203** required with fix.
- **XF-210 F-201:** **Confirmed High** — hyphenate `drillIds` + lint; lesson count **13**.
- **XF-211 AWS-201–203:** **Confirmed High** — lab JSON fixes required before assign-at-scale; CSRF does not negate command-level defects.
- **XF-203 F-202:** **Confirmed High** — content rewrite track remains open.

Prior Phase 13 rows for F-203 GL-20 s03, mock UI, and template spot-checks remain **Confirmed** at Medium/High per original verifier reads; not re-opened in Round B.
