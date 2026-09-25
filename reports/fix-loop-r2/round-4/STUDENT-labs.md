# Student review — round 4, labs

Reviewer: College IT Student persona (read-only). Opened each lab card on the Labs tab at
`http://127.0.0.1:5173/labs?lab=<id>` and read Steps / Acceptance criteria, Hints, Stop charges,
and the PowerShell teardown block top to bottom, as a student preparing to run it by hand.
Cross-checked the rendered card against the source JSON in `content/labs/*.json`. No files
edited, no server started beyond the already-running dev server, no Reset/Import/Check answers
clicked.

## STUDENT-R3-004 follow-up — confirmed fixed

UL-07 and UL-08 now both open with an explicit naming criterion as acceptance-criterion #1:
- UL-07: "Name the resources you create `workbook-ul07`: file system tagged Name=workbook-ul07,
  EC2 instance tagged Name=workbook-ul07, mount-target security group `workbook-ul07-mt-sg`, and
  instance security group `workbook-ul07-sg`."
- UL-08: "Name the resources you create `workbook-ul08`: ALB `workbook-ul08`, target group
  `workbook-ul08-tg`, VPC `workbook-ul08`, security group `workbook-ul08-sg`, and WAF web ACL
  `workbook-ul08`."

Both teardown blocks still use `if ($Var) { ... }` guards keyed off remembered session variables,
but the naming criterion now gives a fixed fallback (matching UL-10/UL-19's pattern), and both
"Lost an ID?" comments point at `workbook-ul07*` / `workbook-ul08*` name search plus the tag
search. **STUDENT-R3-004 is resolved.**

## Per-lab table

| Lab | Followable top-to-bottom? | Criteria names match cleanup? | Multi-line blocks readable? | Contradictions? | Where a student would get stuck |
| --- | --- | --- | --- | --- | --- |
| GL-14 (RDS single-AZ) | Yes | Yes — `$SubnetGroup='workbook-gl14'`, `$DbId='workbookgl14'` used consistently in steps and teardown | N/A (linear list) | None | None found |
| GL-17 (Athena) | Yes | Yes — `$Bucket`/`$ResultsBucket` built the same way in steps and teardown | Yes — the drop-table/drop-database `do { ... } while (...)` wait loops read as one PowerShell statement per line, same shape as the guided steps | Minor: step s09 body says `DROP TABLE gl17.sample` (no `IF EXISTS`) while the teardown block uses `DROP TABLE IF EXISTS gl17.sample` — a small inconsistency in wording, not a blocker since `IF EXISTS` is strictly safer | None blocking |
| GL-19 (EKS control plane) | Yes | Yes — `workbook-gl19` cluster/role names match | N/A (short block) | None | None found |
| UL-01 (Identity/budget) | Yes | Yes — `workbook-ul01-daily` / `-breakglass` match | Yes — the `foreach ($P in (...)) { if (...) { ... } }` inline-policy cleanup reads fine as one line per role | None | None found |
| UL-02 (Private S3) | Yes | Yes — `$Bucket` fallback name `workbook-ul02-<account-id>` matches criterion #1 | Yes — version/delete-marker `foreach` loops are readable | None | Minor: student who reused their GL-02 bucket must remember to set `$Bucket` themselves before running Stop charges, or the script falls back to a name they never created — this is called out in the `# Uses:` comment, so it's a genuine "read the comment first" case rather than a bug |
| UL-07 (EC2/EBS/EFS) | Yes | Yes, see above | Yes — `if ($FileSystemId) { ... }`, `do {...} while` mount-target-drain loop read cleanly one line at a time | None | None found |
| UL-08 (ALB + WAF) | Yes | Yes, see above | Yes — long `if ($X) { ... }` chain, one resource per line, in the order stated in "Teardown order documented" | None | The teardown's own recovery text warns that ENIs can linger and a subnet/IGW/SG delete can return `DependencyViolation` — the fix (wait 1–2 min, rerun from that line) is written right there, so this is a documented hazard, not a silent gap |
| UL-15 (CloudWatch/CloudTrail) | Yes | Yes — trail/bucket/log-group/role names all `workbook-ul15*` | Yes | None | None found — the CloudTrail delete-trail criterion (flagged missing in an earlier round) is present in both the acceptance criteria and the teardown block |
| UL-16 (Private DNS) | Mostly, with one gap | **No** — see "New issues" below: no naming criterion for the hosted zone/VPC, and the only VPC-cleanup instruction is a comment, not a command | Change-batch build (`$Rrs` → `$Changes` → write JSON → submit → wait) reads step by step and is easy to follow | See new issue below | A student who created their own VPC for this lab (not the default VPC) has no PowerShell line that deletes the subnets/security groups they added — only a comment telling them to do it "before delete-vpc" |
| UL-19 (EKS + node group/Fargate) | Yes | Yes — cluster/role/node-group/Fargate-profile names all `workbook-ul19*` | Yes — despite being the longest teardown block in the set (3 IAM roles cleaned in sequence), each role's detach/delete-policy/delete-role trio is on its own lines and the `$EksRole =` / `$NodeRole =` / `$FargateRole =` existence checks make it clear roles you didn't create are skipped | None | None found — this is the most complex teardown reviewed and it stayed readable |
| UL-21 (ElastiCache/HCP) | Mostly, with one gap | Yes — `workbook-ul21` cache cluster/subnet group names match | Yes (short block) | See new issue below | A student who stayed HCP-only (never touched AWS) is told by a comment to "skip if you stayed on HCP," but the two `aws elasticache delete-cache-cluster` / `describe-cache-subnet-groups` lines have no `if` guard around them — the general "run every Stop charges command yourself in order" instruction would have them run a delete against a cluster ID that was never created |

## New issues (Low+)

| ID | Severity | Issue |
| --- | --- | --- |
| STUDENT-R4-001 | Low | UL-16 is missing the "Name the resources you create `workbook-ulNN`" acceptance criterion that UL-01/02/07/08/15/19/21 all now have. Criterion #6 only says "LabId=ul-16 tags where supported" — there is no fixed-name pattern for the hosted zone or the optional VPC, so a student has nothing to fall back on if they lose `$ZoneId`/`$VpcId` (Route 53 zones and ad-hoc VPCs aren't as easy to rediscover by name as an EC2/IAM resource would be). Recommend adding the same naming-criterion sentence used in the sibling unguided labs. |
| STUDENT-R4-002 | Low | UL-16's teardown block has a comment — "Delete any subnets and security groups you added to $VpcId before delete-vpc" — with no actual PowerShell command backing it. Every other conditional step in this lab (and in UL-07/UL-08/UL-19) is a real `if ($Var) { aws ... }` line; here it's advice only. A student who built their own VPC for this lab (rather than reusing the default) has no scripted way to find and delete their subnets/SGs before `delete-vpc`, and `delete-vpc` will fail with `DependencyViolation` until they do it by hand and by memory. |
| STUDENT-R4-003 | Low | UL-21's teardown runs `aws elasticache delete-cache-cluster --cache-cluster-id workbook-ul21` and `aws elasticache delete-cache-subnet-group --cache-subnet-group-name workbook-ul21` unconditionally, even though the preceding comment says "AWS path only (skip if you stayed on HCP)." Every other lab in this batch that has an optional path (UL-02's Macie, UL-07/08/16/19's `if ($Var)` guards) wraps the optional AWS calls in a check; UL-21 does not, so a student who only did the Terraform/HCP half and follows the literal "run every Stop charges command in order" instruction will hit an avoidable `CacheClusterNotFound` error. Not destructive, but inconsistent with how every other lab in this round handles an optional branch. |
| STUDENT-R4-004 | Low (cosmetic, not blocking) | GL-17 step s09's body text runs `DROP TABLE gl17.sample` (no `IF EXISTS`), while the Stop charges teardown block for the same lab runs `DROP TABLE IF EXISTS gl17.sample` / `DROP DATABASE IF EXISTS gl17`. Both are safe and the teardown's guarded version is arguably the better one, but the step text and the teardown text disagree on whether `IF EXISTS` belongs there, which could make a careful student wonder if they typed the guided step wrong. |

No blocking or High-severity issues found. GL-14, GL-17, GL-19, UL-01, UL-02, UL-07, UL-08,
UL-15, and UL-19 were all followable top to bottom with names that stay consistent from
acceptance criteria through Stop charges through the PowerShell teardown block, and the new
multi-line blocks (UL-19's role loop, GL-17's Athena drop/wait loops) read cleanly one line at a
time. UL-16 and UL-21 are the two labs in this batch with a real (if minor) gap between what the
lab tells the student to do and what the script actually does for them.
