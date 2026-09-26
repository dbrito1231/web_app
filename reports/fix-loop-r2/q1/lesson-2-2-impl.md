# Lesson 2.2 rewrite — implementation notes

Task: SAA-C03 task 2.2, "Design highly available and/or fault-tolerant architectures."
Edited: `content/lessons/lesson-2-2.json` and 24 new `content/citations/cite-saa-2-2-*.json` files.
Not touched: any `content/questions/q-saa-2-2-*.json` file, and `content/lessons/lesson-1-3.json` (owned by a parallel agent).

## Section outline (one `###` per objective, in id order)

- K01 — AWS global infrastructure: Region/AZ scope, Route 53 routing policies (simple, weighted, latency, geolocation, multivalue, failover) + health checks.
- K02 — AWS Managed Services: Comprehend (NLP) and Polly (TTS) as already-resilient managed AI services.
- K03 — Basic networking: route tables, per-AZ NAT gateway pattern.
- K04 — DR strategies: backup and restore, pilot light, warm standby, multi-site active/active, with RPO/RTO figures and cost ordering.
- K05 — Distributed design patterns: redundancy/decoupling across AZs and Regions, referring back to 2.1.
- K06 — Failover strategies: RDS Multi-AZ failover, Route 53 failover routing, ASG/ELB health-check healing; plus the required contrast of Multi-AZ DB instance vs Multi-AZ DB cluster vs read replica vs Aurora Replicas vs Aurora Global Database.
- K07 — Immutable infrastructure: atomic deploys, no config drift, rollback by relaunch.
- K08 — Load balancing: ALB health checks and cross-zone load balancing (HA angle only; mechanics deferred to 2.1).
- K09 — Proxy concepts: RDS Proxy connection pooling/multiplexing and failover-time reduction.
- K10 — Service quotas and throttling: quota gaps in a scaled-down DR Region, proactive increases, throttling/backoff.
- K11 — Storage durability: EBS (single-AZ, io2 99.999%), EFS (Regional, all-AZ replication), S3 (3+ AZs, 11 nines) vs S3 One Zone-IA.
- K12 — Workload visibility: CloudWatch metrics/alarms vs X-Ray distributed tracing.
- S01 — Automation for infrastructure integrity: IaC, immutable deploys, ASG self-healing, AWS Backup schedules.
- S02 — HA/FT services across Regions/AZs: in-Region toolbox vs Aurora Global Database, DynamoDB global tables, S3 CRR, Route 53, DRS/AWS Backup cross-Region copy.
- S03 — Metrics from business requirements: availability "nines," RTO/RPO as measurable targets.
- S04 — Mitigating single points of failure: SPOF definition and examples, mitigation patterns.
- S05 — Data durability/availability strategies: AWS Backup vs S3 CRR vs continuous replication, PITR for accidental deletes.
- S06 — Selecting a DR strategy: mapping K04's catalog to stated RTO/RPO/budget.
- S07 — Reliability for legacy/non-cloud-native apps: AWS Elastic Disaster Recovery, RDS Proxy, ALB/NLB in front, AWS Backup — all drop-in, no code change.
- S08 — Purpose-built services for workloads (HA angle): AWS Backup, DynamoDB global tables, Aurora Global Database, Route 53 failover, AWS DRS vs hand-rolled equivalents.

## Concepts per current (placeholder) question

Every `q-saa-2-2-*` question is still an unrewritten placeholder whose stem simply restates its objective's guide text verbatim (e.g. "Pick the action that satisfies: AWS global infrastructure..."). There is no additional topic signal beyond the objective text itself, so the lesson content maps 1:1 to the 20 objective bullets (K01–K12, S01–S08), each with an `-mc` question and 12 of them (K03, K06, K09, K12, S01–S08) also with an `-mr` variant — all 32 are listed in `drillIds` in objective order.

## Doc URLs used (AWS Documentation MCP, all accessed 2026-09-26)

- https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_for_recovery_disaster_recovery.html (DR strategies, RPO/RTO)
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html (Multi-AZ instance vs cluster)
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html
- https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.Aurora_Fea_Regions_DB-eng.Feature.GlobalDatabase.html
- https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html (all 8 routing policy types)
- https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-types.html
- https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
- https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html
- https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_immutable_infrastructure.html
- https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
- https://docs.aws.amazon.com/aws-backup/latest/devguide/how-it-works.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.howitworks.html
- https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html
- https://docs.aws.amazon.com/whitepapers/latest/optimizing-postgresql-on-ec2-using-ebs/ebs-volume-features.html (EBS io2 durability)
- https://docs.aws.amazon.com/efs/latest/ug/features.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html (storage classes, 11 nines durability)
- https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
- https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html
- https://docs.aws.amazon.com/vpc/latest/userguide/RouteTables.html
- https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html
- https://docs.aws.amazon.com/polly/latest/dg/what-is.html

## Verification

- Word count: 3,004 (target ~2,500, hard max ~3,000 — accepted as effectively at cap).
- Single-asterisk spans: 0.
- All 24 `citationIds` and 32 `drillIds` resolve to existing files.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → PASS (questions 429, labs 21+21, lessons 23).
- The old placeholder `cite-2-2` is no longer referenced by the lesson (only by itself); the file was left in place since deleting citation files was outside this task's edit scope.
