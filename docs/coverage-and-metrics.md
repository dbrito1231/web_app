# Coverage and metrics

Curriculum coverage registry, readiness formulas, MCP validation, and baseline audit. Spec version 1. Implements REQ-P30–P35, REQ-P15. Access date: 2026-09-23.

Primary sources:

- Supplied PDF: `solutions-architect-associate-03.pdf` (SAA-C03 exam guide, copyright 2026 Amazon Web Services). 30 physical pages; printed pages 1–26 map to physical pages 5–30 (add 4).
- Coverage contract: `C:\Users\dbadmin\Downloads\cursor_saa_c03_exam_objectives_coverage.md`
- Terraform Associate (004): [exam content list](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004). Objectives 1a–1c through 8a–8d (37 lettered). Weights, item count, and passing score stay `unpublished`. Cover both wordings of 4f and 4h.

Local tracking IDs such as `SAA-1.1-K01` are project IDs, not AWS-issued.

## Discrepancy log (2026-09-23)

REQ-C01. PDF is authoritative for which bullets exist.

| Item | Disposition |
| --- | --- |
| Online edition lists AWS AppSync (twice), Amazon Kendra, AWS Audit Manager; supplied PDF does not | Record as `edition_variance`; teach at awareness level; exclude from service denominator |
| `SAA-2.2-K02` examples list AMS with Comprehend / Polly | Preserve PDF wording; do not teach Comprehend or Polly as AMS components; add flagged current-docs note when authored |
| Guide names Amazon Quick, Amazon SageMaker AI | Keep guide names; add cited current-status note when branding differs |
| Amazon Redshift listed in two PDF categories | Preserve both placements; dedupe for unique-service counts |

## MCP validation (authors/reviewers, not the app)

REQ-C10. AWS items: AWS Knowledge MCP Server (`search_documentation` / `read_documentation`). Store official URL and accessed date.

REQ-C11. Terraform items: Terraform MCP Server **registry/docs tools only**. No HCP workspace create/update/delete/run. Store registry or HashiCorp URL and accessed date.

REQ-C12. If PDF and MCP disagree: keep PDF wording, flag a note, log the discrepancy. Phase 3, 4, and 6 content tasks do not start if these servers are missing.

## Stable identifiers

Examples: `SAA-1.1-K01`, `tf.004.4f`, `lesson.m6.workflow`, `q.m6.014`, `lab.gl07`, `lab.ul07`, `DE-*`.

## Registry row fields

`objective_id`, `domain`, `task`, `ks`, `source_text`, `lesson_refs`, `drill_refs`, `guided_refs`, `unguided_refs`, `exercise_refs`, `practice_mode`, `constraint_reason`, `validation_refs`, `status` (`missing` \| `planned` \| `partial` \| `implemented_unverified` \| `verified`), `gap`, `owner`, `next_action`.

## Curriculum coverage formulas (workbook, not learner)

Half-up whole percents:

- Verified atomic = verified / 189 × 100
- Domain coverage against 32 / 43 / 50 / 64
- Weighted guide coverage = 0.30×D1 + 0.26×D2 + 0.24×D3 + 0.20×D4
- Task and K/S counts separate; live vs design-exercise separate; planned vs verified separate
- Service awareness uses its own denominator (Redshift deduped; `edition_variance` excluded)
- None of these is a pass probability or scaled score

## Learner metrics

- Lesson completion = read / in scope (exposure, not mastery)
- Drill completion = distinct attempted ids / in scope
- Accuracy = correct first-attempt exam-mode / first-attempt exam-mode (“no attempts” if denominator 0)
- Lab completion = all checkpoints self-reported; cleanup recorded separately
- Mastery “not assessed” until attempts exist

## Readiness formula (locked)

Not a pass probability. Integer display. Caption: weighted summary of this workbook’s practice, not a prediction.

```
readiness = round(100 * (0.70 * weightedFirstAttemptAccuracy + 0.20 * objectiveCoverage + 0.10 * recentAccuracy))
```

- AWS withheld until ≥40 first-attempt exam-mode items and ≥5 in each of 4 domains; else “insufficient evidence” plus missing counts.
- Terraform withheld until ≥30 first-attempt exam-mode items and ≥2 in each of 8 groups.
- Recent accuracy: last 14 days if those 14 days have ≥10 items; else the 0.10 weight moves onto first-attempt accuracy.
- AWS domain weights in the formula: 30/26/24/20, renormalized across domains with attempts.
- Terraform: equal group weights; state that HashiCorp publishes none.
- Objective coverage in the formula = fraction of atomic AWS bullets (or Terraform lettered objectives) with at least one first-attempt item. Not lessons read. Not curriculum coverage.
- Assisted attempts excluded. No partial-credit path.
- Confidence: `low` just above threshold; `medium` at ≥80 AWS or ≥60 Terraform items with every domain/group represented. Never “likely to pass.”
- Trend vs score stored 7 days earlier, in percentage points. If either side was insufficient evidence, say that instead of a delta.

## Mock exam

50 items, 15/13/12/10 by domain. Raw score out of 50 and by domain. Never 100–1000 scaled; never compared to 720.

## 14-task rollup (skeleton)

All statuses currently `missing`. Domain weights are official; bullet counts are project coverage units.

| Task | Domain | Weight | K | S | Total | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1.1 | 1 | 30% | 5 | 6 | 11 | missing |
| 1.2 | 1 | 30% | 6 | 4 | 10 | missing |
| 1.3 | 1 | 30% | 4 | 7 | 11 | missing |
| 2.1 | 2 | 26% | 16 | 7 | 23 | missing |
| 2.2 | 2 | 26% | 12 | 8 | 20 | missing |
| 3.1 | 3 | 24% | 3 | 2 | 5 | missing |
| 3.2 | 3 | 24% | 6 | 4 | 10 | missing |
| 3.3 | 3 | 24% | 8 | 5 | 13 | missing |
| 3.4 | 3 | 24% | 4 | 4 | 8 | missing |
| 3.5 | 3 | 24% | 7 | 7 | 14 | missing |
| 4.1 | 4 | 20% | 11 | 10 | 21 | missing |
| 4.2 | 4 | 20% | 9 | 6 | 15 | missing |
| 4.3 | 4 | 20% | 9 | 5 | 14 | missing |
| 4.4 | 4 | 20% | 7 | 7 | 14 | missing |
| **Sum** | | | **107** | **82** | **189** | |

Domain totals: D1=32, D2=43, D3=50, D4=64.

## Terraform Associate (004) outline

Letter groups (37 lettered). Separate readiness and bank from SAA.

| Group | Letters (count) | Bank floor |
| --- | --- | ---: |
| 1 | 1a–1c (3) | ≥3 each / ≥9 group contribution toward 111 |
| 2 | 2a–2d (4) | ≥3 each |
| 3 | 3a–3g (7) | ≥3 each |
| 4 | 4a–4h (8) | ≥3 each; cover both 4f and 4h wordings |
| 5 | 5a–5d (4) | ≥3 each |
| 6 | 6a–6d (4) | ≥3 each |
| 7 | 7a–7c (3) | ≥3 each |
| 8 | 8a–8d (4) | ≥3 each; HCP no-charge only |

Overall Terraform bank floor: ≥111 items.

## Service awareness map (in-scope from PDF)

Status for every named service: `missing` awareness content. Deduped Redshift counts once. `edition_variance` (AppSync, Kendra, Audit Manager) excluded from denominator.

Categories (PDF pp. 16–22): Analytics; Application Integration; Business Applications; Cloud Financial Management; Compute; Containers; Database; Developer Tools (in-scope subset per PDF); Front-End Web and Mobile; Machine Learning; Management and Governance; Media Services; Migration and Transfer; Networking and Content Delivery; Security, Identity, and Compliance; Serverless; Storage.

Out-of-scope tooling/guardrail services (PDF pp. 22–25) must not inflate the SAA service denominator (MWAA, Sumerian, Managed Blockchain, Lightsail, RDS on VMware, CDK/Code* family, IoT all, Braket, Ground Station, etc. — full list in coverage contract).

## Gap report (Phase 0)

| Gap | Severity | Owner phase | Notes |
| --- | --- | --- | --- |
| All 189 rows `missing` | blocking | 3–6 | No lessons, drills, labs, or design exercises yet |
| Terraform 37 lettered objectives unmapped | blocking | 3–4 | Separate from SAA registry |
| Service awareness content empty | high | 3 | Deduped inventory not yet authored |
| Design exercises for non-lab skill bullets | high | 4 | DE-* catalog not started |
| Lab prices unfinished (RDS, EBS, …) | medium | 5 | Fill from official pages before verified |
| Layout tabs Exam drills / Coverage / Start here not live-captured | medium | before P1 | Patch layout plan after Claude sign-in |
| MCP servers not yet confirmed enabled | ~~high for P3+~~ | done 2026-09-24 | Sample re-check in `docs/citation-recheck.md` |

Verified atomic coverage: **0 / 189 (0%)**. Weighted guide coverage: **0%**.

## Proposed mappings (planning only)

| Module | Objectives | Proposed labs | Proposed drills |
| --- | --- | --- | --- |
| A0 | Safety, shared responsibility, MFA, budgets, tags (`SAA-1.1-K05`, `SAA-1.1-S01`, Domain 4 cost tools) | GL-01 | ≥20 MC/MR |
| A1 | Domain 1 (32) | GL-01–04 | ≥36 domain share of AWS bank |
| A2 | Domain 2 (43) | GL-05–11 | ≥48 |
| A3 | Domain 3 (50) | GL-07–19 selective | ≥56 |
| A4 | Domain 4 (64) | Cost-focused steps + DE-* | ≥70 |
| T1–T4 | tf.004.* | GL-20–21 | ≥111; ≥20/module |

Skill bullets without disposable live services → `design_exercise` with rubric (see `docs/labs-and-safety.md`).

## Budget decisions (locked)

- $10 is a warning, not a retain/stop rule (confirmed 2026-09-23).
- Learner accepted spend above $10 for hands-on labs.
- Alert-only budget; no budget actions.
- Expensive services remain in labs the learner runs; agents never create them.

## 189-row registry skeleton

Every row `status=missing`. Generated from the coverage contract on 2026-09-23. Count must remain exactly 189.

| objective_id | domain | task | ks | status | practice_mode | lesson_refs | drill_refs | guided_refs | unguided_refs | exercise_refs | constraint_reason | validation_refs | gap | owner | next_action | source_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAA-1.1-K01 | 1 | 1.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Access controls and management across multiple accounts |
| SAA-1.1-K02 | 1 | 1.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS federated access and identity services (for example, IAM, AWS IAM Identity Center) |
| SAA-1.1-K03 | 1 | 1.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS global infrastructure (for example, Availability Zones, AWS Regions) |
| SAA-1.1-K04 | 1 | 1.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS security best practices (for example, the principle of least privilege) |
| SAA-1.1-K05 | 1 | 1.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | The AWS shared responsibility model |
| SAA-1.1-S01 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Applying AWS security best practices to IAM users and root users (for example, multi-factor authentication [MFA]) |
| SAA-1.1-S02 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing a flexible authorization model that includes IAM users, groups, roles, and policies |
| SAA-1.1-S03 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing a role-based access control strategy (for example, AWS STS, role switching, cross-account access) |
| SAA-1.1-S04 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing a security strategy for multiple AWS accounts (for example, AWS Control Tower, service control policies [SCPs]) |
| SAA-1.1-S05 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the appropriate use of resource policies for AWS services |
| SAA-1.1-S06 | 1 | 1.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining when to federate a directory service with IAM roles |
| SAA-1.2-K01 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Application configuration and credentials security |
| SAA-1.2-K02 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS service endpoints |
| SAA-1.2-K03 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Control ports, protocols, and network traffic on AWS |
| SAA-1.2-K04 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Secure application access |
| SAA-1.2-K05 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Security services with appropriate use cases (for example, Amazon Cognito, Amazon GuardDuty, Amazon Macie) |
| SAA-1.2-K06 | 1 | 1.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Threat vectors external to AWS (for example, DDoS, SQL injection) |
| SAA-1.2-S01 | 1 | 1.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing VPC architectures with security components (for example, security groups, route tables, network ACLs, NAT gateways) |
| SAA-1.2-S02 | 1 | 1.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining network segmentation strategies (for example, using public subnets and private subnets) |
| SAA-1.2-S03 | 1 | 1.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Integrating AWS services to secure applications (for example, AWS Shield, AWS WAF, IAM Identity Center, AWS Secrets Manager) |
| SAA-1.2-S04 | 1 | 1.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Securing external network connections to and from the AWS Cloud (for example, VPN, AWS Direct Connect) |
| SAA-1.3-K01 | 1 | 1.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data access and governance |
| SAA-1.3-K02 | 1 | 1.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data recovery |
| SAA-1.3-K03 | 1 | 1.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data retention and classification |
| SAA-1.3-K04 | 1 | 1.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Encryption and appropriate key management |
| SAA-1.3-S01 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Aligning AWS technologies to meet compliance requirements |
| SAA-1.3-S02 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Encrypting data at rest (for example, AWS KMS) |
| SAA-1.3-S03 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Encrypting data in transit (for example, AWS Certificate Manager [ACM] using TLS) |
| SAA-1.3-S04 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing access policies for encryption keys |
| SAA-1.3-S05 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing data backups and replications |
| SAA-1.3-S06 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing policies for data access, lifecycle, and protection |
| SAA-1.3-S07 | 1 | 1.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Rotating encryption keys and renewing certificates |
| SAA-2.1-K01 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | API creation and management (for example, Amazon API Gateway, REST API) |
| SAA-2.1-K02 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS managed services with appropriate use cases (for example, AWS Transfer Family, Amazon SQS, AWS Secrets Manager) |
| SAA-2.1-K03 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Caching strategies |
| SAA-2.1-K04 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Design principles for microservices (for example, stateless workloads compared with stateful workloads) |
| SAA-2.1-K05 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Event-driven architectures |
| SAA-2.1-K06 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Horizontal scaling and vertical scaling |
| SAA-2.1-K07 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | How to appropriately use edge accelerators (for example, content delivery network [CDN]) |
| SAA-2.1-K08 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | How to migrate applications into containers |
| SAA-2.1-K09 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Load balancing concepts (for example, Application Load Balancer [ALB]) |
| SAA-2.1-K10 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Multi-tier architectures |
| SAA-2.1-K11 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Queuing and messaging concepts (for example, publish/subscribe) |
| SAA-2.1-K12 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Serverless technologies and patterns (for example, AWS Fargate, AWS Lambda) |
| SAA-2.1-K13 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage types with associated characteristics (for example, object, file, block) |
| SAA-2.1-K14 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | The orchestration of containers (for example, Amazon ECS, Amazon EKS) |
| SAA-2.1-K15 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | When to use read replicas |
| SAA-2.1-K16 | 2 | 2.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Workflow orchestration (for example, AWS Step Functions) |
| SAA-2.1-S01 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing event-driven, microservice, and/or multi-tier architectures based on requirements |
| SAA-2.1-S02 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining scaling strategies for components used in an architecture design |
| SAA-2.1-S03 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the AWS services required to achieve loose coupling based on requirements |
| SAA-2.1-S04 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining when to use containers |
| SAA-2.1-S05 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining when to use serverless technologies and patterns |
| SAA-2.1-S06 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Recommending appropriate compute, storage, networking, and database technologies based on requirements |
| SAA-2.1-S07 | 2 | 2.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Using purpose-built AWS services for workloads |
| SAA-2.2-K01 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS global infrastructure (for example, Availability Zones, AWS Regions, Amazon Route 53) |
| SAA-2.2-K02 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS Managed Services (AMS) with appropriate use cases (for example, Amazon Comprehend, Amazon Polly) |
| SAA-2.2-K03 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Basic networking concepts (for example, route tables) |
| SAA-2.2-K04 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Disaster recovery (DR) strategies (for example, backup and restore, pilot light, warm standby, active-active failover, recovery point objective [RPO], recovery time objective [RTO]) |
| SAA-2.2-K05 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Distributed design patterns |
| SAA-2.2-K06 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Failover strategies |
| SAA-2.2-K07 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Immutable infrastructure |
| SAA-2.2-K08 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Load balancing concepts (for example, ALB) |
| SAA-2.2-K09 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Proxy concepts (for example, Amazon RDS Proxy) |
| SAA-2.2-K10 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Service quotas and throttling (for example, how to configure the service quotas for a workload in a standby environment) |
| SAA-2.2-K11 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage options and characteristics (for example, durability, replication) |
| SAA-2.2-K12 | 2 | 2.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Workload visibility (for example, AWS X-Ray) |
| SAA-2.2-S01 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining automation strategies to ensure infrastructure integrity |
| SAA-2.2-S02 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the AWS services required to provide a highly available and/or fault-tolerant architecture across AWS Regions or Availability Zones |
| SAA-2.2-S03 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Identifying metrics based on business requirements to deliver a highly available solution |
| SAA-2.2-S04 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing designs to mitigate single points of failure |
| SAA-2.2-S05 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing strategies to ensure the durability and availability of data (for example, backups) |
| SAA-2.2-S06 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting an appropriate DR strategy to meet business requirements |
| SAA-2.2-S07 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Using AWS services that improve the reliability of legacy applications and applications not built for the cloud (for example, when application changes are not possible) |
| SAA-2.2-S08 | 2 | 2.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Using purpose-built AWS services for workloads |
| SAA-3.1-K01 | 3 | 3.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Hybrid storage solutions to meet business requirements |
| SAA-3.1-K02 | 3 | 3.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage services with appropriate use cases (for example, Amazon S3, Amazon EFS, Amazon EBS) |
| SAA-3.1-K03 | 3 | 3.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage types with associated characteristics (for example, object, file, block) |
| SAA-3.1-S01 | 3 | 3.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining storage services and configurations that meet performance demands |
| SAA-3.1-S02 | 3 | 3.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining storage services that can scale to accommodate future needs |
| SAA-3.2-K01 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS compute services with appropriate use cases (for example, AWS Batch, Amazon EMR, AWS Fargate) |
| SAA-3.2-K02 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Distributed computing concepts supported by AWS global infrastructure and edge services |
| SAA-3.2-K03 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Queuing and messaging concepts (for example, publish/subscribe) |
| SAA-3.2-K04 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Scalability capabilities with appropriate use cases (for example, Amazon EC2 Auto Scaling, AWS Auto Scaling) |
| SAA-3.2-K05 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Serverless technologies and patterns (for example, AWS Lambda, Fargate) |
| SAA-3.2-K06 | 3 | 3.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | The orchestration of containers (for example, Amazon ECS, Amazon EKS) |
| SAA-3.2-S01 | 3 | 3.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Decoupling workloads so that components can scale independently |
| SAA-3.2-S02 | 3 | 3.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Identifying metrics and conditions to perform scaling actions |
| SAA-3.2-S03 | 3 | 3.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate compute options and features (for example, EC2 instance types) to meet business requirements |
| SAA-3.2-S04 | 3 | 3.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate resource type and size (for example, the amount of Lambda memory) to meet business requirements |
| SAA-3.3-K01 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS global infrastructure (for example, Availability Zones, AWS Regions) |
| SAA-3.3-K02 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Caching strategies and services (for example, Amazon ElastiCache) |
| SAA-3.3-K03 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data access patterns (for example, read-intensive compared with write-intensive) |
| SAA-3.3-K04 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database capacity planning (for example, capacity units, instance types, Provisioned IOPS) |
| SAA-3.3-K05 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database connections and proxies |
| SAA-3.3-K06 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database engines with appropriate use cases (for example, heterogeneous migrations, homogeneous migrations) |
| SAA-3.3-K07 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database replication (for example, read replicas) |
| SAA-3.3-K08 | 3 | 3.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database types and services (for example, serverless, relational compared with non-relational, in-memory) |
| SAA-3.3-S01 | 3 | 3.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Configuring read replicas to meet business requirements |
| SAA-3.3-S02 | 3 | 3.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing database architectures |
| SAA-3.3-S03 | 3 | 3.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining an appropriate database engine (for example, MySQL compared with PostgreSQL) |
| SAA-3.3-S04 | 3 | 3.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining an appropriate database type (for example, Amazon Aurora, Amazon DynamoDB) |
| SAA-3.3-S05 | 3 | 3.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Integrating caching to meet business requirements |
| SAA-3.4-K01 | 3 | 3.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Edge networking services with appropriate use cases (for example, Amazon CloudFront, AWS Global Accelerator) |
| SAA-3.4-K02 | 3 | 3.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | How to design network architecture (for example, subnet tiers, routing, IP addressing) |
| SAA-3.4-K03 | 3 | 3.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Load balancing concepts (for example, Application Load Balancer [ALB]) |
| SAA-3.4-K04 | 3 | 3.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Network connection options (for example, AWS VPN, AWS Direct Connect, AWS PrivateLink) |
| SAA-3.4-S01 | 3 | 3.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Creating a network topology for various architectures (for example, global, hybrid, multi-tier) |
| SAA-3.4-S02 | 3 | 3.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining network configurations that can scale to accommodate future needs |
| SAA-3.4-S03 | 3 | 3.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the appropriate placement of resources to meet business requirements |
| SAA-3.4-S04 | 3 | 3.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate load balancing strategy |
| SAA-3.5-K01 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data analytics and visualization services with appropriate use cases (for example, Amazon Athena, AWS Lake Formation, Amazon Quick) |
| SAA-3.5-K02 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data ingestion patterns (for example, frequency) |
| SAA-3.5-K03 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data transfer services with appropriate use cases (for example, AWS DataSync, AWS Storage Gateway) |
| SAA-3.5-K04 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data transformation services with appropriate use cases (for example, AWS Glue) |
| SAA-3.5-K05 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Secure access to ingestion access points |
| SAA-3.5-K06 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Sizes and speeds needed to meet business requirements |
| SAA-3.5-K07 | 3 | 3.5 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Streaming data services with appropriate use cases (for example, Amazon Kinesis) |
| SAA-3.5-S01 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Building and securing data lakes |
| SAA-3.5-S02 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing data streaming architectures |
| SAA-3.5-S03 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing data transfer solutions |
| SAA-3.5-S04 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Implementing visualization strategies |
| SAA-3.5-S05 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting appropriate compute options for data processing (for example, Amazon EMR) |
| SAA-3.5-S06 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting appropriate configurations for ingestion |
| SAA-3.5-S07 | 3 | 3.5 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Transforming data between formats (for example, .csv to .parquet) |
| SAA-4.1-K01 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Access options (for example, an S3 bucket with Requester Pays object storage) |
| SAA-4.1-K02 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management service features (for example, cost allocation tags, multi-account billing) |
| SAA-4.1-K03 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management tools with appropriate use cases (for example, AWS Cost Explorer, AWS Budgets, AWS Cost and Usage Report) |
| SAA-4.1-K04 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS storage services with appropriate use cases (for example, Amazon FSx, Amazon EFS, Amazon S3, Amazon EBS) |
| SAA-4.1-K05 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Backup strategies |
| SAA-4.1-K06 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Block storage options (for example, hard disk drive [HDD] volume types, solid state drive [SSD] volume types) |
| SAA-4.1-K07 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data lifecycles |
| SAA-4.1-K08 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Hybrid storage options (for example, AWS DataSync, AWS Transfer Family, AWS Storage Gateway) |
| SAA-4.1-K09 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage access patterns |
| SAA-4.1-K10 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage tiering (for example, cold tiering for object storage) |
| SAA-4.1-K11 | 4 | 4.1 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Storage types with associated characteristics (for example, object, file, block) |
| SAA-4.1-S01 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing appropriate storage strategies (for example, batch uploads to Amazon S3 compared with individual uploads) |
| SAA-4.1-S02 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the correct storage size for a workload |
| SAA-4.1-S03 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the lowest cost method of transferring data for a workload to AWS storage |
| SAA-4.1-S04 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining when storage auto scaling is required |
| SAA-4.1-S05 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Managing S3 object lifecycles |
| SAA-4.1-S06 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate backup and/or archival solution |
| SAA-4.1-S07 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate service for data migration to storage services |
| SAA-4.1-S08 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate storage tier |
| SAA-4.1-S09 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the correct data lifecycle for storage |
| SAA-4.1-S10 | 4 | 4.1 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the most cost-effective storage service for a workload |
| SAA-4.2-K01 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management service features (for example, cost allocation tags, multi-account billing) |
| SAA-4.2-K02 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management tools with appropriate use cases (for example, AWS Cost Explorer, AWS Budgets, AWS Cost and Usage Report) |
| SAA-4.2-K03 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS global infrastructure (for example, Availability Zones, AWS Regions) |
| SAA-4.2-K04 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS purchasing options (for example, Spot Instances, Reserved Instances, Savings Plans) |
| SAA-4.2-K05 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Distributed compute strategies (for example, edge processing) |
| SAA-4.2-K06 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Hybrid compute options (for example, AWS Outposts) |
| SAA-4.2-K07 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Instance types, families, and sizes (for example, memory optimized, compute optimized, virtualization) |
| SAA-4.2-K08 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Optimization of compute utilization (for example, containers, serverless computing, microservices) |
| SAA-4.2-K09 | 4 | 4.2 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Scaling strategies (for example, auto scaling, hibernation) |
| SAA-4.2-S01 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining an appropriate load balancing strategy (for example, Application Load Balancer [Layer 7] compared with Network Load Balancer [Layer 4] compared with Gateway Load Balancer) |
| SAA-4.2-S02 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining appropriate scaling methods and strategies for elastic workloads (for example, horizontal compared with vertical, EC2 hibernation) |
| SAA-4.2-S03 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining cost-effective AWS compute services with appropriate use cases (for example, AWS Lambda, Amazon EC2, AWS Fargate) |
| SAA-4.2-S04 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining the required availability for different classes of workloads (for example, production workloads, non-production workloads) |
| SAA-4.2-S05 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate instance family for a workload |
| SAA-4.2-S06 | 4 | 4.2 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate instance size for a workload |
| SAA-4.3-K01 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management service features (for example, cost allocation tags, multi-account billing) |
| SAA-4.3-K02 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management tools with appropriate use cases (for example, AWS Cost Explorer, AWS Budgets, AWS Cost and Usage Report) |
| SAA-4.3-K03 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Caching strategies |
| SAA-4.3-K04 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Data retention policies |
| SAA-4.3-K05 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database capacity planning (for example, capacity units) |
| SAA-4.3-K06 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database connections and proxies |
| SAA-4.3-K07 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database engines with appropriate use cases (for example, heterogeneous migrations, homogeneous migrations) |
| SAA-4.3-K08 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database replication (for example, read replicas) |
| SAA-4.3-K09 | 4 | 4.3 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Database types and services (for example, relational compared with non-relational, Amazon Aurora, Amazon DynamoDB) |
| SAA-4.3-S01 | 4 | 4.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Designing appropriate backup and retention policies (for example, snapshot frequency) |
| SAA-4.3-S02 | 4 | 4.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining an appropriate database engine (for example, MySQL compared with PostgreSQL) |
| SAA-4.3-S03 | 4 | 4.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining cost-effective AWS database services with appropriate use cases (for example, DynamoDB compared with Amazon RDS, serverless) |
| SAA-4.3-S04 | 4 | 4.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining cost-effective AWS database types (for example, time series format, columnar format) |
| SAA-4.3-S05 | 4 | 4.3 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Migrating database schemas and data to different locations and/or different database engines |
| SAA-4.4-K01 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management service features (for example, cost allocation tags, multi-account billing) |
| SAA-4.4-K02 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | AWS cost management tools with appropriate use cases (for example, AWS Cost Explorer, AWS Budgets, AWS Cost and Usage Report) |
| SAA-4.4-K03 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Load balancing concepts (for example, Application Load Balancer [ALB]) |
| SAA-4.4-K04 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | NAT gateways (for example, NAT instance costs compared with NAT gateway costs) |
| SAA-4.4-K05 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Network connectivity (for example, private lines, dedicated lines, VPNs) |
| SAA-4.4-K06 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Network routing, topology, and peering (for example, AWS Transit Gateway, VPC peering) |
| SAA-4.4-K07 | 4 | 4.4 | K | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Network services with appropriate use cases (for example, DNS) |
| SAA-4.4-S01 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Configuring appropriate NAT gateway types for a network (for example, a single shared NAT gateway compared with NAT gateways for each Availability Zone) |
| SAA-4.4-S02 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Configuring appropriate network connections (for example, AWS Direct Connect compared with VPN compared with internet) |
| SAA-4.4-S03 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Configuring appropriate network routes to minimize network transfer costs (for example, Region to Region, Availability Zone to Availability Zone, private to public, AWS Global Accelerator, VPC endpoints) |
| SAA-4.4-S04 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Determining strategic needs for content delivery networks (CDNs) and edge caching |
| SAA-4.4-S05 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Reviewing existing workloads for network optimizations |
| SAA-4.4-S06 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting an appropriate throttling strategy |
| SAA-4.4-S07 | 4 | 4.4 | S | missing |  |  |  |  |  |  |  |  | no content yet | phase-3+ | author lesson+assessment | Selecting the appropriate bandwidth allocation for a network device (for example, a single VPN compared with multiple VPNs, Direct Connect speed) |

