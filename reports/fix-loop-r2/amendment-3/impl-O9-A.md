# O9-A implementation report — GL-01 through GL-10

Batch O9-A per Amendment 3 (`.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`), fixing
TEACHER-209 (sidecar files) and TEACHER-210 (s12–s15 boilerplate) in `content/labs/gl-01.json`
through `gl-10.json`. No other paths touched. No `aws`/`git` commands run.

## TEACHER-209 — sidecar files

Every `file://<name>` reference in this batch now has a preceding bullet that writes the file
with `$utf8 = New-Object System.Text.UTF8Encoding $false; [IO.File]::WriteAllText(...)`, matching
the GL-08 `user-data.sh` pattern. Static JSON (no lab variables) uses a single-quoted literal;
JSON that needs a lab variable (bucket name, account/caller ARN, AMI ID, queue/topic ARN) is built
as a PowerShell hashtable and serialized with `ConvertTo-Json -Depth 10 -Compress`, then written
with the same no-BOM `WriteAllText` call.

| Lab | Step | File | Shape | Doc checked |
| --- | --- | --- | --- | --- |
| gl-01 | s06 | `gl01-boundary.json` | IAM managed policy: Allow `*`/`*`, Deny `cloudhsm:*`,`shield:*`,`directconnect:*`,`outposts:*` on `*` | IAM JSON policy grammar (2012-10-17) |
| gl-01 | s10 | `gl01-budget.json` | `BudgetName`, `BudgetLimit{Amount,Unit}`, `TimeUnit=MONTHLY`, `BudgetType=COST` | docs.aws.amazon.com/aws-budgets (create-budget CLI shape) |
| gl-02 | s08 | `lifecycle.json` | `Rules[{ID,Filter.Prefix,Status,Expiration.Days}]` | docs.aws.amazon.com/AmazonS3 PutBucketLifecycleConfiguration |
| gl-02 | s10 | `gl02-policy.json` | Deny `s3:PutObject` on `arn:aws:s3:::$Bucket/*` when `aws:SecureTransport=false` | docs.aws.amazon.com/AmazonS3/userguide/security_s3_ssl.html (TLS-only bucket policy pattern) |
| gl-03 | s07 | `gl03-trust.json` | Trust policy: Allow `sts:AssumeRole`, Principal `AWS: $CallerArn` (added a `$CallerArn = aws sts get-caller-identity --query Arn --output text` bullet, since s02 only captured `$AccountId`) | IAM trust-policy grammar |
| gl-03 | s08 | `gl03-s3read.json` | Two statements: `s3:ListBucket` on bucket ARN, `s3:GetObject` on bucket ARN + `/*` | IAM policy grammar / S3 ARN format |
| gl-09 | s07 | `gl09-lt.json` | `ImageId=$AmiId`, `InstanceType=t3.micro`, `TagSpecifications[{ResourceType=instance,Tags[{Key,Value}]}]` | docs.aws.amazon.com/AWSEC2 RequestLaunchTemplateData |
| gl-10 | s06 | `gl10-trust.json` | Trust policy: Allow `sts:AssumeRole`, Principal Service `lambda.amazonaws.com` | IAM trust-policy grammar |
| gl-10 | s08 | `gl10-queue-policy.json` | Allow `sqs:SendMessage`, Principal Service `sns.amazonaws.com`, Resource `$QueueArn`, Condition `ArnEquals aws:SourceArn=$TopicArn` | docs.aws.amazon.com/AWSSimpleQueueService SQS policy examples (SNS fan-out pattern) |

gl-04, gl-05, gl-06, gl-07 have no `file://` references in this batch — confirmed by grep before editing.

## TEACHER-210 — s12–s15 wording

Rewrote the "Cost checkpoint" bullet (s12) in every lab that had the generic
"Stopping an instance or scaling to zero is not teardown." line, replacing it with the lab's real
billing model, and kept the success/verification lines unchanged.

| Lab | Before | After |
| --- | --- | --- |
| gl-01 | `stopChargesPanel` ended with a redundant "This lab creates no instance. Stopping an instance is not teardown." (no instances exist here at all) | "IAM users, policies, MFA devices, and alert-only budgets carry no charge, so nothing in this lab bills hourly or otherwise." |
| gl-02 | Generic "Stopping an instance or scaling to zero is not teardown." (no instances in this lab) | "S3 bills storage per GB-month and PUT/GET requests per request; nothing in this lab is hourly, and there is no instance to stop." |
| gl-03 | Same generic line (IAM role + S3, no instances) | "IAM roles and policies carry no charge; the only cost here is S3 storage and request charges for the one small object you uploaded. There is no instance to stop." |
| gl-04 | Same generic line (KMS + S3, no instances) | "A customer-managed KMS key bills a monthly per-key fee (prorated) plus per-request charges for encrypt and decrypt calls; S3 adds storage and request charges. Scheduling deletion does not stop the monthly key fee until the 7-day waiting window ends." |
| gl-05 | Same generic line (VPC only, no instances, no NAT) | "VPCs, subnets, route tables, security groups, NACLs, and S3 gateway endpoints carry no hourly charge. This lab has no NAT gateway and no instance, so there is nothing hourly to stop." |
| gl-06 | Same generic line (NAT gateway lab, no EC2 instance) | "A NAT gateway bills hourly plus per-GB of data processed, and an unattached Elastic IP also bills hourly. Deleting the NAT gateway and releasing the EIP in step s11 is what stops that charge, not just removing the private route." |
| gl-07 | Same generic line (this one *does* have an EC2 instance) | "The t3.micro bills hourly while running. Terminating it stops that charge, but the gp3 volume and the snapshot keep billing per GB-month until you delete them. Stopping an instance instead of terminating it is not teardown." |
| gl-08 | Same generic line (ALB + EC2 target, in scope for this batch) | "The Application Load Balancer bills hourly plus per LCU-hour, and the t3.micro target bills hourly while running. Stopping the instance instead of terminating it is not teardown, and the ALB keeps billing until you delete it." |
| gl-09 | Same generic line (Auto Scaling group; "scaling to zero" is a real intermediate step here) | "Launch templates and the Auto Scaling group itself carry no charge; the t3.micro instance the group launches bills hourly while it exists. Scaling to 0 stops that hourly charge, but the ASG resource still exists until you delete it in step s10." |
| gl-10 | Same generic line (SNS/SQS/Lambda, no instances) | "SNS, SQS, and Lambda all bill per request (each has its own monthly free tier), and CloudWatch Logs bills per GB stored. Nothing in this lab is hourly, and there is no instance to stop." |

Also fixed an "Order the deletes" (s13) inconsistency found in gl-05: the prose listed
`VPC endpoint, NACL restore, route disassociation, subnets, IGW, SG, NACL, VPC` (NACL mentioned
twice, in the wrong position), which did not match the actual `orderedDeletesPowerShell` sequence
(endpoint → NACL restore → NACL delete → route disassociation/deletion → subnets → IGW → SG →
VPC). Rewrote the prose to match the existing teardown commands; the commands themselves were not
changed.

s13/s14/s15 in the other labs were checked against each lab's `orderedDeletesPowerShell` and
already matched, so left unchanged, per the instruction not to touch teardown commands unless the
prose disagreed with them.

## Verification

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `questions 429 aws 310 tf 119` /
  `labs 21 + 21` / `lessons 23` / **PASS**
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → **PASS 42 labs scanned**
- Every new/changed PowerShell bullet across the 10 files (11 lines: the 9 sidecar-writing lines
  plus the 1 added `$CallerArn = aws sts get-caller-identity ...` line, plus re-confirmed the
  pre-existing gl-08 `user-data.sh` line) was parsed with
  `[System.Management.Automation.Language.Parser]::ParseInput` under PowerShell 5.1 — all
  `PARSE-OK`, no AST errors.
- Each `WriteAllText`/`ConvertTo-Json` line was executed in a scratch folder (writing only a local
  file — no AWS calls) with dummy stand-in values for lab variables (`$Bucket`, `$CallerArn`,
  `$AmiId`, `$QueueArn`, `$TopicArn`). All 9 produced files that parsed as valid JSON with
  `ConvertFrom-Json` and had no UTF-8 BOM (`0xEF 0xBB 0xBF` check on the raw bytes).
- Re-loaded all 10 changed `content/labs/gl-0*.json` / `gl-10.json` files with Python `json.load`
  and confirmed no BOM and valid JSON after the edits.
- Files were saved via `json.load` / `json.dumps(data, indent=2, ensure_ascii=True) + "\n"` in
  text mode with `encoding="utf-8"`, using `backend\.venv\Scripts\python.exe`, per the batch rules
  — this is why previously-literal em dashes (`—`) in titles/notes in the touched files now show
  as `—` in the diff; content is unchanged, only the escaping.

## Scope confirmation

Only `content/labs/gl-01.json` … `gl-10.json` were edited (including gl-08, wording-only, no
sidecar work needed there). No files in `gl-11`–`gl-21` were touched. No `git`/`git stash`/`aws`
commands were run.
