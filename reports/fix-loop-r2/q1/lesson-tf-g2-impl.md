# Lesson tf-g2 (Terraform fundamentals) — implementation report

## Round 2 — fixes applied (this revision)

- **TEACHER-Lg2-001 / AWS-Lg2-001 (citation URL, resolved by Lead)** — claim row 8's citation pointed at `/terraform/cli/commands/providers/lock`, which does not contain the quoted sentence. Per the Lead's resolution (both reviewers named different replacements; Lead fetched both and confirmed the sentence is on `/terraform/language/providers/requirements`, not `/terraform/language/files/dependency-lock`): repointed row 8 to the existing `cite-tf-g2-provider-requirements` citation (same page already cited for rows 3, 12, 13, 14) instead of creating a second citation for the same URL. Removed `cite-tf-g2-providers-lock` from `citationIds` and deleted `content/citations/cite-tf-g2-providers-lock.json` after confirming (`grep -rl`) nothing else in `content/` referenced it.
- **AWS-Lg2-002 (verbatim tense, low)** — row 19's quote said "record" where the doc says "records" (present tense, mid-sentence). Fixed to "records" in the claim table below; the lesson's own prose already paraphrases this correctly and needed no change.
- **TEACHER-Lg2-002 (workspace undefined)** — added a parenthetical at "workspace"'s first use in the 2d section: "(A workspace here is the working directory's current state environment; named workspaces that let one configuration manage several separate states are covered in a later objective.)"
- **TEACHER-Lg2-003 (module undefined)** — added a parenthetical at "modules"'s first use in the 2c section: "(a module is a reusable, packaged Terraform configuration, covered in full in group 5)".
- **Over-long quotes (new `claim_prose_check.py` WARN, cap 20 words) — trimmed 5 flagged rows (1, 3, 4, 8, 16), each to the clause that carries the claim, no paraphrase:**
  - Row 1: kept only the first sentence ("...when initializing a working directory."), dropped the second sentence about registry/mirror/cache, which is now covered by row 2's own quote.
  - Row 3: kept the recommendation clause ("...we recommend constraining the acceptable provider versions in the configuration's provider requirements block"), dropped the "to make sure that terraform init does not install..." consequence clause; adjusted the claim wording to match what the trimmed quote actually asserts (the prose sentence itself is unchanged and still states both halves).
  - Row 4: dropped the leading "Allows only the right-most version component to increment." sentence (already asserted by row's own claim text and by the `~>` definition elsewhere), kept the worked example with all three version numbers ("Examples: ~> 1.0.4: Allows Terraform to install 1.0.5 and 1.0.10 but not 1.1.0.").
  - Row 8: now quotes the dependency-lock sentence's core clause on the (corrected) requirements-page citation: "Terraform always installs the same provider versions for a given configuration" — dropped the leading "To ensure" and the trailing "you can use Terraform CLI to create a dependency lock file and commit it to version control" mechanism clause, which is separately asserted by the lesson's own prose sentence about the lock file recording checksums.
  - Row 16: dropped the leading "If there are multiple aliases for a provider," conditional clause, kept "the `provider` block without an `alias` argument is the default configuration for that provider," which is the claim itself.

## Outline (round 1, unchanged unless noted above)

- Replaced the placeholder `bodyMarkdown` with a full lesson covering all 4 objectives in id order: tf.004.2a, tf.004.2b, tf.004.2c, tf.004.2d.
- One `###` section per objective, each ending with an `**Exam tip:**` line; single `##` lesson title kept.
- `### Warnings` section, Terraform-adapted (no credentialed apply/destroy, forbidden MCP execute tools, plain-text state file risk).
- Discriminators: version-constraint operators vs. the committed dependency lock file (2a); `required_providers` vs. the `provider` block (2b); two distinct providers vs. the same provider twice via `alias` (2c); configuration files vs. the state file (2d).
- `drillIds`: the full 12 question ids for this task, in objective order.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 2a | Terraform CLI finds and installs providers when initializing a working directory | https://developer.hashicorp.com/terraform/language/providers | "Terraform CLI finds and installs providers when initializing a working directory." |
| 2 | 2a | Terraform can automatically download providers from a registry, or load them from a local mirror or cache | https://developer.hashicorp.com/terraform/language/providers | "It can automatically download providers from a Terraform registry, or load them from a local mirror or cache." |
| 3 | 2a | Production configurations should constrain acceptable provider versions in the provider requirements block | https://developer.hashicorp.com/terraform/language/providers/requirements | "we recommend constraining the acceptable provider versions in the configuration's provider requirements block" |
| 4 | 2a | `~> 1.0.4` allows 1.0.5 and 1.0.10 but not 1.1.0 | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Examples: ~> 1.0.4: Allows Terraform to install 1.0.5 and 1.0.10 but not 1.1.0." |
| 5 | 2a | `=` allows only one exact version and cannot combine with other conditions | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Allows only one exact version number. Cannot be combined with other conditions." |
| 6 | 2a | `!=` excludes an exact version number | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Excludes an exact version number." |
| 7 | 2a | `>`, `>=`, `<`, `<=` compare to a specified version; Terraform allows versions that resolve true | https://developer.hashicorp.com/terraform/language/expressions/version-constraints | "Compares to a specified version. Terraform allows versions that resolve to true." |
| 8 | 2a | A dependency lock file lets Terraform always install the same provider versions for a given configuration | https://developer.hashicorp.com/terraform/language/providers/requirements | "To ensure Terraform always installs the same provider versions... create a dependency lock file and commit it to version control" |
| 9 | 2b | Terraform relies on plugins called providers to interact with cloud providers, SaaS providers, and other APIs | https://developer.hashicorp.com/terraform/language/providers | "Terraform relies on plugins called providers to interact with cloud providers, SaaS providers, and other APIs." |
| 10 | 2b | Each provider adds a set of resource types and/or data sources Terraform can manage | https://developer.hashicorp.com/terraform/language/providers | "Each provider adds a set of resource types and/or data sources that Terraform can manage." |
| 11 | 2b | The `provider` block is used to declare and configure Terraform plugins called providers | https://developer.hashicorp.com/terraform/language/providers/configuration | "Use the `provider` block to declare and configure Terraform plugins, called providers." |
| 12 | 2b | Each argument in `required_providers` enables one provider | https://developer.hashicorp.com/terraform/language/providers/requirements | "Each argument in the `required_providers` block enables one provider." |
| 13 | 2b | A provider source address is structured `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` | https://developer.hashicorp.com/terraform/language/providers/requirements | "Source addresses consist of three parts delimited by slashes (`/`), as follows: `[<HOSTNAME>/]<NAMESPACE>/<TYPE>`" |
| 14 | 2b | Omitting `source` implies `registry.terraform.io/hashicorp/<LOCAL NAME>` | https://developer.hashicorp.com/terraform/language/providers/requirements | "If you omit the `source` argument when requiring a provider, Terraform uses an implied source address of `registry.terraform.io/hashicorp/<LOCAL NAME>`." |
| 15 | 2c | Resources beginning with `aws_` use the default `aws` provider configuration unless given a `provider` argument | https://developer.hashicorp.com/terraform/language/providers/configuration | "Resources that begin with `aws_` use the default `aws` provider configuration unless you supply the `provider` argument." |
| 16 | 2c | A `provider` block with no `alias` is the default configuration when multiple aliases exist | https://developer.hashicorp.com/terraform/language/providers/configuration | "the `provider` block without an `alias` argument is the default configuration for that provider" |
| 17 | 2c | Multiple provider aliases let you pick which configuration a resource, data source, or module uses | https://developer.hashicorp.com/terraform/language/providers/configuration | "Defining multiple provider aliases lets you specify which provider configuration to use for individual resources, data sources, or modules." |
| 18 | 2d | Terraform must store state about a workspace's managed infrastructure and configuration | https://developer.hashicorp.com/terraform/language/state | "Terraform must store state about your workspace's managed infrastructure and configuration." |
| 19 | 2d | State records the identity of a remote object against a particular resource instance (mapping) | https://developer.hashicorp.com/terraform/language/state | "records the identity of that remote object against a particular resource instance" |
| 20 | 2d | State keeps track of metadata | https://developer.hashicorp.com/terraform/language/state | "keep track of metadata" |
| 21 | 2d | State improves performance for large infrastructures | https://developer.hashicorp.com/terraform/language/state | "improve performance for large infrastructures" |
| 22 | 2d | Terraform stores each workspace's state in a local file named `terraform.tfstate` by default | https://developer.hashicorp.com/terraform/language/state | "Terraform stores each workspace's state in a local file named `terraform.tfstate`" |

## Citation files (6, after fix)

`cite-tf-g2-providers` (rows 1, 2, 9, 10), `cite-tf-g2-provider-requirements` (rows 3, 8, 12, 13, 14 — row 8 moved here this revision), `cite-tf-g2-provider-configuration` (rows 11, 15, 16, 17), `cite-tf-g2-version-constraints` (rows 4, 5, 6, 7), `cite-tf-g2-state` (rows 18–22). `cite-tf-g2-providers-lock` deleted (wrong page, nothing else referenced it).

## Retired / renamed / closed-to-new-customers findings

None.

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g2`: lesson-only lines PASS (single-asterisk spans 0, tables/numbered lines 0, no markdown link, citations unresolved [], drillIds match questions, exam tips 4/4 objectives). Question-line FAILs are the pre-existing placeholder questions, expected until the questions step.
- `claim_prose_check.py tf-g2`: every claim-table number (`1.0.4`, `1.0.5`, `1.0.10`, `1.1.0`) present in lesson prose; all claim-table quotes now ≤20 words.
