# lesson-tf-g6 -- AWS (Terraform docs) review, round 1

## Method

- Fetched every URL in the claim table myself this turn with `curl -sL`, stripped HTML to text with a small Python script (scratchpad `awsg6/chk.py`, page texts kept beside it). No WebFetch.
- Machine-checked all 120 quotes against the page named in each row (whitespace, backticks and quote marks normalised): 116 verbatim at once. The other 4 (rows 15, 40, 50, 113) failed only because the page text has a link or code element inside the sentence; I located each sentence in the page text and all four are verbatim (row 15 state/locking, row 40 s3 backend IAM note, row 50 backend page cloud/backend, row 113 state page "Subcommands that are read-only (such as list) do not write any backup files").
- Read the whole `bodyMarkdown` sentence by sentence and checked prose with no claim row (list below). Read tf-g3 for consistency.
- No AWS calls, no terraform commands, no git, no content edits.
- Pages read: language/backend, backend/local, backend/s3, state, state/locking, state/remote, state/remove, state/refactor, block/terraform, block/import, block/removed, import, import/single-resource, modules/develop/refactoring, cli/commands/{init,plan,refresh,import,state,state/list,state/show,state/mv,state/rm,force-unlock}, tutorials/state/resource-drift.

## Rows verified (120 of 120 verbatim; exact-claim judgment below)

| Rows | Page | Verbatim | Exact claim? |
|---|---|---|---|
| 1-7 | backend, backend/local, state | yes | yes. `path` "defaults to "terraform.tfstate" relative to the root module"; `workspace_dir` "The path to non-default workspaces"; backup text is on the state page ("a backup of the previous state in terraform.tfstate.backup"). |
| 15-22 | state/locking, init, force-unlock | yes | yes. `-lock-timeout` "The default is 0s (zero seconds), which causes immediate failure if the lock is already held by another process" is on the init page. "Local state files cannot be unlocked by another process" and "does not modify your infrastructure" are verbatim on force-unlock. |
| 33-40 (S3) | backend/s3 | yes | yes. "State locking is an opt-in feature of the S3 backend. Locking can be enabled via S3 or DynamoDB. However, DynamoDB-based locking is deprecated and will be removed in a future minor version." `use_lockfile - (Optional) ... Defaults to false.` Both argument sets "can be configured simultaneously". The page gives no version number and the lesson states none (correct). IAM note verbatim. |
| 45 | backend/s3 | yes | yes (opening sentence) |
| 50 | backend | yes | yes. Also on block/terraform ("mutually exclusive with"). |
| 51-62 | backend, block/terraform | yes | yes. One backend block; backend cannot refer to named values; cloud block same limit; "You can only provide one cloud block per configuration"; partial-config and `-backend-config`; override order ("later options overriding values set by earlier options"). |
| 63-69 | backend | yes | yes. The page says `.terraform/terraform.tfstate` "contains the backend configuration for the current working directory", and "The local backend configuration is different and entirely separate from the terraform.tfstate file that contains state data about your real-world infrastructure." Concern (e) fully supported. |
| 70-74 | init | yes | yes. See concern (d). |
| 76-95 | resource-drift, refresh, plan, import block | yes | yes. 0.15.4 on three pages; "Terraform 1.5+ supports configuration-driven import" (tutorial); `-generate-config-out=PATH - (Experimental) ... must not already exist`; refresh "effectively an alias for terraform apply -refresh-only -auto-approve". |
| 96-112 | state/mv, state/rm, state/remove, block/removed, import, refactor | yes | yes. See concern (a). |
| 113-120 | state, state/list, state/show | yes | yes ("Terraform expects a one-to-one mapping between configured resource instances and remote objects"; "Do not directly edit this file"). |

## Specific concerns, ruled

- (a) removed block. What the docs say, exactly. Intro of block/removed: "The removed block specifies a resource to remove from state without changing the underlying infrastructure." Its configuration model lists `lifecycle block | required` containing `destroy boolean`. The `lifecycle` section says "By default, Terraform removes the resource from state and destroys the actual resource. Set destroy to false to remove the resource from state without destroying the actual resource." and its summary line says "Default: None." The state/remove page says "Add a lifecycle block to the removed block and set the destroy argument to false. Setting destroy to true removes the resource from state and destroys it." So the reference page is internally inconsistent; `lifecycle { destroy = ... }` is marked required in the model, `destroy` is the only supported lifecycle argument, and the stated default is destroy. The lesson quotes the lifecycle text verbatim and teaches `destroy = false` to keep, which matches both pages. Residual risk in AWS-Lg6-001.
- (b) S3 locking: exactly as the page states (rows 33-40). `use_lockfile` optional, default false; DynamoDB deprecated "and will be removed in a future minor version"; no version floor given. PASS.
- (c) Version floors. -refresh-only 0.15.4: exact (plan page, tutorial, refresh page). import block 1.5: only the tutorial says it ("Terraform 1.5+ supports configuration-driven import"); block/import page gives none; acceptable since the lesson cites the tutorial. moved 1.1: AWS-Lg6-003. removed / remove-and-import 1.7: AWS-Lg6-002.
- (d) `-migrate-state` vs `-reconfigure`: init page says verbatim "Either -reconfigure or -migrate-state must be supplied to update the backend configuration." It follows "Re-running init with an already-initialized backend will update the working directory to use the new backend settings", which the lesson reflects. "-migrate-state will attempt to copy existing state", "-reconfigure disregards any existing configuration, preventing migration of any existing state", "-force-copy ... also automatically enables the -migrate-state option": all verbatim. PASS.
- (e) `.terraform/terraform.tfstate` holds backend configuration, not infrastructure state: PASS (quotes above).

## Prose with no claim row (checked)

- "Do not confuse the backend with the state file": explanation, consistent with the local backend page.
- "The local backend does lock the file, but the file still sits on one machine": locking by system APIs is verbatim (row 2); one-machine is explanation of "limits the ability to collaborate".
- `-lock=false` "dangerous if others might concurrently run commands against the same workspace" is verbatim on the plan, state mv, state rm and import pages. Fine.
- "`terraform refresh` ... overwrites state with no review": inference from the `-auto-approve` alias line. Accurate.
- "a later plan proposes creating a new object for each forgotten instance still in the configuration": state/rm page says Terraform would "create a new" object; paraphrase accurate.
- "-generate-config-out can write the resource block for you": plan page, "generate HCL for any imported resources not already present". Accurate.
- "group 4, section 4h covers how secret values reach state": cross-reference, not a docs claim; not checked against g4 here.

## Findings

**AWS-Lg6-001 (Medium, 6d, `removed` bullet).** The `removed` page contradicts itself (intro "without changing the underlying infrastructure" versus lifecycle "By default ... destroys"), and the model marks `lifecycle` as required. The lesson gives only "By default, Terraform removes the resource from state and destroys the actual resource." A student who reads the page intro will conclude the opposite, and a question on "what happens when destroy is omitted" would rest on an inconsistent page.
- Fix: after the default-destroy quotation add: "The reference page's opening line says the block removes a resource from state "without changing the underlying infrastructure", but its lifecycle section and the removal tutorial both control that with `lifecycle { destroy = ... }`, so always write `lifecycle` and set `destroy` explicitly: the configuration model lists the `lifecycle` block as required."
- Question-writer guidance: ask only "to keep the real object, which setting?" (`destroy = false`); never make "omit lifecycle" a key or distractor.

**AWS-Lg6-002 (Low, 6d exam tip).** The tip says "a `removed` block with `destroy = false` (1.7 or later)". The only doc statement of 1.7 is "Removing and importing resources requires Terraform version 1.7 or newer" (state/refactor page), which the body correctly ties to the "remove-and-import workflow". The tip attaches 1.7 to the `removed` block alone, which the cited pages do not say.
- Fix: "... is a `removed` block with `destroy = false` (the docs give Terraform 1.7 or newer for the remove-and-import workflow) or `terraform state rm`". Questions must not make "1.7 is the removed block floor" the key.

**AWS-Lg6-003 (Low, 6d, `moved` bullet).** "Moved blocks need Terraform 1.1 or later." The page (Refactor modules, Requirements) says "Terraform v1.1 and later is required to use moved blocks to explicitly refactor module addresses. Instead, use the terraform state mv CLI command." The lesson drops the qualifier and the older-version alternative.
- Fix: "Moved blocks need Terraform 1.1 or later (the Refactor modules page says "Terraform v1.1 and later is required to use moved blocks"); on older versions use `terraform state mv`."

**AWS-Lg6-004 (Low, 6c).** "Terraform detects the change and asks about migrating state" has no claim row. Backend page: "When you change a backend's configuration, you must run terraform init again" and "If you're just reconfiguring the same backend, Terraform will still ask if you want to migrate your state." Accurate; add a row: https://developer.hashicorp.com/terraform/language/backend, "If you're just reconfiguring the same backend, Terraform will still ask if you want to migrate your state." (16 words, verbatim).

No other factual errors found; no absolute stated beyond the quoted text; version floors are accurate to the pages.

## Coverage, tips, format, teach-before-test

- Four objectives, one `###` each in id order, each ends with an `**Exam tip:**` line; `### Warnings` present. No format problem.
- Three distinct questions per objective are supported: 6a (no backend block / path and backup; what local lacks; legacy -state/-state-out/-backup and returning to local); 6b (automatic and backend-dependent; -lock-timeout default 0s versus -lock=false; force-unlock and its lock ID; S3 `use_lockfile` default false and DynamoDB deprecated); 6c (block limits and cloud versus backend; partial configuration and `-backend-config`; `-migrate-state` versus `-reconfigure` and credentials in `.terraform`); 6d (refresh-only and its floor; import block versus command; moved versus state mv; removed versus state rm; state list/show; no hand edits).
- Exam tips are discriminating and carry the right absolutes.

## Consistency with tf-g3

- g3 describes `plan` reading state first, `-refresh-only` as updating state only (same quote), re-running `init` after changing the backend block, and the three ways to end up with fewer managed objects. g6 repeats the same quotes with no conflict. g3 gives no 0.15.4 floor; g6 adds it correctly. g3 says a bare init re-run "only adds what is missing" (modules and providers); g6's `-migrate-state`/`-reconfigure` for backend changes is a different init job, not a conflict. No contradiction.

Lesson tf-g6: approve for question writing (the four findings are wording fixes and one added row; none blocks questions, provided question writers follow the AWS-Lg6-001/002 guidance).

Overall: approve
