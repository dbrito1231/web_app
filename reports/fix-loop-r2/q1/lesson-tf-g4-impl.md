# Lesson tf-g4 (Terraform configuration) — implementation report

## What was written

Replaced the placeholder `bodyMarkdown` (objective-text stubs pointing only at the certification-mapping page) with a full lesson covering all 8 objectives in id order: tf.004.4a–4h. One `###` section per objective, each ending with an `**Exam tip:**` line; single `##` lesson title; `### Warnings` section added. `drillIds` replaced the stale 9 with all 24 real question ids (3 per objective: `-mc`, `-mc2`, `-mr`), in objective order.

Discriminators taught explicitly, one per objective, per the brief's list:

- 4a: `resource` (can create/change/destroy, includes the built-in `terraform_data` type) vs `data` (read-only, never appears as add/change/destroy), plus the data-read planning/apply timing deferral.
- 4b: an attribute reference (`aws_iam_role.example.name`) both fetches a value and creates an implicit dependency in one line, vs `depends_on` (forward-referenced to 4f) which creates a dependency with no value fetched.
- 4c: `variable` (set from outside, `var.`) vs `local` (computed inside, never visible outside the module, `local.`) vs `output` (computed inside, exposed to a caller via `module.`).
- 4d: `list`/`tuple` (ordered, indexed by position) vs `set` (unique, unordered, no index — must `tolist()` first) vs `map`/`object` (keyed by string name); `null` as its own typeless value.
- 4e: `for` expressions (transform + filter, cannot generate nested blocks) vs `count` (identical instances, numeric index) vs `for_each` (distinct instances, map/set key, no sensitive values allowed); `try` (fallback value) vs `can` (boolean, used in `validation`); `lookup` and `merge`; conditional expressions.
- 4f: `depends_on` (last resort, literal list, no expression) vs `create_before_destroy` (replacement before destroy) vs `prevent_destroy` (rejects destroy plans, but not a config-removal destroy) — all three direction- and literal-value-constrained; explicit `depends_on = [B]` inside A means A depends on B, never the reverse (same directionality trap flagged for `-target` in g3).
- 4g: `validation` (variable-only, before any plan) vs `precondition` (before creating the object, beats provider argument errors) vs `postcondition` (after creation, via `self`) vs `check` (warns only, never blocks); the run-order sequence stated explicitly to prevent the "validation happens right before precondition" confusion.
- 4h: `sensitive` (CLI/UI redaction only, still in state, still visible via `terraform output -json/-raw`) vs `ephemeral` (omitted from state/plan entirely, restricted reference contexts) vs a write-only argument (the channel that lets an ephemeral value reach an ordinary resource, tracked by a paired `_wo_version` instead of a state diff) vs Vault (external short-lived-credential source, not a language keyword).

Self-consistency check performed per RULES.md "After applying a fix" item 2: each section was re-read in isolation against its own claim-table rows after drafting, specifically checking the `depends_on`/`-target` directionality statement (4f) and the `prevent_destroy` gap (4f) for the kind of contradiction that hit g3's original 3f draft. No contradiction found: 4f states `depends_on = [B]` in A means A depends on B (upstream) and explicitly says it "says nothing about anything that might depend on A," consistent with the g3 `-target` correction on direction.

## Citations (20 files, one per doc page fetched this turn)

`cite-tf-g4-resource`, `cite-tf-g4-data-sources`, `cite-tf-g4-resources-overview`, `cite-tf-g4-variables`, `cite-tf-g4-outputs`, `cite-tf-g4-locals`, `cite-tf-g4-types`, `cite-tf-g4-for-expr`, `cite-tf-g4-count`, `cite-tf-g4-for-each`, `cite-tf-g4-depends-on`, `cite-tf-g4-validate`, `cite-tf-g4-conditionals`, `cite-tf-g4-try`, `cite-tf-g4-can`, `cite-tf-g4-lookup`, `cite-tf-g4-merge`, `cite-tf-g4-sensitive-data`, `cite-tf-g4-write-only`, `cite-tf-g4-vault-tutorial`. `cite-tf-004` untouched on disk (shared with g5–g8); this lesson no longer references it alone.

All fetches were done with the Browser pane's `get_page_text` (rendered page text), not WebFetch's summarizing model, specifically to avoid the g1/g3-style fabricated-quote failure — every quote below was copy-pasted from that raw page text, then trimmed only at word boundaries to fit the 20-word cap.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 4a | A resource block defines a piece of infrastructure and the settings to create it | https://developer.hashicorp.com/terraform/language/block/resource | "The resource block defines a piece of infrastructure and specifies the settings for Terraform to create it with." |
| 2 | 4a | Data sources fetch data from the provider but do not create or modify resources | https://developer.hashicorp.com/terraform/language/data-sources | "Data sources fetch data from the provider, but do not create or modify resources." |
| 3 | 4a | Terraform can only perform read operations on data sources | https://developer.hashicorp.com/terraform/language/data-sources | "Terraform can only perform read operations on data sources." |
| 4 | 4a | Terraform attempts to query data sources during the planning phase | https://developer.hashicorp.com/terraform/language/data-sources | "Terraform attempts to query data sources during the planning phase" |
| 4b | 4a | Terraform may defer reading a data source until the apply phase | https://developer.hashicorp.com/terraform/language/data-sources | "it may defer reading until the apply phase" |
| 5 | 4b | Reference a resource using `<TYPE>.<LABEL>` syntax | https://developer.hashicorp.com/terraform/language/block/resource | "To reference the resource in your configuration, you must refer to it using `<TYPE>.<LABEL>` syntax." |
| 6 | 4b | Reference queried data using `data.<TYPE>.<LABEL>.<ATTRIBUTE>` syntax | https://developer.hashicorp.com/terraform/language/data-sources | "Use the data.<TYPE>.<LABEL>.<ATTRIBUTE> syntax to reference data resource attributes elsewhere in your configuration." |
| 7 | 4b | An attribute reference lets Terraform automatically infer that the referenced resource must be created first | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "Because this expression refers to the role, Terraform automatically infers that the role must be created first." |
| 8 | 4b | Explicit `depends_on` is only needed when a resource relies on another's behavior without referencing its data | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "You only need to explicitly specify a dependency when a resource or module relies on another resource's behavior" |
| 9 | 4c | A variable block lets module consumers customize module behavior without altering the module's source code | https://developer.hashicorp.com/terraform/language/values/variables | "A variable block lets module consumers customize module behavior without altering the module's source code." |
| 10 | 4c | With no default value, Terraform prompts the user for a value before generating a plan | https://developer.hashicorp.com/terraform/language/values/variables | "Terraform prompts the user to assign a value before it generates a plan." |
| 11 | 4c | Local values are similar to function-scoped variables in other programming languages | https://developer.hashicorp.com/terraform/language/values/locals | "Local values are similar to function-scoped variables in other programming languages." |
| 12 | 4c | Local values are accessible only in the module where they are defined, not in other modules | https://developer.hashicorp.com/terraform/language/values/locals | "You can access local values in the module where you define them, but not in other modules" |
| 13 | 4c | Output blocks export information about a module's infrastructure | https://developer.hashicorp.com/terraform/language/values/outputs | "Add output blocks to export information about your module's infrastructure." |
| 14 | 4c | Parent modules access child module outputs using `module.<CHILD_MODULE_NAME>.<OUTPUT_NAME>` syntax | https://developer.hashicorp.com/terraform/language/values/outputs | "Parent modules can access child module outputs using module.<CHILD_MODULE_NAME>.<OUTPUT_NAME> syntax." |
| 15 | 4d | list/tuple is an ordered sequence of values | https://developer.hashicorp.com/terraform/language/expressions/types | "list (or tuple): a sequence of values" |
| 16 | 4d | set is a collection of unique values with no secondary identifiers or ordering | https://developer.hashicorp.com/terraform/language/expressions/types | "set: a collection of unique values that do not have any secondary identifiers or ordering." |
| 17 | 4d | Terraform does not support directly accessing set elements by index because sets are unordered | https://developer.hashicorp.com/terraform/language/expressions/types | "Terraform does not support directly accessing elements of a set by index because sets are unordered collections." |
| 18 | 4d | Convert a set to a list first to access elements by index | https://developer.hashicorp.com/terraform/language/expressions/types | "To access elements in a set by index, first convert the set to a list" |
| 19 | 4d | map/object is a group of values identified by named labels | https://developer.hashicorp.com/terraform/language/expressions/types | "map (or object): a group of values identified by named labels" |
| 20 | 4d | The keys in a map must be strings | https://developer.hashicorp.com/terraform/language/expressions/types | "The keys in a map must be strings" |
| 21 | 4d | null represents absence or omission | https://developer.hashicorp.com/terraform/language/expressions/types | "null: a value that represents absence or omission." |
| 22 | 4d | Setting an argument to null behaves as though it were completely omitted | https://developer.hashicorp.com/terraform/language/expressions/types | "If you set an argument of a resource to null, Terraform behaves as though you had completely omitted it" |
| 23 | 4d | Terraform automatically converts number and bool values to strings when needed | https://developer.hashicorp.com/terraform/language/expressions/types | "Terraform automatically converts number and bool values to strings when needed," |
| 24 | 4e | A for expression creates a complex type value by transforming another complex type value | https://developer.hashicorp.com/terraform/language/expressions/for | "A for expression creates a complex type value by transforming another complex type value." |
| 25 | 4e | A for expression can include an optional if clause to filter elements from the source | https://developer.hashicorp.com/terraform/language/expressions/for | "A for expression can also include an optional if clause to filter elements from the source collection," |
| 26 | 4e | Use the count argument to create nearly identical instances | https://developer.hashicorp.com/terraform/language/meta-arguments/count | "Use the count argument when you want to create nearly identical instances," |
| 27 | 4e | Use for_each when instance arguments must have distinct values not derivable from an integer index | https://developer.hashicorp.com/terraform/language/meta-arguments/count | "Use for_each when some instance arguments must have distinct values that can't be directly derived from an integer index" |
| 28 | 4e | for_each values must be known before Terraform performs any remote resource operations | https://developer.hashicorp.com/terraform/language/meta-arguments/for_each | "All values that the for_each argument iterates over must be known before Terraform performs any remote resource operations." |
| 29 | 4e | Sensitive values cannot be used as for_each arguments | https://developer.hashicorp.com/terraform/language/meta-arguments/for_each | "You cannot use sensitive values, such as sensitive input variables, sensitive outputs, or sensitive resource attributes, as arguments in for_each," |
| 30 | 4e | try returns the result of the first argument expression that does not error | https://developer.hashicorp.com/terraform/language/functions/try | "returns the result of the first one that does not produce any errors" |
| 31 | 4e | can returns a boolean indicating whether the expression evaluated without error | https://developer.hashicorp.com/terraform/language/functions/can | "evaluates the given expression and returns a boolean value indicating whether the expression produced a result without any errors" |
| 32 | 4e | lookup retrieves a single map element by key | https://developer.hashicorp.com/terraform/language/functions/lookup | "retrieves the value of a single element from a map, given its key," |
| 33 | 4e | lookup returns the given default when the key does not exist | https://developer.hashicorp.com/terraform/language/functions/lookup | "If the given key does not exist, the given default value is returned instead" |
| 34 | 4e | merge takes multiple maps/objects and returns one merged map or object | https://developer.hashicorp.com/terraform/language/functions/merge | "takes an arbitrary number of maps or objects, and returns a single map or object" |
| 35 | 4e | On key collision in merge, the later argument in the sequence takes precedence | https://developer.hashicorp.com/terraform/language/functions/merge | "the one that is later in the argument sequence takes precedence" |
| 36 | 4e | Conditional expression: true branch when condition is true | https://developer.hashicorp.com/terraform/language/expressions/conditionals | "If condition is true then the result is true_val," |
| 37 | 4e | Conditional expression: false branch when condition is false | https://developer.hashicorp.com/terraform/language/expressions/conditionals | "If condition is false then the result is false_val." |
| 38 | 4f | depends_on handles hidden dependencies Terraform cannot automatically infer | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "Use the depends_on meta-argument to handle hidden resource or module dependencies that Terraform cannot automatically infer" |
| 39 | 4f | depends_on should only be used as a last resort because it creates more conservative plans | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "You should only use depends_on as a last resort because it can cause Terraform to create more conservative plans" |
| 40 | 4f | Expression references are recommended over depends_on to imply dependencies when possible | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "Instead of depends_on, we recommend using expression references to imply dependencies when possible" |
| 41 | 4f | depends_on on a module affects the processing order of all resources/data sources in that module | https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on | "depends_on affects the order in which Terraform processes all of the resources and data sources associated with that module." |
| 42 | 4f | create_before_destroy creates a replacement resource before destroying the one it replaces | https://developer.hashicorp.com/terraform/language/block/resource | "The create_before_destroy argument instructs Terraform to create a replacement resource before destroying the resource it replaces," |
| 43 | 4f | prevent_destroy instructs Terraform to reject plans to destroy the resource | https://developer.hashicorp.com/terraform/language/block/resource | "The prevent_destroy argument instructs Terraform to reject plans to destroy the resource," |
| 44 | 4f | prevent_destroy does not stop destruction caused by removing the resource's configuration | https://developer.hashicorp.com/terraform/language/block/resource | "This rule doesn't prevent Terraform from destroying the resource if you remove the resource configuration" |
| 45 | 4f | Only literal values are allowed in the lifecycle block, processed before other expressions are evaluated | https://developer.hashicorp.com/terraform/language/block/resource | "You can only use literal values in the lifecycle block because Terraform processes them before it evaluates arbitrary expressions" |
| 46 | 4g | Input variable validations run immediately, before Terraform generates a plan | https://developer.hashicorp.com/terraform/language/validate | "Terraform executes input variable validations immediately, before generating a plan," |
| 47 | 4g | A failed variable validation errors, shows the error_message, and stops the operation | https://developer.hashicorp.com/terraform/language/validate | "When a variable validation fails, Terraform errors, displays the configured error_message, and stops the operation from proceeding." |
| 48 | 4g | Preconditions ensure resources, data sources, and outputs meet requirements before Terraform tries to create them | https://developer.hashicorp.com/terraform/language/validate | "Preconditions ensure individual resources, data sources, and outputs meet your requirements before Terraform tries to create them," |
| 49 | 4g | Terraform evaluates preconditions when it creates a plan | https://developer.hashicorp.com/terraform/language/validate | "Terraform evaluates preconditions on resources, data sources, and outputs when Terraform creates a plan" |
| 50 | 4g | Preconditions take precedence over provider argument errors on incorrectly configured objects | https://developer.hashicorp.com/terraform/language/validate | "Preconditions take precedence over any argument errors raised by providers on incorrectly configured resources, data sources, and outputs," |
| 51 | 4g | Terraform evaluates postconditions after planning/applying a resource or after reading a data source | https://developer.hashicorp.com/terraform/language/validate | "Terraform evaluates postcondition blocks after planning and applying changes to a resource, or after reading from a data source," |
| 52 | 4g | Use the self object in postconditions to refer to the instance under evaluation | https://developer.hashicorp.com/terraform/language/expressions/conditionals | "Use the self object in postcondition blocks to refer to attributes of the instance under evaluation." |
| 53 | 4g | Preconditions verify assumptions before Terraform creates the target block | https://developer.hashicorp.com/terraform/language/validate | "Use preconditions for assumptions that you want to verify before Terraform creates the target block," |
| 54 | 4g | Postconditions verify guarantees after Terraform creates the resource or reads the data source | https://developer.hashicorp.com/terraform/language/validate | "Use postconditions for guarantees that you need to verify after Terraform creates the resource or reads from the data source." |
| 55 | 4g | Check blocks run as the last step of plan/apply, after infrastructure is planned or provisioned | https://developer.hashicorp.com/terraform/language/validate | "the last step of plan or apply operation, after Terraform has planned or provisioned your infrastructure" |
| 56 | 4g | A failed check reports a warning and lets the operation continue | https://developer.hashicorp.com/terraform/language/validate | "When a check block's assertion fails, Terraform reports a warning and continues executing the current operation" |
| 57 | 4g | Order: preconditions after plan generation but before creating the object | https://developer.hashicorp.com/terraform/language/validate | "Terraform executes preconditions after generating a plan but before creating the resource, data source, or output," |
| 58 | 4g | Order: postconditions after planning and applying changes | https://developer.hashicorp.com/terraform/language/validate | "Terraform executes postconditions after planning and applying changes," |
| 59 | 4g | Order: checks at the end of plan and apply operations | https://developer.hashicorp.com/terraform/language/validate | "Terraform executes checks at the end of plan and apply operations" |
| 60 | 4g | can concisely turns the validity of an expression into a condition | https://developer.hashicorp.com/terraform/language/expressions/conditionals | "Use the can function to concisely use the validity of an expression as a condition," |
| 61 | 4g | alltrue/anytrue with a for expression test a condition across a collection | https://developer.hashicorp.com/terraform/language/expressions/conditionals | "Use for expressions in conjunction with the functions alltrue and anytrue to test whether a condition holds" |
| 62 | 4h | Adding secrets directly to configuration stores them in state and plan files | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "If you add secret values directly to your configuration, Terraform stores those secrets in its state and plan files." |
| 63 | 4h | sensitive on variable/output blocks redacts values from Terraform CLI log output | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "redact those values from Terraform CLI log output" |
| 64 | 4h | Terraform treats any expression referencing a sensitive variable/output as sensitive too | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Terraform also automatically treats any expression that references a sensitive variable or output as sensitive" |
| 65 | 4h | Values marked sensitive are still stored in state and plan files, readable by anyone with file access | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Terraform stores values with the sensitive argument in both state and plan files, and anyone who can access those files" |
| 66 | 4h | `terraform output -json`/`-raw` displays sensitive values in plain text | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "If you use the terraform output CLI command with the -json or -raw flags, Terraform displays sensitive variables and outputs" |
| 67 | 4h | Ephemeral values are available at runtime but omitted from state and plan files entirely | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Ephemeral values are available at runtime, but Terraform omits them from state and plan files entirely." |
| 68 | 4h | Terraform restricts where ephemeral values can be referenced in configuration | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Terraform restricts where you can reference ephemeral values in your configuration," |
| 69 | 4h | Write-only arguments pass temporary values to managed resources without persisting them to state | https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only | "let you securely pass temporary values to Terraform's managed resources during an operation without persisting those values to state" |
| 70 | 4h | Terraform stores an argument's paired version value in state and can track when it changes | https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only | "Terraform stores version arguments in state, and can track if a version argument changes." |
| 71 | 4h | Because it cannot track write-only values, Terraform resends them to the provider on every operation | https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only | "Because Terraform cannot track write-only argument values, it sends write-only arguments to the provider during every operation" |
| 72 | 4h | Vault's provider generates appropriately scoped, short-lived cloud credentials for Terraform to use | https://developer.hashicorp.com/terraform/tutorials/secrets/secrets-vault | "leverage Terraform's Vault provider to generate appropriately scoped & short-lived AWS credentials" |
| 73 | 4h | The problem Vault solves: operators otherwise manage many static, long-lived, variously-scoped cloud credentials | https://developer.hashicorp.com/terraform/tutorials/secrets/secrets-vault | "Operators need to manage a large number of static, long-lived AWS IAM credentials with varying scope," |
| 74 | 4h | Short-lived, Vault-issued credentials reduce the risk of a compromised credential in a Terraform run | https://developer.hashicorp.com/terraform/tutorials/secrets/secrets-vault | "reduces the risk from a compromised AWS credential in a Terraform run" |

## Round 1 review fixes (AWS + Teacher, commit 564ae39)

- **AWS-Lg4-001 (fixed):** row 27's quote is genuine but was attributed to the wrong page (`for_each` instead of `count`, where the "...integer index" wording actually lives). Fixed in the table above; no lesson-prose change needed since the quote text itself was already correct.
- **AWS-Lg4-002 (fixed):** added version floors where each feature is taught — `precondition`/`postcondition` (1.2+) and `check` (1.5+) in 4g; `ephemeral` (1.10+) and write-only arguments (1.11+) in 4h. New claim-table rows 75–78 below, all quoted from each page's own "Requirements" list.
- **`nonsensitive()` (fixed, both reviewers' finding):** added one paragraph at the end of 4h, fetched fresh this turn from `language/functions/nonsensitive` (not reused from either reviewer's report, per the hard ban on quoting without fetching it myself this turn). New rows 79–81.
- **TEACHER-Lg4-001 (fixed):** added a claim-table row (82) for the `terraform_data` prose claim in 4a, quoted from `language/resources/terraform-data`, fetched fresh this turn.
- **TEACHER-Lg4-002 (fixed):** defined "meta-argument" in 4a before it does discriminator work, using a real quote from `language/meta-arguments` (row 83) — a clean one-sentence definition exists on that page after all, so no paraphrase-without-quote was needed.

Self-consistency re-read (RULES.md "After applying a fix" #2): re-read 4a, 4g, and 4h in full after editing. The new `nonsensitive()` paragraph states it "does not touch state, does not make a value ephemeral, and does not undo anything already written to disk," which matches rather than contradicts the preceding `sensitive`/`ephemeral` paragraphs (still CLI/UI-only, still in state) — no new contradiction introduced. The `check` version-floor clause ("the newest of the four") is consistent with the stated order of `validation` (0.13, oldest, per the Requirements list, not separately re-quoted in-lesson since it wasn't a review finding), `precondition`/`postcondition` (1.2), and `check` (1.5).

New claim-table rows for the round-1 fixes:

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 75 | 4g | precondition/postcondition require Terraform 1.2.0 or later | https://developer.hashicorp.com/terraform/language/validate | "Terraform v1.2.0 or later for preconditions and postconditions" |
| 76 | 4g | check blocks require Terraform 1.5.0 or later | https://developer.hashicorp.com/terraform/language/validate | "Terraform v1.5.0 or later for check blocks" |
| 77 | 4h | the ephemeral argument requires Terraform 1.10 or later | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Use Terraform 1.10 or later to add the ephemeral argument to variables and child module outputs" |
| 78 | 4h | write-only arguments require Terraform 1.11 or later | https://developer.hashicorp.com/terraform/language/manage-sensitive-data | "Use Terraform 1.11 or later to use a write-only argument on a managed resource." |
| 79 | 4h | nonsensitive strips the sensitive marking from a value, exposing it | https://developer.hashicorp.com/terraform/language/functions/nonsensitive | "takes a sensitive value and returns a copy of that value with the sensitive marking removed" |
| 80 | 4h | nonsensitive is meant for deriving genuinely non-sensitive results (e.g. a hash) from sensitive values | https://developer.hashicorp.com/terraform/language/functions/nonsensitive | "you may wish to write expressions that derive non-sensitive results from sensitive values," |
| 81 | 4h | Misusing nonsensitive exposes values Terraform would otherwise keep redacted | https://developer.hashicorp.com/terraform/language/functions/nonsensitive | "will cause values that Terraform would normally have considered as sensitive to be treated as normal values and shown clearly" |
| 82 | 4a | terraform_data stores values under the managed-resource lifecycle and triggers provisioners with no other resource to hold them | https://developer.hashicorp.com/terraform/language/resources/terraform-data | "useful for storing values which need to follow a manage resource lifecycle, and for triggering provisioners" |
| 83 | 4a | Meta-arguments are built into the language and control how Terraform creates/manages infrastructure, regardless of provider | https://developer.hashicorp.com/terraform/language/meta-arguments | "Meta-arguments are a class of arguments built into the Terraform configuration language that control how Terraform creates and manages" |

## Retired / renamed / closed-to-new-customers findings

None (this lesson has no AWS-service content; the AWS references are incidental to Terraform examples, e.g. `aws_instance`, `aws_iam_role`).

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g4`: lesson-only lines PASS — `drillIds match questions (missing [], extra [])`, `exam tips 8 for 8 objectives`. Question-line FAILs (stem pastes objective text, no citationIds, placeholder stems, MR "(Select N.)" missing, longest-is-key, duplicate 6-word openings) are all against the pre-existing 24 placeholder question files and are expected until the questions step, per this task's scope.
- `claim_prose_check.py tf-g4`: run below.

## Round 2 fix pass

Applied all seven `## Lesson edits` items from `questions-tf-g4-fixspec.md` (L1-L7). All doc pages
re-fetched this turn with `curl -sL` piped through `fixg4_strip.py` (a small HTML-to-text stripper
written this turn in the scratchpad), never WebFetch, per RULES.md.

- **L1 - 4a doubled "but".** Changed "Terraform normally reads a data source during planning, but
  \"Terraform attempts...,\" but \"it may defer...\"" to "...during planning: \"Terraform
  attempts...,\" but \"it may defer...\"" -- drops the first "but", keeps both quotes intact.
- **L2 - 4a refresh-on-each-run sentence.** Added, in the same timing paragraph: "Outside of that
  special case, Terraform re-reads a data source on every ordinary run: 'By default, Terraform
  refreshes prior to creating a plan.'" Re-fetched `language/data-sources` this turn; the sentence
  sits in a paragraph headed "References to non-computed values," confirming it is about data
  source refresh specifically, not state/resources generally: "...Terraform reads the data source
  and updates its state during Terraform's refresh phase. By default, Terraform refreshes prior to
  creating a plan." New claim row (84) below. This also makes the fact `q-tf-004-4a-mr`'s new key
  and `q-tf-004-4a-mc2`'s existing rationale rely on actually taught.
- **L3 - 4c `TF_VAR_` prefix.** Added one sentence after the no-default/prompt sentence: "Terraform
  also reads a variable's value from an environment variable, but only when the name carries the
  `TF_VAR_` prefix, for example `TF_VAR_subnet_id`: 'The environment variables must be in the
  format TF_VAR_name and this will be checked last for a value.'" Re-fetched
  `cli/config/environment-variables` this turn; quote is 19 words, copy-pasted verbatim (case
  preserved: "TF_VAR_name" is the doc's own placeholder spelling). New citation file
  `cite-tf-g4-env-vars.json` created (same schema as other `cite-tf-g4-*` files) and added to the
  lesson's `citationIds`. New claim row (85).
- **L4 - 4f `ignore_changes`/`replace_triggered_by`.** Added one paragraph after the existing
  lifecycle-literal-only sentence, stating that `ignore_changes` stops Terraform from planning
  updates to the attributes listed and accepts the bare `all` keyword to ignore every attribute,
  and that `replace_triggered_by` forces a full replacement when a referenced resource or attribute
  changes rather than controlling create/destroy order. Both quotes re-fetched this turn from
  `language/meta-arguments/lifecycle` -- the `all`-keyword wording only exists on that page, not on
  `language/block/resource` (which states `ignore_changes` more tersely, without the `all` keyword
  detail), so a new citation file `cite-tf-g4-lifecycle.json` was created and added to the lesson's
  `citationIds`, rather than folding this into `cite-tf-g4-resource`. New claim rows (86, 87).
- **L5 - 4g count fix.** "Three condition mechanisms check different things..." changed to "Four
  condition mechanisms check different things..." Now consistent with the later "the fourth
  mechanism, the newest of the four."
- **L6 - 4h ephemeral-sources miscount.** Replaced "There are three ways to get one" (which listed
  the `ephemeral` argument, the `ephemeral` block, and a write-only argument as three sources) with
  "There are two ways to originate one" (the `ephemeral` argument or the `ephemeral` block), plus a
  separate sentence naming a write-only argument as the channel that delivers an already-ephemeral
  value into an ordinary managed resource, not a third source. Re-read the very next sentence
  ("Ephemeral values come with a real restriction on where they can be used...") and the following
  paragraph's "A write-only argument is how an ephemeral value reaches an ordinary managed
  resource's own configuration" -- both now agree with the corrected count instead of contradicting
  it.
- **L7 - 4h wording fix.** "in the writer's own words" changed to "in the documentation's own
  words" (the text that follows is a verbatim HashiCorp quote, not the lesson author's own prose).

New claim-table rows for the round-2 lesson fixes:

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---|---|---|---|
| 84 | 4a | By default, Terraform refreshes a data source prior to creating a plan | https://developer.hashicorp.com/terraform/language/data-sources | "By default, Terraform refreshes prior to creating a plan." |
| 85 | 4c | Terraform only reads an environment variable for a variable's value when it carries the TF_VAR_ prefix | https://developer.hashicorp.com/terraform/cli/config/environment-variables | "The environment variables must be in the format TF_VAR_name and this will be checked last for a value." |
| 86 | 4f | ignore_changes accepts the bare `all` keyword to ignore every resource attribute | https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle | "Instead of a list of items, you can use the `all` keyword to instruct Terraform to ignore all attributes." |
| 87 | 4f | replace_triggered_by forces a replacement when a referenced resource or attribute changes | https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle | "Terraform replaces the resource when any of the referenced resources or specified attributes change." |
| 88 | 4h | (re-verified for the question fix, not added to lesson prose) nonsensitive makes no changes to a value that isn't marked sensitive | https://developer.hashicorp.com/terraform/language/functions/nonsensitive | "nonsensitive will make no changes to values that aren't marked as sensitive, even though such a call may be redundant" |

Row 88 backs a *rejected* lesson addition: AWS-Qg4-005/TEACHER-Qg4-003 found the current
`nonsensitive` docs describe a silent no-op on an already-non-sensitive value, not an error (the
page's own worked example below that sentence is stale and still shows an error, which is an
inconsistency in HashiCorp's current page, not a version-gated behavior to teach). Per the fix
spec's explicit instruction, this claim was **not** added to the lesson -- it only justifies why
`q-tf-004-4h-mr` choice c (Q6) was replaced rather than kept.

Self-consistency re-read (RULES.md "After applying a fix" #2): re-read 4a, 4f, 4g, and 4h in full
after editing, each in isolation against its own claim rows. 4a's "re-reads on every ordinary run"
sentence sits in a "specifically when... otherwise" contrast with the existing defer-to-apply
sentence and does not overstate the source (the source says "by default," and the lesson keeps
that qualifier via "Outside of that special case"). 4f's new paragraph states `ignore_changes` and
`replace_triggered_by` as parallel, separate mechanisms and does not claim either one controls
create/destroy ordering -- matching the doc text exactly. 4g's "Four condition mechanisms" reads
correctly against the immediately following per-mechanism list (variable `validation`,
`precondition`/`postcondition`, `check`) and the later "fourth mechanism" callback. 4h's two-source
rewrite does not claim a write-only argument never appears in a `variable`/`output` context -- it
only demotes it from "source" to "channel," which is exactly the distinction LD-Lg4-010 and
AWS-Lg4-010's own reading of the HashiCorp page (itself internally inconsistent, saying "four" and
listing three) asked for.

## Round 2 checks (whole file, not diff)

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g4`: PASS -- lesson lines unaffected by round 2 (single-asterisk spans 0,
  tables/numbered lines 0, citations unresolved [], exam tips 8/8).
- `claim_prose_check.py tf-g4`: PASS -- "9 distinct numbers in lesson prose... every claim-table
  number appears in the lesson prose" (unchanged from round 1; no new bare numbers were introduced
  by the round-2 lesson prose, since `ignore_changes`/`TF_VAR_`/refresh text carry no new numeric
  literals beyond the version floors already checked).

## Round 2c (Lead Dev, after round-2b confirmations)

Three small fixes from AWS-Qg4-009/TEACHER-Qg4-010, AWS-Qg4-010, and AWS-Lg4-013/TEACHER-Qg4-011. The quote below was fetched this turn with curl + HTML strip; it is verbatim.

| # | Section | Claim | Doc URL | Quote |
|---|---|---|---|---|
| 89 | 4a | terraform_data needs no companion managed resource | https://developer.hashicorp.com/terraform/language/resources/terraform-data | "for triggering provisioners when there is no other logical managed resource in which to place them" |

- 4a: added "It needs no companion resource: the docs describe it as useful \"for triggering provisioners when there is no other logical managed resource in which to place them.\"" This teaches the refutation of `4a-mr` choice e. The Teacher had said it was already taught; a regex over `bodyMarkdown` shows it was not, so the AWS reviewer was right.
- 4f: "`replace_triggered_by` does the opposite of sequencing a replacement:" became "... answers a different question from sequencing a replacement, because it decides whether a replacement happens at all:".
- `4d-mr` choice d: the `for_each` list claim (it answered neither stem need) became `` `null == ""` evaluates to `true`, treating a null and an empty string as the same absent value ``. It targets the `==` need. It is wrong because 4d teaches "`null` is not the same as an empty string or a zero". The AWS wording used "since", a banned giveaway word, so it was reworded. The rationale now also states why the two keys are correct, and `cite-tf-g4-for-each` was dropped from this question.
