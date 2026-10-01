# Lesson tf-g7 (Maintain infrastructure) -- implementation report

## Summary

Replaced the placeholder `bodyMarkdown` in `content/lessons/lesson-tf-g7.json` with a full lesson: one `##` title, one `###` per objective in id order (`### tf.004.7a`, `7b`, `7c`, each with the objective text), each ending in one `**Exam tip:**` line, then the standard `### Warnings` section. Markdown subset only. `####` sub-headings split each objective into short topics. `id`, `title`, `module`, `tier`, `practiceMode`, `objectiveIds` and `labIds` are unchanged. `drillIds` lists all 9 ids (`-mc`, `-mc2`, `-mr` for 7a, 7b, 7c). `citationIds` lists 18 new files `content/citations/cite-tf-g7-*.json`, one per doc page, `accessed: "2026-09-26"`. The shared `cite-tf-004` is no longer referenced.

Doc method: every page was fetched this turn with `curl -sL` and a Python HTML-to-text strip (scratchpad `g7w_fetch.py`), no WebFetch. Every claim-table quote (104 rows) and every double-quoted span in the lesson body (82, exam-tip lines excluded) was machine-checked as a verbatim substring of that text, whitespace collapsed (`g7w_check.py`); all quotes are 20 words or fewer. Every body quote is also covered by a table row (`g7w_cover.py`). No terraform command, no AWS call and no git command was run.

Doc tensions and gaps, stated so reviewers can check my handling:
- `TF_LOG_PATH`: the debugging and environment-variable pages say `TF_LOG` must be set for any logging to be enabled. The troubleshooting tutorial sets only `TF_LOG_CORE` and `TF_LOG_PROVIDER` together with `TF_LOG_PATH`. The lesson follows the debugging page ("TF_LOG must be set ...") and tells the learner to set a level variable; it does not claim `TF_LOG_CORE` alone is insufficient. Questions should use "`TF_LOG_PATH` alone enables nothing", not "`TF_LOG` specifically is required".
- Sensitive values in logs: no page says a TRACE log contains secrets. The only support is the provider-development note that "there may be sensitive data" in provider logs. The lesson quotes that and labels "read a log before sharing it" as its own inference. A question must not assert that TRACE logs always contain secrets.
- `state show -json` needs Terraform v1.16 or later per its page. It is left out on purpose (too new, version-sensitive).
- `state pull` read-only: the pull page does not say "read-only" or "writes no backup". The lesson says only that it downloads and prints state to stdout. Do not write a question that depends on pull writing no backup.
- Group 3 (3d) is where `-out` was taught, not 3e; the lesson says 3d (a draft had 3e, caught by regex before building).

## Three-facts plan per objective (and how each differs from g6's tested facts)

g6's three 6d questions test: (1) `apply -refresh-only` to record drift without touching the real object (versus `plan -refresh-only`, `refresh`, plain `apply`); (2) import blocks (resource block plus `import` block with `to`/`id`) versus `terraform import` or relying on `apply` to find objects, for many buckets in one reviewed run; (3) MR on `moved` blocks, `removed` with `destroy = false`, `state rm`, and not editing state by hand. g7 questions must stay off all of that.

### 7a Import existing infrastructure
- Q1 (generated configuration is a draft). Test: output of `-generate-config-out` is a best-guess template listing all arguments including defaults, to be pruned and reviewed before apply; the plan after generation can show a replace. New versus g6: g6 only taught that the flag exists, is experimental, and needs a new file. Rows 20-31.
- Q2 (one block, many objects). Test: `for_each` on the `import` block with `to = ...[each.key]` and `id = each.value`, versus separate blocks. New versus g6's 6d-mc2, which tests "import block with `to` and `id`, reviewed in plan, not the CLI command or `moved`"; here the distinguishing fact is `for_each` and the `id` expression rules. Rows 11-19.
- Q3 (ID source and what import does not do). Test: the ID comes from the provider documentation for that resource type and must be known at plan time, or after import Terraform manages the whole lifecycle including destruction and does not create relationships. Rows 2-4, 11-12, 34-39. The MR can pair the lifecycle claim with the no-relationships claim, or with `identity` and `id` being mutually exclusive.
- Avoid in 7a questions: `terraform import` versus the block (6d), the 1.5 floor, and the file-must-not-exist rule (all g6).

### 7b Use the CLI to inspect state
- Q1 (find a resource). Test: `terraform state list -id=...` finds which address holds a given provider ID, or `state list module.x` filters to a module and submodules. 6d only taught `state list` unfiltered. Rows 40-44.
- Q2 (outputs for a script). Test: `terraform output -raw NAME` for a string and `-json` for a list or object; only root module outputs appear; a named sensitive output is not redacted while plain `terraform output` shows `<sensitive>`; ephemeral outputs are omitted. 4h taught only that `-json` and `-raw` print sensitive values. Rows 56-68.
- Q3 (whole state, plan or pull versus push). Test: `terraform show planfile` prints a saved plan; `show -json` exposes sensitive values; `state pull` prints raw state to stdout; `state push` uploads and refuses on differing lineage or a higher remote serial, and `-force` removes those checks. Rows 48-55, 69-78. The MR can pair two of these.

### 7c Verbose logging
- Q1 (levels and format). Test: TRACE is the most verbose and ERROR the least, in decreasing order TRACE, DEBUG, INFO, WARN, ERROR; `TF_LOG=JSON` is a TRACE-level parseable format that is not a stable interface; logs go to stderr by default. Rows 79-88.
- Q2 (core versus provider, precedence). Test: `TF_LOG_CORE` is Terraform itself and excludes providers; `TF_LOG_PROVIDER` is plugins; `TF_LOG` overrides the narrower variables; each helps a different bug report. Rows 89-96.
- Q3 (saving and when). Test: `TF_LOG_PATH` appends to an existing file and does nothing without a level variable; bug reports use TRACE; a log can contain sensitive data so check it before sharing. Rows 97-103. The MR can pair the append behaviour with the bug-report level.
- None of this is in g6.

## Claim table

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---|---|---|---|
| 1 | 7a | Goal: existing infrastructure can be imported so you manage it as code | https://developer.hashicorp.com/terraform/language/import | "If you have existing infrastructure resources, you can import them to your Terraform workspace" |
| 2 | 7a | id is the cloud provider ID of the resource to import | https://developer.hashicorp.com/terraform/language/block/import | "The id argument specifies the cloud provider's ID for the resource you want to import." |
| 3 | 7a | The ID format depends on the resource type | https://developer.hashicorp.com/terraform/language/block/import | "The value of the id argument depends on the type of resource you are importing." |
| 4 | 7a | Find the required ID in the provider documentation | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "You can find the required ID in the provider documentation for the resource you wish to import." |
| 5 | 7a | An import block can sit in any configuration file | https://developer.hashicorp.com/terraform/language/block/import | "You can add an import block to any Terraform configuration file" |
| 6 | 7a | Recommended placement: an imports.tf file or beside the destination resource block | https://developer.hashicorp.com/terraform/language/block/import | "creating an imports.tf file for all import configurations or placing each import block beside the destination resource block" |
| 7 | 7a | Plan reports an import count as its own action (example output) | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Plan: 1 to import, 0 to add, 0 to change, 0 to destroy." |
| 8 | 7a | Apply performs the import; example result line | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed." |
| 9 | 7a | Apply is the step that imports | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Run terraform apply to import your infrastructure." |
| 10 | 7a | Once in state, Terraform no longer needs to generate configuration for it | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "In future planning, Terraform knows it doesn't need to generate configuration for resources that already exist in your state." |
| 11 | 7a | id accepts a string or an expression that evaluates to a string | https://developer.hashicorp.com/terraform/language/block/import | "You must specify a string or an expression that evaluates to a string." |
| 12 | 7a | The id must be known during plan | https://developer.hashicorp.com/terraform/language/block/import | "The ID must be known during the plan operation." |
| 13 | 7a | identity is an object of key-value pairs that uniquely identify a resource | https://developer.hashicorp.com/terraform/language/block/import | "The identity argument is an object of key-value pairs that uniquely identify a resource." |
| 14 | 7a | id and identity cannot be used together | https://developer.hashicorp.com/terraform/language/block/import | "You cannot use the id argument and identity argument in the same import block." |
| 15 | 7a | for_each on an import block imports similar resources without separate blocks | https://developer.hashicorp.com/terraform/language/block/import | "The for_each meta-argument instructs Terraform to import similar resources without requiring separate configuration blocks." |
| 16 | 7a | Docs example: for_each = local.buckets, to uses each.key | https://developer.hashicorp.com/terraform/language/block/import | "to = aws_s3_bucket.this[each.key]" |
| 17 | 7a | Docs example: id = each.value with the for_each map | https://developer.hashicorp.com/terraform/language/block/import | "id = each.value" |
| 18 | 7a | provider meta-argument selects the provider configuration used for the import | https://developer.hashicorp.com/terraform/language/block/import | "The provider meta-argument instructs Terraform to import resources according to the specified provider configuration." |
| 19 | 7a | Docs example imports into aws_instance.web using the east alias | https://developer.hashicorp.com/terraform/language/block/import | "Terraform imports the AWS instance with the ID i-096fba6d03d36d262 to the aws_instance.web resource according to the east alias." |
| 20 | 7a | Generated configuration is a template of best guesses | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "HCL to act as a template that contains Terraform's best guess at the appropriate value for each resource argument" |
| 21 | 7a | Generation covers import-block resources missing from configuration | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "for the resources you define in import blocks that do not already exist in your configuration." |
| 22 | 7a | Generated config contains all arguments including defaults and empty ones | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "The generated configuration contains all possible arguments for the imported resources, including those set to default values" |
| 23 | 7a | Recommendation to prune generated configuration | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "We recommend that you prune the generated configuration to only required arguments" |
| 24 | 7a | Recommendation to prune: also keep arguments whose values differ from defaults | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "arguments whose values differ from defaults" |
| 25 | 7a | Terraform asks you to review generated configuration before version control | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Please review the configuration and edit it as necessary before adding it to version control." |
| 26 | 7a | Generation can fail to build valid configuration for complex schemas | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "For certain resources with complex schemas, Terraform may not be able to construct a valid configuration from these values." |
| 27 | 7a | Example error name is Conflicting configuration arguments | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Error: Conflicting configuration arguments" |
| 28 | 7a | The example conflict is two arguments the resource accepts but you must choose one | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "The resource supports both of these arguments, but you must choose only one when configuring the resource." |
| 29 | 7a | Plan after generation in the tutorial warns it would destroy the imported resource | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "# Warning: this will destroy the imported resource" |
| 30 | 7a | Tutorial: Terraform plans to replace the container after import | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Notice that Terraform plans to replace the container after import" |
| 31 | 7a | Tutorial fixes it by changing a generated value (env to an empty set) | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Change the value of env to an empty set using square brackets." |
| 32 | 7a | A provider block is needed if no other resource uses that provider | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "you must add a provider block to inform Terraform which provider it should use to generate configuration" |
| 33 | 7a | A new provider block needs terraform init again | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "If you add a new provider block to your configuration, you must run terraform init again." |
| 34 | 7a | Import cannot determine health or intent | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "It cannot determine: the health of the infrastructure. the intent of the infrastructure." |
| 35 | 7a | Import does not detect or generate relationships | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Terraform import does not detect or generate relationships between infrastructure." |
| 36 | 7a | Not every provider and resource supports import | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Not all providers and resources support Terraform import." |
| 37 | 7a | Imported object is managed for its whole lifecycle including destruction | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "importing a resource into Terraform means that Terraform will manage the entire lifecycle of the resource, including destruction." |
| 38 | 7a | Back up state before importing | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "You may want to create a backup before importing new infrastructure." |
| 39 | 7a | Tutorial: import manipulates state during apply | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Importing manipulates the Terraform state file during the apply." |
| 40 | 7b | state list usage takes optional addresses | https://developer.hashicorp.com/terraform/cli/commands/state/list | "Usage: terraform state list [options] [address...]" |
| 41 | 7b | Patterns filter and use resource addressing format | https://developer.hashicorp.com/terraform/cli/commands/state/list | "To filter these, provide one or more patterns to the command. Patterns are in resource addressing format." |
| 42 | 7b | Module address lists the module and submodules | https://developer.hashicorp.com/terraform/cli/commands/state/list | "This example will list resources in the given module and any submodules" |
| 43 | 7b | -id flag takes the ID of the resources to show | https://developer.hashicorp.com/terraform/cli/commands/state/list | "-id=id - ID of resources to show." |
| 44 | 7b | -id helps find where a resource is in configuration | https://developer.hashicorp.com/terraform/cli/commands/state/list | "This is useful to find where in your configuration a specific resource is located." |
| 45 | 7b | state show needs an address pointing to a single resource | https://developer.hashicorp.com/terraform/cli/commands/state/show | "This command requires an address that points to a single resource in the state." |
| 46 | 7b | Quote resource names with special characters in single quotes | https://developer.hashicorp.com/terraform/cli/commands/state/show | "You must place the resource name in single quotes when it contains special characters like double quotes." |
| 47 | 7b | State subcommand output is designed for Unix tools | https://developer.hashicorp.com/terraform/cli/commands/state/index | "designed to be usable with Unix command-line tools such as grep, awk, and similar PowerShell commands" |
| 48 | 7b | terraform show: human-readable output from a state or plan file | https://developer.hashicorp.com/terraform/cli/commands/show | "The terraform show command provides human-readable output from a state or plan file." |
| 49 | 7b | show with no path shows the latest state snapshot | https://developer.hashicorp.com/terraform/cli/commands/show | "If you don't specify a file path, Terraform will show the latest state snapshot." |
| 50 | 7b | Saved plans are not human-readable; terraform show prints them | https://developer.hashicorp.com/terraform/tutorials/cli/plan | "Use the terraform show command to print out the saved plan." |
| 51 | 7b | plan -out writes an opaque saved plan file | https://developer.hashicorp.com/terraform/cli/commands/plan | "Writes the generated plan to the given filename in an opaque file format" |
| 52 | 7b | show -json makes machine-readable output | https://developer.hashicorp.com/terraform/cli/commands/show | "Add the -json command-line flag to generate machine-readable output." |
| 53 | 7b | show -json for a plan file gives plan, configuration and current state | https://developer.hashicorp.com/terraform/cli/commands/show | "terraform show -json shows a JSON representation of the plan, configuration, and current state." |
| 54 | 7b | show -json displays sensitive state values in plain text | https://developer.hashicorp.com/terraform/cli/commands/show | "any sensitive values in Terraform state will be displayed in plain text" |
| 55 | 7b | Plan files can contain sensitive data | https://developer.hashicorp.com/terraform/tutorials/cli/plan | "Terraform plan files can contain sensitive data." |
| 56 | 7b | output extracts a value from the state file | https://developer.hashicorp.com/terraform/cli/commands/output | "The terraform output command extracts the value of an output variable from the state file." |
| 57 | 7b | No name shows all root module outputs | https://developer.hashicorp.com/terraform/cli/commands/output | "output will display all the outputs for the root module." |
| 58 | 7b | With a NAME only that output is printed | https://developer.hashicorp.com/terraform/cli/commands/output | "If an output NAME is specified, only the value of that output is printed." |
| 59 | 7b | output shows only root module outputs | https://developer.hashicorp.com/terraform/cli/commands/output | "The terraform output command only displays outputs defined in the root module." |
| 60 | 7b | Expose a child module value with an output in the root module | https://developer.hashicorp.com/terraform/cli/commands/output | "define an output block in your root module using the value of an output from a child module" |
| 61 | 7b | Default output format can change over time | https://developer.hashicorp.com/terraform/cli/commands/output | "which can change over time to improve clarity" |
| 62 | 7b | Use -json for the stable JSON format in scripts | https://developer.hashicorp.com/terraform/cli/commands/output | "For scripting and automation, use -json to produce the stable JSON format." |
| 63 | 7b | -raw supports only string, number, boolean | https://developer.hashicorp.com/terraform/cli/commands/output | "it only supports string, number, and boolean values." |
| 64 | 7b | Use -json for complex data types | https://developer.hashicorp.com/terraform/cli/commands/output | "Use -json instead for processing complex data types." |
| 65 | 7b | Plain terraform output shows <sensitive> for a sensitive output | https://developer.hashicorp.com/terraform/cli/commands/output | "password = <sensitive>" |
| 66 | 7b | Output by name does not redact sensitive values | https://developer.hashicorp.com/terraform/cli/commands/output | "Terraform does not redact sensitive values when you specify the output by name" |
| 67 | 7b | Ephemeral values are omitted even by name | https://developer.hashicorp.com/terraform/cli/commands/output | "Terraform completely omits any ephemeral values, even if you specify an output by name." |
| 68 | 7b | -json and -raw show sensitive values in plain text (repeated from 4h) | https://developer.hashicorp.com/terraform/cli/commands/output | "When using the -json or -raw command-line flags, Terraform displays sensitive values in plain text." |
| 69 | 7b | state pull downloads and outputs state from remote or local | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "The terraform state pull downloads and outputs state information from a remote state or local state." |
| 70 | 7b | state pull outputs the raw format to stdout | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "outputs the raw format to stdout" |
| 71 | 7b | state pull is useful for reading values out of state, e.g. with jq | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "This is useful for reading values out of state (potentially pairing this command with something like jq)." |
| 72 | 7b | state push uploads a local state file to the backend | https://developer.hashicorp.com/terraform/cli/commands/state/push | "The terraform state push command uploads a local state file to remote state or a local state." |
| 73 | 7b | Push recommended only for manual modification of remote state | https://developer.hashicorp.com/terraform/cli/commands/state/push | "We only recommend using this command when you must manually modify the remote state." |
| 74 | 7b | Push safety check: differing lineage | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Differing lineage: If the "lineage" value in the state differs, Terraform will not allow you to push the state." |
| 75 | 7b | Push safety check: higher remote serial | https://developer.hashicorp.com/terraform/cli/commands/state/push | "If the "serial" value in the destination state is higher than the state being pushed, Terraform will prevent the push." |
| 76 | 7b | Name of the second push safety check | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Higher remote serial" |
| 77 | 7b | -force disables both safety checks | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Both of these safety checks can be disabled with the -force flag." |
| 78 | 7b | With checks disabled the destination state is overwritten | https://developer.hashicorp.com/terraform/cli/commands/state/push | "the destination state will be overwritten." |
| 79 | 7c | Logging is off by default | https://developer.hashicorp.com/terraform/plugin/log/managing | "Logging is off for all subsystems by default." |
| 80 | 7c | Setting TF_LOG sends detailed logs to stderr | https://developer.hashicorp.com/terraform/internals/debugging | "Enabling this setting causes detailed logs to appear on stderr." |
| 81 | 7c | Levels: TRACE, DEBUG, INFO, WARN, ERROR | https://developer.hashicorp.com/terraform/internals/debugging | "TRACE, DEBUG, INFO, WARN or ERROR" |
| 82 | 7c | Levels are listed in order of decreasing verbosity | https://developer.hashicorp.com/terraform/internals/debugging | "(in order of decreasing verbosity)" |
| 83 | 7c | TRACE is most verbose | https://developer.hashicorp.com/terraform/plugin/log/managing | "TRACE - Most verbose, typically includes low-level execution steps." |
| 84 | 7c | ERROR is least verbose | https://developer.hashicorp.com/terraform/plugin/log/managing | "ERROR - Least verbose, typically provides more detail about user-facing errors." |
| 85 | 7c | TF_LOG=JSON outputs TRACE-or-higher parseable JSON | https://developer.hashicorp.com/terraform/internals/debugging | "Setting TF_LOG to JSON outputs logs at the TRACE level or higher, and uses a parseable JSON encoding" |
| 86 | 7c | JSON log encoding is not a stable interface | https://developer.hashicorp.com/terraform/internals/debugging | "The JSON encoding of log files is not considered a stable interface." |
| 87 | 7c | Default log format is plaintext lines with timestamp and level | https://developer.hashicorp.com/terraform/plugin/log/managing | "By default, logs are written as plaintext lines, prefixed with a timestamp and the level in square braces." |
| 88 | 7c | Turn logging off by unsetting or setting off | https://developer.hashicorp.com/terraform/cli/config/environment-variables | "To disable, either unset it, or set it to off." |
| 89 | 7c | TF_LOG_CORE and TF_LOG_PROVIDER enable logs separately for core and plugins | https://developer.hashicorp.com/terraform/internals/debugging | "Logging can be enabled separately for Terraform itself and the provider plugins" |
| 90 | 7c | They take the same levels but only a subset of logs | https://developer.hashicorp.com/terraform/internals/debugging | "These take the same level arguments as TF_LOG, but only activate a subset of the logs." |
| 91 | 7c | TF_LOG_CORE covers the Terraform binary, not providers | https://developer.hashicorp.com/terraform/plugin/log/managing | "TF_LOG_CORETerraform binaryDoes not include providers." |
| 92 | 7c | TF_LOG overrides all other logging variables | https://developer.hashicorp.com/terraform/plugin/log/managing | "TF_LOGAll loggers (Terraform, SDKs, providers)Overrides all other logging environment variables." |
| 93 | 7c | Docs example: TF_LOG=TRACE with a provider variable at WARN makes all providers log at TRACE | https://developer.hashicorp.com/terraform/plugin/log/managing | "If you set TF_LOG=TRACE and TF_LOG_PROVIDER_AZUREM=WARN, all providers will write logs at the TRACE level." |
| 94 | 7c | Core application holds the operation logic | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "The Terraform core application contains all the logic for operations." |
| 95 | 7c | Core logs are what the Terraform team needs for core errors | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "The Terraform development team needs the core logs for your attempted operation to troubleshoot core-related errors." |
| 96 | 7c | Provider logs help the provider team reproduce provider errors | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "By including these in your bug reports, the provider development team can reproduce and debug provider specific errors." |
| 97 | 7c | Without TF_LOG_PATH logs go to stderr | https://developer.hashicorp.com/terraform/plugin/log/managing | "If you do not specify a log path, Terraform writes the specified log output to stderr." |
| 98 | 7c | TF_LOG_PATH file is appended, not truncated | https://developer.hashicorp.com/terraform/plugin/log/managing | "Terraform adds new log output onto the end of the file without truncating the file contents." |
| 99 | 7c | TF_LOG_PATH alone does not enable logging; TF_LOG must be set | https://developer.hashicorp.com/terraform/internals/debugging | "even when TF_LOG_PATH is set, TF_LOG must be set in order for any logging to be enabled" |
| 100 | 7c | Bug reports: set TF_LOG=TRACE | https://developer.hashicorp.com/terraform/plugin/log/managing | "When you report bugs to issue trackers, we recommend setting TF_LOG=TRACE." |
| 101 | 7c | Bug reports: use TRACE (core logging) | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "For bug reports, you should use the TRACE level." |
| 102 | 7c | Before v0.15.0 levels other than TRACE may be unreliable | https://developer.hashicorp.com/terraform/plugin/log/managing | "Before Terraform v0.15.0, levels besides TRACE may not be reliable." |
| 103 | 7c | Provider logs may contain sensitive data | https://developer.hashicorp.com/terraform/plugin/log/filtering | "there may be sensitive data which should not be present in log messages or structured log fields." |
| 104 | 7c | Purpose of enabling logs: debug unexpected behaviors | https://developer.hashicorp.com/terraform/internals/debugging | "This topic describes how to enable Terraform logs so that you can debug unexpected behaviors." |

## Self-consistency check

Each section was re-read in isolation against its own claim-table rows, with each sentence covered except for what its row supports.

- 7a: rows 1-39. The `for_each` description is the docs' own wording plus the docs' example (`to` with `each.key`, `id` with `each.value`, matching `for_each` on the resource). "An import appears as its own action in the plan" rests on the example plan line "1 to import, 0 to add ..." and says no more. The replace-after-import warning rests on the tutorial's plan text and its fix sentence; the lesson says "read the plan before you apply", which is advice, not a doc claim. The lesson does not say to delete the `import` block after applying, because no fetched page says so; it quotes only the "future planning" sentence.
- 7b: rows 40-78. `state pull` is described only as download and print to stdout (rows 69-71). The lineage and serial checks are the page's own wording, with the check names quoted and the sentences split so each quote is exact. "Plan files can contain sensitive data" is from the plan tutorial (row 55). The 4h sentence repeats a fact g4 already taught (output `-json`/`-raw` print sensitive values) and then adds the by-name and ephemeral facts, which g4 does not state.
- 7c: rows 79-104. The level order sentence combines two rows (the level list and "in order of decreasing verbosity"). The `TF_LOG` precedence rests on the managing-logs table row and the docs' worked example (row 93). The `TF_LOG_PATH` caveat is stated exactly as the debugging page states it. The sensitive-data paragraph quotes the provider-development note and labels the "treat a log like state" advice as the lesson's inference.
- Warnings: the first bullet is the standard one. The import-lifecycle bullet rests on row 37 (7a). The plain-text bullet rests on rows 54-55 and 63-68 (show, output) and on g6's "state ... can contain secrets" fact for `state pull`. The `push -force` bullet rests on rows 72-78. The logs bullet repeats the 7c inference.

### Cross-references, checked by regex (`g7w_refs.py`, against the live lesson files)

- g6 6d actually contains (all True): the `import` block, `terraform import ADDRESS ID`, `-generate-config-out`, the word Drift, `-refresh-only`, `terraform state list`, `terraform state show`, "Do not directly edit this file", and "`to` for the address and `id`". g7's opening says 6d "covered" these, and 6d itself says Group 3 (3d) introduced `-refresh-only`, so g7 does not claim 6d introduced it (a draft did; fixed).
- g3 3d contains `-out` (True). g7 says "Group 3 (3d) covered saving a plan with `-out`".
- g4 4h contains "terraform output ... -json or -raw ... plain text" (True). g7 says "Section 4h said `-json` and `-raw` print sensitive values in plain text". g4 4h does not mention outputs by name or ephemeral omission in `terraform output`; g7 states those as new.
- No other "group N" or "section N" reference occurs in the lesson.

## Checks run

Outputs are pasted below.

### content_lint.py
```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
```
### q1_batch_check.py tf-g7 (lesson lines PASS; question lines FAIL because the 9 question files are still placeholders: objective-text stems, no citationIds, no mcpStatus, MR stems lack "(Select N.)", duplicate openings, longest-is-key; all expected until questions are written. Per-question FAIL lines omitted here.)
```
task tf-g7: 9 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 3 for 3 objectives
FAIL: duplicate 6-word openings: ['select two actions that support this']
FAIL: longest-is-key 4/6 = 67%
PASS: shortest-is-key 0/6 = 0%
WARN: MC key positions {'a': 2, 'b': 1, 'd': 3}
PASS: MR key slots {'a': 1, 'b': 1, 'c': 1, 'd': 2, 'e': 1}
PASS: MR key sets: most common 'd,e' in 1/3 (33%); all {'d,e': 1, 'c,d': 1, 'a,b': 1}
RESULT: FAIL
```
### claim_prose_check.py tf-g7
```
task tf-g7: 3 distinct numbers in lesson prose
PASS: every claim-table number appears in the lesson prose
```


## Round 1 fix pass

Appended after the checks above; earlier sections are untouched and describe the first draft. The claim table below supersedes the first table's row numbers (118 rows now). Every page was re-fetched this turn with `curl -sL` and the HTML-to-text strip (`g7w_fetch.py`), including one new page, the provider block configuration page. Method as before: all 118 quotes are verbatim substrings of the fetched text and all are 20 words or fewer; all 99 double-quoted body spans are on a fetched page; every body span is covered by a row. No terraform command, AWS call or git command was run.

### Findings applied

| Finding | Change |
|---|---|
| AWS-Lg7-001 / TEACHER-Lg7-001 (`TF_LOG_PATH`) | Saving-the-log bullet now quotes both sides: the debugging page ("TF_LOG must be set ...") and the troubleshooting tutorial ("the TF_LOG_PATH variable will create the specified file and append logs generated by Terraform."), then states what the pages share: a level variable is set alongside the path, so set `TF_LOG` (or `TF_LOG_CORE` or `TF_LOG_PROVIDER`). The exam tip keeps "a level variable such as `TF_LOG`". Tutorial row added; its citation (`cite-tf-g7-debug-tut`) was already listed. |
| AWS-Lg7-002 | `TF_LOG` bullet says the plugin-development page's table gives the precedence rule and keeps its single worked example; no claim about `TF_LOG_CORE` versus `TF_LOG`. |
| AWS-Lg7-003 | Level bullet adds that `OFF` is not one of the five verbosity levels and quotes "OFF - Turns off logging for that logger." |
| AWS-Lg7-004 | `identity` is now "the alternative to `id`: an object of key-value pairs" with the quote "The keys and values are specific to the resource type and provider."; the unsupported "for providers that define one" is gone. `for_each` sentence adds the model's "map or set of strings". No version floor is stated for either. |
| AWS-Lg7-005 | Replace-after-import wording fixed: the plan after generation proposes a replace "due to the default value of the env parameter returned by the provider"; the Warning comment belongs to a later plan; the page's advice to review plan output is quoted; "verbose" dropped. |
| AWS-Lg7-006 | Warnings split: `show -json`, `output -json`, `output -raw` print sensitive values; `state pull` prints raw state "which can contain secrets" (pointing to 6d's Warnings); push bullet now says "pushing could lose data" and quotes "not recommended."; the logs bullet and the log-file clause are labelled as this lesson's advice. |
| AWS-Lg7-007 | Question-writer guidance, followed (see the questions report). |
| AWS-Lg7-008 | "unreadable by itself" became "in an "opaque file format" (plan page)"; the `-raw` quote "will print the string directly with no extra escaping or whitespace" added. |
| TEACHER-Lg7-002 | Lineage and serial glossed with the page's own sentences, plus the refusal sentences ("Terraform will not allow you to push the state." and "Terraform will prevent the push.") so a question on refusal rests on taught text. |
| TEACHER-Lg7-003 | Plan and apply bullets merged into one (6d covered both); the opening now says 6d covered "the `import` block, the resource block it needs, and the `terraform import` command"; alias glossed with the provider-configuration page ("Optionally use the alias argument to define multiple configurations for the same provider." and the different-regions example). |
| TEACHER-Lg7-004 | `TF_LOG_PROVIDER` bullet added: "All providers and provider SDKs used during the run." |
| TEACHER-Lg7-005 | 7c advice opens "Our own advice, not a doc claim:"; Warnings label it too. |
| TEACHER-Lg7-006 | Row 34 split into two single spans (health, intent); the `TF_LOG_CORE` and `TF_LOG` rows now quote only "Does not include providers." and "Overrides all other logging environment variables." |
| TEACHER-Lg7-007 | "Treat both as sensitive" replaced by two separate claims: `show -json` prints sensitive state values; a saved plan "can contain sensitive data". |

Two additions beyond the findings, both needed so a question rests on taught text: the `jq` sentence ("You can parse the output using a JSON command-line parser such as jq", output page) for the `-json` distractor, and the push refusal sentences above.

### Self-consistency after the fix

- No sentence says a page supports more than it does. The new 7c bullet says "What these pages share is that a level variable is set alongside `TF_LOG_PATH`"; this is the lesson's synthesis of three pages (one says `TF_LOG` must be set, the tutorial pairs the path with core or provider variables, the plugin page says one or more variables enable logging), not a quoted claim, and is worded as such.
- The exam tip still reads "a level variable such as `TF_LOG`", consistent with the bullet.
- Cross-references re-run by regex (`g7w_refs.py`): 6d, 3d and 4h all still hold; the new "6d's Warnings cover secrets in state" is true (6d Warnings: "State can contain secrets in plain text").

### Checks after the fix pass (lesson and questions together)

```
(g7w_chain.txt) content_lint PASS; q1_batch_check tf-g7 RESULT: PASS (all lines);
distractor_type_audit PASS; stem_echo_check PASS (0 giveaways); claim_prose_check PASS;
test_q1_letter PASS (12 bad, 10 good, 0 failures)
```
Full output is pasted in the questions report.

### Claim table (current, 118 rows)

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---|---|---|---|
| 1 | 7a | Goal: existing infrastructure can be imported so you manage it as code | https://developer.hashicorp.com/terraform/language/import | "If you have existing infrastructure resources, you can import them to your Terraform workspace" |
| 2 | 7a | id is the cloud provider ID of the resource to import | https://developer.hashicorp.com/terraform/language/block/import | "The id argument specifies the cloud provider's ID for the resource you want to import." |
| 3 | 7a | The ID format depends on the resource type | https://developer.hashicorp.com/terraform/language/block/import | "The value of the id argument depends on the type of resource you are importing." |
| 4 | 7a | Find the required ID in the provider documentation | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "You can find the required ID in the provider documentation for the resource you wish to import." |
| 5 | 7a | An import block can sit in any configuration file | https://developer.hashicorp.com/terraform/language/block/import | "You can add an import block to any Terraform configuration file" |
| 6 | 7a | Recommended placement: an imports.tf file or beside the destination resource block | https://developer.hashicorp.com/terraform/language/block/import | "creating an imports.tf file for all import configurations or placing each import block beside the destination resource block" |
| 7 | 7a | Plan reports an import count as its own action (example output) | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Plan: 1 to import, 0 to add, 0 to change, 0 to destroy." |
| 8 | 7a | Apply performs the import; example result line | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed." |
| 9 | 7a | Once in state, Terraform no longer needs to generate configuration for it | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "In future planning, Terraform knows it doesn't need to generate configuration for resources that already exist in your state." |
| 10 | 7a | id accepts a string or an expression that evaluates to a string | https://developer.hashicorp.com/terraform/language/block/import | "You must specify a string or an expression that evaluates to a string." |
| 11 | 7a | The id must be known during plan | https://developer.hashicorp.com/terraform/language/block/import | "The ID must be known during the plan operation." |
| 12 | 7a | identity is an object of key-value pairs that uniquely identify a resource | https://developer.hashicorp.com/terraform/language/block/import | "The identity argument is an object of key-value pairs that uniquely identify a resource." |
| 13 | 7a | identity keys and values are specific to the resource type and provider | https://developer.hashicorp.com/terraform/language/block/import | "The keys and values are specific to the resource type and provider." |
| 14 | 7a | id and identity cannot be used together | https://developer.hashicorp.com/terraform/language/block/import | "You cannot use the id argument and identity argument in the same import block." |
| 15 | 7a | for_each on an import block imports similar resources without separate blocks | https://developer.hashicorp.com/terraform/language/block/import | "The for_each meta-argument instructs Terraform to import similar resources without requiring separate configuration blocks." |
| 16 | 7a | Configuration model: for_each takes a map or set of strings | https://developer.hashicorp.com/terraform/language/block/import | "map or set of strings" |
| 17 | 7a | Docs example: for_each = local.buckets, to uses each.key | https://developer.hashicorp.com/terraform/language/block/import | "to = aws_s3_bucket.this[each.key]" |
| 18 | 7a | Docs example: id = each.value with the for_each map | https://developer.hashicorp.com/terraform/language/block/import | "id = each.value" |
| 19 | 7a | provider meta-argument selects the provider configuration used for the import | https://developer.hashicorp.com/terraform/language/block/import | "The provider meta-argument instructs Terraform to import resources according to the specified provider configuration." |
| 20 | 7a | An alias defines multiple configurations for the same provider | https://developer.hashicorp.com/terraform/language/providers/configuration | "Optionally use the alias argument to define multiple configurations for the same provider." |
| 21 | 7a | Docs example of two provider configurations: different regions | https://developer.hashicorp.com/terraform/language/providers/configuration | "two configurations for the AWS provider support different regions" |
| 22 | 7a | Docs example imports into aws_instance.web using the east alias | https://developer.hashicorp.com/terraform/language/block/import | "Terraform imports the AWS instance with the ID i-096fba6d03d36d262 to the aws_instance.web resource according to the east alias." |
| 23 | 7a | Generated configuration is a template of best guesses | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "HCL to act as a template that contains Terraform's best guess at the appropriate value for each resource argument" |
| 24 | 7a | Generation covers import-block resources missing from configuration | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "for the resources you define in import blocks that do not already exist in your configuration." |
| 25 | 7a | Generated config contains all arguments including defaults and empty ones | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "The generated configuration contains all possible arguments for the imported resources, including those set to default values" |
| 26 | 7a | Recommendation to prune generated configuration | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "We recommend that you prune the generated configuration to only required arguments" |
| 27 | 7a | Recommendation to prune: also keep arguments whose values differ from defaults | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "arguments whose values differ from defaults" |
| 28 | 7a | Terraform asks you to review generated configuration before version control | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Please review the configuration and edit it as necessary before adding it to version control." |
| 29 | 7a | Generation can fail to build valid configuration for complex schemas | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "For certain resources with complex schemas, Terraform may not be able to construct a valid configuration from these values." |
| 30 | 7a | Example error name is Conflicting configuration arguments | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "Error: Conflicting configuration arguments" |
| 31 | 7a | The example conflict is two arguments the resource accepts but you must choose one | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "The resource supports both of these arguments, but you must choose only one when configuring the resource." |
| 32 | 7a | Plan after generation in the tutorial warns it would destroy the imported resource | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "# Warning: this will destroy the imported resource" |
| 33 | 7a | Plan after generation proposes replacing the container because of a provider-returned default | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "due to the default value of the env parameter returned by the provider" |
| 34 | 7a | Tutorial fixes it by changing a generated value (env to an empty set) | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Change the value of env to an empty set using square brackets." |
| 35 | 7a | Tutorial advises carefully reviewing plan output to avoid destructive changes | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "recommend carefully reviewing plan output before applying to avoid destructive changes." |
| 36 | 7a | A provider block is needed if no other resource uses that provider | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "you must add a provider block to inform Terraform which provider it should use to generate configuration" |
| 37 | 7a | A new provider block needs terraform init again | https://developer.hashicorp.com/terraform/language/import/generating-configuration | "If you add a new provider block to your configuration, you must run terraform init again." |
| 38 | 7a | Import cannot determine the health of the infrastructure | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "It cannot determine: the health of the infrastructure." |
| 39 | 7a | Import cannot determine the intent of the infrastructure | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "the intent of the infrastructure." |
| 40 | 7a | Import does not detect or generate relationships | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Terraform import does not detect or generate relationships between infrastructure." |
| 41 | 7a | Not every provider and resource supports import | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Not all providers and resources support Terraform import." |
| 42 | 7a | Imported object is managed for its whole lifecycle including destruction | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "importing a resource into Terraform means that Terraform will manage the entire lifecycle of the resource, including destruction." |
| 43 | 7a | Back up state before importing | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "You may want to create a backup before importing new infrastructure." |
| 44 | 7a | Tutorial: import manipulates state during apply | https://developer.hashicorp.com/terraform/tutorials/state/state-import | "Importing manipulates the Terraform state file during the apply." |
| 45 | 7b | state list usage takes optional addresses | https://developer.hashicorp.com/terraform/cli/commands/state/list | "Usage: terraform state list [options] [address...]" |
| 46 | 7b | Patterns filter and use resource addressing format | https://developer.hashicorp.com/terraform/cli/commands/state/list | "To filter these, provide one or more patterns to the command. Patterns are in resource addressing format." |
| 47 | 7b | Module address lists the module and submodules | https://developer.hashicorp.com/terraform/cli/commands/state/list | "This example will list resources in the given module and any submodules" |
| 48 | 7b | -id flag takes the ID of the resources to show | https://developer.hashicorp.com/terraform/cli/commands/state/list | "-id=id - ID of resources to show." |
| 49 | 7b | -id helps find where a resource is in configuration | https://developer.hashicorp.com/terraform/cli/commands/state/list | "This is useful to find where in your configuration a specific resource is located." |
| 50 | 7b | state show needs an address pointing to a single resource | https://developer.hashicorp.com/terraform/cli/commands/state/show | "This command requires an address that points to a single resource in the state." |
| 51 | 7b | Quote resource names with special characters in single quotes | https://developer.hashicorp.com/terraform/cli/commands/state/show | "You must place the resource name in single quotes when it contains special characters like double quotes." |
| 52 | 7b | State subcommand output is designed for Unix tools | https://developer.hashicorp.com/terraform/cli/commands/state/index | "designed to be usable with Unix command-line tools such as grep, awk, and similar PowerShell commands" |
| 53 | 7b | terraform show: human-readable output from a state or plan file | https://developer.hashicorp.com/terraform/cli/commands/show | "The terraform show command provides human-readable output from a state or plan file." |
| 54 | 7b | show with no path shows the latest state snapshot | https://developer.hashicorp.com/terraform/cli/commands/show | "If you don't specify a file path, Terraform will show the latest state snapshot." |
| 55 | 7b | Saved plans are not human-readable; terraform show prints them | https://developer.hashicorp.com/terraform/tutorials/cli/plan | "Use the terraform show command to print out the saved plan." |
| 56 | 7b | plan -out writes an opaque saved plan file | https://developer.hashicorp.com/terraform/cli/commands/plan | "Writes the generated plan to the given filename in an opaque file format" |
| 57 | 7b | show -json makes machine-readable output | https://developer.hashicorp.com/terraform/cli/commands/show | "Add the -json command-line flag to generate machine-readable output." |
| 58 | 7b | show -json for a plan file gives plan, configuration and current state | https://developer.hashicorp.com/terraform/cli/commands/show | "terraform show -json shows a JSON representation of the plan, configuration, and current state." |
| 59 | 7b | show -json displays sensitive state values in plain text | https://developer.hashicorp.com/terraform/cli/commands/show | "any sensitive values in Terraform state will be displayed in plain text" |
| 60 | 7b | Plan files can contain sensitive data | https://developer.hashicorp.com/terraform/tutorials/cli/plan | "Terraform plan files can contain sensitive data." |
| 61 | 7b | output extracts a value from the state file | https://developer.hashicorp.com/terraform/cli/commands/output | "The terraform output command extracts the value of an output variable from the state file." |
| 62 | 7b | No name shows all root module outputs | https://developer.hashicorp.com/terraform/cli/commands/output | "output will display all the outputs for the root module." |
| 63 | 7b | With a NAME only that output is printed | https://developer.hashicorp.com/terraform/cli/commands/output | "If an output NAME is specified, only the value of that output is printed." |
| 64 | 7b | output shows only root module outputs | https://developer.hashicorp.com/terraform/cli/commands/output | "The terraform output command only displays outputs defined in the root module." |
| 65 | 7b | Expose a child module value with an output in the root module | https://developer.hashicorp.com/terraform/cli/commands/output | "define an output block in your root module using the value of an output from a child module" |
| 66 | 7b | Default output format can change over time | https://developer.hashicorp.com/terraform/cli/commands/output | "which can change over time to improve clarity" |
| 67 | 7b | Use -json for the stable JSON format in scripts | https://developer.hashicorp.com/terraform/cli/commands/output | "For scripting and automation, use -json to produce the stable JSON format." |
| 68 | 7b | -raw supports only string, number, boolean | https://developer.hashicorp.com/terraform/cli/commands/output | "it only supports string, number, and boolean values." |
| 69 | 7b | Use -json for complex data types | https://developer.hashicorp.com/terraform/cli/commands/output | "Use -json instead for processing complex data types." |
| 70 | 7b | -raw prints the string with no extra escaping or whitespace | https://developer.hashicorp.com/terraform/cli/commands/output | "will print the string directly with no extra escaping or whitespace" |
| 71 | 7b | -json output can be parsed with a JSON parser such as jq | https://developer.hashicorp.com/terraform/cli/commands/output | "You can parse the output using a JSON command-line parser such as jq" |
| 72 | 7b | Plain terraform output shows <sensitive> for a sensitive output | https://developer.hashicorp.com/terraform/cli/commands/output | "password = <sensitive>" |
| 73 | 7b | Output by name does not redact sensitive values | https://developer.hashicorp.com/terraform/cli/commands/output | "Terraform does not redact sensitive values when you specify the output by name" |
| 74 | 7b | Ephemeral values are omitted even by name | https://developer.hashicorp.com/terraform/cli/commands/output | "Terraform completely omits any ephemeral values, even if you specify an output by name." |
| 75 | 7b | -json and -raw show sensitive values in plain text (repeated from 4h) | https://developer.hashicorp.com/terraform/cli/commands/output | "When using the -json or -raw command-line flags, Terraform displays sensitive values in plain text." |
| 76 | 7b | state pull downloads and outputs state from remote or local | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "The terraform state pull downloads and outputs state information from a remote state or local state." |
| 77 | 7b | state pull outputs the raw format to stdout | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "outputs the raw format to stdout" |
| 78 | 7b | state pull is useful for reading values out of state, e.g. with jq | https://developer.hashicorp.com/terraform/cli/commands/state/pull | "This is useful for reading values out of state (potentially pairing this command with something like jq)." |
| 79 | 7b | state push uploads a local state file to the backend | https://developer.hashicorp.com/terraform/cli/commands/state/push | "The terraform state push command uploads a local state file to remote state or a local state." |
| 80 | 7b | Push recommended only for manual modification of remote state | https://developer.hashicorp.com/terraform/cli/commands/state/push | "We only recommend using this command when you must manually modify the remote state." |
| 81 | 7b | Name of the first push safety check; lineage mismatch suggests different states and possible data loss | https://developer.hashicorp.com/terraform/cli/commands/state/push | "suggests that the states are completely different and you may lose data" |
| 82 | 7b | A higher destination serial suggests data not accounted for in the local state | https://developer.hashicorp.com/terraform/cli/commands/state/push | "suggests that data is in the destination state that isn't accounted for in the local state being pushed" |
| 83 | 7b | A differing lineage makes Terraform refuse the push | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Terraform will not allow you to push the state." |
| 84 | 7b | A higher destination serial makes Terraform prevent the push | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Terraform will prevent the push." |
| 85 | 7b | Names of the two push safety checks | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Differing lineage" |
| 86 | 7b | Name of the second push safety check | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Higher remote serial" |
| 87 | 7b | -force disables both safety checks | https://developer.hashicorp.com/terraform/cli/commands/state/push | "Both of these safety checks can be disabled with the -force flag." |
| 88 | 7b | The docs follow -force with a not-recommended note | https://developer.hashicorp.com/terraform/cli/commands/state/push | "This is not recommended." |
| 89 | 7b | With checks disabled the destination state is overwritten | https://developer.hashicorp.com/terraform/cli/commands/state/push | "the destination state will be overwritten." |
| 90 | 7c | Logging is off by default | https://developer.hashicorp.com/terraform/plugin/log/managing | "Logging is off for all subsystems by default." |
| 91 | 7c | Setting TF_LOG sends detailed logs to stderr | https://developer.hashicorp.com/terraform/internals/debugging | "Enabling this setting causes detailed logs to appear on stderr." |
| 92 | 7c | Levels: TRACE, DEBUG, INFO, WARN, ERROR | https://developer.hashicorp.com/terraform/internals/debugging | "TRACE, DEBUG, INFO, WARN or ERROR" |
| 93 | 7c | Levels are listed in order of decreasing verbosity | https://developer.hashicorp.com/terraform/internals/debugging | "(in order of decreasing verbosity)" |
| 94 | 7c | TRACE is most verbose | https://developer.hashicorp.com/terraform/plugin/log/managing | "TRACE - Most verbose, typically includes low-level execution steps." |
| 95 | 7c | ERROR is least verbose | https://developer.hashicorp.com/terraform/plugin/log/managing | "ERROR - Least verbose, typically provides more detail about user-facing errors." |
| 96 | 7c | OFF turns logging off for that logger (listed separately from the verbosity levels) | https://developer.hashicorp.com/terraform/plugin/log/managing | "OFF - Turns off logging for that logger." |
| 97 | 7c | TF_LOG=JSON outputs TRACE-or-higher parseable JSON | https://developer.hashicorp.com/terraform/internals/debugging | "Setting TF_LOG to JSON outputs logs at the TRACE level or higher, and uses a parseable JSON encoding" |
| 98 | 7c | JSON log encoding is not a stable interface | https://developer.hashicorp.com/terraform/internals/debugging | "The JSON encoding of log files is not considered a stable interface." |
| 99 | 7c | Default log format is plaintext lines with timestamp and level | https://developer.hashicorp.com/terraform/plugin/log/managing | "By default, logs are written as plaintext lines, prefixed with a timestamp and the level in square braces." |
| 100 | 7c | Turn logging off by unsetting or setting off | https://developer.hashicorp.com/terraform/cli/config/environment-variables | "To disable, either unset it, or set it to off." |
| 101 | 7c | TF_LOG_CORE and TF_LOG_PROVIDER enable logs separately for core and plugins | https://developer.hashicorp.com/terraform/internals/debugging | "Logging can be enabled separately for Terraform itself and the provider plugins" |
| 102 | 7c | They take the same levels but only a subset of logs | https://developer.hashicorp.com/terraform/internals/debugging | "These take the same level arguments as TF_LOG, but only activate a subset of the logs." |
| 103 | 7c | TF_LOG_CORE does not include providers | https://developer.hashicorp.com/terraform/plugin/log/managing | "Does not include providers." |
| 104 | 7c | TF_LOG_PROVIDER covers all providers and provider SDKs used in the run | https://developer.hashicorp.com/terraform/plugin/log/managing | "All providers and provider SDKs used during the run" |
| 105 | 7c | TF_LOG overrides all other logging variables (plugin-development table) | https://developer.hashicorp.com/terraform/plugin/log/managing | "Overrides all other logging environment variables." |
| 106 | 7c | Docs example: TF_LOG=TRACE with a provider variable at WARN makes all providers log at TRACE | https://developer.hashicorp.com/terraform/plugin/log/managing | "If you set TF_LOG=TRACE and TF_LOG_PROVIDER_AZUREM=WARN, all providers will write logs at the TRACE level." |
| 107 | 7c | Core application holds the operation logic | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "The Terraform core application contains all the logic for operations." |
| 108 | 7c | Core logs are what the Terraform team needs for core errors | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "The Terraform development team needs the core logs for your attempted operation to troubleshoot core-related errors." |
| 109 | 7c | Provider logs help the provider team reproduce provider errors | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "By including these in your bug reports, the provider development team can reproduce and debug provider specific errors." |
| 110 | 7c | Without TF_LOG_PATH logs go to stderr | https://developer.hashicorp.com/terraform/plugin/log/managing | "If you do not specify a log path, Terraform writes the specified log output to stderr." |
| 111 | 7c | TF_LOG_PATH file is appended, not truncated | https://developer.hashicorp.com/terraform/plugin/log/managing | "Terraform adds new log output onto the end of the file without truncating the file contents." |
| 112 | 7c | TF_LOG_PATH alone does not enable logging; TF_LOG must be set | https://developer.hashicorp.com/terraform/internals/debugging | "even when TF_LOG_PATH is set, TF_LOG must be set in order for any logging to be enabled" |
| 113 | 7c | Tutorial wording: TF_LOG_PATH creates and appends the file (paired with core or provider logging) | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "the TF_LOG_PATH variable will create the specified file and append logs generated by Terraform." |
| 114 | 7c | Bug reports: set TF_LOG=TRACE | https://developer.hashicorp.com/terraform/plugin/log/managing | "When you report bugs to issue trackers, we recommend setting TF_LOG=TRACE." |
| 115 | 7c | Bug reports: use TRACE (core logging) | https://developer.hashicorp.com/terraform/tutorials/configuration-language/troubleshooting-workflow | "For bug reports, you should use the TRACE level." |
| 116 | 7c | Before v0.15.0 levels other than TRACE may be unreliable | https://developer.hashicorp.com/terraform/plugin/log/managing | "Before Terraform v0.15.0, levels besides TRACE may not be reliable." |
| 117 | 7c | Provider logs may contain sensitive data | https://developer.hashicorp.com/terraform/plugin/log/filtering | "there may be sensitive data which should not be present in log messages or structured log fields." |
| 118 | 7c | Purpose of enabling logs: debug unexpected behaviors | https://developer.hashicorp.com/terraform/internals/debugging | "This topic describes how to enable Terraform logs so that you can debug unexpected behaviors." |
