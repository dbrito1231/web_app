# Lesson 2.1 rewrite — implementation notes

Task 2.1: "Design scalable and loosely coupled architectures" (16 knowledge + 7 skill bullets, 34 current placeholder questions across q-saa-2-1-k01..k16 and q-saa-2-1-s01..s07, mc + mr).

## Section outline (one `###` per objective, in id order)

1. K01 — API creation and management: API Gateway REST vs HTTP vs WebSocket APIs.
2. K02 — AWS managed services: Transfer Family (SFTP/FTPS/FTP/AS2), SQS, Secrets Manager rotation vs Parameter Store.
3. K03 — Caching strategies: ElastiCache Redis vs Memcached, CloudFront/API Gateway caching.
4. K04 — Microservices design principles: stateless vs stateful, externalized session state.
5. K05 — Event-driven architectures: EventBridge rules/targets vs polling.
6. K06 — Horizontal vs vertical scaling.
7. K07 — Edge accelerators: CloudFront TTL caching vs Global Accelerator (non-cacheable TCP/UDP).
8. K08 — Migrating applications into containers: AWS App2Container.
9. K09 — Load balancing: ALB (layer 7) vs NLB (layer 4) vs GWLB.
10. K10 — Multi-tier architectures: presentation/logic/data tiers, serverless equivalent.
11. K11 — Queuing/messaging: SQS standard vs FIFO, SNS fan-out, EventBridge, Kinesis Data Streams contrast.
12. K12 — Serverless: Lambda vs Fargate vs EC2.
13. K13 — Storage types: block (EBS/instance store) vs object (S3) vs file (EFS/FSx).
14. K14 — Container orchestration: ECS vs EKS, both on EC2 or Fargate.
15. K15 — Read replicas: async read scaling/DR vs synchronous Multi-AZ failover.
16. K16 — Workflow orchestration: Step Functions Standard vs Express.
17. S01 — Designing event-driven/microservice/multi-tier architectures from requirements.
18. S02 — Scaling strategy selection: target tracking, step, scheduled, predictive.
19. S03 — Services for loose coupling: SQS/SNS/EventBridge/ALB/Step Functions.
20. S04 — When to use containers vs Lambda.
21. S05 — When to use serverless vs EC2/ECS-EKS-on-EC2.
22. S06 — Recommending compute/storage/networking/database per requirement.
23. S07 — Purpose-built AWS services vs self-managed equivalents.

Each section ends with a `**Exam tip:**` line contrasting the confusable options, per the plan's Amendment 3 instructions.

## Concepts the current (placeholder) questions test

The 34 questions under `content/questions/q-saa-2-1-*.json` are still the generic Q1-pilot placeholders (stem: "Which action is the right fit for this requirement: <objective text>?" with generic distractors about root user, teardown, and budget alerts). They do not yet test specific facts — they will be rewritten later in the pipeline. Each question's `objectiveIds`/id maps 1:1 to one of the 23 SAA-2.1 objective bullets, so the lesson's `drillIds` lists every `q-saa-2-1-*-mc`/`-mr` id in objective order (23 K/S bullets, 34 question files total, since K02/K05/K08/K11/K14 and all S bullets each have both an `-mc` and an `-mr`).

## Doc URLs verified (AWS Documentation MCP: search_documentation + read_documentation)

- API Gateway REST vs HTTP vs WebSocket: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-overview-developer-experience.html
- AWS Transfer Family: https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html
- Secrets Manager rotation: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html
- ElastiCache Redis/Memcached overview: https://docs.aws.amazon.com/whitepapers/latest/scale-performance-elasticache/full.html
- Microservices on AWS (stateless design): https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html
- EventBridge event bus/rules: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html
- EC2 Auto Scaling dynamic scaling policies: https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html
- CloudFront TTL/expiration: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html
- AWS App2Container: https://docs.aws.amazon.com/app2container/latest/UserGuide/start-intro.html
- Application Load Balancer / ELB: https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/full.html
- Multi-tier pattern whitepaper: https://docs.aws.amazon.com/whitepapers/latest/serverless-multi-tier-architectures-api-gateway-lambda/introduction.html
- SQS queue types (standard/FIFO): https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html
- SNS fanout: https://docs.aws.amazon.com/sns/latest/dg/welcome.html
- Kinesis Data Streams (choosing the right streaming service): https://docs.aws.amazon.com/whitepapers/latest/build-modern-data-streaming-analytics-architectures/key-considerations-while-building-streaming-analytics.html
- AWS Lambda: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
- AWS Fargate (compute services overview): https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html
- EC2 storage options (block/object/file): https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Storage.html
- Amazon ECS overview: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
- Amazon EKS / Kubernetes concepts: https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-concepts.html
- RDS read replicas: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html
- Step Functions (Standard vs Express workflows): https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html

21 citation files created under `content/citations/cite-saa-2-1-*.json` (same shape as `cite-saa-1-1-iam-bp.json`, `accessed: "2026-09-26"`), all listed in the lesson's `citationIds` and all resolving to a file.

## Verification performed

- `bodyMarkdown`: 0 single-asterisk spans (only `**bold**`), no links, no tables, no numbered lists, only `###`/`####` headings and `- ` bullets.
- Word count: 3,101 (task allows up to ~3,000 given the large number of objectives on this task; kept as tight as practical after two trim passes).
- Every `citationIds` entry resolves to a file in `content/citations/`.
- Every `drillIds` entry resolves to a file in `content/questions/`, and every `q-saa-2-1-*` question file is included in `drillIds`.
- `python scripts\content_lint.py` → PASS (429 questions, 21+21 labs, 23 lessons).
- File written with `json.load` / `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, UTF-8 text mode, via `backend\.venv\Scripts\python.exe`.

## Files touched

- `content/lessons/lesson-2-1.json` (bodyMarkdown, citationIds, drillIds rewritten; objectiveIds unchanged)
- `content/citations/cite-saa-2-1-apigw-overview.json`
- `content/citations/cite-saa-2-1-transfer-family-what-is.json`
- `content/citations/cite-saa-2-1-secrets-manager-rotate.json`
- `content/citations/cite-saa-2-1-elasticache-overview.json`
- `content/citations/cite-saa-2-1-microservices-whitepaper.json`
- `content/citations/cite-saa-2-1-eventbridge-bus.json`
- `content/citations/cite-saa-2-1-asg-dynamic-scaling.json`
- `content/citations/cite-saa-2-1-cloudfront-ttl.json`
- `content/citations/cite-saa-2-1-app2container.json`
- `content/citations/cite-saa-2-1-alb-elb.json`
- `content/citations/cite-saa-2-1-multitier-whitepaper.json`
- `content/citations/cite-saa-2-1-sqs-types.json`
- `content/citations/cite-saa-2-1-sns-fanout.json`
- `content/citations/cite-saa-2-1-kinesis-streaming.json`
- `content/citations/cite-saa-2-1-lambda-welcome.json`
- `content/citations/cite-saa-2-1-fargate-compute.json`
- `content/citations/cite-saa-2-1-ec2-storage-options.json`
- `content/citations/cite-saa-2-1-ecs-welcome.json`
- `content/citations/cite-saa-2-1-eks-concepts.json`
- `content/citations/cite-saa-2-1-rds-read-replicas.json`
- `content/citations/cite-saa-2-1-step-functions-welcome.json`

No questions, git commands, or servers were touched, per task scope.

## Fixes (Amendment 3 — AWS + Teacher review follow-up)

All numbers below were re-verified against current AWS documentation fetched today (2026-09-26) via the AWS Documentation MCP (`search_documentation` / `read_documentation`). Where the docs disagreed with the reviewers' suggested numbers, the docs won — noted explicitly below.

1. **AWS-L21-001 (Medium, K09) — ALB cross-zone load balancing.**
   - Before: "...HTTP/2, WebSockets, and always has cross-zone load balancing enabled..."
   - After: "...HTTP/2, WebSockets, and has cross-zone load balancing enabled by default, though it is a `load_balancing.cross_zone.enabled` target-group attribute you can turn off per target group..."
   - Doc quote (`elasticloadbalancing/latest/application/load-balancer-target-groups.html`, via MCP search context): "Configurable settings on a target group that control deregistration delay, cross-zone load balancing, client IP preservation..." and (`application-load-balancers.html` search context) "cross-zone load balancing... enabled by default on Application Load Balancers and configurable at the target group level."
   - New citation: `content/citations/cite-saa-2-1-alb-cross-zone.json`.

2. **AWS-L21-002 (Low, K11) — SQS FIFO throughput numbers.**
   - Before: "300 API calls per second unbatched, 3,000 with batching, up to 30,000 in high-throughput mode."
   - After: "300 transactions per second per API action unbatched, 3,000 with batching, and a further Region-dependent quota (up to 70,000 TPS unbatched, or 700,000 batched, in the highest-throughput Regions, less elsewhere) once high-throughput mode is turned on."
   - Doc quote (`AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html`): "Each partition in a FIFO queue is limited to 300 transactions per second, per API action... If you use batching, non-high throughput FIFO queues support up to 3,000 messages per second..." and the high-throughput table: "US East (N. Virginia), US West (Oregon), and Europe (Ireland): Up to 70,000 transactions per second (TPS)... All other AWS Regions: Default throughput of 2,400 TPS" (batched: up to 700,000 / 24,000 respectively). The old lesson's flat "30,000" figure does not appear on the current quotas page and was replaced — the docs' Region-variable figures win, per the reviewer's own note that the quota is Region-variable.
   - New citation: `content/citations/cite-saa-2-1-sqs-quotas-messages.json`.

3. **TEACHER-L21-001 (K12) — Lambda maximum execution timeout.**
   - Added: "A function has a hard maximum execution timeout of 900 seconds (15 minutes) per invocation, so work that could run longer belongs on Fargate, EC2, or in a Step Functions workflow instead."
   - Doc quote (`lambda/latest/dg/configuration-timeout.html`): "The default value for this setting is 3 seconds, but you can adjust this in increments of 1 second up to a maximum value of 900 seconds (15 minutes)." (The same page also now documents a 5,400-second/90-minute ceiling for AWS Lambda Managed Instances async/event-source-mapping invocations — a newer, non-exam-scope exception — so the lesson keeps the standard 900-second figure the exam tests.)
   - New citation: `content/citations/cite-saa-2-1-lambda-timeout.json`.

4. **TEACHER-L21-002 (K11) — SQS retention, message size, visibility timeout.**
   - Added: "A queue also retains a message for 4 days by default (up to 14 days maximum), accepts messages up to 1,048,576 bytes (1 MiB), and hides a received message from other consumers behind a visibility timeout that defaults to 30 seconds and can be extended up to 12 hours."
   - Doc quote (`quotas-messages.html`): "Message retention... By default, a message is retained for 4 days... The maximum is 1,209,600 seconds (14 days)." / "Message size | The minimum message size is 1 byte... The maximum is 1,048,576 bytes (1 MiB)." / "Message visibility timeout | The default visibility timeout for a message is 30 seconds... The maximum is 12 hours." **Note:** the max message size is currently 1 MiB per the SQS Developer Guide's own quotas page, not the older 256 KB figure still shown on the AWS General Reference service-endpoints page (`general/latest/gr/sqs-service.html`) — the Developer Guide's dedicated quotas page is the more current, authoritative source, so 1 MiB was used.
   - Reused citation: `content/citations/cite-saa-2-1-sqs-quotas-messages.json` (same page backs both #2 and #4).

5. **TEACHER-L21-003 (K01/S01) — API Gateway integration timeout.**
   - Added: "Both REST and HTTP APIs cap how long API Gateway waits for a backend integration to respond: an HTTP API's integration timeout is a fixed 30 seconds, while a Regional REST API's 50-millisecond-to-29-second integration timeout can be raised via a service quota request. Because that ceiling cannot be raised away entirely, long-running work belongs behind an asynchronous pattern — return immediately and let the client poll, or hand off to Step Functions or a queue — rather than a synchronous integration call."
   - Doc quote (REST, `apigateway/latest/developerguide/api-gateway-execution-service-limits-table.html`): "Integration timeout for Regional APIs | 50 milliseconds - 29 seconds for all integration types... | Yes *" (increasable via a Service Quotas console link), versus "Integration timeout for edge-optimized APIs | 50 milliseconds - 29 seconds... | No". Doc quote (HTTP, `apigateway/latest/developerguide/http-api-quotas.html`): "Maximum integration timeout | 30 seconds | No". This confirms the Teacher's note that REST regional limits are now raisable while HTTP API's is not, and that REST and HTTP quotas differ.
   - New citations: `content/citations/cite-saa-2-1-apigw-rest-quotas.json`, `content/citations/cite-saa-2-1-apigw-http-quotas.json`.

6. **TEACHER-L21-004 (K11) — Kinesis Data Streams per-shard throughput.**
   - Added: "Each shard supports up to 1 MB/second (1,000 records/second) of writes and up to 2 MB/second of reads, and that 2 MB/second read throughput is normally shared by every consumer reading the shard — a consumer that registers for enhanced fan-out instead gets its own dedicated 2 MB/second per shard."
   - Doc quote (`streams/latest/dev/service-sizes-and-limits.html`): "Each shard can support up to 1 MB/sec or 1,000 records/sec write throughput or up to 2 MB/sec or 2,000 records/sec read throughput." Doc quote (`streams/latest/dev/enhanced-consumers.html`): "Read throughput | Fixed at a total of 2 MB/sec per shard. If there are multiple consumers reading from the same shard, they all share this throughput... | Scales as consumers register to use enhanced fan-out. Each consumer registered to use enhanced fan-out receives its own read throughput per shard, up to 2 MB/sec, independently of other consumers."
   - New citations: `content/citations/cite-saa-2-1-kinesis-shard-limits.json`, `content/citations/cite-saa-2-1-kinesis-enhanced-fanout.json`.

## Post-fix verification

- `bodyMarkdown`: 0 single-asterisk spans (regex-checked), only `**bold**` and backticks used for the new `load_balancing.cross_zone.enabled` attribute name.
- Word count: 3,325 (up from 3,101; all six additions are one or two sentences each).
- All 7 new `citationIds` entries resolve to files in `content/citations/`; all pre-existing citations still resolve.
- File written with `json.load` / `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, UTF-8 text mode, via `backend\.venv\Scripts\python.exe`.
- `python scripts\content_lint.py` → PASS (429 questions, 21+21 labs, 23 lessons).

## Files touched (this pass)

- `content/lessons/lesson-2-1.json` (bodyMarkdown: K01, K09, K11, K12 sections; citationIds appended)
- `content/citations/cite-saa-2-1-alb-cross-zone.json` (new)
- `content/citations/cite-saa-2-1-sqs-quotas-messages.json` (new)
- `content/citations/cite-saa-2-1-kinesis-shard-limits.json` (new)
- `content/citations/cite-saa-2-1-kinesis-enhanced-fanout.json` (new)
- `content/citations/cite-saa-2-1-lambda-timeout.json` (new)
- `content/citations/cite-saa-2-1-apigw-rest-quotas.json` (new)
- `content/citations/cite-saa-2-1-apigw-http-quotas.json` (new)
