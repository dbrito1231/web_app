# Round B — PYTHON rebuttals (run-2 strict)

Replies to Round A on Python Critical/High Confirmed findings and test blind spots.

---

## PYTHON-230 — Missing CSRF_TRUSTED_ORIGINS

**Round A (PYTHON):** Round A list predates explicit PYTHON-230; carried note mis-tags CSRF as PYTHON-201.

**Round B:** **ACCEPT** **Confirmed Critical** — Phase 3 POST with `HTTP_ORIGIN=http://127.0.0.1:5173` → **403** (EV-PYTHON-215, EV-GATE0-001/002).

**Round B:** **REBUT** inference that `manage.py test workbook` PASS implies working browser saves — EV-PYTHON-203 documents `enforce_csrf_checks=False` and no Origin header.

**Quote (Round A — FULLSTACK on PYTHON-203):** extend tests when fixing GET payload.

**Round B:** **ACCEPT** — add Origin + CSRF integration test alongside trusted origins settings change.

**Final stance:** **Confirmed Critical**; related **FULLSTACK-230**, **ITMGR-230**.

---

## PYTHON-201 — Rationale on question GET

**Round A (PYTHON):** “**PYTHON-201: AGREE primary (XF-201)**.”

**Round A (PYTHON):** “**FULLSTACK-201: AGREE** same root cause.”

**Round B:** **ACCEPT** — `public_question` strips keys only; EV-PYTHON-217 **Has rationale: True**.

**Round A (PYTHON):** “**FULLSTACK-203: EXTEND** N+1 GET multiplies rationale exposure.”

**Round B:** **ACCEPT** — amplification argument; remediation still starts at `public_question`.

**Round B:** **REBUT** conflation with CSRF — prefetch works while POST fails; two Confirmed clusters.

**Final stance:** **Confirmed High** (XF-201).

---

## PYTHON-203 — Test gap on rationale

**Round A (PYTHON):** “**PYTHON-203: AGREE** — Confirmed gap in `test_question_hides_answer_key`.”

**Round B:** **ACCEPT** — **Confirmed Medium** maintainability; must ship with PYTHON-201 fix.

---

## PYTHON-204 / FULLSTACK-205 — MR selectCount

**Round A (PYTHON):** “**FULLSTACK-205: AGREE** — PYTHON-204 does not validate `selectCount` server-side (XF-209).”

**Round B:** **ACCEPT** **Likely** — scoring design is intentional all-or-nothing (PYTHON-202 **REFINE Informational**); UI should enforce count, optional server 400.

---

## PYTHON-202 — MR all-or-nothing

**Round A (PYTHON):** “**PYTHON-202: REFINE** Informational by design.”

**Round B:** **ACCEPT** — no withdrawal; not a defect.

---

## PYTHON-206 — DEBUG / SECRET_KEY localhost scope

**Round A (PYTHON):** “**PYTHON-206: AGREE** acceptable for localhost-only scope.”

**Round B:** **ACCEPT** **Subjective Observation** — **REBUT** any run-2 attempt to upgrade to Confirmed without hosted deployment scope change.

---

## AWS-205 / scan script (cross-role)

**Round A (Python in group):** “**REFINE** — script lives in repo; enable check in Lead Dev plan.”

**Round B:** **ACCEPT** — engineering action on `scan_lab_placeholders.py`; does not downgrade AWS-205 Confirmed observation about current `pass` at L66.

---

## Teacher F-201 (cross-role)

**Round A (ITMGR):** extends F-201 to assigned paths.

**Round B:** **ACCEPT** — GET `/api/questions/<dotted-id>` 404 hypothesis aligns with hyphen filenames; content fix, not backend normalization required for closure.
