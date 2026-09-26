# Teacher review: lesson 2.1 (commit `56353b4`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

## Findings

- **AWS findings:** the Teacher agrees with AWS-L21-001 (Medium: ALB cross-zone is on by default, not always on) and AWS-L21-002 (Low: SQS FIFO quota sourcing).
- **Accuracy spot-check:** 10 more facts checked, all accurate. These covered Step Functions Standard vs Express, HTTP API JWT/CORS, instance store, RDS cross-Region replicas and the Multi-AZ standby, GWLB, and Memcached vs Redis.
- **Coverage gaps (omissions, not errors):**
  - Lambda's 15-minute timeout;
  - SQS retention (4 days default, 14 max), message size and visibility timeout;
  - the API Gateway integration timeout;
  - Kinesis per-shard throughput.
- **Objectives:** all 23 have sections.
- **Teach-before-test:** vacuous until the questions are rewritten.
- **Pedagogy:** clear. Confusing pairs are contrasted, and the exam tips are correct.
- **Length:** 3,101 words, about 135 per objective, which is leaner than lessons 1.1–1.3. Nothing to cut.
- **Format:** clean. All 21 citations and 34 drillIds resolve, in objective order.
- **content_lint:** PASS.

## New issues (all Low)

| ID | Section | Fix |
|---|---|---|
| TEACHER-L21-001 | K12 | Add Lambda's 15-minute maximum execution time |
| TEACHER-L21-002 | K11 | Add SQS retention (default 4 days, max 14), message size, and visibility timeout (default 30 s, max 12 h) |
| TEACHER-L21-003 | K01/S01 | Add the API Gateway integration timeout. Lead Dev note: verify the current quota; REST API regional limits may now be raisable, and HTTP API differs |
| TEACHER-L21-004 | K11 | Add Kinesis per-shard throughput |

**Lesson 2.1: approve for question writing.** Overall: approve.
