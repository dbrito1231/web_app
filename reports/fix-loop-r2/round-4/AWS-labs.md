# Fix-loop r2, round 4 (labs): AWS Architect re-check of Amendment 2 F1–F3

Reviewer: Senior AWS SA (read-only). Commits: `983fc78` (F1), `fa763c2` (F2), `0f96bf5` (F3). Diff: `git diff 6820628 0f96bf5 -- content/labs` (23 files). I made no AWS calls and started no servers. Only this report file was written.

## Local checks (no state changed, scratchpad only)

- **Parser:** Windows PowerShell 5.1.26100 `[Parser]::ParseInput` over all 386 `orderedDeletesPowerShell` lines and 311 `Run \`…\`` step commands in 42 labs. There are **0 errors in teardown lines**. The 3 step hits are pre-existing and unchanged, and none is a real error: the GL-01 `<SerialNumber Arn>` placeholder, plus GL-08 s08 and GL-17 s06, where my regex cut the command at the `` `n `` escape.
- **PS 5.1 native-argument test**, using a Python argv echo in place of `aws`:
  - GL-14/GL-21 `(… ) -split '\s+' | Where-Object { $_ }` turns a tab-joined string into `['--subnet-ids','subnet-aaa','subnet-bbb']`, and one ID into one argument. PS 5.1 splats an array variable into separate native arguments. **Correct.**
  - GL-19 `subnetIds=$($SubnetIds -join ',')` becomes the single argument `subnetIds=subnet-aaa,subnet-bbb`. The two-filter `--filters Name=vpc-id,Values=… Name=availability-zone,Values=us-east-1a,us-east-1b` reaches the CLI as two arguments. **Correct.**
  - UL-11 multi-line JSON piped to `ConvertFrom-Json` without `Out-String` parses in 5.1. A single match gives `.ApiId`; `[]` gives `$null` (guard false). Two matches give a 2-element array (see AWS-R4L-003).
  - A native call that writes only to stderr (a missing resource) leaves the variable `$null`, and `$X -and $X -ne 'None'` is then false. This covers `describe-table`, `get-function`, `get-work-group` and `get-crawler` when the resource is absent. **Correct.**
  - The UL-16 guard gives `'True'→False`, `'False'→True` and `$null→False`. The UL-19 paged `list-roles` values behave safely: `@('None','x')` → guard true, `@('None','None')` → guard false. The UL-09 guard skips `'None'` and passes an ID array.

## Verdict table: AWS round-3 items

| ID | Lab | Verdict | Evidence (current content) | Doc URL |
|---|---|---|---|---|
| AWS-R3-001 | UL-10 | **Gone** | Topic ARN is built as `"arn:aws:sns:us-east-1:$($AccountId):workbook-ul10"`, so no list call is needed; `delete-topic` is idempotent ("deleting a topic that does not exist does not result in an error"). Table lookup is now `dynamodb describe-table --table-name workbook-ul10-idem --query Table.TableName` | https://docs.aws.amazon.com/sns/latest/api/API_DeleteTopic.html ; https://awscli.amazonaws.com/v2/documentation/api/latest/reference/dynamodb/describe-table.html |
| AWS-R3-001 | UL-11 | **Gone** (edge cases in R4L-002/003) | `get-apis … --output json \| ConvertFrom-Json`: JSON output is "processed as a single, native structure before the --query filter is applied". `lambda get-function --function-name workbook-ul11-auth --query Configuration.FunctionName`. `list-user-pools … --output json \| ConvertFrom-Json` | https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html ; https://docs.aws.amazon.com/cli/latest/reference/apigatewayv2/get-apis.html |
| AWS-R3-001 | UL-12 | **Gone** | `$SmArn = "arn:aws:states:us-east-1:$($AccountId):stateMachine:workbook-ul12"` (unqualified ARN form per the API reference); task Lambda uses `get-function` | https://docs.aws.amazon.com/step-functions/latest/apireference/API_DeleteStateMachine.html |
| AWS-R3-001 | UL-17 | **Gone** | `athena get-work-group --work-group workbook-ul17 --query WorkGroup.Name`; `glue get-crawler --name workbook-ul17 --query Crawler.Name`. Both return nothing on stdout when the resource is absent, so the guard skips the delete | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/athena/get-work-group.html ; https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-crawler.html |
| AWS-R3-001 | UL-19 | **Gone / harmless** (kept as `list-roles \| [0]`) | Deletes use the literal role name, and a paged array `@('None','workbook-ul19-eks')` still gives the right guard result (tested) | https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html |
| AWS-R3-002 | GL-14 s06 | **Gone** | `$SubnetIds = (… --output text) -split '\s+' \| Where-Object { $_ }` → `--subnet-ids $SubnetIds` (tested: 2 separate arguments) | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/rds/create-db-subnet-group.html |
| AWS-R3-002 | GL-21 s06 | **Gone** | Same pattern → `create-cache-subnet-group --subnet-ids $SubnetIds` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/elasticache/create-cache-subnet-group.html |
| AWS-R3-002 | GL-19 s07 | **Gone** | `-split '\s+'` then `subnetIds=$($SubnetIds -join ',')` (tested) | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/eks/create-cluster.html |
| AWS-R3-003 | GL-19 s07 | **Gone as written, but the fix is imperfect** (my R3 suggestion was wrong; see AWS-R4L-004) | `Name=availability-zone,Values=us-east-1a,us-east-1b` is valid syntax. EKS disallows the AZ **ID** `use1-az3`, and AZ names map to different AZ IDs in each account | https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html |
| AWS-R3-003 | UL-19 C1 | **Still present** (Low) | C1 says "in the default VPC (as in GL-19)" but has no note about the disallowed AZ; the new hint 1 covers only Fargate/private subnets | same |
| AWS-R3-004 | GL-17 s09 + teardown L3–L6 | **Gone** | Each DROP captures `QueryExecutionId`, then `do { Start-Sleep 2; … get-query-execution … Status.State } while (QUEUED or RUNNING)` runs before the next DROP and before `s3 rm`. Teardown polls are guarded by `if ($DropTableId)`. The loop ends on SUCCEEDED, FAILED or CANCELLED, or on an empty value | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/athena/get-query-execution.html ; https://docs.aws.amazon.com/athena/latest/ug/drop-database.html |
| AWS-R3-005 | GL-19 panel + verification | **Gone** | The panel now says "Delete the cluster and wait (EKS removes the cluster security group and network interfaces it created)…". Verification adds `describe-security-groups --filters Name=tag:aws:eks:cluster-name,Values=workbook-gl19 … returns []` | https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html |
| AWS-R3-006 | UL-04 last criterion | **Gone** | "Tag search LabId=ul-04 shows only the KMS key, in PendingDeletion." | https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html |
| AWS-R3-007 | UL-16 L12–L14 | **Gone** | `$IsDefault = aws ec2 describe-vpcs --vpc-ids $VpcId --query "Vpcs[0].IsDefault"`; `$NotDefaultVpc = ($IsDefault -eq 'False')`; `if ($VpcId -and $NotDefaultVpc) { delete-vpc }`. A failed describe gives `$null`, so the delete is skipped (tested) | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-vpcs.html |
| AWS-R3-008 | UL-09 L5 | **Gone** | `if ($AsgInstanceIds -and $AsgInstanceIds -ne 'None')` | https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output |
| AWS-R3-008 | UL-07 L5, UL-09 L6, GL-09 L2, (new) GL-17 polls | **Still present** (Low) | No iteration cap was added to the `do … while` loops. UL-07 recovery still has no line saying "if delete-file-system returns FileSystemInUse, rerun the poll line, then the delete" | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/efs/delete-file-system.html |
| AWS-R3-009 | UL-15 C2/C3 | **Gone** | C3 is now "Trail `workbook-ul15` logs management events to the ul-15 bucket." | — |
| AWS-R3-010 | UL-08 hint 3; UL-11 hint 2, C14 | **Gone** | All now say `curl.exe`; a grep finds no bare `curl` in any lab | https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-5.1 |
| AWS-R3-011 | UL-18 L10 | **Gone** | `--filters Name=group-name,Values=workbook-ul18-sg Name=tag:LabId,Values=ul-18` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-security-groups.html |

## Verdict table: Teacher round-3 items that touch commands

| ID | Lab | Verdict | Evidence | Doc URL |
|---|---|---|---|---|
| TEACHER-R3-001 | UL-15 | **Gone** | CloudTrail criterion restored as C3 (see above) | — |
| TEACHER-R3-002 | UL-01 | **Gone** | `foreach ($P in ((aws iam list-role-policies --role-name workbook-ul01-daily --query PolicyNames --output text) -split '\s+')) { if ($P -and $P -ne 'None') { delete-role-policy … } }` for each role, placed before `delete-role`. An empty or absent role gives `''`, which is skipped (tested) | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/list-role-policies.html |
| TEACHER-R3-003 | UL-02 | **Gone as written, but it adds a new Medium** (AWS-R4L-001) | The new C1 names `workbook-ul02-<account-id>`. L3 is now `if (-not $Bucket) { $Bucket = "workbook-ul02-…" }` | — |
| TEACHER-R3-006 | UL-16 | **Gone** | The record delete is split into 3 guarded, commented lines: build → write+submit → wait | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/route53/change-resource-record-sets.html |
| TEACHER-R3-007 | UL-16 | **Gone** | `# Delete any subnets and security groups you added to $VpcId before delete-vpc` | — |
| TEACHER-R3-008 | UL-19 | **Gone** | One guarded 4-line block per role (eks, node, fargate): detach managed → delete inline → delete role | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/delete-role.html |
| TEACHER-R3-010 | UL-21 | **Gone** (see AWS-R4L-006 for a Low follow-up) | `terraform logout app.terraform.io` is a real command line; usage is `terraform logout [hostname]` | https://developer.hashicorp.com/terraform/cli/commands/logout |
| TEACHER-R3-015 | UL-20 | **Gone** | `head-bucket` moved to verification ("returns 404"); the `gl-20` tag check is explained ("only relevant if you imported the GL-20 bucket") | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/head-bucket.html |

## Command-syntax check (changed and added commands)

All of the following are valid AWS CLI v2 syntax as written for PS 5.1:
- **Athena:** `athena start-query-execution … --query QueryExecutionId --output text`; `athena get-query-execution --query-execution-id … --query QueryExecution.Status.State`; `athena get-work-group --work-group`.
- **Filters:** `ec2 describe-subnets` with two `--filters` entries and a comma list; `ec2 describe-security-groups --filters Name=tag:aws:eks:cluster-name,Values=…`; `ec2 describe-vpcs --query "Vpcs[0].IsDefault"` (text output prints `True`/`False`, and the PS `-eq` comparison is case-insensitive).
- **Direct lookups:** `lambda get-function --query Configuration.FunctionName`; `dynamodb describe-table --query Table.TableName`; `glue get-crawler --name`.
- **Others:** `iam list-role-policies --query PolicyNames`; `terraform logout app.terraform.io`.
- **Paginated list calls:** `get-apis` and `list-user-pools` are paginated operations (their synopses list `--starting-token`, `--page-size` and `--max-items`). With `--output json`, the whole result is aggregated before `--query` runs.

## Teardown order and blast radius

The order is correct in every changed lab:
- **GL-17:** DROP TABLE (wait) → DROP DATABASE (wait) → empty the buckets → delete the buckets.
- **UL-10:** event source mappings → function → log group → queues → topic → table → IAM.
- **UL-12:** stop the RUNNING executions → `delete-state-machine`. This call is asynchronous: the state machine goes to DELETING and is removed when its executions complete. Then log groups → Lambda → IAM.
- **UL-16:** records → wait → zone → VPC.
- **UL-19:** node groups and Fargate profiles → cluster (wait) → log group → roles.
- **UL-21:** cluster (wait) → subnet group.

Protection against deleting anything outside the lab has improved: the UL-18 SG is found by tag, UL-16 checks for the default VPC, and UL-10/12 use exact names and ARNs. **One regression:** the UL-02 bucket variable (AWS-R4L-001).

## New issues

| ID | Sev | Conf | Lab / step | Problem | Exact fix | Doc URL |
|---|---|---|---|---|---|---|
| AWS-R4L-001 | **Medium** | High | UL-02 teardown L3 (and L5–L10) | `if (-not $Bucket) { … }` trusts whatever `$Bucket` holds in the current shell. Eleven labs set `$Bucket` in their steps or teardown (GL-02/03/04/15/17/20, UL-03/04/15/17). The GL-02 build (s0x) and the GL-02 teardown both leave `$Bucket = workbook-gl02-<acct>`. The natural order is GL-02 → UL-02 in one window. There, (a) a learner who made a new UL-02 bucket gets a teardown aimed at the GL-02 name, so the UL-02 bucket is orphaned; and (b) if another lab's bucket still exists (for example GL-03/04/17 in progress), L5–L10 remove its bucket policy, **delete every object version** and delete that bucket. That is data outside this lab | Use a lab-specific variable and always echo it: L1 `# Uses: $Ul02Bucket (optional — set it to your GL-02 bucket name if you reused it)`; L3 `if (-not $Ul02Bucket) { $Ul02Bucket = "workbook-ul02-$((aws sts get-caller-identity --query Account --output text))" }; "Deleting bucket: $Ul02Bucket"`; replace `$Bucket` with `$Ul02Bucket` on L5–L10. Optional hard guard: `$Lab = aws s3api get-bucket-tagging --bucket $Ul02Bucket --query "TagSet[?Key=='LabId'].Value \| [0]" --output text` and run L5–L10 only `if ($Lab -eq 'ul-02' -or $Lab -eq 'gl-02')` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/get-bucket-tagging.html |
| AWS-R4L-002 | Low | Medium | UL-11 L13 | `list-user-pools --max-results 60`. The current CLI v2 reference lists no `--max-results` (the synopsis has only `--starting-token`, `--page-size` and `--max-items`, and it is no longer required; my R3 note that it is required was wrong). In the CLI, passing the API's own limit key directly turns auto-pagination off, so with more than 60 pools `workbook-ul11` may be silently missed | Replace `--max-results 60` with `--page-size 60` (or drop it) | https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/list-user-pools.html ; https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-pagination.html |
| AWS-R4L-003 | Low | High | UL-11 L4–L5, L13–L14 | API names and user-pool names are not unique. A learner who reruns a create step has two `workbook-ul11` APIs or pools. `$ApiId` is then a 2-element array (tested), and `delete-api --api-id a b` fails with "Unknown options", which leaves both | `foreach ($Id in @($ApiId)) { if ($Id) { aws apigatewayv2 delete-api --api-id $Id } }`, and the same for `$PoolId` / `delete-user-pool` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/apigatewayv2/delete-api.html |
| AWS-R4L-004 | Low | High | GL-19 s07 (and UL-19 C1, carried from R3-003) | EKS disallows subnets in the **AZ ID** `use1-az3`. AZ **names** such as us-east-1a/b are mapped to different AZ IDs in each account, so the `availability-zone` name filter does not reliably exclude it (my R3 suggestion caused this) | GL-19 s07: `--filters Name=vpc-id,Values=$VpcId Name=availability-zone-id,Values=use1-az1,use1-az2,use1-az4,use1-az6`. UL-19: add a hint, "EKS rejects subnets in AZ ID use1-az3; pick default-VPC subnets by `availability-zone-id` as in GL-19" | https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html ; https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-subnets.html |
| AWS-R4L-005 | Low | High | UL-16 L9 | If `change-resource-record-sets` fails (for example InvalidChangeBatch), `$ChangeId` is `$null` and `wait … --id` fails with "expected one argument". `delete-hosted-zone` then fails with HostedZoneNotEmpty. The damage is limited to a confusing error | `if ($ZoneId -and $Rrs -and $ChangeId) { aws route53 wait resource-record-sets-changed --id $ChangeId }` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/route53/wait/resource-record-sets-changed.html |
| AWS-R4L-006 | Low | High | UL-21 L4–L5, panel | "The API token is only removed locally"; it stays valid in HCP Terraform until it is revoked. The panel says "remove local terraform tokens", but nothing tells the learner to revoke the token | Add `# terraform logout only deletes the local copy; revoke the token in HCP Terraform (User settings → Tokens)` after L5, and a verification line saying the token no longer appears in User settings → Tokens | https://developer.hashicorp.com/terraform/cli/commands/logout |

## Overall

**Pass with one Medium follow-up.** All 11 AWS round-3 items are Gone, except AWS-R3-003 for UL-19 (Low) and the loop-cap and recovery half of AWS-R3-008 (Low). All 8 Teacher command items are Gone. Every changed teardown line parses in PS 5.1 (0 errors in 386 lines). The subnet arrays, the Athena polls, the direct `get-*`/`describe-*` lookups and the UL-16 default-VPC guard behave correctly in local PS 5.1 tests. Teardown order is correct. Fix **AWS-R4L-001** (the UL-02 stale `$Bucket` can empty and delete another lab's bucket) before the labs are called done. AWS-R4L-002 to 006 are Low.
