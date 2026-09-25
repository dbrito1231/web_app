# Teacher verdict: Amendment 1 revised, post-implementation (round 3)

Saved by Lead Dev, word for word from the Teacher's reply. The Teacher does not write files (AGENTS.md).

Reviewed commits `4cba746`, `8955543`, `081541d` (diff `bbb05de..081541d -- content/labs`). Read-only; no AWS calls.

## Checks run

| Check | Result |
|---|---|
| `backend\.venv\Scripts\python.exe scripts\content_lint.py` | `questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23 / PASS` (the uncommitted Q1 question edits in the working tree were included in the lint) |
| `scripts\scan_lab_placeholders.py` | `PASS 42 labs scanned` |
| `= $null` in any lab | 0 |
| `-ErrorAction` in labs | only on `Remove-Item` cmdlets (gl-03, ul-03, ul-21), never on `aws` |
| Objective IDs / `pairId` / `labId` | unchanged |
| `# Lost an ID?` line | present in all 21 UL labs |

## Earlier required changes

| Item | Status |
|---|---|
| UL deletes guarded | Done. Every line that uses a variable is `if (...)`-guarded. Labs marked `# Uses: none` use fixed names or guarded lookups. |
| `# Uses` lists only real resources | Done. The ul-06 and ul-08 lists no longer carry dead ALB, ASG or NACL variables. |
| Lost-ID hint | Done. It uses the `resourcegroupstaggingapi` form. |
| UL teardowns match criteria | Done for ul-05 (4 subnets, 2 NACL associations), ul-08 (WAF, `$SubnetPub2`), ul-09 (SG, waits), ul-10 (event source mappings, DLQ), ul-14 (copy, snapshot, waits, SG), ul-16 (records deleted before the zone). |
| GL-08 s06/s13 text | Done. s06: "both public subnets (us-east-1a and us-east-1b) are associated…"; s13: "ALB (wait until deleted; its listener goes with it), target group, instance (wait until terminated), both route-table associations, route table, both subnets, internet gateway, security group, VPC". A DependencyViolation note was added to recovery. |
| UL-07 unmount note | Done. `# First unmount on the instance: sudo umount <mountpoint>`, plus the poll loop, both SGs and a `describe-file-systems` check. |
| N5/N6 `-ErrorAction` | Done. |

## Per-lab verdicts

| Lab | Verdict | Notes |
|---|---|---|
| GL-01 | approve | `$AccountId` lookup comes first; `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"` |
| GL-06 | approve | Dead lines and the duplicate NAT/EIP pair are removed; the teardown matches the steps |
| GL-07 | approve | Detach → `wait volume-available` → delete. Nit R3-013: "NotFound or IncorrectState … already gone" (IncorrectState on detach means the volume is already detached, not gone) |
| GL-08 | approve | Second subnet, tagged RT/TG/subnets, `target-in-service` wait, `curl.exe`. Steps, s13, panel, teardown and recovery all agree |
| GL-09 | approve | ASG poll loop is explained in s13 ("The AWS CLI has no Auto Scaling waiter") |
| GL-10 | approve | The unsubscribe loop is replaced by "delete-topic also deletes its SNS subscriptions"; s13 and the panel agree |
| GL-11 | approve | `$($AccountId):$($ApiId)` fix with a short explanation; `curl.exe` |
| GL-14 | approve | Teardown re-sets `$DbId`/`$SubnetGroup` to the s06 values (`workbookgl14`, `workbook-gl14`) and waits before the subnet-group delete |
| GL-15 | approve | Flag removed |
| GL-16 | approve | DELETE change batch in s10 and in the teardown; s13 explains the InvalidChangeBatch case |
| GL-19 | approve | Flag removed |
| GL-21 | approve | `cache-cluster-deleted` wait added; panel and s13 agree |
| UL-01 | **concerns** | R3-002: the teardown runs `delete-role-policy … --policy-name ul01-daily` / `ul01-bg`, but no criterion names these policies. If the learner chose other names, `delete-role` fails with DeleteConflict |
| UL-02 | **concerns** | R3-003: the comment says "if you reused your GL-02 bucket, set $Bucket to that name instead", but the next line `$Bucket = "workbook-ul02-…"` overwrites it. The name `workbook-ul02-<account-id>` also appears in no criterion |
| UL-03 | approve | New C1 is clear. GuardDuty skip note is good. Nits: C9 repeats C1 (R3-011); the inline-policy loop could be one `delete-role-policy … ul03-read` line |
| UL-04 | approve | Order matches C12; the PendingDeletion caveat in verification is good |
| UL-05 | approve | All 4 subnets, both NACL associations, default-NACL lookup; the duplicate verification line is removed |
| UL-06 | approve | Uses list is limited to real NAT/VPC variables |
| UL-07 | approve | MT → poll → FS → EC2 → MT SG → instance SG matches the panel and C5/C7/C8 |
| UL-08 | approve | WAF disassociate/delete with lock token; order matches C12. Nit R3-012: recovery says "rerun that line" (GL-08 says "from that line") and uses "1-2" instead of "1–2" |
| UL-09 | approve | Captures instance IDs, waits, polls, then deletes the alarm, LT and SG |
| UL-10 | approve | Order matches C11–C14. Teachability is borderline: 16 lines, 3 `foreach` loops, JMESPath `ends_with`. Acceptable |
| UL-11 | **concerns** | R3-004: C10 "Teardown deletes authorizer before routes" contradicts the teardown's `# delete-api removes the API's authorizers, routes, integrations and stages together` |
| UL-12 | concerns (low) | R3-009: teardown looks up `/aws/vendedlogs/states/workbook-ul12`, but C1 doesn't name the log group. The five `foreach` loops are heavy |
| UL-13 | approve | Simple and clear; the gl-13 references are gone |
| UL-14 | approve | Copy → source (waits) → snapshot → subnet group → SG matches C5/C7/C12 |
| UL-15 | **concerns** | R3-001: C2 and C3 are identical: "CloudWatch log group `/workbook/ul15` (or the UL-10 Lambda log group) has retention set to 1 day." The old C3 ("CloudTrail portion matches GL-15 minimal trail.") was lost |
| UL-16 | concerns (low) | R3-006: the record delete is one line that builds JSON with `ConvertFrom-Json`/`ConvertTo-Json -Depth 10`, a hashtable and a wait, which is hard for a student to follow. R3-007: `delete-vpc` has no note to delete any subnets first |
| UL-17 | approve | `DROP DATABASE … CASCADE` with a state loop, which is explained in a comment; `workbook_ul17` underscore is correct |
| UL-18 | approve | Services → tasks → task definitions → cluster; the recovery hints are good. The loops are long but commented |
| UL-19 | concerns (low) | R3-005: C1 says "in the default VPC use the node group path", but C3 and the scenario still offer "Fargate profile OR node group". R3-008: the IAM role cleanup is one line of nested `foreach` loops |
| UL-20 | approve | Nit R3-015: the teardown's `head-bucket` is a check, not a delete, so it belongs in verification. The `Values=gl-20` verification needs a short "why" |
| UL-21 | concerns (low) | R3-010: `# terraform logout removes the token…` is only a comment, but the panel says "remove local terraform tokens" |

## Teachability of the new naming criterion (UL-03, 04, 10, 11, 12, 13, 15, 17, 18, 19, 21)

- **Clear?** Yes. Every one uses the same pattern: "Name the resources you create `workbook-ulNN`: …".
- **Spoils the challenge?** No. It lists names only, except UL-19 C1, which adds a design hint (R3-005).
- **Too many criteria?** Most labs now have 16. Each C1 overlaps with an older tag criterion; merging them brings each lab back to 15 (R3-011).
- **Readable teardowns?** Mostly. UL-16 and UL-19 are the exceptions; UL-10 and UL-12 are at the limit.

## New issues

| ID | Sev | Lab | Problem | Suggested fix |
|---|---|---|---|---|
| TEACHER-R3-001 | Medium | UL-15 | C2 and C3 are identical; the CloudTrail criterion was lost | Restore C3 as a trail criterion, e.g. "Trail `workbook-ul15` logs management events to the ul-15 bucket". Add a duplicate-criterion check to `content_lint.py` |
| TEACHER-R3-002 | Medium | UL-01 | Teardown hard-codes inline policy names `ul01-daily` and `ul01-bg`, which no criterion states | Name them in C1/C3, or use the `list-role-policies` loop as UL-03 does |
| TEACHER-R3-003 | Medium | UL-02 | The `# Uses` comment says "set $Bucket", then the next line overwrites it; the bucket name is in no criterion | Add a naming criterion for `workbook-ul02-<account-id>`; change the comment to "if you reused your GL-02 bucket, edit the next line" |
| TEACHER-R3-004 | Low | UL-11 | C10 "authorizer before routes" contradicts the delete-api teardown | Reword C10: "Teardown deletes the API (this removes its authorizer, routes, integrations and stages)" |
| TEACHER-R3-005 | Low | UL-19 | C1 includes a design hint that removes the Fargate/node-group choice in C3 and the scenario | Move the private-subnet fact to a hint, or reword C3 and the scenario to "node group (default VPC)" |
| TEACHER-R3-006 | Low | UL-16 | Record-delete one-liner builds JSON and is hard to follow | Split it into 3–4 commented lines, or tell learners to write DELETE batches for their two records as GL-16 does |
| TEACHER-R3-007 | Low | UL-16 | `delete-vpc` has no note about subnets or SGs | Add a comment: "delete any subnets you added first" |
| TEACHER-R3-008 | Low | UL-19 | IAM cleanup is one nested-loop line | One block per role, or three commented lines |
| TEACHER-R3-009 | Low | UL-12 | Teardown's log group name is not in C1 | Add `/aws/vendedlogs/states/workbook-ul12` to C1 |
| TEACHER-R3-010 | Low | UL-21 | `terraform logout` appears only as a comment | Make it a command line |
| TEACHER-R3-011 | Low | UL-03, 04, 10, 13, 15, 17, 18, 19, 21 | The new C1 "Tag each one LabId=ul-NN" repeats an older tag criterion | Remove or merge the older criterion |
| TEACHER-R3-012 | Low | UL-08 | Recovery says "rerun that line" and uses "1-2"; GL-08 says "rerun Stop charges from that line" and uses "1–2" | Use the GL-08 wording |
| TEACHER-R3-013 | Low | GL-07 | s13 says IncorrectState means "already gone" | "NotFound means already gone; IncorrectState on detach means already detached" |
| TEACHER-R3-014 | Low | UL labs with `# Uses: none` | "Lost an ID?" fits badly when no IDs are used | Use "Lost track? List what is left:" in those labs |
| TEACHER-R3-015 | Low | UL-20 | `head-bucket` check sits in the teardown; the `gl-20` tag check has no explanation | Move the check to verification and add "(if you imported the GL-20 bucket)" |

Overall: concerns
