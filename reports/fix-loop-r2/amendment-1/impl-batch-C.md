# Amendment 1 revised: implementation batch C (UL-03, 04, 10, 11, 12, 13, 15, 17, 18, 19, 21)

Lead Dev, 2026-09-26. Applies N7, N2b, N6, T2, T3 and T6 from `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` (Amendment 1, revised), using commands from `AWS.md` and `TEACHER.md`. No AWS calls were made. The edits came from a scratchpad script: `json.load`, then `json.dumps(indent=2, ensure_ascii=True) + "\n"`, written as UTF-8 text. Nothing was committed.

Checks after the edit: `scripts\content_lint.py` PASS. `scripts\scan_lab_placeholders.py` (hardened version already in the tree) PASS, 42 labs.

## Conventions used in all 11 files

- **N7.** A new first acceptance criterion: "Name the resources you create `workbook-ulNN`: …", which lists every resource name and asks for tag `LabId=ul-NN`. The teardown uses those names. No `workbook-gl` name is left in any of these files.
- **N2b.**
  - Line 1 is `# Uses: none (resources are named workbook-ulNN)`. None of the teardowns relies on a variable that the learner set while building. Every ID is either a fixed name or looked up in the teardown itself.
  - Line 2 is `# Lost an ID? aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=ul-NN`.
  - Every delete that uses a variable is guarded by `if ($X -and $X -ne 'None') { … }` or by a `foreach` loop with `if ($x)`. With `--output text`, a JMESPath `| [0]` that finds nothing prints `None`, so the guard also checks for that value.
  - No line sets a variable to `$null`.
- **N6.** `-ErrorAction SilentlyContinue` is removed from every `aws` line. It stays only on the `Remove-Item` cmdlet (UL-03, UL-21), where it is a real PowerShell parameter.
- **IAM roles.** A role is deleted with three lines: detach every attached managed policy (`list-attached-role-policies --query "AttachedPolicies[].[PolicyArn]"`), delete every inline policy (`list-role-policies` split on whitespace), then `delete-role`. This way the teardown still works when the learner attaches a different policy than the guided lab did. `delete-role` fails while any policy is still attached. Doc: https://docs.aws.amazon.com/cli/latest/reference/iam/delete-role.html
- **Optional resources.** Log groups, Lambda functions, the Cognito pool, the workgroup, the crawler and the security group are looked up by exact name first, so a resource the learner did not create is skipped without an error.
- **Verification.** The stale `LabId=gl-NN` tag-search line is replaced with `ul-NN` checks.

## Per lab

### UL-03 (T3, N7)
- **Before:**
  - The teardown deleted `workbook-gl03-role` / `gl03-read` and bucket `workbook-gl03-<acct>`.
  - There was no GuardDuty delete.
  - Verification checked gl-03.
- **After:**
  - Criterion: role `workbook-ul03-role` (inline `ul03-read`), bucket `workbook-ul03-<acct>`, optional trail `workbook-ul03-trail`.
  - Teardown order:
    1. Clear the STS environment variables.
    2. A comment says to skip the GuardDuty lines if GuardDuty was on before the lab, because findings and settings are lost.
    3. `$DetectorId = aws guardduty list-detectors --query "DetectorIds[0]" --output text`, then `if ($DetectorId -and $DetectorId -ne 'None') { aws guardduty delete-detector … }`.
    4. Optional trail lookup and `delete-trail`.
    5. Role policy loops, then `delete-role`.
    6. Empty the bucket, then delete it.
  - This follows the criterion "GuardDuty before IAM and S3".
  - Verification: tag search, `list-detectors` empty, `get-role` NoSuchEntity, `head-bucket` 404.
  - The stopChargesPanel is reworded.
- **Added:** the GuardDuty detector delete, the optional CloudTrail trail delete, and removal of every role policy.
- **Docs:**
  - https://docs.aws.amazon.com/cli/latest/reference/guardduty/delete-detector.html
  - https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_suspend-disable.html (says disabling loses findings and configuration)

### UL-04 (T3, N7)
- **Before:**
  - Bucket and alias used gl04 names.
  - The comment "Key remains scheduled for deletion" had no command behind it.
  - The secret and parameter were never deleted.
- **After:**
  - Criterion: alias `alias/workbook-ul04`, secret `workbook-ul04-secret`, parameter `workbook-ul04-param`, bucket `workbook-ul04-<acct>`.
  - Teardown order:
    1. `$KeyId = aws kms describe-key --key-id alias/workbook-ul04 --query KeyMetadata.KeyId --output text`. This runs first, while the alias still exists.
    2. `aws secretsmanager delete-secret --secret-id workbook-ul04-secret --force-delete-without-recovery`.
    3. `aws ssm delete-parameter --name workbook-ul04-param`.
    4. Empty and delete the bucket.
    5. `delete-alias`.
    6. `if ($KeyId -and $KeyId -ne 'None') { aws kms schedule-key-deletion --key-id $KeyId --pending-window-in-days 7 }`.
  - Verification: `describe-secret` returns ResourceNotFound, `get-parameter` returns ParameterNotFound, `head-bucket` returns 404, and the key state is PendingDeletion.
- **Why force-delete and not a recovery window:**
  - The lab's own criteria require "describe-secret returns ResourceNotFound" and "No secrets … remain after teardown". A recovery window leaves the secret visible until the window ends.
  - Hint 3 already points to `--force-delete-without-recovery`.
  - The value is a dummy.
  - Cost is the same either way: AWS says "There is no charge for secrets that you have marked for deletion."
  - The teardown comment explains the choice.
- **Docs:**
  - https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/delete-secret.html
  - https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html
  - https://docs.aws.amazon.com/cli/latest/reference/kms/schedule-key-deletion.html (7–30 days; the key becomes PendingDeletion)

### UL-10 (N2b, N7, T1)
- **Before:**
  - `$TopicArn = $null` / `$QueueUrl = $null`.
  - gl10 names.
  - No mapping delete and no DLQ delete.
  - The unsubscribe pipe broke when a topic had more than one subscription.
- **After:**
  - Criterion: function `workbook-ul10`, role `workbook-ul10-lambda`, queues `workbook-ul10` and `workbook-ul10-dlq`, topic `workbook-ul10`, optional table `workbook-ul10-idem`.
  - Teardown order (mappings first, as the criteria require):
    1. `list-event-source-mappings --query "EventSourceMappings[].[UUID]"`, then `delete-event-source-mapping` for each.
    2. `delete-function`, then delete its log group.
    3. Look up both queue URLs with `get-queue-url`, then delete each queue.
    4. Look up the topic with `list-topics` and `ends_with(TopicArn, ':workbook-ul10')`, then delete it. `delete-topic` also removes the topic's subscriptions.
    5. Optional DynamoDB table.
    6. Role loops.
  - The unsubscribe line is dropped.
- **Docs:**
  - https://docs.aws.amazon.com/cli/latest/reference/lambda/delete-function.html
  - https://docs.aws.amazon.com/cli/latest/reference/sns/delete-topic.html

### UL-11 (N2b, N7)
- **Before:** `$ApiId = $null`, gl11 names, and the authorizer function was not deleted.
- **After:**
  - Criterion: API, function and role are named `workbook-ul11`. The optional `workbook-ul11-auth` Lambda authorizer or `workbook-ul11` Cognito pool is also named.
  - Teardown order:
    1. Look up `$ApiId` with `get-apis "Items[?Name=='workbook-ul11'].ApiId | [0]"`, then `delete-api`. This removes the authorizers, routes and stages; a comment says so.
    2. Function and its log group.
    3. Optional authorizer function and its log group.
    4. Optional Cognito pool: lookup, then `delete-user-pool`, with a note to delete any domain first.
    5. Role loops.

### UL-12 (N2b, N7)
- **Before:** `$SmArn = $null` and gl12 names.
- **After:**
  - Criterion: state machine `workbook-ul12`, role `workbook-ul12-sfn`, optional `workbook-ul12-task` and `workbook-ul12-lambda`.
  - Teardown order:
    1. `$SmArn` lookup.
    2. Stop RUNNING executions. Criterion: "No running executions remain".
    3. `delete-state-machine`.
    4. Optional vended log group.
    5. Optional task function and its log group.
    6. Both roles.

### UL-13 (N7)
- **Before:** `delete-table workbook-gl13`.
- **After:**
  - Criterion: table `workbook-ul13`.
  - Teardown: `delete-table`, then `aws dynamodb wait table-not-exists`.
  - Verification: `describe-table` returns ResourceNotFound.

### UL-15 (N6, N7)
- **Before:**
  - `-ErrorAction` on `stop-logging` / `delete-trail` meant neither command ever ran.
  - gl15 names.
  - The scenario pointed at the GL-10 log group, which the GL-10 teardown has already deleted.
- **After:**
  - Scenario and criterion 2: create `/workbook/ul15`, or reuse the UL-10 log group while it still exists.
  - Criterion: trail, bucket, log group, alarm and optional role, all named `workbook-ul15*`.
  - Teardown order:
    1. `stop-logging`, then `delete-trail`.
    2. Alarm.
    3. Log group lookup and delete. The criteria say to reset or delete the log group.
    4. Empty and delete the bucket.
    5. Optional trail role.

### UL-17 (N7)
- **Before:** gl17 buckets, and no table or database drop.
- **After:**
  - Criterion: one bucket `workbook-ul17-<acct>` with prefixes `raw/`, `converted/` and `results/`; database `workbook_ul17`; optional workgroup or crawler `workbook-ul17`.
  - Teardown order:
    1. `DROP DATABASE IF EXISTS workbook_ul17 CASCADE` through Athena. It drops the tables too, which covers the criterion "Drop table statements executed".
    2. Poll `get-query-execution` until the query leaves QUEUED/RUNNING, and print the final state.
    3. Optional `delete-work-group --recursive-delete-option`.
    4. Optional `glue delete-crawler`.
    5. Empty and delete the bucket.
- **Why Athena DROP and not `glue delete-database`:** Glue deletes the tables under a deleted database only asynchronously.
- **Docs:**
  - https://docs.aws.amazon.com/cli/latest/reference/glue/delete-database.html
  - https://docs.aws.amazon.com/cli/latest/reference/athena/delete-work-group.html

### UL-18 (T6, N7)
- **Before:** `delete-cluster workbook-gl18` ran with no check for tasks or services.
- **After:**
  - Criterion: cluster and family `workbook-ul18`, role `workbook-ul18-task`, optional log group `/ecs/workbook-ul18` and security group `workbook-ul18-sg`.
  - Teardown order:
    1. For each service: `update-service --desired-count 0`, then `delete-service --force`, then `aws ecs wait services-inactive`.
    2. For each RUNNING task: `stop-task`, then `aws ecs wait tasks-stopped`.
    3. Deregister every ACTIVE revision in the family (criterion: both revisions).
    4. `delete-cluster`.
    5. Log group.
    6. Security group lookup and delete.
    7. Role loops.
  - Recovery now says what to do on ClusterContainsServices/Tasks errors and on an SG DependencyViolation.
- **Why `--force` is added after scaling to 0:** it makes the delete deterministic while the tasks drain.
- **Docs:**
  - https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeleteCluster.html (ClusterContainsServicesException, ClusterContainsTasksException)
  - https://docs.aws.amazon.com/cli/latest/reference/ecs/delete-service.html
  - https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/services-inactive.html
  - https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/tasks-stopped.html

### UL-19 (T2, N6, N7)
- **Before:**
  - `delete-cluster` / `wait` carried `-ErrorAction`, so they never ran.
  - The node group and Fargate profile were never deleted, so delete-cluster would have failed anyway.
  - Only the gl19 cluster role was removed.
- **After:**
  - Criterion: cluster `workbook-ul19` in the default VPC; role `workbook-ul19-eks`; node group `workbook-ul19-ng` with role `workbook-ul19-node`, or Fargate profile `workbook-ul19-fp` with role `workbook-ul19-fargate`. The criterion also notes that Fargate profiles accept only private subnets, so the default-VPC path is the node group.
  - Teardown order:
    1. For each node group: `delete-nodegroup`, then `aws eks wait nodegroup-deleted`.
    2. For each Fargate profile: `delete-fargate-profile`, then `aws eks wait fargate-profile-deleted`, one at a time.
    3. `delete-cluster`, then `aws eks wait cluster-deleted`.
    4. Cluster log group.
    5. A loop over the three role names. Each existing role is found with `list-roles`, its policies are removed, and the role is deleted.
  - VPC pieces: none. The criteria now require the default VPC, as GL-19 uses, so the lab creates no VPC resources. The EKS cluster SG is removed with the cluster. Verification checks for leftover SGs (`tag:aws:eks:cluster-name`) and running EC2 (`tag:eks:cluster-name`).
  - Recovery covers ResourceInUseException.
- **Docs:**
  - https://docs.aws.amazon.com/cli/latest/reference/eks/delete-cluster.html
  - https://docs.aws.amazon.com/cli/latest/reference/eks/wait/nodegroup-deleted.html
  - https://docs.aws.amazon.com/cli/latest/reference/eks/wait/fargate-profile-deleted.html

### UL-21 (N6, N7)
- **Before:** gl21 names, and both ElastiCache deletes carried `-ErrorAction`, so they never ran.
- **After:**
  - Criterion: cluster and subnet group are both named `workbook-ul21`.
  - Teardown order:
    1. `Remove-Item Env:TF_TOKEN_app_terraform_io`, plus a comment about `terraform logout`. This follows the stopChargesPanel: "remove local terraform tokens".
    2. `delete-cache-cluster`.
    3. `aws elasticache wait cache-cluster-deleted`.
    4. `delete-cache-subnet-group`.
- **Doc:** https://docs.aws.amazon.com/cli/latest/reference/elasticache/wait/cache-cluster-deleted.html

## Needs verification / open

1. **UL-04 tag search.** A KMS key in PendingDeletion may still appear in `resourcegroupstaggingapi get-resources`, which conflicts with the criterion "Tag search LabId=ul-04 is empty". The verification line now notes that exception. AWS should confirm it.
2. **UL-19 tag keys.** The verification filters assume that managed-node EC2 instances carry `eks:cluster-name` and that the cluster SG carries `aws:eks:cluster-name`. AWS should confirm both.
3. **Optional-resource lines without a lookup.** In UL-15 (alarm, trail role), UL-12 (Lambda task role) and UL-19 (the cluster itself), a resource the learner never created prints a harmless NotFound error. A comment says so where it applies.
4. **UL-17 crawler.** A crawler in the RUNNING state cannot be deleted. The teardown does not stop it first. It is listed as optional.
5. **Teacher re-validation** of the wording is still required, including the new naming criterion. Each of the 11 labs now has 16 criteria instead of 15.
