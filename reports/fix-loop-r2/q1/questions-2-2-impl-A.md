# Task 2.2 questions — Writer A (16 knowledge questions, k01–k12)

Scope: `content/questions/q-saa-2-2-k*.json` (k01–k12, including k03-mr, k06-mr, k09-mr, k12-mr). Writer B owns the `s*` files in parallel; not touched here. `content/lessons/lesson-2-2.json` not edited.

## Metrics

- Files edited: 16 (`q-saa-2-2-k01-mc` … `q-saa-2-2-k12-mr`). No new citation files needed — all 16 questions cite ids already in `lesson-2-2.json`'s `citationIds`.
- `choices` count: 4/4 MC (12), 5/5 MR (4). All PASS.
- `correctAnswerIds` length matches `selectCount` on all 16. PASS.
- 6-word stem-opening collisions across the 16: **0**.
- Letter references in rationale (e.g. "choice a", "(b)"): **0**.
- Objective text pasted verbatim into a stem: **0**.
- MC key letter spread (12 MC): a=3, b=3, c=3, d=3 — perfectly even.
- MR key-slot spread (4 MR × 2 slots = 8): a=2, b=1, c=1, d=2, e=2.
- Longest-choice-is-key (MC only, after Lead Dev review fixes below): **3/12 = 25%** (limit ≤35%). Matches: k05, k10, k12.
- `id`, `type`, `module`, `objectiveIds`, `selectCount` verified unchanged from the pre-rewrite stub files (asserted in the write script before saving).
- `citationIds` non-empty, `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` on all 16. PASS.
- `python scripts\content_lint.py` → `PASS` (429 questions total, 310 AWS / 119 TF, no shape/registry/banned-copy/template-stem errors).

## Per-question table

| ID | Objective | Tests | Key | Lesson sentence(s) backing key + distractors | Doc URL(s) |
|---|---|---|---|---|---|
| k01-mc | K01 | Route 53 routing-policy selection (latency-based vs weighted vs geolocation vs failover) | b (latency-based) | "latency-based to send each client to the lowest-latency Region"; "weighted to split traffic across resources by a percentage"; "geolocation to route by client location, for compliance or localization"; "failover for active-passive DNS failover" | routing-policy.html |
| k02-mc | K02 | Managed AI service selection vs self-hosted / wrong-service | a (Comprehend) | "Amazon Comprehend runs natural-language processing (sentiment...) ... with no model training infrastructure to run or patch"; "Amazon Polly turns text into lifelike speech"; "not a model you host and fail over yourself on EC2" | comprehend `what-is.html`; polly `what-is.html` |
| k03-mc | K03 | Route table / NAT gateway per-AZ resiliency | c (one NAT + one route table per AZ) | "one NAT gateway and one route table per AZ, so each AZ's outbound path survives independently"; "a route table in one AZ that points at a NAT gateway in a different AZ creates a cross-AZ dependency" | RouteTables.html |
| k03-mr | K03 | Same pattern, Select TWO (both AZs need their own NAT+table) | a, d | same K03 lesson text, applied per-AZ | RouteTables.html |
| k04-mc | K04 | DR-tier selection from RTO/RPO numbers | d (pilot light) | "Pilot light — RPO in minutes, RTO in tens of minutes... compute is not deployed until needed"; contrast text for backup/restore, warm standby, multi-site active/active | wellarchitected `rel_planning_for_recovery_disaster_recovery.html` |
| k05-mc | K05 | Distributed/redundant design vs single-instance SPOF | a (stateless multi-AZ fleet) | "a distributed design spreads redundant copies of each component across AZs... removes any dependency on one specific instance or AZ"; "a single scaled-up instance handling everything is the opposite of this pattern" | wellarchitected reliability-pillar `welcome.html` |
| k06-mc | K06 | RDS Multi-AZ instance vs cluster vs read replica vs Aurora Global Database | b (Multi-AZ DB cluster) | "A Multi-AZ DB cluster keeps two readable standbys across three AZs, adding read capacity on top of that same failover protection"; contrast to Multi-AZ DB instance, read replica, Aurora Global Database | Concepts.MultiAZ.html; multi-az-db-clusters-concepts.html |
| k06-mr | K06 | Compute-tier automatic healing (ALB + ASG health checks) vs DB/DNS-layer failover, Select TWO | b, e | "Auto Scaling and Elastic Load Balancing health checks replace unhealthy instances automatically and stop sending traffic to instances that fail their checks"; contrast to RDS Multi-AZ failover and Route 53 failover routing (DNS layer) | target-group-health-checks.html; auto-scaling-benefits.html |
| k07-mc | K07 | Immutable infrastructure vs in-place patching | c (AMI + ASG instance refresh) | "no in-place updates... every change ships as a new image or template that replaces the old resource entirely"; "rollback is simply relaunching the previous image rather than undoing a change in place" | rel_tracking_change_management_immutable_infrastructure.html |
| k08-mc | K08 | Cross-zone load balancing vs ALB health checks / ASG health checks / Route 53 multivalue | d (cross-zone LB) | "Cross-zone load balancing, on by default for an ALB, spreads requests evenly across every healthy target in every enabled AZ"; contrast to ALB health checks, ASG health checks, Route 53 multivalue answer | target-group-health-checks.html |
| k09-mc | K09 | RDS Proxy connection pooling vs Multi-AZ/read replica/Aurora Global Database | a (RDS Proxy) | "RDS Proxy sits between an application and its RDS or Aurora database, pooling and multiplexing many short-lived client connections onto fewer database connections" | rds-proxy.howitworks.html |
| k09-mr | K09 | RDS Proxy's two benefits (pooling + failover-time reduction), Select TWO | c, d | same RDS Proxy sentence, plus "RDS Proxy also improves availability during a failover: it holds client-side connections open and transparently switches them to the new writer... cutting the failover time" | rds-proxy.howitworks.html |
| k10-mc | K10 | Service Quotas planning for standby/DR capacity | b (request increase ahead of time) | "Request the needed quota increases in the recovery Region ahead of time, through the Service Quotas console or API, rather than discovering the gap during an actual disaster" | request-quota-increase.html |
| k11-mc | K11 | Storage durability + access-pattern fit (S3 vs EFS vs EBS vs S3 One Zone-IA) | c (S3, non-One-Zone) | "Amazon S3 stores objects redundantly across at least three AZs by default and is designed for 99.999999999%... durability"; "S3 One Zone-IA, which trades that redundancy for a lower price by using a single AZ"; "Amazon EFS... replicates data and metadata across all AZs"; "An Amazon EBS volume replicates within a single AZ only" | DataDurability.html; Welcome.html; efs `features.html`; EBS durability whitepaper page |
| k12-mc | K12 | CloudWatch vs X-Ray scope (alarm/metric vs per-request trace) | d (X-Ray) | "AWS X-Ray adds distributed tracing... traces a single request across multiple services, builds a service map, and pinpoints which downstream call... introduced latency"; "Amazon CloudWatch collects the metrics, logs, and alarms" | xray `aws-xray.html`; cloudwatch `WhatIsCloudWatch.html` |
| k12-mr | K12 | CloudWatch alarm (scaling trigger) + X-Ray trace, Select TWO | a, e | same as k12-mc, applied to a two-need scenario | xray `aws-xray.html`; cloudwatch `WhatIsCloudWatch.html` |

## Distractor-type table (16 questions, my writer-A slice)

| Type | Questions | Count |
|---|---|---|
| Route 53 routing-policy selection | k01-mc | 1 |
| Managed AI service selection (Comprehend/Polly vs self-hosted/misapplied service) | k02-mc | 1 |
| Route table / NAT gateway per-AZ design | k03-mc, k03-mr | 2 |
| DR strategy tiers (RTO/RPO) | k04-mc | 1 |
| Distributed design pattern vs single-instance SPOF | k05-mc | 1 |
| RDS Multi-AZ instance vs cluster vs read replica vs Aurora Global Database | k06-mc | 1 |
| Compute-tier failover (ALB/ASG health checks) vs DB/DNS-layer failover | k06-mr | 1 |
| Immutable infrastructure vs in-place patching | k07-mc | 1 |
| Cross-zone load balancing vs health-check/DNS distribution | k08-mc | 1 |
| RDS Proxy vs other RDS HA options / vs its own two benefits | k09-mc, k09-mr | 2 |
| Service Quotas planning for standby/DR capacity | k10-mc | 1 |
| Storage durability & access-pattern fit (S3 vs EBS vs EFS vs One Zone-IA) | k11-mc | 1 |
| CloudWatch vs X-Ray observability scope | k12-mc, k12-mr | 2 |

Every type is used at most twice, within the 16 slots owned by writer A. No type exceeds the task-wide limit of 4 across all 32 questions (writer B's contribution unknown at time of writing, but writer A's own usage caps each type at 2).

## Lesson additions requested

- **K08 citation gap (pre-existing, not introduced by this change):** the lesson's own `citationIds` list ties K08 only to `cite-saa-2-2-elb-healthchecks` (AWS's ALB target-group-health-checks page), but the lesson's K08 body text also asserts a specific fact this citation's note does not verify: that cross-zone load balancing is *on by default* for an ALB and spreads requests evenly across all healthy targets regardless of AZ. `q-saa-2-2-k08-mc` tests this exact fact and cites the same id per the "reuse the lesson's citation ids" instruction, but Lead Dev / AWS may want a dedicated citation (e.g. the ALB cross-zone load balancing doc page) added to the lesson so K08's claim has its own verified source rather than borrowing the health-checks page's citation.

No other facts were needed beyond what lesson-2-2.json already teaches; all 16 keys and all distractors trace to a sentence quoted in the table above.

## Lead Dev review fixes

Re-ran `scripts\content_lint.py` (PASS, 429/310/119) and the writer-A verification script after every fix below. Final state: 0 letter references, 0 pasted objective text, 0 six-word stem collisions, MC keys still 3/3/3/3 across a–d, MR keys still spread a=2/b=1/c=1/d=2/e=2, longest-choice-is-key now 3/12 = 25% (down from 33%). `q-saa-2-2-k08-mc`'s Lead-Dev-added citation `cite-saa-2-1-alb-cross-zone` was kept as-is.

| # | File | Issue | Old | New |
|---|---|---|---|---|
| 1 | k06-mc | Choices a/b echoed the stem, so b stated its own justification | a: "Deploy a Multi-AZ DB instance, which keeps one non-readable standby for automatic failover"; b: "Deploy a Multi-AZ DB cluster, which keeps two readable standby instances across three AZs and adds automatic failover"; c: "Deploy a single read replica in a second Availability Zone to add read capacity"; d: "Deploy an Aurora Global Database with a secondary cluster in another Region" | a: "A Multi-AZ DB instance deployment"; b: "A Multi-AZ DB cluster deployment"; c: "A single read replica in a second Availability Zone"; d: "An Aurora Global Database with a secondary cluster in another Region". Rationale rewritten to carry all the explanatory content that used to live in the choice text. |
| 2 | k08-mc d | Self-explaining choice ("enabled by default… spreading requests evenly…") | "Cross-zone load balancing, enabled by default on the Application Load Balancer, is spreading requests evenly across every healthy target regardless of AZ" | "Cross-zone load balancing on the Application Load Balancer". Rationale updated to state the default-on/even-spread fact instead of the choice text. |
| 3a | k05-mc b | Strawman (no real candidate would pick "keep resizing one instance" as a genuine HA fix) | "Continue resizing the single instance to a larger instance type within the same subnet as demand grows" | "Add a second EC2 instance in the same Availability Zone as the first, behind a load balancer with health checks" — a real config that survives a single-host failure but not an AZ failure, so it still fails the stated requirement for exactly one reason. Rationale updated to explain the AZ-level gap instead of dismissing the choice as just "resizing." |
| 3b | k10-mc d | Strawman ("wait until the next disaster to request a quota increase" — no real operator plan) | "Wait until the next failover event and request the increase through a support case at that point" | "Configure a Route 53 failover record pointing at the recovery Region" — a real, lesson-taught mechanism that correctly routes traffic to the recovery Region but does nothing about the vCPU quota, so it still fails on the one stated requirement. Added `cite-saa-2-2-route53-failover` to `citationIds` since the distractor now rests on a specific lesson fact, and rewrote the rationale's fourth sentence to explain the gap. |
| 4 | k09-mr a/b/e | Distractors named unrelated services (Multi-AZ DB instance, Aurora Global Database, read-replica promotion) that no candidate would mistake for an RDS Proxy benefit | a: "Provisions a Multi-AZ DB instance to add a non-readable standby"; b: "Creates an Aurora Global Database secondary cluster in another Region"; e: "Promotes a read replica to reduce read traffic on the primary" | a: "Adds readable standby capacity for the database in other Availability Zones"; b: "Replicates the database to a secondary cluster in another Region"; e: "Removes the need for a Multi-AZ deployment because the proxy stores the data itself" — each is now phrased as a false claim about RDS Proxy's own behavior (or what it would let you skip), not a description of a different, obviously unrelated service. Rationale rewritten to name which real feature (Multi-AZ DB cluster / Aurora Global Database / Multi-AZ deployment) each false claim is actually describing, and to state plainly that RDS Proxy does none of those things. Keys unchanged (c, d). |
| 5 | k12-mr b/c/d | Question joined two needs (alarm-triggered scaling + tracing) but three distractors (Route 53 health check, RDS Proxy, AWS Backup) answered neither half | b: "Configure a Route 53 health check to fail over DNS to a secondary endpoint"; c: "Configure RDS Proxy to pool database connections from the checkout fleet"; d: "Schedule AWS Backup jobs to protect the checkout database" | b: "Configure a Route 53 health check on the checkout endpoint to detect when it stops responding" (plausible-wrong answer to the alarm/scaling half — reports up/down, not a latency metric that can trigger scaling); c: "Search aggregated application logs with CloudWatch Logs Insights for the affected time window" (plausible-wrong answer to the tracing half); d: "Add a custom CloudWatch dashboard widget that graphs per-service latency" (plausible-wrong answer to the tracing half). Rationale rewritten so every distractor is refuted against the specific half of the requirement it's closest to. Keys unchanged (a, e). |
| 6a | k03-mc a/b | Distractors a and b were the same idea repeated ("keep the shared NAT gateway in AZ-A, just add another route table pointing at it" vs. "move both AZs onto the main route table pointing at it") | a: "Keep the single NAT gateway in AZ-A, but add a second route table copy for AZ-B that still targets it"; b: "Move both AZs' private subnets onto the VPC's main route table, pointed at the AZ-A NAT gateway" | a: "Replace the NAT gateway with a NAT instance in AZ-A, but keep referencing it from both AZs' route tables" (distinct idea: swapping the NAT technology, not the sharing pattern); b unchanged in substance ("Move both AZs' private subnets onto the VPC's main route table, pointed at the AZ-A NAT gateway") — now the only "shared main route table" distractor, since a no longer duplicates it. Rationale rewritten to match. |
| 6b | k03-mr c | Distractor c ("remove the per-AZ route tables and use only the main route table") overlapped with distractor b's "shared NAT gateway" idea | "Remove the per-AZ route tables and let both AZs rely on the VPC's main route table alone" | "Give AZ-A its own dedicated NAT gateway, but leave AZ-B's route table still pointed at AZ-A's NAT gateway" — a distinct idea (a half-finished fix that only corrects AZ-A), rather than a second variant of "everything shares one route table." Rationale rewritten to explain the partial-fix gap. The NAT-instance option in choice e was kept as-is per Lead Dev's note that it was already a good, distinct distractor. Keys unchanged (a, d). |
