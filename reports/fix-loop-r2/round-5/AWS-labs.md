# Fix-loop r2, round 5 (labs): AWS Architect re-check of commit a4681e0 (F10)

Reviewer: Senior AWS SA (read-only). No AWS calls, no servers started. Files read: the 11 changed
lab JSONs, `reports/fix-loop-r2/round-4/AWS-labs.md`, `reports/fix-loop-r2/round-4/STUDENT-labs.md`,
`reports/fix-loop-r2/amendment-2/impl-F10.md`, and `git show a4681e0` / `git diff a4681e0~1 a4681e0`.
Only this report file was written.

## Local checks (no state changed, scratchpad only)

- **Parser:** Windows PowerShell 5.1.26100 `[Parser]::ParseInput` over all 94 non-comment
  `orderedDeletesPowerShell` lines in the 11 touched labs (gl-09, gl-17, gl-19, ul-02, ul-07,
  ul-09, ul-11, ul-16, ul-17, ul-19, ul-21). **0 parse errors.**
- **`content_lint.py`:** `PASS` (`questions 429 aws 310 tf 119`, `labs 21 + 21`, `lessons 23`) —
  same result claimed in impl-F10.md.
- **Stubbed-`aws` PowerShell logic tests** (fake `aws`/native functions, no real AWS calls):
  - UL-02 `get-bucket-tagging` on an untagged bucket → simulated stderr `NoSuchTagSet` + empty
    stdout → `$Ul02BucketLabId` is `$null` → every guarded delete line evaluates false and prints
    `Skipping <bucket>: LabId tag is not ul-02 or gl-02`. **The gate skips safely.**
  - UL-11 `foreach ($Id in @($ApiId))`: 2-element array → both ids visited; single string → 1 id;
    `$null`/`'None'` → outer guard blocks entry, nothing deleted.
  - Capped loop with a stub that always returns `RUNNING` → stops at exactly `$i = 60` and prints
    the timeout message. Capped loop with a stub that resolves on the 3rd call → exits at `i = 3`
    (cap does not change normal-speed teardown).
  - UL-16 `SecurityGroups[?GroupName!='default']` query filter, applied to a 3-item fake set,
    excludes `default` and keeps only the two learner-created groups.
  - `$NotDefaultVpc` truth table: `IsDefault='True'`→`False` (skip), `'False'`→`True` (act),
    `$null` (failed describe)→`False` (fails closed, skip).
  - UL-21 `if ($AwsPath)`: unset → skipped; `$true` → runs.
  - `-split '\s+' | Where-Object { $_ }` piped into a fake native-arg echo: a 4-subnet tab-joined
    string becomes 4 separate array elements, and PS 5.1 splats them as 4 separate native
    arguments (not one joined string).
- **WebFetch verification against AWS docs:**
  - `ec2 describe-subnets --filters` accepts `availability-zone-id` as a documented filter name
    (distinct from `availability-zone`), confirming the GL-19/UL-19 fix's filter key is real.
  - EKS "View Amazon EKS networking requirements" page's own table of "Disallowed Availability
    Zone IDs" lists `use1-az3` for `us-east-1` — confirming the fix's premise is accurate, not just
    plausible.
  - `cognito-idp list-user-pools` synopsis lists `--starting-token`, `--page-size`, `--max-items`
    only; `--max-results` is not a valid parameter — confirming AWS-R4L-002's fix.

## Verdict table

| ID | Lab | Verdict | Evidence (current content) | Doc URL |
|---|---|---|---|---|
| AWS-R4L-001 | UL-02 | **Gone** | Renamed to `$Ul02Bucket` (no longer shared with GL-02/03/04/15/17/20 or UL-03/04/15/17's `$Bucket`). Every delete line (`delete-bucket-policy`, `list-object-versions`, both version/marker `foreach` loops, `delete-bucket-lifecycle`, `delete-bucket`) is individually gated on `$Ul02BucketLabId -eq 'ul-02' -or $Ul02BucketLabId -eq 'gl-02'`, read fresh via `get-bucket-tagging` on the resolved bucket. Tested: a bucket with no LabId tag, or the wrong LabId tag, or a `NoSuchTagSet` error, all fail closed (skip) rather than deleting | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/get-bucket-tagging.html |
| AWS-R4L-002 | UL-11 | **Gone** | `list-user-pools --page-size 60` replaces the invalid `--max-results 60`; `--page-size` is a documented pagination parameter | https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/list-user-pools.html |
| AWS-R4L-003 | UL-11 | **Gone** | `$ApiId`/`$PoolId` deletes both wrapped in `foreach ($Id in @($ApiId)) { if ($Id) { aws … --api-id $Id } }` (and the Cognito equivalent). Tested: a 2-element array deletes both ids; a single string still deletes the one id; `$null`/`'None'` deletes nothing | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/apigatewayv2/delete-api.html |
| AWS-R4L-004 / AWS-R3-003 | GL-19, UL-19 | **Gone** | GL-19 s07 now filters `Name=availability-zone-id,Values=use1-az1,use1-az2,use1-az4,use1-az6` (confirmed `availability-zone-id` is a valid EC2 filter, and `use1-az3` is EKS's documented disallowed AZ ID for us-east-1). UL-19 hint 1 now points learners at the same `availability-zone-id` approach | https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-subnets.html |
| AWS-R4L-005 | UL-16 | **Gone** | `route53 wait resource-record-sets-changed --id $ChangeId` guarded by `if ($ZoneId -and $Rrs -and $ChangeId)` — a failed `change-resource-record-sets` (null `$ChangeId`) now skips the wait instead of erroring "expected one argument" | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/route53/wait/resource-record-sets-changed.html |
| AWS-R4L-006 | UL-21 | **Gone** | Comment added after `terraform logout app.terraform.io`: "terraform logout only deletes the local copy of the token; it does not revoke it. Revoke the token in HCP Terraform under User settings -> Tokens." | https://developer.hashicorp.com/terraform/cli/commands/logout |
| AWS-R3-003 | GL-19 / UL-19 | **Gone** (folded into AWS-R4L-004 above; the R3 fix that caused this was itself corrected) | Same evidence as AWS-R4L-004 | https://docs.aws.amazon.com/eks/latest/userguide/network-reqs.html |
| AWS-R3-008 | GL-09, GL-17 (x2), UL-07, UL-09, UL-17 | **Gone** | All five uncapped `do { … } while (…)` loops in the whole `content/labs/*.json` set now carry `$i`/`$j` counters and `-and $i -lt 60` (or `$j -lt 60`), plus a `Write-Host` timeout message on cap-out. Tested: a stub that never resolves stops at exactly 60 tries; a stub that resolves early exits immediately (cap is inert on the happy path). UL-07's `recovery` field also gained the missing "if delete-file-system returns FileSystemInUse, wait a minute and rerun the mount-target poll line" sentence | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/efs/delete-file-system.html |
| STUDENT-R4-001 | UL-16 | **Gone** | New acceptance criterion #1: "Name the resources you create `workbook-ul16`: private hosted zone `workbook-ul16` and, if you create one, VPC `workbook-ul16`. Tag each one LabId=ul-16." | — |
| STUDENT-R4-002 | UL-16 | **Gone** | The advice-only comment is now backed by two real, guarded commands — `describe-subnets`/`delete-subnet` and `describe-security-groups`/`delete-security-group` — both inside the pre-existing `$NotDefaultVpc` guard, placed after the hosted-zone delete and before `delete-vpc` | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-subnets.html |
| STUDENT-R4-003 | UL-21 | **Gone** | All three ElastiCache lines wrapped in `if ($AwsPath) { … }`; an HCP-only learner who never sets `$AwsPath` now skips them instead of hitting `CacheClusterNotFound` | — |
| STUDENT-R4-004 | GL-17 | **Gone** | Step s09 now runs `DROP TABLE IF EXISTS gl17.sample` / `DROP DATABASE IF EXISTS gl17`, matching the teardown block's wording exactly | — |

## Focused checks from the assignment

- **UL-02 `get-bucket-tagging` / LabId gate:** confirmed by test — a bucket with no tags at all
  produces AWS CLI's `NoSuchTagSet` error on stderr with empty stdout, which assigns `$null` to
  `$Ul02BucketLabId` in PowerShell 5.1's native-command capture. `$null -eq 'ul-02'` is false, so
  every one of the six guarded delete lines is skipped and the `else` branch prints the skip
  message — no partial delete, no error propagation into the next line. The one interpolation bug
  the implementer caught mid-check (`"$Ul02Bucket:"` parsed as a drive/scope reference) was fixed
  with `${Ul02Bucket}:` and re-verified to parse clean. I also checked the lab's own acceptance
  criteria ("All creatable resources carry Workbook, LabId=ul-02… tags where the API supports
  tags") — a bucket built by following this lab's own instructions will carry the LabId tag, so
  the new gate does not block a correctly-completed lab's own teardown; it only blocks stale/wrong
  buckets, which is the intended fix.
- **UL-11 `foreach` deletes:** tested with 0/1/2-element inputs; the loop degrades correctly in
  every case and never receives a raw multi-element array as a single `--api-id`/`--user-pool-id`
  argument (which is what caused AWS-R4L-003 originally).
- **GL-19/UL-19 `availability-zone-id` filter:** syntax is valid (`Name=availability-zone-id,Values=…`
  is one `--filters` clause with a comma-joined value list, same shape as the pre-existing
  `availability-zone` filter it replaced), and WebFetch against the current AWS CLI and EKS docs
  confirms both the filter name and the underlying `use1-az3` restriction are real, not invented.
- **Capped loops (60 tries):** all five pre-existing uncapped loops in the whole lab set are now
  capped, each keeping its original exit condition ORed with the new `$i -lt 60`/`$j -lt 60`, so
  normal (fast-resolving) teardown behavior is unchanged and only a genuinely stuck resource now
  stops the script with a console message instead of hanging forever.
- **UL-16 VPC/SG blast radius:** the new subnet and security-group deletes sit inside the
  pre-existing `$NotDefaultVpc` guard (itself fails closed to `False` if the `describe-vpcs` call
  errors), so the default VPC can never reach these lines. The security-group delete's `--query`
  additionally excludes `GroupName!='default'`, so even inside a non-default VPC the account's
  default security group for that VPC is never targeted. Both new loops only ever touch resources
  inside `$VpcId`, which is a VPC this lab's own instructions have the learner create.
- **UL-21 `$AwsPath` guards:** all three ElastiCache lines are individually wrapped; an HCP-only
  learner's teardown run is now a no-op for the AWS half, and an AWS-path learner who sets
  `$AwsPath = $true` still gets the original delete-cluster → wait → delete-subnet-group order.

## Cleanup order and blast radius (all 11 files)

Order is unchanged and correct everywhere the diff touched: UL-16 is records → wait → hosted zone
→ subnets → security groups → VPC (new lines inserted between the zone delete and the VPC delete,
which is the right slot); UL-02's guard sits in front of every S3 delete without reordering them;
UL-11's `foreach` wrapping and UL-21's `if ($AwsPath)` wrapping are drop-in replacements around
existing single lines, so the surrounding sequence (function → log group, cluster → subnet group,
etc.) is untouched. I found nothing in this batch that can delete a resource outside its own lab —
the one prior regression (AWS-R4L-001, UL-02's shared `$Bucket`) is fixed, and no new
shared/ambiguous variable was introduced (`$Ul02Bucket`, `$AwsPath`, `$i`/`$j` loop counters are all
lab-local and reset at the top of their own guarded block).

## New issues

None found at Low severity or higher. Two cosmetic notes, not filed as issues:

1. UL-21's `# Uses:` comment line has a mangled character (`—` em dash rendered as `�` in a
   plain-text terminal) in both the before and after JSON — pre-existing encoding artifact from
   Windows console code page, not something this batch introduced or worsened, and it does not
   affect JSON validity (`content_lint.py` passes) or PowerShell parsing.
2. UL-02's new `Write-Host "Deleting bucket: $Ul02Bucket"` line runs before the tag check, so a
   learner running line-by-line sees the target bucket name printed even in cases where every
   later line will end up skipped by the tag gate — this is a UX quirk in a read-only reviewer's
   opinion, not a safety or correctness defect.

## Overall

**Pass — all 13 tracked items (AWS-R4L-001 to 006, AWS-R3-003, AWS-R3-008, STUDENT-R4-001 to 004)
are Gone**, each confirmed with a parse-check, a stubbed-logic test, or a live doc lookup rather
than just re-reading the diff. All 94 non-comment teardown lines across the 11 touched labs parse
clean under the PowerShell 5.1 AST parser, `content_lint.py` passes, and the UL-02 tag gate, the
UL-16 default-VPC/default-SG protections, and the capped poll loops all behave safely under
adversarial stub inputs (no tags, failed describes, never-resolving polls, multi-match lookups). No
new problem was found.
