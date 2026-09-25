# Round B — TEACHER rebuttals (run-2 strict)

Replies to Round A on Teacher-owned High findings and CR-0005 closure language.

---

## F-201 — Lesson drill ID dot/hyphen mismatch (XF-210)

**Round A (Teacher):** “**F-201 (drill IDs): AGREE primary — XF-210**”

**Round B:** **ACCEPT** — no peer dispute in Round A.

**Round A (Student):** “**Teacher F-201: AGREE** — lesson drill IDs wrong on inspection.”

**Round A (group, PYTHON paraphrase):** dotted lesson IDs 404 against hyphen files.

**Round B:** **ACCEPT** elevation to **Confirmed High** for discussion closure. Run-2 evidence narrows affected lessons to **13** (not 20) in `lesson-drillids-run2.md`; the defect class is unchanged — CR-0001 pattern regressed outside `lesson-1-1`.

**Final stance:** **Confirmed High**; fix = bulk hyphenate `drillIds` + lint rule.

---

## F-202 — Template MC bank (XF-203)

**Round A (Teacher):** “**F-202 (template MC): AGREE primary — XF-203**”

**Round A (AWS):** “**Teacher F-202: AGREE** (AWS-211 — pedagogy not service accuracy).”

**Round B:** **ACCEPT** AWS **REFINE** — I do not claim AWS factual errors in template rationales; I claim **exam-skill transfer** failure. ITMGR-203 **EXTEND** on workforce guessability is consistent, not a rebuttal.

**Round A (Student):** “**Teacher F-202: AGREE** — 24/28 sampled MCs keyed to choice `a`.”

**Round B:** **ACCEPT** corroboration; primary evidence remains EV-TEACHER-201/202 and stem grep (~227 MC).

**Final stance:** **Confirmed High** content-quality; phased rewrite F-202.

---

## F-203 / F-204 — GL-20 s03, GL-21 HCP title

**Round A (Teacher):** “**F-203/F-204 (GL-20/21): AGREE Confirmed Medium**”

**Round A (AWS):** “**Teacher F-203/F-204: AGREE** lab copy issues on GL-20/21.”

**Round B:** **ACCEPT** — independent AWS read matches JSON; no withdrawal.

---

## AWS-201–203 (V-01 blockers)

**Round A (Teacher):** “**AWS-201–003: AGREE** — paper review confirms V-01 blockers on GL-08/05/17.”

**Round B:** **ACCEPT** — aligns with my V-01 table; GL-05/08/17 remain assign-before-fix for guided paths.

**Note:** Round A numbering “003” maps to **AWS-203** (Athena DDL), not a legacy teardown ID.

---

## AWS-205 / CR-0005 teardown claims

**Round A (Teacher):** “**AWS-205: AGREE** — CR-0005 teardown claims partially verified.”

**Round A (Teacher):** “**CR-0005: REFINE** — concerns, not closed for learning quality.”

**Round B:** **ACCEPT** both — I **REBUT** any interpretation that placeholder scan PASS alone closes CR-0005 for learners. Enable var symmetry in Lead Dev plan (Python **REFINE** in Round A accepted).

---

## Gate 0 CSRF cluster (not a Teacher finding)

**Round A footnote:** “CSRF save failure … FULLSTACK-201 / PYTHON-201 / ITMGR-201.”

**Round B:** **REBUT** that footnote’s ID mix-up for CSRF — save failure is **FULLSTACK-230 / PYTHON-230 / ITMGR-230** (Critical). **PYTHON-201 / ITMGR-201** remain the separate **rationale leak / audit-grade metrics** cluster (High). I **ACCEPT** both clusters as Confirmed; they intersect on “trust exam progress” but differ on fix (settings + tests vs `public_question` strip).

**Round A (Teacher on PYTHON-201):** “**PYTHON-201: AGREE**”

**Round B:** **ACCEPT** — strip rationale from GET; CSRF fix does not remediate prefetch cheat.

---

## P-01 / UL beforeYouStart (preserved disagreement)

**Group (Round A summary):** “UL `beforeYouStart` omission = design concern vs defect.”

**Round B:** **REBUT** treating F-205 as optional forever — for **21/21 UL** missing preflight, I keep **Likely Medium** until product documents intentional pair design in `intended-design.md`. No **WITHDRAW** of F-205.
