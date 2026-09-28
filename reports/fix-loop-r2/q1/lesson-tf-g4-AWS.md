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

## Round 2

Method: HashiCorp pages fetched with `curl -sL` piped through a small HTML-to-text stripper
(`r2aws_strip.py`, written this turn in the scratchpad), not WebFetch, per RULES.md. Pages fetched
fresh this round: `functions/sort`, `expressions/type-constraints`, `meta-arguments/lifecycle`,
`functions/nonsensitive` (latest, plus pinned `v1.2.x`/`v1.5.x`/`v1.9.x` to check for a documented
behavior change), `language/validate`, `manage-sensitive-data`, `manage-sensitive-data/write-only`,
`meta-arguments/count`, `resources/terraform-data`, `meta-arguments` (overview), `data-sources`,
`cli/config/environment-variables`.

### (a) My own round-1 findings

- **AWS-Lg4-001 — Gone.** Claim-table row 27 now cites
  `https://developer.hashicorp.com/terraform/language/meta-arguments/count`. Re-fetched that page
  this round: "Use for_each when some instance arguments must have distinct values that can't be
  directly derived from an integer index" is present verbatim in its "How to choose between count
  and for_each" section. Correctly repointed.
- **AWS-Lg4-002 — Gone.** Re-fetched `language/validate` and `manage-sensitive-data` this round.
  Lesson rows 75–78 quote "Terraform v1.2.0 or later for preconditions and postconditions,"
  "Terraform v1.5.0 or later for check blocks," "Use Terraform 1.10 or later to add the ephemeral
  argument to variables and child module outputs," and "Use Terraform 1.11 or later to use a
  write-only argument on a managed resource" — all four match the current docs verbatim, and the
  lesson prose states each floor next to the feature it gates (4g and 4h).
- **`nonsensitive()` request — Gone, but see AWS-Qg4-005 below.** The lesson now has a full
  paragraph on `nonsensitive()` in 4h with three doc-verified quotes (rows 79–81), matching the
  current `functions/nonsensitive` page word for word. The lesson addition itself is accurate. The
  problem that surfaced this round is downstream, in `q-tf-004-4h-mr`'s use of a *fourth*
  `nonsensitive()` fact that was never in the lesson and turns out to be stale doc wording — see
  (c)/(e).

### (b) Second-role check: Teacher's round-1 findings

- **TEACHER-Lg4-001 — Gone.** Claim-table row 82 quotes "useful for storing values which need to
  follow a manage resource lifecycle, and for triggering provisioners." Re-fetched
  `resources/terraform-data`: the page's actual sentence is "The terraform_data resource is useful
  for storing values which need to follow a manage resource lifecycle, and for triggering
  provisioners when there is no other logical managed resource in which to place them." Verbatim
  match, correctly trimmed.
- **TEACHER-Lg4-002 — Gone.** Claim-table row 83 quotes "Meta-arguments are a class of arguments
  built into the Terraform configuration language that control how Terraform creates and manages."
  Re-fetched `language/meta-arguments`: opening sentence is "Meta-arguments are a class of arguments
  built into the Terraform configuration language that control how Terraform creates and manages
  your infrastructure." Verbatim match. The lesson now defines the term before using it as a
  discriminator in 4a.

### (c) / (d) / (e) Questions, version numbers, and Lead Dev pre-check verification

**AWS-Qg4-001 (High, confirms and sharpens LD-Qg4-001).** The 10 flagged rationales
(`4a-mr`, `4b-mr`, `4c-mr`, `4d-mr`, `4e-mr`, `4f-mc`, `4f-mr`, `4g-mr`, `4h-mc2`, `4h-mr`) do use
letter references that no longer match the current choice order — I read every one of the ten
choice-sets against its rationale directly. The shift is systematic (content shifted by one letter
in most cases, consistent with a post-hoc reorder for key-balance), but **in two of the ten it is
worse than a cosmetic mislabel: the rationale calls a correct key "wrong."**
- `q-tf-004-4g-mr` (keys `c`, `d`): rationale says *"c reverses the real order... d is wrong; self
  inside a precondition would refer to an object that doesn't exist yet."* Both `c` and `d` are this
  question's keys ("Terraform executes input variable validations immediately, before it generates
  a plan" and "A variable validation block can only evaluate the variable it is attached to"). The
  content actually being described ("reverses order," "self inside precondition") belongs to
  choices `a` and `b`.
- `q-tf-004-4h-mc2` (key `d`): rationale says *"...d is wrong; sensitive and write-only are unrelated
  mechanisms."* `d` is the key ("No — write-only arguments need Terraform 1.11 or later..."). The
  "sensitive/write-only are unrelated" content actually refutes choice `c`.
Fix: rewrite all 10 rationales to describe each wrong choice by its content, with no letters at all
(RULES.md already bans letter references outright). Two doc-verified corrected rationales as a
pattern for the rest:
  - `q-tf-004-4g-mr`: "Reversing the order — claiming postconditions run before preconditions —
    misstates the actual sequence; preconditions run first. A precondition cannot reference `self`
    the way a postcondition can, because `self` reflects the object's final attributes, which don't
    exist yet when a precondition runs. Check blocks do not run before a plan exists either — they
    run at the end of a plan or apply operation."
  - `q-tf-004-4h-mc2`: "1.5 is a real Terraform version floor, but it belongs to `check` blocks, not
    write-only arguments. Write-only arguments do have a minimum version, so claiming they have none
    is wrong. Marking a value `sensitive` does not unlock or enable write-only argument support —
    the two mechanisms are unrelated."

**AWS-Qg4-002 (High, confirms LD-Qg4-002).** `q-tf-004-4d-mc` choice d ("Sort the set alphabetically
first; it becomes indexable") is a real second path to the stated goal, not a false one. Verified via
`functions/sort` ("sort takes a list of strings and returns **a new list** with those strings sorted
lexicographically") and `expressions/type-constraints` ("Sets are almost similar to both tuples and
lists... When a set is converted to a list or tuple... If the set's elements were strings, they will
be in lexicographical order"). Terraform auto-converts a `set(string)` argument to `list(string)`
when a function parameter requires a list, so `sort(local.subnet_names)` on a `set(string)` works
today and returns an indexable list — the rationale's "a set is still not indexable, sorted or not"
is false for this case. `sort` is also untaught in the lesson. Fix: replace choice d with **"Call
`values()` on the set to obtain an ordered, indexable list"** — `values()` is real but operates on a
map/object (returning its values by sorted key), not a set, so applying it to a `set(string)` is
wrong for a reason 4d already teaches (map/object is "identified by named labels"; a set has "no
secondary identifiers"). Same real-function-wrong-category shape, no lesson addition needed.

**AWS-Qg4-003 (High, confirms LD-Qg4-003).** `q-tf-004-4f-mc2`:
- Choice c, `ignore_changes = [all]`: verified against `meta-arguments/lifecycle` — *"Instead of a
  list of items, you can use the `all` keyword to instruct Terraform to ignore all attributes."* The
  documented form is the bare keyword `ignore_changes = all`, not a one-element list containing the
  identifier `all`; as written this choice's syntax doesn't match any documented form, and
  `ignore_changes` is untaught anywhere in this lesson (0 hits, confirmed independently).
- Choice b, `count = 2 (creates two independent instances instead of sequencing one resource's own
  replacement)`: `count` is a `count` meta-argument, not a `lifecycle` argument, so it's a category
  error against a "which lifecycle argument fits" stem, not a same-category wrong answer — and the
  parenthetical spells out exactly why it's wrong, a banned self-answering tell.
Fix, keeping all four choices genuine `lifecycle` arguments:
  - Replace `ignore_changes = [all]` with **`replace_triggered_by = [aws_lb_target_group.old]`** —
    real (`meta-arguments/lifecycle`: "Terraform replaces the resource when any of the referenced
    resources or specified attributes change") but wrong here because it forces a replacement on a
    trigger rather than sequencing create-before-destroy. Needs one doc-verified lesson sentence in
    4f (**Lesson addition requested**): "The `replace_triggered_by` argument replaces the resource
    when any of the referenced resources or specified attributes change," cited to
    `https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle`.
  - Replace `count = 2 (...)` with **`create_before_destroy = false`** — the documented default
    behavior, real, same-category, and wrong for a reason 4f already teaches (the default
    destroy-then-create order is exactly the gap the scenario is trying to avoid). No lesson
    addition or self-answering parenthetical needed.

**AWS-Qg4-004 (Medium, confirms LD-Qg4-004).** `q-tf-004-4e-mc2` key "`can`, boolean-only" echoes
the stem's "plain true/false result" and is the only choice carrying an appended justification.
Fix: shorten the key to plain **"`can`"**, and to preserve the round-2 length-balance work (longest-
is-key 6%, shortest-is-key 0%), lengthen choice a instead of leaving the key short and bare: **"`try`,
using its first successful argument as the result"** (accurate to `try`'s documented behavior, still
wrong for this stem since it returns a value, not a boolean).

**AWS-Qg4-005 (High, confirms and extends LD-Qg4-005 — this is the most important finding this
round).** `q-tf-004-4h-mr` choice c ("Calling `nonsensitive()` on a value that was never marked
sensitive quietly returns that same value with no warning") is marked wrong, with the rationale
asserting this is "documented as an error, not a quiet no-op." I fetched `functions/nonsensitive` at
three pinned versions specifically to check LD's suspicion that this changed:
- `v1.2.x` and `v1.5.x`: *"nonsensitive will return an error if you pass a value that isn't marked
  as sensitive, because such a call would be redundant and potentially confusing,"* with a worked
  example showing `Error: Invalid function argument ... the given value is not sensitive, so this
  call is redundant.`
- `v1.9.x` and the current/latest page: that same sentence is now *"nonsensitive will make no
  changes to values that aren't marked as sensitive, even though such a call may be redundant and
  potentially confusing."* — a silent no-op, not an error. (The current page still carries a stale
  `> nonsensitive("clear")` → error example lower down that HashiCorp appears not to have updated to
  match its own revised prose — that leftover example is itself an inconsistency in HashiCorp's
  current page, but the deliberate behavioral statement is the prose sentence, not the stale
  example.)
The lesson's `nonsensitive()` paragraph (added this round, see (a)) states no version floor for this
specific no-arg-error-vs-no-op behavior, and the question pins no version either. Under the
**current** documented behavior, choice c is **true**, not false — the rationale's factual basis is
stale, exactly the failure mode RULES.md's "After applying a fix" section warns about (a claim
asserting something the current source no longer supports). Fix: replace choice c with a distractor
that doesn't depend on this version-sensitive wording: **"`nonsensitive()` converts the value to a
different type, the same way `tostring()` or `tonumber()` would"** — real functions exist in this
family, and this is wrong for a reason the lesson's own `nonsensitive()` paragraph already states:
"It only lifts the CLI/UI redaction already taught for `sensitive` — it does not touch state, does
not make a value ephemeral" (i.e., it changes a marking, not a type). Also: do not "fix" this by
adding an error-on-unmarked-value claim to the lesson instead — that would directly contradict the
current page this task's own citation points to.

**Version numbers (task d).** Re-verified against current docs, independent of the writer's and
round-1 claim table: `language/validate` — "Terraform v1.2.0 or later for preconditions and
postconditions," "v1.5.0 or later for check blocks"; `manage-sensitive-data` — "Use Terraform 1.10
or later to add the ephemeral argument"; `manage-sensitive-data/write-only` — "you must use
Terraform v.1.11 or later" for write-only arguments. All four numbers, everywhere they appear across
the lesson and the 24 questions (including the deliberately-wrong pairings in `q-tf-004-4g-mc2` and
`q-tf-004-4h-mc2`, both of which correctly use real floors attached to the wrong feature), match the
current docs. No version-number errors found.

**AWS-Qg4-006 (Medium, confirms LD-Qg4-006).** `q-tf-004-4c-mc2` choice c's wrongness depends on the
`TF_VAR_` prefix rule — confirmed real (`cli/config/environment-variables`: "The environment
variables must be in the format `TF_VAR_name`") but never mentioned in this lesson (0 hits). Fix: add
one sentence to 4c (**Lesson addition requested**, doc-verified): "Terraform only reads environment
variables carrying the `TF_VAR_` prefix (for example `TF_VAR_subnet_id`), never an identically-named
bare variable," cited to `https://developer.hashicorp.com/terraform/cli/config/environment-variables`.
Choice d (reusing the previous apply's value) needs no citation — nothing in the lesson or the docs
suggests Terraform remembers a variable's value between runs, so it's eliminable by the absence of
any taught persistence mechanism rather than by a specific untaught fact.

**AWS-Qg4-007 (Medium, confirms LD-Qg4-007).** `q-tf-004-4b-mc2` choices a ("based on the instance
profile depending on the instance's IP address") and b ("treating the reference as pointing to
whichever object is destroyed first") invent mechanisms no part of Terraform's dependency model
uses — not RULES.md's literal strawman examples (hardcode an IP, do it by hand), but fabricated
reasoning attached to a real conclusion, which fails the same "is the reason it's wrong taught in
this lesson" test from the other direction: the claim itself isn't taught anywhere because it isn't
true anywhere. Fix, using real, taught misconceptions about this exact scenario:
  - a → **"Terraform infers no ordering between the two resources at all, because a `name` argument
    is just plain data with no dependency implication"** — tests 4b's actual discriminator (an
    attribute reference does create an implicit dependency) against its natural wrong belief.
  - b → **"Terraform creates both resources in parallel unless an explicit `depends_on` argument is
    added"** — directly contradicted by 4b's own text ("no extra block needed") and a genuinely
    common beginner misconception.

**AWS-Qg4-008 (Low, partially confirms LD-Qg4-008).** `q-tf-004-4d-mr` choice d ("can never be used
interchangeably... in Terraform's own documentation") is absolute in phrasing but tests a fact 4d
teaches verbatim ("Terraform's own documentation treats list and tuple as interchangeable terms
whenever the distinction... doesn't matter") — no fix needed. `q-tf-004-4a-mr` choice e ("locked and
can never be refreshed") tests a fact that is **not** in the lesson body — I found no sentence
stating data sources are re-read on later runs. Verified real and current via `data-sources`: "By
default, Terraform refreshes prior to creating a plan." Fix: add that sentence (with this citation)
to 4a near the existing timing discussion so the fact `4a-mr`'s rationale relies on is actually
taught.

**Stem-echo classification for `q-tf-004-4a-mr` (specifically requested).** **Structural, not
leakage.** The shared tokens are "data," "block," and "apply" — "data block" is the scenario's own
subject noun, present in every choice, and "apply" was deliberately echoed into distractor d during
the round-2 fix pass ("once Terraform reaches the apply step"). Both satisfy RULES.md's Student-
section test (does the term also appear in a distractor, or does it simply name the object the stem
introduced — yes, on both counts). No waiver entry is needed beyond recording this classification.

**Lesson findings LD-Lg4-009 to -012.**
- **LD-Lg4-009 — confirmed, Low-Medium.** 4g opens "Three condition mechanisms check different
  things at different times" then later calls `check` "the fourth mechanism, the newest of the
  four." Read in sequence, a reader is told three, then told four. Fix: change the opening clause to
  "Four condition mechanisms check different things at different times," or add ", plus a fourth
  introduced below."
- **LD-Lg4-010 — confirmed, Medium, with a source nuance.** 4h's "There are three ways to get one
  [ephemeral value]" lists a write-only argument alongside the `ephemeral` argument and the
  `ephemeral` block, but a later paragraph correctly says a write-only argument is "how an ephemeral
  value **reaches**" a resource, not a way to produce one — a real disagreement between the lesson's
  own two paragraphs. Context for the record: HashiCorp's `manage-sensitive-data` page makes the same
  conflation — it groups "A write-only argument on a managed resource" under "Terraform provides four
  ways to define ephemeral values in your configuration" (verbatim), and that source list is itself
  inconsistent (says "four," enumerates three) — so the lesson inherited this looseness rather than
  inventing it, but the self-contradiction between the lesson's own two paragraphs still needs
  fixing. Fix: "There are two ways to originate an ephemeral value — the `ephemeral` argument on a
  variable or child module output, or a dedicated `ephemeral` resource block — plus a write-only
  argument as the channel that delivers one into an ordinary managed resource."
- **LD-Lg4-011 — confirmed, Low.** "in the writer's own words" precedes a verbatim HashiCorp
  documentation quote, not lesson-author prose. Fix: "in the documentation's own words."
- **LD-Lg4-012 — confirmed, Low.** 4a has a doubled "but": "Terraform normally reads a data source
  during planning, but "Terraform attempts to query data sources during the planning phase," but "it
  may defer reading until the apply phase."" Fix: drop the first "but."

**Key-length observation — my view: metric over-fitting, not a new tell.** With four choices,
excluding the longest (the existing 35% cap) and the shortest (the new round-2 mirror check) leaves
only the two middle-length choices as candidates — once both caps are independently satisfied near
their low ends (6% and 0% here), a key landing at rank 2-3 in ~94% of cases is close to the
arithmetic default outcome of satisfying both caps at once, not an additional exploitable signal
layered on top. A test-taker who "always picks a middle-length choice" gets the same 50/50 benefit
from either single cap alone (eliminate two, guess between two); clustering at rank 2-3 doesn't
shrink the guess further below that. I would not add a third length-rank rule chasing this number
down — the existing longest-is-key and shortest-is-key caps already bound the real signal.

Task tf-g4: not yet
Overall: concerns
