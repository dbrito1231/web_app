# Round B — FULLSTACK rebuttals (run-2 strict)

Replies to Round A on Full-Stack Critical/High findings and bootstrap coupling.

---

## FULLSTACK-230 — CSRF trusted origins (Gate 0)

**Round A:** FULLSTACK Round A predates explicit FULLSTACK-230 line; carried note mentions CSRF with wrong IDs (**FULLSTACK-201**).

**Round B:** **ACCEPT** as **Confirmed Critical** primary owner for dev-stack save path.

- I **REBUT** run-1 attribution that **STUDENT-211** was evaluator-browser-specific. Gate 0 CDP capture: **403** + Django CSRF origin message for `http://127.0.0.1:5173`.
- **WITHDRAW** prior run-1 wording that implied MCP-only failure without settings defect.

**Quote (Round A — PYTHON):** tests use `enforce_csrf_checks=False` and omit `Origin`.

**Round B:** **ACCEPT** — explains green CI vs red browser; regression test with Origin required.

**Final stance:** **Confirmed Critical**; pairs **PYTHON-230**, **ITMGR-230**, **STUDENT-211** (symptom).

---

## FULLSTACK-201 — Question GET delivers rationales

**Round A (FULLSTACK):** “**PYTHON-201: AGREE** EV-FULLSTACK-201 / EV-FULLSTACK-210.”

**Round A (FULLSTACK):** “**FULLSTACK-201: AGREE primary (XF-201)**.”

**Round B:** **ACCEPT** — distinct from CSRF. UI hiding is not security; GET leak is **Confirmed High**.

**Round A (FULLSTACK):** “**FULLSTACK-203: AGREE Medium — amplifies XF-201 prefetch**.”

**Round B:** **ACCEPT** — 429× N+1 on mount multiplies exposure; fix catalog endpoint or strip fields server-side first.

**Final stance:** **Confirmed High** (XF-201).

---

## FULLSTACK-202 — Mock exam stale Phase 4 copy

**Round A (FULLSTACK):** “**FULLSTACK-202: AGREE Confirmed Medium (XF-202)**.”

**Round A (Student):** “**FULLSTACK-202: AGREE** — STUDENT-206 mock card.”

**Round B:** **ACCEPT** — wire mock from `mock-saa-50.json` or update disabled copy; **Confirmed Medium**.

---

## PYTHON-203 — Missing rationale regression test

**Round A (FULLSTACK):** “**PYTHON-203: AGREE** — extend test when fixing GET payload.”

**Round B:** **ACCEPT** — ship `assertNotIn("rationale", data)` with FULLSTACK-201 fix.

---

## FULLSTACK-203 / FULLSTACK-209 — N+1 and duplicate GET

**Round A (FULLSTACK):** “**FULLSTACK-203: AGREE Medium**”; duplicate GET noted in report.

**Round B:** **ACCEPT** Likely maintainability findings; not withdrawn pending catalog API.

---

## FULLSTACK-205 — MR selectCount not enforced

**Round A (FULLSTACK):** “**FULLSTACK-205: AGREE** — MR UX gap (XF-209).”

**Round A (PYTHON):** “**FULLSTACK-205: AGREE** — PYTHON-204 does not validate `selectCount` server-side.”

**Round B:** **ACCEPT** group **Likely Medium** — independent of XF-201 and CSRF cluster.

---

## FULLSTACK-207 / FULLSTACK-208 — Progress desync / bootstrap lab load

**Round A (FULLSTACK):** “**FULLSTACK-207: AGREE Likely**”; “**FULLSTACK-208: AGREE** — pairs with ITMGR-202.”

**Round B:** **ACCEPT** — CSRF fix restores POST but does not fix refresh desync or 42-lab eager load; remain **Likely** until implemented.

---

## ITMGR-202 extension

**Round A (FULLSTACK):** “**ITMGR-202: EXTEND** silent lab skip in same hook.”

**Round B:** **ACCEPT** — same file `useWorkbookBootstrap.ts`; banner recommendation stands.
