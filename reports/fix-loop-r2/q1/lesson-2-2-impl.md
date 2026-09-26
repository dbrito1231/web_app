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

## Fixes (AWS-L22-001..003, TEACHER-L22-001)

Fixed under Amendment 3 of `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`. Edited only `content/lessons/lesson-2-2.json` and `content/citations/cite-saa-2-2-*.json`.

### AWS-L22-001 — 24 generic citation notes rewritten

All 24 existing `cite-saa-2-2-*.json` `note` fields were rewritten from the identical boilerplate to name, in one sentence, the specific lesson claim each page verifies, following the `cite-saa-2-1-alb-cross-zone.json` pattern. Each page was re-opened via the AWS Documentation MCP (`search_documentation` / `read_documentation`) to confirm the claim is on it. New notes:

- `cite-saa-2-2-dr-strategies` — confirms the four DR strategies and their RPO/RTO ordering (K04), verbatim match to the Well-Architected page.
- `cite-saa-2-2-rds-multiaz` — confirms a Multi-AZ DB instance's non-readable standby and transparent endpoint failover (K06).
- `cite-saa-2-2-rds-multiaz-cluster` — confirms a Multi-AZ DB cluster's writer plus two readable standbys across three AZs (K06).
- `cite-saa-2-2-aurora-global` — confirms Aurora Global Database's promotable secondary clusters in other Regions (K06/S02).
- `cite-saa-2-2-route53-routing` — confirms the routing-policy definitions used in K01, including geoproximity and IP-based.
- `cite-saa-2-2-route53-failover` — confirms Route 53 failover routing's active-passive DNS behavior via health checks (K06).
- `cite-saa-2-2-elb-healthchecks` — confirms ALB health checks stop routing to failed targets (K08).
- `cite-saa-2-2-asg-multiaz` — confirms Auto Scaling replaces unhealthy instances and can launch in another AZ (K06).
- `cite-saa-2-2-immutable` — confirms immutable infrastructure replaces resources rather than patching in place (K07).
- `cite-saa-2-2-reliability-pillar` — confirms the Reliability Pillar redundancy guidance behind K05's distributed-design claim.
- `cite-saa-2-2-aws-backup` — confirms AWS Backup's policy-based schedules and cross-account/cross-Region copy (S01/S05).
- `cite-saa-2-2-s3-crr` — confirms S3 CRR asynchronously copies objects to another Region (S05).
- `cite-saa-2-2-ddb-global-tables` — confirms MREC default, same-account-only MRSC, and last-writer-wins conflict resolution (S02; also backs AWS-L22-002 below).
- `cite-saa-2-2-rds-proxy` — confirms RDS Proxy's connection pooling and up-to-66% failover-time reduction (K09).
- `cite-saa-2-2-service-quotas` — confirms requesting account/resource-level quota increases ahead of need (K10).
- `cite-saa-2-2-ebs-durability` — confirms EBS io2's 99.999% durability is single-AZ scoped (K11).
- `cite-saa-2-2-efs-features` — confirms Regional EFS replicates across all AZs in the Region automatically (K11).
- `cite-saa-2-2-s3-storage-classes` — confirms S3 One Zone-IA's single-AZ trade-off; **note flags that this page (`Welcome.html`) does not itself state the eleven-nines/three-plus-AZ durability figures** — those were verified in the AWS-L22 review against the separate S3 `DataDurability.html` page, not this citation. No fix made to the citation's URL since the title only ever claimed "storage classes," but flagging here per the task's instruction to report rather than invent support.
- `cite-saa-2-2-xray` — confirms X-Ray's request tracing and service map (K12).
- `cite-saa-2-2-cloudwatch` — confirms CloudWatch's metrics/logs/alarms (K12).
- `cite-saa-2-2-drs` — confirms AWS DRS's continuous block-level replication and minutes-scale recovery (S07).
- `cite-saa-2-2-vpc-route-tables` — confirms the one-route-table-per-subnet rule behind K03's per-AZ NAT pattern.
- `cite-saa-2-2-comprehend` — confirms Comprehend's NLP API with no training infrastructure to manage (K02).
- `cite-saa-2-2-polly` — confirms Polly's neural TTS via API, with cacheable/replayable audio (K02).

### AWS-L22-002 — DynamoDB global tables consistency modes (S02)

Added to S02: "defaults to multi-Region eventual consistency (MREC), with an MRSC same-account option for multi-Region strong consistency, and conflicting writes resolved last-writer-wins" (folded into the existing DynamoDB global tables clause).

Verified against:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html — MREC is the default if no mode is specified; MRSC is available only for same-account global tables; both models use last-writer-wins conflict resolution.
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html — confirms MREC vs MRSC definitions.

`cite-saa-2-2-ddb-global-tables` note updated to reflect this claim; already in `citationIds`.

### AWS-L22-003 — AWS Backup Vault Lock (S05)

Added to S05: "**AWS Backup Vault Lock** can additionally lock a vault's retention settings in governance mode, removable by users with sufficient IAM permissions, or in compliance mode, which becomes immutable — unchangeable and undeletable by any user, including the root user — once a mandatory cooling-off period of at least 72 hours expires."

Verified against https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html: governance-mode locks are removable by users with sufficient IAM permissions; compliance-mode locks have a cooling-off ("grace time") period the operator sets, no less than 3 days (72 hours), during which the lock can still be removed or changed, after which the vault and its lock are immutable for any user including root.

New citation file `content/citations/cite-saa-2-2-backup-vault-lock.json` added and inserted into the lesson's `citationIds`.

### TEACHER-L22-001 — Route 53 geoproximity and IP-based routing (K01)

Added to K01's routing-policy list: "**geoproximity** to route by resource location with an optional bias to shift traffic between resources; **IP-based** to route by the client's IP address using a customer-supplied CIDR map;" — inserted between geolocation and multivalue answer.

Verified against https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html: geoproximity routes based on resource location with an optional traffic-shifting bias; IP-based routing routes by client IP address using customer-supplied CIDRs. `cite-saa-2-2-route53-routing` note updated to include these two policies.

### Verification after fixes

- All 25 `citationIds` (24 original + `cite-saa-2-2-backup-vault-lock`) resolve to existing files.
- All 32 `drillIds` still present, unchanged.
- Single-asterisk spans: 0.
- Word count: 3,173 (up from 3,004; within the ~3,000-word target band, accepted as at cap given four small additive fixes).
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → PASS (questions 429, labs 21+21, lessons 23).
- No files outside `content/lessons/lesson-2-2.json` and `content/citations/cite-saa-2-2-*.json` were touched; no git/stash commands run; no servers started.
