# Amendment 1, revised: implementation batch A (guided labs)

Implementer: Lead Developer. Scope: `content/labs/gl-{01,03,06,07,08,09,10,11,14,15,16,19,21}.json` only. No AWS calls were made, and no git commands changed anything.

Method: one Python script loaded each file with `json.load` and wrote it back with `json.dumps(indent=2, ensure_ascii=True) + "\n"` in text mode (CRLF kept). The script asserts each old string before replacing it. Sources: `reports/fix-loop-r2/amendment-1/AWS.md` and `TEACHER.md`, plus the CLI references listed under each lab.

Format note: gl-07, 09, 10, 11, 14, 15, 16, 19 and 21 had raw UTF-8 `—`/`–` characters in `title`, `stillBillingNote` and s15. The prescribed writer turns them into `—`/`–` escapes. The parsed JSON is identical, but those lines show up in the diff.

Checks run: `python scripts\content_lint.py` passes. `scripts\scan_lab_placeholders.py` reports no `gl-*` finding; its remaining failures are all `ul-*` labs, which belong to other batches. No `aws` line in any GL file still has `-ErrorAction`, and no GL teardown has a `= $null` line.

## GL-01 (N2a)
Teardown line 1:
- before: `$BoundaryArn = $null`
- after: `$AccountId = aws sts get-caller-identity --query Account --output text` and then `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"`

Both lines come before `delete-policy` and before `delete-budget`, which uses `$AccountId`.

Docs: https://docs.aws.amazon.com/cli/latest/reference/iam/delete-policy.html ; https://docs.aws.amazon.com/cli/latest/reference/iam/delete-user.html

## GL-03
No change. Its only `-ErrorAction` is on `Remove-Item`, a real PowerShell cmdlet, so it stays (AWS report, N6).

## GL-06 (N2c)
Teardown drops from 31 lines to 10.
- Removed the 10 `$X = $null` lines.
- Removed the duplicate NAT/EIP pair (old lines 14–15).
- Removed the guarded deletes for resources the steps never create: endpoint, ALB, target group, ASG, launch template, instance, NACL association, custom NACL, and SG.
- Kept, in this order: NAT delete + `wait nat-gateway-deleted`, release EIP, disassociate public and private route tables, delete both route tables, delete both subnets, detach and delete the IGW, delete the VPC.

The s13 order text and the stopChargesPanel already matched, so neither changed.

Doc: https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-nat-gateway.html

## GL-07 (N6)
- Teardown:
  - before: `if ($VolumeId) { aws ec2 detach-volume --volume-id $VolumeId -ErrorAction SilentlyContinue; aws ec2 delete-volume --volume-id $VolumeId -ErrorAction SilentlyContinue }`
  - after: `if ($VolumeId) { aws ec2 detach-volume --volume-id $VolumeId; aws ec2 wait volume-available --volume-ids $VolumeId; aws ec2 delete-volume --volume-id $VolumeId }`
- s13 order text:
  - before: "snapshot, any remaining volume, terminated instance"
  - after: "instance (if still running), any remaining volume (detach, wait until available, delete), snapshot", plus a note that NotFound or IncorrectState means the resource is already gone. This now matches the teardown order.
- stopChargesPanel now reads: terminate and wait → detach and delete the volume → delete the snapshot.

Docs: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_commonparameters?view=powershell-5.1 ; https://docs.aws.amazon.com/cli/latest/reference/ec2/wait/volume-available.html

## GL-08 (N1, N2c, T6)
Step changes:
- **s06**
  - `$SubnetPub` gains `--tag-specifications "ResourceType=subnet,Tags=[{Key=LabId,Value=gl-08}]"`.
  - New: `$SubnetPub2 = aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.80.2.0/24 --availability-zone us-east-1b --query Subnet.SubnetId --output text --tag-specifications "ResourceType=subnet,Tags=[{Key=LabId,Value=gl-08}]"`.
  - `create-route-table` gains `--tag-specifications "ResourceType=route-table,Tags=[{Key=LabId,Value=gl-08}]"`.
  - New: `$RtAssocPub2 = aws ec2 associate-route-table --route-table-id $PublicRouteTableId --subnet-id $SubnetPub2 --query AssociationId --output text`.
  - Success line: before "public subnet has internet route"; after "both public subnets (us-east-1a and us-east-1b) are associated with the route table that has the internet route".
- **s09**
  - ALB: `--subnets $SubnetPub` becomes `--subnets $SubnetPub $SubnetPub2`.
  - `create-target-group` gains `--tags Key=LabId,Value=gl-08 Key=Workbook,Value=aws-tf-lab`.
  - New, before the success line: `aws elbv2 wait target-in-service --target-group-arn $TargetGroupArn --targets Id=$InstanceId`. It polls every 15 s, 40 attempts.
  - Success line now reads: the wait returns with no error.
- **s10:** `curl http://$Dns/` becomes `curl.exe http://$Dns/`, with a note on the PS 5.1 alias.
- **s11:** text reads: ALB (wait) → target group → instance → VPC stack.
- **s13:** text reads: ALB (wait; listener goes with it), target group, instance (wait), both route-table associations, route table, both subnets, IGW, SG, VPC.

Teardown, stopChargesPanel and recovery:
- **stopChargesPanel:** rewritten to the same order.
- **Teardown:** replaced with the AWS report's 11-line N1 block verbatim. All 11 `$null` lines are gone, along with the endpoint, NAT, EIP, ASG, launch template, NACL, private route-table and private-subnet lines.
- **recovery:** appended the DependencyViolation note (ALB ENIs can linger; wait 1–2 minutes and rerun from that line).

Docs:
- https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#availability-zones
- https://docs.aws.amazon.com/cli/latest/reference/elbv2/wait/target-in-service.html
- https://docs.aws.amazon.com/cli/latest/reference/elbv2/create-target-group.html (`--tags`)
- https://docs.aws.amazon.com/cli/latest/reference/ec2/create-route-table.html (`ResourceType=route-table`)
- https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-route-table.html
- https://docs.aws.amazon.com/cli/latest/reference/ec2/delete-subnet.html

## GL-09 (N6 + ASG wait)
- Teardown line 1: removed both ` -ErrorAction SilentlyContinue`.
- New line 2: `if ($AsgName) { do { Start-Sleep -Seconds 15; $AsgLeft = aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names $AsgName --query "length(AutoScalingGroups)" --output text } while ($AsgLeft -and $AsgLeft -ne '0') }`.
  - The AWS CLI has no `aws autoscaling wait`; the index page lists no `wait` command.
  - `$AsgLeft -and` stops the loop if the describe call itself fails, so it cannot spin forever.
- s13 text:
  - before: "ASG, launch template, any instances"
  - after: "ASG (scale to 0, force-delete, poll until gone; terminates its instances), launch template"
- stopChargesPanel: the old text mentioned SGs, subnets and VPC, which this lab never creates (it uses the default VPC). The new text says so.

Docs: https://docs.aws.amazon.com/cli/latest/reference/autoscaling/index.html ; https://docs.aws.amazon.com/cli/latest/reference/autoscaling/delete-auto-scaling-group.html

## GL-10 (T6)
- Dropped the teardown line `aws sns list-subscriptions-by-topic ... --output text | ForEach-Object { ... unsubscribe ... }`. With two subscriptions, text output is one tab-separated line, so that call failed. `delete-topic` "Deletes a topic and all its subscriptions."
- s13:
  - before: "SNS subscriptions, Lambda, log group, queue, topic, IAM role"
  - after: "Lambda, log group, queue, topic (delete-topic also deletes its SNS subscriptions), IAM role"
- stopChargesPanel updated to match.

Docs: https://docs.aws.amazon.com/cli/latest/reference/sns/delete-topic.html ; https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#text-output

## GL-11 (T5)
- s08:
  - before: `--source-arn arn:aws:execute-api:us-east-1:$AccountId:$ApiId/*/*`
  - after: `--source-arn "arn:aws:execute-api:us-east-1:$($AccountId):$($ApiId)/*/*"`, plus a note on the `$( )`.
- s09: `curl "$InvokeUrl/prod/hello"` becomes `curl.exe "$InvokeUrl/prod/hello"`. This is the same PS 5.1 alias issue as GL-08, applied for consistency; the amendment did not list it.

Doc: https://docs.aws.amazon.com/cli/latest/reference/lambda/add-permission.html

## GL-14 (N6, T4)
T4 was already satisfied: s06 sets `$SubnetGroup = "workbook-gl14"` and s07 sets `$DbId = "workbookgl14"`. Those names were kept unchanged.

Teardown before:
- `if ($DbId) { aws rds delete-db-instance ... --skip-final-snapshot -ErrorAction SilentlyContinue }`
- `if ($SubnetGroup) { aws rds delete-db-subnet-group ... -ErrorAction SilentlyContinue }`

Teardown after:
1. `$SubnetGroup = 'workbook-gl14'`
2. `$DbId = 'workbookgl14'` (string builds, so the teardown still works in a new shell)
3. `aws rds delete-db-instance --db-instance-identifier $DbId --skip-final-snapshot`
4. `aws rds wait db-instance-deleted --db-instance-identifier $DbId` (succeeds when the instance list is empty)
5. `aws rds delete-db-subnet-group --db-subnet-group-name $SubnetGroup`

Text changes:
- s13 now says "RDS instance (wait until deleted), subnet group", with a note on DBInstanceNotFound if s09 already ran.
- stopChargesPanel no longer mentions security groups; the lab uses the default VPC SG.

Docs: https://docs.aws.amazon.com/cli/latest/reference/rds/wait/db-instance-deleted.html ; https://docs.aws.amazon.com/cli/latest/reference/rds/delete-db-subnet-group.html

## GL-15 (N6)
Removed ` -ErrorAction SilentlyContinue` from `aws cloudtrail stop-logging` and `aws cloudtrail delete-trail`. Nothing else changed.

## GL-16 (T3)
Steps:
- **s08:** the vague "Save gl16-record.json with A record …" became an explicit command:

  ```powershell
  $Utf8 = New-Object System.Text.UTF8Encoding $false; [IO.File]::WriteAllText("$pwd\gl16-record.json", '{"Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"app.workbook.gl16.local","Type":"A","TTL":300,"ResourceRecords":[{"Value":"10.160.1.10"}]}}]}', $Utf8)
  ```

  It fixes TTL 300 so the DELETE can match it exactly.
- **s10:** "Run change-batch DELETE for the app record." became two commands: the same writer with `"Action":"DELETE"` into `gl16-record-delete.json`, then `aws route53 change-resource-record-sets --hosted-zone-id $ZoneId --change-batch file://gl16-record-delete.json`.
- **s13:** "hosted zone records, zone, VPC" became "the app A record (DELETE change batch), zone, VPC", with a note that InvalidChangeBatch (not found) means s10 already removed the record.

Teardown:
- before: `aws route53 delete-hosted-zone --id $ZoneId` and `aws ec2 delete-vpc --vpc-id $VpcId`
- after:
  1. The DELETE-file writer, so it works even if the learner stops before s10.
  2. `if ($ZoneId) { aws route53 change-resource-record-sets --hosted-zone-id $ZoneId --change-batch file://gl16-record-delete.json }`
  3. `if ($ZoneId) { aws route53 delete-hosted-zone --id $ZoneId }`
  4. `if ($VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }`

stopChargesPanel updated to match.

Docs: https://docs.aws.amazon.com/cli/latest/reference/route53/change-resource-record-sets.html (DELETE must repeat all values) ; https://docs.aws.amazon.com/cli/latest/reference/route53/delete-hosted-zone.html (HostedZoneNotEmpty)

## GL-19 (N6)
- Removed ` -ErrorAction SilentlyContinue` from `aws eks delete-cluster --name workbook-gl19` and `aws eks wait cluster-deleted --name workbook-gl19`.
- GL-19 creates no node group or Fargate profile (the body says "no managed nodes"), so no extra deletes were added.

Docs: https://docs.aws.amazon.com/cli/latest/reference/eks/wait/cluster-deleted.html ; https://docs.aws.amazon.com/eks/latest/userguide/delete-cluster.html

## GL-21 (N6 + wait)
Teardown before:
- `delete-cache-cluster ... -ErrorAction SilentlyContinue`
- `delete-cache-subnet-group ... -ErrorAction SilentlyContinue`

Teardown after:
1. `aws elasticache delete-cache-cluster --cache-cluster-id workbook-gl21`
2. `aws elasticache wait cache-cluster-deleted --cache-cluster-id workbook-gl21`
3. `aws elasticache delete-cache-subnet-group --cache-subnet-group-name workbook-gl21`

The s13 text and stopChargesPanel now mention the wait.

Doc: https://docs.aws.amazon.com/cli/latest/reference/elasticache/wait/cache-cluster-deleted.html

## Open items / unsure
- **GL-19 stopChargesPanel.** It still says "Delete cluster, IAM roles, security groups AWS creates", but no teardown line deletes a security group. I could not find a doc stating that EKS removes its cluster security group on delete-cluster, so I left the wording alone. Teacher/AWS should confirm and adjust it.
- **GL-08.** The optional best-practice split of the ALB SG and the target SG (AWS report, Low) is not done.
- **GL-06.** Subnets and route tables are still untagged, so the tag-search check cannot see them. This was not in scope; only GL-08 tagging was requested.
- **GL-14 and GL-16.** The teardowns now contain non-`aws` assignment lines: GL-14 builds name strings, and GL-16 has the `$Utf8` writer. The rewritten scanner must allow both.
