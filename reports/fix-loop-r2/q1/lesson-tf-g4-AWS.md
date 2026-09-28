# lesson-tf-g4 — AWS (Terraform docs) review, round 1

## Method

Checked every quote using the Browser pane's rendered `get_page_text` (not WebFetch), reading
each source page in full and comparing the claim-table quote character for character against
the raw text, per RULES.md's method note.

## Rows verified (56 of 75 — far beyond the 12 minimum)

Pages fetched in full and cross-checked against the claim table:

- `language/data-sources` — rows 2, 3, 4, 4b, 6 (5 rows)
- `language/meta-arguments/depends_on` — rows 7, 8, 39, 40, 41 (5 rows)
- `language/block/resource` — rows 1, 5, 42, 43, 44, 45 (6 rows)
- `language/validate` — rows 46–59 (14 rows) + version-requirements block
- `language/expressions/conditionals` — rows 36, 37, 52, 60, 61 (5 rows)
- `language/manage-sensitive-data` — rows 62–68 (7 rows) + version-requirements block
- `language/manage-sensitive-data/write-only` — rows 69, 70, 71 (3 rows) + version requirement
- `language/functions/can` — row 31
- `language/functions/try` — row 30
- `language/expressions/types` — rows 15–23 (9 rows)
- `language/meta-arguments/for_each` — rows 27, 28, 29
- `language/meta-arguments/count` — cross-check for row 27
- `tutorials/secrets/secrets-vault` — rows 72, 73, 74

Every quote listed above is a verbatim, contiguous substring of its source page (word-boundary
trims only), with one exception (below). No fabricated quotes found — the g1/g3 defect class did
not repeat here across this large a sample.

## Findings

**AWS-Lg4-001 (Low, cite/attribution error, not a fabrication).** Claim-table row 27
("Use for_each when some instance arguments must have distinct values that can't be directly
derived from an integer index") is cited to `language/meta-arguments/for_each`. That page's
actual sentence, in its "How to choose between for_each and count" section, reads: *"Use for_each
when some instance arguments must have distinct values that can't be directly derived from an
integer."* — no "index". The word "index" only appears in the near-duplicate sentence on
`language/meta-arguments/count`'s own "How to choose between count and for_each" section: *"Use
for_each when some instance arguments must have distinct values that can't be directly derived
from an integer index."* The quote text itself is genuine and verbatim — it just lives on the
other page. Fix: repoint row 27's Doc URL (and `cite-tf-g4-for-each`'s citation, if it backs this
specific sentence) to `https://developer.hashicorp.com/terraform/language/meta-arguments/count`,
or swap the quote for the for_each page's own "...derived from an integer." wording. This is
exactly the kind of thing that looks like a fabrication until the correct page is checked, so
it's worth fixing even though it isn't one.

**AWS-Lg4-002 (Moderate, version sensitivity — item 5 in the brief).** The lesson states
`precondition`/`postcondition`/`check` (4g) and `ephemeral`/write-only arguments (4h) as
current facts with no version floor, but HashiCorp gates all of them:
- `language/validate` "Requirements": *"Terraform v0.13.0 or later for input variable
  validation. ... v1.2.0 or later for preconditions and postconditions. ... v1.5.0 or later for
  check blocks."*
- `language/manage-sensitive-data` "Requirements": *"Use Terraform 0.15 or later to add the
  sensitive argument... Use Terraform 1.10 or later to add the ephemeral argument... Use
  Terraform 1.11 or later to use a write-only argument on a managed resource."*
`check`, `ephemeral`, and write-only arguments are the newest constructs in the whole lesson
(1.5, 1.10, 1.11 respectively — all within the last ~2 years), and a candidate testing against
an older pinned Terraform version, or a real job running an older release, would not have them.
Fix: add one clause per feature naming the minimum version — e.g. in 4g's exam tip or intro,
"`check` blocks require Terraform 1.5+"; in 4h, "`ephemeral` requires 1.10+, write-only arguments
require 1.11+." This doesn't change any existing claim's truth, it just adds the missing
currency qualifier the brief asks for.

No other issues found. Directionality (4b implicit references, 4f `depends_on`,
`create_before_destroy`) matches the docs exactly, including the `depends_on = [B]` → "A depends
on B, B created first" direction. The 4h security claims are accurate and not overstated:
`sensitive` is correctly taught as CLI/UI redaction only, still written to state/plan, still
exposed via `terraform output -json/-raw`; `ephemeral` is correctly taught as omitted from state
and plan entirely, with the doc's own 6-item reference-context restriction list reproduced
correctly; write-only argument mechanics (`_wo`/`_wo_version`, resent every operation) match the
write-only page exactly. `data` vs `resource` timing/apply-deferral claim matches the
data-sources page's own "Data source behavior" section.

## can() / nonsensitive() verdict

The premise needs correcting: **`can()` is already taught** — extensively, in both 4e ("`try`
and `can` both catch a runtime evaluation error, but they return different things...") and again
in 4g ("`can` reappears here as the standard way to turn a possibly-erroring expression into the
boolean a condition needs"), backed by claim-table row 31 and the `functions/can` page verified
above. Only **`nonsensitive()`** is genuinely absent.

`nonsensitive()` doesn't appear on either doc page cited for 4h (`manage-sensitive-data`,
`manage-sensitive-data/write-only`); it lives on its own page,
`language/functions/nonsensitive`, which I fetched independently: *"nonsensitive takes a
sensitive value and returns a copy of that value with the sensitive marking removed, thereby
exposing the sensitive value."* Available since Terraform 0.15, same floor as `sensitive` itself.

Having read it, I agree with the Teacher: **worth filling now, not a reasonable scope boundary
to skip.** Reasons:
- It is the direct counterpart to a fact the lesson already teaches — "Terraform also
  automatically treats any expression that references a sensitive variable or output as
  sensitive" — `nonsensitive()` is literally the documented override for that propagation, so it
  completes a claim the lesson makes rather than introducing an unrelated topic.
- It is security-relevant in exactly the way item 4 of the brief cares about: misuse discloses a
  value ("If you use nonsensitive with content that ought to be considered sensitive then that
  content will be disclosed"), and it's a very plausible wrong-answer or right-answer shape for a
  4h question ("how do you deliberately surface a hash derived from a sensitive value" vs. a
  distractor that misuses it to leak the raw secret).
- It reinforces rather than complicates the lesson's existing theme: `nonsensitive()` only
  changes the *display* marking, the same "display control, not storage control" idea already
  taught for `sensitive` — a natural one-paragraph extension, not a new concept.
- Teach-before-test: if a writer reaches for `nonsensitive()` in any of the 24 questions (a
  reasonable thing to do for 4h, given how squarely it sits in this objective), the lesson
  currently has nothing to teach it against, which would violate RULES.md's teach-before-test
  requirement outright rather than just being a coverage gap.

Suggested addition (one short paragraph at the end of 4h, doc-verified, ≤20-word quotes):
`nonsensitive()` "takes a sensitive value and returns a copy of that value with the sensitive
marking removed" — it only lifts the display marking already discussed for `sensitive`, it does
not affect what was already stored in state, and misusing it "will cause values that Terraform
would normally have considered as sensitive to be treated as normal values and shown clearly in
Terraform's output."

## New retired/renamed/closed-service finds

None.

---

Lesson tf-g4: approve for question writing
Overall: approve
