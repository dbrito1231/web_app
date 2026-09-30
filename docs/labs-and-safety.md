# Labs and safety

Lab catalog, teardown, budget, and credential rules. Spec version 1. Implements REQ-P20–P27, REQ-P04, REQ-P99. Access date for example rates: 2026-09-29.

## Company sandbox (if you run labs at work)

Use a sandbox account or OU, not a production account. Budget alerts warn only; they do not stop spend. Tear down the same day. Do not treat this workbook's progress file as an audit record of who completed training.

## Hard rules

REQ-L01. Agents never touch AWS. The learner is the only actor who may create, change, or delete AWS resources. Lab commands in content are labeled **unexecuted** until the learner reports they ran them.

REQ-L02. Agents may write lab files and fixtures; run `terraform fmt` and `terraform validate` without credentials; use AWS Knowledge MCP (docs) and Terraform MCP registry/docs only. No AWS API MCP. No credentialed `terraform plan` / `apply` / `destroy`. No HCP workspace ops by agents.

REQ-L03. $10 is a warning, not a stop or a promised total. Forgotten hourly resources overnight can exceed $10.

REQ-L04. Every guided and unguided lab includes teardown: ordered PowerShell deletes (dependents first); delete not stop; KMS scheduled deletion not canceled; verification expecting empty/`ResourceNotFound`; still-billing note; recovery pointing to the tagged kill switch for that lab id.

REQ-L05. Guided labs ≥15 execution steps. Unguided labs ≥15 acceptance criteria. Unguided pairs change requirements; they do not repeat guided steps. Reference solution is gated; Stop charges and teardown remain available without opening the gate.

REQ-L06. Cost-risk confirmation: type `I ACCEPT THE COST RISK` before create/apply on GL-06, GL-07, GL-08, GL-09, GL-14, GL-18, GL-19, GL-21.

REQ-L07. Preflight: `aws sts get-caller-identity`, region, CLI v2, Terraform version, same-hour and 24-hour estimates. Default region `us-east-1`. Profile via `$env:AWS_PROFILE`, `$env:AWS_REGION`.

REQ-L08. Tags on creatable resources: `Workbook=aws-tf-lab`, `LabId`, `CreatedAt`, `ExpiresAt` (same calendar day).

REQ-L09. One alert-only budget (actual $2/$5/$8, forecast $5/$8). No budget actions. Alerts lag ~8–12 hours and do not stop spend.

REQ-L10. Kill switch: GL-01 PowerShell snippet the **learner** runs. Lists tagged resources in `$env:AWS_REGION`, deletes only those ids after typing the STS account id, refuses root profile / empty region / zero or unexpectedly large matches. Does not delete untagged resources. Not a product button.

REQ-L11. Do not create live: Direct Connect, Outposts, Snow Family, Wavelength, VMware Cloud on AWS, Shield Advanced, CloudHSM, or an AWS Organization. SCPs taught via GL-01 permission boundary (denies CloudHSM, Shield Advanced, Direct Connect, Outposts only).

REQ-L12. Free Tier never assumed. No root access keys. No secrets in git. Terraform state gitignored.

## Example rates (illustration only)

Re-read official pricing for the learner’s region before a lab is marked verified. Same-hour `us-east-1` examples read 2026-09-29 from the public AWS pricing pages (claim table with verbatim quotes and the method used per row: `reports/fix-loop-r2/d6/pricing-claims.md`). Instance-type tables (EC2, RDS, ElastiCache) were read in the pages' rendered rate widgets with the region set to US East (N. Virginia). The other pages' region tables did not render, so those rows come from static page text; a row marked "not verified for us-east-1" must be re-checked on the page before a lab run.

| Resource | Example | Status |
| --- | --- | --- |
| NAT Gateway | $0.045/hour + $0.045/GB; partial hour bills as full hour | Page example is US East (Ohio); not verified for us-east-1 |
| Public IPv4 | $0.005/hour in use or idle | Static page text, not region-specific; per-second billing, 60-second minimum |
| Gateway VPC endpoints | no hourly/data charge in that example | Static page text |
| Customer-managed KMS | $1/month prorated; scheduled-for-deletion not charged | Read 2026-09-23, not re-read |
| ALB | $0.0225/hour plus LCU; partial hour bills as full hour | Worked-example rate, region not named; not verified for us-east-1 |
| t3.micro Linux | $0.0104/hour | Verified us-east-1 (EC2 on-demand widget) |
| t3.medium Linux | $0.0416/hour | Verified us-east-1 (EC2 on-demand widget) |
| RDS PostgreSQL db.t3.micro Single-AZ | $0.018/hour | Verified us-east-1 (RDS PostgreSQL rate widget); partial hours bill as full hours |
| RDS storage | gp2/gp3 not read; io1 $0.125/GB-month used only as an upper bound | gp2/gp3 not verified; io1 from a US East (N. Virginia) page example |
| ElastiCache cache.t3.micro | Redis $0.017/hour (Valkey $0.0136/hour); partial hour bills as full hour | Verified us-east-1 (ElastiCache rate widget) |
| EBS gp3 | $0.08/GB-month | Worked-example rate, region not named; not verified for us-east-1 |
| EBS snapshot (standard) | $0.05/GB-month | Worked-example rate, region not named; not verified for us-east-1 |
| Fargate Linux/x86 | $0.000011244/vCPU-second ($0.0405/h), $0.000001235/GB-second ($0.00445/h); 1-minute minimum | Verified: page example names US East (N. Virginia) |
| EKS standard support | $0.10/cluster-hour (extended $0.60 out of lab) | Static page text, flat per-cluster rate |
| WAF | $5.00/web ACL/month, $1.00/rule or managed rule group/month, $0.60 per million requests | Worked-example rates, region not named; not verified for us-east-1 |
| CloudWatch standard alarm | $0.10 per alarm metric per month | Worked example ("US East"); not verified for us-east-1 |
| Alert-only Budgets | no charge | Read 2026-09-23, not re-read |

Still to fill from official pages: EFS Standard storage and RDS gp2/gp3 storage (page price tables did not render), plus Step Functions, Athena, Route 53 private zone, Secrets Manager, GuardDuty, Macie (the last six are not used by the 16 hourly labs). GL/UL-07's EFS part keeps its earlier conservative 24 h figure until EFS is read.

## Lab catalog (21 + 21)

| Pair | Title | ~Time | Notes |
| --- | ---: | ---: | --- |
| GL-01 / UL-01 | Identity, budget, and preflight | 90 | IAM lab user + MFA, alert-only budget, tags, permission boundary, kill-switch snippet. UL: daily role vs break-glass. Same-hour ~$0 for alert-only budget. |
| GL-02 / UL-02 | Private S3 data controls | 90 | BPA, versioning, lifecycle, tiny object, bucket policy. UL: second prefix + Macie after price, then disable. |
| GL-03 / UL-03 | IAM role, resource policy, and STS | 75 | Role reads only lab bucket; assume with STS. UL: scoped policy; GuardDuty on/off after price. |
| GL-04 / UL-04 | Customer-managed KMS key | 75 | Symmetric key, encrypt one object, schedule deletion, do not cancel. UL: key policy; Secrets Manager + SSM standard param after price, then delete. |
| GL-05 / UL-05 | VPC segmentation | 90 | VPC, two subnets, routes, SG, NACL, S3 gateway endpoint. No NAT. UL: second AZ + tighter NACL. |
| GL-06 / UL-06 | NAT gateway, then delete it | 75 | One NAT, private route, check, delete NAT, release EIP. Cost-risk gate. |
| GL-07 / UL-07 | EC2, EBS, and EFS | 120 | t3.micro, gp3, snapshot, terminate and delete. UL: small EFS mount/unmount/delete. Cost-risk gate. Stopped ≠ teardown. |
| GL-08 / UL-08 | Application Load Balancer | 90 | Internet-facing ALB, one healthy t3.micro, HTTP check, delete. UL: WAF web ACL after price. Cost-risk gate. |
| GL-09 / UL-09 | Auto Scaling | 75 | Launch template, ASG desired 1 then 0, delete. UL: target tracking to 2 then 0. Cost-risk gate. |
| GL-10 / UL-10 | Queue and event path | 90 | SQS, SNS, Lambda no VPC. Delete function and log group. UL: DLQ + idempotency. |
| GL-11 / UL-11 | API Gateway and Lambda | 75 | One HTTP API route, one Lambda, one test call, delete. UL: authorized second route + 403. |
| GL-12 / UL-12 | Step Functions | 75 | Small standard state machine, one success, delete. UL: failure branch + retry. Transition price before publish. |
| GL-13 / UL-13 | DynamoDB | 75 | On-demand table, handful of items. UL: one GSI, query, remove. No reserved/provisioned. |
| GL-14 / UL-14 | RDS, single AZ | 120 | Smallest single-AZ PostgreSQL, short backup, delete with no final snapshot. UL: restore copy then delete. Main forgotten-resource risk. Cost-risk gate. |
| GL-15 / UL-15 | CloudWatch and CloudTrail | 75 | Alarm on existing metric, trail to lab bucket, delete. UL: one-day retention on GL-10 log group. No paid custom metrics. |
| GL-16 / UL-16 | Private DNS | 60 | One Route 53 private hosted zone, one private record, delete. No public zone / domain purchase. |
| GL-17 / UL-17 | Athena on a tiny file | 60 | Small CSV, one table, one query, drop. No leftover crawler. UL: convert result, delete outputs. |
| GL-18 / UL-18 | ECS on Fargate | 90 | Cluster, task definition, short task, desired 0, delete. UL: change priced CPU/memory once. Cost-risk gate. |
| GL-19 / UL-19 | EKS control plane, then delete | 120 | Cluster on standard support, no node group, then delete leftovers. UL: Fargate profile or one managed node, remove before cluster delete. Cost-risk gate. |
| GL-20 / UL-20 | Terraform workflow | 150 | Local backend: init, fmt, validate, plan, apply, state list, out-of-band change, refresh, destroy. State gitignored. **Learner** runs apply/destroy. UL: local module, import, saved plan not applied. |
| GL-21 / UL-21 | ElastiCache, then HCP as allowed | 120 | Guided: smallest ElastiCache, describe, delete. UL: Terraform 8a–8d; no-charge HCP only, stop before AWS credentials. If paid path required, docs + drills + design_exercise. Cost-risk gate. |

## Lab file schema (content phase)

Each lab spec includes: id, time, difficulty, same-hour and 24-hour estimates, objectives, services, prerequisites, diagram, least-privilege actions, region, preflight, ≥15 steps or criteria, checks, troubleshooting, security and cost questions, teardown block (REQ-L04).

Lint rejects: guided lab under 15 steps; unguided under 15 criteria; missing teardown deletes/verification/still-billing note; `delete-bucket` without named bucket variable; account-id or `AKIA` patterns in source.

## Design exercises (skill bullets without live lab)

REQ-L20. All 82 skill bullets need an applied exercise with observable criteria. Labs cover disposable services. Remaining skill coverage uses `DE-*` design exercises: scenario, constraints, decision/diagram/policy/sizing/cost/troubleshooting, rubric. Never labeled as AWS experience.

Required at least for: Direct Connect vs VPN vs internet; Outposts/hybrid; Snow Family; multi-account Control Tower/SCPs; directory federation; multi-Region DR vs RPO/RTO; CloudHSM vs KMS; Kinesis/MSK; EMR/Glue; data lake/Lake Formation; visualization; Spot/RI/Savings Plans comparisons; Transit Gateway/peering; Global Accelerator/CDN; throttling; storage migration; cross-engine database migration.

## Phase packets

- **5-AWS:** GL/UL-01 through GL/UL-19 and ElastiCache guided half of GL-21.
- **5-TF:** GL/UL-20 and HCP half of UL-21 under no-charge-only rule. `terraform fmt -check` and `terraform validate` without credentials.

Live apply remains unexecuted in agent workflows.
