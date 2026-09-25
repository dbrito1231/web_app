# Student review — fix-loop-r2 round-3

Role: College IT Student (learner check)
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`
Checked: 2026-09-25
UI method: Claude Browser MCP (own tab `tab-1`) against the running app at `http://127.0.0.1:5173`. Used screenshots, `read_page`, `get_page_text`, and `javascript_tool` (read-only DOM inspection, no app code touched). Did not click Reset or Import, did not run `aws`, did not use curl/Playwright.
Did submit exactly **one** drill's answer (Part 2, last section) as instructed. No other drills or lab checkpoints were submitted.

---

## Part 1 — Stop charges, followed literally

### GL-01 — Identity, budget, and preflight

Could follow top to bottom. Every teardown variable (`$AccountId`, `$BoundaryArn`, `$Serial`) is **derived inside the teardown block itself** (`$AccountId = aws sts get-caller-identity --query Account --output text`, `$BoundaryArn = "arn:aws:iam::$($AccountId):policy/gl01-boundary"`), so a learner who opens Stop charges cold (new PowerShell session, lost the build-time variables) can still run it — nothing is assumed to still be in memory. Delete order (deactivate MFA → delete MFA device → remove boundary → delete user → delete boundary policy → delete budget) matches step 13's stated order. No place to get stuck.

### GL-08 — Application Load Balancer

Could follow top to bottom. Step 8's user-data write is now:
`[IO.File]::WriteAllText("$pwd\user-data.sh", "#!/bin/bash`npython3 -m http.server 80`n", $utf8)` with `$utf8 = New-Object System.Text.UTF8Encoding $false` — this is LF-only (PowerShell backtick-n inside a double-quoted string is a real newline, not CRLF) and no BOM, and the step says so explicitly ("This writes LF line endings and no BOM, so the shebang works on Linux."). **R2 fix confirmed.** Teardown IDs ($AlbArn, $TargetGroupArn, $InstanceId, $RtAssocPub/2, $PublicRouteTableId, $SubnetPub/2, $IgwId, $SgId, $VpcId) are all things the learner sets while building in steps 6–9, and every teardown line is guarded with `if ($X) { ... }` so a partial build doesn't crash the whole block. Would get stuck only if I closed PowerShell between building and teardown (variables lost) — but that risk is common to every LIVE AWS lab here, not new to GL-08.

### GL-17 — Athena on a tiny file

Could follow top to bottom. Step 9 (drop table/database) now uses the same `aws athena start-query-execution --query-string 'DROP TABLE gl17.sample' --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/` wrapper as steps 7–8, so it is a real, runnable command a learner can paste — not bare SQL text. **R1 fix confirmed.** Teardown independently re-derives both bucket names via `aws sts get-caller-identity` subshells and runs `DROP TABLE IF EXISTS` / `DROP DATABASE IF EXISTS` before touching S3, matching the stated order (table → database → buckets). CSV write (step 6) uses the same LF-safe `[IO.File]::WriteAllText(...,"name,value`nfoo,1`n",$utf8)` pattern as GL-08 — the round-1 "literal `\n`" concern is gone.

### UL-07 — Challenge: EC2, EBS, and EFS

Could follow the acceptance criteria and Stop charges. The `# Uses: $FileSystemId, $InstanceId, $MountTargetSgId, $InstanceSgId (the IDs you set while building; unset ones are skipped)` and `# Lost an ID? aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=ul-07` header lines are genuinely useful — they tell me exactly which variables I need to have kept and give me a recovery command if I didn't. Teardown correctly deletes mount targets, waits for the count to hit zero, *then* deletes the file system, matching acceptance criterion 7/8. Notable gap: **UL-07 has no "name the resources `workbook-ul07`" criterion** — criterion 10 only says "All resources tagged LabId=ul-07," so unlike UL-10/UL-19 there's no fixed name to fall back on if I lose an ID; I'd be fully dependent on the tag search.

### UL-08 — Challenge: Application Load Balancer

Could follow it. The `# Uses:` line lists all 15 possible variables ($WebAclName, $WebAclId, $AlbArn, $ListenerArn, $TargetGroupArn, $InstanceId, $AllocationId, $VpcId, $SubnetPub, $SubnetPub2, $IgwId, $PublicRouteTableId, $RtAssocPub, $RtAssocPub2, $SgId) and the `# Lost an ID?` tag-search line is present. Teardown order (disassociate WAF → delete web ACL → delete listener → delete ALB and wait → target group → instance → route table → subnets → IGW → SG → VPC) matches acceptance criteria 5–7 and the dependency order taught in GL-08. Same gap as UL-07: **no `workbook-ul08` naming criterion**, tag search is the only recovery path.

### UL-10 — Challenge: Queue and event path

Very easy to follow — this is the clearest of the four. Criterion 1 says explicitly: *"Name the resources you create `workbook-ul10`: function `workbook-ul10`, role `workbook-ul10-lambda`, queues `workbook-ul10` and `workbook-ul10-dlq`, topic `workbook-ul10`, and table `workbook-ul10-idem`..."* and the teardown header says `# Uses: none (resources are named workbook-ul10)`. Because everything is fixed-named, the teardown script doesn't depend on any session variable at all — it looks up the Lambda, queues, SNS topic, and role by their fixed names. This is the easiest of the four unguided labs to recover from if I lost my session (close PowerShell, come back next day — the names are still `workbook-ul10*`).

### UL-19 — Challenge: EKS control plane then delete

Also very followable, same "fixed naming" pattern as UL-10: criterion 1 requires `workbook-ul19` cluster, `workbook-ul19-eks` role, and either `workbook-ul19-ng`/`workbook-ul19-node` or `workbook-ul19-fp`/`workbook-ul19-fargate`. Teardown header: `# Uses: none (resources are named workbook-ul19)`. The teardown script itself lists node groups/Fargate profiles by API call rather than a remembered ID, deletes them, waits, then deletes the cluster, then cleans up the log group and the three possible IAM role names — genuinely resilient to a lost session. The in-teardown comment "Node groups and Fargate profiles must be gone before delete-cluster... node groups can take 10+ minutes" set my expectations correctly before I'd hit `ResourceInUseException` myself.

**New (Low) — inconsistent naming criterion.** UL-10 and UL-19 both got the explicit "Name the resources you create `workbook-ulNN`" acceptance criterion and a naming-driven, session-independent teardown. UL-07 and UL-08 did not — they still rely entirely on remembered PowerShell variables (with a tag-search fallback) even though the same fixed-naming pattern would make their teardown just as resilient. See "New issues" table below (STUDENT-R3-004).

---

## Part 2 — UI re-check

**O1 — header shows progress before Labs tab opens.** Read `frontend/src/App.tsx`: `<Header activeTab={tab} onTabChange={setTab} stats={headerStats} />` is rendered unconditionally, and only `<main>` is gated behind `{loading && <p className="page-loading">Connecting to local API…</p>}` (line 82) followed by `{!loading && summary && (...)}` for the actual tab content. So the header — brand, the four tabs including "Labs," and the "Saved in this browser / 0% / 0 of 42 labs done" strip — mounts before the Labs panel does, confirmed structurally in source, not just by observed timing (dev server is fast enough that it's hard to catch the loading frame live). **Pass.**

**O5 — exam at 375×812 has no sideways scroll.** Set the Browser pane to `mobile` (375×812) on `/exam`, then checked `document.documentElement.scrollWidth` vs `clientWidth` (both `375`) and `document.body.scrollWidth` (`375`) — no overflow. Visually the drill-bank list, search box, and category chips all wrap inside the viewport. Reset back to `desktop` afterward. **Pass.**

**O6 — every drill shows a "Study:" link.** Spot-checked 5 drills via `?q=` deep links and DOM inspection of the resulting `<article class="pbq">`:
| Drill | Type | Study link shown |
| --- | --- | --- |
| `q-tf-004-8a-mc` | Terraform, MC | "Study: T4 — HCP Terraform concepts" → `/start?lesson=lesson-tf-g8` |
| `q-tf-004-8a-mc2` | Terraform, MC | "Study: T4 — HCP Terraform concepts" → `/start?lesson=lesson-tf-g8` |
| `q-saa-1-1-k01-mc` | AWS, MC | "Study: A1 — Secure access to AWS resources" → `/start?lesson=lesson-1-1` |
| `q-saa-1-1-k01-mr` | AWS, MR | "Study: A1 — Secure access to AWS resources" → `/start?lesson=lesson-1-1` |
| `q-saa-1-1-k04-mr` | AWS, MR | "Study: A1 — Secure access to AWS resources" → `/start?lesson=lesson-1-1` |

All 5 showed a Study link (2 Terraform, 3 AWS, including 3 MR/2 MC mix). **Pass** on this sample.

**O7 — lesson → lab links.** `StartHereTab.tsx` line 34 renders `<a href="/labs?lab=${encodeURIComponent(lab.id)}">{lab.title}</a>` for labs matching a lesson's objectives. Followed one to `/labs?lab=gl-08`: `LabsTab.tsx` line 28 reads `?lab=` and seeds the search box with it (`const linkedLab = new URLSearchParams(window.location.search).get('lab') ?? ''`), which filters the list to exactly that one card ("1 labs shown") and the GL-08 card renders already expanded with its full step list visible, not just the title. **Pass** — this is a real, working deep link, not just a same-page anchor.

**R5 — `/exam?q=` deep link.**
- Good id (`q-tf-004-8a-mc`): the page scrolled to that question (`window.scrollY` = 32000, deep in the 429-card list) and `document.activeElement` was the question's own `<h2 tabindex="-1" class="pbq-heading">q-tf-004-8a-mc</h2>` — i.e. it is genuinely focused (assistive tech would announce it), not just scrolled into view. **Pass — R1's silent "falls back to first card" bug is gone.**
- Bad id (`q=bad`): page now shows **"No drill matches "bad"."** as visible text above the (unfiltered) drill list, instead of silently opening the first card. **Pass.**

---

## Answering one drill (before clicking Check answers)

Chose `q-tf-004-8a-mc` (Terraform, T4, MC, "Select 1"): *"A teammate asks how to meet this requirement: Use HCP Terraform to create infrastructure. Which action is appropriate?"*

Choices seen: (1) "Leave hourly resources running overnight without teardown," (2) "Apply the objective directly: Use HCP Terraform to create infrastructure," (3) "Treat budget alerts as a hard spend stop that deletes resources," (4) "Ignore least privilege and use the root user for speed."

**My answer, chosen before clicking Check: choice 2 ("Apply the objective directly...").** Reasoning at the time: choices 1, 3, and 4 each describe a concrete unsafe/incorrect practice this workbook explicitly warns against elsewhere (leaving hourly resources running, treating alerts as if they stop spend, using root) — none of them actually describes using HCP Terraform. Choice 2 is the only one left standing, even though its wording just restates the objective rather than naming a real Terraform action (e.g. "define the config, run plan, then apply in HCP Terraform").

**Result after clicking Check answers once:** 100%, "Clean pass. Move on to the next drill." Rationale shown: *"The choice that applies the stated requirement is correct. Using the root user, leaving hourly resources running, and treating budget alerts as a hard stop are not."*

**Does the explanation make sense?** Partly. It correctly explains why the three distractors are wrong, in plain terms tied to their content (root user, no teardown, alerts-as-stop) rather than by letter — so this drill does **not** show the known "names letters like A and B" bug. But the explanation for the *correct* choice is circular ("the choice that applies the stated requirement is correct") — it never says what actually applying the requirement looks like (e.g., write/commit Terraform config, then `terraform plan`/`apply` through an HCP Terraform run). A learner who guessed right by elimination, like I did, doesn't come away actually knowing the HCP Terraform workflow. This is the same generic "Apply the objective directly" pattern flagged as R3/STUDENT-R1 in round 1 — still present, not a new bug, but worth re-flagging since it's the one drill this round I read closely enough to judge the explanation quality.

---

## Verdict table

| ID | Verdict | Evidence |
| --- | --- | --- |
| GL-01 Stop charges | **Pass** | Teardown re-derives `$AccountId`/`$BoundaryArn` from scratch; delete order matches step 13 |
| GL-08 Stop charges (R2) | **Pass** | `[IO.File]::WriteAllText` with backtick-n + `UTF8Encoding($false)` = LF, no BOM, as stated in the step |
| GL-17 Stop charges (R1) | **Pass** | Drop steps wrapped in `aws athena start-query-execution` like s07/s08; teardown drops table then database before S3; CSV write is LF-safe |
| UL-07 Stop charges | **Pass** (with a gap, see STUDENT-R3-004) | `# Uses:` / `# Lost an ID?` present; teardown waits for mount targets to clear before file-system delete |
| UL-08 Stop charges | **Pass** (with a gap, see STUDENT-R3-004) | `# Uses:` / `# Lost an ID?` present; teardown order matches WAF-then-ALB-then-network dependency chain |
| UL-10 "name the resources" criterion | **Pass** | Explicit `workbook-ul10*` naming criterion; teardown needs no remembered variables |
| UL-19 "name the resources" criterion | **Pass** | Explicit `workbook-ul19*` naming criterion; teardown needs no remembered variables |
| O1 header progress before Labs opens | **Pass** | `<Header>` rendered outside the `loading` gate in `App.tsx` |
| O5 exam mobile no sideways scroll | **Pass** | `scrollWidth === clientWidth === 375` at 375×812 |
| O6 every drill shows Study link | **Pass** (5/5 sampled) | 2 Terraform + 3 AWS, mix of MC/MR, all had a working Study link |
| O7 lesson → lab links | **Pass** | `/labs?lab=gl-08` filters to and expands GL-08 |
| R5 good id | **Pass** | Scrolls to and focuses the question heading (`document.activeElement`) |
| R5 bad id | **Pass** | Shows `No drill matches "bad".` instead of silently opening the first card |
| Drill answer explanation quality | **Still a known issue, not new** | No letter-naming in this sample, but "Apply the objective directly" rationale is still tautological |

---

## New issues (Low+)

| ID | Severity | Issue |
| --- | --- | --- |
| STUDENT-R3-001 | Info | Browser pane was intermittently reported "hidden" mid-session, which makes `computer` screenshots return blank; had to fall back to `read_page`/`get_page_text`/`javascript_tool` for verification. Not an app bug — noting for future review sessions using this tooling. |
| STUDENT-R3-002 | Info | The drill-bank search box (`All drills` field on Exam drills) does not appear to filter when typing a module code like "A1" — typing produced no visible narrowing of the list before I switched to `?q=` deep links instead. Not verified further since it was outside the requested scope; flagging in case it's a real filter gap Lead Dev wants to check. |
| STUDENT-R3-003 | Low | The `?q=` / `?lab=` deep-link pattern is inconsistent between tabs: Exam drills scrolls to and focuses the question (`tabindex="-1"` + `.focus()`), while Labs only pre-fills the search box with `?lab=` (no explicit scroll/focus call needed since the single filtered result renders at the top, but there's no `tabindex`/focus management if that ever changes to allow multiple matches). Cosmetic only today; would matter if the `lab=` filter is ever loosened to match more than one card. |
| STUDENT-R3-004 | Low | The new "name the resources you create `workbook-ulNN`" acceptance criterion (and the resulting variable-free teardown) was added to UL-10 and UL-19 but not to UL-07 or UL-08 — those two still rely entirely on remembered PowerShell session variables, with only a tag-search as a lost-ID fallback. Recommend applying the same fixed-naming criterion to UL-07/UL-08 for consistency with the other three checked unguided labs. |
| STUDENT-R3-005 | Low (carried over, not new) | Drill `q-tf-004-8a-mc`'s correct-answer rationale ("The choice that applies the stated requirement is correct") is tautological and doesn't explain the actual HCP Terraform action a learner should take. Ties to round-1 R3 finding about `Apply the objective directly:` choice text; re-confirmed live this round via one submitted answer, not a new pattern. |
