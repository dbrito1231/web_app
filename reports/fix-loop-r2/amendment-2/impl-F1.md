# Batch F1 implementation log (Amendment 2, round-3 fixes)

Scope: `content/labs/gl-07.json`, `gl-14.json`, `gl-17.json`, `gl-19.json`, `gl-21.json`. No other files touched. No AWS calls made.

## GL-14 — AWS-R3-002 (subnet ID join)

**Before:** `$Subnets = aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text` then `--subnet-ids $Subnets`. Under PS 5.1, `--output text` on a 2-item list returns one tab-separated string, so `create-db-subnet-group` received a single malformed subnet ID.

**After:** `$SubnetIds = (aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text) -split '\s+' | Where-Object { $_ }`, then `--subnet-ids $SubnetIds`. Step s06 updated (both the lookup line and the `create-db-subnet-group` line).

Doc: https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output

## GL-21 — AWS-R3-002 (subnet ID join)

Same fix pattern as GL-14, applied to step s06 (`Cache subnet group`): the subnet lookup now produces `$SubnetIds` via `-split '\s+'`, and `create-cache-subnet-group --subnet-ids $SubnetIds` replaces the old `$Subnets` reference.

Doc: https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output

## GL-19 — AWS-R3-002 (EKS subnetIds join) + AWS-R3-003 (us-east-1e) + AWS-R3-005 (panel wording)

**Before (s07):** `$Subnets = aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text`, then `$SubnetList = (($Subnets -split ' +') | Where-Object { $_ }) -join ','` — splitting on a literal space does not split a tab-joined string, so `subnetIds=` still received one malformed value. The default-VPC subnet pick could also land on `us-east-1e`, which EKS rejects for the control plane.

**After:** the `describe-subnets` filter now adds `Name=availability-zone,Values=us-east-1a,us-east-1b` to exclude `us-east-1e`. The split now uses `-split '\s+'` into `$SubnetIds`, and the cluster is created with `subnetIds=$($SubnetIds -join ',')` (comma-joined array, per the AWS report).

**stopChargesPanel before:** "Delete cluster, IAM roles, security groups AWS creates; control plane bills hourly." — implied a manual SG delete step that does not exist.

**stopChargesPanel after:** "Delete the cluster and wait (EKS removes the cluster security group and network interfaces it created), then the IAM role; control plane bills hourly."

Added a teardown verification line: `aws ec2 describe-security-groups --filters Name=tag:aws:eks:cluster-name,Values=workbook-gl19 --query "SecurityGroups[].GroupId"` returns `[]`.

Docs: https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html ; https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html ; https://docs.aws.amazon.com/eks/latest/userguide/delete-cluster.html

## GL-17 — AWS-R3-004 (async DROP race)

**Before:** s09 and the teardown fired `DROP TABLE` then immediately `DROP DATABASE` via `start-query-execution` with no wait; both are asynchronous, so `DROP DATABASE` could run before the table drop finished, and the later bucket delete/empty could race a still-running query.

**After:** each `start-query-execution` for `DROP TABLE` / `DROP DATABASE` now captures `--query QueryExecutionId --output text` into `$DropTableId` / `$DropDbId`, followed by a `do { Start-Sleep -Seconds 2; ... get-query-execution --query-execution-id $Id --query QueryExecution.Status.State --output text } while ($State -eq 'QUEUED' -or $State -eq 'RUNNING')` poll before moving on. Applied identically in step s09 and in `teardown.orderedDeletesPowerShell` (teardown lines wrap the poll in `if ($Id) { ... }` since teardown variables are guarded there). Bucket empty/delete steps now only run after both polls resolve.

Docs: https://docs.aws.amazon.com/athena/latest/ug/drop-database.html ; https://awscli.amazonaws.com/v2/documentation/api/latest/reference/athena/get-query-execution.html

## GL-07 — TEACHER-R3-013 (s13 wording)

**Before:** "A NotFound or IncorrectState error on a line means that resource is already gone"

**After:** "NotFound means the volume is already gone; IncorrectState on detach means it is already detached." (matches the Teacher's requested wording exactly)

## Verification performed

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → PASS (`questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23`)
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → PASS (42 labs scanned)
- Every changed PowerShell line parsed with `[System.Management.Automation.Language.Parser]::ParseInput(...)` in PS 5.1 → 0 errors across all 10 changed lines.
- `git status` confirms only `gl-07.json`, `gl-14.json`, `gl-17.json`, `gl-19.json`, `gl-21.json` were touched by this batch (other `ul-*` diffs in the working tree belong to the parallel F2 batch).
- Grep confirms no `= $null`, no `-ErrorAction` on any `aws` line was introduced in the five files.

## Unresolved / out of scope for F1

- AWS-R3-001 (paginated `[0]` lookups in UL-10/11/12/17) is out of scope — those files belong to batch F3.
- AWS-R3-006/007/008/009/010/011 and the various TEACHER-R3-* items for UL labs belong to batches F2/F3.
- Nothing unresolved within F1's own scope (GL-07, GL-14, GL-17, GL-19, GL-21) — all four assigned items (AWS-R3-002 x3, GL-17 async fix, GL-19 us-east-1e + panel wording, TEACHER-R3-013) are implemented and verified.
