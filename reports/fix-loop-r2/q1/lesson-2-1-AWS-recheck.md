# Lesson 2.1 — AWS re-check (fix commit `4508cee`)

Reviewer: Senior AWS Solutions Architect (read-only re-check)
Scope: `content/lessons/lesson-2-1.json` sections K01, K09, K11, K12 as changed in commit `4508cee`; the 7 new `content/citations/cite-saa-2-1-*.json` files it added; the "Fixes" section of `reports/fix-loop-r2/q1/lesson-2-1-impl.md`.
Method: AWS Documentation MCP (`search_documentation` / `read_documentation`) against docs.aws.amazon.com, re-fetched today. No AWS calls, no edits (other than this report).

## 1. Prior findings — status

| ID | Item | Status |
|---|---|---|
| AWS-L21-001 | ALB cross-zone load balancing described as "always... enabled" | **Gone.** K09 now reads "has cross-zone load balancing enabled by default, though it is a `load_balancing.cross_zone.enabled` target-group attribute you can turn off per target group." Verified verbatim against current docs (see §2). |
| AWS-L21-002 | SQS FIFO high-throughput quota asserted as a flat, un-sourced 30,000 | **Gone.** K11 now gives the Region-tiered figures and is backed by `cite-saa-2-1-sqs-quotas-messages`. Verified against the current quotas page (see §2). |
| AWS-L21-003 (informational) | ElastiCache section doesn't mention Valkey | Not addressed and not required — this was explicitly flagged "no fix required for exam accuracy." Still fine to leave as-is. |
| TEACHER-L21-001 | Missing Lambda 15-minute timeout | **Gone.** K12 now states the 900-second maximum, backed by `cite-saa-2-1-lambda-timeout`. Verified. |
| TEACHER-L21-002 | Missing SQS retention / message size / visibility timeout | **Gone.** K11 now states 4-day default / 14-day max retention, 1 MiB max message size, 30 s default / 12 h max visibility timeout. Verified. |
| TEACHER-L21-003 | Missing API Gateway integration timeout | **Gone.** K01 now distinguishes the HTTP API's fixed 30 s from the Regional REST API's 50 ms–29 s (raisable) timeout, backed by two new citations. Verified. |
| TEACHER-L21-004 | Missing Kinesis per-shard throughput | **Gone.** K11 now states 1 MB/s (1,000 records/s) write and 2 MB/s read per shard, plus the enhanced-fan-out distinction, backed by two new citations. Verified. |

All 6 actionable items from the prior AWS and Teacher reviews are resolved. No workaround or softened restatement was used — each fix states the current, specific number.

## 2. New/changed numbers — verification against current docs

- **SQS message size 1 MiB, retention 4 days default/14 days max, visibility timeout 30 s default/12 h max.** Confirmed verbatim on `AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html`: "By default, a message is retained for 4 days... maximum is 1,209,600 seconds (14 days)"; "the maximum is 1,048,576 bytes (1 MiB)"; "default visibility timeout... is 30 seconds... maximum is 12 hours." The lesson's implementer note about the older 256 KB figure on the General Reference service-endpoints page is correct context but not itself asserted in the lesson body — no issue.
- **SQS FIFO throughput: 300 TPS/API action unbatched, 3,000/s batched (non-high-throughput), Region-dependent higher quota in high-throughput mode.** Confirmed on the same page. The lesson's own numeric example ("up to 70,000 TPS unbatched, or 700,000 batched, in the highest-throughput Regions") matches the current table exactly (N. Virginia/Oregon/Ireland: 70,000 TPS unbatched, 700,000/s batched). Accurate and current.
- **Lambda 900-second (15-minute) maximum timeout.** Confirmed verbatim on `lambda/latest/dg/configuration-timeout.html`. The lesson correctly scopes out the newer 5,400 s Managed-Instances exception as non-exam material rather than folding it into the headline number — good call, matches SAA-C03 scope.
- **API Gateway HTTP API integration timeout: fixed 30 s, not increasable.** Confirmed verbatim on `apigateway/latest/developerguide/http-api-quotas.html` ("Maximum integration timeout | 30 seconds | No").
- **API Gateway REST API (Regional) integration timeout: 50 ms–29 s, increasable via service quota request.** Confirmed verbatim on `apigateway/latest/developerguide/api-gateway-execution-service-limits-table.html` ("Integration timeout for Regional APIs | 50 milliseconds - 29 seconds... | Yes *"), contrasted correctly against the edge-optimized row, which is "No." The lesson specifically scopes its claim to "a Regional REST API," which is the correct scope — an edge-optimized REST API's timeout is not increasable.
- **Kinesis Data Streams per-shard throughput: 1 MB/s (1,000 records/s) write, 2 MB/s read.** Confirmed verbatim on `streams/latest/dev/service-sizes-and-limits.html` (provisioned-mode column).
- **Kinesis enhanced fan-out: shared 2 MB/s read per shard by default vs. dedicated 2 MB/s per shard per enhanced-fan-out consumer.** Confirmed verbatim on `streams/latest/dev/enhanced-consumers.html`.
- **ALB cross-zone load balancing: on by default, configurable per target group via `load_balancing.cross_zone.enabled`.** Confirmed via AWS Documentation MCP search context matching this exact phrasing ("enabled by default on Application Load Balancers and configurable at the target group level") from `elasticloadbalancing/latest/application/application-load-balancers.html`, and the attribute name is listed as a target-group attribute on `load-balancer-target-groups.html`.

No discrepancies found between any new or changed number in the lesson and the current AWS documentation.

## 3. Citations

All 7 new `cite-saa-2-1-*` files (`alb-cross-zone`, `sqs-quotas-messages`, `kinesis-shard-limits`, `kinesis-enhanced-fanout`, `lambda-timeout`, `apigw-rest-quotas`, `apigw-http-quotas`) resolve, are listed in the lesson's `citationIds`, and each `url` is the correct current AWS docs page for the claim its `note` describes — spot-checked all 7 against the live pages above; every URL loaded and every `note` accurately paraphrases the specific number(s) it backs. No orphaned or mismatched citations.

## 4. New issues

None found. Nothing newly added in this fix pass is wrong or misleading for an exam student. The added sentences are appropriately scoped (e.g., "Regional REST API," "non-high-throughput," "shared throughput consumer" vs. "enhanced fan-out") so they don't overstate a single flat number where AWS's own quota is tiered or conditional.

## 5. Overall

**Lesson 2.1: approve for question writing.**

Overall: approve
