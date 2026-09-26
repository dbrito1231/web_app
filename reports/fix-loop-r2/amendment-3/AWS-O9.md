# AWS review — O9 (commits b761f9f, 0eba340)

Reviewer: Senior AWS Solutions Architect (read-only). Scope: `content/labs/gl-01.json`
through `gl-21.json`, sidecar-writing bullets added/changed in commits `b761f9f` (GL-01–GL-10)
and `0eba340` (GL-11–GL-21), plus the s12–s15 rewrites. No AWS calls made; no files edited.

Method:
- `git show` on both commits, full diff, cross-checked against `impl-O9-A.md` / `impl-O9-B.md`.
- Every new/changed `file://` writer line extracted and executed verbatim (with stand-in
  variable values) in a scratch folder via the PowerShell tool: parsed first with
  `[System.Management.Automation.Language.Parser]::ParseInput` (PS 5.1 AST), then run for real,
  then the output checked with `ConvertFrom-Json` and a raw-byte BOM check; `function.zip` opened
  with `System.IO.Compression.ZipFile` and its entry contents read back.
- IAM/ASL/task-definition/network-configuration shapes checked against AWS docs via
  `search_documentation` / `read_documentation` (AWS Knowledge MCP).
- Billing claims checked against known AWS pricing models for each service; delete order checked
  against each lab's own `teardown.orderedDeletesPowerShell`.

## Per-lab table

| Lab | Sidecars valid y/n | s12–s15 correct y/n | Evidence / doc |
| --- | --- | --- | --- |
| GL-01 | y | y | `gl01-boundary.json` (Allow \*/\*, Deny 4 services/\*) and `gl01-budget.json` parsed OK, no BOM. IAM JSON policy grammar per docs.aws.amazon.com/IAM/.../reference_policies_elements.html. IAM/budget-only cost line correct (no billable resources). |
| GL-02 | y | y | `lifecycle.json`, `gl02-policy.json` parsed OK, no BOM. Lifecycle shape (`Rules[].Filter.Prefix/Status/Expiration.Days`) matches PutBucketLifecycleConfiguration; TLS-deny bucket policy matches docs.aws.amazon.com/AmazonS3/userguide/security_s3_ssl.html pattern (scoped to `s3:PutObject` only, matching the lab's own instruction). S3 storage/request billing line correct. |
| GL-03 | y | y | `$CallerArn` now captured via `aws sts get-caller-identity --query Arn`; `gl03-trust.json` (Principal.AWS = user ARN) and `gl03-s3read.json` (ListBucket on bucket ARN, GetObject on bucket ARN/\*) parsed OK, no BOM. IAM role carries no charge; S3-only billing line correct. |
| GL-04 | n/a (no new sidecar) | y | KMS $1/mo-per-key prorated + per-request, S3 storage/request; "scheduling deletion does not stop the fee until the 7-day window ends" matches KMS pricing/behavior for pending-deletion keys. |
| GL-05 | n/a | y | s13 prose rewritten to match `orderedDeletesPowerShell` exactly (endpoint → NACL restore/delete → route tables → subnets → IGW → SG → VPC). No hourly resources; correct. |
| GL-06 | n/a | y | NAT Gateway hourly + per-GB, unattached EIP hourly — correct; teardown (delete NAT + release EIP) matches. |
| GL-07 | n/a | y | t3.micro hourly, EBS gp3 + snapshot per GB-month — correct. |
| GL-08 | n/a | y | ALB hourly + per-LCU-hour, target t3.micro hourly — correct. |
| GL-09 | y | y | `gl09-lt.json` (ImageId/InstanceType/TagSpecifications) parsed OK, no BOM, matches EC2 `RequestLaunchTemplateData` shape. ASG/LT free, instance hourly — correct. |
| GL-10 | y | y | `gl10-trust.json` (Principal.Service lambda.amazonaws.com) and `gl10-queue-policy.json` (Allow sqs:SendMessage, Principal.Service sns.amazonaws.com, Condition ArnEquals aws:SourceArn) parsed OK, no BOM — matches documented SNS→SQS fan-out policy. SNS/SQS/Lambda per-request + Logs per-GB — correct. |
| GL-11 | y | y | `gl11-trust.json` (Principal.Service lambda.amazonaws.com) parsed OK, no BOM. `function.zip` built for real: contains exactly `lambda_function.py`, handler text confirmed with `def lambda_handler(event, context):` matching `--handler lambda_function.lambda_handler`. Lambda/API-GW/Logs billing — correct. s13 now includes the CloudWatch log group delete step, matching `orderedDeletesPowerShell` (apigatewayv2 → lambda → logs delete-log-group → detach policy → delete role). |
| GL-12 | y, but see AWS-O9-001 | y | `gl12-trust.json` (Principal.Service states.amazonaws.com), `gl12-log-policy.json`, `gl12.asl.json` all parsed OK, no BOM. `gl12-log-policy.json` is a byte-for-byte match of the documented policy at docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html (`logs:CreateLogDelivery` … `logs:DescribeLogGroups`, Resource `*`). ASL (`StartAt`/`States`/`Pass`→`Next`/`Succeed`) is valid per the Amazon States Language state-machine-structure doc. Standard Workflow per-transition billing — correct. See AWS-O9-001: the log policy is attached but never used. |
| GL-13 | n/a | y | DynamoDB on-demand per-request + per-GB-month storage — correct. |
| GL-14 | n/a | y | RDS db.t3.micro instance-hour + storage/backups; "stopping still bills for storage" — correct. |
| GL-15 | n/a | y | CloudTrail management events free, trail S3 bucket per GB-month, CloudWatch alarm small per-alarm-month — correct. |
| GL-16 | n/a | y | Route 53 private hosted zone small monthly + per-million-query — correct. |
| GL-17 | n/a | y | Athena per-TB-scanned (rounds to minimum) + S3 storage — correct. |
| GL-18 | y | y | `gl18-trust.json` (Principal.Service ecs-tasks.amazonaws.com), `gl18-task.json`, `network.json` all parsed OK, no BOM. Task definition has `family`, `networkMode=awsvpc` (required for Fargate per docs.aws.amazon.com/AmazonECS/.../task_definition_parameters.html), `requiresCompatibilities=[FARGATE]`, `cpu`/`memory` (both required for Fargate), `executionRoleArn` (role has `AmazonECSTaskExecutionRolePolicy` attached). `$VpcId`/`$SubnetId` are now resolved before `network.json` is written (the s08 fix), closing the previously-undefined-variable defect; `network.json` re-verified valid JSON with the real value. s13 correctly reflects that the teardown never deletes the task definition (task definitions are free to leave registered) and that s10 deregisters it separately. Fargate per-vCPU/GB-second-while-RUNNING billing — correct. |
| GL-19 | y | y | `gl19-eks-trust.json` (Principal.Service eks.amazonaws.com) parsed OK, no BOM, matches docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html. EKS control-plane per-cluster-hour, "cannot be stopped, only deleted" — correct. |
| GL-20 | n/a (Terraform lab, untouched) | y | S3 storage/request billing rewritten to match the s12/s15 pattern used elsewhere; fixture untouched, consistent with `lab-fixtures/gl-20/main.tf`. |
| GL-21 | n/a | y | ElastiCache cache.t3.micro per-node-hour, "no stop feature, only delete-cache-cluster ends it" — correct. |

## New issues

**AWS-O9-001 (Low) — GL-12: CloudWatch Logs execution-role policy is attached but never used.**
`content/labs/gl-12.json`, step `s06`, writes and attaches `gl12-log-policy.json` (the documented
`logs:CreateLogDelivery`/`CreateLogStream`/.../`DescribeLogGroups` permission set for a Step
Functions execution role) to `workbook-gl12-sfn`. The policy content itself is a correct,
byte-for-byte match of AWS's documented example. However, step `s07`'s
`aws stepfunctions create-state-machine` call never passes `--logging-configuration`, so the
state machine is created with logging disabled — the role never uses these permissions, and
CloudWatch Logs is never actually exercised in this lab (a minor least-privilege smell: an unused,
if narrowly-scoped, grant sits on the role for the life of the lab).
*Exact fix*: either (a) add `level=ALL,logGroupArn=...,includeExecutionData=true` via
`--logging-configuration` in s07 (requires creating a log group first and referencing its ARN, so
the permissions get used and the lab actually demonstrates CloudWatch Logs for Step Functions), or
(b) if execution-history logging isn't meant to be taught in this lab, drop the `gl12-log-policy.json`
write and `put-role-policy` bullet from s06 entirely, since the base state machine only needs
`sts:AssumeRole` trust — no other role permissions are required to run a `Pass`→`Succeed`
state machine with no CloudWatch/Lambda/other integrations.

No other new problems at Low or above were found. All 20 tested sidecar-writing PowerShell lines
(across GL-01, GL-02, GL-03, GL-09, GL-10, GL-11, GL-12, GL-18, GL-19) parsed under the PS 5.1 AST
parser with zero errors, executed cleanly in a scratch folder, produced valid UTF-8-no-BOM JSON
(or, for GL-11, a `function.zip` containing exactly the expected handler), and used only variables
that are set earlier in their own lab (GL-03's `$CallerArn`, GL-18's `$SubnetId` — both confirmed
fixed as described in the impl reports).

## Overall: approve

The sidecar-file work (TEACHER-209) is technically sound: every IAM trust/permission policy uses
the correct service principal and valid IAM JSON grammar, the Step Functions ASL and log policy
are verified against AWS's own documented examples, the ECS Fargate task definition carries all
fields required for Fargate, and the two real defects called out in the impl reports (GL-03's
missing `$CallerArn`, GL-18's undefined `$SubnetId`) are genuinely fixed and verified. The s12–s15
rewrites (TEACHER-210) are accurate per-lab billing statements and the one prose/command mismatch
found (GL-05's teardown order) was correctly repaired. AWS-O9-001 is a Low-severity, easily-fixed
loose end (an unused IAM grant) and does not block approval.
