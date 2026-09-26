# Task 3.5 Question Fairness Review -- College IT Student Evaluation
**Date:** 2026-09-26 | **Reviewer:** College IT Student (Q1 Fairness Review)

---

## Executive Summary

**Fairness rate: 100% (24/24 questions)**. All questions are answerable from the lesson alone, each has exactly one defensible answer (or answer set), and all explanations teach something useful. No wording giveaways, no silly distractors, and no tricks.

---

## Fairness Table

| Q# | Question ID | My Answer (Before Reveal) | Reason | Right? | Fair? | Why / Notes |
|----|---|---|---|---|---|---|
| 1 | k01-mc | c | Lesson: Athena is serverless SQL over S3 | YES | YES | Clear distinction between all four services taught; only Athena = serverless + no servers |
| 2 | k01-mr | a, d | Lesson: Lake Formation = permissions; QuickSight = dashboards | YES | YES | Both choices taught distinctly; clear two-service answer |
| 3 | k02-mc | b | Lesson: streaming = within seconds; fraud needs seconds | YES | YES | Streaming vs. batch/micro-batch clearly framed; no ambiguity |
| 4 | k03-mc | a | Lesson: DataSync for one-time bulk from NFS | YES | YES | File Gateway (persistent), Kinesis (streams), Glue crawler (schema) all wrong for this need |
| 5 | k04-mc | d | Lesson: Glue ETL for scriptable, scheduled; DataBrew for visual (opposite) | YES | YES | Clear contrast; all four choices taught |
| 6 | k04-mr | b, e | Lesson: DataBrew = visual, crawler = schema discovery | YES | YES | K04 explicitly contrasts both; Athena/EMR/Ray are wrong |
| 7 | k05-mc | b | Lesson: S3 access points for per-team, per-VPC scoping | YES | YES | Bucket policy (large), IAM (no boundary), Lake Formation admin (broad) all wrong |
| 8 | k06-mc | c | Lesson: 1,000 rec/sec per shard; 8,500 ÷ 1,000 = 8.5 → 9 | YES | YES | Math is exact; all four choices testable numbers |
| 9 | k07-mc | a | Lesson: Managed Flink for custom windowed computation | YES | YES | Firehose (delivery only), MSK (transport), Glue (batch) all wrong for continuous windowed logic |
| 10 | k07-mr | a, c | Lesson: Firehose = delivery; Kinesis Data Streams = independent replay | YES | YES | K07 taught both roles; Glue Ray/Flink/access point all wrong |
| 11 | s01-mc | d | Lesson: Lake Formation grant/revoke model for table-level permissions | YES | YES | IAM (permission-by-permission), Intelligent-Tiering (storage cost), Glue Ray (row filter) all wrong |
| 12 | s01-mr | b, d | Lesson: Hybrid access mode for gradual migration; admin for granting | YES | YES | S01 explicitly taught both; crawler/storage-class/EMR all wrong |
| 13 | s02-mc | b | Lesson: KDS ordered, replayable, multiple independent readers | YES | YES | Firehose (single destination, no replay), Glue (batch), QuickSight (viz only) all wrong |
| 14 | s02-mr | c, e | Lesson: fan-out = dedicated throughput; larger buffer = fewer files | YES | YES | S02 taught both levers; retention/on-demand/smaller-buffer all wrong |
| 15 | s03-mc | c | Lesson: S3 File Gateway for persistent hybrid NFS share with cache | YES | YES | DataSync (one-time), Kinesis (streams), Lake Formation (permissions) all wrong for NFS mount |
| 16 | s03-mr | a, e | Lesson: Data Transfer Terminal for offline; Kinesis/Firehose for continuous stream | YES | YES | S03 explicitly taught both; DataSync (online), File Gateway (files), EMR (batch) all wrong |
| 17 | s04-mc | a | Lesson: SPICE caching avoids re-query, fast under concurrent load | YES | YES | Direct query (slower), Athena query (not dashboard), Ray report (static) all wrong |
| 18 | s04-mr | b, d | Lesson: Glue crawler catalogs; Athena is QuickSight source | YES | YES | S04 explicitly taught pipeline; access point/EMR/Lake Formation all wrong |
| 19 | s05-mc | d | Lesson: EMR cluster mode for long-lived, tuned, custom software workloads | YES | YES | Athena (no cluster), Glue (serverless = no tuning), EMR Serverless (removes cluster) all wrong |
| 20 | s05-mr | a, c | Lesson: Athena for occasional SQL; EMR Serverless for existing Spark | YES | YES | S05 taught compute options in order; access point/Lake Formation all wrong |
| 21 | s06-mc | b | Lesson: uniform partition key overloads shard; use distinct, evenly distributed key | YES | YES | Retention (replay window), Firehose buffer (downstream), fan-out (read side) all wrong for write-side overload |
| 22 | s06-mr | c, d | Lesson: date partition scheme + Hive-style keys for query pruning | YES | YES | S06/S07 taught both; shard count (throughput), buffer size (cadence), Intelligent-Tiering (cost) all wrong |
| 23 | s07-mc | c | Lesson: CSV to Parquet reduces columns scanned | YES | YES | Shard count (Kinesis concept), DataBrew (prep tool), enhanced fan-out (KDS consumer) all wrong |
| 24 | s07-mr | b, e | Lesson: Parquet shrinks storage; partitioning reduces query scan | YES | YES | Kinesis retention (stream concept), Transfer Acceleration (transfer speed), MSK storage (cluster) all wrong |

---

## Fairness Assessment

**Answerability from lesson:** 24/24 (100%)
- Every question tests concepts explicitly taught in the lesson.
- No external AWS knowledge required beyond what K01–S07 covers.
- Even the math question (Q8) relies on a single, clearly stated fact (1,000 rec/sec per shard).

**Only one defensible answer:** 24/24 (100%)
- MC questions (14) each have exactly one correct choice; the other three are real AWS services or concepts misapplied to the scenario.
- MR questions (10) each have exactly one correct pair; no ambiguous overlaps.

**No wording giveaways:** 24/24 (100%)
- No correct answer is notably longer or shorter than distractors.
- No obvious hints in phrasing (e.g., "best" or "most" language).
- Rationales match choices exactly and explain why other options fail.

**No silly wrong choices:** 24/24 (100%)
- All distractors are real AWS services or patterns taught in the lesson.
- Each distractor fails the scenario for a specific, learnable reason (not because it's nonsense).
- Example: Q5 offers Athena (a tool, but ad hoc, not scheduled), Glue crawler (discovers schema, not transforms), DataBrew (visual, not scriptable) — all real, all taught, all wrong for this need in distinct ways.

**Explanation quality:** 24/24 (100%)
- All rationales match the choices and explain why each distractor fails.
- All rationales teach the underlying concept, not just "A is right, B is wrong."
- Examples: Q8 explains shard math step-by-step; Q21 explains the partition-key hot-shard problem and its solution.

---

## Confusing Issues

None. All questions are clear, testable, and unambiguous. The lesson is well-structured, and the question wording directly follows scenario language taught in K01–S07.

---

## Task Closure

**Task 3.5: close**

All 24 questions meet fairness criteria. The question set is ready for deployment.

---

## Overall Verdict

**Overall: approve**

As a student, I found every question to be fair: each one tested exactly what the lesson taught, with no tricks, ambiguities, or silly choices. All explanations made sense and helped me understand not just why the right answer was right, but why the other options failed — and I learned something from every single one.

