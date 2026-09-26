# Teacher re-check: lesson 2.1 (commit `4508cee`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

## 1. Prior items — status

| ID | Status |
|---|---|
| AWS-L21-001 (ALB cross-zone) | **Gone.** K09 now correctly says "enabled by default... though it is a `load_balancing.cross_zone.enabled` target-group attribute you can turn off per target group." |
| AWS-L21-002 (SQS FIFO quota sourcing) | **Gone.** K11 now gives Region-tiered figures (300/3,000 TPS baseline; up to 70,000/700,000 TPS in high-throughput mode in top Regions), backed by `cite-saa-2-1-sqs-quotas-messages`. |
| TEACHER-L21-001 (Lambda 15-min timeout) | **Gone.** K12 states the 900-second maximum. |
| TEACHER-L21-002 (SQS retention/size/visibility) | **Gone.** K11 states 4-day default/14-day max retention, 1 MiB max size, 30s default/12h max visibility timeout. |
| TEACHER-L21-003 (API Gateway integration timeout) | **Gone.** K01 distinguishes HTTP API's fixed 30s from Regional REST API's 50ms–29s (raisable). |
| TEACHER-L21-004 (Kinesis per-shard limits) | **Gone.** K11 states 1 MB/s (1,000 rec/s) write, 2 MB/s read, plus enhanced fan-out contrast. |

All six items verified resolved by reading the actual file text, independently of the AWS recheck report.

## 2. New numbers — clarity and placement

All six additions are placed inside the section that already teaches the relevant contrast (K01 REST-vs-HTTP timeout ceiling; K09 ALB cross-zone; K11 SQS size/retention/visibility plus FIFO throughput plus Kinesis shard/fan-out; K12 Lambda timeout), each as one or two sentences ending in a concrete number, not a vague qualifier. Each addition ties the number to a decision consequence (e.g., "work that could run longer belongs on Fargate... or Step Functions," "long-running work belongs behind an asynchronous pattern"), which is good pedagogy — it teaches the number and why it matters, not just the number. Exam tips were re-read and remain correct after the additions; none were invalidated by the new numeric detail (I spot-checked the SQS visibility-timeout claim against AWS Documentation MCP search results, which confirms `quotas-messages.html` is the authoritative page — consistent with the AWS recheck).

No new issue here.

## 3. Length

Word count: **3,350** (I count 3,350, not the reported 3,325 — a 25-word discrepancy from `lesson-2-1-impl.md`'s count, likely a tokenizer/counting-method difference, not a content difference; not worth a CR). For 23 objectives (16 K + 7 S) that's ~146 words/objective, in line with lesson-1.1–1.3 density and leaner per-objective than some other lessons. Given every section carries a contrast + exam tip + (for several) a load-bearing quota number, this is acceptable as-is. Nothing to cut.

## 4. Format

- Markdown subset: 0 single-asterisk spans (regex-checked directly on the file); only `###` headings (plus the standard lesson-level `##` title used identically across every lesson, e.g. lesson-1-3 — not a defect), `- ` bullets are absent (this lesson uses no bullet lists, prose only, which is fine), `**bold**`, and backticks (6, all wrapping the one `load_balancing.cross_zone.enabled` attribute name). No tables, no numbered lists, no markdown links.
- `citationIds`: all 28 resolve to files in `content/citations/` (verified programmatically).
- `drillIds`: all 35 entries resolve 1:1 to the 35 `q-saa-2-1-*` question files in `content/questions/` (34 K/S single-question objectives... actually 16 K + 7 S = 23 objectives, 5 of the K's and all 7 S's have both `-mc` and `-mr`, giving 35 total — matches file count exactly), and are listed in objective order (K01→K16, S01→S07), confirmed programmatically.

No format issues found.

## 5. Teach-before-test readiness

All 23 objectives now have a section that states the core fact, the contrasting alternative, and (where the objective is inherently numeric — SQS, Kinesis, Lambda, API Gateway, ALB) a specific number a question could test against. Concepts a question writer could ground: every K/S bullet's headline distinction and every named number. No exam-testable concept from the 23 objectives is missing a grounding sentence in this lesson.

## 6. Lint

`backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, aws 310, tf 119, labs 21+21, lessons 23).

## New issues

None. (TEACHER-L21-005 through -### not needed — no defects found in this re-check.)

**Lesson 2.1: approve for question writing.**

Overall: approve
