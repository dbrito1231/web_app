# AWS-O9 targeted re-check — commit 1a0b773 (Amendment 3)

Reviewer: Senior AWS Solutions Architect (read-only). Scope: `git show 1a0b773`, cross-checked
against `reports/fix-loop-r2/amendment-3/impl-O9-fix.md`. No AWS calls, no `terraform
plan/apply/destroy`, no servers started. PowerShell verification done in a scratch folder under
the session scratchpad only (local file writes, then deleted).

## Verdicts

### STUDENT-O9-001 (GL-10) — **Gone**

`content/labs/gl-10.json`, step `s09`, bullet 1 now runs `WriteAllText` + `Compress-Archive` to
produce `lambda_function.py` → `function.zip`, matching the `create-function` call's `--handler
lambda_function.lambda_handler` and `--zip-file fileb://function.zip` (both unchanged, and were
already consistent with each other before this fix — only the source filename/content was wrong).

Evidence:
- Re-ran the exact `WriteAllText`/`Compress-Archive` line in a scratch folder: `lambda_function.py`
  written with first bytes `105,109,112` (`imp`, i.e. no BOM); `function.zip` opened with
  `System.IO.Compression.ZipFile` contains exactly one entry, `lambda_function.py`, at the zip
  root — matches `fileb://function.zip` + `--handler lambda_function.lambda_handler` expectations.
- Handler event shape: step `s10` ("Wire SNS to Lambda") subscribes Lambda **directly** to the SNS
  topic (`aws sns subscribe --protocol lambda --notification-endpoint $FunctionArn`) — the SQS
  subscription in `s0x` is a separate fan-out branch, never wired to this Lambda. So the correct
  shape for this specific invocation path is `event['Records'][i]['Sns']['Message']`, which is
  what the handler reads. Confirmed against AWS docs (`search_documentation` /
  `read_documentation`, AWS Knowledge MCP):
  `docs.aws.amazon.com/lambda/latest/dg/example_serverless_SNS_Lambda_section.html` and
  `docs.aws.amazon.com/sns/latest/dg/example_serverless_SNS_Lambda_section.html` — both show the
  identical documented pattern `record['Sns']['Message']` inside `event['Records']`.
- Runtime/handler string (`python3.12`, `lambda_function.lambda_handler`) unchanged and correct.

### STUDENT-O9-002 (GL-06, GL-09, GL-14, GL-18) — **Gone** (for the four named files)

All four flagged step-id references now name the step by title instead of `sNN`:
GL-06 s12, GL-09 s12, GL-14 s12 and s13, GL-18 s13 — verified by reading each diff hunk directly.
A repo-wide grep for `\bs0[0-9]\b|\bs1[0-9]\b` in bullet text (excluding `"id"` fields) confirms
zero remaining matches in these four files.

New finding while sweeping the rest of the labs — see AWS-O9-R-002 below.

### AWS-O9-001 (GL-12) — **Gone**, with one new gap found (AWS-O9-R-001)

- **Log group created and tagged:** `s07` now runs `aws logs create-log-group --log-group-name
  /aws/vendedlogs/states/workbook-gl12 --tags Workbook=aws-tf-lab,LabId=gl-12,...` before
  `create-state-machine`. Verified against
  `docs.aws.amazon.com/cli/latest/reference/logs/create-log-group.html`: `--tags` is documented as
  a **map**, shorthand `KeyName1=string,KeyName2=string` — exactly the syntax used. Log group name
  starts with `/aws/...` (leading slash); the CLI doc's naming rule forbids only a bare `aws/`
  prefix (no leading slash), so this name is valid.
- **`--logging-configuration` JSON shape, level, destination ARN:** `gl12-logging-config.json` is
  `{"level":"ERROR","includeExecutionData":true,"destinations":[{"cloudWatchLogsLogGroup":{"logGroupArn":"<arn>"}}]}`.
  Confirmed against `docs.aws.amazon.com/step-functions/latest/apireference/API_LoggingConfiguration.html`
  (shape/field names) and
  `docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html`
  / `docs.aws.amazon.com/step-functions/latest/apireference/API_CloudWatchLogsLogGroup.html`,
  both of which state the log group ARN **must end in `:*`**. `describe-log-groups` output ARNs
  already carry that suffix, so no string manipulation was needed and none was added — correct.
  Re-ran the `describe-log-groups`→`ConvertTo-Json`→`WriteAllText` line in a scratch folder with a
  stand-in `:*`-suffixed ARN: file written with no BOM, round-tripped through `ConvertFrom-Json`
  with `level=ERROR`, `includeExecutionData=True`, and the ARN intact.
- **Execution role policy covers logging actions:** `s06`'s `gl12-log-policy.json` (unchanged by
  this commit) already grants `logs:CreateLogDelivery`, `CreateLogStream`, `GetLogDelivery`,
  `UpdateLogDelivery`, `DeleteLogDelivery`, `ListLogDeliveries`, `PutLogEvents`,
  `PutResourcePolicy`, `DescribeResourcePolicies`, `DescribeLogGroups` on `Resource: '*'` — this is
  the AWS-documented permission set for Step Functions CloudWatch Logs delivery, and is now
  actually exercised now that logging is enabled.
- **Teardown deletes the log group in the right order:** `orderedDeletesPowerShell` is now
  `delete-state-machine` → `delete-log-group` → `delete-role-policy` → `delete-role` — dependents
  before parents, and `s13` ("Order the deletes") bullet text matches this order.
- **Billing text:** `s12` cost checkpoint now correctly adds CloudWatch Logs per-GB
  ingestion/per-GB-month storage note; `s15` correctly flags the log group as a residual biller
  (unlike the state machine and role, which are genuinely free while idle).
- PS 5.1 AST parse (`[System.Management.Automation.Language.Parser]::ParseInput`) on all three
  changed/added lines in `s07` (create-log-group, describe-log-groups, the logging-config write,
  and the updated create-state-machine call) — 0 parse errors.

**New gap (AWS-O9-R-001):** `s11` ("Prepare delete") still reads "Delete state machine, then IAM
role policy and role." — it was not updated to mention the CloudWatch log group, so it now
disagrees with `s13`'s "state machine, CloudWatch log group, IAM role" and with the corrected
`orderedDeletesPowerShell`. Not a billing risk (the source of truth, `orderedDeletesPowerShell`,
is correct, and `s13` is correct), but it is a stale/incomplete step a student reads before `s13`
and could act on prematurely without deleting the log group. Severity: **Low**.

## New issues found

### AWS-O9-R-001 (Low) — `content/labs/gl-12.json`, step `s11`
`s11` ("Prepare delete") bullet 1 was not updated when the log group was added to the teardown
chain; it still says "Delete state machine, then IAM role policy and role," omitting the log
group that `s13` and `teardown.orderedDeletesPowerShell` both now correctly include. Fix: reword
`s11` bullet 1 to "Delete state machine, then the CloudWatch log group, then the IAM role policy
and role." (or point the student to `s13` for the authoritative order).

### AWS-O9-R-002 (Low) — step-id references remain outside the four labs this commit fixed
The STUDENT-O9-002 defect pattern (raw `sNN` step-id references in student-facing bullet prose)
is not fully swept from the workbook. Found via `grep -rnE "\bs0[0-9]\b|\bs1[0-9]\b"
content/labs/*.json | grep -v '"id"'`:
- `content/labs/gl-16.json:132` — "Teardown order for this lab: the app A record (DELETE change
  batch), zone, VPC. If **s10** already deleted the record, the DELETE returns InvalidChangeBatch
  (not found); continue with the next line" — same defect as the fixed GL-14 s13 bullet
  ("If **s09** already deleted the instance...").
- `content/labs/gl-03.json:84` — "...allowing sts:AssumeRole for your IAM user Arn from **s02**."
  — a milder instance (references where a value comes from, not a teardown-order claim), but the
  same raw-id pattern.

These two files were not in the CR's named scope (`GL-06, GL-09, GL-14, GL-18`), so this is not a
regression from commit `1a0b773`, but the impl report's own verification claim ("no remaining
`s0N`/`s1N` references in bullet prose in any of the six edited files") is scoped only to the
edited files, not the workbook as a whole — worth a follow-up CR for content consistency.

## Overall: concerns

Rationale: all three re-checked items (STUDENT-O9-001, STUDENT-O9-002 for the named labs, and
AWS-O9-001) are genuinely fixed and technically correct against current AWS documentation and
PS 5.1 syntax/execution. The "concerns" verdict is solely because of the two new Low-severity
findings above (a stale GL-12 `s11` bullet the fix should have updated, and the STUDENT-O9-002
pattern persisting in two labs outside this fix's scope) — neither blocks the fixed items, but
both should be logged as follow-up CRs before this amendment is closed out.
