# College IT Student Evaluation — Phase 3 (strict)

**Persona:** Second-year IT student; no production AWS/Terraform.  
**Date:** 2026-09-25  
**Mode:** Paper-feedback (Gate 0 Result A — `reports/evidence/gate0-save-failure.md`).  
**Evidence:** `reports/evidence/STUDENT/evidence-log.md`, `db-actions.md`, `ui-journey/*.md`

## Evaluation Scope

| Area | Count | Path |
|------|------:|------|
| Exam drills (paper + JSON keys) | **60** | `reports/evidence/STUDENT/ui-journey/exam.md` |
| Lessons read (API / A0 in UI) | **23** | `reports/evidence/STUDENT/ui-journey/lessons.md` |
| Labs paper walk | **13** | `reports/evidence/STUDENT/ui-journey/labs.md` |
| Design exercise | **1** (`de-multi-account`) | `ui-journey/labs.md` |
| Cold-start narrative | ~20 min | `ui-journey/start.md` |

**Browser note:** MCP `cursor-ide-browser` could not attach a tab this session; stems used `GET /api/questions/{id}` (same as Exam tab, keys stripped). Tab layout cross-checked against `reports/evidence/ui/*.md` (not `archive/run-1`).

## Executive summary

Start here is welcoming and A0 lab safety is clear. The 60-drill batch exposed a **repeatable MC/MR template** (paper score 60/60 without learning AWS). **Check answers** always returned **Forbidden** (CSRF), so I never saw UI rationales and SQLite stayed at **0** attempts. **22 of 23 lessons** are not surfaced in the React shell—only A0 on `/start`. UL-01 assumes **GL-03** and permissions-boundary vocabulary that lessons do not teach before GL-01.

---

## Jargon log (first encounter)

| Term | Where seen | Student understanding |
|------|------------|------------------------|
| Permissions boundary | GL-01 s06, UL-01 criteria | “Extra IAM cap?” — not defined in lessons |
| STS assume role | GL-03, UL-01 | “Temporary credentials swap” — clearer after GL-03 JSON |
| SCP | `de-multi-account` | “Org-wide deny list” — from exercise only |
| NACL vs SG | GL-05 | Stateless vs stateful — lesson 3-4 helped |
| HCP Terraform | lesson-tf-g8, tf drills | “Terraform Cloud successor brand” — vague |
| Requester Pays | SAA 4.x drills | S3 billing shift — not in labs yet |

---

## Confirmed Issues

### STUDENT-201 — UL-01 assumes GL-03 bucket not on learner path

**Severity:** Medium  
**Category:** lab-sequence, pedagogy  
**Location:** `content/labs/ul-01.json` acceptance criteria; Labs UI  
**Evidence:** EV-STUDENT-210, `ui-journey/labs.md`  
**Description:** UL-01 requires listing a **GL-03** bucket and a boundary tied to GL-01, but the Labs tab does not enforce GL-03 before UL-01 and Start workflow emphasizes GL-01 first.  
**Impact:** Challenge lab looks impossible on day one; undermines UL/Gl pairing trust.  
**Reproduction / Validation:** Expand UL-01 in UI; read criteria; confirm GL-03 not marked prerequisite.  
**Recommended Improvement:** Add explicit prerequisite chips (GL-01 → GL-03 → UL-01) or soften UL-01 criteria until GL-03 complete.  
**Confidence:** Confirmed  
**Related:** STUDENT-202

---

### STUDENT-202 — Permissions boundary not taught before GL-01

**Severity:** Low  
**Category:** pedagogy  
**Location:** `content/labs/gl-01.json` step s06; `content/lessons/*.json`  
**Evidence:** EV-STUDENT-211 (grep), `ui-journey/lessons.md`  
**Description:** GL-01 commands create a permissions boundary, but none of the 23 lesson bodies introduce the term or concept.  
**Impact:** Second-year student must web-search mid-lab; exam drills do not repair the gap.  
**Reproduction / Validation:** Grep lessons for `permissions boundary` (zero hits); open GL-01 s06 in Labs.  
**Recommended Improvement:** Add a short A1 sidebar callout or A0 addendum linking to IAM boundary docs.  
**Confidence:** Confirmed  
**Related:** STUDENT-201

---

### STUDENT-203 — Twenty-two lessons absent from app navigation

**Severity:** Medium  
**Category:** ux, pedagogy  
**Location:** `frontend/src/App.tsx`, `StartHereTab.tsx`  
**Evidence:** EV-STUDENT-231, `ui-journey/lessons.md`  
**Description:** Only `a0-lab-safety` renders in UI; `lesson-1-1` … `lesson-tf-g8` are API-only with no route or tab.  
**Impact:** “Read all lessons in app” is impossible without devtools; Exam/Coverage do not link to study material.  
**Reproduction / Validation:** Navigate all four tabs; search UI for lesson-2-1 title string (absent).  
**Recommended Improvement:** Add Lessons tab or Coverage → lesson deep links.  
**Confidence:** Confirmed  
**Related:** STUDENT-205

---

### STUDENT-204 — Template MC/MR drills train pattern matching

**Severity:** Medium  
**Category:** assessment-quality  
**Location:** SAA/Terraform MC/MR in `drill-60-ids.txt` sample  
**Evidence:** EV-STUDENT-219, EV-STUDENT-235, `ui-journey/exam.md`  
**Description:** Most MC choices are identical four-line template (“Apply the objective directly…” + three anti-patterns); MR keys always `{a,b}` vs unsafe `{c,d,e}`.  
**Impact:** 60/60 paper score overstates readiness; real SAA scenario questions (`q-saa-*-s*`) not in this batch still matter.  
**Reproduction / Validation:** Open any five consecutive SAA MC IDs in Exam sidebar; compare choice text.  
**Recommended Improvement:** Replace template distractors with scenario-based wrong answers per objective.  
**Confidence:** Confirmed  
**Related:** TEACHER template findings (discussion)

---

### STUDENT-211 — Exam and lab saves blocked (CSRF trusted origin)

**Severity:** Medium  
**Category:** ux, api  
**Location:** `/exam` **Check answers**; lab checkpoint POSTs  
**Evidence:** EV-GATE0-001, EV-STUDENT-217, EV-STUDENT-220, `db-actions.md`  
**Description:** POST `/api/attempts` returns **403** with CSRF origin failure for Vite origin `http://127.0.0.1:5173`; UI shows **Forbidden**; SQLite attempts remain 0.  
**Impact:** No scored feedback loop; readiness metrics never move; student cannot tell right/wrong except off-line keys.  
**Reproduction / Validation:** Gate 0 procedure on `q-a0-mc-001`; confirm `CSRF_TRUSTED_ORIGINS` missing in settings.  
**Recommended Improvement:** Add Vite origin to `CSRF_TRUSTED_ORIGINS` or exempt local API per product decision.  
**Confidence:** Confirmed  
**Related:** Gate 0, FULLSTACK findings

---

## Likely / subjective (nine-field where applicable)

### STUDENT-205 — Exam tab isolated from lessons

**Severity:** Low  
**Category:** ux  
**Location:** `ExamDrillsTab.tsx`  
**Evidence:** EV-STUDENT-203  
**Description:** No “read lesson X” link from module filters.  
**Impact:** Drills feel like trivia disconnected from GL/Labs path.  
**Reproduction / Validation:** Browse `/exam` modules A1–A4; confirm no lesson links.  
**Recommended Improvement:** Module header links to corresponding `lesson-*` reader.  
**Confidence:** Likely  
**Related:** STUDENT-203

---

### STUDENT-206 — Mock exam still labeled Phase 4 Locked

**Severity:** Informational  
**Category:** ux  
**Location:** `/exam` mock exam control  
**Evidence:** EV-STUDENT-203  
**Description:** Disabled control shows stale Phase 4 Locked copy.  
**Impact:** Minor confusion about product maturity.  
**Reproduction / Validation:** Open `/exam`; inspect mock exam button title/disabled state.  
**Recommended Improvement:** Update label to match current phase or hide control.  
**Confidence:** Likely  

---

### STUDENT-208 — Paper lab walk would block on GL-05, GL-08, GL-17

**Severity:** Medium  
**Category:** lab-command (learner perspective)  
**Location:** `gl-05.json` s10; `gl-08.json` s08; `gl-17.json` s07  
**Evidence:** EV-STUDENT-233, `ui-journey/labs.md`  
**Description:** NACL `-1` deny vs SSH intent; PowerShell user-data on AL2023; Athena DDL abbreviated.  
**Impact:** Student would burn hourly dollars debugging unhealthy targets / failed queries.  
**Reproduction / Validation:** Paper-walk steps without AWS; compare bullets to AWS docs (AWS role findings).  
**Recommended Improvement:** Fix commands per AWS architect review.  
**Confidence:** Likely  
**Related:** AWS-201–203

---

## Strengths

- Four-tab shell is easy to discover; A0 threat model matches college security instincts.
- GL-06/21 hourly cost gates and teardown ordering are repeated consistently.
- API strips answer keys from drill payloads — good integrity when saves work.

---

## Counts (return packet)

- **Drills logged:** 60 — `reports/evidence/STUDENT/ui-journey/exam.md`
- **Lessons read:** 23 — `reports/evidence/STUDENT/ui-journey/lessons.md`
- **Paths:**  
  - `reports/01-college-it-student.md`  
  - `reports/evidence/STUDENT/evidence-log.md`  
  - `reports/evidence/STUDENT/db-actions.md`  
  - `reports/evidence/STUDENT/ui-journey/start.md`  
  - `reports/evidence/STUDENT/ui-journey/labs.md`  
  - `reports/evidence/STUDENT/ui-journey/exam.md`  
  - `reports/evidence/STUDENT/ui-journey/coverage.md`  
  - `reports/evidence/STUDENT/ui-journey/lessons.md`

**Post-discussion:** Pending Phase 5–6.
