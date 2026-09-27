# Lesson tf-g2 (Terraform fundamentals) — implementation report

## Outline

- Replaced the placeholder `bodyMarkdown` with a full lesson covering all 4 objectives in id order: tf.004.2a, tf.004.2b, tf.004.2c, tf.004.2d.
- One `###` section per objective (`### tf.004.<id> — <objective text>`), each ending with an `**Exam tip:**` line; single `##` lesson title kept (`## Terraform fundamentals`).
- Added the required `### Warnings` section, same Terraform-adapted text used in lesson-tf-g1 (no credentialed apply/destroy, forbidden MCP execute tools, plain-text state file risk).
- Discriminators taught per objective: version-constraint operators (`~>`, `>=`, `=`, etc.) vs. the committed dependency lock file for reproducibility (2a); `required_providers` (declares the dependency/version) vs. the `provider` block (configures the downloaded plugin) (2b); using two distinct providers together vs. using the same provider twice via `alias` (2c); the configuration files (`.tf`, desired end state) vs. the state file (`terraform.tfstate`, actual already-created resources) (2d).
- Jargon defined on first use: provider (plugin), plugin, registry, HCL/`.tf` configuration, backend (named but deferred to group 6), drift (named but deferred), state, dependency lock file, alias.
- Version-sensitive fact flagged in prose: Large Bandwidth-style version-range behavior is not relevant here, but the `~>` operator's own example is version-specific by construction (`~> 1.0.4` allows `1.0.5`/`1.0.10`, not `1.1.0`) and is stated exactly as HashiCorp's docs phrase it, with no claim that this is tied to a specific Terraform CLI release (the version-constraint syntax itself is stable across current Terraform 1.x).
- `drillIds` corrected from the stale 5-id list to the full 12 question ids for this task, in objective order (`-mc`, `-mc2`, `-mr` per objective).
- `citationIds` replaced the single shared `cite-tf-004` with 6 new page-specific citations: `cite-tf-g2-providers`, `cite-tf-g2-provider-requirements`, `cite-tf-g2-provider-configuration`, `cite-tf-g2-providers-lock`, `cite-tf-g2-version-constraints`, `cite-tf-g2-state`.
- Confirmed `cite-tf-004` is still referenced by `lesson-tf-g3.json` through `lesson-tf-g8.json`, so it was left in place, not deleted.
- Round-1 self-check caught 3 pairs of single-asterisk italics (`*acceptable*`, `*same*` ×2) left over from drafting; replaced with plain text before verification, per the "no single-asterisk italics" markdown-subset rule. Re-read both edited paragraphs afterward to confirm no sentence was duplicated by the fix.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 2a | Terraform CLI finds and installs providers when initializing a working directory | https://developer.hashicorp.com/terraform/language/providers | "Terraform CLI finds and installs providers when initializing a working directory. It can automatically download providers from a Terraform registry, or load them from a local mirror or cache." |
| 2 | 2a | The Terraform Registry is the main public directory of providers | https://developer.hashicorp.com/terraform/language/providers | "The Terraform Registry is the main directory of publicly available Terraform providers, and hosts providers for most major infrastructure platforms." |
| 3 | 2a | Production configurations should constrain acceptable provider versions so init doesn't install an incompatible newer version | https://developer.hashicorp.com/terraform/language/providers/requirements | "In production we recommend constraining the acceptable provider versions in the configuration's provider requirements block, to make sure that terraform init does not install newer versions of the provider that are incompatible with the configuration." |
| 4 | 2a | `~> 1.0.4` allows 1.0.5 and 1.0.10 but not 1.1.0 | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Allows only the right-most version component to increment. Examples: ~> 1.0.4: Allows Terraform to install 1.0.5 and 1.0.10 but not 1.1.0." |
| 5 | 2a | `=` allows only one exact version and cannot combine with other conditions | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Allows only one exact version number. Cannot be combined with other conditions." |
| 6 | 2a | `!=` excludes an exact version number | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Excludes an exact version number." |
| 7 | 2a | `>`, `>=`, `<`, `<=` compare to a specified version; Terraform allows versions that resolve true | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Compares to a specified version. Terraform allows versions that resolve to true." |
| 8 | 2a | A committed dependency lock file makes Terraform always install the same provider versions | https://developer.hashicorp.com/terraform/cli/commands/providers/lock | "To ensure Terraform always installs the same provider versions for a given configuration, you can use Terraform CLI to create a dependency lock file and commit it to version control." |
| 9 | 2b | Terraform relies on plugins called providers to interact with cloud providers, SaaS providers, and other APIs | https://developer.hashicorp.com/terraform/language/providers | "Terraform relies on plugins called providers to interact with cloud providers, SaaS providers, and other APIs." |
| 10 | 2b | Each provider adds a set of resource types and/or data sources Terraform can manage | https://developer.hashicorp.com/terraform/language/providers | "Each provider adds a set of resource types and/or data sources that Terraform can manage." |
| 11 | 2b | The `provider` block is used to declare and configure Terraform plugins called providers | https://developer.hashicorp.com/terraform/language/providers/configuration | "Use the `provider` block to declare and configure Terraform plugins, called providers." |
| 12 | 2b | Each argument in `required_providers` enables one provider | https://developer.hashicorp.com/terraform/language/providers/requirements | "Each argument in the `required_providers` block enables one provider." |
| 13 | 2b | A provider source address is structured `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` | https://developer.hashicorp.com/terraform/language/providers/requirements | "Source addresses consist of three parts delimited by slashes (`/`), as follows: `[<HOSTNAME>/]<NAMESPACE>/<TYPE>`" |
| 14 | 2b | Omitting `source` implies `registry.terraform.io/hashicorp/<LOCAL NAME>` | https://developer.hashicorp.com/terraform/language/providers/requirements | "If you omit the `source` argument when requiring a provider, Terraform uses an implied source address of `registry.terraform.io/hashicorp/<LOCAL NAME>`." |
| 15 | 2c | Resources beginning with `aws_` use the default `aws` provider configuration unless given a `provider` argument | https://developer.hashicorp.com/terraform/language/providers/configuration | "Resources that begin with `aws_` use the default `aws` provider configuration unless you supply the `provider` argument." |
| 16 | 2c | A `provider` block with no `alias` is the default configuration when multiple aliases exist | https://developer.hashicorp.com/terraform/language/providers/configuration | "If there are multiple aliases for a provider, the `provider` block without an `alias` argument is the default configuration for that provider." |
| 17 | 2c | Multiple provider aliases let you pick which configuration a resource, data source, or module uses | https://developer.hashicorp.com/terraform/language/providers/configuration | "Defining multiple provider aliases lets you specify which provider configuration to use for individual resources, data sources, or modules." |
| 18 | 2d | Terraform must store state about a workspace's managed infrastructure and configuration | https://developer.hashicorp.com/terraform/language/state | "Terraform must store state about your workspace's managed infrastructure and configuration." |
| 19 | 2d | State records the identity of a remote object against a particular resource instance (mapping) | https://developer.hashicorp.com/terraform/language/state | "record the identity of that remote object against a particular resource instance" |
| 20 | 2d | State keeps track of metadata | https://developer.hashicorp.com/terraform/language/state | "keep track of metadata" |
| 21 | 2d | State improves performance for large infrastructures | https://developer.hashicorp.com/terraform/language/state | "improve performance for large infrastructures" |
| 22 | 2d | Terraform stores each workspace's state in a local file named `terraform.tfstate` by default | https://developer.hashicorp.com/terraform/language/state | "Terraform stores each workspace's state in a local file named `terraform.tfstate`" |

## New citation files (6)

`cite-tf-g2-providers` (rows 1, 2, 9, 10), `cite-tf-g2-provider-requirements` (rows 3, 12, 13, 14), `cite-tf-g2-provider-configuration` (rows 11, 15, 16, 17), `cite-tf-g2-providers-lock` (row 8), `cite-tf-g2-version-constraints` (rows 4, 5, 6, 7), `cite-tf-g2-state` (rows 18–22). All `accessed: "2026-09-26"`.

## Retired / renamed / closed-to-new-customers findings

None. No AWS-specific services are discussed in this lesson.

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g2`: lesson-only lines PASS (single-asterisk spans 0 after the round-1 self-fix described above, tables/numbered lines 0, no markdown link, citations unresolved [], drillIds match questions, exam tips 4/4 objectives). Question-line FAILs (objective-text echoes, missing citationIds, `mcpStatus`/`reviewedOn`, duplicate 6-word openings, longest-is-key rate, MR key-set repetition) are the pre-existing placeholder questions and are expected to fail until the questions step.
- `claim_prose_check.py tf-g2`: PASS — every claim-table number (`1.0.4`, `1.0.5`, `1.0.10`, `1.1.0`) appears in the lesson prose; verified below.
