# AWS Solutions Architect — evidence log (run-2, strict Phase 3)

**Role:** Senior AWS Solutions Architect (Agent 3)  
**Date:** 2026-09-25  
**Mode:** Paper-feedback per `reports/evidence/gate0-save-failure.md` (Result A — CSRF origin; no live AWS CLI).  
**No AWS credentials used.**

## Volume summary

| Metric | Count | Source |
|---|---:|---|
| Lab command review rows | **42** | Table below (gl-01 … ul-21) |
| AWS doc lookups (EV-AWS-2xx) | **52** | MCP + WebFetch table below |
| SAA-path lessons spot-checked | **15** | `content/lessons/` excluding `lesson-tf-*` |
| Sampled SAA+A0 question keys read | **310** | `reports/evidence/sample.md` + `content/questions/*.json` |
| Guided lab CLI rows in extract | **316** | `reports/evidence/lab-commands.md` (gl-01–gl-21 only) |

---

## Re-verification: findings AWS-201 … AWS-205 (fresh content read)

| EV-ID | Finding | Locator | Excerpt (≤30 words) | Tool run |
|---|---|---|---|---|
| EV-AWS-REF201 | AWS-201 GL-08 user data | `content/labs/gl-08.json` s08 L98 | AL2023 AMI via SSM; `--user-data "<powershell>python -m http.server 80</powershell>"` | Read JSON + MCP EV-AWS-200 + WebFetch EV-AWS-235 |
| EV-AWS-REF202 | AWS-202 GL-05 NACL | `content/labs/gl-05.json` s10 L115 | `--protocol -1 --rule-action deny --cidr-block 0.0.0.0/0 --port-range From=22,To=22` | Read JSON + MCP EV-AWS-201 + WebFetch EV-AWS-232 |
| EV-AWS-REF203 | AWS-203 GL-17 Athena | `content/labs/gl-17.json` s07–s08 | s07: "Run DDL for external table"; s08: `SELECT * FROM gl17.sample` | Read JSON + MCP EV-AWS-206 + WebFetch EV-AWS-233 |
| EV-AWS-REF204 | AWS-204 GL-07 EFS gap | `content/labs/gl-07.json` L3, L49; `ul-07.json` criteria | Title "EC2, EBS, and EFS"; steps have no `efs` CLI | Read JSON + MCP EV-AWS-207 |
| EV-AWS-REF205 | AWS-205 teardown scan | `scripts/scan_lab_placeholders.py`; var scan | Output `PASS 41 labs`; L66 `pass`; 4 guided + 12 unguided teardown var gaps | `python scripts\scan_lab_placeholders.py` + scratchpad var scan |

---

## Per-lab command review (42 rows)

Commands for guided labs cross-checked against `reports/evidence/lab-commands.md` (316 rows). Unguided labs (ul-*) reviewed via JSON steps, acceptance criteria, and `teardown.orderedDeletesPowerShell`.

| # | Lab | Command source | Cleanup / teardown | Verdict |
|---:|---|---|---|---|
| 1 | gl-01 | lab-commands + JSON | IAM/MFA/budget deletes in steps; `$Serial` re-derived in teardown | OK with unguided var note |
| 2 | gl-02 | lab-commands + JSON | S3 lifecycle delete in teardown; spurious `$m`/`$v`/`$versions` in teardown text | OK commands; teardown var noise |
| 3 | gl-03 | lab-commands + JSON | Role/policy/bucket cleanup in steps | OK |
| 4 | gl-04 | lab-commands + JSON | KMS deletion window + bucket empty | OK |
| 5 | gl-05 | lab-commands + JSON | VPC endpoint + NACL; **NACL rule defect** (AWS-202) | Blocking semantics error |
| 6 | gl-06 | lab-commands + JSON | NAT route; meg-teardown refs `$AlbArn`, `$EndpointId` not created | Teardown hygiene (AWS-205) |
| 7 | gl-07 | lab-commands + JSON | EC2/EBS only; **no EFS** (AWS-204) | Content gap |
| 8 | gl-08 | lab-commands + JSON | ALB hourly; **PowerShell user data on AL2023** (AWS-201) | Blocking |
| 9 | gl-09 | lab-commands + JSON | ASG scale-to-zero before delete | OK |
| 10 | gl-10 | lab-commands + JSON | Lambda/SNS/SQS ordered deletes | OK |
| 11 | gl-11 | lab-commands + JSON | HTTP API + Lambda permission | OK |
| 12 | gl-12 | lab-commands + JSON | SFN + IAM role delete order | OK |
| 13 | gl-13 | lab-commands + JSON | DynamoDB on-demand create/delete | OK |
| 14 | gl-14 | lab-commands + JSON | RDS micro + skip-final-snapshot path | OK |
| 15 | gl-15 | lab-commands + JSON | CloudWatch alarm on placeholder instance | OK (syntax drill) |
| 16 | gl-16 | lab-commands + JSON | Route53 private zone + VPC association | OK |
| 17 | gl-17 | lab-commands + JSON | **Missing Athena DDL** before SELECT (AWS-203) | Blocking sequence |
| 18 | gl-18 | lab-commands + JSON | ECS Fargate `run-task` shorthand | Likely PS quoting (AWS-207) |
| 19 | gl-19 | lab-commands + JSON | EKS `subnetIds=$Subnets` space-separated | Likely (AWS-206) |
| 20 | gl-20 | lab-commands + JSON | Terraform apply/destroy; tag drill | OK (TF execution) |
| 21 | gl-21 | lab-commands + JSON | ElastiCache hourly delete order | OK |
| 22 | ul-01 | JSON criteria + teardown | EventBridge/IAM teardown list | OK unguided pattern |
| 23 | ul-02 | JSON teardown L66 | `macie2 update-macie-session --status PAUSED` | CR-0005 fix verified |
| 24 | ul-03 | JSON teardown | Paired gl-03 naming | OK |
| 25 | ul-04 | JSON teardown | KMS + bucket mirror gl-04 | OK |
| 26 | ul-05 | JSON teardown | `$VpcId`/`$EndpointId` not in JSON steps | Teardown var gap (AWS-205) |
| 27 | ul-06 | JSON teardown | NAT/VPC meg-script | Teardown var gap |
| 28 | ul-07 | JSON criteria + teardown | Criteria require EFS; gl-07 gap | AWS-204 |
| 29 | ul-08 | JSON teardown | ALB/VPC template teardown | Var-dependent |
| 30 | ul-09 | JSON teardown | ASG/LT vars learner-tracked | Expected unguided |
| 31 | ul-10 | JSON teardown | Reuses gl-10 names | OK paired |
| 32 | ul-11 | JSON teardown | `$ApiId` learner-tracked | OK unguided |
| 33 | ul-12 | JSON teardown | SFN + role | OK |
| 34 | ul-13 | JSON teardown | DynamoDB delete-table | OK |
| 35 | ul-14 | JSON teardown | RDS vars not declared | Var gap |
| 36 | ul-15 | JSON teardown | CloudTrail delete | OK |
| 37 | ul-16 | JSON teardown | Route53 + VPC vars | Learner-tracked |
| 38 | ul-17 | JSON teardown | Reconstructs `$ResultsBucket` from account | Good pattern |
| 39 | ul-18 | JSON teardown | ECS cluster cleanup | OK |
| 40 | ul-19 | JSON teardown | EKS delete wait | Same subnetIds concern |
| 41 | ul-20 | JSON teardown | `terraform destroy -auto-approve` | Facilitator note vs gl-20 |
| 42 | ul-21 | JSON teardown | ElastiCache subnet group order | OK |

---

## AWS documentation lookups (EV-AWS-2xx) — 52 entries

| EV-ID | Tool | Topic / URL | Excerpt (≤30 words) |
|---|---|---|---|
| EV-AWS-200 | MCP | AL2023 cloud-init user data | User-data fields pass actions to cloud-init; runs user scripts in user-data |
| EV-AWS-201 | MCP | CreateNetworkAclEntry API | Protocol "-1" means all protocols; all ports allowed regardless of port-range |
| EV-AWS-202 | MCP | S3 CreateBucketConfiguration | us-east-1 bucket creation does not need LocationConstraint |
| EV-AWS-203 | MCP | macie2 update_macie_session | status PAUSED suspends all Macie activities for the account |
| EV-AWS-204 | MCP | EKS create-cluster CLI example | `subnetIds=subnet-a,subnet-b` comma-separated in resources-vpc-config |
| EV-AWS-205 | MCP | AWS Budgets alerts | Budget alerts notify; sending alerts does not stop resource charges by itself |
| EV-AWS-206 | MCP | Athena CREATE EXTERNAL TABLE | CREATE EXTERNAL TABLE requires LOCATION and schema before querying |
| EV-AWS-207 | MCP | EFS create-file-system CLI | `aws efs create-file-system` documented create/mount workflow |
| EV-AWS-208 | MCP | IAM put-user-permissions-boundary | Sets permissions boundary ARN on IAM user |
| EV-AWS-209 | MCP | S3 Block Public Access | Block public access overrides public ACLs/policies |
| EV-AWS-210 | MCP | KMS schedule-key-deletion | pending-window-in-days between 7 and 30 for customer keys |
| EV-AWS-211 | MCP | EC2 create-vpc-endpoint S3 gateway | `com.amazonaws.us-east-1.s3` gateway endpoint example |
| EV-AWS-212 | MCP | NAT Gateway pricing | Charged per NAT Gateway-hour plus data processing per GB |
| EV-AWS-213 | MCP | ALB target health checks | Targets must pass health checks before healthy state |
| EV-AWS-214 | MCP | ECS Fargate networkConfiguration | awsvpcConfiguration required for Fargate launch type |
| EV-AWS-215 | MCP | RDS delete-db-instance | `--skip-final-snapshot` skips final DB snapshot on delete |
| EV-AWS-216 | MCP | DynamoDB PAY_PER_REQUEST | On-demand billing mode valid for create-table |
| EV-AWS-217 | MCP | Auto Scaling create-auto-scaling-group | Launch template recommended; group name required |
| EV-AWS-218 | MCP | ELBv2 create-load-balancer | Application load balancer requires subnets in VPC |
| EV-AWS-219 | MCP | SNS subscribe SQS | SNS can deliver to SQS queue subscriptions |
| EV-AWS-220 | MCP | Step Functions create-state-machine | Requires definition JSON and roleArn |
| EV-AWS-221 | MCP | Route53 create-hosted-zone | Private zones associate with VPC |
| EV-AWS-222 | MCP | CloudTrail create-trail | Requires Name and S3BucketName |
| EV-AWS-223 | MCP | ElastiCache create-cache-cluster | CLI example for Redis cache cluster create |
| EV-AWS-224 | MCP | STS get-caller-identity | CLI reference for identity preflight |
| EV-AWS-225 | MCP | resourcegroupstaggingapi get-resources | TagFilters Key/Values query supported |
| EV-AWS-226 | MCP | Shared responsibility model | Customer responsible for security *in* the cloud |
| EV-AWS-227 | MCP | Root user MFA guidance | Do not use root for everyday tasks; use MFA |
| EV-AWS-228 | MCP | EBS same-AZ attach | Volume must be in same Availability Zone as instance |
| EV-AWS-229 | MCP | API Gateway v2 AWS_PROXY | IntegrationType AWS_PROXY for Lambda proxy |
| EV-AWS-230 | MCP | SAA-C03 domain 1 content | Secure architectures domain tasks 1.1–1.3 |
| EV-AWS-231 | MCP | Lambda execution role | create-function requires IAM role for Lambda service |
| EV-AWS-232 | WebFetch | ec2 create-network-acl-entry CLI | Protocol -1 allows all ports regardless of port-range |
| EV-AWS-233 | WebFetch | athena start-query-execution CLI | Query-string required; database in query-execution-context |
| EV-AWS-234 | WebFetch | s3api create-bucket CLI | us-east-1 create-bucket region handling |
| EV-AWS-235 | WebFetch | ec2 run-instances CLI | user-data parameter documented for instance launch |
| EV-AWS-236 | WebFetch | cloudwatch put-metric-alarm CLI | Alarm creation parameters reference |
| EV-AWS-237 | WebFetch | logs create-log-group CLI | log-group-name required |
| EV-AWS-238 | WebFetch | ssm get-parameters CLI | Names parameter for AMI path lookup (gl-08) |
| EV-AWS-239 | WebFetch | sqs create-queue CLI | QueueName required; attributes map |
| EV-AWS-240 | MCP | iam enable-mfa-device | MFA device enable requires serial-number and TOTP codes |
| EV-AWS-241 | MCP | ec2 create-nat-gateway | NAT gateway in public subnet with allocation-id |
| EV-AWS-242 | MCP | elbv2 delete-load-balancer | Delete ALB before dependencies removed |
| EV-AWS-243 | MCP | ec2 delete-nat-gateway | NAT delete waits before EIP release |
| EV-AWS-244 | MCP | s3 delete-bucket | Bucket must be empty before delete-bucket |
| EV-AWS-245 | MCP | iam delete-user | User must have keys/MFA removed before delete |
| EV-AWS-246 | MCP | budgets create-budget | Budget creation requires account-id and budget JSON |
| EV-AWS-247 | MCP | ec2 create-volume | create-volume requires availability-zone parameter |
| EV-AWS-248 | MCP | ecs create-cluster | ECS cluster create for Fargate labs |
| EV-AWS-249 | MCP | eks delete-cluster | Cluster delete waits for ACTIVE/DELETING states |
| EV-AWS-250 | MCP | glue create-database | Glue database for Athena catalog context |
| EV-AWS-251 | MCP | SAA exam domains overview | Four content domains map to secure/resilient/performant/cost |

---

## Supplemental (non-doc) evidence

| ID | Locator | Excerpt |
|---|---|---|
| EV-SUP-001 | `python scripts\scan_lab_placeholders.py` | `PASS 41 labs scanned` |
| EV-SUP-002 | `scripts/scan_lab_placeholders.py` L66 | Teardown var check is `pass` |
| EV-SUP-003 | `content/coverage/mock-saa-50.json` | A1:15 A2:13 A3:12 A4:10 |
| EV-SUP-004 | `content/coverage/saa_registry.json` | d1:30 d2:26 d3:24 d4:20 |
| EV-SUP-005 | Sampled keys script | 310/310 `correctAnswerIds`; 189 template stems |
| EV-SUP-006 | `reports/evidence/gate0-save-failure.md` | Paper-feedback: 403 Forbidden on POST attempts |
| EV-SUP-007 | All 15 SAA lessons read | Spot-check: boilerplate tradeoffs; URLs valid; budgets don't stop spend |

---

## Sampled SAA question keys (paper-feedback)

| EV-ID | Scope | Result |
|---|---|---|
| EV-SUP-005 | All 310 sampled `q-saa-*` + `q-a0-*` | Every file has `correctAnswerIds`; 0 missing keys |
| EV-SUP-005b | Template stems (189) | Key `a`; distractor D Budgets claim matches EV-AWS-205 |
| EV-SUP-005c | Non-template / MR (121) | Rationale AWS claims checked against EV-AWS-200–251 |
| EV-SUP-006 | Paper-feedback UI | Check answers shows `Forbidden`; feedback UI **Needs Verification** |

**Drill grading method:** For each sampled ID, stem and choices read in app (where applicable), answer chosen on paper, then `content/questions/<id>.json` opened for key/rationale — per plan §4 and gate0.

| EV-AWS-252 | 2026-09-25 | MCP | GL-08 user-data AL2023 | EC2 Linux user-data shell vs PowerShell wrapper | AWS docs / MCP |
| EV-AWS-253 | 2026-09-25 | MCP | EKS create-cluster CLI | subnetIds / networkConfiguration quoting | AWS CLI docs |
| EV-AWS-254 | 2026-09-25 | MCP | `ul-02.json` teardown Macie | `update-macie-session --status PAUSED` vs disable | Registry/docs lookup |
| EV-AWS-256 | 2026-09-25 | file | `ul-05.json` teardown verify | Tag filter `LabId,Values=gl-05` should be `ul-05` | Grep lab JSON |
