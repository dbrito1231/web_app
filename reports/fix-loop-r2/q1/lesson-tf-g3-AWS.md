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

## Round 2

### (a) Own findings — Gone/not gone

**AWS-Lg3-001: Gone.** Row 42 now cites "This command applies a subset of the Terraform
language style conventions, along with other minor adjustments for readability." — re-fetched
the fmt page's intro paragraphs verbatim, confirmed genuine. The "does not check correctness"
point is now unquoted lesson reasoning in 3g's prose, no longer dressed as a quote. Fixed
correctly.

**AWS-Lg3-002: Gone.** 3d and 3f now say "0.15.2" and cite the destroy page's precise sentence
("The `-destroy` option to `terraform apply` exists only in Terraform v0.15.2 and later.") —
re-fetched and confirmed verbatim. The looser plan-page wording is kept at row 32 but explicitly
labeled as superseded, so it will not be used to "correct" 0.15.2 back to 0.15 later. This
resolution is right: the plan and destroy pages do state the boundary differently ("v0.15 and
earlier" vs. "v0.15.2 and later"), and 0.15.2 is the more precise, doc-supported cutover.

**Fabrication audit spot-check.** Independently re-fetched three quotes not among my 30
round-1 checks, chosen to include the replacement text: validate row 20 ("thus primarily useful
for general verification of reusable modules, including correctness of attribute names and
value types" — confirmed, lesson's wording is a trimmed but faithful substring), apply row 34
(confirmed verbatim), fmt row 43 (confirmed verbatim). All three genuine. This corroborates the
writer's "1 fabrication, 44 genuine (8 trimmed-but-faithful)" audit rather than just taking it on
faith.

### (b) Second-role check on Teacher findings

**TEACHER-Lg3-001 (version boundary): Gone.** Same underlying issue as AWS-Lg3-002, same fix,
confirmed above.

**TEACHER-Lg3-002 (CI acronym): Gone.** 3g now reads "a CI (continuous integration) pipeline."

**TEACHER-Lg3-003 (drift gloss): Gone.** 3e now reads "...has since drifted (changed outside
Terraform since the plan was made)."

**TEACHER-Lg3-004 (thin 3f, needs a third discriminator): Gone.** 3f now teaches
`destroy -target`, quoting the destroy page: "You can use the `-target` option to destroy a
particular resource and its dependencies," with the page's own example
`terraform destroy -target aws_instance.example`. Re-fetched this sentence directly — genuine.
I also re-fetched the plan page's `-target` description to check direction: it "extend[s] the
selection to include all other objects that those selections depend on," i.e. upstream
dependencies only, never downstream dependents. The lesson's corrected 3f text and exam tip now
say `-target` "also destroys whatever that resource depends on," matching this direction, and
correctly states the routes are equivalent only when the target has no dependencies of its own.
The Lead's fix (item 3 in the coordinator's brief) is accurate.

### (c)/(d) Question review — key, distractors, rationale, stems, citations, and flag literals

Read all 21 question files. Every `citationIds` entry matches the question's objective's single
g3 citation (3a → core-workflow, 3b → init, 3c → validate, 3d → plan, 3e → apply, 3f → destroy,
3g → fmt); `mcpStatus`/`reviewedOn` present on all 21.

Checked every flag/behavior literal that a key or rationale turns on against the doc pages:
`-upgrade` (ignores lock file, takes newest constraint-satisfying version) in 3b-mc2/3b-mr;
`-refresh-only` (state/output reconciliation only) in 3d-mc; `-out` (opaque file, replayable,
not hand-editable) in 3d-mr; `-target`'s dependency direction (extends to what the target
depends on, not what depends on it) in 3d-mc2, 3f-mc2, 3f-mr — all three now state the correct
direction and are mutually consistent with the fixed lesson; `-auto-approve` (removes prompt
regardless of `-destroy`) in 3e-mc and 3e-mr; saved-plan-file semantics (no recompute, no
prompt) in 3e-mc2; `destroy` vs `apply -destroy` vs `plan -destroy` alias/version relationship
in 3f-mc; `-recursive` and `-check` (exit-code, no rewrite, file-name listing) in 3g-mc/3g-mc2;
`validate` vs `fmt` scope in 3g-mr; `validate`'s no-remote-services / needs-plugins-not-credentials
boundary in 3c-mc2/3c-mr. No misstatement found in any of the 21 — every flag behavior tested in
a key or rationale matches its doc page at the correct strength, and the two reworked
consequence questions (`3d-mc2`, `3g-mc2`) and the two `-target`-direction rewrites (`3f-mc2`,
`3f-mr`) all check out against the sources I fetched this round.

No new findings. No `AWS-Qg3-###` issues.

Task tf-g3: close

Overall: approve
