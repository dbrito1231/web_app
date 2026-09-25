# Amendment 1, revised: implementation batch B (UL-05, 06, 07, 08, 09, 14, 16)

Lead Dev, 2026-09-26. Files edited: `content/labs/ul-{05,06,07,08,09,14,16}.json` only. No AWS calls, no git.
Edited with `backend\.venv\Scripts\python.exe` (json.load, then `json.dumps(indent=2, ensure_ascii=True) + "\n"`, text mode, UTF-8, CRLF kept). The diff against the originals shows only the fields listed below.

Common to all seven labs:
- **N2b:** every `$X = $null` line removed. Lines 1 and 2 are now `# Uses: … (the IDs you set while building; unset ones are skipped)` and `# Lost an ID? aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=ul-NN`. Every delete is now `if ($Var …) { … }`, and the condition names every variable the line uses. Lookup lines (`$DefaultNaclId`, `$MtIds`, `$AsgInstanceIds`, `$LockToken`, `$Rrs`/`$ChangeId`) are also guarded.
- **Verification:** the `gl-NN` tag search is replaced by `ul-NN`-specific describe checks.
- **stopChargesPanel:** rewritten so it names the teardown order.
- **N6:** no `-ErrorAction` is left on any `aws` line.
- **N7:** none of these seven labs used `workbook-glNN` names, so no naming criterion was needed.

Checks run:
- `scripts\content_lint.py` PASS.
- Every teardown line parsed with the PowerShell 5.1 parser (`[Parser]::ParseInput`): 0 errors.
- A script asserted that no line contains `= $null`, `ErrorAction` or `workbook-gl`, that every non-comment line starts with `if (`, and that no verification line mentions `gl-`.

## UL-05 (T1, N2b)
- **Before:** 13 `$null` lines, then 13 unguarded deletes. They covered only `$SubnetPub`/`$SubnetPriv`, one private route-table association and one NACL association, so `delete-vpc` failed on the 2 leftover subnets. Verification listed the tag search twice.
- **After:** `# Uses` lists 17 vars (4 subnets, 4 RT associations, 2 NACL associations, endpoint, custom NACL, both RTs, IGW, SG, VPC). Order: endpoint → default NACL looked up (`describe-network-acls --filters Name=vpc-id,Values=$VpcId Name=default,Values=true`) → 2× `replace-network-acl-association` → delete custom NACL → 4× disassociate → 2× delete RT → 4× delete subnet → IGW detach and delete → SG → VPC.
- **Verification:** tag search, `describe-vpcs` NotFound, `describe-nat-gateways --filter Name=vpc-id,…` empty.
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-subnet.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-route-table.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/replace-network-acl-association.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-nat-gateways.html (option is `--filter`, singular, verified)

## UL-06 (N2b, N2c)
- **Before:** 20 `$null` lines. The NAT delete/wait and EIP release pair appeared twice. There were dead lines for endpoint, ALB, TG, ASG, LT, instance, NACL and SG, which the criteria never create.
- **After:** `# Uses` lists `$VpcId, $SubnetPub, $SubnetPriv, $IgwId, $PublicRouteTableId, $PrivateRouteTableId, $RtAssocPub, $RtAssocPriv, $AllocationId, $NatGatewayId`. Order: NAT delete, then `wait nat-gateway-deleted` → release EIP → 2× disassociate → 2× delete RT → 2× delete subnet → IGW → VPC.
- **Verification:** tag search, NAT State deleted, `describe-addresses` NotFound, VPC NotFound.
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-nat-gateway.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/release-address.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/detach-internet-gateway.html

## UL-07 (N3, N6)
- **Before:** it handled only the instance, `$VolumeId` (with `-ErrorAction`, so it never ran) and `$SnapshotId`. There was no EFS and no SG cleanup.
- **After:** `# Uses: $FileSystemId, $InstanceId, $MountTargetSgId, $InstanceSgId`. Line 3 is `# First unmount on the instance: sudo umount <mountpoint>`. The mount targets are deleted with the AWS report's commands (`MountTargets[].[MountTargetId]` one per line, then a foreach loop). A poll loop on `length(MountTargets)` waits until 0, then `delete-file-system` runs → terminate and `wait instance-terminated` → mount-target SG → instance SG. The volume and snapshot lines were dropped because the criteria create neither, and the root EBS volume is deleted when the instance terminates.
- **Verification:** tag search, `aws efs describe-file-systems --file-system-id $FileSystemId` returns FileSystemNotFound, instance terminated.
- **Deviation from the AWS report:** the poll condition is `while ($MtLeft -and $MtLeft -ne '0')` instead of `while ($MtLeft -ne '0')`. Without this, the loop never ends if `describe-mount-targets` errors (empty output).
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/efs/delete-mount-target.html ; https://docs.aws.amazon.com/cli/latest/reference/efs/delete-file-system.html ; https://docs.aws.amazon.com/cli/latest/reference/efs/describe-mount-targets.html ; https://docs.aws.amazon.com/efs/latest/ug/wt1-getting-started.html#wt1-clean-up

## UL-08 (N1, N2b, N2c, T1)
- **Before:** 20 `$null` lines. There was no WAF cleanup, only one public subnet, and dead endpoint/NAT/ASG/LT/NACL/private-subnet lines.
- **Criteria:** the first criterion now also requires "two public subnets in different Availability Zones (for example us-east-1a and us-east-1b), both tagged LabId=ul-08 and associated with the public route table". The count stays at 15.
- **After:** `# Uses` lists `$WebAclName, $WebAclId, $AlbArn, $ListenerArn, $TargetGroupArn, $InstanceId, $AllocationId, $VpcId, $SubnetPub, $SubnetPub2, $IgwId, $PublicRouteTableId, $RtAssocPub, $RtAssocPub2, $SgId`. Order: `wafv2 disassociate-web-acl --resource-arn $AlbArn` → `$LockToken = aws wafv2 get-web-acl --name --scope REGIONAL --id --query LockToken` → `delete-web-acl … --lock-token $LockToken` → delete listener → ALB delete and `wait load-balancers-deleted` → TG → instance terminate and wait → EIP release (kept because the criterion says "Public IPv4 released if allocated standalone") → 2× disassociate → RT → 2× subnet → IGW → SG → VPC. This follows the criterion "WAF, listener, ALB, TG, EC2".
- **Recovery:** added the note to wait 1–2 min and rerun on DependencyViolation (lingering ALB ENIs).
- **Verification:** tag search, `wafv2 list-web-acls --scope REGIONAL`, ALB NotFound, VPC NotFound.
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/wafv2/get-web-acl.html (LockToken is top-level, verified) ; https://docs.aws.amazon.com/cli/latest/reference/wafv2/delete-web-acl.html ; https://docs.aws.amazon.com/cli/latest/reference/wafv2/disassociate-web-acl.html ; https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#availability-zones

## UL-09 (N2b, N6)
- **Before:** `$null` lines. The ASG update and delete carried `-ErrorAction`, so they never ran. There was no SG, alarm or wait.
- **After:** `# Uses: $AsgName, $LaunchTemplateId, $AlarmName, $SgId`. The instance IDs are captured (`AutoScalingGroups[0].Instances[].[InstanceId]`) → scale to 0 and `--force-delete` → `ec2 wait instance-terminated` on those IDs → poll `length(AutoScalingGroups)` until 0 (the autoscaling CLI has **no** `wait` command, verified) → `cloudwatch delete-alarms` → delete launch template → delete SG.
- **Verification:** tag search, empty ASG list, no `LabId=ul-09` volumes.
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/autoscaling/index.html ; https://docs.aws.amazon.com/cli/latest/reference/autoscaling/delete-auto-scaling-group.html ; https://docs.aws.amazon.com/cli/latest/reference/ec2/wait/instance-terminated.html

## UL-14 (N2b, N6, T1)
- **Before:** only `$DbId`/`$SubnetGroup`, both with `-ErrorAction` (the RDS delete never ran). There was no copy, snapshot or SG delete and no wait.
- **After:** `# Uses: $CopyDbId, $DbId, $DbSnapshotId, $SubnetGroup, $SgId`. The copy is deleted with `--skip-final-snapshot` and `wait db-instance-deleted` → then the source, the same way → `delete-db-snapshot` → `delete-db-subnet-group` → SG.
- **Verification:** tag search, DBInstanceNotFound for both, DBSnapshotNotFound.
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-instance.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/wait/db-instance-deleted.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-snapshot.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-subnet-group.html

## UL-16 (N2b, T1)
- **Before:** `$null` lines, then an unguarded `delete-hosted-zone`, which fails with HostedZoneNotEmpty, then `delete-vpc`.
- **After:** `# Uses: $ZoneId, $VpcId`. Line 3 is `# Set $VpcId only if you created a VPC for this lab. Never delete the default VPC.`
  - `list-resource-record-sets --query "ResourceRecordSets[?Type != 'SOA' && Type != 'NS']" --output json | Out-String | ConvertFrom-Json`.
  - That list builds a DELETE change batch (`ConvertTo-Json -Depth 10 | Set-Content -Encoding Ascii ul16-records-delete.json`), which is passed to `change-resource-record-sets --change-batch file://…`. Then `route53 wait resource-record-sets-changed --id $ChangeId` → `delete-hosted-zone` → `delete-vpc`.
- **Deviation from the AWS report:** the report expected the learner to hand-edit their create file. The batch is generated here instead, so records created in the console are also covered. The PS 5.1 builder was checked offline with a sample record set and produced a valid `{"Changes":[{"Action":"DELETE","ResourceRecordSet":{…}}]}`.
- **Verification:** tag search, `get-hosted-zone` NoSuchHostedZone, VPC NotFound (if created).
- **Docs:** https://docs.aws.amazon.com/cli/latest/reference/route53/change-resource-record-sets.html ; https://docs.aws.amazon.com/cli/latest/reference/route53/wait/resource-record-sets-changed.html (`--id` required, verified) ; https://docs.aws.amazon.com/cli/latest/reference/route53/delete-hosted-zone.html

## Open / for review
- The Teacher needs to re-validate (AGENTS.md "after implementation"). The AWS and Student reviewers should check the two deviations: the UL-07 poll guard and the UL-16 generated batch.
- UL-16: an NS record for a delegated subdomain would be skipped by the `Type != 'NS'` filter. That is an edge case, and the criteria do not create one.
- UL-09: if the ASG is already gone, the instance-ID lookup returns `None` and the wait line errors harmlessly.
