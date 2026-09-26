# Implementation — O9 fix (Amendment 3)

Fixes STUDENT-O9-001, STUDENT-O9-002, and AWS-O9-001. Edited files: `content/labs/gl-06.json`,
`gl-09.json`, `gl-10.json`, `gl-12.json`, `gl-14.json`, `gl-18.json`. All edits made with
`backend\.venv\Scripts\python.exe`, `json.load` / `json.dumps(data, indent=2, ensure_ascii=True) +
"\n"`, UTF-8 text mode. Helper script: `scratchpad/fix_o9.py` (session scratchpad, not committed).

## STUDENT-O9-001 (Medium) — `content/labs/gl-10.json`, step `s09`

**Before:** bullet 1 read "Zip gl10_lambda.py as function.zip with a handler that logs the event."
with no PowerShell line writing the file, and the filename didn't match the `--handler
lambda_function.lambda_handler` flag already on the `create-function` call.

**After:** bullet 1 is now a `WriteAllText` + `Compress-Archive` line (GL-08/GL-11 pattern) that
writes `lambda_function.py` (matching `--handler lambda_function.lambda_handler`) and zips it to
`function.zip`. The `create-function` bullet (`--zip-file fileb://function.zip`) is unchanged
because the zip name already matched; only the source file name and its content changed.

Handler logic: GL-10's Lambda is invoked directly by SNS (`s10` subscribes Lambda to the SNS topic
with `aws sns subscribe --protocol lambda`), not through the SQS queue (SQS is a separate fan-out
subscriber, never wired to Lambda). So the handler reads `event['Records'][*]['Sns']['Message']`,
prints each message, and returns a record count — this is what shows up when `s11` runs `aws logs
tail /aws/lambda/workbook-gl10 --since 5m` after `aws sns publish`.

```python
import json

def lambda_handler(event, context):
    records = event.get('Records', [])
    for record in records:
        message = record.get('Sns', {}).get('Message', '')
        print('Received SNS message: ' + str(message))
    return {'recordCount': len(records)}
```

Verified against AWS docs:
- `docs.aws.amazon.com/lambda/latest/dg/example_serverless_SNS_Lambda_section.html` — SNS event
  shape delivered to Lambda is `event['Records'][i]['Sns']['Message']` (confirmed via
  `search_documentation`/`read_documentation`, AWS Knowledge MCP).
- `--handler lambda_function.lambda_handler` and `python3.12` runtime format were already correct
  on the `create-function` call; only the source file needed to match.

## STUDENT-O9-002 (Low) — internal step-ids in student-facing text

Reworded every "step s0N"/"s0N" reference found by grepping `\bs0[0-9]\b|\bs1[0-9]\b` inside
bullet text (not `"id"` fields) across the four flagged labs, naming the step by its visible title
instead:

| File | Step | Before | After |
| --- | --- | --- | --- |
| `gl-06.json` | s12 | "...releasing the EIP in step s11 is what stops that charge..." | "...releasing the EIP in the Delete NAT and release EIP step is what stops that charge..." |
| `gl-09.json` | s12 | "...the ASG resource still exists until you delete it in step s10." | "...the ASG resource still exists until you delete it in the Delete ASG step." |
| `gl-14.json` | s12 | "...so only deletion in s09 stops the meter." | "...so only deletion in the Delete without final snapshot step stops the meter." |
| `gl-14.json` | s13 | "If s09 already deleted the instance..." | "If the Delete without final snapshot step already deleted the instance..." (found via the same grep sweep; not in the original report table but same defect pattern, same batch) |
| `gl-18.json` | s13 | "...but s10 deregisters this one for tidiness." | "...but the Deregister task definition step deregisters this one for tidiness." |

Re-ran the grep after editing; no remaining `s0N`/`s1N` references in bullet prose in any of the
six edited files (only in `"id": "sNN"` step fields, which are not student-facing).

## AWS-O9-001 (Low) — `content/labs/gl-12.json`, step `s07`

**Before:** `s06` wrote and attached `gl12-log-policy.json` (CloudWatch Logs permissions) to the
execution role, but `s07`'s `create-state-machine` call never passed `--logging-configuration`, so
the state machine ran with logging off and the role's log permissions were never exercised.

**After (Fix (a) from AWS-O9's suggested fix — enable logging rather than drop the policy):**
`s07` now, before calling `create-state-machine`:
1. Creates a dedicated log group: `aws logs create-log-group --log-group-name
   /aws/vendedlogs/states/workbook-gl12 --tags Workbook=aws-tf-lab,LabId=gl-12,...` (tagged
   `LabId=gl-12` per the amendment's instruction).
2. Captures its ARN: `$LogGroupArn = aws logs describe-log-groups --log-group-name-prefix
   /aws/vendedlogs/states/workbook-gl12 --query "logGroups[0].arn" --output text`.
3. Writes `gl12-logging-config.json` — `{"level":"ERROR","includeExecutionData":true,
   "destinations":[{"cloudWatchLogsLogGroup":{"logGroupArn":"<arn>"}}]}` — via a PowerShell
   hashtable piped to `ConvertTo-Json`, same pattern as `gl12.asl.json`.
4. `create-state-machine` now includes `--logging-configuration
   file://gl12-logging-config.json`.

Also updated for consistency:
- `stopChargesPanel`: now mentions the log group.
- `s12` cost checkpoint: adds the per-GB ingestion / per-GB-month storage note for the
  ERROR-level execution logs.
- `s13` "Order the deletes": now lists state machine → CloudWatch log group → IAM role.
- `s15`: notes the log group can still bill if left behind.
- `teardown.orderedDeletesPowerShell`: inserted `aws logs delete-log-group --log-group-name
  /aws/vendedlogs/states/workbook-gl12` between the state-machine delete and the role-policy
  delete (dependents before parents, matching the reworded `s13` text).

Verified against AWS docs (AWS Knowledge MCP `search_documentation` / `read_documentation`):
- `docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html` — `LoggingConfiguration` is passed
  to `CreateStateMachine`; Standard Workflows are not logged by default via API/CLI, matching this
  lab's previous (broken) state.
- `docs.aws.amazon.com/step-functions/latest/apireference/API_LoggingConfiguration.html` —
  `destinations` (array, max 1), `includeExecutionData` (bool), `level` (`ALL|ERROR|FATAL|OFF`).
  Used `level=ERROR` per the amendment instruction ("ERROR or ALL").
  `docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html`
  — confirms the destination ARN must be a CloudWatch Logs log group ARN ending in `:*`, which
  `describe-log-groups` already returns for a log group ARN, so no string manipulation was added.
- `docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateLogGroup.html` —
  `tags` is a flat string-to-string map, confirming the `--tags Key=Value,Key=Value` CLI shorthand
  used (log group names starting with `/aws/...` are allowed; only a bare leading `aws/` without
  the slash is disallowed).
- The existing `gl12-log-policy.json` (unchanged) already grants exactly the actions AWS's
  documented example lists (`logs:CreateLogDelivery`, `CreateLogStream`, `GetLogDelivery`,
  `UpdateLogDelivery`, `DeleteLogDelivery`, `ListLogDeliveries`, `PutLogEvents`,
  `PutResourcePolicy`, `DescribeResourcePolicies`, `DescribeLogGroups`), so those permissions are
  now genuinely used.

## Verification

- **PS 5.1 AST parse** (`[System.Management.Automation.Language.Parser]::ParseInput`) — every new
  or changed PowerShell line in `gl-10.json` (`s09` write+zip, unchanged `create-function`) and
  `gl-12.json` (`create-log-group`, `describe-log-groups`, `create-state-machine` with
  `--logging-configuration`, teardown `delete-log-group`) parsed with zero errors.
- **Real execution in a scratch folder** (PowerShell tool, temp dirs under the session
  scratchpad, deleted after the run):
  - GL-10 write+zip line executed for real: `lambda_function.py` written with no BOM (first
    bytes `105,109,112` = `imp`, i.e. plain UTF-8 ASCII), valid Python; `function.zip` opened
    with `System.IO.Compression.ZipFile` — contains exactly one entry, `lambda_function.py`, at
    the zip root.
  - GL-12 logging-config write line executed for real with a stand-in ARN: file written with no
    BOM (first bytes `123,34,100` = `{"d`), parsed back with `ConvertFrom-Json` —
    `level=ERROR`, `includeExecutionData=True`,
    `logGroupArn=arn:aws:logs:us-east-1:123456789012:log-group:/aws/vendedlogs/states/workbook-gl12:*`
    round-tripped correctly.
- **`python scripts\content_lint.py`** — `PASS` (`questions 429 aws 310 tf 119`, `labs 21 + 21`,
  `lessons 23`).
- **`python scripts\scan_lab_placeholders.py`** — `PASS 42 labs scanned`.
- All six edited JSON files re-parsed with `json.load` after editing — valid JSON, no syntax
  errors introduced by the `WriteAllText`/`ConvertTo-Json` escaping.

## Not changed

- GL-11 (already fixed under this same amendment; used as the pattern reference for GL-10).
- `gl12-log-policy.json` contents (already a byte-for-byte match of AWS's documented policy; the
  fix wires it up rather than replacing it, per AWS-O9's suggested fix (a)).
- No AWS calls were made, no `terraform plan`/`apply`/`destroy` was run, and `git`/`git stash`
  were not used.

## Leftovers — AWS-O9-R-001 / AWS-O9-R-002 (Amendment 3 follow-up)

Fixes `reports/fix-loop-r2/amendment-3/AWS-O9-recheck.md` findings AWS-O9-R-001 and
AWS-O9-R-002. Edited files: `content/labs/gl-03.json`, `gl-12.json`, `gl-16.json`. Same
`backend\.venv\Scripts\python.exe` / `json.load` / `json.dumps(data, indent=2,
ensure_ascii=True) + "\n"` / UTF-8 text-mode process as above. No `git`, no AWS calls, no
`terraform plan`/`apply`/`destroy`.

### AWS-O9-R-001 (Low) — `content/labs/gl-12.json`, step `s11`

**Before:** "Delete state machine, then IAM role policy and role."

**After:** "Delete state machine, then the CloudWatch log group, then the IAM role policy and
role."

Now matches `s13` ("state machine, CloudWatch log group, IAM role") and
`teardown.orderedDeletesPowerShell` (state machine → log group → role policy → role).

### AWS-O9-R-002 (Low) — raw step-ID references in student-facing text

| File | Step | Before | After |
| --- | --- | --- | --- |
| `gl-16.json` | s13 | "...If s10 already deleted the record, the DELETE returns InvalidChangeBatch..." | "...If \"Delete record\" already deleted the record, the DELETE returns InvalidChangeBatch..." |
| `gl-16.json` | s10 | "...A DELETE must repeat the exact name, type, TTL, and value from s08." | "...A DELETE must repeat the exact name, type, TTL, and value from \"Private record\"." (found in this batch's own sweep, not in the recheck report's two named lines, same defect pattern) |
| `gl-03.json` | s07 | "Save gl03-trust.json allowing sts:AssumeRole for your IAM user Arn from s02." | "Save gl03-trust.json allowing sts:AssumeRole for your IAM user Arn from \"Confirm who is signed in\"." |

**Full-workbook scan** (`grep -rnE "\bs0[0-9]\b|\bs1[0-9]\b" content/labs/*.json | grep -v
'"id"'`), run before and after the edits above:

- Before: 3 matches — `gl-16.json:132` (s10, in s13's bullet), `gl-16.json:105` (s08, in s10's
  bullet — not named in the recheck report but caught by the same grep pattern), and
  `gl-03.json:84` (s02, in s07's bullet).
- After: 0 matches. All three were inside the three files this task was scoped to, so no
  out-of-scope leftovers to report.

### Verification

- `python scripts\content_lint.py` — `PASS` (`questions 429 aws 310 tf 119`, `labs 21 + 21`,
  `lessons 23`).
- `python scripts\scan_lab_placeholders.py` — `PASS 42 labs scanned`.
- `gl-03.json`, `gl-12.json`, `gl-16.json` re-serialized with `json.load`/`json.dumps` after
  editing; `git diff` confirms only the intended bullet-text lines changed (no reordering, no
  stray whitespace).
