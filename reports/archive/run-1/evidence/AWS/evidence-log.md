# AWS Solutions Architect — evidence log

Agent role: Senior AWS Solutions Architect (Agent 3).  
Evaluation date: 2026-09-25. No AWS CLI executed; AWS Knowledge MCP used for doc validation.

## Per-lab command review (42 labs)

| EV-ID | Timestamp (UTC) | Type | Locator | Excerpt (≤30 words) | Tool run | Lab review verdict |
|---|---|---|---|---|---|---|
| EV-AWS-001 | 2026-09-25T17:30Z | file | `content/labs/gl-01.json` s05; lab-commands L7–8 | `aws iam create-user --user-name workbook-gl01` | Read + lint | Preflight/IAM/budget CLI shape OK; teardown re-derives `$Serial` (unguided gap). |
| EV-AWS-002 | 2026-09-25T17:30Z | file | `content/labs/gl-02.json` s06–75 | `create-bucket` us-east-1; bullet: do not pass LocationConstraint | Read + MCP EV-AWS-050 | **CR-0005 fix verified** — correct for us-east-1. |
| EV-AWS-003 | 2026-09-25T17:30Z | file | `content/labs/gl-03.json` s06–09 | `assume-role` + `s3 cp` read/write | Read | IAM/S3 role lab commands align with STS + inline policy pattern. |
| EV-AWS-004 | 2026-09-25T17:30Z | file | `content/labs/gl-04.json` s06–10 | `kms schedule-key-deletion --pending-window-in-days 7` | Read | KMS+SSE lab; key deletion window matches API. |
| EV-AWS-005 | 2026-09-25T17:30Z | file | `content/labs/gl-05.json` s10 L115 | NACL `--protocol -1` deny `0.0.0.0/0` | Read + MCP EV-AWS-051 | **Defect**: rule denies all ingress, not SSH-only (see AWS-005). |
| EV-AWS-006 | 2026-09-25T17:30Z | file | `content/labs/gl-06.json` s09; teardown L194–215 | `create-nat-gateway`; meg teardown with `if ($AlbArn)` | Read + var scan | NAT create/delete OK; teardown copy-paste from VPC template (see AWS-006). |
| EV-AWS-007 | 2026-09-25T17:30Z | file | `content/labs/gl-07.json` s08 L94 | `create-volume --availability-zone us-east-1a` | Read | AZ hardcode risk; **no EFS** despite title (AWS-004). |
| EV-AWS-008 | 2026-09-25T17:30Z | file | `content/labs/gl-08.json` s08 L98 | `--user-data "<powershell>python -m http.server 80</powershell>"` on AL2023 | Read + MCP EV-AWS-052 | **Defect**: PowerShell user data on Linux AMI (AWS-001). |
| EV-AWS-009 | 2026-09-25T17:30Z | file | `content/labs/gl-09.json` s08 | `autoscaling create-auto-scaling-group` | Read | ASG+LT commands valid; scale-to-zero before delete present in steps. |
| EV-AWS-010 | 2026-09-25T17:30Z | file | `content/labs/gl-10.json` s09 | `lambda create-function` with execution role | Read | Lambda+SNS+SQS wiring; roles created in steps (CR-0005 fix). |
| EV-AWS-011 | 2026-09-25T17:30Z | file | `content/labs/gl-11.json` s07–08 | `apigatewayv2 create-integration` AWS_PROXY | Read | HTTP API + Lambda permission ARN pattern OK for us-east-1. |
| EV-AWS-012 | 2026-09-25T17:30Z | file | `content/labs/gl-12.json` s07 | `stepfunctions create-state-machine` | Read | SFN role created in s06; standard CLI. |
| EV-AWS-013 | 2026-09-25T17:30Z | file | `content/labs/gl-13.json` s06 | `dynamodb create-table` PAY_PER_REQUEST | Read | On-demand table; delete in s11 before teardown panel. |
| EV-AWS-014 | 2026-09-25T17:30Z | file | `content/labs/gl-14.json` s07 | `rds create-db-instance` db.t3.micro postgres | Read | Hourly RDS; skip-final-snapshot delete in steps — cost panel accurate. |
| EV-AWS-015 | 2026-09-25T17:30Z | file | `content/labs/gl-15.json` s09 | `cloudwatch put-metric-alarm` placeholder InstanceId | Read | Demo alarm on fake instance ID — OK for syntax drill. |
| EV-AWS-016 | 2026-09-25T17:30Z | file | `content/labs/gl-16.json` s07 | `route53 create-hosted-zone` private VPC association | Read | Private zone + VPC link; delete order in steps. |
| EV-AWS-017 | 2026-09-25T17:30Z | file | `content/labs/gl-17.json` s07–08 | s07: "Run DDL for external table"; s08 SELECT gl17.sample | Read | **Defect**: incomplete DDL; query cannot succeed (AWS-007). |
| EV-AWS-018 | 2026-09-25T17:30Z | file | `content/labs/gl-18.json` s08 L94 | `ecs run-task` Fargate network-configuration shorthand | Read | Likely CLI quoting issue on PowerShell (AWS-008). |
| EV-AWS-019 | 2026-09-25T17:30Z | file | `content/labs/gl-19.json` s07 L85 | `eks create-cluster ... subnetIds=$Subnets` | Read + MCP EV-AWS-053 | **Likely defect**: subnetIds must be comma-separated IDs (AWS-009). |
| EV-AWS-020 | 2026-09-25T17:30Z | file | `content/labs/gl-20.json` s09–13 | `terraform apply`; teardown destroy | Read | Terraform workflow; OOB tag drill documented. |
| EV-AWS-021 | 2026-09-25T17:30Z | file | `content/labs/gl-21.json` s07 | `elasticache create-cache-cluster` cache.t3.micro | Read | Hourly Redis; delete cluster + subnet group in steps. |
| EV-AWS-022 | 2026-09-25T17:30Z | file | `content/labs/ul-01.json` teardown | IAM role/policy teardown for EventBridge | Read | Unguided criteria-only; teardown CLI list present. |
| EV-AWS-023 | 2026-09-25T17:30Z | file | `content/labs/ul-02.json` teardown L66 | `aws macie2 update-macie-session --status PAUSED` | Read + MCP EV-AWS-054 | **CR-0005 Macie fix verified** (replaces disable-macie). |
| EV-AWS-024 | 2026-09-25T17:30Z | file | `content/labs/ul-03.json` teardown | Reuses gl-03 bucket name pattern | Read | Teardown assumes gl-03 naming; acceptable for paired challenge. |
| EV-AWS-025 | 2026-09-25T17:30Z | file | `content/labs/ul-04.json` teardown | KMS + bucket cleanup | Read | Mirrors gl-04 resource types. |
| EV-AWS-026 | 2026-09-25T17:30Z | file | `content/labs/ul-05.json` teardown L64–81 | `$EndpointId`, `$VpcId` without learner step vars | Read + var scan | **Defect**: unguided teardown needs vars learner must capture (AWS-010). |
| EV-AWS-027 | 2026-09-25T17:30Z | file | `content/labs/ul-06.json` teardown | NAT/VPC meg-script | Read + var scan | Same template as gl-06; guarded `if()` but vars not documented. |
| EV-AWS-028 | 2026-09-25T17:30Z | file | `content/labs/ul-07.json` teardown | EC2/EBS cleanup; criteria require EFS | Read | Teardown omits EFS APIs; criteria vs gl-07 gap (AWS-004). |
| EV-AWS-029 | 2026-09-25T17:30Z | file | `content/labs/ul-08.json` teardown | ALB/VPC template | Read + var scan | Copy-paste teardown; ALB path OK if vars set. |
| EV-AWS-030 | 2026-09-25T17:30Z | file | `content/labs/ul-09.json` teardown | ASG/LT deletes | Read | `$AsgName`/`$LaunchTemplateId` not in JSON steps (unguided). |
| EV-AWS-031 | 2026-09-25T17:30Z | file | `content/labs/ul-10.json` teardown | Lambda/SNS/SQS delete sequence | Read | Uses gl-10 resource names — intentional pair reuse. |
| EV-AWS-032 | 2026-09-25T17:30Z | file | `content/labs/ul-11.json` teardown | API Gateway + Lambda delete | Read | `$ApiId` unset in file — learner must track. |
| EV-AWS-033 | 2026-09-25T17:30Z | file | `content/labs/ul-12.json` teardown | SFN + IAM role | Read | Standard serverless teardown ordering. |
| EV-AWS-034 | 2026-09-25T17:30Z | file | `content/labs/ul-13.json` teardown | DynamoDB delete-table | Read | OK. |
| EV-AWS-035 | 2026-09-25T17:30Z | file | `content/labs/ul-14.json` teardown | RDS subnet group + instance vars | Read | `$DbId`/`$SubnetGroup` not declared in JSON. |
| EV-AWS-036 | 2026-09-25T17:30Z | file | `content/labs/ul-15.json` teardown | CloudTrail delete | Read | OK. |
| EV-AWS-037 | 2026-09-25T17:30Z | file | `content/labs/ul-16.json` teardown | Route53 + VPC | Read | `$ZoneId`/`$VpcId` learner-tracked. |
| EV-AWS-038 | 2026-09-25T17:30Z | file | `content/labs/ul-17.json` teardown | Reconstructs `$ResultsBucket` from account id | Read | Teardown self-seeds bucket names — good pattern. |
| EV-AWS-039 | 2026-09-25T17:30Z | file | `content/labs/ul-18.json` teardown | ECS cluster + IAM role | Read | Fargate cleanup; mirrors gl-18. |
| EV-AWS-040 | 2026-09-25T17:30Z | file | `content/labs/ul-19.json` teardown | EKS cluster wait deleted | Read | Same subnetIds concern as gl-19. |
| EV-AWS-041 | 2026-09-25T17:30Z | file | `content/labs/ul-20.json` teardown | `terraform destroy -auto-approve` | Read | Differs from gl-20 interactive destroy — note for facilitators. |
| EV-AWS-042 | 2026-09-25T17:30Z | file | `content/labs/ul-21.json` teardown | ElastiCache subnet group delete | Read | OK ordering after cluster delete. |

## Supplemental evidence

| EV-ID | Timestamp (UTC) | Type | Locator | Excerpt | Tool run |
|---|---|---|---|---|---|
| EV-AWS-043 | 2026-09-25T17:25Z | command | `scripts/scan_lab_placeholders.py` | Output: `PASS 41 labs scanned` | `python scripts\scan_lab_placeholders.py` (read-only) |
| EV-AWS-044 | 2026-09-25T17:26Z | file | `scripts/scan_lab_placeholders.py` L54–66 | Variable symmetry check body is `pass` (no enforcement) | Read |
| EV-AWS-045 | 2026-09-25T17:27Z | file | `reports/evidence/lab-commands.md` | 316 command rows (guided labs gl-01–gl-21) | Read full extract |
| EV-AWS-046 | 2026-09-25T17:28Z | file | `docs/change-requests.md` CR-0005 | LocationConstraint, Macie, teardown variable issues listed | Read |
| EV-AWS-047 | 2026-09-25T17:29Z | file | `reports/evidence/sample.md` | 429 sampled question IDs; all 23 lessons; 42 labs | Read |
| EV-AWS-048 | 2026-09-25T17:31Z | file | `content/lessons/lesson-1-3.json` | SAA 1.3 lesson bodyMarkdown (KMS tradeoff boilerplate) | Read all 16 SAA lessons (a0 + 1-1…4-4) |
| EV-AWS-049 | 2026-09-25T17:32Z | file | `content/questions/q-saa-1-3-s02-mc.json` | Template stem "Which statement best reflects this exam objective" | Spot-check + sample list |
| EV-AWS-050 | 2026-09-25T17:33Z | MCP | AWS CreateBucketConfiguration | us-east-1: do not need to specify location | `aws___search_documentation` |
| EV-AWS-051 | 2026-09-25T17:34Z | MCP | API CreateNetworkAclEntry | Protocol -1 allows all ports; port range for TCP/UDP only | `aws___read_documentation` |
| EV-AWS-052 | 2026-09-25T17:35Z | MCP | EC2 user data guide | Amazon Linux uses cloud-init/bash, not PowerShell tags | `aws___search_documentation` |
| EV-AWS-053 | 2026-09-25T17:36Z | MCP | EKS create-cluster example | `subnetIds=subnet-a,subnet-b` comma-separated | `aws___search_documentation` |
| EV-AWS-054 | 2026-09-25T17:37Z | MCP | macie2 update_macie_session | status PAUSED suspends Macie activities | `aws___search_documentation` |
| EV-AWS-055 | 2026-09-25T17:38Z | MCP | S3 delete-bucket-lifecycle | `aws s3api delete-bucket-lifecycle --bucket` documented | `aws___search_documentation` |
| EV-AWS-056 | 2026-09-25T17:39Z | file | `content/labs/ul-05.json` verification L81 | Tag filter `LabId,Values=gl-05` on ul-05 lab | Read |

## Command extract coverage note

`lab-commands.md` includes **gl-01 through gl-21 only** (no ul-* step rows). Unguided labs reviewed via teardown blocks and acceptance criteria (EV-AWS-022–042).
