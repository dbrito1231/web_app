# AWS review: Amendment 1 (N1–N4, N6, N7). Pre-implementation

Target path (write blocked: this session is in plan mode): `reports/fix-loop-r2/amendment-1/AWS.md`. Copy this content there.

Reviewer: Senior AWS SA (read-only). Commit reviewed: working tree at `8789bf5`. No AWS calls made.

## Per-item verdicts

| ID | Confirmed? | Verdict | Corrected commands / notes | Docs |
|---|---|---|---|---|
| N1 GL-08 ALB one subnet | **Yes.** An ALB needs at least two subnets, each in a different AZ | **approve with additions** | See N1 block below. Tag both subnets. `--subnets $SubnetPub $SubnetPub2` is valid in PowerShell (two separate args to a list parameter). Teardown order approved | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#availability-zones |
| N2a GL-01 boundary ARN | **Yes** | **approve** | `$AccountId = aws sts get-caller-identity --query Account --output text` then `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"`. The `$( )` is required. Without it, PowerShell reads `$AccountId:policy` as a drive-qualified variable. This also repairs line 8 (budget delete uses `$AccountId`). Order deactivate MFA → delete virtual MFA → delete boundary → delete user → delete policy → delete budget is valid. The delete-user prerequisites are password, access keys, signing certificates, SSH keys, service credentials, MFA, inline and attached policies, and groups. A permissions boundary is **not** on that list. The lab removes it first anyway, which is still correct because delete-policy then finds nothing that uses the policy. GL-01 creates no login profile, so none needs deleting | https://docs.aws.amazon.com/cli/latest/reference/iam/delete-user.html ; https://docs.aws.amazon.com/cli/latest/reference/iam/delete-policy.html |
| N2b 10 UL `$X = $null` | **Yes.** `$X = $null` sets the value to null, so `if ($X)` is false and the delete is skipped | **concerns** | Removing the null lines is right, but several teardowns are still wrong or incomplete after that. See the N2b table. Also, **UL-05, 10, 11, 12 and 16 have unguarded commands**, so the proposed comment "Unset ones are skipped" is false for them. Fix: wrap every delete in `if ($X) { … }`, or reword the comment | https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_variables?view=powershell-5.1 |
| N2c GL-06/GL-08 dead lines | **Yes** | **approve** | GL-06 dead lines (1-based index in `orderedDeletesPowerShell`): 1–10, 13, 14–15 (duplicate NAT/EIP), 16–22, 30. Keep 11, 12, 23–29, 31. GL-08 dead lines: 1–11, 12, 13, 14, 16, 17, 19, 20, 22, 24, 26. Keep 15, 18, 21, 23, 25, 27–29 and add the N1 lines. **UL-06 also has the duplicate NAT/EIP pair (lines 24–25)**. Remove it too | n/a (derived from steps) |
| N3 UL-07 EFS | **Yes.** Mount targets must be deleted before the file system. Both deletes are asynchronous. The CLI has **no** `aws efs wait` | **approve with corrected commands** | See N3 block below. After the file system is gone, delete the mount-target SG **before** the instance SG, because it references the instance SG | https://docs.aws.amazon.com/cli/latest/reference/efs/delete-file-system.html ; https://docs.aws.amazon.com/cli/latest/reference/efs/delete-mount-target.html ; https://docs.aws.amazon.com/efs/latest/ug/wt1-getting-started.html#wt1-clean-up ; https://docs.aws.amazon.com/cli/latest/reference/efs/index.html |
| N6 `-ErrorAction` on `aws` | **Yes.** Common parameters exist only for cmdlets and advanced functions. PowerShell passes `-ErrorAction SilentlyContinue` to `aws.exe` as literal words. AWS CLI v2 treats unknown arguments as a parse failure and exits with code 252 or 2 **before calling the API** | **concerns (High)** | 16 affected lines: GL-07, GL-09, GL-14 (2), GL-15 (2), GL-19 (2), GL-21 (2), UL-07, UL-09, UL-14 (2), UL-15 (2), UL-19 (2), UL-21 (2). **EKS delete-cluster (GL-19/UL-19), ElastiCache delete-cache-cluster (GL-21/UL-21), RDS delete-db-instance (GL-14/UL-14) and the ASG delete (GL-09/UL-09) never run, so hourly resources keep billing.** Fix: **drop the flag.** A failed native command does not stop the next line in an interactive session, and the learner should see the error. Do not use `2>$null`, because it hides real failures in a cost-safety teardown. Leave `Remove-Item … -ErrorAction` in GL-03/UL-03 as is (it is a cmdlet). Add waits where a parent delete follows: `aws rds wait db-instance-deleted` before `delete-db-subnet-group`, and `aws elasticache wait cache-cluster-deleted --cache-cluster-id …` before `delete-cache-subnet-group`. In GL-07/UL-07, run `aws ec2 wait volume-available --volume-ids $VolumeId` between detach and delete | https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_commonparameters?view=powershell-5.1 ; https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-returncodes.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-subnet-group.html ; https://docs.aws.amazon.com/cli/latest/reference/elasticache/delete-cache-subnet-group.html |
| N7 UL hard-coded `workbook-glNN` | **Yes.** None of UL-03, 04, 10, 11, 12, 13, 15, 17, 18, 19 or 21 tells the learner, in its scenario, acceptance criteria or hints, to use those names. The GL labs end with an empty tag search, so the GL resources are already gone. The UL teardowns therefore target resources that do not exist and miss the learner's own | **concerns** | Fix: add one criterion to each UL: "Name every resource `workbook-ulNN[-suffix]` and tag it `LabId=ul-NN`". Rewrite the teardowns to use those names, or better, variables named in the `# Uses …` header (`$FunctionName`, `$RoleName`, `$TableName`, `$ClusterName`…). UL-15 explicitly reuses "the GL-10 Lambda log group (or equivalent)". Change it to the UL-10 or the learner's own log group | n/a (content cross-check) |
| Scanner hardening | Sound, with gaps | **concerns (minor)** | (1) UL labs have no `steps`, so rule 1 must defer to the `# Uses` header for `ul-*`. (2) Allow teardown assignments whose right-hand side is a lookup (`$AccountId = aws sts …`, `$Serial = …`, `$Bucket = "…"`, `$MtIds = …`, loop variables). Ban only `= $null`, `= ''`, `= ""`, `Clear-Variable` and `Remove-Variable`. (3) Add rule: fail on `-ErrorAction`/`-ea` on any line that invokes `aws`, while allowing it on cmdlets (N6). (4) Add rule: fail on `workbook-gl` inside `ul-*` teardowns (N7). (5) Add rule: in `ul-*` teardowns, every `aws … delete|terminate|release|detach` must sit inside `if ($Var)`, or the header comment must not promise skipping. (6) Add rule: warn on duplicate identical teardown lines (the GL-06/UL-06 NAT/EIP pair) | n/a |

### N1: exact commands (GL-08)

s06, add after `$SubnetPub` (and tag `$SubnetPub` the same way):
```powershell
$SubnetPub2 = aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.80.2.0/24 --availability-zone us-east-1b --query Subnet.SubnetId --output text --tag-specifications "ResourceType=subnet,Tags=[{Key=LabId,Value=gl-08}]"
$RtAssocPub2 = aws ec2 associate-route-table --route-table-id $PublicRouteTableId --subnet-id $SubnetPub2 --query AssociationId --output text
```
s09:
```powershell
$AlbArn = aws elbv2 create-load-balancer --name workbook-gl08 --subnets $SubnetPub $SubnetPub2 --security-groups $SgId --query "LoadBalancers[0].LoadBalancerArn" --output text --tags Key=LabId,Value=gl-08 Key=Workbook,Value=aws-tf-lab
```
Add before s10: `aws elbv2 wait target-in-service --target-group-arn $TargetGroupArn --targets Id=$InstanceId` (5 healthy checks × 30 s by default is about 2.5 min).

Teardown (final, in order):
```powershell
if ($AlbArn) { aws elbv2 delete-load-balancer --load-balancer-arn $AlbArn; aws elbv2 wait load-balancers-deleted --load-balancer-arns $AlbArn }
if ($TargetGroupArn) { aws elbv2 delete-target-group --target-group-arn $TargetGroupArn }
if ($InstanceId) { aws ec2 terminate-instances --instance-ids $InstanceId; aws ec2 wait instance-terminated --instance-ids $InstanceId }
if ($RtAssocPub) { aws ec2 disassociate-route-table --association-id $RtAssocPub }
if ($RtAssocPub2) { aws ec2 disassociate-route-table --association-id $RtAssocPub2 }
if ($PublicRouteTableId) { aws ec2 delete-route-table --route-table-id $PublicRouteTableId }
if ($SubnetPub) { aws ec2 delete-subnet --subnet-id $SubnetPub }
if ($SubnetPub2) { aws ec2 delete-subnet --subnet-id $SubnetPub2 }
if ($IgwId -and $VpcId) { aws ec2 detach-internet-gateway --internet-gateway-id $IgwId --vpc-id $VpcId; aws ec2 delete-internet-gateway --internet-gateway-id $IgwId }
if ($SgId) { aws ec2 delete-security-group --group-id $SgId }
if ($VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }
```
Why this order works:
- A route table cannot be deleted while it is associated with a subnet, so disassociate first (https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-route-table.html).
- A subnet cannot be deleted while it has running instances (https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-subnet.html).
- The IGW cannot be detached while the VPC has public or Elastic IPs mapped (https://docs.aws.amazon.com/cli/latest/reference/ec2/detach-internet-gateway.html).
- A security group cannot be deleted while an ENI still uses it (https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-security-group.html).
- Deleting the ALB does not delete target groups or instances (https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-delete.html).
- **Needs Verification:** ALB ENIs may linger briefly after `load-balancers-deleted`. If a subnet, IGW or SG delete returns DependencyViolation, wait about a minute and rerun that line. Add one sentence saying so to `recovery`.

### N3: exact commands (UL-07), placed before the instance and SG deletes
```powershell
# Uses $FileSystemId
if ($FileSystemId) { $MtIds = aws efs describe-mount-targets --file-system-id $FileSystemId --query "MountTargets[].[MountTargetId]" --output text; foreach ($MtId in $MtIds) { if ($MtId) { aws efs delete-mount-target --mount-target-id $MtId } } }
if ($FileSystemId) { do { Start-Sleep -Seconds 10; $MtLeft = aws efs describe-mount-targets --file-system-id $FileSystemId --query "length(MountTargets)" --output text } while ($MtLeft -ne '0') }
if ($FileSystemId) { aws efs delete-file-system --file-system-id $FileSystemId }
if ($MountTargetSgId) { aws ec2 delete-security-group --group-id $MountTargetSgId }   # after the MT ENIs are gone; before the instance SG
```
Notes:
- `[MountTargetId]` in brackets gives one ID per line, so PowerShell builds an array. Without brackets, the output is one tab-separated line (https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output).
- Mount targets in the `deleting` state still appear in the list, so the loop waits for a count of 0 (https://docs.aws.amazon.com/cli/latest/reference/efs/describe-mount-targets.html).
- The EFS user guide also says to delete access points first. UL-07 does not create any. **Needs Verification**: whether the API requires this. If the lab ever adds access points, add `aws efs describe-access-points --file-system-id $FileSystemId --query "AccessPoints[].[AccessPointId]" --output text` followed by a `delete-access-point` loop.
- Optional confirmation: `aws efs describe-file-systems --file-system-id $FileSystemId` eventually returns FileSystemNotFound.

### N2b: per-lab teardown check (after removing the `$null` lines)

| Lab | Problem | Severity | Fix | Doc |
|---|---|---|---|---|
| UL-05 | AC requires 4 subnets (2 public, 2 private). The teardown handles only one of each, one private association and one NACL association. Leftover subnets make `delete-vpc` fail. All lines are unguarded | Medium | Add `$SubnetPub2`, `$SubnetPriv2`, `$RtAssocPub2`, `$RtAssocPriv2`, `$NaclAssocId2`, and wrap every line in `if` | delete-subnet / delete-route-table URLs above |
| UL-06 | Order is valid (NAT delete + wait, then EIP release). Duplicate NAT/EIP pair (24–25). ALB/ASG/NACL/endpoint lines are dead | Low | Remove the duplicates and dead lines | https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-nat-gateway.html (deleting the NAT does not release the EIP) |
| UL-07 | No EFS cleanup (N3). No SG deletes, although AC requires dedicated SGs. `-ErrorAction` (N6). No `wait volume-available` | Medium | N3 block, then SG deletes, then N6 fix | see N3/N6 |
| UL-08 | **No WAF cleanup**, although AC requires disassociating and deleting the web ACL, which bills monthly. Only one `$SubnetPub`, but the ALB needs two (same bug as N1) | **High** | Before the ALB: `if ($AlbArn) { aws wafv2 disassociate-web-acl --resource-arn $AlbArn }`, then `if ($WebAclId) { $LockToken = aws wafv2 get-web-acl --name $WebAclName --scope REGIONAL --id $WebAclId --query LockToken --output text; aws wafv2 delete-web-acl --name $WebAclName --scope REGIONAL --id $WebAclId --lock-token $LockToken }`. Add `$SubnetPub2`/`$RtAssocPub2` | https://docs.aws.amazon.com/cli/latest/reference/wafv2/delete-web-acl.html |
| UL-09 | `-ErrorAction` stops the ASG update/delete from running (N6). The dedicated SG is not deleted (AC). Scaling to 0 then `--force-delete` is valid | High (via N6) | Drop the flag. Add an SG delete after the instances terminate | N6 URLs |
| UL-10 | Hard-coded gl10 names (N7). No event-source-mapping delete, although AC puts it first; delete-function does not remove mappings. No DLQ delete (one `$QueueUrl`). The unsubscribe pipe breaks with 2+ subscriptions (one tab-separated line), and delete-topic removes subscriptions anyway | Medium | `aws lambda list-event-source-mappings --function-name $FunctionName --query "EventSourceMappings[].[UUID]" --output text` → `delete-event-source-mapping --uuid`. Add `if ($DlqUrl) { aws sqs delete-queue --queue-url $DlqUrl }`. Drop the unsubscribe line | https://docs.aws.amazon.com/cli/latest/reference/lambda/delete-function.html ; https://docs.aws.amazon.com/cli/latest/reference/sns/delete-topic.html |
| UL-11 | Syntax valid (`delete-api` removes routes, authorizers and stages). N7 names. If the learner used a Lambda authorizer function, it is not deleted | Low | N7. Guard with `if` | https://docs.aws.amazon.com/cli/latest/reference/iam/delete-role.html |
| UL-12 | Syntax valid. N7 names. The Lambda task function from the hint is not deleted | Low | N7. Add a function delete if one was created | — |
| UL-14 | `-ErrorAction` stops **RDS delete** from running (N6, cost). Only one `$DbId`, but AC has a source, a restored copy and a manual snapshot. Manual snapshots are not deleted by delete-db-instance. Subnet group delete runs before the instance is gone and fails. SG not deleted | **High** | `if ($CopyDbId) { aws rds delete-db-instance --db-instance-identifier $CopyDbId --skip-final-snapshot }`; same for `$DbId`; `aws rds wait db-instance-deleted` for each; `if ($DbSnapshotId) { aws rds delete-db-snapshot --db-snapshot-identifier $DbSnapshotId }`; then `delete-db-subnet-group`; then the SG | https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-instance.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-subnet-group.html |
| UL-16 | `delete-hosted-zone` fails with HostedZoneNotEmpty because AC requires ≥2 records. `delete-vpc` then also fails, because the zone still exists | Medium | Before the zone delete: `if ($ZoneId) { aws route53 change-resource-record-sets --hosted-zone-id $ZoneId --change-batch file://ul16-records-delete.json }` (the learner's create file with `"Action": "DELETE"`). Guard the zone and VPC lines | https://docs.aws.amazon.com/cli/latest/reference/route53/delete-hosted-zone.html |

## Other problems found in these labs

| Sev | Lab | Problem | Fix | Doc |
|---|---|---|---|---|
| High | GL-19, UL-19 | N6 flag blocks the EKS delete. UL-19 also adds a node group or Fargate profile, and delete-cluster fails while one exists. The node group's EC2 instances and the cluster ($/h) keep billing | `aws eks delete-nodegroup … ; aws eks wait nodegroup-deleted …` and/or `delete-fargate-profile` + `wait fargate-profile-deleted`, then `delete-cluster` + `wait cluster-deleted` | https://docs.aws.amazon.com/cli/latest/reference/eks/delete-cluster.html ; https://docs.aws.amazon.com/cli/latest/reference/eks/wait/index.html |
| High | GL-21, UL-21 | N6 flag blocks the ElastiCache delete. The subnet group needs the cluster gone first | Drop the flag. Add `aws elasticache wait cache-cluster-deleted` | elasticache URL above |
| Medium | UL-03 | AC enables GuardDuty and then disables it, but the teardown has no `guardduty delete-detector` | `$DetectorId = aws guardduty list-detectors --query "DetectorIds[0]" --output text`, then `delete-detector --detector-id` (only if the learner created it) | https://docs.aws.amazon.com/cli/latest/reference/guardduty/delete-detector.html |
| Medium | UL-04 | The comment says "Key remains scheduled for deletion", but no `schedule-key-deletion` runs. The Secrets Manager secret and SSM parameter from AC are not deleted | `aws kms schedule-key-deletion --key-id $KeyId --pending-window-in-days 7`; `aws secretsmanager delete-secret --secret-id $SecretId --force-delete-without-recovery` (Needs Verification: whether to allow recovery instead); `aws ssm delete-parameter --name $ParamName` | https://docs.aws.amazon.com/cli/latest/reference/kms/schedule-key-deletion.html |
| Medium | GL-16 | s11 and the teardown delete the zone without first deleting the s08 record, so HostedZoneNotEmpty. `delete-vpc` then also fails | Add a DELETE change batch (mirror of `gl16-record.json`) first | route53 URL above |
| Medium | GL-14 | s06/s07 use `$SubnetGroup`/`$DbId`, but no step sets them | Add `$SubnetGroup = 'workbook-gl14'` and `$DbId = 'workbook-gl14'` in s06 | — |
| Low | UL-18 | `delete-cluster` needs no running tasks or active services. The one-off task should have stopped already, but no check is taught | Add `aws ecs list-tasks --cluster …` check, or `stop-task` | https://docs.aws.amazon.com/cli/latest/reference/ecs/delete-cluster.html |
| Low | GL-08 | Instance and ALB share one SG open 80/0.0.0.0/0. It works, because the instance has no public IP. The documented best practice is a target SG whose source is the ALB SG | Optional teaching improvement | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html |
| Low | GL-08 | Health check defaults (HTTP, `/`, 200, 5×30 s) match `python3 -m http.server 80`. The instance needs no public IP, because the ALB reaches targets on private IPs. Target group, subnet and route table are untagged, so the tag-search verification cannot see leftovers | Add `--tags Key=LabId,Value=gl-08` to create-target-group, and tag-specifications to the subnet and route table | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html |
| Low | GL-08 s10 | In Windows PowerShell 5.1, `curl` is an alias of `Invoke-WebRequest` (Needs Verification: citation). Output differs from what learners expect | Use `curl.exe http://$Dns/` | Needs Verification |
| Low | GL-10 | The unsubscribe pipe gets one tab-separated line for 2 subscriptions (SQS + Lambda), so the call fails. It is harmless, because delete-topic removes subscriptions | Drop the line, or use `[SubscriptionArn]` | https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output |
| Low | GL-11 s08 | `arn:aws:execute-api:us-east-1:$AccountId:$ApiId/*/*`: the `$AccountId:` in front of `$` may fail to parse in PowerShell (Needs Verification) | Use `"arn:aws:execute-api:us-east-1:$($AccountId):$($ApiId)/*/*"` | Needs Verification |

## Overall: concerns

The approach for N1, N2a, N2c and N3 is correct. Approve them with the exact commands above. Blocking concerns:
- N6 is High. Hourly EKS, ElastiCache, RDS and ASG deletes never execute. Fold it into this amendment.
- N2b alone is not enough. UL-08 (WAF plus the two-subnet ALB) and UL-14 (copy, snapshot and waits) stay broken. UL-05 and UL-16 fail at delete-vpc and delete-hosted-zone. The "Unset ones are skipped" comment is false for unguarded labs.
- N7 affects 11 UL labs. It needs a naming criterion and variable-based teardown.
