# Lesson tf-g6 (Terraform state) -- implementation report

## Summary

Replaced the placeholder `bodyMarkdown` in `content/lessons/lesson-tf-g6.json` with a full lesson: one `##` title, one `###` per objective in id order (tf.004.6a to 6d, headings `### tf.004.6x -- <objective text>`), each ending with a single `**Exam tip:**` line, then the standard `### Warnings` section. Markdown subset only (no tables, links, numbered lists, fenced code or single-asterisk italics). `id`, `title`, `module`, `tier`, `practiceMode`, `objectiveIds` and `labIds` are unchanged. `drillIds` now lists all 12 ids (`-mc`, `-mc2`, `-mr` per objective) in objective order. `citationIds` lists 25 new files, one per doc page, `cite-tf-g6-*.json`, all `accessed: "2026-09-26"`; the shared `cite-tf-004` was not touched and is no longer referenced by this lesson.

Doc method: every page was fetched this turn with `curl -sL` piped through a small Python HTML-to-text stripper (scratchpad `g6w_fetch.py`); no WebFetch. Every quote in the claim table below, and every double-quoted span in the lesson body, was machine-checked as a verbatim substring of that fetched text (whitespace collapsed; `g6w_claims.py` for the table, `g6w_qcheck.py` for the body). Only my own exam-tip scenario phrases are quoted without a page match, by design (16 of them, all inside `**Exam tip:**` lines). No terraform command, no AWS call, no git command was run.

Version floors stated in the lesson, each with its source row:
- `-refresh-only`: Terraform v0.15.4 or later (row 83).
- `import` block (configuration-driven import): Terraform 1.5 or later (row 94, from the drift tutorial). The `plan` page still labels `-generate-config-out` experimental (row 95).
- `moved` block: Terraform v1.1 or later (row 101).
- remove-and-import workflow with `removed` and `import` blocks: Terraform 1.7 or newer (row 106). The page states this for the combined workflow; the lesson says exactly that and does not claim a separate floor for the `removed` block alone.

S3 backend locking, exactly as the page states it: locking is opt-in; "Locking can be enabled via S3 or DynamoDB"; S3 locking uses `use_lockfile`, default false; "DynamoDB-based locking is deprecated and will be removed in a future minor version"; both sets of arguments can be configured simultaneously to ease migration. The page gives no version number for `use_lockfile`, so the lesson states none.

One doc tension flagged for reviewers (not copied into the lesson as a claim): the `removed` block page opens with "The removed block specifies a resource to remove from state without changing the underlying infrastructure," but its `lifecycle` section says the default is destroy ("By default, Terraform removes the resource from state and destroys the actual resource"). The lesson teaches the default-destroy rule (rows 104-105) and `destroy = false` to keep the object, which is what the spec section and the remove-from-state page state. Questions should not rest on the intro sentence.

## Three distinct facts per objective (question plan)

Each objective has far more than three separable facts; the three below are the ones each question set should use, one per question, none overlapping.

- 6a Describe the local backend
  - Q1: no `backend` block means the local backend; state is `terraform.tfstate` relative to the root module (`path`; `workspace_dir` for non-default workspaces); previous state kept in `terraform.tfstate.backup`.
  - Q2: what a local file lacks: it limits collaboration and risks loss if the file is lost; each user must have the latest state and nobody else may run at the same time (the backend does lock via system APIs, but the file is on one machine).
  - Q3: `-state`, `-state-out`, `-backup` are legacy local-backend-only options that have no effect under another backend (also: removing the backend block prompts to migrate state back to local).
- 6b Describe state locking
  - Q1: locking is automatic on all state-writing operations but only if the backend supports it; if the lock fails Terraform does not continue; not all backends support locking.
  - Q2: `-lock-timeout` (default 0s, immediate failure) versus `-lock=false` (disables locking, not recommended, dangerous with concurrent users).
  - Q3: `force-unlock` takes a lock ID, is only for your own lock after automatic unlocking failed, risks multiple writers otherwise; or, as the S3 variant, `use_lockfile` (opt-in, default false) versus the deprecated DynamoDB `LockID` table.
- 6c Configure remote state using the backend block
  - Q1: backend block limits: nested in `terraform`, only one, cannot refer to variables/locals/data sources; `cloud` and `backend` are mutually exclusive (HCP Terraform manages state).
  - Q2: partial configuration: empty `backend` block naming the type, remaining values via `-backend-config` (file or KEY=VALUE) or interactively; later options override; credentials via environment variables, otherwise values land in `.terraform` and plan files.
  - Q3: changing a backend requires `terraform init` again; `-migrate-state` copies existing state, `-reconfigure` disregards the old configuration and does not migrate; `-force-copy`; back up state first.
- 6d Manage resource drift and Terraform state
  - Q1: `plan -refresh-only` / `apply -refresh-only` update state to match reality without changing infrastructure (0.15.4+); a normal plan would revert; `terraform refresh` deprecated alias with auto-approve.
  - Q2: `import` block (1.5+, `to`/`id`, needs a destination resource block, previewed in plan, `-generate-config-out` experimental) versus the `terraform import ADDRESS ID` command.
  - Q3: `moved` block (1.1+) / `state mv` rename without destroying; `removed` block (default destroys, `destroy = false` keeps; 1.7+ workflow) / `state rm` forget; do not hand-edit the state JSON.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 6a | The default backend is local | https://developer.hashicorp.com/terraform/language/backend | "Terraform uses a backend called local by default." |
| 2 | 6a | The local backend stores state on the local filesystem, locks it using system APIs, and runs operations locally | https://developer.hashicorp.com/terraform/language/backend/local | "The local backend stores state on the local filesystem, locks that state using system APIs, and performs operations locally." |
| 3 | 6a | No backend block is needed to use the local backend | https://developer.hashicorp.com/terraform/language/backend/local | "default to the local backend by not specifying a backend at all" |
| 4 | 6a | path is optional and defaults to terraform.tfstate relative to the root module | https://developer.hashicorp.com/terraform/language/backend/local | "defaults to "terraform.tfstate" relative to the root module" |
| 5 | 6a | path is an optional argument naming the tfstate file | https://developer.hashicorp.com/terraform/language/backend/local | "path - (Optional) The path to the tfstate file." |
| 6 | 6a | workspace_dir sets the path for non-default workspaces | https://developer.hashicorp.com/terraform/language/backend/local | "workspace_dir - (Optional) The path to non-default workspaces." |
| 7 | 6a | Terraform keeps a backup of the previous state in terraform.tfstate.backup | https://developer.hashicorp.com/terraform/language/state | "a backup of the previous state in terraform.tfstate.backup" |
| 8 | 6a | Local state limits collaboration and risks losing state if the file is lost | https://developer.hashicorp.com/terraform/language/state | "limits the ability to collaborate with others, and risks losing workspace state if the local state file is lost" |
| 9 | 6a | With a local file each user must make sure they have the latest state | https://developer.hashicorp.com/terraform/language/state/remote | "each user must make sure they always have the latest state data before running Terraform" |
| 10 | 6a | With a local file each user must also make sure nobody else runs Terraform at the same time | https://developer.hashicorp.com/terraform/language/state/remote | "make sure that nobody else runs Terraform at the same time" |
| 11 | 6a | -state, -state-out and -backup are legacy local-backend options that are no longer recommended | https://developer.hashicorp.com/terraform/language/backend/local | "describes legacy features that we've preserved for backward compatibility but that we no longer recommend" |
| 12 | 6a | The three legacy options have no effect under a different backend type | https://developer.hashicorp.com/terraform/language/backend/local | "These three options have no effect for configurations that have a different backend type selected." |
| 13 | 6a | The recommended replacement is a backend that supports remote state | https://developer.hashicorp.com/terraform/language/backend/local | "select a different backend which supports remote state" |
| 14 | 6a | Removing the backend block and reinitializing prompts to migrate state back to local | https://developer.hashicorp.com/terraform/language/backend | "Terraform also prompts you to migrate the state to the default local backend." |
| 15 | 6b | Terraform locks state for write operations if the backend supports it | https://developer.hashicorp.com/terraform/language/state/locking | "If supported by your backend, Terraform will lock your state for all operations that could write state." |
| 16 | 6b | Locking prevents others acquiring the lock and corrupting state | https://developer.hashicorp.com/terraform/language/state/locking | "This prevents others from acquiring the lock and potentially corrupting your state." |
| 17 | 6b | Locking is automatic on all operations that could write state | https://developer.hashicorp.com/terraform/language/state/locking | "State locking happens automatically on all operations that could write state." |
| 18 | 6b | Terraform shows no message that locking happens | https://developer.hashicorp.com/terraform/language/state/locking | "You do not see any message that it happens." |
| 19 | 6b | If locking fails Terraform does not continue | https://developer.hashicorp.com/terraform/language/state/locking | "If state locking fails, Terraform does not continue." |
| 20 | 6b | Not all backends support locking | https://developer.hashicorp.com/terraform/language/state/locking | "Not all backends support locking." |
| 21 | 6b | HCP Terraform supports an even stronger locking concept | https://developer.hashicorp.com/terraform/language/state/remote | "supports an even stronger locking concept" |
| 22 | 6b | HCP Terraform queues operations in a central location | https://developer.hashicorp.com/terraform/language/state/remote | "by queuing Terraform operations in a central location" |
| 23 | 6b | -lock-timeout sets how long Terraform waits to acquire a lock | https://developer.hashicorp.com/terraform/cli/commands/init | "Override the time Terraform will wait to acquire a state lock." |
| 24 | 6b | The default lock timeout is 0s, failing immediately if the lock is held | https://developer.hashicorp.com/terraform/cli/commands/init | "The default is 0s (zero seconds), which causes immediate failure if the lock is already held by another process." |
| 25 | 6b | -lock=false disables locking for most commands but is not recommended | https://developer.hashicorp.com/terraform/language/state/locking | "You can disable state locking for most commands with the -lock=false flag, but we do not recommend it." |
| 26 | 6b | -lock=false is dangerous if others may run commands against the same workspace | https://developer.hashicorp.com/terraform/cli/commands/state/mv | "This is dangerous if others might concurrently run commands against the same workspace." |
| 27 | 6b | force-unlock is only for your own lock after automatic unlocking failed | https://developer.hashicorp.com/terraform/language/state/locking | "Force unlock should only be used to unlock your own lock in the situation where automatic unlocking failed." |
| 28 | 6b | Unlocking someone else's held lock could cause multiple writers | https://developer.hashicorp.com/terraform/language/state/locking | "If you unlock the state when someone else is holding the lock it could cause multiple writers." |
| 29 | 6b | force-unlock requires a unique lock ID | https://developer.hashicorp.com/terraform/language/state/locking | "the force-unlock command requires a unique lock ID" |
| 30 | 6b | Terraform outputs the lock ID if unlocking fails | https://developer.hashicorp.com/terraform/language/state/locking | "Terraform will output this lock ID if unlocking fails." |
| 31 | 6b | force-unlock does not modify infrastructure | https://developer.hashicorp.com/terraform/cli/commands/force-unlock | "The terraform force-unlock command does not modify your infrastructure." |
| 32 | 6b | Local state files cannot be unlocked by another process | https://developer.hashicorp.com/terraform/cli/commands/force-unlock | "Local state files cannot be unlocked by another process." |
| 33 | 6b | S3 locking is opt-in | https://developer.hashicorp.com/terraform/language/backend/s3 | "State locking is an opt-in feature of the S3 backend." |
| 34 | 6b | Locking can be enabled via S3 or DynamoDB | https://developer.hashicorp.com/terraform/language/backend/s3 | "Locking can be enabled via S3 or DynamoDB." |
| 35 | 6b | use_lockfile is optional and defaults to false | https://developer.hashicorp.com/terraform/language/backend/s3 | "Whether to use a lockfile for locking the state file. Defaults to false." |
| 36 | 6b | DynamoDB-based locking is deprecated and will be removed in a future minor version | https://developer.hashicorp.com/terraform/language/backend/s3 | "DynamoDB-based locking is deprecated and will be removed in a future minor version." |
| 37 | 6b | dynamodb_table names the table used for locking | https://developer.hashicorp.com/terraform/language/backend/s3 | "Name of the DynamoDB Table to use for state locking and consistency." |
| 38 | 6b | The DynamoDB table needs a partition key LockID of type String | https://developer.hashicorp.com/terraform/language/backend/s3 | "The table must have a partition key named LockID with a type of String." |
| 39 | 6b | S3 and DynamoDB locking arguments can be set at the same time | https://developer.hashicorp.com/terraform/language/backend/s3 | "the S3 and DynamoDB arguments can be configured simultaneously" |
| 40 | 6b | With use_lockfile, Get/Put/DeleteObject permissions are needed on the lock file | https://developer.hashicorp.com/terraform/language/backend/s3 | "If use_lockfile is set, s3:GetObject, s3:PutObject, and s3:DeleteObject are required on the lock file" |
| 41 | 6c | Remote state is written to a remote data store shared by the team | https://developer.hashicorp.com/terraform/language/state/remote | "writes the state data to a remote data store, which can then be shared between all members of a team" |
| 42 | 6c | Remote state is implemented by a backend or HCP Terraform | https://developer.hashicorp.com/terraform/language/state/remote | "Remote state is implemented by a backend or by HCP Terraform" |
| 43 | 6c | A backend is configured as a backend block nested in the terraform block | https://developer.hashicorp.com/terraform/language/backend | "add a nested backend block within the top-level terraform block" |
| 44 | 6c | Backend block arguments are specific to the backend type | https://developer.hashicorp.com/terraform/language/backend | "The arguments in the backend block body are specific to the backend type." |
| 45 | 6c | The S3 backend stores state as a key in a bucket | https://developer.hashicorp.com/terraform/language/backend/s3 | "Stores the state as a given key in a given bucket on Amazon S3." |
| 46 | 6c | Backends cannot be loaded as plugins | https://developer.hashicorp.com/terraform/language/backend | "You cannot load additional backends as plugins." |
| 47 | 6c | The backend type must be available in your Terraform version | https://developer.hashicorp.com/terraform/language/backend | "The specified backend must be available in the version of Terraform you are using." |
| 48 | 6c | Only one backend block per configuration | https://developer.hashicorp.com/terraform/language/backend | "A configuration can only provide one backend block." |
| 49 | 6c | A backend block cannot refer to named values | https://developer.hashicorp.com/terraform/language/backend | "A backend block cannot refer to named values (like input variables, locals, or data source attributes)." |
| 50 | 6c | A cloud block and a backend block cannot coexist | https://developer.hashicorp.com/terraform/language/backend | "If your configuration includes a cloud block, it cannot include a backend block." |
| 51 | 6c | Do not configure a backend when connecting to HCP Terraform or Terraform Enterprise workspaces | https://developer.hashicorp.com/terraform/language/backend | "Do not configure a backend when connecting your configuration to workspaces in HCP Terraform or Terraform Enterprise." |
| 52 | 6c | HCP Terraform and Terraform Enterprise manage state in the associated workspaces | https://developer.hashicorp.com/terraform/language/backend | "These systems automatically manage state in the workspaces associated with your configuration." |
| 53 | 6c | The cloud block cannot refer to named values | https://developer.hashicorp.com/terraform/language/block/terraform | "The cloud block cannot refer to named values, such as input variables, locals, or data source attributes." |
| 54 | 6c | Only one cloud block per configuration | https://developer.hashicorp.com/terraform/language/block/terraform | "You can only provide one cloud block per configuration." |
| 55 | 6c | Definition of partial configuration | https://developer.hashicorp.com/terraform/language/backend | "When some or all of the arguments are omitted, we call this a partial configuration." |
| 56 | 6c | Remaining arguments must be supplied at initialization | https://developer.hashicorp.com/terraform/language/backend | "the remaining configuration arguments must be provided as part of the initialization process" |
| 57 | 6c | A file is supplied with -backend-config=PATH on init | https://developer.hashicorp.com/terraform/language/backend | "use the -backend-config=PATH option when running terraform init" |
| 58 | 6c | A single key/value pair is supplied with -backend-config="KEY=VALUE" | https://developer.hashicorp.com/terraform/language/backend | "use the -backend-config="KEY=VALUE" option" |
| 59 | 6c | Terraform can ask interactively for the remaining values | https://developer.hashicorp.com/terraform/language/backend | "Terraform will interactively ask you for the required values" |
| 60 | 6c | An empty backend block in a root file specifies the backend type | https://developer.hashicorp.com/terraform/language/backend | "an empty backend configuration is specified in one of the root Terraform configuration files, to specify the backend type" |
| 61 | 6c | Command-line options override settings in the main configuration | https://developer.hashicorp.com/terraform/language/backend | "any command-line options override the settings in the main configuration" |
| 62 | 6c | Later -backend-config options override earlier ones | https://developer.hashicorp.com/terraform/language/backend | "with later options overriding values set by earlier options" |
| 63 | 6c | Use environment variables for credentials and sensitive data | https://developer.hashicorp.com/terraform/language/backend | "We recommend using environment variables to supply credentials and other sensitive data." |
| 64 | 6c | The warning applies to -backend-config and hardcoded values | https://developer.hashicorp.com/terraform/language/backend | "If you use -backend-config or hardcode these values directly in your configuration" |
| 65 | 6c | Such values are written into .terraform and plan files | https://developer.hashicorp.com/terraform/language/backend | "Terraform will include these values in both the .terraform subdirectory and in plan files." |
| 66 | 6c | .terraform/terraform.tfstate holds the backend configuration | https://developer.hashicorp.com/terraform/language/backend | "The .terraform/terraform.tfstate file contains the backend configuration for the current working directory." |
| 67 | 6c | The .terraform directory must not be checked into Git | https://developer.hashicorp.com/terraform/language/backend | "Do not check this directory into Git, as it may contain sensitive credentials for your remote backend." |
| 68 | 6c | Changing backend configuration requires running init again | https://developer.hashicorp.com/terraform/language/backend | "When you change a backend's configuration, you must run terraform init again" |
| 69 | 6c | Terraform asks about migrating state when the backend changes | https://developer.hashicorp.com/terraform/language/backend | "Terraform will ask if you'd like to migrate your existing state to the new configuration" |
| 70 | 6c | -migrate-state copies existing state to the new backend | https://developer.hashicorp.com/terraform/cli/commands/init | "The -migrate-state option will attempt to copy existing state to the new backend" |
| 71 | 6c | -reconfigure disregards existing configuration and prevents migration | https://developer.hashicorp.com/terraform/cli/commands/init | "The -reconfigure option disregards any existing configuration, preventing migration of any existing state." |
| 72 | 6c | Re-running init needs -reconfigure or -migrate-state to update the backend | https://developer.hashicorp.com/terraform/cli/commands/init | "Either -reconfigure or -migrate-state must be supplied to update the backend configuration." |
| 73 | 6c | -force-copy suppresses migration prompts | https://developer.hashicorp.com/terraform/cli/commands/init | "The -force-copy option suppresses these prompts" |
| 74 | 6c | -force-copy also enables -migrate-state | https://developer.hashicorp.com/terraform/cli/commands/init | "Enabling -force-copy also automatically enables the -migrate-state option." |
| 75 | 6c | Back up state before migrating to a new backend | https://developer.hashicorp.com/terraform/language/backend | "we strongly recommend manually backing up your state by copying your terraform.tfstate file to another location" |
| 76 | 6d | Manual changes make state drift from real infrastructure | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "out of sync, or "drift," from the real infrastructure" |
| 77 | 6d | Manual changes to Terraform-controlled resources are discouraged | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "You should not make manual changes to resources controlled by Terraform" |
| 78 | 6d | plan and apply compare state to real infrastructure by default | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "Terraform compares your state file to real infrastructure whenever you invoke terraform plan or terraform apply." |
| 79 | 6d | Without -refresh-only, Terraform would attempt to revert manual changes | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "without the -refresh-only flag now, Terraform would attempt to revert your manual changes" |
| 80 | 6d | Refresh-only mode updates state and root outputs to match outside changes | https://developer.hashicorp.com/terraform/cli/commands/plan | "update the Terraform state and any root module output values to match changes made to remote objects outside of Terraform" |
| 81 | 6d | Applying a refresh-only plan records new values in state without changing remote objects | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "apply this plan to record the updated values in the Terraform state without changing any remote objects" |
| 82 | 6d | A refresh-only operation does not modify infrastructure to match the configuration | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "A refresh-only operation does not attempt to modify your infrastructure to match your Terraform configuration" |
| 83 | 6d | -refresh-only requires Terraform v0.15.4 or later | https://developer.hashicorp.com/terraform/cli/commands/plan | "The -refresh-only option is available only in Terraform v0.15.4 and later." |
| 84 | 6d | terraform refresh is deprecated | https://developer.hashicorp.com/terraform/cli/commands/refresh | "This command is deprecated." |
| 85 | 6d | terraform refresh is an alias for apply -refresh-only -auto-approve | https://developer.hashicorp.com/terraform/cli/commands/refresh | "This command is effectively an alias for the following command: terraform apply -refresh-only -auto-approve" |
| 86 | 6d | terraform refresh overwrites state without showing the updates | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "automatically overwrites your state file without displaying the updates" |
| 87 | 6d | An import block requires the resource ID to import | https://developer.hashicorp.com/terraform/language/import | "Importing unmanaged resources to your workspace requires an import block that specifies the unique infrastructure resource ID to import." |
| 88 | 6d | import block id is the provider ID of the resource | https://developer.hashicorp.com/terraform/language/block/import | "The id argument specifies the cloud provider's ID for the resource you want to import." |
| 89 | 6d | The to argument must match an existing resource block address | https://developer.hashicorp.com/terraform/language/block/import | "The to argument must match the address of an existing resource block." |
| 90 | 6d | A destination resource block matching the import address is required | https://developer.hashicorp.com/terraform/language/import | "you must create a destination resource block that matches the address declared in the import block" |
| 91 | 6d | A resource block is needed for any resource in state or Terraform will destroy it | https://developer.hashicorp.com/terraform/language/import/single-resource | "you must define a resource block for any resource in state to prevent Terraform from destroying it" |
| 92 | 6d | Run plan to preview an import | https://developer.hashicorp.com/terraform/language/state/refactor | "Run terraform plan to ensure that Terraform will properly import the resources." |
| 93 | 6d | The import block imports when terraform apply runs | https://developer.hashicorp.com/terraform/cli/commands/import | "Terraform imports resources when you run the terraform apply command" |
| 94 | 6d | Configuration-driven import needs Terraform 1.5 or later | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | "Terraform 1.5+ supports configuration-driven import" |
| 95 | 6d | -generate-config-out generates HCL for imported resources and is experimental | https://developer.hashicorp.com/terraform/cli/commands/plan | "(Experimental) If import blocks are present in configuration, instructs Terraform to generate HCL for any imported resources not already present." |
| 96 | 6d | The -generate-config-out file must not already exist | https://developer.hashicorp.com/terraform/cli/commands/plan | "The configuration is written to a new file at PATH, which must not already exist, or Terraform will error." |
| 97 | 6d | terraform import ADDRESS ID imports an existing resource into state at an address | https://developer.hashicorp.com/terraform/cli/commands/import | "Import will find the existing resource from ID and import it into your Terraform state at the given ADDRESS." |
| 98 | 6d | Import each remote object to only one resource address | https://developer.hashicorp.com/terraform/cli/commands/import | "be careful to import each remote object to only one Terraform resource address" |
| 99 | 6d | A moved block updates an address without destroying the resource | https://developer.hashicorp.com/terraform/language/modules/develop/refactoring | "You can use a moved block to update a resource address without destroying it." |
| 100 | 6d | Without moved, a renamed address is treated as destroy plus create | https://developer.hashicorp.com/terraform/language/modules/develop/refactoring | "interprets a change as an instruction to destroy the existing resource and create a new resource at the new address" |
| 101 | 6d | moved blocks need Terraform v1.1 or later | https://developer.hashicorp.com/terraform/language/modules/develop/refactoring | "Terraform v1.1 and later is required to use moved blocks to explicitly refactor module addresses" |
| 102 | 6d | state mv changes bindings so existing remote objects bind to new resource instances | https://developer.hashicorp.com/terraform/cli/commands/state/mv | "The terraform state mv command changes bindings in Terraform state so that existing remote objects bind to new resource instances." |
| 103 | 6d | state mv can only move to a new address of the same resource type | https://developer.hashicorp.com/terraform/cli/commands/state/mv | "you can only move it to a new address with the same resource type" |
| 104 | 6d | removed block default is to remove from state and destroy the real resource | https://developer.hashicorp.com/terraform/language/block/removed | "By default, Terraform removes the resource from state and destroys the actual resource." |
| 105 | 6d | destroy = false removes from state without destroying | https://developer.hashicorp.com/terraform/language/block/removed | "Set destroy to false to remove the resource from state without destroying the actual resource." |
| 106 | 6d | Remove-and-import with these blocks requires Terraform 1.7 or newer | https://developer.hashicorp.com/terraform/language/state/refactor | "Removing and importing resources requires Terraform version 1.7 or newer." |
| 107 | 6d | state rm removes the binding without destroying the remote object | https://developer.hashicorp.com/terraform/cli/commands/state/rm | "The terraform state rm command removes the binding to an existing remote object without first destroying it." |
| 108 | 6d | After state rm a later plan proposes creating a new object for each forgotten instance | https://developer.hashicorp.com/terraform/cli/commands/state/rm | "will include an action to create a new object for each of the "forgotten" instances" |
| 109 | 6d | The removed block is recommended over state rm | https://developer.hashicorp.com/terraform/language/state/remove | "we recommend using the removed block instead" |
| 110 | 6d | The removed block lets you preview the operation | https://developer.hashicorp.com/terraform/language/state/remove | "the removed block lets you preview the results of the operation" |
| 111 | 6d | state list lists resources within state | https://developer.hashicorp.com/terraform/cli/commands/state/list | "The terraform state list command lists resources within a Terraform state." |
| 112 | 6d | state show shows the attributes of a single resource | https://developer.hashicorp.com/terraform/cli/commands/state/show | "The terraform state show command shows the attributes of a single resource in the Terraform state." |
| 113 | 6d | Read-only subcommands such as list write no backup | https://developer.hashicorp.com/terraform/cli/commands/state | "Subcommands that are read-only (such as list) do not write any backup files" |
| 114 | 6d | State is stored as JSON and should not be edited directly | https://developer.hashicorp.com/terraform/language/state | "Terraform stores your workspaces state as a JSON text file. Do not directly edit this file." |
| 115 | 6d | The state commands exist to modify state instead of editing it directly | https://developer.hashicorp.com/terraform/cli/commands/state | "You can use the terraform state commands to modify the Terraform state instead modifying the state directly." |
| 116 | 6d | Every state modification command writes a backup | https://developer.hashicorp.com/terraform/cli/commands/state | "Terraform forces every state modification command to write a backup file." |
| 117 | 6d | Terraform expects a one-to-one mapping between resource instances and remote objects | https://developer.hashicorp.com/terraform/language/state | "Terraform expects a one-to-one mapping between configured resource instances and remote objects." |
| 118 | 6d | Importing or state rm changes bindings so you must keep the one-to-one rule true | https://developer.hashicorp.com/terraform/language/state | "you'll then need to ensure for yourself that this one-to-one rule is followed" |
| 119 | Warnings | State data contains extremely sensitive information | https://developer.hashicorp.com/terraform/language/backend | "state data contains extremely sensitive information" |
| 120 | Warnings | Storing state in version control can cause data loss or secret exposure | https://developer.hashicorp.com/terraform/language/state | "can result in data loss or exposure of secrets stored in the state file" |

## Self-consistency check

Each section was re-read in isolation against its own claim-table rows (RULES.md "After applying a fix", step 2), with the prose sentence covered except for what the row's quote supports.

- 6a: every sentence is backed by rows 1-14. Two sentences go slightly beyond a single quote and are written as inference, not as doc quotes: that the local file "still sits on one machine" (a consequence of rows 2, 8-9, not a doc sentence), and that the local backend locks "but the file still sits on one machine, so a team needs a remote backend". Rows 8 and 9 (remote-state page) are what the lesson cites for the team problem. No claim that local locking cannot protect other machines is attributed to the docs.
- 6b: rows 15-40. The `-lock=false` danger quote comes from the `state mv` page (row 26) and the lesson says "the state-modifying commands warn", which matches that page (the same sentence is on `state rm` and `import`). "So a plain run that meets a held lock fails at once" is an inference from the 0s default (row 24) and is stated as such by its wording. "An S3 backend with no locking arguments does not lock" follows from rows 33-35 (opt-in, `use_lockfile` default false).
- 6c: rows 41-75. The `cloud` versus `backend` rule is stated in both directions by the docs (rows 50-51 and 53-54), and the lesson says "mutually exclusive" only. Credential rows 64-65 are split so the condition (hardcoded or `-backend-config`) and the consequence (`.terraform` and plan files) are each exactly quoted.
- 6d: rows 76-118. The default-destroy behavior of `removed` (rows 104-105) is the opposite of what a reader might assume from `terraform state rm`; the lesson states both. Version floors are tied to the correct feature (see Summary). The `refresh` row 84 says "deprecated" and the lesson also says it overwrites state without review (row 86 from the drift tutorial: "automatically overwrites your state file without displaying the updates").
- Warnings: rows 119-120 plus rows already used above. The bullet about group 4 section 4h states only that 4h covers how secret values reach state (no quote), which matches that section.

### Where the lesson touches tf-g3, and why there is no contradiction

- 3b says init consults backend configuration, that "remote backends are a later objective", that the default backend is the local state file, and that init must be re-run when the backend block changes. 6a-6c are that later objective and agree: default local, `terraform init` again after a backend change (row 68).
- 3d teaches `-refresh-only` with the exact "update the Terraform state and any root module output values to match changes made to remote objects outside of Terraform" sentence; 6d reuses the same sentence and adds the apply side, the 0.15.4 floor, and `terraform refresh`. g3's 0.15.2 boundary is for `-destroy` on `apply`, a different feature; 6d states only 0.15.4 for `-refresh-only`. No conflict.
- 3e: `-auto-approve` skips the prompt. 6d says `terraform refresh` is an alias that includes `-auto-approve` (so it applies with no review) while `apply -refresh-only` is the reviewed form; consistent with 3e's "drops the wait".
- 3c/3b: `init -backend=false` is not mentioned in 6c, so nothing there to conflict with g3's use of it for validate.
- 3f/3d: `-target` and the directionality rule are not used in g6.
- g2 (2d) says remote backends and locking are covered in group 6 and that `terraform.tfstate` defaults to local plain JSON; 6a agrees. g4 (4h): state holds secrets; 6 Warnings cross-references 4h without restating its quotes.

No sentence in the lesson contradicts another: in particular the lesson says `-lock=false` is discouraged in 6b and again in Warnings, `force-unlock` is for your own lock in both 6b and Warnings, and `removed` defaults to destroy in 6d and only the `destroy = false` form keeps the object in both the body and the exam tip.

## Reviewer notes

- Lesson-only chain lines pass (see outputs below). Question-line FAILs are expected: the 12 questions are still the generic placeholders (objective text pasted in stems, no citationIds, no mcpStatus, placeholder stems, duplicate 6-word openings, longest-is-key 50 percent, MR key-set concentration). They are the next pipeline step, not lesson defects.
- `lesson-tf-g6.json` tier/module strings and the existing `title` ("T3 - Terraform state") are unchanged.
- Heading texts were checked against `content/objectives/terraform_004.json` and match exactly.
- Retired/closed services list: none of those services is mentioned.
- The lesson never states a version for `use_lockfile`, because the S3 page does not.

## Script outputs (exact)

### scripts\content_lint.py
```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
```

### scripts\q1_batch_check.py tf-g6 (lesson lines PASS; every FAIL is a question line, because the 12 questions are still placeholders)
```
task tf-g6: 12 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 4 for 4 objectives
FAIL: q-tf-004-6a-mc choice c: pastes objective text
FAIL: q-tf-004-6a-mc: stem pastes objective text
FAIL: q-tf-004-6a-mc: no citationIds
FAIL: q-tf-004-6a-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6a-mc: still a placeholder stem
FAIL: q-tf-004-6a-mc2 choice a: pastes objective text
FAIL: q-tf-004-6a-mc2: stem pastes objective text
FAIL: q-tf-004-6a-mc2: no citationIds
FAIL: q-tf-004-6a-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6a-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-6a-mr: stem pastes objective text
FAIL: q-tf-004-6a-mr: no citationIds
FAIL: q-tf-004-6a-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6b-mc: no citationIds
FAIL: q-tf-004-6b-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6b-mc2: no citationIds
FAIL: q-tf-004-6b-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6b-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-6b-mr: no citationIds
FAIL: q-tf-004-6b-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6c-mc choice b: pastes objective text
FAIL: q-tf-004-6c-mc: stem pastes objective text
FAIL: q-tf-004-6c-mc: no citationIds
FAIL: q-tf-004-6c-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6c-mc2 choice c: pastes objective text
FAIL: q-tf-004-6c-mc2: stem pastes objective text
FAIL: q-tf-004-6c-mc2: no citationIds
FAIL: q-tf-004-6c-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6c-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-6c-mr: stem pastes objective text
FAIL: q-tf-004-6c-mr: no citationIds
FAIL: q-tf-004-6c-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6d-mc choice d: pastes objective text
FAIL: q-tf-004-6d-mc: stem pastes objective text
FAIL: q-tf-004-6d-mc: no citationIds
FAIL: q-tf-004-6d-mc: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6d-mc2 choice a: pastes objective text
FAIL: q-tf-004-6d-mc2: stem pastes objective text
FAIL: q-tf-004-6d-mc2: no citationIds
FAIL: q-tf-004-6d-mc2: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: q-tf-004-6d-mr: MR stem lacks '(Select N.)'
FAIL: q-tf-004-6d-mr: stem pastes objective text
FAIL: q-tf-004-6d-mr: no citationIds
FAIL: q-tf-004-6d-mr: mcpStatus/reviewedOn not verified/2026-09-26
FAIL: duplicate 6-word openings: ['select two actions that support this', 'a teammate asks how to meet']
FAIL: longest-is-key 4/8 = 50%
PASS: shortest-is-key 2/8 = 25%
PASS: MC key positions {'a': 2, 'b': 1, 'c': 3, 'd': 2}
PASS: MR key slots {'a': 2, 'b': 2, 'c': 1, 'd': 2, 'e': 1}
FAIL: MR key sets: most common 'a,b' in 2/4 (50%); all {'a,b': 2, 'c,d': 1, 'd,e': 1}
RESULT: FAIL
```

### scripts\claim_prose_check.py tf-g6
```
task tf-g6: 8 distinct numbers in lesson prose
PASS: every claim-table number appears in the lesson prose
```

Overall: approve
