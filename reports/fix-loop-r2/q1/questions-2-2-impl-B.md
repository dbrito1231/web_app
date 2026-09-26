# Task 2.2 question rewrite — writer B (skill questions s01–s08)

Scope: `content/questions/q-saa-2-2-s{01..08}-{mc,mr}.json` (16 files). No `k*` files, no `lesson-2-2.json`, no `q-saa-2-1-*` touched. No new citation files were needed — all 25 citations already attached to `lesson-2-2.json` covered every fact used.

## Lead Dev review fixes

All fixes below were re-verified: unique 6-word openings, 0 letter references, 0 objective text, MC longest-is-key 2/8 = 25%, MC keys a/b/c/d = 2 each, MR key slots a–e = 4/3/3/3/3, all citations resolve, `content_lint.py` PASS.

**1. Self-explaining / giveaway wording**

| File | Choice | Old | New |
|---|---|---|---|
| s01-mc | a | "Provision infrastructure from templates, and apply urgent configuration fixes directly in the console **when a redeploy is inconvenient**." | "Provision infrastructure from templates, and make configuration fixes directly in the console for routine changes." |
| s01-mc | b | "Continue to apply patches directly to the running fleet on a recurring schedule, **without changing how those patches are deployed**." | "Apply patches directly to the running fleet on a recurring schedule." |
| s01-mc | c | "Rely on an Auto Scaling group's health checks **alone** to terminate and relaunch any instance that fails a check." | "Use an Auto Scaling group's health checks to terminate and relaunch any instance that fails a check." |
| s01-mr | c | "...on a fixed schedule, **leaving the deployment process unchanged**." | "Apply patches directly to the currently running fleet on a fixed schedule." |
| s01-mr | d | "...to replace failed instances, **without changing how deployments are made**." | "Rely on Auto Scaling health checks to replace any instance that fails a check." |
| s01-mr | e | "...for the fleet's volumes, **without changing how deployment changes are applied**." | "Schedule AWS Backup's policy-based backups for the fleet's volumes." |
| s03-mc | a | "An availability target of 99.9%, **the next tier down**." | "An availability target of 99.9% for the same annual downtime budget." |
| s07-mr | c | "RDS Proxy, **to pool the many short-lived connections onto fewer database connections**." | "RDS Proxy, placed between the application and the database." |
| s07-mr | d | "AWS Elastic Disaster Recovery, **to launch a replacement server from continuous replication within minutes**." | "AWS Elastic Disaster Recovery, configured for the application server." |
| s05-mc | b | "Enable AWS Backup Vault Lock in compliance mode **on a vault that has no backup plan attached to it**." | "Enable AWS Backup Vault Lock in compliance mode on the existing backup vault." (rationale reworded to explain Vault Lock governs retention of existing backups rather than scheduling them, without naming the flaw in the choice text) |

**2. Strawmen replaced with real, lesson-taught near-misses**

| File | Choice | Old (strawman) | New (real option, wrong for one requirement) |
|---|---|---|---|
| s04-mr | a | "Increase the single instance's instance size to handle more load." | "Add an Application Load Balancer with health checks in front of the single instance, without placing it in an Auto Scaling group." — real, meets the health-check requirement but not redundancy. Added `cite-saa-2-2-elb-healthchecks`. |
| s07-mc | b | "Add a health-check endpoint and failover logic inside the application's own code" (directly contradicts the stem's no-code-change constraint). | "Use Amazon Route 53 failover routing with health checks, pointing at a single instance as the primary endpoint." — real, no code change, but wrong granularity/speed versus a load balancer. Added `cite-saa-2-2-route53-failover`. |
| s02-mr | b | "An Application Load Balancer spanning only the Availability Zones of the primary Region." | "AWS Elastic Disaster Recovery, replicating the application's servers into a staging area in the second Region." — real, cross-Region, but the servers stay dormant and it does not route live traffic or replicate storage. Swapped citation `elb-healthchecks` → `drs`. |
| s05-mr | b | "Grant the backup administrator role permission to override the lock in an emergency." | Rebuilt as part of fix 3 below (now "A mandatory grace period of 24 hours before the lock becomes final."). |

**3. s05-mr reworked**

Old correct pair: "Lock the vault in compliance mode" + "Wait out the mandatory cooling-off period of at least 72 hours before treating the lock as final" (read as an odd action). New correct pair states two parallel facts: "Lock the vault in compliance mode." and "A mandatory grace period of at least 72 hours before the lock becomes final." Distractors rebuilt to match the same neutral, fact-style shape: "Lock the vault in governance mode instead of compliance mode.", "A mandatory grace period of 24 hours before the lock becomes final." (wrong number), "Configure AWS Backup's cross-Region copy for the vault's recovery points." (real but doesn't lock retention). Rationale and citations (`backup-vault-lock`, `aws-backup`; dropped `s3-crr`) updated to match.

**4. s08-mr — DynamoDB ambiguity fixed**

Stem changed from "...a script that replicates **a table's rows**..." to "...a script that replicates **a DynamoDB table's items**..." so Aurora Global Database (a relational/Aurora-only feature) is unambiguously wrong rather than arguably applicable. Rationale for that distractor now states explicitly that Aurora Global Database is a relational-database feature that does not apply to a DynamoDB table.

**5. s03-mr — implausible distractors replaced**

| Choice | Old | New |
|---|---|---|
| c | "A CloudWatch alarm threshold set on a single metric." | "A durability percentage, such as 99.999999999% (eleven nines)." (grounded in lesson K11) |
| d | "An AWS X-Ray trace showing latency across a chain of services." | "A service quota, such as an EC2 vCPU limit in the recovery Region." (grounded in lesson K10) |

Citations swapped from `cloudwatch`/`xray` to `s3-durability`/`service-quotas`; rationale rewritten to explain each as a real but differently-scoped metric rather than an implausible non-answer.

## Metrics

| Check | Result |
|---|---|
| Files written | 16/16, valid JSON via `json.load`/`json.dumps(indent=2, ensure_ascii=True)` |
| `content_lint.py` | PASS (`questions 429 aws 310 tf 119`) |
| Unique 6-word stem openings | 16/16 unique, 0 duplicates |
| Objective text pasted verbatim in stem | 0 |
| Letter references (`choice a`, `option b`, etc.) | 0 |
| `citationIds` present, `mcpStatus: verified`, `reviewedOn: 2026-09-26` | 16/16 |
| Citations resolve to existing files | 16/16 |
| MC longest choice = key | 2/8 = 25% (≤35% target) |
| MC key letter spread | a:2, b:2, c:2, d:2 |
| MR key-slot spread (16 correct slots over a–e) | a:4, b:3, c:3, d:3, e:3 |
| id/type/module/objectiveIds/selectCount unchanged | yes (module `A2`, ids/objectiveIds/selectCount untouched) |
| MC = 4 choices, MR = 5 choices, exact select counts | 16/16 |
| Stems starting with a company/team noun phrase (writer A's pattern) | 0 |

Doc facts double-checked against AWS docs via `search_documentation` (AWS Knowledge MCP):
- DynamoDB global tables MREC uses last-writer-wins conflict resolution on simultaneous item writes (`amazondynamodb/latest/developerguide/globaltables_HowItWorks.html`) — backs Q3 and Q16.
- AWS Backup Vault Lock compliance mode is immutable to all users including root, with a minimum 72-hour (three-day) cooling-off period before the lock is final (`aws-backup/latest/devguide/vault-lock.html`) — backs Q10 and Q16.
Both match the lesson's existing `cite-saa-2-2-ddb-global-tables` and `cite-saa-2-2-backup-vault-lock` citations, so no citation edits or "Lesson additions requested" were needed.

## Per-question table

| # | id | Objective | What it tests | Key | Lesson sentence(s) grounding key/distractors | Doc URL |
|---|---|---|---|---|---|---|
| 1 | q-saa-2-2-s01-mc | S01 | Recognizing immutable deployment vs. in-place patch/console-edit/ASG-only as "closes the pipeline gap" | Deploy as new image/template, replace resource | K07 "no in-place updates... every change ships as a new image or template"; S01 "deploy application changes as immutable infrastructure... let Auto Scaling health checks replace failed instances" | docs.aws.amazon.com (immutable infra pattern, Well-Architected) |
| 2 | q-saa-2-2-s01-mr | S01 | Same automation gap, two correct fixes (immutable deploy + IaC provisioning) vs. in-place patch/ASG-only/backup-only | Immutable image deploy; IaC provisioning | Same S01/K07 text plus S05 "AWS Backup's policy-based schedules" (used as a plausible-but-off-topic distractor) | same |
| 3 | q-saa-2-2-s02-mc | S02 | DynamoDB global tables (multi-active, conflict-resolved) vs. Aurora Global Database (read-only secondary), RDS Multi-AZ (AZ-scope), S3 CRR (object storage) | DynamoDB global tables | S02 "DynamoDB global tables (multi-Region, multi-active replication... conflicting writes resolved last-writer-wins)"; K06 "Aurora Global Database extends... secondary, read-only clusters" | docs.aws.amazon.com/amazondynamodb/.../globaltables_HowItWorks.html |
| 4 | q-saa-2-2-s02-mr | S02 | Region-spanning traffic (Route 53) + storage (S3 CRR) vs. AZ-scoped RDS/ALB and S3 One Zone-IA | Route 53 spanning policy; S3 CRR | S02 "a Route 53 policy that spans the Regions... S3 Cross-Region Replication"; K11 "S3 One Zone-IA, which trades that redundancy... using a single AZ" | docs.aws.amazon.com/Route53, S3 storage classes |
| 5 | q-saa-2-2-s03-mc | S03 | Converting an annual downtime budget into the correct nines target vs. RTO/RPO confusion | 99.99% availability | S03 "99.9% allows roughly 8.7 hours... 99.99% allows roughly 52 minutes" | Well-Architected reliability pillar |
| 6 | q-saa-2-2-s03-mr | S03 | RTO + RPO as the two explicit numbers vs. aggregate availability %, CloudWatch alarm, X-Ray trace | RTO; RPO | S03 "RTO is the maximum acceptable downtime and RPO the maximum acceptable data loss"; K12 CloudWatch/X-Ray distinction | Well-Architected, CloudWatch/X-Ray docs |
| 7 | q-saa-2-2-s04-mc | S04 | Per-AZ NAT gateway/route table vs. same-AZ redundancy, IGW-on-private-subnet, default main route table | One NAT gateway + route table per AZ | K03 "one NAT gateway and one route table per AZ, so each AZ's outbound path survives independently" | VPC route tables docs |
| 8 | q-saa-2-2-s04-mr | S04 | ASG multi-AZ + RDS Multi-AZ as SPOF fixes vs. vertical scaling, manual snapshot, read replica | ASG spanning AZs; RDS Multi-AZ | S04 SPOF list; K06 "read replica... not to fail over automatically" | ASG/RDS Multi-AZ docs |
| 9 | q-saa-2-2-s05-mc | S05 | AWS Backup scheduled/PITR vs. faster replication, Vault Lock without a plan, read replica | AWS Backup scheduled backups | S05 "replication alone still propagates an accidental delete to every replica... combine continuous replication... with scheduled AWS Backup snapshots for point-in-time recovery" | AWS Backup docs |
| 10 | q-saa-2-2-s05-mr | S05 | Compliance mode + 72h cooling-off vs. governance mode, admin override, CRR | Compliance mode; wait out cooling-off period | S05 "compliance mode, which becomes immutable... once a mandatory cooling-off period of at least 72 hours expires" | aws-backup/latest/devguide/vault-lock.html (re-verified) |
| 11 | q-saa-2-2-s06-mc | S06 | Cheapest strategy meeting a 24h/hours-RPO requirement among the four DR tiers | Backup and restore | K04 DR tier table | Well-Architected DR strategies |
| 12 | q-saa-2-2-s06-mr | S06 | Two strategies meeting a seconds-level RPO (warm standby, active/active) vs. backup/pilot light/Multi-AZ | Warm standby; multi-site active/active | K04 DR tier table | same |
| 13 | q-saa-2-2-s07-mc | S07 | ALB/NLB health-checked failover for an unmodifiable legacy app vs. code change, DRS, RDS Proxy | ALB/NLB in front of the fleet | S07 "An ALB or NLB in front of a legacy fleet adds health-checked failover the application was never written to do itself" | ELB health check docs |
| 14 | q-saa-2-2-s07-mr | S07 | RDS Proxy (connections) + AWS DRS (server recovery) for a legacy app vs. ALB, AWS Backup, RDS Multi-AZ | RDS Proxy; AWS DRS | S07 "RDS Proxy improves resiliency for a legacy application that opens many short-lived... connections"; "AWS DRS... can launch fully booted recovery instances on AWS within minutes" | RDS Proxy / DRS docs |
| 15 | q-saa-2-2-s08-mc | S08 | Route 53 failover routing as the purpose-built replacement for a DIY DNS-flip script vs. Lambda-scripted equivalent, CloudWatch+human, DRS | Route 53 failover + health checks | S08 "Route 53 health-checked failover instead of a custom heartbeat-and-DNS script" | Route 53 failover docs |
| 16 | q-saa-2-2-s08-mr | S08 | AWS Backup + DynamoDB global tables replacing two homegrown scripts vs. Vault Lock alone, Aurora Global DB, DRS | AWS Backup; DynamoDB global tables | S08 "AWS Backup instead of custom snapshot scripts, DynamoDB global tables instead of hand-rolled cross-Region replication with conflict resolution" | AWS Backup / DynamoDB global tables docs |

## Distractor-type table (my 16 questions)

| Type | Questions | Count |
|---|---|---|
| Immutable/IaC vs. in-place patch or partial automation (ASG-only, backup-only) | s01-mc, s01-mr | 2 |
| Aurora Global Database (read-only secondary) mistaken for a multi-writer/Region-scope answer | s02-mc, s08-mr | 2 |
| S3 Standard vs. One Zone-IA | s02-mr | 1 |
| RTO/RPO vs. availability-percentage confusion | s03-mc | 1 |
| CloudWatch vs. X-Ray | s03-mr | 1 |
| NAT gateway / route table per-AZ vs. shared/default route table | s04-mc | 1 |
| Multi-AZ DB instance vs. read replica (no auto-failover) | s04-mr | 1 |
| Backup vs. replication vs. PITR | s05-mc | 1 |
| Backup Vault Lock governance vs. compliance mode | s05-mr, s08-mr | 2 |
| Four DR tiers (RPO/RTO ordering) | s06-mc, s06-mr | 2 |
| RDS Proxy misapplied to traffic failover instead of connection pooling | s07-mc | 1 |
| AWS DRS / AWS Backup / RDS Multi-AZ misapplied to a different recovery need | s07-mr | 1 |
| Purpose-built Route 53 failover vs. DIY scripted equivalent (Lambda+API, CloudWatch+human) | s08-mc | 1 |

No type exceeds 2 of my 16 questions; the whole task's cap (4 of 32) depends on writer A's k-file tally, which is outside this report.

## Lesson additions requested

None. Every key and every distractor across all 16 questions is a service, configuration, or concept `lesson-2-2.json` already names and explains (immutable infrastructure/K07, IaC/S01, ASG multi-AZ/K06/S04, RDS Multi-AZ instance vs. cluster vs. read replica vs. Aurora Replica vs. Aurora Global Database/K06, Route 53 routing and failover/K01/K06, S3 storage classes and CRR/K11/S05, AWS Backup and Vault Lock/S05, DynamoDB global tables MREC/MRSC/S02, RDS Proxy/K09/S07, AWS DRS/S07/S08, CloudWatch vs. X-Ray/K12, VPC route tables/K03, the four DR strategies/K04, RTO/RPO/K04/S03). No doc-verified fact outside the lesson's own text was required.
