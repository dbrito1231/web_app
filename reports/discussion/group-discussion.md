# Multi-Agent Group Discussion

## STUDENT-201 — UL-01 vs GL-03 prerequisite

**Student:** AGREE primary — criterion 8 references GL-03 bucket; lessons silent.

**Teacher:** AGREE — extends V-02 cross-lab dependency.

**AWS Architect:** REFINE — not AWS factual error; sequencing.

**Group Conclusion:** Confirmed Medium pedagogy/lab-sequence fix.

## XF-202 — Mock exam not exposed (FULLSTACK-202)

**Student:** AGREE — looks unfinished on `/exam`.

**Teacher:** AGREE — mock-50 content exists; UX gap vs curriculum promise.

**Full-Stack:** AGREE primary (Confirmed Medium).

**Group Conclusion:** Wire mock flow or update copy; not a content accuracy defect.

## XF-209 — MR selection count not enforced (FULLSTACK-205, PYTHON-204)

**Full-Stack:** AGREE — submit with one box checked on "Select TWO".

**Python:** AGREE — backend accepts any list; set compare only.

**Teacher:** REFINE — drill fairness, not wrong key.

**Group Conclusion:** Likely Medium UX/API hardening; independent of XF-201.

## XF-201 — Question GET leaks rationale (PYTHON-201, FULLSTACK-201, PYTHON-203)

**Student:** AGREE — did not need exploit, but unfair exams worry me if someone cheats via network tab.

**Teacher:** AGREE — defeats purpose of rationales after attempt; fix is backend strip.

**AWS Architect:** AGREE — no AWS impact; local integrity issue.

**IT Manager:** AGREE — corporate sandbox still affected on shared PCs.

**Full-Stack:** AGREE — EV-FULLSTACK-201.

**Python:** AGREE — EV-PYTHON-201.

**Group Conclusion:** Confirmed High; strip rationale from GET; **PYTHON-203** regression test required (test today only hides keys).

## XF-210 — Lesson drill ID regression (Teacher F-201)

**Teacher:** AGREE — 20 lessons use `q-saa-3.2-*`; files are `q-saa-3-2-*`; only lesson-1-1 fixed under CR-0001.

**Student:** AGREE — lesson sidebar drills will 404 when wired.

**Python:** AGREE — GET `/api/questions/q-saa-1.2-k01-mc` would 404 (hyphen file is `q-saa-1-2-k01-mc`).

**Group Conclusion:** Confirmed High; bulk hyphen fix + lint rule.

## XF-203 — Template drill stems (Teacher F-202)

**Teacher:** AGREE — ~227 MC template stems; Confirmed High pedagogically.

**Student:** AGREE — items feel like pattern matching.

**AWS Architect:** REFINE — drill-design not factual AWS error.

**IT Manager:** EXTEND — workforce readiness impact (ITMGR-203).

**Group Conclusion:** Confirmed High content-quality issue; phased rewrite F-202.

## Required questions (abbrev.)

1. Multi-role: drill quality + API leak intersect on readiness trust.
2. Learning effectiveness: strong labs/lessons volume undermined by weak MC templates.
3. AWS accuracy: no confirmed factual regression post CR-0005 in spot checks.
4. Terraform: fixture validate OK; TF drills need same stem rewrite concern as SAA.
5. UX: navigation solid; exam list dense; mock button stale (XF-202).
6. Engineering: small test suite; API contract gap.
7. Disagreements preserved: UL `beforeYouStart` omission = design concern vs defect.
8. Needs evidence: AWS-210 pricing refresh; AWS-206/007 live CLI quoting; remaining GL spot-runs after JSON fixes.
9. Systemic: template stems (≥10) and rationale leak (all questions).
10. Strengths: safety narrative, four-tab clarity, lint/tf validate passing.

## XF-206 — Hourly labs + corporate deployment (ITMGR-205, AWS-201)

**IT Manager:** EXTEND — organizational High even when product disclaimers are correct.

**AWS Architect:** AGREE — cost/safety is learner discipline + account boundary.

**Group Conclusion:** Not a software defect; mandatory sandbox policy for enterprise assignees.

## XF-207 — Coverage `implemented_unverified` (ITMGR-204)

**Teacher:** AGREE — aligns with TEACHER-202 MCP recheck backlog.

**IT Manager:** AGREE — managers must not read as validated curriculum.

**Group Conclusion:** Confirmed Medium UX/comms issue.

## XF-208 — Bootstrap load cost + silent lab failures (ITMGR-202, FULLSTACK-208)

**Full-Stack:** AGREE — 42 lab GETs on every bootstrap (FULLSTACK-208); per-lab catch swallows errors.

**IT Manager:** AGREE — header % can lie if labs missing from map.

**Group Conclusion:** Likely Medium performance + progress honesty; lazy-load labs when tab opens.

## XF-211 — Blocking guided lab commands (AWS-201–004)

**AWS Architect:** AGREE — GL-08 user data, GL-05 NACL, GL-17 DDL, GL-07 EFS title gap (primary).

**Teacher:** AGREE — supports V-01 concerns; CR-0005 not fully closed for learning quality.

**Student:** AGREE — GL-08/17 would block completion on paper walkthrough.

**IT Manager:** EXTEND — hourly ALB/EC2 debug spend if GL-08 deployed (ITMGR-205).

**Group Conclusion:** Confirmed High/Medium lab fixes before assigning those labs at scale.

## XF-205 — CR-0005 teardown claims vs scanner (AWS-205, Teacher V-01)

**AWS Architect:** AGREE — `scan_lab_placeholders` var check is no-op; 16 labs with unset teardown vars.

**Teacher:** AGREE — concerns on CR-0005 closure.

**Python:** REFINE — script lives in repo; enable check in Lead Dev plan.

**Group Conclusion:** Partial verification only; do not treat scan PASS as end-to-end teardown proof.

## Revalidation outcomes

See `revalidation.md` — XF-201, XF-203, XF-210, XF-211 (AWS-201–003) Confirmed.

---

## Run-2 strict rebuttals (Gate 0 CSRF cluster)

*Moderator record — quoted text only from Round A / Round B role files.*

### Cluster scope (Critical): PYTHON-230, FULLSTACK-230, ITMGR-230, STUDENT-211 symptom

**Round A footnote (all six role files):**

> *Run-2 note: Round A text carried forward; CSRF save failure (Gate 0) added in run-2 reports as FULLSTACK-201 / PYTHON-201 / ITMGR-201.*

**Round B — TEACHER:**

> **REBUT** that footnote’s ID mix-up for CSRF — save failure is **FULLSTACK-230 / PYTHON-230 / ITMGR-230** (Critical). **PYTHON-201 / ITMGR-201** remain the separate **rationale leak / audit-grade metrics** cluster (High).

**Round B — ITMGR:**

> **REBUT** Round A carried footnote that labeled CSRF as ITMGR-201 — ITMGR-201 is rationale/metrics integrity; CSRF is ITMGR-230.

**Round B — FULLSTACK:**

> I **REBUT** run-1 attribution that **STUDENT-211** was evaluator-browser-specific. Gate 0 CDP capture: **403** + Django CSRF origin message for `http://127.0.0.1:5173`.
>
> **WITHDRAW** prior run-1 wording that implied MCP-only failure without settings defect.

**Round B — STUDENT:**

> I **WITHDRAW** the run-1 implication that normal Chrome always works while the evaluator browser alone fails. Gate 0 and PYTHON-230 show **403** with Django text `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins` for the standard Vite URL.

**Round B — PYTHON:**

> **REBUT** inference that `manage.py test workbook` PASS implies working browser saves — EV-PYTHON-203 documents `enforce_csrf_checks=False` and no Origin header.

**Round B — AWS:**

> **ACCEPT** **FULLSTACK-230 / PYTHON-230 / ITMGR-230** as Critical save blocker. **REBUT** conflation with rationale leak — AWS lab Confirmed items are independent of POST persistence.

**Group outcome (Round B consensus):** Gate 0 CSRF origin mismatch is **Confirmed Critical** for the standard Vite dev stack; **STUDENT-211** is the learner-visible symptom, not a separate root cause. Fix: align `CSRF_TRUSTED_ORIGINS` with `CORS_ALLOWED_ORIGINS` + Origin-aware regression tests.

### Rationale leak cluster (High): PYTHON-201, FULLSTACK-201, ITMGR-201, PYTHON-203

**Round A — FULLSTACK:**

> **PYTHON-201: AGREE** EV-FULLSTACK-201 / EV-FULLSTACK-210.
>
> **FULLSTACK-201: AGREE primary (XF-201).**

**Round A — PYTHON:**

> **PYTHON-201: AGREE primary (XF-201).**
>
> **FULLSTACK-201: AGREE** same root cause.

**Round A — ITMGR:**

> **PYTHON-201: AGREE** ITMGR-201 audit-grade impact.

**Round A — STUDENT:**

> **PYTHON-201: AGREE without independent exploit**

**Round B — STUDENT:**

> **ACCEPT** finding, **REBUT** my own evidentiary ceiling — I did not run DevTools harvest, but Teacher and Python **Confirmed** GET payloads include `rationale`.

**Round B — PYTHON:**

> **REBUT** conflation with CSRF — prefetch works while POST fails; two Confirmed clusters.

**Group outcome (Round B consensus):** **Confirmed High** (XF-201); strip `rationale` from GET; add **PYTHON-203** assertion. CSRF fix does not close this cluster.

### Teacher F-201 / XF-210 (High)

**Round A — TEACHER:**

> **F-201 (drill IDs): AGREE primary — XF-210**

**Round B — TEACHER:**

> **ACCEPT** elevation to **Confirmed High** for discussion closure. Run-2 evidence narrows affected lessons to **13** (not 20) in `lesson-drillids-run2.md`; the defect class is unchanged.

**Group outcome:** **Confirmed High**; count refined, fix unchanged.

### AWS-201–203 / XF-211 (High)

**Round A — AWS:**

> **AWS-201: AGREE primary — GL-08 user data (XF-211)**
>
> **AWS-202: AGREE** — GL-05 NACL (XF-211).
>
> **AWS-203: AGREE** — GL-17 Athena DDL (XF-211); *not* the old “teardown completeness” placeholder ID.

**Round B — AWS (each of 201–203):**

> **ACCEPT** — … **Final stance:** **Confirmed High**.

**Round B — AWS (Gate 0):**

> UI checkpoint POST failure (CSRF) does not **REBUT** command defect; learners still hit broken user-data when they run CLI in terminal.

**Group outcome:** **Confirmed High** for AWS-201, AWS-202, AWS-203; independent of CSRF cluster.

### ITMGR-205 (organizational vs defect)

**Round A — ITMGR:**

> **ITMGR-205: AGREE** sandbox policy required for hourly labs.

**Round B — ITMGR:**

> **REBUT** classifying ITMGR-205 as a **software Confirmed defect** … I **WITHDRAW** any implied Critical/High **product bug** label for ITMGR-205.

**Round A group (XF-206, prior):**

> Not a software defect; mandatory sandbox policy for enterprise assignees.

**Group outcome:** **Subjective Observation** / policy checklist; cross-link **AWS-201–203** in trainer comms — not a code CR for ITMGR-205 itself.
