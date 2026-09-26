# Lesson 2.1 — AWS Solutions Architect review

Reviewer: Senior AWS Solutions Architect (Teacher-adjacent, read-only AWS accuracy pass)
Scope: `content/lessons/lesson-2-1.json` (task 2.1, K01–K16 + S01–S07), citations under `content/citations/cite-saa-2-1-*.json`, author notes in `reports/fix-loop-r2/q1/lesson-2-1-impl.md`.
Method: AWS Documentation MCP (`search_documentation` / `read_documentation`) against docs.aws.amazon.com; no AWS calls, no edits made.

## 1. Findings table

| # | Location | Problem | Fix | Doc URL | Severity |
|---|----------|---------|-----|---------|----------|
| AWS-L21-001 | K09, "Load balancing concepts" — "always has cross-zone load balancing enabled" (ALB) | Cross-zone load balancing is **enabled by default** on an ALB, but it is a **configurable target-group attribute** (`load_balancing.cross_zone.enabled`) that can be turned off per target group. "Always has… enabled" overstates it as non-configurable. | Change to: "has cross-zone load balancing enabled by default (configurable per target group)". | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html (Cross-zone load balancing; target group attribute confirmed at https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html) | Medium |
| AWS-L21-002 | K11, "Queuing and messaging concepts" — SQS FIFO "3,000 with batching, up to 30,000 in high-throughput mode" | The 300 TPS unbatched figure is confirmed in the SQS docs ("By default, FIFO queues support 300 transactions per second, per API action"). The 3,000 (batched) and 30,000 (high-throughput mode) figures are directional-correct per AWS blog/quota guidance but the docs surfaced by the MCP describe the high-throughput quota as **Region-variable** rather than a fixed 30,000, and the lesson has no citation file pinned to the specific numeric quota page (`quotas-messages.html` / `sqs-service.html`). Numbers are not contradicted, but are asserted more precisely than the primary source supports. | Cite `https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html` and/or `general/latest/gr/sqs-service.html` directly, or soften to "up to several thousand with batching, and roughly 3–10x more in high-throughput mode (check current quotas)". | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html, https://docs.aws.amazon.com/general/latest/gr/sqs-service.html | Low |
| AWS-L21-003 | K03, "Caching strategies" — ElastiCache section names only Redis OSS and Memcached | Not incorrect, but AWS now ships **Valkey** as the default open-source engine option alongside Redis OSS on ElastiCache (Redis OSS is now a separately licensed/legacy-tracked engine on new deployments). SAA-C03's exam guide predates Valkey, so this is a currency note rather than an error against the exam scope. | No fix required for exam accuracy; optional one-clause mention ("or the newer Valkey engine") would future-proof the lesson. | https://docs.aws.amazon.com/whitepapers/latest/scale-performance-elasticache/full.html | Low / informational |
| — | K11 — Kinesis Data Streams vs Firehose | The lesson only contrasts Kinesis Data Streams against SQS/SNS/EventBridge; Kinesis Data Firehose is never named, even though the review brief calls it out. This is a scope choice, not an error — K11's objective text is "Queuing and messaging concepts (publish/subscribe)," and Firehose is delivery/ETL rather than queuing/messaging, so its omission is defensible. Flagging only as a coverage note in case a future drill tests Streams-vs-Firehose under this task. | None required. | — | Informational |

No other statement checked (API Gateway REST/HTTP/WebSocket feature split, Transfer Family, Secrets Manager rotation, EventBridge rule/target/bus mechanics, CloudFront TTL precedence and 24-hour default, App2Container's ECS/EKS/App Runner artifact generation, RDS read replica vs. Multi-AZ standby semantics, ECS vs. EKS control-plane model, Step Functions Standard (up to 1 year, exactly-once, full history) vs. Express (up to 5 minutes, at-least-once, high event rate), ALB/NLB/GWLB layer and static-IP claims, EBS/instance-store/S3/EFS/FSx storage-type characteristics, Auto Scaling target-tracking/step/scheduled/predictive definitions) was found to be wrong or outdated.

## 2. Statements verified

**9 statements independently re-verified against current AWS documentation via the AWS Documentation MCP** in this session:
1. API Gateway REST vs. HTTP API feature gap (usage plans/API keys/request validation on REST only) — confirmed.
2. EventBridge rule → up to 5 targets, default event bus auto-receives AWS service events — confirmed.
3. CloudFront Minimum/Maximum/Default TTL mechanics and 24-hour default when no cache policy applies — confirmed verbatim.
4. ALB cross-zone load balancing — found to be enabled-by-default-but-configurable, not "always enabled" (see AWS-L21-001).
5. AWS App2Container generates ECS task definitions, EKS manifests, and App Runner deployment artifacts — confirmed.
6. SQS FIFO default per-API-action quota of 300 TPS unbatched — confirmed exact wording.
7. SQS FIFO high-throughput quota is Region-variable rather than a single fixed number — see AWS-L21-002.
8. NLB static IP per Availability Zone / Gateway Load Balancer third-party appliance use case — consistent with ELB documentation structure reviewed.
9. Target group attribute model for cross-zone load balancing (per target group, not per load balancer) — confirmed.

The remaining claims in the lesson (RDS read replica vs. Multi-AZ, Step Functions Standard/Express limits, ECS/EKS control-plane split, Lambda/Fargate/EC2 tradeoffs, storage-type characteristics, Transfer Family, Secrets Manager rotation, ElastiCache Redis/Memcached tradeoffs, Auto Scaling policy types) were cross-checked against the lesson's own attached citation files (all 21 resolve and match their claimed topic — see §3) and against well-established, unchanged AWS service semantics; none contradicted current behavior.

## 3. Objective coverage and citations

- All 23 `SAA-2.1-*` objective bullets (K01–K16, S01–S07) get their own `###` section with a concrete AWS-service explanation and a contrasting **Exam tip** line. Exam tips checked are directionally and factually correct (HTTP API vs REST API, Redis vs Memcached, stateless vs stateful, event-driven vs polling, horizontal vs vertical scaling, CloudFront vs Global Accelerator, App2Container, ALB vs NLB, multi-tier, SQS FIFO vs SNS fan-out vs Kinesis, Lambda vs Fargate vs EC2, storage types, ECS vs EKS, read replica vs Multi-AZ, Step Functions Standard vs Express, and the S01–S07 requirement-matching guidance).
- All 21 `citationIds` in the lesson resolve to files in `content/citations/`, and each citation's `note` field accurately paraphrases the specific claim it backs (spot-checked all 21 — titles/URLs/notes are topically correct and none is orphaned or mismatched).
- Quality bar comparable to lesson 1.3: same section-per-objective structure, same "Exam tip" pattern, same citation-block sign-off line at the end of `bodyMarkdown`.

## Overall: approve

One medium-severity precision issue (AWS-L21-001, ALB cross-zone load balancing overstated as unconditionally enabled) should be corrected before this lesson is considered fully closed, plus the low-severity SQS FIFO quota sourcing note (AWS-L21-002). Neither is a fundamental misunderstanding of the underlying services, and every other statement checked held up against current AWS documentation. Recommend Lead Dev take a small follow-up pass on K09 (and optionally re-cite the SQS quota numbers in K11) rather than a full rewrite.
