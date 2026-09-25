# Round B — AWS rebuttals (run-2 strict)

Replies to Round A on AWS Confirmed High lab findings and cross-role refinements.

---

## AWS-201 — GL-08 PowerShell user-data on AL2023

**Round A (AWS):** “**AWS-201: AGREE primary — GL-08 user data (XF-211)**”

**Round A (Teacher):** “**AWS-201–003: AGREE** — paper review confirms V-01 blockers on GL-08/05/17.”

**Round A (Student):** “**AWS GL-08/17: AGREE** — paper walkthrough would block (STUDENT-208).”

**Round B:** **ACCEPT** — MCP EV-AWS-252 and JSON s08 unchanged; no live CLI required for Confirmed.

**Gate 0 note:** UI checkpoint POST failure (CSRF) does not **REBUT** command defect; learners still hit broken user-data when they run CLI in terminal.

**Final stance:** **Confirmed High**.

---

## AWS-202 — GL-05 NACL deny-all ingress semantics

**Round A (AWS):** “**AWS-202: AGREE** — GL-05 NACL (XF-211).”

**Round B:** **ACCEPT** — protocol `-1` deny behavior documented in EV-AWS-251; lab text implying SSH-only deny is misleading for SAA.

**Final stance:** **Confirmed High**.

---

## AWS-203 — GL-17 missing Athena DDL

**Round A (AWS):** “**AWS-203: AGREE** — GL-17 Athena DDL (XF-211); *not* the old “teardown completeness” placeholder ID.”

**Round B:** **ACCEPT** — explicit rejection of legacy ID confusion is correct; s07–s08 gap is Confirmed from JSON read (EV-AWS-217).

**Final stance:** **Confirmed High**.

---

## AWS-204 — GL-07 title vs EFS in UL-07

**Round A (AWS):** “**AWS-204: AGREE** — GL-07/UL-07 EFS gap.”

**Round B:** **ACCEPT** — guided path does not practice EFS APIs UL-07 requires.

**Final stance:** **Confirmed Medium** (XF-211 bundle).

---

## AWS-205 — Teardown variable symmetry / scan script

**Round A (AWS):** “**AWS-205: AGREE** — scan var symmetry disabled (XF-205).”

**Round A (Python):** “**REFINE** — script lives in repo; enable check in Lead Dev plan.”

**Round B:** **ACCEPT** Python refine as implementation path, **REBUT** treating CR-0005 scan PASS as proof of learner-safe teardown — L66 `pass` is Confirmed (EV-AWS-244).

**Final stance:** **Confirmed Medium**; CR-0005 **partially verified** only.

---

## CR-0005 overall

**Round A (AWS):** “**CR-0005: REFINE** — improved but not universal; GL-02/UL-02 fixes confirmed.”

**Round B:** **ACCEPT** — GL-02 LocationConstraint and UL-02 Macie fixes stand as **Confirmed** improvements; blocking labs AWS-201–203 remain open.

---

## Teacher F-202 / AWS-211

**Round A (AWS):** “**Teacher F-202: AGREE** (AWS-211 — pedagogy not service accuracy).”

**Round B:** **ACCEPT** **REFINE** — AWS-211 stays **Subjective Observation / drill-key**; I do not co-sign F-202 as an AWS factual defect. No **WITHDRAW** of AWS-211 as pedagogy note.

---

## Gate 0 CSRF cluster (cross-role)

**Round A footnote (all roles):** CSRF tied incorrectly to PYTHON-201 / ITMGR-201 in carried note.

**Round B:** **ACCEPT** **FULLSTACK-230 / PYTHON-230 / ITMGR-230** as Critical save blocker. **REBUT** conflation with rationale leak — AWS lab Confirmed items are independent of POST persistence; ITMGR-205 **EXTEND** on hourly spend if GL-08 assigned remains policy, not AWS JSON error.

**Round A (ITMGR on AWS-201):** workforce table cites GL-08 debug spend.

**Round B:** **ACCEPT** **EXTEND** — operational risk, not a downgrade of AWS-201 severity.
