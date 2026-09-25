# College IT Student Evaluation (UI re-review)

**Supersedes:** Prior Student pass that used direct `POST /api/attempts` without in-browser screens (void per `.cursor/plans/student-ui-rereview-20260925.plan.md`).

Persona: second-year IT student, no AWS/Terraform production experience. **No source read** before UI exploration.

## Evaluation Scope

| Area | Method | Evidence |
|------|--------|----------|
| `/start` | Browser tab `b56e36`, desktop | `reports/evidence/STUDENT/ui-journey/start.md` |
| `/labs` | GL-01 expanded, UL-01 criteria seen | `ui-journey/labs.md` |
| `/coverage` | Registry task list | `ui-journey/coverage.md` |
| `/exam` | A0 filter + 15 drill cards via UI clicks | `ui-journey/exam.md` |
| Invalid URL | `/not-a-tab` shows Labs, URL unchanged | `ui-journey/exam.md` |
| Labs (paper) | GL-01,02,06,10,20 + UL-01 JSON after UI | findings below |
| Lesson JSON | Grep only for Confirmed teach-before-test | STUDENT-001, STUDENT-002 |

**Drill attempts:** UI **Check answers** clicked for **16+** question loads (15-card batch + A0 retries). **SQLite:** 0 rows persisted — evaluator browser returned **Forbidden** on submit (see Confirmed STUDENT-011).

---

## Confirmed Issues

### STUDENT-001 — UL-01 assumes GL-03 bucket not on lesson path

- **Severity:** Medium | **Category:** lab-sequence, pedagogy  
- **Location:** `ul-01.json` criterion; UI quoted in `ui-journey/labs.md`  
- **Evidence:** EV-STUDENT-010 (UI), lesson grep  
- **Confidence:** Confirmed  

### STUDENT-002 — Permissions boundary not taught before GL-01

- **Severity:** Low | **Category:** pedagogy  
- **Location:** GL-01 step s06 vs `content/lessons/`  
- **Evidence:** EV-STUDENT-011  
- **Confidence:** Confirmed  

### STUDENT-011 — Exam submit blocked with Forbidden in evaluator browser

- **Severity:** Medium  
- **Category:** ux, api (eval environment)  
- **Location:** `/exam` after **Check answers**  
- **Evidence:** EV-STUDENT-016, `ui-journey/exam.md`, `GET /api/progress` total 0  
- **Description:** UI selection and submit button work, but POST appears blocked (page text "Forbidden"; likely `LocalOriginGuardMiddleware` vs MCP browser Origin).  
- **Impact:** Student re-review could not persist 30 attempts in SQLite; normal Chrome at `127.0.0.1:5173` may differ — **Needs Verification** in your browser.  
- **Confidence:** Confirmed (for this session)  

---

## Subjective Observations

- **STUDENT-004:** Template MC stems / "pick first answer" pattern on A1 cards (UI + prior sample).  
- **STUDENT-005:** Exam tab does not link to prep lessons.  
- **STUDENT-006:** Mock exam "Phase 4 Locked" (UI).  
- **STUDENT-007:** Start here clear; Labs accordion long.  
- **STUDENT-008:** Paper walkthrough notes (GL-06 cost warning good; GL-20 s03 boilerplate — aligns Teacher F-03).  
- **STUDENT-010:** A0 drills fair when rationale visible (blocked this session after submit).

---

## Strengths

- Four-tab shell easy to discover from Start here copy.  
- GL-01 cost/steps visible without reveal.  
- GL/UL pairs on one Labs view.

---

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| STUDENT-001 | Confirmed Medium | — |
| STUDENT-002 | Confirmed Low | — |
| STUDENT-011 | Confirmed (eval browser) | — |
| STUDENT-004 | Subjective | XF-003 |
