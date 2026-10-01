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

---

## Round 2

Method: re-ran my table checker against the current `lesson-tf-g6-impl.md` (136 rows): 131 verbatim directly; the 5 misses are rows 15, 40, 50, 113 (link/code split, verified by hand in round 1) and row 125 (`lifecycle block ... required`, an ellipsis join of two fragments that the page separates with a pipe; both fragments are on the page's configuration-model line). Re-read the import command page, import overview, import-single, block/import and resource-drift pages to rule on the dropped sentences. Read the current lesson and all 12 `q-tf-004-6*.json` (keys from `correctAnswerIds`), and checked every citation id exists with `accessed: 2026-09-26`. No AWS, no terraform, no git, no content edits.

### (a) My round-1 findings

- AWS-Lg6-001: Gone. The lesson now states that the model marks `lifecycle` "required", that only `destroy` is supported, the opening-line tension, and "always write the `lifecycle` block and set `destroy` explicitly". It makes no claim about omitting it. Questions use only `lifecycle { destroy = false }`.
- AWS-Lg6-002: Gone. The tip scopes 1.7 to "the remove-and-import workflow"; no question tests 1.7.
- AWS-Lg6-003: Gone. The 1.1 sentence carries the page's wording and the `state mv` alternative; no question tests 1.1.
- AWS-Lg6-004: Gone. The row-124 sentence is in 6c, verbatim.

### (b) Second-role check of TEACHER-Lg6-001..008

- 001 Gone (nesting shown; discriminator and tip use `lifecycle { destroy = false }`).
- 002 Gone, and the writer was right to drop the five unsupported sentences. The `terraform import` command page says none of: "no plan preview", cannot generate configuration, must write the resource block first, "To import multiple resources, use the import block". I read the whole page text: it says only "Import will find the existing resource from ID and import it into your Terraform state at the given ADDRESS", the one-address warning, and "Instead of manually importing resources, you can add the import block ...". "Changes state immediately" and "records the rename for others" are on no fetched page either. The replacements (rows 97, 128-130) are verbatim and say no more than the source. Caution: the resource-drift tutorial itself says "This tutorial uses terraform import to bring infrastructure under Terraform management", so `terraform import` is a working way to adopt a bucket; a question may fail it only on a stated requirement (see AWS-Qg6-001).
- 003 Gone (rows 131-136 verbatim; "legacy command" correctly scoped to moving resources between state files).
- 004 Gone (four `####` headings plus "Putting it together"; garbled quote rewritten; one `**Exam tip:**` for 6d).
- 005 Gone. 006 Gone (rows 121-123 verbatim; "HashiCorp's hosted service" is the lesson's attribution of the page's "hosted service", acceptable).
- 007 Confirmed real and outside g6: g4 says "per group 3's state-security guidance" but g3 has no state-security text. The right pointer is g6's Warnings. g6's own cross-reference "group 4, section 4h covers how secret values reach state" is accurate (g4 has `### tf.004.4h ... Manage sensitive data` and opens with "Terraform stores those secrets in its state and plan files"). The CR against g4 stands.
- 008 Gone (no fix needed).

### (c)/(d) Question review

All 12: keys correct; every distractor is a real Terraform option or a common belief; citations resolve; `mcpStatus` verified. MR stems carry "(Select TWO.)", and each joins two needs that every distractor addresses (6a: flags vs return-to-local; 6b: S3 locking vs force-unlock; 6c: `-migrate-state` vs `-force-copy`; 6d: rename vs forget), so the MR stem-need rule holds. No distractor is a working answer against its stem (6d-mc `terraform refresh` and plan-only fail "inspect before it is recorded" and "state updated"; 6d-mc2 `terraform import` fails "one reviewed run with adoption visible in the plan"). No fact is duplicated across the 12. Numbers and versions in keys and distractors: `-lock-timeout=0s` (default "0s" on the init page; used as a false "wait indefinitely" distractor, correct), `use_lockfile` default false (S3 page), and "1.5 or later" in the 6d-mc2 rationale (tutorial: "Terraform 1.5+ supports configuration-driven import"). No 1.1, 1.7 or 0.15.4 appears in any key or distractor. The S3 locking defaults and "deprecated and will be removed in a future minor version" match the page exactly; no `removed` question rests on the intro line.

**AWS-Qg6-001 (Medium, q-tf-004-6d-mc2; this rules LD-Qg6-002).**
- Is the `terraform import` distractor's refutation taught? Partly. The lesson never says the command lacks a preview or handles only one object, and rightly does not. It does teach that the block "lets you import multiple resources at once, review the import in your plan-and-apply workflow" (row 130), set beside a command whose usage is `ADDRESS ID`. A reader can infer the contrast, but "one object per run" is stated nowhere in the lesson, and only the stem's "adoption visible in the plan output" excludes the command.
- Doc support for the rationale's claims: "one object per run" is supported only by the command page's usage line (`terraform import [options] ADDRESS ID`, one address and one ID) and by its examples each importing a single instance. "Several resources in one reviewed run" is supported (row 130). "The docs steer readers to the block" is supported (row 129). "Resource blocks alone ... Terraform would plan to create new buckets" is neither taught nor on a fetched page; the lesson says only that an `import` block is required and that a resource block must exist to stop Terraform destroying the object.
- Keyword tell: "plan" is in the stem ("plan-and-apply run", "plan output") and in the key ("review `terraform plan` first") and in no distractor.
- Fix 1, lesson (Importing paragraph, after the sentence ending "at the given ADDRESS."): add "Its usage line is `terraform import [options] ADDRESS ID`, so each run names one address and one ID." Add a claim row quoting "terraform import [options] ADDRESS ID" from https://developer.hashicorp.com/terraform/cli/commands/import.
- Fix 2, stem: "Cobalt Retail has twenty S3 buckets created by hand in the console. They want all twenty adopted in a single reviewed run, with every adoption listed in a preview before anything is applied. How should they bring the buckets under management?"
- Fix 3, rationale, replace "so Terraform would plan to create new buckets" with "so nothing is adopted", and replace the last sentence with: "The `terraform import ADDRESS ID` command names one address and one ID per run, and the docs steer readers to the `import` block instead, which lets you import multiple resources at once and review the import in the plan-and-apply workflow." Do not assert that the command shows no preview.

**AWS-Qg6-002 (Low, 6a-mc rationale).** "HCP Terraform is only used when a `cloud` block connects the configuration to a workspace" is too strong: the docs' own examples use `backend "remote"` with `workspaces { name = ... }`, and the state page says remote state "is implemented by a backend or by HCP Terraform". Stem and key are fine.
- Fix: "HCP Terraform is used when the configuration connects to a workspace there (the `cloud` block is the documented way), not by default; with no block declared, the state is the local file."

**AWS-Qg6-003 (Low, 6a-mc2 rationale).** (1) "Other workspaces are supported through the `workspace_dir` setting" misstates it: `workspace_dir` is only "The path to non-default workspaces". (2) "Version control does not offer state locking or secure access control" generalises the page, which says to avoid "a version control system or other storage solution that does not support Terraform state locking and secure access control". The key is unaffected.
- Fix: "The local backend has a `workspace_dir` setting for the path of non-default workspaces, so more than the default workspace is possible. The docs say to avoid a version control system or other storage that does not support state locking and secure access control, because it can lead to data loss or exposure of secrets, so committing the file is not a fix." The lesson's Warnings quote only the data-loss clause; either add "does not support Terraform state locking and secure access control" to that quote (it is verbatim on the state page) or drop the locking clause from the rationale.

**AWS-Qg6-004 (Low, 6a-mr key a).** "the docs no longer recommend them for new systems" adds "for new systems"; the page says "we no longer recommend" the options.
- Fix: "Those options are legacy features kept for backward compatibility, and the docs no longer recommend them".

**AWS-Qg6-005 (Low, 6c-mc rationale).** "no setting writes state to two places" is supported by no page or lesson sentence; the supported point is mutual exclusivity.
- Fix: replace "and no setting writes state to two places" with "so a cloud block cannot sit beside a backend block".

Checked and not defects: 6b-mc2 stem "keep retrying" versus key "keeps trying" is a paraphrase and the verb also fits distractor c; 6c-mr key c is true in isolation (the unattended-job need is carried by key d); the 6a-mr stem timeline reads acceptably.

Task tf-g6: not yet (AWS-Qg6-001 needs a lesson sentence, a claim row, and a stem and rationale rewrite; 002-005 are rationale wording and may ride along; I will recheck)

Overall: concerns

---

## Round 2b (confirmation, 7e68d75)

Method: fetched `https://developer.hashicorp.com/terraform/cli/import` and `.../cli/commands/import` with `curl -sL` plus the text stripper and searched the text; read the "Round 2 fix pass" sections, the Teacher round-2 note, the current lesson, and the 6a-mc, 6a-mc2, 6a-mr, 6b-mc, 6c-mc and 6d-mc2 JSON (keys, choices, rationales, citations). No AWS, terraform or git; no edits.

### Correction to my Round 2 (b)

I wrote that the writer was right to drop all five unsupported sentences and that "none" of the dropped sentences was on the page, but I had searched only the `cli/commands/import` page. The overview page `cli/import` does carry three of them; the Teacher was right and I was wrong on those three. Still unsupported by any page I have read, and rightly absent: "no plan preview" and "changes state at once". The other dropped sentences ("changes state immediately", "records the rename for others") are also still unsupported.

### 3. Rows 137-140 re-verified (curl)

| Row | Page | Verbatim | Exact claim? |
|---|---|---|---|
| 137 | cli/commands/import | yes ("Usage: terraform import [options] ADDRESS ID") | yes: one address and one ID per run follows from the usage line |
| 138 | cli/import | yes ("Before you run terraform import you must manually write a resource configuration block for the resource.") | yes |
| 139 | cli/import | yes ("Importing via the CLI does not generate configuration.") | yes; the page adds "use the import block instead" for generating configuration |
| 140 | cli/import | yes ("To import multiple resources, use the import block.") | yes |

The lesson's sentence cites them accurately, attributing the three overview quotes to "the import overview page", and the new citation file `cite-tf-g6-import-cli-overview` exists with the right URL and note.

### 1. AWS-Qg6-001..005

- AWS-Qg6-001 (6d-mc2): Gone. The lesson now teaches "each run names one address and one ID" and "To import multiple resources, use the import block." The rationale's last sentence and the "nothing imported by resource blocks alone" clause are now taught. The unsupported "would plan to create new buckets" is gone. The "plan" keyword tell is gone because distractor d now ends "then run `terraform plan` to confirm". I accept not rewriting the stem. Changed distractor d: real (the tutorial itself uses `terraform import`); refuted by the taught sentences that the command names one address and one ID and that multiple resources go through the `import` block, against the stem's "all twenty ... in one reviewed plan-and-apply run"; no giveaway words. It is not a working answer to the stem as written. Residual wording nit (not blocking): the rationale's "and review the import in the plan-and-apply workflow" is the tutorial's statement about configuration-driven import, not the overview's, but both are quoted in the lesson.
- AWS-Qg6-002 (6a-mc rationale): Gone.
- AWS-Qg6-003 (6a-mc2 rationale): Gone. The `workspace_dir` sentence now matches the page; the unsupported "does not offer locking" is replaced by the taught data-loss warning. New distractor d ("There is none: ... a shared, versioned copy of the latest state") is real, refuted by "can result in data loss or exposure of secrets" and by the stem's "genuine weakness", and has no giveaway wording.
- AWS-Qg6-004 (6a-mr key a): Gone.
- AWS-Qg6-005 (6c-mc rationale): Gone as to the unsupported claim, but the replacement creates a small logic slip (AWS-Qg6-006 below).

### 2. Second-role check of TEACHER-Qg6-001, 002, 003, 006

- 001: Gone (fixes 1, 2, 3 applied; matches my AWS-Qg6-001).
- 002: Gone (choice d and rationale as proposed; every quoted claim now taught).
- 003: Gone. The 6b-mc rationale ends at "locking covers all operations that could write state", which is verbatim-taught ("State locking happens automatically on all operations that could write state"). Distractor c now reads "Locking covers `apply` but not state-modifying commands such as `terraform state mv`": real command, refuted by that same taught sentence, no giveaway wording; it also keeps the `state rm` type out of 6b (audit clean). The `cite-tf-g6-state-mv` citation on 6b-mc now backs only the distractor's command, not a locking claim; harmless.
- 006: Gone as to substance: the page's Requirements paragraph reads "Terraform v1.1 and later is required to use moved blocks ... Instead, use the terraform state mv CLI command", so "(on versions older than 1.1 ...)" is the correct antecedent. Punctuation defect: see AWS-Qg6-007.

### New findings

**AWS-Qg6-006 (Low, 6c-mc rationale).** "Workspaces do not change the one-block rule, so a cloud block cannot sit beside a backend block." The "so" is a non sequitur: the cloud/backend exclusion does not follow from workspaces. Fix: "Workspaces do not change the one-block rule. A cloud block cannot sit beside a backend block either."

**AWS-Qg6-007 (Low, lesson 6d `moved` bullet).** Current text reads "... later ("Terraform v1.1 and later is required to use moved blocks"); (on versions older than 1.1 the page says "Instead, use the terraform state mv CLI command") `terraform state mv` is the CLI version:" with a stray semicolon, a second parenthesis and a missing sentence break. Fix: "... later ("Terraform v1.1 and later is required to use moved blocks"); on versions older than 1.1 the page says "Instead, use the terraform state mv CLI command." `terraform state mv` is the CLI version:". No question depends on it.

Neither new item blocks closure; both are editorial and no claim row or key is affected.

Task tf-g6: close (AWS-Qg6-001..005 Gone; 006 and 007 are Low wording nits the Lead Dev may fix inline)

Overall: approve
