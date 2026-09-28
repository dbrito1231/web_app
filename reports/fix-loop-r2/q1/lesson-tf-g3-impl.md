# Lesson tf-g3 (Core Terraform workflow) — implementation report

## Outline

- Replaced the placeholder `bodyMarkdown` (objective-text stubs pointing only at the certification-mapping page) with a full lesson covering all 7 objectives in id order: tf.004.3a–3g.
- One `###` section per objective, each ending with an `**Exam tip:**` line; single `##` lesson title kept; `### Warnings` section added (no credentialed apply/destroy, forbidden MCP execute tools, `-auto-approve`/saved-plan caution).
- Discriminators taught explicitly, one per objective: write/plan/apply as three non-interchangeable stages (3a); `init` installs and initializes but never checks correctness or touches real infrastructure (3b); `validate` vs `plan` — schema-only vs. live-state (3c); `plan` only reports proposed actions, `-out` is what makes them executable later (3d); interactive `apply` vs. `-auto-approve` vs. applying a saved `-out` file (3e); `destroy` (whole configuration) vs. removing one resource block and applying (single resource) (3f); `fmt` (style) vs. `validate` (correctness) (3g).
- Command-flag coverage required by the brief: `-upgrade` (3b), `-out`, `-target`, `-refresh-only`, `-destroy` on plan (3d), `-auto-approve`, `-destroy` on apply (3e), `-recursive`, `-check` (3g). Every flag is taught with what it changes, not just named.
- Version sensitivity: 3d and 3f both state that before Terraform 0.15 only `terraform plan` (not `apply`) accepted `-destroy`, so `terraform destroy` was the only way to execute a destroy plan on those older versions; current Terraform accepts `-destroy` on both.
- `drillIds`: replaced the stale 8 with all 21 question ids for this task, in objective order (3a mc/mc2/mr, 3b mc/mc2/mr, ... 3g mc/mc2/mr).
- `citationIds`: replaced the sole shared `cite-tf-004` with 7 new page-specific citations. `cite-tf-004` is left in place on disk (shared with g4–g8) but this lesson no longer cites it, per the brief's instruction not to rely on it alone.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 3a | Write stage: author infrastructure as code | https://developer.hashicorp.com/terraform/intro/core-workflow | "Author infrastructure as code." |
| 2 | 3a | Plan stage: preview changes before applying | https://developer.hashicorp.com/terraform/intro/core-workflow | "Preview changes before applying." |
| 3 | 3a | Apply stage: provision reproducible infrastructure | https://developer.hashicorp.com/terraform/intro/core-workflow | "Provision reproducible infrastructure." |
| 4 | 3a | Team members save changes to version control branches to avoid colliding with each other's work | https://developer.hashicorp.com/terraform/intro/core-workflow | "save their changes to version control branches to avoid colliding with each other's work" |
| 5 | 3a | Plan output creates an opportunity for team members to review each other's work | https://developer.hashicorp.com/terraform/intro/core-workflow | "Terraform's plan output creates an opportunity for team members to review each other's work" |
| 6 | 3a | After merge, the team should review the final concrete plan run against the shared branch and latest state | https://developer.hashicorp.com/terraform/intro/core-workflow | "review the final concrete plan that's run against the shared team branch and the latest version of the state file" |
| 7 | 3b | `terraform init` initializes a working directory containing Terraform configuration files | https://developer.hashicorp.com/terraform/cli/commands/init | "The `terraform init` command initializes a working directory containing Terraform configuration files." |
| 8 | 3b | `init` is the first command to run after writing a new configuration | https://developer.hashicorp.com/terraform/cli/commands/init | "the first command you should run after writing a new Terraform configuration" |
| 9 | 3b | It is safe to run `terraform init` multiple times | https://developer.hashicorp.com/terraform/cli/commands/init | "It is safe to run this command multiple times." |
| 10 | 3b | During init, the backend configuration is consulted and the chosen backend is initialized | https://developer.hashicorp.com/terraform/cli/commands/init | "the root configuration directory is consulted for backend configuration and the chosen backend is initialized" |
| 11 | 3b | During init, Terraform searches for `module` blocks and retrieves referenced module source code | https://developer.hashicorp.com/terraform/cli/commands/init | "Terraform searches the configuration for module blocks, and retrieves the source code for referenced modules" |
| 12 | 3b | During init, Terraform also searches for provider references and attempts to install those provider plugins | https://developer.hashicorp.com/terraform/cli/commands/init | "searches...for both direct and indirect references to providers and attempts to install the plugins for those providers" |
| 13 | 3b | After installation, Terraform writes the selected provider information to the dependency lock file | https://developer.hashicorp.com/terraform/cli/commands/init | "After successful installation, Terraform writes information about the selected providers to the dependency lock file." |
| 14 | 3b | Re-running init installs sources for modules added since the last init | https://developer.hashicorp.com/terraform/cli/commands/init | "will install the sources for any modules that were added to configuration since the last init" |
| 15 | 3b | Re-running init will not change any already-installed modules | https://developer.hashicorp.com/terraform/cli/commands/init | "but will not change any already-installed modules" |
| 16 | 3b | `-upgrade` overrides normal behavior, updating all modules to the latest available source code | https://developer.hashicorp.com/terraform/cli/commands/init | "Use `-upgrade` to override this behavior, updating all modules to the latest available source code" |
| 17 | 3b | `-upgrade` ignores selections recorded in the dependency lock file | https://developer.hashicorp.com/terraform/cli/commands/init | "ignore any selections recorded in the dependency lock file" |
| 18 | 3b | `-upgrade` takes the newest available version matching the configured version constraints | https://developer.hashicorp.com/terraform/cli/commands/init | "take the newest available version matching the configured version constraints" |
| 19 | 3c | `validate` checks whether a configuration is syntactically valid and internally consistent, regardless of variables or existing state | https://developer.hashicorp.com/terraform/cli/commands/validate | "verify whether a configuration is syntactically valid and internally consistent, regardless of any provided variables or existing state" |
| 20 | 3c | `validate` is primarily useful for verifying reusable modules, including correctness of attribute names and value types | https://developer.hashicorp.com/terraform/cli/commands/validate | "primarily useful for general verification of reusable modules, including correctness of attribute names and value types" |
| 21 | 3c | `validate` does not validate remote services such as remote state or provider APIs | https://developer.hashicorp.com/terraform/cli/commands/validate | "does not validate remote services, such as remote state or provider APIs" |
| 22 | 3c | `validate` requires an initialized working directory with referenced plugins and modules installed | https://developer.hashicorp.com/terraform/cli/commands/validate | "an initialized working directory with any referenced plugins and modules installed" |
| 23 | 3d | `plan` creates an execution plan that lets you preview the changes Terraform plans to make | https://developer.hashicorp.com/terraform/cli/commands/plan | "creates an execution plan, which lets you preview the changes that Terraform plans to make" |
| 24 | 3d | `plan` reads current remote object state to make sure Terraform state is up to date | https://developer.hashicorp.com/terraform/cli/commands/plan | "Reads the current state of any already-existing remote objects to make sure that the Terraform state is up-to-date" |
| 25 | 3d | `plan` proposes a set of change actions that would make remote objects match the configuration | https://developer.hashicorp.com/terraform/cli/commands/plan | "Proposes a set of change actions that should, if applied, make the remote objects match the configuration." |
| 26 | 3d | The plan command alone does not actually carry out the proposed changes | https://developer.hashicorp.com/terraform/cli/commands/plan | "The plan command alone does not actually carry out the proposed changes." |
| 27 | 3d | `-out` writes the generated plan to a file in an opaque format | https://developer.hashicorp.com/terraform/cli/commands/plan | "Writes the generated plan to the given filename in an opaque file format" |
| 28 | 3d | The `-out` file can later be passed to `terraform apply` | https://developer.hashicorp.com/terraform/cli/commands/plan | "you can later pass to `terraform apply`" |
| 29 | 3d | `-target` focuses planning only on resource instances matching the given address (and dependents) | https://developer.hashicorp.com/terraform/cli/commands/plan | "Instructs Terraform to focus its planning efforts only on resource instances which match the given address" |
| 30 | 3d | `-refresh-only` mode only updates state and root module outputs to match changes made outside Terraform | https://developer.hashicorp.com/terraform/cli/commands/plan | "update the Terraform state and any root module output values to match changes made to remote objects outside of Terraform" |
| 31 | 3d | `-destroy` mode creates a plan to destroy all remote objects, leaving an empty state | https://developer.hashicorp.com/terraform/cli/commands/plan | "Creates a plan whose goal is to destroy all remote objects that currently exist, leaving an empty Terraform state." |
| 32 | 3d / 3f | Before Terraform 0.15, only `plan` (not `apply`) supported `-destroy` | https://developer.hashicorp.com/terraform/cli/commands/plan | "the `-destroy` option is supported only by the `terraform plan` command, and not by the `terraform apply` command" |
| 33 | 3e | `apply` executes the operations proposed in a Terraform plan | https://developer.hashicorp.com/terraform/cli/commands/apply | "The `terraform apply` command executes the operations proposed in a Terraform plan." |
| 34 | 3e | Without a saved plan, `apply` automatically creates a new execution plan as if `plan` had run | https://developer.hashicorp.com/terraform/cli/commands/apply | "automatically creates a new execution plan as if you had run [`terraform plan`]" |
| 35 | 3e | `apply` prompts for approval and performs the indicated operations | https://developer.hashicorp.com/terraform/cli/commands/apply | "prompts you to approve that plan, and performs the indicated operations" |
| 36 | 3e | `-auto-approve` applies the plan without asking for confirmation | https://developer.hashicorp.com/terraform/cli/commands/apply | "You can pass the `-auto-approve` option to instruct Terraform to apply the plan without asking for confirmation." |
| 37 | 3e | Applying a saved plan file performs its operations without prompting for confirmation | https://developer.hashicorp.com/terraform/cli/commands/apply | "Terraform performs the operations in the saved plan without prompting you for confirmation." |
| 38 | 3e | `apply -destroy` creates a plan to destroy all remote objects | https://developer.hashicorp.com/terraform/cli/commands/apply | "creates a plan to destroy all remote objects" |
| 39 | 3f | `terraform destroy` deprovisions all objects managed by a configuration | https://developer.hashicorp.com/terraform/cli/commands/destroy | "The `terraform destroy` command deprovisions all objects managed by a Terraform configuration." |
| 40 | 3f | `terraform destroy` is a convenience alias for `terraform apply -destroy` | https://developer.hashicorp.com/terraform/cli/commands/destroy | "This command is just a convenience alias for the following command: `terraform apply -destroy`" |
| 41 | 3g | `fmt` formats configuration file contents to match the canonical format and style | https://developer.hashicorp.com/terraform/cli/commands/fmt | "The `terraform fmt` command formats Terraform configuration file contents so that it matches the canonical format and style." |
| 42 | 3g | `fmt` does not check whether configurations are correct or valid | https://developer.hashicorp.com/terraform/cli/commands/fmt | "does not check whether configurations are correct or valid" |
| 43 | 3g | By default, `fmt` only processes the current directory | https://developer.hashicorp.com/terraform/cli/commands/fmt | "By default, the command only processes the specified, or current, directory." |
| 44 | 3g | `-recursive` processes files in subdirectories in addition to the current directory | https://developer.hashicorp.com/terraform/cli/commands/fmt | "processes files in subdirectories in addition to the current directory" |
| 45 | 3g | `-check` reports formatting status via exit code (0 if properly formatted) instead of rewriting | https://developer.hashicorp.com/terraform/cli/commands/fmt | "checks if the input is formatted. The exit status is `0` if the command's input is properly formatted" |

## Citation files (7)

`cite-tf-g3-core-workflow` (rows 1–6), `cite-tf-g3-init` (rows 7–18), `cite-tf-g3-validate` (rows 19–22), `cite-tf-g3-plan` (rows 23–32), `cite-tf-g3-apply` (rows 33–38), `cite-tf-g3-destroy` (rows 39–40), `cite-tf-g3-fmt` (rows 41–45). `cite-tf-004` untouched on disk (still used by g4–g8); this lesson no longer references it.

## Retired / renamed / closed-to-new-customers findings

None (this lesson has no AWS content).

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g3`: lesson-only lines PASS — single-asterisk spans 0, tables/numbered lines 0, citations unresolved [], drillIds match questions (21/21), exam tips 7/7 objectives. Question-line FAILs (stem pastes objective text, no citationIds, placeholder stems, MR "(Select N.)" missing, longest-is-key, MR key-set duplication) are all against the pre-existing 21 placeholder question files and are expected until the questions step, per this task's scope.
- `claim_prose_check.py tf-g3`: PASS — every claim-table number (`0.15`) appears in lesson prose; no quote-length WARN (all 45 quotes ≤20 words).
