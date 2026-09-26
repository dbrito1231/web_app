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
