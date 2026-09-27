# Lesson tf-g1 (IaC with Terraform) — implementation report

## Outline

- Replaced the placeholder `bodyMarkdown` with a full lesson covering all 3 objectives in id order: tf.004.1a, tf.004.1b, tf.004.1c.
- One `###` section per objective (`### tf.004.<id> — <objective text>`), each ending with an `**Exam tip:**` line; single `##` lesson title kept (`## IaC with Terraform`).
- Added the required `### Warnings` section, adapted for a Terraform context (no credentialed apply/destroy, the forbidden MCP execute tools, plain-text state file risk) since this is the first Terraform lesson and the AWS-specific Warnings text (root user, teardown, budget alerts) does not apply.
- Discriminators taught per objective: IaC (versioned file) vs. manual console/CLI provisioning, and declarative vs. imperative (1a); an IaC pattern's tracked-state/dependency-graph advantage vs. a plain repeatable automation script (1b); Terraform's provider-plugin, multi-cloud model vs. a single-cloud-specific tool such as CloudFormation (1c).
- Jargon defined on first use: IaC, HCL (HashiCorp Configuration Language), declarative vs. imperative, provider (as a plugin), service-agnostic.
- `drillIds` corrected from the stale 4-id list to the full 9 question ids for this task, in objective order (`-mc`, `-mc2`, `-mr` per objective): `q-tf-004-1a-mc`, `q-tf-004-1a-mc2`, `q-tf-004-1a-mr`, `q-tf-004-1b-mc`, `q-tf-004-1b-mc2`, `q-tf-004-1b-mr`, `q-tf-004-1c-mc`, `q-tf-004-1c-mc2`, `q-tf-004-1c-mr`.
- `citationIds` replaced the single shared `cite-tf-004` (too generic — it only cites the top-level HashiCorp exam-content-list page) with 2 new page-specific citations: `cite-tf-g1-intro`, `cite-tf-g1-vs-cloudformation`.
- Confirmed `cite-tf-004` is still referenced by `lesson-tf-g3.json` through `lesson-tf-g8.json` (`grep -rl "cite-tf-004" content/`), so it was left in place, not deleted.
- No numeric claims were made in this lesson (1a–1c are conceptual, not version/number-specific), so `claim_prose_check.py tf-g1` has nothing to enforce beyond the absence of stray numbers; confirmed below.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | 1a | Terraform is an IaC tool that builds, changes, and versions cloud and on-prem resources | https://developer.hashicorp.com/terraform/intro | "Terraform is an infrastructure as code tool that lets you build, change, and version cloud and on-prem resources safely and efficiently." |
| 2 | 1a | IaC resources are defined in human-readable files meant to be versioned, reused, shared | https://developer.hashicorp.com/terraform/intro | "Define both cloud and on-prem resources in human-readable configuration files that you can version, reuse, and share." |
| 3 | 1a | Terraform configuration files are declarative — they describe the end state | https://developer.hashicorp.com/terraform/intro | "Terraform configuration files are declarative, meaning that they describe the end state of your infrastructure." |
| 4 | 1b | Terraform provides one consistent workflow across the whole infrastructure lifecycle | https://developer.hashicorp.com/terraform/intro | "Use a consistent workflow to provision and manage all of your infrastructure throughout its lifecycle." |
| 5 | 1b | Terraform builds a resource graph and creates/modifies non-dependent resources in parallel | https://developer.hashicorp.com/terraform/intro | "Terraform builds a resource graph to determine resource dependencies and creates or modifies non-dependent resources in parallel." |
| 6 | 1b | Terraform tracks real infrastructure in a state file that acts as a source of truth | https://developer.hashicorp.com/terraform/intro | "Terraform keeps track of your real infrastructure in a state file, which acts as a source of truth for your environment." |
| 7 | 1b | Teams commit configuration to a VCS and use HCP Terraform to manage workflows across teams | https://developer.hashicorp.com/terraform/intro | "Commit it to a Version Control System (VCS) and use HCP Terraform to efficiently manage Terraform workflows across teams." |
| 8 | 1c | Providers let Terraform work with virtually any platform or service with an accessible API | https://developer.hashicorp.com/terraform/intro | "Providers enable Terraform to work with virtually any platform or service with an accessible API." |
| 9 | 1c | Terraform can orchestrate AWS and OpenStack simultaneously plus third-party providers like Cloudflare/DNSimple | https://developer.hashicorp.com/terraform/intro/vs/cloudformation | "Terraform can be used to orchestrate an AWS and OpenStack cluster simultaneously, while enabling 3rd-party providers like Cloudflare and DNSimple." |
| 10 | 1c | Terraform's single unified syntax replaces independent, non-interoperable per-platform tools | https://developer.hashicorp.com/terraform/intro/vs/cloudformation | "It provides a single unified syntax, instead of requiring operators to use independent and non-interoperable tools for each platform and service." |
| 11 | 1c | Terraform manages the entire infrastructure and its supporting services, not just one provider's subset | https://developer.hashicorp.com/terraform/intro/vs/cloudformation | "Terraform to represent and manage the entire infrastructure with its supporting services, instead of only the subset that exists within a single provider." |

## New citation files (2)

`cite-tf-g1-intro` (developer.hashicorp.com/terraform/intro — rows 1–8), `cite-tf-g1-vs-cloudformation` (developer.hashicorp.com/terraform/intro/vs/cloudformation — rows 9–11). Both `accessed: "2026-09-26"`.

## Retired / renamed / closed-to-new-customers findings

None named in this lesson (no AWS services are discussed here; CloudFormation is named only as a currently-supported comparison tool, not flagged as retired).

## Checks

- `content_lint.py`: PASS (see combined run below).
- `q1_batch_check.py tf-g1`: all lesson-only lines PASS (single-asterisk spans 0, tables/numbered lines 0, no markdown link, citations unresolved [], drillIds match questions, exam tips 3/3 objectives). The question-line FAILs (stem echoes objective text, missing citationIds, `mcpStatus`/`reviewedOn` not verified, duplicate 6-word openings, longest-is-key rate) are the pre-existing placeholder questions, expected to fail until the questions step per the task prompt.
- `claim_prose_check.py tf-g1`: PASS — this lesson makes no numeric claims, so there is nothing for the script to find missing from prose.
