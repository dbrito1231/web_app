# Teacher verdict: Amendment 1 (N1–N4), pre-implementation

Intended target: `reports/fix-loop-r2/amendment-1/TEACHER.md`. Plan mode blocked writing it, so the content is recorded here for Lead Dev to copy verbatim.

Reviewed at commit `8789bf5`. Read-only. No AWS calls were made.

## Per-item table

| Item | Confirmed? | Evidence (quote) | Fix verdict | Notes |
|---|---|---|---|---|
| N1 GL-08 single-subnet ALB | Yes | s06: `$SubnetPub = aws ec2 create-subnet ... --availability-zone us-east-1a`. s09: `create-load-balancer --name workbook-gl08 --subnets $SubnetPub` | Approve, with additions | AWS: "You must select at least two Availability Zone subnets... Each subnet must be from a different Availability Zone" ([ALB docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html)). Missed items: s06 success line ("public subnet has internet route") must say both subnets. s13 order text should say "…instance, both subnets, VPC stack". Tag the route table too. Add a recovery hint: ALB ENIs can linger after the waiter finishes, so SG, subnet, or IGW deletes may return DependencyViolation. Wait 1–2 min and re-run from that line. |
| N2a GL-01 `$BoundaryArn = $null` | Yes | Teardown line 1 `$BoundaryArn = $null`. Line 7 `aws iam delete-policy --policy-arn $BoundaryArn` | Approve | The `$($AccountId)` syntax is correct. Put the `$AccountId` line first so line 8 (delete-budget) also works after a new shell. It conflicts with scanner rule 1 (see below). |
| N2b 10 UL labs `= $null` | Yes | e.g. ul-06 lines 1–20 `$NatGatewayId = $null` … `$SgId = $null` come before the guarded deletes. The same happens in ul-05/07/08/09/10/11/12/14/16 | **Concerns** | Removing `$null` alone exposes teardowns that are wrong for their scenario (see "Missed" below). The comment text "Unset ones are skipped" is false for ul-05/10/11/12/16, because their lines are unguarded (e.g. ul-16 `aws route53 delete-hosted-zone --id $ZoneId`). For ul-06/08 the comment would list `$AlbArn`, `$AsgName`, `$LaunchTemplateId`, and so on, which is misleading in a NAT lab. |
| N2c GL-06/GL-08 dead lines | Yes | gl-06 lines 11–12 and 14–15 are the same NAT/EIP pair. gl-06 `$AlbArn = $null`, `$AsgName = $null` (the lab never creates these). gl-08 `$EndpointId`/`$NatGatewayId`/…/`$SubnetPriv = $null` | Approve, extend scope | The same dead lines and the duplicate NAT/EIP pair (lines 21–22 = 24–25) exist in **ul-06**, and the dead ALB/ASG/NACL lines exist in ul-06 and ul-08. Apply N2c to those labs too. |
| N3 UL-07 no EFS delete | Yes | teardown only has `$InstanceId`, `$VolumeId`, `$SnapshotId`. stopChargesPanel: "Delete mount targets, EFS, EC2, volumes for ul-07." | Approve, with additions | AWS: "if the file system has any mount targets, you must first delete them" ([CLI ref](https://docs.aws.amazon.com/cli/latest/reference/efs/delete-file-system.html)). The EFS CLI has no waiter, so the plan must spell out the poll loop, e.g. `do { Start-Sleep 10; $n = aws efs describe-mount-targets --file-system-id $FileSystemId --query 'length(MountTargets)' --output text } while ($n -ne '0')`. The amendment says "before the instance and security group", but UL-07 has **no SG delete at all**. Add `$EfsSgId`/`$SgId` deletes after the instance terminates. Add a first comment line: `# First unmount on the instance: sudo umount <mountpoint>` (criterion "unmount before terminating"). Add a verification line: `aws efs describe-file-systems --file-system-id $FileSystemId` returns FileSystemNotFound. The order MT → FS → EC2 → volume → snapshot → SG matches the stopChargesPanel. |
| N4 drill IDs in Start here | Yes | `StartHereTab.tsx:276` `<a href={...}>{id}</a>` (the amendment cites line 224, which is wrong) | Approve (defer with Q1) | Fix the line reference. |
| Scanner hardening | n/a | `scan_lab_placeholders.py:75` `if steps:`, so the unassigned-var check never runs for UL labs (they have no steps). Line 68 whitelists `ErrorAction` | **Concerns** | Rule 1 ("assigned only in steps, never teardown") would fail GL-01's valid lookups (`$Serial = aws iam list-mfa-devices…`, and the new `$AccountId` and `$BoundaryArn`). Change it to: a teardown assignment is allowed only when its right-hand side is an `aws …` lookup or a string built from vars, and it comes before first use. `= $null` stays banned. Add: fail on `aws … -ErrorAction` (see N5). Add: in UL labs, every line that uses a `# Uses` var must be `if (...)`-guarded. |

## Missed issues (new)

- **N5 (High): `-ErrorAction SilentlyContinue` is appended to native `aws` calls.** PowerShell passes it to aws.exe as an argument, and the AWS CLI rejects it as an unknown option. The command fails every time, so these deletes never run. Found 22 times in 14 labs: gl-03, 07, 09, 14, 15, 19, 21 and ul-03, 07, 09, 14, 15, 19, 21. Examples: ul-14 `aws rds delete-db-instance ... --skip-final-snapshot -ErrorAction SilentlyContinue`, ul-07 `aws ec2 delete-volume --volume-id $VolumeId -ErrorAction SilentlyContinue`. This is a cost risk (RDS, ASG). Remove the flag. If you need to suppress errors, use `2>$null`.
- **UL teardowns that don't match their own criteria or stopChargesPanel.** These must be fixed in the same pass, because the `# Uses` header will present them as complete:
  - ul-08: no WAF `disassociate-web-acl` / `delete-web-acl` (needs `--name --scope REGIONAL --id --lock-token`). The stopChargesPanel says "Remove WAF ACL association, delete ACL" (the web ACL bills monthly). It also needs `$SubnetPub2` if the learner follows the fixed GL-08 pattern.
  - ul-05: the criteria require four subnets, but the teardown deletes only `$SubnetPub` and `$SubnetPriv`, so VPC delete will fail.
  - ul-09: no SG delete (criterion: "Teardown removes security groups dedicated to lab"). Also, force-delete runs without waiting before later deletes.
  - ul-10: no DLQ delete and no event-source-mapping delete (the criteria require both, mappings first).
  - ul-14: the restored copy instance and the manual snapshot are never deleted. There is no wait (`aws rds wait db-instance-deleted`) before `delete-db-subnet-group`, so that delete fails. No SG delete.
  - ul-16: records are not deleted before `delete-hosted-zone`, which returns `HostedZoneNotEmpty` ([API ref](https://docs.aws.amazon.com/Route53/latest/APIReference/API_DeleteHostedZone.html)). `delete-vpc` also runs with no subnet/SG cleanup.
  - ul-10/11/12 hard-code guided names (`workbook-gl10`, `workbook-gl11-lambda`, `workbook-gl12-sfn`). Either list these names in the `# Uses` comment as "names you chose", or use variables (`$FunctionName`, `$RoleName`).
- ul-05 verification lists the same tag-search line twice.

## On the `# Uses …` comment approach

It is sound and teachable for unguided labs, but only if:
1. every variable-using line is guarded;
2. the comment lists only resources that the lab's scenario creates;
3. the comment tells learners how to recover a lost ID (a per-lab tag lookup, e.g. `aws ec2 describe-vpcs --filters Name=tag:LabId,Values=ul-06 --query 'Vpcs[].VpcId'`) instead of saying only "set any you named differently".

Recommended wording: `# Uses the IDs you set while building: $A, $B. Check with Get-Variable A,B. Lost one? Find it by tag LabId=ul-NN (see Recovery). Lines whose variable is empty are skipped.`

## Required design changes

1. N1: update the GL-08 s06 success line and the s13 order text. Tag the route table. Add a DependencyViolation retry note to recovery.
2. N2b: guard every line in ul-05/10/11/12/16. Limit each `# Uses` list to the lab's real resources. Add the lost-ID tag lookup to the comment.
3. N2c: extend it to ul-06 (duplicate NAT/EIP pair, dead lines) and ul-08 (dead lines).
4. N3: add the EFS poll loop (no CLI waiter exists), SG deletes, the unmount comment, and the describe-file-systems verification.
5. Add N5: remove `-ErrorAction SilentlyContinue` from all aws calls (14 labs) and add it to the files touched.
6. Add a per-lab criteria-coverage fix for ul-05, 08 (WAF, subnet2), 09, 10, 14, 16, or log it as its own CR (High for ul-08/14) and do not claim N2b closes the cost risk.
7. Scanner: allow lookup assignments in teardown (they must not be `$null`), run the check for UL labs, fail on `-ErrorAction` in aws lines, and require guards in UL teardowns.
8. N4: fix the line reference to `StartHereTab.tsx:276`.

Overall: concerns
