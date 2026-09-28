# Teacher round 1 — lesson-tf-g4

## Rows verified (13 of 75, exceeds the 10 minimum)
Claim rows 1, 3, 4/4b, 8, 12, 17, 26/27, 29, 39, 40, 41, 44, 45, 48/50, 55/56, 65, 66, 67, 68, 69, 70, 71
(fetched via WebFetch on developer.hashicorp.com: data-sources, block/resource, meta-arguments/depends_on,
meta-arguments/for_each, language/validate, manage-sensitive-data, manage-sensitive-data/write-only,
values/locals, expressions/types). All quotes matched the source verbatim in substance and were not
over-trimmed past their asserted strength. No fabricated or stretched quote found in this sample.
Also independently fetched terraform/language/resources/terraform-data and functions/nonsensitive,
neither cited in the claim table (see findings).

## Findings

**TEACHER-Lg4-001 (Low, format) — 4a, claim table.**
The prose sentence "it also covers the built-in `terraform_data` resource type, which stores values
and triggers Terraform operations without creating actual infrastructure" has no claim-table row
(URL + quote). The underlying fact is accurate (verified against
https://developer.hashicorp.com/terraform/language/resources/terraform-data: "The `terraform_data`
resource is useful for storing values which need to follow a manage resource lifecycle, and for
triggering provisioners when there is no other logical managed resource in which to place them."),
so this is a table-completeness gap, not a content error.
Fix: add a claim-table row — Section 4a, Doc URL
https://developer.hashicorp.com/terraform/language/resources/terraform-data, Quote: "useful for
storing values which need to follow a manage resource lifecycle, and for triggering provisioners"
(15 words).

**TEACHER-Lg4-002 (Low, undefined jargon) — 4a.**
"Meta-argument" appears twice and does real discriminator work the first time ("both blocks can
carry the same meta-arguments ... so a shared syntax is not the discriminator") but is never
defined. A student who doesn't already know the term can't evaluate why shared meta-arguments fail
to distinguish resource from data blocks.
Fix: insert one clause in 4a right after the parenthetical list, e.g. "— meta-arguments are
arguments every resource or data block accepts regardless of provider, listed on Terraform's
meta-arguments overview page, as opposed to a provider-specific argument." Cite
https://developer.hashicorp.com/terraform/language/meta-arguments (page lists count, for_each,
provider, lifecycle, depends_on under that heading; no single one-line definition sentence exists
on that page shorter than the paraphrase above, so the fix is a paraphrase + citation, not a quote).
Checked other jargon on the brief's list (expression, splat, interpolation, tuple, object, coercion,
lifecycle, precondition, drift, idempotent): tuple/object are defined via the list/set/map
enumeration in 4d; lifecycle and precondition are defined in context in 4f/4g; splat, interpolation,
drift, idempotent do not appear anywhere in this lesson and are not required by any of the 8
objective texts, so their absence is not a finding.

No other issues found across the 13 spot-checked rows or the internal-consistency re-read.

## Internal-contradiction check (4b / 4f, per round-1 brief)
Re-read 4b and 4f against each other and against themselves. Direction is stated once and held
consistently: 4b says an attribute reference both fetches a value and orders the referencer after
the referenced resource; 4f says `depends_on = [B]` inside A means A depends on B, "It says nothing
about anything that might depend on A." No g3-style reversal found — both sections agree on
direction and neither claims the dependency also protects/isolates the referenced resource's own
downstream dependents. No contradiction.

## Lesson additions requested
1. 4a — claim-table row for the `terraform_data` claim (TEACHER-Lg4-001).
2. 4a — one-clause definition of "meta-argument" before it is used to justify a discriminator
   (TEACHER-Lg4-002).
3. 4h — one sentence on `nonsensitive()` (see verdict below), doc-verified quote: "`nonsensitive`
   takes a sensitive value and returns a copy of that value with the sensitive marking removed,
   thereby exposing the sensitive value." Source:
   https://developer.hashicorp.com/terraform/language/functions/nonsensitive.

## Three-per-objective verdict (24 questions / 8 objectives)
- 4a: yes — 3 distinct facts (resource-vs-data by action, timing deferral, terraform_data exception).
- 4b: yes — 3 distinct facts (TYPE.LABEL vs data.TYPE.LABEL.ATTRIBUTE syntax, implicit reference
  also orders, depends_on's narrower behavior-only trigger).
- 4c: yes — variable / local / output are three cleanly separable concepts.
- 4d: yes — list/tuple vs set vs map/object vs null, plus the `==` coercion exception.
- 4e: yes, comfortably — for-expression, count vs for_each, try vs can, lookup, merge, conditional
  expression are six distinct testable facts for 3 slots.
- 4f: yes — depends_on vs create_before_destroy vs prevent_destroy, plus the lifecycle-literal-only
  rule and the prevent_destroy config-removal gap.
- 4g: yes — validation vs precondition vs postcondition vs check (4 mechanisms) plus explicit
  ordering and the can()/alltrue/anytrue pairing.
- 4h: yes — sensitive vs ephemeral vs write-only vs Vault is 4 distinct concepts for 3 slots, with
  room to spare.
All eight objectives have enough distinct, non-repetitive taught material for 3 questions each.

## can() / nonsensitive() verdict
The round-1 brief's premise is only half right for this lesson: **`can()` is already taught**,
substantially — 4e ("`can` ... never returns the value itself, only true or false") and 4g
("`can` reappears here as the standard way to turn a possibly-erroring expression into the boolean
a condition needs") both cover it with doc quotes. **`nonsensitive()` is not taught anywhere**
(0 occurrences). Given the brief's own priority on job-relevant sensitive-data discriminators, and
that `nonsensitive()` is a real hazard — a practitioner can use it to silence the redaction `sensitive`
provides while nothing about it touches state, the same trap as `sensitive` itself — this is worth
filling now, not deferring: one sentence (see Lesson additions #3) closes it before the 4h questions
are written, cheaper than finding a gap after 3 questions exist per the g1/g3 precedent cited in the
brief.

Lesson tf-g4: approve for question writing
Overall: approve
