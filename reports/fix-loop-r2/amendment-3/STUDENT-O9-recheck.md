# Student re-check — O9 fixes (Amendment 3)

Reviewer: College IT Student (read-only). Basic IT background, not an AWS expert. Re-checked the
fixes described in `reports/fix-loop-r2/amendment-3/impl-O9-fix.md` (commit `1a0b773` plus the
"O9 leftovers" commit) by opening each named lab card in the running app
(`http://127.0.0.1:5173`, Labs tab) and reading it top to bottom, the way I did for the original
review. No commands run, no files edited, no Reset/Import/Check-answers clicked.

Scope: GL-10 (STUDENT-O9-001), GL-06/GL-09/GL-14/GL-18/GL-03/GL-16 (STUDENT-O9-002), GL-12
(AWS-O9-001 logging clarity + cleanup order).

## 1. STUDENT-O9-001 — GL-10 Lambda file step

**Verdict: Gone.**

Step 9 ("Create Lambda function") now reads:

> Run `$utf8 = New-Object System.Text.UTF8Encoding $false; [IO.File]::WriteAllText("$pwd\lambda_function.py", ...); Compress-Archive -Path lambda_function.py -DestinationPath function.zip -Force`. This writes a handler that reads the SNS records this lab's subscription delivers, logs each message, and returns a record count, with LF endings and no BOM, then zips it to function.zip.

followed by `aws lambda create-function ... --handler lambda_function.lambda_handler --zip-file
fileb://function.zip`. The file it tells me to write (`lambda_function.py`) now matches the
`--handler` flag, and the write+zip command is spelled out the same way GL-11 does it. I could
follow this step and end up with a zip that actually contains what `create-function` expects.

## 2. STUDENT-O9-002 — internal step-ids in student-facing text

**Verdict: Gone in all six labs checked.**

| Lab | Step | Text now reads |
| --- | --- | --- |
| GL-06 | 12 (cost checkpoint) | "...releasing the EIP in **the Delete NAT and release EIP step** is what stops that charge..." |
| GL-09 | 12 (cost checkpoint) | "...the ASG resource still exists until you delete it in **the Delete ASG step**." |
| GL-14 | 12 (cost checkpoint) | "...so only deletion in **the Delete without final snapshot step** stops the meter." |
| GL-14 | 13 (order the deletes) | "If **the Delete without final snapshot step** already deleted the instance, delete-db-instance reports DBInstanceNotFound..." |
| GL-18 | 13 (order the deletes) | "...but **the Deregister task definition step** deregisters this one for tidiness." |
| GL-03 | 7 (create IAM role) | "Save gl03-trust.json allowing sts:AssumeRole for your IAM user Arn from **"Confirm who is signed in"**." |
| GL-16 | 10 (delete record) | "A DELETE must repeat the exact name, type, TTL, and value from **"Private record"**." |
| GL-16 | 13 (order the deletes) | "If **"Delete record"** already deleted the record, the DELETE returns InvalidChangeBatch..." |

I did not find any bare "s0N"/"s1N" reference left in the on-screen text of GL-06, GL-09, GL-14,
GL-18, GL-03, or GL-16. Every reference now names the step the way it appears on screen (either a
plain step title in prose, or the title in quotes), so I don't have to go count steps to figure out
what's being pointed at. This is a strict improvement over the version I reviewed before.

## 3. GL-12 — logging policy payoff and cleanup order

**Verdict: Clear now, and cleanup order is consistent everywhere.**

Step 6 still writes and attaches `gl12-log-policy.json`, but now step 7 also:
- creates a dedicated log group (`aws logs create-log-group --log-group-name
  /aws/vendedlogs/states/workbook-gl12 ...`),
- reads its ARN back,
- writes a `gl12-logging-config.json` (ERROR level, execution data included, one CloudWatch Logs
  destination),
- and passes `--logging-configuration file://gl12-logging-config.json` on the
  `create-state-machine` call, with "Success: state machine Arn is set and logging is enabled."

So this time the permission policy from step 6 is actually used one step later — I don't have to
wonder where the payoff went. The cost checkpoint (step 12) now also explicitly says "CloudWatch
Logs bills per-GB for log ingestion and per-GB-month for storage of the ERROR-level execution logs
this lab now enables," which answers the "why does this cost anything" question up front.

Cleanup order is consistent everywhere I can see it on this card:
- Step 11 ("Prepare delete"): "Delete state machine, then the CloudWatch log group, then the IAM
  role policy and role."
- Step 13 ("Order the deletes"): "state machine, CloudWatch log group, IAM role."
- Stop-charges summary line: "Delete state machine, its CloudWatch log group, and the IAM role
  used by Step Functions."
- Teardown PowerShell block: `delete-state-machine` → `delete-log-group` →
  `delete-role-policy` → `delete-role`, in that order.

All four places agree with each other and with dependents-before-parents ordering (the thing
using the log group is deleted before the log group, and the thing granting the role's logging
permission is deleted before the role itself). No mismatch found.

## New issues found

None. I did not find any new problems in the eight lab cards checked (GL-10, GL-06, GL-09, GL-14,
GL-18, GL-03, GL-16, GL-12).

## O9: close

## Overall: approve
