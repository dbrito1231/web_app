# Round B — ITMGR rebuttals (run-2 strict)

Replies to Round A on IT Manager Critical/High findings and extensions.

---

## ITMGR-230 — Save failure / CSRF trusted origins (Gate 0)

**Round A:** ITMGR Round A did not list ITMGR-230 explicitly (added run-2); Student **STUDENT-211** and engineering **FULLSTACK-230 / PYTHON-230** align.

**Round B:** **ACCEPT** as **Confirmed Critical** primary for corporate **No-Go** on mandatory tracking.

- Gate 0 text quoted in report: `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins`.
- I **REBUT** any remaining narrative that only automation browsers fail — standard Vite origin is affected (EV-GATE0-001/002).

**Final stance:** **Confirmed Critical**; release gate for L&D rollout checklist.

---

## ITMGR-201 — Audit-grade metrics / rationale prefetch

**Round A (ITMGR):** “**PYTHON-201: AGREE** ITMGR-201 audit-grade impact.”

**Round A (Teacher):** “**PYTHON-201: AGREE**” (group XF-201).

**Round B:** **ACCEPT** — **Confirmed High** independent of CSRF. Even when POST works, GET prefetch undermines compliance use cases.

**Round B:** **REBUT** Round A carried footnote that labeled CSRF as ITMGR-201 — ITMGR-201 is rationale/metrics integrity; CSRF is ITMGR-230.

**Final stance:** **Confirmed High**; block compliance reporting until PYTHON-201 fixed.

---

## ITMGR-204 — Coverage `implemented_unverified`

**Round A (ITMGR):** “**ITMGR-204: AGREE** coverage status not executive sign-off.”

**Round B:** **ACCEPT** — **Confirmed Medium** comms gap; unchanged.

---

## ITMGR-202 — Silent lab load omission

**Round A (ITMGR):** “**ITMGR-202: AGREE** silent lab skip risks inflated header %.”

**Round A (FULLSTACK):** “**ITMGR-202: EXTEND** silent lab skip in same hook.”

**Round B:** **ACCEPT** Full-Stack extension — same `useWorkbookBootstrap` catch path; stays **Likely Medium** pending injected 404 repro.

---

## ITMGR-203 — Longest-choice heuristic / F-202

**Round A (ITMGR):** “**Teacher F-202: EXTEND** workforce ROI via ITMGR-203.”

**Round B:** **ACCEPT** extension — **Needs Verification** at IT layer until Teacher validates guessability vs template length; not a rebuttal of F-202.

---

## ITMGR-205 — Corporate sandbox policy

**Round A (ITMGR):** “**ITMGR-205: AGREE** sandbox policy required for hourly labs.”

**Round B:** **REBUT** classifying ITMGR-205 as a **software Confirmed defect** — it is **Subjective Observation / organizational control** in my report. I **WITHDRAW** any implied Critical/High **product bug** label for ITMGR-205.

**Round A (group XF-206):** “Not a software defect; mandatory sandbox policy.”

**Round B:** **ACCEPT** group conclusion — keep **High organizational risk**, **not** a code fix ticket.

**Final stance:** **Subjective Observation** (policy checklist), cross-ref **AWS-201–203** in trainer comms.

---

## Teacher F-201 extension

**Round A (ITMGR):** “**Teacher F-201: EXTEND** broken lesson drill links hurt assigned learning paths.”

**Round B:** **ACCEPT** — supports **Confirmed High** F-201 for assigned module paths; separate from ITMGR-230.

---

## Workforce verdict (post-rebuttal)

**Round B summary:** **No-Go** mandatory tracked rollout until **ITMGR-230** + **ITMGR-201** addressed; **Conditional Go** voluntary self-study after CSRF fix and written sandbox policy (**ITMGR-205**, non-defect).
