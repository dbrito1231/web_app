# O9-B implementation report — GL-11 through GL-21

Batch O9-B per Amendment 3 (`.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`), fixing
TEACHER-209 (missing sidecar templates) and TEACHER-210 (shared s12–s15 boilerplate) from
`reports/02-teacher.md`. Files touched: `content/labs/gl-11.json` … `gl-21.json` only. No git
commands run, no `aws` calls, no edits to `lab-fixtures/gl-20/main.tf`.

## TEACHER-209 — sidecar files

| Lab | `file://` name | Was written already? | Action |
| --- | --- | --- | --- |
| GL-11 | `gl11-trust.json` | No | Added `[IO.File]::WriteAllText` bullet in s06 writing the Lambda trust policy (`Principal.Service = lambda.amazonaws.com`), UTF-8 no BOM, before `create-role`. |
| GL-11 | `function.zip` (via `--zip-file fileb://function.zip`) | No | Added a bullet in s06 that writes `lambda_function.py` (LF, no BOM) then `Compress-Archive -Force` to `function.zip`, before `create-function`. |
| GL-12 | `gl12-trust.json` | No | Added a bullet in s06 writing the Step Functions trust policy (`Principal.Service = states.amazonaws.com`), before `create-role`. |
| GL-12 | `gl12-log-policy.json` | No | Added a bullet in s06 writing the AWS-documented CloudWatch Logs permission set for Step Functions execution roles, before `put-role-policy`. |
| GL-12 | `gl12.asl.json` | No (prose only: "Save gl12.asl.json...") | Replaced the prose bullet in s07 with a `WriteAllText` bullet building the ASL (`Pass` → `Succeed`) via a PowerShell hashtable piped through `ConvertTo-Json -Depth 10 -Compress`. |
| GL-13 | — | n/a | No `file://` references; not touched. |
| GL-14 | — | n/a | No `file://` references; not touched. |
| GL-15 | — | n/a | No `file://` references; not touched. |
| GL-16 | `gl16-record.json`, `gl16-record-delete.json` | Yes (already `WriteAllText`, UTF-8 no BOM) | No sidecar change needed. |
| GL-17 | — | n/a (writes `gl17.csv` already) | No sidecar change needed. |
| GL-18 | `gl18-trust.json` | No | Added a bullet in s06 writing the ECS task trust policy (`Principal.Service = ecs-tasks.amazonaws.com`), before `create-role`. |
| GL-18 | `gl18-task.json` | No (prose only: "Save gl18-task.json...") | Replaced the prose bullet in s07 with a `WriteAllText` bullet building a Fargate task definition (`family`, `networkMode=awsvpc`, `requiresCompatibilities=[FARGATE]`, `cpu=256`, `memory=512`, `executionRoleArn=$TaskRoleArn`, one container `hello-world`), before `register-task-definition`. |
| GL-18 | `network.json` | Partially — s08 already wrote it via `Set-Content -Encoding ascii`, but the referenced `$SubnetId` variable was **never set anywhere in the lab** (a real defect: the `awsvpc` network configuration would ship a null subnet). | Rewrote s08 to (1) resolve `$VpcId`/`$SubnetId` from the default VPC first, then (2) write `network.json` with the `WriteAllText` UTF-8-no-BOM pattern instead of `Set-Content -Encoding ascii`, keeping the same JSON shape. |
| GL-19 | `gl19-eks-trust.json` | No | Added a bullet in s06 writing the EKS cluster trust policy (`Principal.Service = eks.amazonaws.com`), before `create-role`. |
| GL-20 | — | n/a | No `file://` references (Terraform lab); not touched, fixture untouched. |
| GL-21 | — | n/a | No `file://` references; not touched. |

All new JSON bodies were checked against AWS docs fetched with WebFetch:
- Lambda / generic IAM trust policy grammar: `docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html`, `docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html`
- Step Functions ASL structure (`StartAt`/`States`/`Type`/`Next`/`End`): `docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-state-machine-structure.html`
- Step Functions execution-role trust policy (`states.amazonaws.com`) and CloudWatch Logs permission set: `docs.aws.amazon.com/step-functions/latest/dg/procedure-create-iam-role.html`, `docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html`
- ECS task-definition parameters (Fargate required fields): `docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html`
- ECS task execution-role trust policy (`ecs-tasks.amazonaws.com`): `docs.aws.amazon.com/AmazonECS/latest/developerguide/task-execution-IAM-role.html`
- EKS cluster IAM role trust policy (`eks.amazonaws.com`): `docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html`

## TEACHER-210 — s12–s15 per lab

For every lab in this batch, s12 ("Cost checkpoint") was rewritten to name the actual billing
model (hourly per-instance/node/cluster-hour vs. per-request/per-GB-month/free) and the generic
"Stopping an instance or scaling to zero is not teardown" line was removed from labs with no
stoppable instance (GL-11, 12, 13, 15, 16, 17, 20); it was kept only implicitly via lab-specific
wording for GL-14 (RDS), GL-18 (Fargate task RUNNING/STOPPED), GL-19 (EKS control plane cannot be
stopped), GL-21 (ElastiCache has no stop feature). s13's first bullet was corrected to match the
lab's actual teardown order for GL-11 (added the CloudWatch log group step) and GL-18 (removed the
implication that the teardown deletes the task definition, since `teardown.orderedDeletesPowerShell`
never touches it — task definitions cost nothing to leave registered). s15's last bullet now names
the specific resource(s) that keep billing if teardown is interrupted. s14 and the
`aws resourcegroupstaggingapi` success/verification lines were left unchanged in every lab, per
the "keep the success lines and the tag-search verification" instruction. GL-20's Terraform steps
were left consistent with `lab-fixtures/gl-20/main.tf` (not touched).

Example (GL-14, RDS, hourly): s12 now reads "RDS bills per instance-hour for db.t3.micro plus per
GB-month of allocated storage and backups; stopping an instance still bills for storage, so only
deletion in s09 stops the meter," replacing the previous lab-agnostic phrasing.

## Verification

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `PASS` (questions 429, aws 310, tf 119, labs 21+21, lessons 23).
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → `PASS 42 labs scanned`.
- Every new/changed PowerShell snippet (10 distinct file-writing lines across GL-11, GL-12, GL-18, GL-19) was parsed with
  `[System.Management.Automation.Language.Parser]::ParseInput(...)` (PS 5.1 AST) — zero parse errors.
- Each file-writing line was executed for real in a scratch folder
  (`…/scratchpad/o9b_exec2`), producing `gl11-trust.json`, `lambda_function.py` + `function.zip`,
  `gl12-trust.json`, `gl12-log-policy.json`, `gl12.asl.json`, `gl18-trust.json`, `gl18-task.json`,
  `network.json`, `gl19-eks-trust.json`. All JSON files were loaded with `json.loads` and confirmed
  to start without a UTF-8 BOM; `function.zip` was opened with `zipfile` and confirmed to contain
  exactly `lambda_function.py` with the expected handler text.
- `git diff --stat` on `content/labs/gl-11.json` … `gl-21.json` shows only the 11 files in scope
  changed, no `lab-fixtures/**` changes, and `gl-01.json`–`gl-10.json` (owned by the parallel O9-A
  agent) are untouched by this session.

## Follow-ups (not fixed here, out of O9-B's file scope)

- GL-18's `$SubnetId` bug (undefined variable feeding `network.json`) was fixed as part of making
  the sidecar valid, since an unset subnet would make the `awsvpc` network configuration invalid
  for the AWS API — this was necessary to satisfy "the content must be valid for the AWS API," not
  an optional extra.
