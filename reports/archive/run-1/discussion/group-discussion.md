# Multi-Agent Group Discussion

## STUDENT-001 — UL-01 vs GL-03 prerequisite

**Student:** AGREE primary — criterion 8 references GL-03 bucket; lessons silent.

**Teacher:** AGREE — extends V-02 cross-lab dependency.

**AWS Architect:** REFINE — not AWS factual error; sequencing.

**Group Conclusion:** Confirmed Medium pedagogy/lab-sequence fix.

## XF-002 — Mock exam not exposed (FULLSTACK-002)

**Student:** AGREE — looks unfinished on `/exam`.

**Teacher:** AGREE — mock-50 content exists; UX gap vs curriculum promise.

**Full-Stack:** AGREE primary (Confirmed Medium).

**Group Conclusion:** Wire mock flow or update copy; not a content accuracy defect.

## XF-009 — MR selection count not enforced (FULLSTACK-005, PYTHON-004)

**Full-Stack:** AGREE — submit with one box checked on "Select TWO".

**Python:** AGREE — backend accepts any list; set compare only.

**Teacher:** REFINE — drill fairness, not wrong key.

**Group Conclusion:** Likely Medium UX/API hardening; independent of XF-001.

## XF-001 — Question GET leaks rationale (PYTHON-001, FULLSTACK-001, PYTHON-003)

**Student:** AGREE — did not need exploit, but unfair exams worry me if someone cheats via network tab.

**Teacher:** AGREE — defeats purpose of rationales after attempt; fix is backend strip.

**AWS Architect:** AGREE — no AWS impact; local integrity issue.

**IT Manager:** AGREE — corporate sandbox still affected on shared PCs.

**Full-Stack:** AGREE — EV-FULLSTACK-001.

**Python:** AGREE — EV-PYTHON-001.

**Group Conclusion:** Confirmed High; strip rationale from GET; **PYTHON-003** regression test required (test today only hides keys).

## XF-010 — Lesson drill ID regression (Teacher F-01)

**Teacher:** AGREE — 20 lessons use `q-saa-3.2-*`; files are `q-saa-3-2-*`; only lesson-1-1 fixed under CR-0001.

**Student:** AGREE — lesson sidebar drills will 404 when wired.

**Python:** AGREE — GET `/api/questions/q-saa-1.2-k01-mc` would 404 (hyphen file is `q-saa-1-2-k01-mc`).

**Group Conclusion:** Confirmed High; bulk hyphen fix + lint rule.

## XF-003 — Template drill stems (Teacher F-02)

**Teacher:** AGREE — ~227 MC template stems; Confirmed High pedagogically.

**Student:** AGREE — items feel like pattern matching.

**AWS Architect:** REFINE — drill-design not factual AWS error.

**IT Manager:** EXTEND — workforce readiness impact (ITMGR-003).

**Group Conclusion:** Confirmed High content-quality issue; phased rewrite F-02.

## Required questions (abbrev.)

1. Multi-role: drill quality + API leak intersect on readiness trust.
2. Learning effectiveness: strong labs/lessons volume undermined by weak MC templates.
3. AWS accuracy: no confirmed factual regression post CR-0005 in spot checks.
4. Terraform: fixture validate OK; TF drills need same stem rewrite concern as SAA.
5. UX: navigation solid; exam list dense; mock button stale (XF-002).
6. Engineering: small test suite; API contract gap.
7. Disagreements preserved: UL `beforeYouStart` omission = design concern vs defect.
8. Needs evidence: AWS-010 pricing refresh; AWS-006/007 live CLI quoting; remaining GL spot-runs after JSON fixes.
9. Systemic: template stems (≥10) and rationale leak (all questions).
10. Strengths: safety narrative, four-tab clarity, lint/tf validate passing.

## XF-006 — Hourly labs + corporate deployment (ITMGR-005, AWS-001)

**IT Manager:** EXTEND — organizational High even when product disclaimers are correct.

**AWS Architect:** AGREE — cost/safety is learner discipline + account boundary.

**Group Conclusion:** Not a software defect; mandatory sandbox policy for enterprise assignees.

## XF-007 — Coverage `implemented_unverified` (ITMGR-004)

**Teacher:** AGREE — aligns with TEACHER-002 MCP recheck backlog.

**IT Manager:** AGREE — managers must not read as validated curriculum.

**Group Conclusion:** Confirmed Medium UX/comms issue.

## XF-008 — Bootstrap load cost + silent lab failures (ITMGR-002, FULLSTACK-008)

**Full-Stack:** AGREE — 42 lab GETs on every bootstrap (FULLSTACK-008); per-lab catch swallows errors.

**IT Manager:** AGREE — header % can lie if labs missing from map.

**Group Conclusion:** Likely Medium performance + progress honesty; lazy-load labs when tab opens.

## XF-011 — Blocking guided lab commands (AWS-001–004)

**AWS Architect:** AGREE — GL-08 user data, GL-05 NACL, GL-17 DDL, GL-07 EFS title gap (primary).

**Teacher:** AGREE — supports V-01 concerns; CR-0005 not fully closed for learning quality.

**Student:** AGREE — GL-08/17 would block completion on paper walkthrough.

**IT Manager:** EXTEND — hourly ALB/EC2 debug spend if GL-08 deployed (ITMGR-005).

**Group Conclusion:** Confirmed High/Medium lab fixes before assigning those labs at scale.

## XF-005 — CR-0005 teardown claims vs scanner (AWS-005, Teacher V-01)

**AWS Architect:** AGREE — `scan_lab_placeholders` var check is no-op; 16 labs with unset teardown vars.

**Teacher:** AGREE — concerns on CR-0005 closure.

**Python:** REFINE — script lives in repo; enable check in Lead Dev plan.

**Group Conclusion:** Partial verification only; do not treat scan PASS as end-to-end teardown proof.

## Revalidation outcomes

See `revalidation.md` — XF-001, XF-003, XF-010, XF-011 (AWS-001–003) Confirmed.
