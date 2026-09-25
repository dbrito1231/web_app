# Batch F2 implementation log

Scope: `content/labs/ul-01.json`, `ul-02.json`, `ul-03.json`, `ul-04.json`, `ul-07.json`, `ul-08.json`, `ul-09.json`. No other files touched, no AWS calls made.

## Changes

- **ul-01.json** (TEACHER-R3-002): replaced the fixed-name `delete-role-policy` lines with a `list-role-policies` loop per role (same pattern as UL-03), so teardown works regardless of the inline policy name the learner chose. Also applied TEACHER-R3-014: line 2 changed from "Lost an ID?" to "Lost track? List what is left: ..." since `# Uses: none`.
- **ul-02.json** (TEACHER-R3-003): added a new first acceptance criterion naming the bucket `workbook-ul02-<account-id>` (or the reused GL-02 bucket). Reworded the `# Uses:` comment and changed the bucket assignment to `if (-not $Bucket) { $Bucket = "workbook-ul02-$(...)" }` so a pre-set `$Bucket` (reused GL-02 bucket) is respected.
- **ul-03.json** (TEACHER-R3-011): removed the duplicate criterion "All tagged resources use LabId=ul-03." (already covered by the C1 naming criterion). 16 -> 15 criteria.
- **ul-04.json** (TEACHER-R3-011, item 4): removed the duplicate criterion "LabId=ul-04 on all tagged resources." Reworded the final tag-search criterion to "Tag search LabId=ul-04 shows only the KMS key, in PendingDeletion." to match the verification note and AWS-R3-006.
- **ul-07.json** (STUDENT-R3-004): added a first criterion naming the resources `workbook-ul07` (file system, EC2 instance, mount-target SG, instance SG). Kept the `# Uses:` teardown variables; added the names to the "Lost an ID?" comment.
- **ul-08.json** (STUDENT-R3-004, TEACHER-R3-012): added a first criterion naming the resources `workbook-ul08` (ALB, target group, VPC, SG, WAF web ACL). Kept the `# Uses:` teardown variables; added the names to the "Lost an ID?" comment. Recovery text now matches GL-08 wording exactly: "...wait 1–2 minutes and rerun Stop charges from that line." Hint level 3 changed `curl` to `curl.exe`.
- **ul-09.json**: guarded the ASG instance-wait line against the literal string `None` (`if ($AsgInstanceIds -and $AsgInstanceIds -ne 'None')`), per AWS-R3-008.

## Checks

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23 / PASS`
- `backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py` → `PASS 42 labs scanned`
- Every changed `orderedDeletesPowerShell` line for all 7 files parsed cleanly with `[System.Management.Automation.Language.Parser]::ParseFile` (no syntax errors).

## Unresolved / out of scope

- None of the 8 assigned items were skipped. Item 8 (TEACHER-R3-014, "# Uses: none" line-2 wording) applied only to ul-01, since ul-02/03/04/07/08/09 either already use real variables or were not `# Uses: none` labs.
- TEACHER-R3-011's other affected labs (UL-10, 13, 15, 17, 18, 19, 21) and TEACHER-R3-004/005/etc. are out of scope for F2 (assigned to batch F3).
