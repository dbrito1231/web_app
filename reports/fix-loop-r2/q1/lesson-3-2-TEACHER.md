# Teacher review: lesson 3.2 (commit `89081d4`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Method:** Read `content/lessons/lesson-3-2.json`, the author notes (`lesson-3-2-impl.md`), and AWS's review (`lesson-3-2-AWS.md`). Independently verified 8 fact clusters via the AWS Documentation MCP (`search_documentation`/`read_documentation`, all fetched today, 2026-09-26): EC2 placement group partition (7/AZ) and spread (7 instances/AZ) limits; Lambda memory range 128 MB–10,240 MB in 1 MB increments and the 1,769 MB = 1 vCPU breakpoint; reserved vs. provisioned concurrency semantics; SnapStart's Firecracker-snapshot mechanism and its Java 11+/Python 3.12+/.NET 8+ runtime cutoffs, including the exact "use provisioned concurrency if... can't be adequately addressed by SnapStart" line; EC2 Auto Scaling warm pool states (Stopped/Running/Hibernated); AWS Compute Optimizer's 14-day default / 93-day enhanced-metrics lookback; and the SQS `ApproximateNumberOfMessagesVisible` CloudWatch metric. Also independently confirmed the Graviton citation defect (fetched `instance-types.html` directly — no percentage figure appears on that page) and confirmed by grep that the lesson body contains no occurrence of "interrupt," "rebalance," or "two-minute," so the Spot-interruption citation is indeed unsupported by body text.

## Verdicts

1. **Coverage:** All 10 `SAA-3.2-*` objectives (K01–K06, S01–S04) have their own `###` section in exact id order, matching `content/objectives/saa_c03.json` verbatim (confirmed by direct comparison, not just trusting the impl notes). No missing or extra objective.
2. **Accuracy:** I agree with AWS's review in full. Every fact I independently spot-checked matches current docs exactly, including the two defects AWS already flagged (AWS-L32-001, AWS-L32-002). I found no additional factual errors.
3. **Teaching quality:** Clear for a college IT student. Confused pairs are well contrasted: AWS Batch vs. EMR vs. Fargate (K01); EC2 Auto Scaling vs. the unified AWS Auto Scaling service (K04); reserved vs. provisioned concurrency vs. SnapStart (K05); cluster vs. partition vs. spread placement groups (S03); ENA vs. EFA (S03). All 10 exam tips are correct and consistent with their section bodies. No filler. No repetition of Lesson 2.1 content beyond brief, clearly-scoped references (Lambda/Fargate/EC2 choice, SQS/SNS/EventBridge basics, the four ASG policy types, ECS-vs-EKS) — each reference correctly defers rather than re-teaches, and I found no contradiction with 2.1.
4. **Length:** 2,442 words for 10 objectives (~244 words/objective) — confirmed by independent word count, matches the author's claim exactly. This sits between Lesson 2.1's leaner ~135/objective and Lesson 3.1's fact-dense ~374/objective, which is appropriate: 3.2 mixes conceptual contrasts (K01, K02, K06) with numeric mechanics (K04 warm pools, K05 Lambda memory/vCPU, S03 placement-group limits). Acceptable, nothing to cut.
5. **Format:** Independently verified, not just trusting impl notes — 0 single-asterisk spans, 0 pipe/table rows, 0 markdown links, 0 numbered-list lines, 11 total `###` headings (10 objectives + 1 Warnings block). All 18 `citationIds` resolve to files in `content/citations/`. All 16 `drillIds` resolve to existing `q-saa-3-2-*` placeholder files, listed in exact objective order (K01→S04).
6. **Teach-before-test readiness:** Mostly vacuous since all 16 questions remain unrewritten placeholders (consistent with 2.1's and 3.1's precedent). One real gap beyond AWS's findings: K04 discusses Spot as a cost/capacity option (mixed instances policy) but never teaches that Spot capacity can be reclaimed with a two-minute warning — a student has no way to answer a drill built on the exam-relevant "how does a fleet react to Spot reclamation" concept. This is the same gap AWS already identified as AWS-L32-002; I concur it must be fixed before question writing.
7. **Lint:** `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, labs 21+21, lessons 23).

## AWS's findings — do I agree?

Yes, on both. Independently confirmed:
- **AWS-L32-001** (citation-source mismatch, Medium): `cite-saa-3-2-graviton` points to `instance-types.html`, which I fetched directly — it contains no Graviton percentage figure, only a link out to the marketing page. The 20%/20% claim itself is accurate AWS language, just wrongly sourced. Agree with AWS's fix (repoint to the prescriptive-guidance page that has the exact figure and a worked pricing table).
- **AWS-L32-002** (citation-without-supporting-text, Medium): I grepped the body for "interrupt," "rebalance," and "two-minute" and found zero matches — the two-minute Spot interruption notice and rebalance recommendations are never taught anywhere in K01 or K04, even though a citation for exactly this fact exists. Agree with AWS's proposed fix (add 1–2 sentences to K04 after the mixed-instances-policy sentence).
- **AWS-L32-003** (Compute Optimizer resource-list subset, Low/optional): Agree this is defensible as-is since SAA-3.2 is compute-scoped; the optional clarifying clause is a nice-to-have, not required.

## New issue (Teacher-side)

| ID | Severity | Location | Fix |
|---|---|---|---|
| TEACHER-L32-001 | Low | K04, Spot/mixed-instances sentence | Same underlying gap as AWS-L32-002, recorded from the teach-before-test angle: a student reading only K04 has no way to answer a question about how a fleet should react when Spot capacity is reclaimed. Endorse AWS's exact proposed insertion (two-minute interruption notice as an EventBridge event/instance-metadata item, plus the earlier rebalance-recommendation signal) rather than a separate fix — one edit closes both AWS-L32-002 and this item. |

No other teach-before-test gaps found; the two orchestrators (K06), the placement-group/EFA/ENA cluster (S03), and the Lambda sizing chain (K05/S04) are each fully covered for their stated exam-tested facts.

**Lesson 3.2: not yet**

## Overall: concerns

Every fact I independently checked — placement-group partition/spread limits, Lambda memory-to-vCPU mapping, reserved vs. provisioned concurrency, SnapStart's runtime cutoffs, warm pool states, Compute Optimizer's lookback periods, and the SQS scaling metric — is accurate and matches current AWS documentation, corroborating AWS's review with no new factual errors. Both blocking issues are the same two AWS already found: a citation pointed at the wrong URL (AWS-L32-001) and a real, exam-relevant fact (Spot interruption notice/rebalance recommendations) that has a citation but was never actually written into the lesson body (AWS-L32-002, which I'm also raising independently as TEACHER-L32-001 from the teach-before-test angle — one fix closes both). Recommend Lead Dev apply AWS-L32-001 and AWS-L32-002/TEACHER-L32-001 (AWS-L32-003 optional), then re-validate for approval.
