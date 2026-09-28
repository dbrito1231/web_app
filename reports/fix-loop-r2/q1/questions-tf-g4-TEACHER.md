# Teacher round 2 — lesson-tf-g4 + 24 questions (content at db11570)

## (a) My own round-1 findings

- **TEACHER-Lg4-001 — Gone.** Claim-table row 82 (`4a`, `terraform_data`, `https://developer.hashicorp.com/terraform/language/resources/terraform-data`) is present in `lesson-tf-g4-impl.md`, and `cite-tf-g4-terraform-data` is now in the lesson's `citationIds`. Prose unchanged and still accurate.
- **TEACHER-Lg4-002 — Gone.** `bodyMarkdown` §4a now reads "— 'Meta-arguments are a class of arguments built into the Terraform configuration language that control how Terraform creates and manages' your infrastructure regardless of provider, as opposed to a provider-specific argument that differs by resource type —" immediately before the discriminator claim, backed by new row 83 / `cite-tf-g4-meta-arguments`.
- **`nonsensitive()` addition — Gone.** §4h's closing paragraph on `nonsensitive` is present, doc-quoted, and consistent with the surrounding `sensitive`/`ephemeral` material (re-read per RULES.md "After applying a fix" #2 — no new contradiction).

## (b) Second-role check on AWS's round-1 findings

- **AWS-Lg4-001 — Gone.** Claim-table row 27's Doc URL now points to `https://developer.hashicorp.com/terraform/language/meta-arguments/count`, matching where the "...integer index" wording actually lives. I independently re-fetched that page's text this turn: the sentence is verbatim there.
- **AWS-Lg4-002 — Gone.** Version floors are now stated in prose for all four gated features and match HashiCorp's own Requirements sections (independently re-fetched this turn): `precondition`/`postcondition` → 1.2.0 (`language/validate`), `check` → 1.5.0 (`language/validate`), `ephemeral` → 1.10 (`language/manage-sensitive-data`), write-only → 1.11 (`language/manage-sensitive-data`). Claim rows 75–78 back each one.

## (c)/(d) Question review — new findings

Ran the full chain fresh against the whole files (not diffs): `content_lint.py` PASS; `q1_batch_check.py tf-g4` PASS (longest-is-key 6%, shortest-is-key 0%, MC keys a:4/b:4/c:4/d:4, MR sets all 8 distinct); `distractor_type_audit.py tf-g4` PASS (max 12%, cap 15%); `stem_echo_check.py tf-g4` PASS (0 unwaived, 1 advisory bulk echo on `4a-mr`); `claim_prose_check.py tf-g4` PASS. None of the findings below are caught by any script — all found by reading every choice and rationale against the lesson and, where a version/behavior claim was involved, against HashiCorp's docs fetched fresh this turn.

**TEACHER-Qg4-001 (High) — the letter-shift bug is real and systemic, confirming LD-Qg4-001.** I hand-checked every affected file by matching rationale prose to actual choice text. In every case the rationale's lettered claims are off by one relative to the current choice order, and worst of all, several rationales explicitly call the *correct* answer "wrong" under its own reassigned letter:
- `4b-mr` (key b,d): rationale's "d is wrong" text ("takes a literal list... never an arbitrary computed expression") actually describes wrong-choice **c**'s content — but **d** is a correct answer and gets called wrong.
- `4d-mr` (key c,e): rationale's "e is wrong" text (list/tuple interchangeability) describes wrong-choice **d**'s content — but **e** is a correct answer and gets called wrong.
- `4f-mr` (key a,d): same pattern — "d is wrong" describes actual choice **c**'s content, while **d** is correct.
- Also affected: `4a-mr`, `4c-mr`, `4e-mr`, `4f-mc`, `4g-mr`, `4h-mc2`, `4h-mr`.

Fix — RULES.md already bans letter references outright ("No letter references... describes each wrong claim by its content"), so the fix is to purge letters entirely, not renumber them. Exact replacement rationales (content-matched to the current choice order):

- `q-tf-004-4a-mr`: "A data block records only what it read in state, not a stateful placeholder object managed the way a resource is. A data block never appears in plan output as an add, change, or destroy action, only as a read. And Terraform re-reads a data source on each ordinary run; there is no permanent lock after the first read."
- `q-tf-004-4b-mr`: "Adding a redundant `depends_on` to a pair that already has an attribute reference is discouraged, not harmless — it makes Terraform treat more of the dependency's future values as unknown than the attribute reference alone would. `depends_on` takes a literal list of resource or module addresses, never an arbitrary computed expression. And module blocks can declare `depends_on` just as resource blocks can."
- `q-tf-004-4c-mr`: "A parent module can only reach a child's output blocks, never its locals directly. A locals block computes its value from an expression inside the module; it does not accept an externally supplied value the way a variable does. And there is no automatic mirroring between a local and an output of the same name — an output only exposes what its own value argument computes."
- `q-tf-004-4d-mr`: "Automatic type conversion happens for most arguments but never for the equality operator, where a number and the string of that number are not treated as equal. Map keys must be strings regardless of how consistent the key types otherwise look — a number or boolean key isn't valid. And Terraform's own documentation treats list and tuple as interchangeable terms whenever the distinction doesn't matter for the point being made."
- `q-tf-004-4e-mr`: "`lookup` accepts an optional default value and returns that instead of erroring when the key is missing. A `for` expression only ever produces a value, not a configuration block; generating repeated nested blocks is what `dynamic` blocks are for. And `merge` accepts maps with completely different keys and combines them all — it doesn't require the inputs to already match."
- `q-tf-004-4f-mc`: "Claiming B depends on A reverses the direction entirely: `depends_on = [B]` inside A means A depends on B, not the other way around. Claiming this also delays anything that depends on A overreaches — nothing about A's own `depends_on` argument reaches out to control the timing of a third resource that depends on A. And `depends_on` completes all operations, including reads, on the named dependency before touching the dependent resource; it isn't split into separate read and write timing."
- `q-tf-004-4f-mr`: "Claiming `prevent_destroy` blocks a destroy under every circumstance, including when the resource's own block is deleted, directly contradicts its documented gap: removing the resource's own configuration block bypasses it. `lifecycle` arguments only accept literal values, not a variable-derived expression, unlike `count` — so `create_before_destroy` cannot be set to a computed expression. And a resource has a single `lifecycle` block, not several merged together."
- `q-tf-004-4g-mr`: "Claiming postconditions run before preconditions reverses the real order: Terraform evaluates preconditions after generating a plan but before creating the object, and postconditions only afterward. Claiming a precondition can reference `self` is wrong, since `self` refers to an object that doesn't exist yet at precondition time — `self` is a postcondition tool. And `check` blocks run at the end of a plan or apply operation, not before a plan exists."
- `q-tf-004-4h-mc2`: "Claiming write-only arguments need 1.5, the same floor as `check` blocks, names a real version floor but attaches it to the wrong feature — 1.5 is `check` blocks' floor, not write-only arguments'. Claiming there is no minimum version at all is wrong, since a minimum version (1.11) does exist. And `sensitive` and write-only are unrelated mechanisms; marking a value `sensitive` doesn't unlock or enable write-only argument support."
- `q-tf-004-4h-mr`: see TEACHER-Qg4-003 below (needs a content fix too, not just relettering).

**TEACHER-Qg4-002 (High, doc-verified content error) — `q-tf-004-4d-mc` choice d is not clearly wrong; the rationale's refutation is false.** I fetched `developer.hashicorp.com/terraform/language/functions/sort` and `.../language/expressions/type-constraints` today. `sort` takes `list(string)`. Type-constraints page, "Conversion of Complex Types": *"When a set is converted to a list or tuple, the elements will be in an arbitrary order. If the set's elements were strings, they will be in lexicographical order."* Terraform auto-converts a `set(string)` argument to `list(string)` when a function parameter demands it, and for a string set that conversion is already alphabetical — so `sort(var.names)[1]` does work, making choice d ("Sort the set alphabetically first; it becomes indexable") a real, working technique, not a caricature. The rationale's closing line — "a set is still not indexable, sorted or not" — is directly contradicted by this doc text. This is either a second correct answer or a distractor asserting a false reason; either way it fails teach-before-test twice over (the claim is wrong, and `sort` isn't taught in the lesson at all).
Fix: replace choice d with `"Reference the set by string key, such as var.names["second"]"` (wrong for a taught reason: the lesson's own line says a set is "a collection of unique values that do not have any secondary identifiers," so there is no key to reference at all — unlike map/object, which is "a group of values identified by named labels"). Replace the rationale's last sentence with: "A set has no named keys the way a map does, so there is nothing to reference by key — 'named labels' is what distinguishes a map/object, not a set."

**TEACHER-Qg4-003 (High, doc-verified content error) — `q-tf-004-4h-mr` choice c is true, not false.** Fetched `developer.hashicorp.com/terraform/language/functions/nonsensitive` today: *"nonsensitive will make no changes to values that aren't marked as sensitive, even though such a call may be redundant and potentially confusing."* The rationale (once un-shifted, see TEACHER-Qg4-001) claims this is "documented as an error" — the opposite of the source. This is a real content error, not merely untaught, and on the objective RULES.md itself flags as carrying real-world stakes.
Fix — choice c text → `"Calling nonsensitive() on a value that was never marked sensitive raises an error and halts the run."` (now genuinely false and directly checkable against the doc line above). Full corrected rationale: "Claiming `nonsensitive()` also removes a value from the state file is the dangerous misconception this objective exists to prevent — it only lifts the CLI/UI redaction and does nothing to keep a value out of state, unlike `ephemeral`. Claiming that calling it on an already non-sensitive value raises an error is wrong; the documentation states it makes no changes to values that aren't already marked sensitive, so the call is a harmless, if redundant, no-op. And Vault is an external secrets engine the provider talks to, not a Terraform-language keyword alongside `sensitive`, `ephemeral`, or write-only arguments."

**TEACHER-Qg4-004 (High) — `q-tf-004-4f-mc2` has two defective distractors, confirming LD-Qg4-003.** Fetched `developer.hashicorp.com/terraform/language/meta-arguments/lifecycle` today: *"Instead of a list of items, you can use the `all` keyword..."* — the real special form is the bare keyword `ignore_changes = all`, not `[all]`; the choice as written is invalid syntax, failing "every distractor is a real option." Separately, choice b's parenthetical ("creates two independent instances instead of sequencing one resource's own replacement") refutes itself before the reader even reasons about it, and `count` is not a `lifecycle` argument at all even though the stem asks "Which lifecycle argument fits?" — a category tell that lets a reader eliminate it without engaging the content.
Fix: choice c → `"ignore_changes = all"`. Choice b → `"replace_triggered_by = [aws_db_instance.B]"` (real, same lifecycle page, wrong because it forces a *replacement* on an unrelated change, not create-before-destroy sequencing). Rationale addition: "`replace_triggered_by` forces a replacement when a referenced value changes; it doesn't control which order create and destroy happen in. `ignore_changes = all` stops Terraform from planning updates to any attribute; it has nothing to do with replacement ordering."

**TEACHER-Qg4-005 (High) — `q-tf-004-4e-mc2` key is self-justifying, confirming LD-Qg4-004.** Key text is `"can, boolean-only"` — the only choice carrying an appended explanatory tag, and that tag echoes the stem's "plain true/false result." RULES.md: "No key that restates the stem's requirement or justifies itself." Fix: change key text to bare `` `can` `` (matching the other three choices' bare-name format); the boolean-vs-value distinction is already carried in the rationale.

**TEACHER-Qg4-006 (Medium, agree with LD-Qg4-006) — `q-tf-004-4c-mc2` choice c needs `TF_VAR_` knowledge the lesson never gives.** Case-insensitive, backtick-tolerant regex over `bodyMarkdown` confirms zero occurrences of `TF_VAR`. A student who only read this lesson cannot eliminate this distractor for a stated reason. Fix (teach it): add to §4c, doc-verified from `language/values/variables` ("Environment Variables"): *"the value that is available in the environment variable named `TF_VAR_` + variable name"* — one sentence: "Terraform also reads a variable's value from an identically-named environment variable prefixed `TF_VAR_`, for example `TF_VAR_subnet_id`."

**TEACHER-Qg4-007 (Medium, agree with LD-Qg4-007) — `q-tf-004-4b-mc2` choices a and b are caricature reasoning, not real misconceptions.** "based on the instance profile depending on the instance's IP address" and "treating the reference as pointing to whichever object is destroyed first" are not beliefs any practitioner plausibly holds; only choice c (thinking `depends_on` is also required) is a real misconception. Fix — replace both with lesson-grounded, plausible confusions: choice a → `"Terraform infers no ordering at all, because iam_instance_profile is a plain string argument, not a resource reference"` (wrong because an attribute reference creates the implicit dependency regardless of the argument's own declared type — taught in §4b). Choice b → `"Terraform infers that the instance profile is created before the instance, but only because both resources share the same provider meta-argument"` (wrong because the ordering comes from the attribute reference itself, not from sharing a meta-argument — meta-arguments are defined in §4a as not being the discriminator).

**TEACHER-Qg4-008 (Low, agree with LD-Qg4-008) — two absolutist/meta-trivia distractors.** `4d-mr`'s "can never be used interchangeably in Terraform's own documentation" tests knowledge of documentation wording, not technical behavior. `4a-mr`'s "locked and can never be refreshed" is a plausible-enough misconception (unlike the "run it on one instance" style strawman the rules ban) and I would not block on it alone. Fix for the `4d-mr` one: replace with a technical claim — `"A list and a tuple are two entirely different types with mutually exclusive operations, so a for expression producing one can never be assigned where the other is expected"` (wrong because the lesson teaches Terraform converts between them).

**TEACHER-Qg4-009 (Medium-high, new) — duplicate facts on objective 4a.** `q-tf-004-4a-mr`'s two correct answers are the identical facts already keyed elsewhere: choice a (data blocks are read-only) duplicates `4a-mc`'s key; choice c (deferral to apply) duplicates `4a-mc2`'s entire question. Round 1's own three-facts verdict for 4a promised a third distinct fact — the `terraform_data` exception — but that fact is only ever used as a wrong choice in `4a-mc`, never as a question's own tested content. Net effect: objective 4a has two distinctly-*keyed* facts across three question slots, not three.
Fix: retarget `4a-mr`'s correct pair onto material not already keyed elsewhere, using content already present in its own wrong choices or the lesson's `terraform_data` claim, e.g. correct set = "A data block can only perform read operations; it never creates or modifies a resource" (keep) + "A `terraform_data` resource is a `resource` block that stores a value under the managed-resource lifecycle without creating actual infrastructure" (new, doc-backed by the lesson's own row 82/`cite-tf-g4-terraform-data`); move the apply-deferral statement to a distractor slot since `4a-mc2` already owns that fact as its key.

## (d) Number/version verification

Checked every version literal appearing in a key: `4g-mc` stem "Terraform 1.2 or later" + key `postcondition` — matches lesson/doc floor 1.2.0 for pre/postconditions. `4g-mc2` key `check` block "1.5 onward" — matches doc floor 1.5.0. `4h-mc2` stem "Terraform 1.9," key "write-only arguments need Terraform 1.11 or later... doesn't meet that floor" — matches doc floor 1.11, and 1.9 < 1.11 is arithmetically correct. All version numbers used in keys are correct against both the lesson and the HashiCorp source pages I re-fetched this turn.

## (e) Verdict on Lead Dev's pre-check findings

- **LD-Qg4-001 — Agree, confirmed by direct text comparison (see TEACHER-Qg4-001).** High severity is right; several mislabeled rationales call a *correct* answer wrong, which is worse than a cosmetic letter slip.
- **LD-Qg4-002 — Agree, and I upgraded it with doc confirmation (TEACHER-Qg4-002).** `sort()` on a string set genuinely works via Terraform's documented set→list conversion rule; the rationale's refutation is false.
- **LD-Qg4-003 — Agree on both sub-points (TEACHER-Qg4-004).** `ignore_changes = [all]` is invalid syntax per the lifecycle page; the `count` parenthetical is self-refuting and off-category for a "which lifecycle argument" stem.
- **LD-Qg4-004 — Agree (TEACHER-Qg4-005).** Self-justifying key, direct RULES.md violation.
- **LD-Qg4-005 — Agree, and I upgraded severity (TEACHER-Qg4-003).** I fetched the `nonsensitive` page myself: the "documented as an error" claim is false — the doc says the opposite (a silent no-op). This is a content error, not just an untaught-fact risk, and it sits squarely in the 4h sensitive-data stakes zone the brief calls out. Choice d (Vault-as-keyword) is indeed a caricature nobody would believe; low-stakes since it's clearly absurd rather than misleading.
- **LD-Qg4-006 — Agree (TEACHER-Qg4-006).** Confirmed zero `TF_VAR` hits via regex.
- **LD-Qg4-007 — Agree (TEACHER-Qg4-007).**
- **LD-Qg4-008 — Agree, low severity, as LD rated it (TEACHER-Qg4-008).**
- **LD-Lg4-009 — Agree.** §4g opens "Three condition mechanisms check different things at different times" then later calls `check` "the fourth mechanism, the newest of the four" — the opening framing sentence undercounts by one. Fix: change "Three condition mechanisms" to "Four condition mechanisms."
- **LD-Lg4-010 — Agree.** §4h's "There are three ways to get one [an ephemeral value]" lists a write-only argument as a *source*, but the very next paragraph correctly describes a write-only argument as the *channel that receives* an already-ephemeral value, not something that produces one. Fix: drop the write-only argument from the "three ways to get one" list (it becomes two ways: the `ephemeral` argument, or a dedicated `ephemeral` resource block), and adjust the count.
- **LD-Lg4-011 — Agree, low.** "in the writer's own words" is confusing phrasing for "in the documentation's own words." Fix: reword to "in HashiCorp's own words."
- **LD-Lg4-012 — Agree, low.** Doubled "but" in §4a's timing sentence is a genuine copy-edit glitch. Fix: "Terraform normally reads a data source during planning — 'Terraform attempts to query data sources during the planning phase,' but 'it may defer reading until the apply phase'" (drop the first "but").
- **Key-length observation (94% of MC keys at rank 2–3 of 4) — partly a real tell, not pure over-fitting.** With only 4 choices, simultaneously satisfying "not longest" (≤35%) and "not shortest" (0% observed, no explicit cap) mechanically collapses most keys into the two middle ranks — that's an artifact of enforcing both extremes-avoidance rules on a 4-item set, not necessarily deliberate gaming. But the practical effect for a test-taker is real regardless of cause: "never guess the longest or shortest" is an exploitable shortcut once a student notices it across enough questions, which is exactly the failure mode the longest-is-key cap was meant to prevent from the other direction. I'd flag this to whoever owns cross-task quality metrics (it's bigger than tf-g4) rather than block this task on it, since both individual caps pass and no per-task rule is violated.

## Verdict

Nine new Teacher findings, two of them (TEACHER-Qg4-002, TEACHER-Qg4-003) confirmed *content errors* against fresh doc fetches — one makes a real, working Terraform technique into a wrongly-refuted distractor, the other makes the 4h sensitive-data question assert something the docs directly contradict. Combined with the systemic rationale letter-shift (confirmed across 10 files) and a duplicate-fact gap on objective 4a, this task is not ready to close.

Task tf-g4: not yet
Overall: concerns

---

# Teacher round 2b — tf-g4 confirmation (5a470ae)

Saved by Lead Dev from the Teacher's reply; condensed to the verdicts (full reasoning in the session transcript).

Chain re-run fresh at 5a470ae: all five PASS (longest-is-key 6%, shortest-is-key 12%, max distractor type 12%, 0 echoes). Re-fetched `language/data-sources`, `cli/config/environment-variables`, `language/meta-arguments/lifecycle`.

## (a) Own findings
TEACHER-Qg4-001 … 009: **all Gone.** 003 was fixed with the AWS type-conversion distractor rather than the Teacher's "raises an error" flip. The Teacher calls it a better fix, since it has no version dependency. On 008, the replacement introduced TEACHER-Qg4-010.

## (b) Second-role checks
AWS-Qg4-001 … 008: **all Gone** (verified independently against files). LD-Qg4-001 … 008: **all Gone**. LD-Lg4-009 … 012: **all Gone.**

## (c) Lead Dev concerns
1. `4a-mr` choice e (terraform_data needs a companion resource): real misconception (tutorials pair it with a resource). Its refutation is taught by row 82's sentence ("when there is no other logical managed resource…"). No fix needed.
2. **TEACHER-Qg4-010 (Medium-High, new):** `4d-mr` choice d (`for_each` accepts a plain list) answers neither stated need, which violates the RULES MR join rule and can be eliminated on relevance alone. It must be replaced by a choice that plausibly answers one of the two needs.
3. **TEACHER-Qg4-011 (Low-Medium, new):** in 4f, "`replace_triggered_by` does the opposite of sequencing a replacement" is overstated. Reword it to "answers a different question than sequencing a replacement". The `4f-mc2` rationale is already precise.
4. "By default, Terraform refreshes prior to creating a plan": verbatim on `language/data-sources` in the data-source refresh context, so the claim is supported and not overstated.
5. 4h: no residual dangerous misconception.

## (d) Versions: unchanged, all correct.
## (e) Key-length: still partly a real cross-task tell in the Teacher's view; not blocking; the user decides.

Task tf-g4: not yet
Overall: concerns

---

# Teacher round 2c — tf-g4 (157e12a)

Saved by the Lead Dev from the Teacher's reply (condensed).

- **TEACHER-Qg4-010 — Gone.** `4d-mr` choice d (`null == ""` evaluates to `true`) addresses the stem's `==` need, and all five choices now map onto one of the two stated needs.
- **TEACHER-Qg4-011 — Gone.** 4f now describes `replace_triggered_by` as deciding whether a replacement happens, which is a separate question from ordering.
- **Second-role check on AWS-Qg4-010: agree, and Gone.** The Teacher's round-2b verdict that this was "taught" was wrong: the four terms had 0 hits in the prose. The new 4a sentence teaches it, using the quote already verified against `resources/terraform-data`.
- **New `4d-mr` choice d:** it is a real thing a learner might try. It is wrong for a reason 4d states verbatim ("`null` is not the same as an empty string or a zero"). The rationale covers both keys and all three distractors by content.
- **Chain:** the Teacher ran four of the scripts (lint, batch check, stem echo, claim prose); all PASS.

Task tf-g4: close
Overall: approve
