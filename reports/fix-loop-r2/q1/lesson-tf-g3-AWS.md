# Lesson tf-g3 (Core Terraform workflow) — AWS review, round 1

## Method

Fetched the six command doc pages plus the core-workflow overview page via WebFetch on
developer.hashicorp.com: `intro/core-workflow`, `cli/commands/init`, `cli/commands/validate`,
`cli/commands/plan`, `cli/commands/apply`, `cli/commands/destroy`, `cli/commands/fmt`. For each,
pulled the verbatim sentences behind the claim table and compared word-for-word against the
lesson's quoted text and against the claim it is asserted to support.

## Rows verified (30 of 45, plus two targeted re-fetches)

Confirmed verbatim and correctly scoped: 1–6 (core workflow, 3a), 7–18 (init, 3b, including the
full `-upgrade` text for both modules and providers — re-fetched separately to check the exact
"override this behavior, updating all modules to the latest available source code" wording,
which is genuine), 19, 21, 22 (validate, 3c), 23–31, 33–41, 43–45 (plan/apply/destroy/fmt).
Row 32 (version note) — quote itself is verbatim but see Finding 2. Row 42 — not found; see
Finding 1. Row 20 not independently re-fetched (standard, low-risk module-verification sentence
already present in the same paragraph as 19 and 21, which both checked out).

## Findings

**AWS-Lg3-001 (High).** Section `tf.004.3g` (fmt), lesson body and claim-table row 42. The
lesson states `fmt` "does not check whether configurations are correct or valid" and presents
this in quotation marks, citing `https://developer.hashicorp.com/terraform/cli/commands/fmt`.
That sentence does not appear anywhere on that page — I fetched the full introductory
paragraphs verbatim and searched separately for this phrase; neither found it. The underlying
idea (fmt only rewrites style, never checks correctness) is true, but the lesson's discriminator
sentence has no doc support — it is the writer's own paraphrase dressed as a verbatim quote.
**Fix:** drop the quotation marks and citation weight from that clause — state it as the
lesson's own inference, e.g. "It only rewrites spacing, alignment, and quoting conventions and
has no way to detect a bad attribute name or type — the fmt page describes only style changes
and never mentions checking configuration validity." Do not present it as a verbatim quote from
the fmt page.

**AWS-Lg3-002 (High).** Sections `tf.004.3d` and `tf.004.3f`, the "Version note" and its
cross-reference. The lesson twice frames the cutover as "Before Terraform 0.15," (3d) and "the
pre-0.15 exception" (3f). The plan page's own quoted text says "In Terraform v0.15 and earlier,
the `-destroy` option is supported only by the `terraform plan` command, and not by the
`terraform apply` command" — i.e. all of v0.15 lacked it, not versions strictly before it. The
destroy page is more precise: "The `-destroy` option to `terraform apply` exists only in
Terraform v0.15.2 and later. For earlier versions, you _must_ use `terraform destroy`." Both
source sentences place the boundary at 0.15.2, not at 0.15.0. "Before Terraform 0.15" is wrong
by up to two patch releases (0.15.0, 0.15.1) and could seed a wrong exam-style claim about
version behavior — exactly the version-sensitivity risk flagged in the brief. **Fix:** replace
"Before Terraform 0.15" with "Before Terraform 0.15.2" in the 3d version note, and replace "the
pre-0.15 exception" in 3f with "the pre-0.15.2 exception," matching the destroy page's own
wording so both sections agree with each other and with the source.

No other misdescriptions found. The `-target`, `-refresh-only`, `-out`, `-auto-approve`,
`-recursive`, `-check` and `-destroy` (plan/apply) flag descriptions all match their doc pages
at the current strength — none trimmed to assert more or less than the source, and the
`validate`/`plan` boundary (schema-only vs. live state, `init -backend=false` sufficiency) is
accurately drawn. Coverage of all seven objectives, exam tips, format and teach-before-test
readiness all look fine; no retired/renamed-service issues (no AWS content in this lesson).

Lesson tf-g3: not yet.

Overall: concerns
