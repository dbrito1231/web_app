# Lesson 3.2 — AWS Solutions Architect re-check

Reviewed: `content/lessons/lesson-3-2.json` at commit `db714a6` ("Lesson 3.2: Spot interruption
notice and rebalance recommendation taught, Graviton citation repointed, Compute Optimizer scope
(Q1 LF)"). Diff verified with `git show db714a6`. Prior findings: `AWS-L32-001..003` in
`reports/fix-loop-r2/q1/lesson-3-2-AWS.md`; `TEACHER-L32-001` in
`reports/fix-loop-r2/q1/lesson-3-2-TEACHER.md`. Method: AWS Documentation MCP
(`search_documentation`) against docs.aws.amazon.com, fetched 2026-09-26. No AWS calls, no edits
made outside this report.

## Verdicts

| # | Item | Verdict |
|---|---|---|
| AWS-L32-001 | `cite-saa-3-2-graviton` repointed to `prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html` | **Gone.** The commit changes the citation's `url` and `title` to the prescriptive-guidance page and leaves the lesson's S03 Graviton sentence itself unchanged. `search_documentation` confirms this exact page/section ("Understand price variations between processor architectures") states: "ARM-based processor designed by AWS for EC2 instances, offering 20 percent lower cost and 20 percent or greater performance improvement over Intel counterparts" — matching the lesson's "around 20% lower cost and 20% or greater performance" and the citation's `note` verbatim. The citation now backs the exact claim it names. |
| AWS-L32-002 / TEACHER-L32-001 | New K04 sentence on the two-minute Spot interruption notice and rebalance recommendation; `cite-saa-3-2-spot-rebalance` added | **Gone.** The lesson body (current `bodyMarkdown`, K04) now reads: "Because Spot capacity can be reclaimed, Amazon EC2 sends a **two-minute Spot Instance interruption notice** as an EventBridge event and an instance metadata item before interrupting a Spot Instance, and it can send an earlier **rebalance recommendation** when a Spot Instance is at elevated risk of interruption; an Auto Scaling group or fleet can use either signal to drain work and launch a replacement before the hard interruption." This matches current AWS docs verbatim on both facts: `spot-instance-termination-notices.html` — "A two-minute advance warning issued by Amazon EC2 as an EventBridge event and instance metadata item before a Spot Instance is interrupted"; `rebalance-recommendations.html` — "A signal that notifies you when a Spot Instance is at an elevated risk of interruption, giving you time to proactively manage the instance before the two-minute interruption notice." Both citations (`cite-saa-3-2-spot-interruption`, re-scoped to K04, and the new `cite-saa-3-2-spot-rebalance`) now have supporting body text, and the body text is fully backed by current, correctly cited docs. |
| AWS-L32-003 | S02 Compute Optimizer clause: "(it also covers several database, cache, and other resource types beyond compute)" | **Gone** (was optional; applied). No accuracy issue — Compute Optimizer's supported-resource list does extend well beyond the compute-adjacent subset the lesson otherwise names, so the added clause is accurate and does not overreach. |

## 4. Nothing new is wrong

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, aws 310, tf
  119, labs 21+21, lessons 23).
- Diff reviewed line by line (`git show db714a6`): only `cite-saa-3-2-graviton.json` (url/title/note),
  `cite-saa-3-2-spot-interruption.json` (note re-scoped from K01/S03 to K04), the new
  `cite-saa-3-2-spot-rebalance.json`, and `lesson-3-2.json` (`citationIds` array gained
  `cite-saa-3-2-spot-rebalance`; `bodyMarkdown` gained the K04 Spot sentence and the S02 parenthetical)
  were touched, plus the two report files. No other section of the lesson, no drill IDs, and no other
  citation were changed.
- All 19 `citationIds` (18 + the new `cite-saa-3-2-spot-rebalance`) resolve to existing files under
  `content/citations/`.
- No new factual claim was introduced beyond the three items above, and none of them contradicts any
  fact confirmed in the original `lesson-3-2-AWS.md` review (placement-group limits, Lambda
  memory/vCPU mapping, SnapStart runtimes, warm pool states, instance refresh, mixed instances policy,
  AWS Batch/EMR, SQS scaling metric — all untouched by this commit).
- No new issue found.

**Lesson 3.2: approve for question writing**

## Overall: approve
