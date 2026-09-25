# Round B — STUDENT rebuttals (run-2 strict)

Replies to Round A positions that touch Student Confirmed findings or Gate 0 paper-feedback mode.

---

## STUDENT-211 — Exam submit Forbidden (CSRF cluster)

**Round A (self, carried note):** Run-2 reports tie save failure to engineering IDs; Student report still describes “likely `LocalOriginGuardMiddleware` vs MCP browser Origin`.”

**Round B:** **ACCEPT** reclassification — primary root cause is **`CSRF_TRUSTED_ORIGINS`**, not a browser quirk.

- I **WITHDRAW** the run-1 implication that normal Chrome always works while the evaluator browser alone fails. Gate 0 and PYTHON-230 show **403** with Django text `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins` for the standard Vite URL.
- Round A did not dispute STUDENT-211; Full-Stack and Python own **FULLSTACK-230 / PYTHON-230 / ITMGR-230**. I **ACCEPT** those as the authoritative cluster for the same UI symptom (`Forbidden` on **Check answers**).
- **Impact unchanged for learners:** I still could not persist attempts or see scored rationales in UI this session; paper keys against JSON remain valid evidence for drill fairness notes (STUDENT-204, STUDENT-210).

**Final stance:** STUDENT-211 remains **Confirmed** as the learner-visible face of the CSRF cluster; cite **ITMGR-230** for workforce wording.

---

## STUDENT-201 — UL-01 / GL-03 prerequisite

**Round A (AWS):** “**REFINE** — not AWS factual error; sequencing.”

**Round B:** **ACCEPT** AWS refinement — I am not claiming wrong S3 API text.

**Round A (Teacher):** “**AGREE** — extends V-02 cross-lab dependency.”

**Round B:** **ACCEPT** — criterion still blocks someone who follows **lessons only**; that is the learner path I tested.

**Final stance:** **Confirmed Medium** pedagogy/lab-sequence (group conclusion unchanged).

---

## STUDENT-202 — Permissions boundary not taught before GL-01

**Round A (Teacher):** “**AGREE** — boundary not in lessons.”

**Round B:** **ACCEPT** — no Round A challenge; severity **Low** stands.

---

## Cross-role: PYTHON-201 / rationale leak

**Round A (STUDENT):** “**PYTHON-201: AGREE without independent exploit**.”

**Round B:** **ACCEPT** finding, **REBUT** my own evidentiary ceiling — I did not run DevTools harvest, but Teacher and Python **Confirmed** GET payloads include `rationale`. CSRF blocked post-submit UI feedback, so I cannot claim “hidden until submit” from UX alone; integrity issue is still **Confirmed High** via XF-201.

**Quote (Round A — Teacher):** “**PYTHON-201: AGREE**”

**Round B:** **ACCEPT** Teacher alignment; separate from CSRF (prefetch works even when POST fails).

---

## Cross-role: AWS GL-08 / GL-17 blockers

**Round A (STUDENT):** “**AWS GL-08/17: AGREE** — paper walkthrough would block (STUDENT-208).”

**Round B:** **ACCEPT** — paper walkthrough of GL-08 user-data and GL-17 DDL gap matches AWS-201 and AWS-203; no withdrawal.

---

## Cross-role: Teacher F-202 template MC

**Round A (STUDENT):** “**Teacher F-202: AGREE** — 24/28 sampled MCs keyed to choice `a` (STUDENT-204).”

**Round B:** **ACCEPT** — subjective pattern still **Confirmed High** at group level (XF-203); my sample supports but does not replace Teacher primary evidence.

---

## Cross-role: FULLSTACK-202 mock exam

**Round A (STUDENT):** “**FULLSTACK-202: AGREE** — STUDENT-206 mock card.”

**Round B:** **ACCEPT** — disabled “Phase 4 Locked” copy matches my `/exam` observation; **Confirmed Medium** (XF-202).
