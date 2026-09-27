# lesson-tf-g1 / lesson-tf-g2 — Round 1 technical review (AWS role, HashiCorp docs as primary source)

## Rows verified (11 total, WebFetch on developer.hashicorp.com)

**tf-g1** (claim table rows, source: `/terraform/intro`, `/terraform/intro/vs/cloudformation`):
- Row 1 — "infrastructure as code tool that lets you build, change, and version..." — exact match on `/terraform/intro`.
- Row 3 — "Terraform configuration files are declarative, meaning that they describe the end state..." — exact match on `/terraform/intro`.
- Row 9 — "orchestrate an AWS and OpenStack cluster simultaneously..." — exact match on `/terraform/intro/vs/cloudformation`; confirms the claim (Terraform runs both clouds from one config), not a mere mention.
- Row 10 — "single unified syntax, instead of requiring operators to use independent and non-interoperable tools..." — exact match, same page; confirms the claim.
- Row 11 — "represent and manage the entire infrastructure with its supporting services, instead of only the subset..." — exact match, same page; confirms the claim.

**tf-g2**:
- Row 4 — `~> 1.0.4` example — exact match on `/terraform/language/expressions/version-constraints`.
- Row 8 — dependency lock file claim — **quote does not appear on the cited page.** See Finding AWS-Lg2-001.
- Row 13 — source-address format `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` — exact match on `/terraform/language/providers/requirements`.
- Row 15 — "Resources that begin with `aws_` use the default `aws` provider configuration..." — exact match on `/terraform/language/providers/configuration`.
- Row 16 — "provider block without an alias argument is the default configuration..." — exact match, same page.
- Row 19 — "record[s] the identity of that remote object against a particular resource instance" — present, `/terraform/language/state`; confirms the mapping claim, though verbatim quote has a tense mismatch (see Finding AWS-Lg2-002).
- Row 21/22 — "improve performance for large infrastructures," and default local file `terraform.tfstate` — both confirmed current (no deprecation notice as of the live page).

That is 11 rows spot-checked (5 in g1, 6 in g2), above the 8-row minimum, each checked for "asserts the claim" not just "mentions the topic."

## Findings

**AWS-Lg2-001 — Major — lesson-tf-g2.json, section tf.004.2a, claim-table row 8 / citation `cite-tf-g2-providers-lock`**
The quote "To ensure Terraform always installs the same provider versions for a given configuration, you can use Terraform CLI to create a dependency lock file and commit it to version control" is cited to `https://developer.hashicorp.com/terraform/cli/commands/providers/lock`. That page is the `terraform providers lock` subcommand reference; its own opening text is "The `terraform providers lock` adds new provider selection information to the dependency lock file without initializing the referenced providers..." — a different claim. The quoted sentence is actually the introduction of `https://developer.hashicorp.com/terraform/language/files/dependency-lock` (confirmed via search). Fix: change the URL in claim-table row 8 and in citation file `cite-tf-g2-providers-lock.json` to `https://developer.hashicorp.com/terraform/language/files/dependency-lock`, and rename the citation id if the naming convention expects the id to match the page (e.g. `cite-tf-g2-dependency-lock`). The lesson prose claim itself is accurate; only the citation is wrong.

**AWS-Lg2-002 — Low — lesson-tf-g2.json, section tf.004.2d, claim-table row 19**
Quote is given as "record the identity of that remote object against a particular resource instance." The actual doc sentence is "...it **records** the identity of that remote object against a particular resource instance..." (present tense, embedded mid-sentence: "When Terraform creates a remote object in response to a change of configuration, it records..."). Not a substantive error, but the claim-table rule asks for a verbatim quote; fix by changing "record" to "records" in the claim table (the lesson's own prose paraphrases correctly and is not affected).

No other misquotes, no version-stated-as-current-but-stale claims, and no deprecated/renamed terms found in either lesson. `required_providers`, provider installation, the dependency lock file, and the constraint operators (`=`, `!=`, `>`, `>=`, `<`, `<=`, `~>`) are all stated in line with the current docs, with no operator or syntax that has been renamed or removed.

## g1 sourcing judgment (11 rows on 2 pages)

Two pages can carry all 11 rows **as currently written**, because every row already has its own verbatim, on-topic quote and group 1 is explicitly the overview/conceptual tier of the objective list (what IaC is, why it helps, that Terraform is multi-cloud) rather than the mechanism tier that groups 2–4 cover in depth. I checked five of the eleven rows directly and all five both resolve and assert (not merely mention) the attached claim.

That said, two rows are the weakest links and are the ones I'd single out if this lesson is revisited later for a deeper technical pass:
- **Row 5** (resource graph / parallel creation of non-dependent resources) — `/terraform/intro` states this as a bullet-point benefit; HashiCorp's own dependency-graph mechanics live on a separate internals page. For a group-1 "why Terraform" claim this is fine, but it is the most mechanism-like claim resting on the marketing-toned intro page.
- **Row 7** (HCP Terraform collaboration) — same pattern: a specific product claim resting on an intro paragraph rather than an HCP Terraform product page. Fine for this lesson's tier, but the row a technical reviewer would want re-sourced first if group 8 (which does cover HCP Terraform) needs a shared citation later.
Rows 1–4, 6, 8–11 are squarely within what their two source pages are written to assert, so I would not require new citations for them.

## Objective and format coverage

All seven group-1/group-2 objectives (`tf.004.1a/1b/1c`, `tf.004.2a/2b/2c/2d`) have their own `###` section, in id order, each ending with `**Exam tip:**`. Both lessons keep the single `##` title and end with the standard `### Warnings` section — both are the established pattern per RULES.md, not defects.

`required_providers` vs `provider` block (2b) and single-provider vs same-provider-twice-via-alias (2c) are each given an explicit, applicable rule ("if the stem is about which version Terraform is allowed to download, that is `required_providers`; if it's about a runtime setting for an already-downloaded plugin, that is the `provider` block" / "two different platforms = two ordinary declarations; the same platform twice = `alias`"), not just a true sentence a student would have to infer from. This resolves the confusion the task asked me to check.

Teach-before-test readiness: both lessons state the key fact and the contrasting wrong-answer fact for every discriminator, sufficient to support MC/MR questions once written.

Lesson tf-g1: approve for question writing
Lesson tf-g2: not yet — hold for AWS-Lg2-001 (citation URL wrong; lesson text itself is fine, no rewrite needed) and AWS-Lg2-002 (verbatim-quote nit) to be fixed in the citation file / claim table.

Overall: concerns
