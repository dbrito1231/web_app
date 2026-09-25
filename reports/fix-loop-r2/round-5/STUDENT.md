# Student review — round 5

Reviewer: College IT Student persona (read-only). No files edited, no server started beyond the
already-running dev server, no Reset/Import/Check answers clicked, no `aws` run. Labs were read
from the rendered card in the Labs tab (`http://127.0.0.1:5173/labs?lab=<id>`) and cross-checked
against `content/labs/*.json`. Screens were exercised in the built-in browser at
`http://127.0.0.1:5173`.

## STUDENT-R4-001 to 004 — confirmed Gone

| ID | Round-4 issue | Round-5 check | Status |
| --- | --- | --- | --- |
| STUDENT-R4-001 | UL-16 had no "Name the resources you create" naming criterion | Criterion #1 now reads "Name the resources you create `workbook-ul16`: private hosted zone `workbook-ul16` and, if you create one, VPC `workbook-ul16`. Tag each one LabId=ul-16." Confirmed rendered on the card. | **Gone** |
| STUDENT-R4-002 | UL-16 teardown had only a comment telling the student to delete subnets/SGs before `delete-vpc`, no real command | Teardown now runs `describe-vpcs` to check `IsDefault`, then real `foreach` loops that `delete-subnet` and `delete-security-group` for every subnet/SG in `$VpcId`, guarded by `$NotDefaultVpc`, before `delete-vpc`. Confirmed rendered on the card. | **Gone** |
| STUDENT-R4-003 | UL-21 ran `elasticache delete-cache-cluster` / `delete-cache-subnet-group` unconditionally even on the HCP-only path | Both lines (plus the new `wait cache-cluster-deleted`) are now wrapped in `if ($AwsPath) { ... }`, with a leading comment explaining "$AwsPath (optional — set it only if you built the AWS ElastiCache half; unset, the AWS lines below are skipped)". | **Gone** |
| STUDENT-R4-004 | GL-17 step s09 body ran `DROP TABLE gl17.sample` (no `IF EXISTS`) while the teardown block used `IF EXISTS` | Step s09 now reads `DROP TABLE IF EXISTS gl17.sample` and `DROP DATABASE IF EXISTS gl17`, matching the teardown block. | **Gone** |

## Part 1 — per-lab table

| Lab | Followable top to bottom? | Confusing points | Notes / quotes |
| --- | --- | --- | --- |
| UL-02 | Yes | The new bucket-safety check repeats the same `if ($Ul02BucketLabId -eq 'ul-02' -or $Ul02BucketLabId -eq 'gl-02')` condition on 6 separate lines instead of one guard wrapping a block. Verbose, but each line reads on its own and a student typing them one at a time won't be confused — it's just longer than it needs to be. | "Skipping ${Ul02Bucket}: LabId tag is not ul-02 or gl-02" is a clear, plain-English message if the check fails. |
| UL-11 | Yes | **New issue** — see STUDENT-R5-001 below: the Cognito user-pool-domain line is advice in a comment only, not a command. | Everything else (API delete, Lambda x2, log groups x2, user pool, IAM role loops) reads in dependency order and is easy to follow. |
| UL-16 | Yes | None found this round — the VPC cleanup gap from round 4 is fixed. | "Never delete the default VPC" comment plus the `$NotDefaultVpc` check makes it clear a student who reused the default VPC is automatically skipped. |
| UL-19 | Yes | Long, but the three-role IAM cleanup (`$EksRole` / `$NodeRole` / `$FargateRole`) each get their own existence check, so a student who only built the node-group path isn't confused by the Fargate role lines — they just no-op. | Recovery text explicitly says what `ResourceInUseException` on `delete-cluster` means and what to rerun. |
| UL-21 | Yes | None found this round — the AWS-path guard gap from round 4 is fixed. | `terraform logout` comment correctly warns that logout only removes the *local* token copy and does not revoke it — a student could otherwise think they're done. |
| GL-17 | Yes | None found this round — the `IF EXISTS` wording mismatch from round 4 is fixed. | The capped wait loops read as "try up to 60 times, 2 seconds apart" and each has a plain `Write-Host 'Timed out waiting for DROP TABLE/DATABASE to finish after 60 tries; check the Athena console'` if they give up — a student would understand this means "go look at the console, don't panic." |
| GL-19 | Yes | None found | Short, four-line teardown; cluster delete then role cleanup, in the order the "Order the deletes" step (s13) describes. |
| UL-07 | Yes | The capped mount-target wait loop reads the same way as GL-17's: "wait 10s, check again, up to 60 tries" with `Write-Host 'Timed out waiting for EFS mount targets to delete after 60 tries; check the EFS console before deleting the file system'` if it gives up. Clear and matches the recovery note ("If delete-file-system returns FileSystemInUse, wait a minute and rerun the mount-target poll line"). | None found |

**"Gave up after 60 tries" messages** (GL-17 x2, UL-07 x1): all three read the same way and all name
the specific thing to go check (Athena console, EFS console) rather than just failing silently.
This pattern is consistent and understandable.

## New issues (Low+)

| ID | Severity | Lab | Issue |
| --- | --- | --- | --- |
| STUDENT-R5-001 | Low | UL-11 | The teardown has the comment `# Cognito: if you added a user pool domain, delete it first (aws cognito-idp delete-user-pool-domain)` immediately before the `delete-user-pool` lines, but there is no actual PowerShell command that runs `delete-user-pool-domain` — it's advice only, the student has to write and run it themselves. This is the exact same shape of gap that was flagged and fixed for UL-16 in round 4 (STUDENT-R4-002): AWS requires a custom domain to be deleted before the user pool it's attached to, so a student who added a domain and follows "run every Stop charges command yourself in order" literally will hit an error on `delete-user-pool` that the script gave no command to prevent. Recommend the same fix pattern used for UL-16: a real `if ($DomainCreated) { aws cognito-idp delete-user-pool-domain ... }` line (or a describe-then-delete check) ahead of the pool delete. |

No other new Low+ issues found. UL-02's repeated-condition style (see table above) is a readability
quibble, not something that would block or mislead a student, so it is not logged as a numbered issue.

## Part 2 — screens table

| Check | Result | What I saw |
| --- | --- | --- |
| Open `/exam?q=q-saa-2-1-k01-mc`, click "Study:" link — does Start here open at the lesson title? | **Pass** | Clicking "Study: A2 — Scalable and loosely coupled architectures" navigated to `/start?lesson=lesson-2-1` and the viewport landed with the "A2 — Scalable and loosely coupled architectures" heading right under the top nav — the long "Learn it by building it" landing content above it was skipped, not shown mid-scroll. |
| Pick a few lessons in the picker — does the address bar update? | **Pass** | Selecting lessons via the dropdown (keyboard-driven, real `change` events) updated the URL each time: `?lesson=lesson-1-2` → `?lesson=lesson-3-1` → `?lesson=lesson-3-2`. |
| Does the Back button behave sensibly after picking several lessons? | **Pass, with a note** | One Back press from the third lesson picked went straight to the exam page the student had arrived from (`/exam?q=q-saa-2-1-k01-mc`), not to the second-to-last lesson. The lesson picker appears to use `replaceState` rather than pushing a new history entry per selection. For a student this means Back "escapes" the lesson browsing in one press instead of stepping back through each lesson they looked at — arguably the friendlier behavior (no multi-click history maze), but a student who expects Back to undo their last dropdown pick one step at a time will be surprised it jumps further than that. Not a blocker. |
| On the exam tab, change modules — does the address follow? | **Pass** | Clicking the A2 module chip changed the URL to `?q=q-saa-2-1-k01-mc` (first drill in that module) and highlighted that question; clicking A4 changed it to `?q=q-saa-4-1-k01-mc`. |
| Lesson's drill links | **Pass** | Clicking a drill id link (e.g. `q-saa-2-1-k02-mc`) under "Drills for this lesson" navigated to the Exam drills tab with that exact question focused/highlighted at the top, and its own "Study: A2 — ..." link pointed back to the same lesson. |
| Lesson's lab links | **Pass** | Clicking a lab link (e.g. `GL-11 — API Gateway and Lambda`) under "Labs for this lesson" navigated to `/labs?lab=gl-11` and opened that exact lab card. |
| "Back to Start here" | **Pass** | On the Exam drills page, the "Back to Start here" link is context-aware: its `href` was `/start?lesson=lesson-2-1` (the lesson the current question belongs to), not a generic Start here link, and clicking it landed back on that same lesson. |
| Repeat at mobile preset (375×812) | **Pass** | The exam question card, options, and the "Study:" link all reflowed cleanly with no horizontal scroll or clipped text. Clicking the "Study:" link (needed a precise click on the wrapped link's first line rather than its second line/gap — a minor click-target quirk of the automation, not a rendering bug) navigated to `/start?lesson=lesson-2-1` and again landed right at the lesson heading, same as desktop. |
| Reset to desktop | Done | `resize_window` preset `desktop` cleared the emulation before finishing. |

No Fail results in Part 2. The one behavior worth a mention (Back button skipping multiple lesson
picks in one press) is noted above but not logged as a numbered issue since it doesn't lose the
student's place or mislead them — it just needs a second look before writing bug reports about
"Back not working."

## Summary of new issues this round

- STUDENT-R5-001 (Low): UL-11 teardown has an advice-only comment for deleting a Cognito user pool
  domain before `delete-user-pool`, with no actual command — same shape as the round-4 UL-16 gap
  that was just fixed.
