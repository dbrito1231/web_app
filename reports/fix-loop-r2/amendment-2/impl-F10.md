# Amendment 2, Batch F10 — implementation report

Scope: `content/labs/gl-17.json`, `gl-19.json`, `gl-09.json`, `ul-02.json`, `ul-07.json`, `ul-09.json`,
`ul-11.json`, `ul-16.json`, `ul-17.json`, `ul-19.json`, `ul-21.json`. `gl-09.json` and `ul-17.json` were
added beyond the named list because they were the only other lab JSON files with an uncapped
`do { ... } while` poll loop (item 7); a grep of every `content/labs/*.json` for `do \{` / `while \(`
confirmed the full set is exactly these two plus the five already named (`gl-17`, `ul-07`, `ul-09`).
No other files were touched. No AWS calls, no `git`, no `terraform plan/apply`.

## 1. AWS-R4L-001 (UL-02, Medium)

**Before:** teardown reused whatever `$Bucket` held in the shell; 10 other labs also set `$Bucket`, so
an in-progress GL-02/GL-03/GL-04/GL-17/GL-20/UL-03/UL-04/UL-15/UL-17 bucket could be emptied and
deleted by mistake.

**After:**
- Renamed to a lab-specific `$Ul02Bucket`. `# Uses:` line updated to describe it.
- `if (-not $Ul02Bucket) { $Ul02Bucket = "workbook-ul02-$((aws sts get-caller-identity --query Account --output text))" }; Write-Host "Deleting bucket: $Ul02Bucket"` — prints the target before any delete.
- Added `$Ul02BucketLabId = aws s3api get-bucket-tagging --bucket $Ul02Bucket --query "TagSet[?Key=='LabId'].Value | [0]" --output text`.
- Every S3 delete (`delete-bucket-policy`, `list-object-versions`, both version/delete-marker
  `foreach` loops, `delete-bucket-lifecycle`, `delete-bucket`) is now individually guarded by
  `if ($Ul02BucketLabId -eq 'ul-02' -or $Ul02BucketLabId -eq 'gl-02') { ... }`; the first one has an
  `else { Write-Host "Skipping ${Ul02Bucket}: LabId tag is not ul-02 or gl-02" }`.
- The Macie pause line is unchanged/ungated (it is an account-level session setting, not tied to
  the bucket).
- Doc: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/get-bucket-tagging.html

Bug caught during parse-check: `"Skipping $Ul02Bucket: LabId tag is..."` — PowerShell parses
`$Ul02Bucket:` as a drive/scope reference and fails with "Variable reference is not valid". Fixed
by using `${Ul02Bucket}:`.

Test (stubbed, no AWS calls) — see `test_logic.ps1` output: tag `ul-02`/`gl-02` → DELETE; tag
`gl-03`/`'None'`/`$null`/`''` → SKIP; fallback bucket name builds to
`workbook-ul02-111122223333` from a stubbed `aws sts get-caller-identity`.

## 2. AWS-R4L-002 (UL-11)

**Before:** `aws cognito-idp list-user-pools --max-results 60 …` — `--max-results` is not a
`list-user-pools` parameter in the current CLI v2 reference (only `--starting-token`,
`--page-size`, `--max-items`); passing it directly can silently disable auto-pagination.
**After:** `--page-size 60`.
Doc: https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/list-user-pools.html

## 3. AWS-R4L-003 (UL-11)

**Before:** `if ($ApiId -and $ApiId -ne 'None') { aws apigatewayv2 delete-api --api-id $ApiId }` and
the matching Cognito line — both fail if a rerun left two matching APIs/pools (`$ApiId`/`$PoolId`
becomes a 2-element array; `delete-api --api-id a b` errors with "Unknown options").
**After:** both wrapped in `foreach ($Id in @($ApiId)) { if ($Id) { aws apigatewayv2 delete-api --api-id $Id } }` (and the Cognito equivalent), so every matching id is deleted whether there is one or several.
Doc: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/apigatewayv2/delete-api.html

## 4. AWS-R4L-004 / AWS-R3-003 (GL-19, UL-19)

**Before:** GL-19 step s07 filtered subnets with `Name=availability-zone,Values=us-east-1a,us-east-1b`.
EKS rejects the AZ **ID** `use1-az3`, and AZ *names* map to different AZ *IDs* per account, so the
name filter did not reliably exclude it.
**After:** `Name=availability-zone-id,Values=use1-az1,use1-az2,use1-az4,use1-az6`, with an added
sentence explaining why (AZ ID filter, not AZ name). UL-19 hint level 1 gets an appended sentence:
"EKS also rejects subnets in AZ ID use1-az3; pick default-VPC subnets by availability-zone-id, as
GL-19 does." (the existing hint 1 only covered Fargate/private-subnet requirements).
Doc: https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html ;
https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-subnets.html

## 5. AWS-R4L-005 / STUDENT-R4-001 / STUDENT-R4-002 (UL-16)

- **AWS-R4L-005:** `aws route53 wait resource-record-sets-changed --id $ChangeId` now guarded by
  `if ($ZoneId -and $Rrs -and $ChangeId)` instead of `if ($ZoneId -and $Rrs)`, so a failed
  `change-resource-record-sets` (leaving `$ChangeId` null) skips the wait cleanly instead of
  erroring with "expected one argument".
  Doc: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/route53/wait/resource-record-sets-changed.html
- **STUDENT-R4-001:** added acceptance criterion #1: "Name the resources you create
  `workbook-ul16`: private hosted zone `workbook-ul16` and, if you create one, VPC `workbook-ul16`.
  Tag each one LabId=ul-16." (matches the naming-criterion pattern already used in UL-01/02/07/08/15/19/21).
- **STUDENT-R4-002:** the comment "Delete any subnets and security groups you added to $VpcId
  before delete-vpc" is now backed by two real, guarded commands, inserted after the existing
  `$NotDefaultVpc` check and before `delete-vpc`:
  `if ($VpcId -and $NotDefaultVpc) { foreach ($SubnetId in ((aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[].SubnetId" --output text) -split '\s+')) { if ($SubnetId) { aws ec2 delete-subnet --subnet-id $SubnetId } } }`
  and the same pattern for `aws ec2 describe-security-groups --filters Name=vpc-id,Values=$VpcId --query "SecurityGroups[?GroupName!='default'].GroupId" --output text` / `delete-security-group`.
  Both stay inside the pre-existing default-VPC guard (`$NotDefaultVpc`), so the default VPC is
  never touched.

## 6. AWS-R4L-006 / STUDENT-R4-003 (UL-21)

- **AWS-R4L-006:** added a comment after `terraform logout app.terraform.io`: "terraform logout
  only deletes the local copy of the token; it does not revoke it. Revoke the token in HCP
  Terraform under User settings -> Tokens."
  Doc: https://developer.hashicorp.com/terraform/cli/commands/logout
- **STUDENT-R4-003:** `# Uses:` line now documents an optional `$AwsPath` flag. All three
  ElastiCache lines (`delete-cache-cluster`, `wait cache-cluster-deleted`,
  `delete-cache-subnet-group`) are now wrapped in `if ($AwsPath) { ... }`, so an HCP-only student
  who never sets `$AwsPath` skips them cleanly instead of hitting `CacheClusterNotFound`.

## 7. AWS-R3-008 — iteration caps on poll loops

Grepped every `content/labs/*.json` for `do \{`/`while \(` — found exactly 5 files:
`gl-09.json`, `gl-17.json` (x2 loops), `ul-07.json`, `ul-09.json`, `ul-17.json`. All five were
capped at 60 tries, matching the existing sleep interval per lab:

| Lab | Loop | Sleep | Cap added |
|---|---|---|---|
| GL-17 | DROP TABLE wait (step s09 + teardown) | 2s | `$i -lt 60`, `Write-Host` timeout message |
| GL-17 | DROP DATABASE wait (step s09 + teardown) | 2s | `$j -lt 60` (teardown), `Write-Host` timeout message |
| UL-17 | DROP DATABASE ... CASCADE wait | 2s | `$i -lt 60`, `Write-Host` timeout message |
| GL-09 | ASG-gone poll | 15s | `$i -lt 60`, `Write-Host` timeout message |
| UL-09 | ASG-gone poll | 15s | `$i -lt 60`, `Write-Host` timeout message |
| UL-07 | EFS mount-target-gone poll | 10s | `$i -lt 60`, `Write-Host` timeout message |

GL-09's step s13 narrative text was also updated ("poll every 15 seconds, up to 60 tries") to stay
consistent with the capped teardown loop.

Each capped loop keeps the pre-existing exit condition unchanged and ORs in `-and $i -lt 60`, so a
loop that resolves normally still exits immediately (verified in test 3 below); only a loop that
never resolves now stops after 60 tries instead of running forever.

**UL-07 recovery** — added sentence: "If delete-file-system returns FileSystemInUse, wait a minute
and rerun the mount-target poll line." (appended to the existing `recovery` field.)

Doc: https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html ;
https://awscli.amazonaws.com/v2/documentation/api/latest/reference/efs/delete-file-system.html

## 8. STUDENT-R4-004 (GL-17)

**Before:** step s09 body ran `DROP TABLE gl17.sample` / `DROP DATABASE gl17` (no `IF EXISTS`)
while the teardown block ran the `IF EXISTS` form — a wording mismatch a careful student could
question.
**After:** step s09 now matches the teardown exactly: `DROP TABLE IF EXISTS gl17.sample` and
`DROP DATABASE IF EXISTS gl17`.

## Checks run

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `PASS` (`questions 429 aws 310 tf
  119`, `labs 21 + 21`, `lessons 23`).
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → `PASS 42 labs scanned`.
- PS 5.1 AST parse-check (`[System.Management.Automation.Language.Parser]::ParseInput`) over all
  94 non-comment `orderedDeletesPowerShell` lines in the 11 touched labs: 0 errors (one real bug
  was caught and fixed mid-check — the `$Ul02Bucket:` interpolation above — then re-verified clean).
  Also parse-checked the edited inline step commands in GL-17/GL-19/GL-09: the two new/changed
  Athena and `describe-subnets` lines parse clean. (GL-17 step s06's pre-existing, unedited
  `` `n `` line still trips the same regex-splitting artifact noted in the round-4 AWS report; it
  is unrelated to this batch and was not touched.)
- Stubbed-`aws` PowerShell tests (`test_logic.ps1`, no AWS calls):
  - UL-02 tag guard: `ul-02`/`gl-02` → delete; `gl-03`, `'None'`, `$null`, `''` → skip.
  - UL-02 fallback bucket name builds correctly from a stubbed `sts get-caller-identity` and is
    printed via `Write-Host` before any delete.
  - Capped loop with an `aws` stub that always returns `RUNNING`: stops at exactly 60 iterations
    and prints the timeout message (does not loop forever).
  - Capped loop with an `aws` stub that resolves to `SUCCEEDED` on the 3rd call: exits after 3
    iterations, confirming the cap does not change normal (fast) teardown behavior.

## F13: UL-11 Cognito domain

**Problem (STUDENT-R5-001):** the UL-11 teardown's only guidance for a user pool domain was a
comment — "Cognito: if you added a user pool domain, delete it first (aws cognito-idp
delete-user-pool-domain)" — with no actual command. `delete-user-pool` fails while a domain
(default prefix or custom) is still attached to the pool.

**Before:**
```
"# Cognito: if you added a user pool domain, delete it first (aws cognito-idp delete-user-pool-domain)",
"$PoolId = (aws cognito-idp list-user-pools --page-size 60 --query \"UserPools[?Name=='workbook-ul11']\" --output json | ConvertFrom-Json).Id",
"if ($PoolId -and $PoolId -ne 'None') { foreach ($Id in @($PoolId)) { if ($Id) { aws cognito-idp delete-user-pool --user-pool-id $Id } } }",
```

**After:**
```
"# Cognito: a domain (default prefix or custom) must be deleted before delete-user-pool, or the pool delete fails",
"$PoolId = (aws cognito-idp list-user-pools --page-size 60 --query \"UserPools[?Name=='workbook-ul11']\" --output json | ConvertFrom-Json).Id",
"if ($PoolId -and $PoolId -ne 'None') { foreach ($Id in @($PoolId)) { if ($Id) { $Domain = aws cognito-idp describe-user-pool --user-pool-id $Id --query \"UserPool.Domain\" --output text; if ($Domain -and $Domain -ne 'None') { aws cognito-idp delete-user-pool-domain --domain $Domain --user-pool-id $Id }; $CustomDomain = aws cognito-idp describe-user-pool --user-pool-id $Id --query \"UserPool.CustomDomain\" --output text; if ($CustomDomain -and $CustomDomain -ne 'None') { aws cognito-idp delete-user-pool-domain --domain $CustomDomain --user-pool-id $Id }; aws cognito-idp delete-user-pool --user-pool-id $Id } } }",
```

Both `Domain` (the auto-generated Cognito prefix domain) and `CustomDomain` (a user-supplied custom
domain) are looked up and deleted if present, since `describe-user-pool` returns them as separate
fields and either can block `delete-user-pool`. `delete-user-pool-domain` takes `--domain` and
`--user-pool-id` as its only two required parameters, so the same call shape works for both domain
types. Everything stays inside the existing `if ($PoolId -and $PoolId -ne 'None') { foreach ($Id
in @($PoolId)) { if ($Id) { ... } } }` guard, and none of the `aws` lines use `-ErrorAction`.

`stopChargesPanel` updated to say "any Cognito user pool (delete its domain first, default prefix
or custom)" instead of just "any Cognito user pool". `recovery` did not mention the domain and was
left unchanged.

Docs:
- https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/delete-user-pool-domain.html —
  confirms the only required parameters are `--domain` and `--user-pool-id`.
- https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/describe-user-pool.html — confirms
  `UserPool.Domain` (Cognito-hosted prefix) and `UserPool.CustomDomain` (custom domain) are
  separate output fields.

Checks: `content_lint.py` → PASS; `scan_lab_placeholders.py` → `PASS 42 labs scanned`; PS 5.1 AST
parse-check (`[System.Management.Automation.Language.Parser]::ParseInput`) of the full
`orderedDeletesPowerShell` array → 0 errors.

## Not changed

`content_lint.py` and `scan_lab_placeholders.py` required no follow-up fixes. No other lab JSON,
frontend, backend, or script files were touched.
