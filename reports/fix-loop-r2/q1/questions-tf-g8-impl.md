# Questions tf-g8 (HCP Terraform concepts) -- implementation report

## Summary

Twenty questions written in place into `content/questions/q-tf-004-8{a,b,c,d}-{mc,mc2,mr}.json` and `q-tf-004-8-extra-00..07-mc.json`. `id`, `type`, `module`, `objectiveIds` and `selectCount` are unchanged; `difficulty` is set per question (foundation or applied). Every question has `citationIds` (cite-tf-g8-* files), `mcpStatus: "verified"` and `reviewedOn: "2026-09-26"`. MC has 4 choices, MR has 5 with "(Select TWO.)" at the start of the stem. Every stem ends with a question. The shape matches the tf-g7 questions (same fields, rationale per choice by content, no letter references; a regex for a lone choice letter followed by is/misstates/reverses finds nothing).

The Teacher's fact ownership from `lesson-tf-g8-TEACHER.md` was binding and is followed question by question below. Tier or edition membership is not a key anywhere. No question claims hard mandatory can never be overridden. No question makes Remote the key to a generic "default execution mode" stem. No question uses Stacks. No question rests on a fact the lesson lacks, so there are no lesson additions requested.

Check (R) = the distractor is a practice or belief real teams have. Check (T) = the reason it is wrong is taught in the lesson (sentence named). The two were checked separately.

## Balance

- MC keys: a 4, b 4, c 4, d 4 (8a-mc c, 8a-mc2 a, 8b-mc d, 8b-mc2 b, 8c-mc a, 8c-mc2 c, 8d-mc b, 8d-mc2 d, extra-00 b, -01 d, -02 a, -03 c, -04 d, -05 b, -06 c, -07 a).
- MR key slots: 8a-mr b,d; 8b-mr a,c; 8c-mr a,e; 8d-mr c,d. Four different key sets.
- `q1_batch_check`: longest-is-key 4 of 16 (25%), shortest-is-key 3 of 16 (19%). I deliberately did not drive longest-is-key to 0 after a first pass left it at 0 of 16, because the shortest-key reopen found "never pick the longest" to be a tell.

## Questions

### 8a-mc (tf.004.8a; applied) key c
Fact owned: remote operations run on disposable VMs, and a CLI apply executes there.
- Laptop with only state in the workspace: R yes (Local mode). T 8a "the run happens in HCP Terraform even when you start it from your own terminal"; 8c Local mode is a different setting.
- Agent inside a private network: R yes (Agent mode). T 8c Agent mode "to run Terraform in isolated, private, or on-premises infrastructure" is a separate mode from the remote operations in the stem.
- Plan on the laptop, apply remote: R belief (hybrid expectation, the weakest of the three). T 8a "It always plans first, then uses that plan's output for the apply" and the run happens in HCP Terraform.

### 8a-mc2 (8a; foundation) key a
Fact owned: the three workflows and what starts each (key is API-driven).
- UI/VCS-driven: R yes (primary workflow). T 8a "HCP Terraform does not fetch configuration files from version control" in the API workflow, and the stem has no linked repository.
- CLI-driven: R yes. T the stem says no Terraform commands are run; CLI-driven runs start from `terraform plan` and `terraform apply`.
- Run trigger: R yes (8c). T 8c run triggers queue a run "on successful apply of runs in any of the source workspaces", not from a pipeline's web requests.

### 8a-mr (8a; applied) keys b, d
Fact owned: a merge to the linked branch queues a run; remote apply works only with no linked repo. No pull-request fact.
- First run starts by itself: R yes. T 8a "You must manually trigger an initial run in any new VCS-driven workspace."
- Commit to any branch queues a run: R yes. T 8d "linked to one branch of a VCS repository and ignores changes to other branches."
- Files uploaded from the working directory: R yes (CLI-driven habit). T 8d "The Terraform code for a normal run always comes from version control."
- MR stem-need rule: every choice is a statement about runs in the one VCS-linked workspace the stem names.

### 8a-extra-00 (8a; foundation) key b
Fact owned: speculative plans are plan-only, cannot apply, and pull requests start them. (The fork rule is not asked, to keep one fact.)
- Normal run with auto-apply off: R yes. T 8a "waits for user approval before running an apply", so a confirmed run is applied.
- Saved plan from `plan -out`: R yes. T 8a "Saved plans are a different thing ... `terraform apply` on the saved file".
- Health assessment: R yes. T 8b "health assessments are the scheduled version" of drift checking; it checks a built workspace, not a proposal.

### 8a-extra-04 (8a; foundation) key d
Fact owned: per-workspace run queue; a waiting run sits pending. (Plan-first and "Planned and finished" are not asked.)
- Fails with a lock error: R yes (plain state locking). T 6b "`-lock-timeout` ... immediate failure", which 8a contrasts with "this is the queue behind it".
- Cancels the first run: R yes (some CI tools supersede runs). T 8a "processes those runs in order".
- Plans alongside, only apply waits: R yes (a natural guess). T 8a only plan-only runs "can proceed at any time"; a normal run waits.

### 8b-mc (tf.004.8b; applied) key d
Fact owned: the Plan role cannot apply; roles build upward.
- Write: R yes. T 8b Apply means "Approve and apply Terraform plans in the workspace"; Write is the day-to-day provisioning role.
- Admin: R yes. T 8b "Each role builds upon the previous level, with Admin granting the most comprehensive access."
- Read: R yes (least privilege). T 8b Plan means "Queue Terraform plans in the workspace" and each role builds on the previous level, so Read lacks it. This is an inference from the ladder, not a quoted sentence; flagged for the reviewers.

### 8b-mc2 (8b; foundation) key b
Fact owned: one framework per policy set; the same workspace can use sets of different frameworks. (No enforcement levels, no empty-array fact.)
- One set with both: R yes. T 8b "A policy set can only contain policies written in a single policy framework."
- Rego kept for a second workspace: R yes (a workaround). T 8b "The same workspace can use several sets in different frameworks"; the stem requires both on the payments workspace.
- Run task for the Rego rules: R yes (run tasks call external tools). T 8b run tasks are "an external service called by HCP Terraform" versus policies "rules evaluated by HCP Terraform itself", and the stem requires HCP Terraform to evaluate both.

### 8b-mr (8b; applied) keys a, c
Fact owned: soft, hard and OPA mandatory override rules (per AWS-Lg8-001).
- Advisory pauses until override: R yes. T 8b Sentinel advisory "Failed policies never interrupt the run."
- Soft mandatory ends with no way to continue: R yes. T 8b soft mandatory "organization admins can configure the platform to allow team members to override failures"; the run is paused and can be continued.
- OPA has the same three levels: R yes. T 8b "OPA has one mandatory level"; two levels, advisory and mandatory.
- Keys are not a true/false pair: no distractor is the negation of a key.

### 8b-extra-01 (8b; foundation) key d
Fact owned: run tasks, advisory versus mandatory, most restrictive wins.
- Completes with warnings only: R yes. T 8b "the run ends based on the most restrictive enforcement level".
- Pauses for Manage Policy Overrides: R yes (policy habit). T 8b run tasks "have their own enforcement levels, which are not the policy levels".
- Blocked only when every task is mandatory: R yes (a misreading of the rule). T same most-restrictive sentence; "Mandatory: Failed run tasks can block a run from completing."

### 8b-extra-05 (8b; foundation) key b
Fact owned: health assessments only, drift detection, Remote or Agent mode required.
- Cost estimation: R yes. T 8b it is off by default and "an extra run phase, between the plan and apply", and it is not a drift check.
- Post-apply run task for drift: R yes. T 8b run tasks start at four points of a run; health assessments are the scheduled check ("HCP Terraform periodically runs health assessments").
- Audit trail token: R yes. T 8b audit trails record who changed what; they do not compare infrastructure with configuration.
- The Local-mode reading is worded as the lesson words it: it follows from the requirement and the docs do not name Local mode.

### 8c-mc (tf.004.8c; applied) key a
Fact owned: an HCP workspace is required; a CLI workspace is optional.
- Project with no workspace: R yes. T 8c "Every workspace and Stack must belong to exactly one project"; a project only groups workspaces.
- Working directory alone: R yes. T 8c CLI workspaces are tied to a directory; "HCP Terraform workspaces are required".
- CLI workspace created with `terraform workspace new`: R yes. T 8c "The Terraform CLI does not require you to create CLI workspaces" and the two kinds function differently.

### 8c-mc2 (8c; foundation) key c
Fact owned: each workspace is in exactly one project; project and workspace-scope permissions.
- In both projects: R yes. T 8c "exactly one project".
- Variable set scoped to both projects: R yes. T 8c a project-scoped set is "applied and available to all current and future workspaces" in it; it shares variables, not membership.
- Default Project: R yes. T 8c "Each project has a separate permissions set", so the Default Project does not grant every team access.

### 8c-mr (8c; applied) keys a, e
Fact owned: the execution modes.
- Local stores no state in HCP Terraform: R yes. T 8c Local "HCP Terraform keeps the state".
- Remote runs on the workstation: R yes (mode swap). T 8c Remote "on its own disposable virtual machines".
- Remote is the only choice for private systems: R yes. T 8c Agent mode "to run Terraform in isolated, private, or on-premises infrastructure".

### 8c-extra-02 (8c; foundation) key a
Fact owned: remote state sharing is off by default.
- No run trigger: R yes (the Teacher's suggestion). T 8c run triggers start runs; they do not grant state access.
- Workspace must be locked: R yes. T 8c lock "prevents ... any applies" and keeps new runs Pending; it says nothing about state access.
- Variable set not reached `app`: R yes. T 8c variable sets share variables, not state or outputs.

### 8c-extra-06 (8c; applied) key c
Fact owned: variable precedence (`-var` over workspace-specific over variable sets).
- Global set value: R yes. T 8c "Workspace-specific variables always overwrite variables from variable sets".
- Workspace value: R yes. T 8c "-var or -var-file values overwrite workspace-specific and variable set variables".
- Terraform stops on a key in several places: R yes. T the same precedence sentences; duplicates are resolved, not rejected.

### 8d-mc (tf.004.8d; applied) key b
Fact owned: `terraform login`, app.terraform.io default, plain-text token.
- Encrypted in the OS keychain: R yes (other tools do this). T 8d by default Terraform will "save it in plain text in a local CLI configuration file".
- Written into the `cloud` block: R yes (the docs describe that option). T 8d the docs advise against it: "We recommend omitting the token from the configuration".
- Refuses without a hostname: R yes. T 8d "If you don't provide an explicit hostname, Terraform will assume ... app.terraform.io."

### 8d-mc2 (8d; foundation) key d
Fact owned: `name` versus `tags`.
- `name` with all three names: R yes. T 8d `name` is a single workspace.
- `prefix`: R yes (legacy `remote` backend). T 8d "the cloud block does not support the prefix argument".
- `name` plus `tags`: R yes. T 8d "If you configure the name, you cannot use the tags configuration."

### 8d-mr (8d; applied) keys c, d
Fact owned: `TF_CLOUD_*` apply only when the argument is omitted; an empty `cloud` block; `TF_WORKSPACE` never creates. Keys are the empty block and the precedence; the `TF_WORKSPACE` fact appears as a distractor, not a key.
- `TF_WORKSPACE` creates the workspace: R yes. T 8d "HCP Terraform will not create a new workspace from this variable".
- `TF_CLOUD_HOSTNAME` has no default: R yes. T 8d "The `hostname` argument defaults to app.terraform.io".
- `TF_CLOUD_ORGANIZATION` selects the workspace: R yes (naming confusion). T 8d `TF_WORKSPACE` is the variable that selects one workspace.

### 8d-extra-03 (8d; foundation) key c
Fact owned: `terraform init` migrates state. (The `prefix` to `tags` fact is left to 8d-mc2's distractor.)
- Keep `backend` beside `cloud`: R yes. T 8d "You cannot configure a backend block when the configuration also contains a cloud configuration".
- `terraform login` again: R yes. T 8d login "obtains an API token"; it does not move state.
- Destroy and re-apply: R yes (greenfield rebuild). T 8d "Terraform prompts you to migrate state", so state moves in place with no destroy.

### 8d-extra-07 (8d; foundation) key a
Fact owned: VCS integration, specific directories trigger runs. (Commits starting runs is left to 8a.)
- Different branch per folder: R yes. T 8d "linked to one branch ... ignores changes to other branches".
- `.terraformignore`: R yes. T 8d it keeps files out of a CLI-driven upload; it does not filter VCS triggers.
- Run trigger from `network` to `app`: R yes. T 8c run triggers fire on a successful apply in a source workspace, not on file changes.

## Distractor type table

| Type | Questions |
|---|---|
| Wrong execution mode (Local, Agent, Remote swapped) | 8a-mc, 8c-mr |
| Wrong run workflow or run type | 8a-mc2, extra-00 |
| Run trigger used where it does not fit | 8a-mc2, extra-02, extra-07 |
| Wrong policy or enforcement level claim | 8b-mr, 8b-extra-01 |
| Wrong role | 8b-mc |
| Wrong cloud-block or environment-variable behaviour | 8d-mc2, 8d-mr |
| Wrong state or migration step | extra-03, 8d-mc |
| Other single uses | the rest |

Run trigger appears in 3 of 20 (15%), at the cap, and in 8a-mc2 and extra-02 and extra-07 as three different wrong reasons. The audit script counts "HCP Terraform" in 3 of 20 distractors (extra-03, 8a-mc, 8c-mr), at the cap; see the TERMS note below.

## TERMS proposal for `distractor_type_audit.py`

TERMS already contains "HCP Terraform" (from tf-g1), and it is the subject of this whole lesson, so by the HANDOFF rule on bare subject vocabulary it is not a reused distractor type here. It counts 3 of 20 (15%) and passes only because I reworded two distractors to avoid it. I did not edit the script. Proposed tf-g8 constructs for the Lead Dev to add if wanted: `speculative plan`, `run trigger`, `variable set`, `tfe_outputs`, `TF_CLOUD_`, `TF_WORKSPACE`, `.terraformignore`, `terraform login`, `Sentinel`, `OPA`. "Sentinel" and "OPA" are 8b's subject vocabulary and would be over cap in 8b, so adding them is not recommended; the other eight are safe.

## Chain output

```
$ python3 scripts/content_lint.py
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS

$ python3 scripts/q1_batch_check.py tf-g8
task tf-g8: 20 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 4 for 4 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 4/16 = 25%
PASS: shortest-is-key 3/16 = 19%
PASS: MC key positions {'a': 4, 'b': 4, 'c': 4, 'd': 4}
PASS: MR key slots {'a': 2, 'b': 1, 'c': 2, 'd': 2, 'e': 1}
PASS: MR key sets: most common 'b,d' in 1/4 (25%); all {'b,d': 1, 'a,c': 1, 'a,e': 1, 'c,d': 1}
RESULT: PASS

$ python3 scripts/distractor_type_audit.py tf-g8
task tf-g8: 20 questions; 15% cap = 3 questions

HCP Terraform                 3   15%  q-tf-004-8-extra-03-mc,q-tf-004-8a-mc,q-tf-004-8c-mr
-out                          1    5%  q-tf-004-8-extra-00-mc

RESULT: PASS

$ python3 scripts/stem_echo_check.py tf-g8
task tf-g8: 20 questions, 0 waiver(s) on file

no stem/key echo found

0 unwaived giveaway, 0 waived, 0 bulk echo, of 20 questions
RESULT: PASS

$ python3 scripts/claim_prose_check.py tf-g8
task tf-g8: 8 distinct numbers in lesson prose
PASS: every claim-table number appears in the lesson prose

$ python3 scripts/test_q1_letter.py
PASS: 12 bad, 10 good, 0 failures

```

Overall: every check above PASSES in this run. (The claim-table note: rows 220 to 234 in the lesson report carry no finding ids in the claim column, because the checker reads digits there.)


## Round 2 fix pass

Files: the nine questions below. Chain re-run after the edits is at the end. Distractor (R) and (T) checks were redone for each rewritten choice.

| Finding | Question | Old | New |
|---|---|---|---|
| AWS-Qg8-001 / AWS-Lg8-012 (ruling 1) | extra-06 | stem "a global variable set defines"; choice d "None of them; Terraform stops at a key that is defined in several places" | stem "a global variable set that is not marked as priority defines"; d "Terraform reports an error for a key defined in several places" (also TEACHER-Qg8-006); rationale says the set is not priority, so the workspace value would beat it without a command-line value. R yes; T the lesson's precedence sentences (duplicates are resolved) and the new priority exception. |
| AWS-Qg8-002 (2) | 8c-mc2 | no access constraint | stem adds "Neither team should end up able to open workspaces it does not already use."; rationale for d: moving it leaves both teams without access (separate permissions set per project) or, if both are granted access, exposes the other workspaces that start in the Default Project. T 8c "Each project has a separate permissions set" that grants teams access to all its workspaces. |
| TEACHER-Qg8-001 / AWS-Qg8-005 / LD-Qg8-001 (3) | 8b-mc | stem "propose infrastructure changes and queue plan runs to preview each one, while a senior engineer signs off before anything goes live"; c "Read, the lowest built-in role on the workspace"; d "Plan, which queues Terraform plans without the apply permission" | stem "submit changes for review and preview what each would do on their own, while a senior engineer decides what is applied"; c "Read, which lets people view information about workspace runs"; d "Plan, which can queue Terraform plans". Rationale quotes the taught Read and Plan descriptions. R yes; T the new Read quote (row 236) against the Plan quote. Shortest-is-key is now 4 of 16 (25%), passing. |
| AWS-Qg8-003 / TEACHER-Qg8-003 (9) | extra-03 | stem "What completes the migration of that state?"; a "Keep the existing `backend` block beside the `cloud` block until the state has moved" | stem "What gets that state into the HCP Terraform workspace?"; a "Keep a `backend "local"` block beside the `cloud` block until the state has moved". Key kept ("accept the prompt to migrate the existing state"); stem_echo_check passes. Rationale says a backend block, local or otherwise, cannot be configured beside `cloud`. |
| AWS-Qg8-004 / TEACHER-Qg8-005 (10) | extra-02 | key "...switched on in the `network` workspace itself"; c "The `network` workspace has to be locked before another workspace can read its state" | key "State sharing is off by default and has to be enabled for `network`"; c "The two workspaces sit in different projects, and remote state only works within one project". R yes (misconception); T the three taught share scopes (organization, same project, specific workspaces), now in the rationale in place of the lock sentence. |
| AWS-Qg8-006 / TEACHER-Qg8-002 (11) | 8a-mr | c "A commit pushed to any branch of the repository queues a run" | c "A commit pushed to any other branch of the repository queues a regular plan-and-apply run in this workspace". Lengths: c 104 against keys b 78 and d 84, so the keys are no longer the two longest. R yes; T "linked to one branch ... ignores changes to other branches". Rationale says a push to another branch does not queue a regular run. |
| TEACHER-Qg8-002 (12) | 8b-mr | a 104 chars, c 115, e 56 | a "A failed OPA mandatory policy can be overridden by a user with Manage Policy Overrides" (86); c "A failed Sentinel hard mandatory policy can be overridden only if its policy set allows overrides" (97); e "OPA offers the same three enforcement levels as Sentinel: advisory, soft mandatory and hard mandatory" (101). Order e, c, a, b, d: only one key is among the two longest, and the longest choice is a distractor. |
| TEACHER-Qg8-004 (13) | 8a-mc | d "The plan runs on the laptop and only the apply runs on HCP Terraform's machines" | d "On HCP Terraform's machines only for repository-linked workspaces, while CLI runs stay on the laptop". R yes (a plausible misreading of remote apply); T the lesson sentence "CLI operations are remotely executed in HCP Terraform's run environment by default" (confirmed in the lesson body) and "Remote terraform apply is for workspaces without a linked VCS repository". Rationale updated. "HCP Terraform" is still 3 of 20 in the audit, as before. |
| extra-07 c (14) | extra-07 | "does not filter VCS triggers" | "it is not the setting the docs name for choosing which repository files trigger runs" |

Key and letter balance are unchanged (MC keys a 4, b 4, c 4, d 4). `id`, `type`, `module`, `objectiveIds` and `selectCount` are unchanged, and `reviewedOn` and `mcpStatus` are untouched.

Chain re-run after the edits: content_lint PASS; q1_batch_check RESULT: PASS (longest-is-key 3/16 = 19%, shortest-is-key 4/16 = 25%); distractor_type_audit RESULT: PASS; stem_echo_check RESULT: PASS (0 unwaived giveaway, 0 bulk echo); claim_prose_check PASS; test_q1_letter PASS (12 bad, 10 good, 0 failures).
