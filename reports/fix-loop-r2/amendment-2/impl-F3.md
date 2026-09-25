# Implementer log: Batch F3 (Amendment 2, round-3 fixes)

Scope: `content/labs/ul-10.json` through `ul-21.json` only.

## Changes by lab

- **ul-10**: removed duplicate tag criterion (TEACHER-R3-011). Teardown: SNS topic ARN is now built from `$AccountId` (`aws sts get-caller-identity`) instead of a paginated `list-topics | [0]` lookup; DynamoDB table lookup switched to `describe-table` (AWS-R3-001). R3-014 header line reworded.
- **ul-11**: reworded C10 to "Teardown deletes the API (this removes its authorizer, routes, integrations and stages)" (TEACHER-R3-004). `curl` → `curl.exe` in hint 2 and criterion 14 (AWS-R3-010). Teardown: `get-apis`/`list-user-pools` `| [0]` lookups switched to `--output json | ConvertFrom-Json`; auth-Lambda lookup switched to direct `get-function` (AWS-R3-001). R3-014 header line reworded.
- **ul-12**: C1 now names the log group `/aws/vendedlogs/states/workbook-ul12` (TEACHER-R3-009). Teardown: state-machine ARN built from `$AccountId` instead of paginated `list-state-machines | [0]`; task-Lambda lookup switched to direct `get-function` (AWS-R3-001). R3-014 header line reworded.
- **ul-13**: removed duplicate tag criterion (TEACHER-R3-011). R3-014 header line reworded.
- **ul-14**: no changes (not in scope of any listed issue).
- **ul-15**: restored C3 as a distinct CloudTrail criterion ("Trail `workbook-ul15` logs management events to the ul-15 bucket"), replacing the duplicate of C2 (TEACHER-R3-001). Removed the separate duplicate tag criterion (TEACHER-R3-011). R3-014 header line reworded.
- **ul-16**: split the DELETE-record one-liner into four commented, guarded steps (TEACHER-R3-006). Added a comment to delete subnets/SGs before `delete-vpc`, and guarded `delete-vpc` with an `IsDefault` check via a `$NotDefaultVpc` boolean so the guard stays lint-clean (TEACHER-R3-007, AWS-R3-007).
- **ul-17**: removed duplicate tag criterion (TEACHER-R3-011). Teardown: workgroup/crawler lookups switched to direct `get-work-group`/`get-crawler` calls instead of paginated `list-*` + `| [0]` (AWS-R3-001). R3-014 header line reworded.
- **ul-18**: removed duplicate tag criterion (TEACHER-R3-011). Security-group lookup now also filters on `tag:LabId=ul-18` (AWS-R3-011). R3-014 header line reworded.
- **ul-19**: removed the design-forcing clause from C1 ("...so in the default VPC use the node group path") and moved that fact into a new hint, so C1 no longer contradicts C3/scenario's Fargate-or-node-group choice (TEACHER-R3-005). Removed duplicate tag criterion (TEACHER-R3-011). Split the nested-loop IAM cleanup into one guarded 4-line block per role (eks/node/fargate) (TEACHER-R3-008). R3-014 header line reworded.
- **ul-20**: moved the `head-bucket` check out of the teardown into verification, and added a note explaining the GL-20 tag check is only relevant if the GL-20 bucket was imported (TEACHER-R3-015). Teardown line1 uses named variables, not "# Uses: none", so R3-014 did not apply.
- **ul-21**: made `terraform logout app.terraform.io` an actual command line (previously only a comment) (TEACHER-R3-010). Removed duplicate tag criterion (TEACHER-R3-011). R3-014 header line reworded.

## R3-014 ("Lost track? List what is left")

Applied to every teardown in this batch whose line 1 is `# Uses: none …`: ul-10, ul-11, ul-12, ul-13, ul-15, ul-17, ul-18, ul-19, ul-21. Not applied to ul-14, ul-16, ul-20 (their line 1 names real variables, not "none").

## Verification

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23 / PASS`.
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → the current (in-flight, being edited by another batch in parallel) scanner reports failures only in `gl-*` and `ul-07` files, none of which this batch touched; **zero** findings for `ul-10` through `ul-21`.
- Every line in the 12 files' `orderedDeletesPowerShell` (154 lines total) was parsed with `[System.Management.Automation.Language.Parser]::ParseInput` in PowerShell 5.1 — 0 parse errors.
- No `-ErrorAction` on any `aws` line, no `= $null`/self-assignment, no `workbook-gl` names introduced.

## Unresolved / notes for reviewers

- The scanner's `_guard_covers` check only recognizes `-ne` comparisons inside a guard term, not `-eq`. The AWS report's literal suggested fix for UL-16 (`... -eq 'False'`) fails that check, so it was rewritten as a separate `$NotDefaultVpc = ($IsDefault -eq 'False')` line, then guarded as `if ($VpcId -and $NotDefaultVpc)`. Same intent, lint-clean.
- UL-19's `$R` nested-loop `iam list-roles ... | [0]` pattern (AWS-R3-001's "UL-19 L11 is harmless") was left unchanged per the report's own note, and was preserved (now duplicated three times as `$EksRole`/`$NodeRole`/`$FargateRole` lookups) rather than converted to a direct-get pattern, since IAM has no "does this role exist" get-by-name call cheaper than `get-role` itself — `get-role` would have been an equally valid and slightly simpler alternative but was not required by the fix list, so the existing `list-roles | [0]` shape was kept to minimize unrelated diff.
- Did not touch `content/labs/ul-14.json`, `gl-*.json`, or `ul-07.json` — outside this batch's assigned scope even though the currently-in-progress (uncommitted) `scripts/scan_lab_placeholders.py` now flags pre-existing patterns in those files.
