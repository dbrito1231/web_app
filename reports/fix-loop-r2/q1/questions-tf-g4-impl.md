# Questions tf-g4 (Terraform configuration) — implementation report

## What was written

24 questions, 3 per objective (`-mc`, `-mc2`, `-mr`) across tf.004.4a–4h, all in `content/questions/`, overwriting the pre-existing placeholder files. Each tests a distinct fact already taught in `lesson-tf-g4` (including the round-1 fixes: version floors for `precondition`/`postcondition` (1.2+), `check` (1.5+), `ephemeral` (1.10+), write-only arguments (1.11+), and `nonsensitive()`):

- **4a**: data-vs-resource by action (read-only vs. can create/change/destroy); the planning/apply timing deferral; two true/false statements about `data` block behavior (never appears as add/change/destroy, no permanent read-lock).
- **4b**: `<TYPE>.<LABEL>` vs `data.<TYPE>.<LABEL>.<ATTRIBUTE>` syntax; the implicit-reference direction (`aws_iam_instance_profile` created first, not the instance) with a reversed-direction distractor; when `depends_on` is actually needed vs. redundant.
- **4c**: `output` vs `variable` vs `locals` by who can read/set them; the no-default prompt-before-plan behavior; locals' module-only visibility and `local.` vs `locals` naming.
- **4d**: converting a `set` to a `list` before indexing; what `null` does and does not do (not the same as `""` or `0`); map keys must be strings, and the `==` operator's own exemption from automatic type conversion.
- **4e**: `for_each` vs `count` for genuinely distinct vs. nearly identical instances; `can` (boolean, for `validation`) vs `try` (fallback value); `for` expression filtering and `merge`'s later-argument-wins precedence.
- **4f**: `depends_on` direction (`depends_on = [B]` inside A means A depends on B, explicitly stated as implying nothing about A's own dependents) with a reversed-direction distractor; `create_before_destroy` vs `prevent_destroy` vs `ignore_changes`; the `prevent_destroy` config-removal gap and the lifecycle-literal-only rule.
- **4g**: `postcondition`+`self` vs `precondition` vs variable `validation` vs `check`, each paired with its actual version floor (1.2 for pre/postcondition, 1.5 for `check`); the real execution order (preconditions before creation, postconditions after, checks last).
- **4h**: what `sensitive` does and does not protect (still in state, still exposed via `-json`/`-raw`, never implies encryption or exclusion from state); the 1.11 write-only version floor; `nonsensitive()`'s real risk (exposes a value, does not touch state) paired with Vault's short-lived-credential value proposition.

## Fix pass (five defects caught by the automated chain, all now clean)

The first draft placed every MC key on `a` and every MR key pair on `a,b`, and had a handful of other problems. Rather than list them as separate "rounds," here is what changed and why, since RULES.md's "After applying a fix" section asks for the state of the whole file, not a diff:

1. **Key-position shuffle.** Reordered choices (keeping distractor content and meaning identical) so the 16 MC keys land 4/4/4/4 on a/b/c/d, and the 8 MR key-pairs use 8 distinct letter combinations spread across a–e.
2. **Letter reference in rationale (`q-tf-004-4b-mc2`).** The original rationale said "Option b invents...Option c reverses...Option d is wrong." Rewritten to describe each wrong claim by its content instead.
3. **Banned tell-word "must" in two choices.** `q-tf-004-4a-mr` choice and `q-tf-004-4d-mr`'s key both used "must"; reworded without changing the claim's truth.
4. **`depends_on` distractor-type over cap (4 of 24, cap 3).** Replaced `q-tf-004-4f-mc2`'s `depends_on = [self]` distractor with `count = 2`, a real, taught, and clearly wrong-for-the-scenario option, dropping the count to 3.
5. **`longest-is-key` at 38% (6 of 16).** Six MC keys happened to be the longest choice. Fixed by lengthening a distractor (or, in one case, shortening the key) in `q-tf-004-4b-mc`, `q-tf-004-4d-mc2`, `q-tf-004-4f-mc`, `q-tf-004-4f-mc2`, `q-tf-004-4h-mc`, and `q-tf-004-4h-mc2` — none of the edits changed which claim is true, only relative length.
6. **Stem/key giveaway (`q-tf-004-4h-mc`).** "sensitive" appeared in the stem and only in the key. Added the word to one distractor ("...derived from the sensitive value...") so it's no longer exclusive to the key — the underlying claim is unchanged.

After every fix, the full chain was re-run against the whole file (not just the touched lines) per RULES.md; results below are from that final run.

## Directionality re-check (4b, 4f)

Per the round-1 brief's explicit warning about direction: `q-tf-004-4b-mc2`'s key states the instance profile is created first "from the instance's argument reading the profile's exported attribute," with a distractor that reverses this ("the instance is created before the instance profile"), and `q-tf-004-4f-mc`'s key states "A depends on B, so B is created first, and nothing is implied about anything that might depend on A," with a distractor asserting the opposite. Both match the lesson's own corrected direction (upstream dependency created first; nothing implied about downstream dependents), checked against `language/meta-arguments/depends_on` and `language/block/resource` again this turn.

## `sensitive` stakes re-check (4h)

`q-tf-004-4h-mc`'s three wrong choices each assert a specific incorrect protection (excluded from state like `ephemeral`; automatically encrypted at rest; stored only as a one-way hash) and the rationale states plainly why each is false and what `sensitive` actually does (CLI/UI redaction only, real value still in state and plan, still exposed via `-json`/`-raw`). No choice in this question, or in `q-tf-004-4h-mr`'s `nonsensitive()`/Vault pair, implies `sensitive` encrypts or removes a value from state without that being the thing being marked false.

## Distractor-type table (final run, `distractor_type_audit.py tf-g4`)

| Type | Count | % of 24 | Questions |
|---|---|---|---|
| depends_on | 3 | 12% | q-tf-004-4b-mc2, q-tf-004-4b-mr, q-tf-004-4e-mc |
| precondition | 3 | 12% | q-tf-004-4g-mc, q-tf-004-4g-mc2, q-tf-004-4g-mr |
| prevent_destroy | 2 | 8% | q-tf-004-4f-mc2, q-tf-004-4f-mr |
| validation | 2 | 8% | q-tf-004-4g-mc, q-tf-004-4g-mc2 |
| ephemeral | 2 | 8% | q-tf-004-4h-mc, q-tf-004-4h-mr |
| write-only | 2 | 8% | q-tf-004-4h-mc2, q-tf-004-4h-mr |
| terraform_data | 1 | 4% | q-tf-004-4a-mc |
| tomap | 1 | 4% | q-tf-004-4d-mc |
| ignore_changes | 1 | 4% | q-tf-004-4f-mc2 |
| create_before_destroy | 1 | 4% | q-tf-004-4f-mr |
| postcondition | 1 | 4% | q-tf-004-4g-mr |
| nonsensitive | 1 | 4% | q-tf-004-4h-mr |

All at or under the 15%-of-24 (3-question) cap. New TERMS added to `scripts/distractor_type_audit.py`: `for_each`, `depends_on`, `create_before_destroy`, `prevent_destroy`, `ignore_changes`, `precondition`, `postcondition`, `validation`, `check block`, `terraform_data`, `nonsensitive`, `ephemeral`, `write-only`, `tolist`, `tomap`, `toset`. Deliberately left out as core subject vocabulary (same treatment as "resource"/"data"/bare command names in earlier tasks): `resource`, `data`, `variable`, `local`, `output`, `count`, `for` expression, `try`, `can`, `lookup`, `merge`, `sensitive`.

## Final results (all five scripts, whole file)

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g4`: PASS — single-asterisk spans 0, tables/numbered lines 0, citations unresolved [], drillIds match (24/24), exam tips 8/8, duplicate 6-word openings [], longest-is-key 0/16 = 0%, MC key positions {a:4, b:4, c:4, d:4}, MR key slots {a:3, b:3, c:4, d:3, e:3}, MR key sets all 8 distinct (12% each, no repeats).
- `distractor_type_audit.py tf-g4`: PASS (table above; highest is 12%, cap is 15%).
- `stem_echo_check.py tf-g4`: PASS — no stem/key giveaway, no bulk echo, 0 waivers needed.
- `claim_prose_check.py tf-g4`: PASS — no questions-side check (lesson-only script), re-run to confirm the lesson side is still clean after the questions pass touched no lesson content; every claim-table number still appears in lesson prose, no over-length quotes.

## Round 2 fixes (Lead Dev pre-check, commit 6577724)

1. **Shortest-is-key (new mirror check), 6 of 16 MC.** `4a-mc`, `4a-mc2`, `4c-mc2`, `4d-mc` were fixed by tightening one over-verbose distractor down to or below the key's length (no meaning changed). `4e-mc2` (`try`/`can`/`lookup`/`merge`, all 5-8 chars) and `4g-mc2` (two choices tied at 52 chars) had no verbose distractor to tighten, so the key gained a short, genuinely load-bearing clause instead of filler: `4e-mc2`'s key now names the real can-vs-try distinction ("boolean-only" — trimmed further below to kill a new echo, see next), and `4g-mc2`'s key gained "only" (it's the one correct version floor among two check-block options at the same wrong length). Final: longest-is-key 1/16 (6%), shortest-is-key 0/16 (0%), both under the 35% cap. No key moved position from this pass.
2. **Four recall-with-a-name MR stems rewritten**: `4a-mr`, `4c-mr`, `4d-mr`, `4e-mr` now open on a concrete situation (a teammate's theories about a stalled data read; reusing a child module's local from the parent; a literal `tags = { 3 = "prod" }` argument and an `==` comparison; refactoring a module's `for`-expression-plus-`merge` logic) before asking which two statements hold, matching `4b-mr`/`4f-mr`'s pattern. Facts tested and keys are unchanged; only the stems moved.
3. **New stem/key giveaways from both of the above**, caught by `stem_echo_check.py`: the new scenario details introduced "apply", "defines", "string", and "filters" as stem words that had landed in exactly one choice, and the `4e-mc2` fix from #1 did the same with "value" and then "false". Each was resolved by either echoing the shared word into a true distractor (`4a-mr`'s plan-output statement now also says "once Terraform reaches the apply step") or removing the incidental word from the stem/key wording without changing the claim (`4c-mr`, `4d-mr`, `4e-mr`, `4e-mc2`).

Final chain, whole files: `content_lint.py` PASS; `q1_batch_check.py tf-g4` PASS (longest-is-key 6%, shortest-is-key 0%, MC keys a:4/b:4/c:4/d:4, MR sets all 8 distinct); `distractor_type_audit.py tf-g4` PASS (max 12%, cap 15%); `stem_echo_check.py tf-g4` PASS (0 unwaived giveaways, 1 advisory bulk-echo on `4a-mr` left as-is per the script's own guidance not to treat it as a defect); `claim_prose_check.py tf-g4` PASS.

## Round 3 (round-2 review) fix pass

Applied every item under `## Question edits` in `questions-tf-g4-fixspec.md` (Q1-Q10), following
the Lead Dev's decision wherever the two round-2 reviewers (Teacher, AWS) differed. All doc pages
were re-fetched this turn with `curl -sL` through `fixg4_strip.py`, never WebFetch.

- **Q1 (letter-purge, 10 files): done.** Rewrote every rationale in `4a-mr 4b-mr 4c-mr 4d-mr
  4e-mr 4f-mc 4f-mr 4g-mr 4h-mc2 4h-mr` to name each wrong choice by content, with no single-letter
  references anywhere. For the six files untouched by Q2-Q9 (`4b-mr`, `4c-mr`, `4e-mr`, `4f-mc`,
  `4f-mr`, `4g-mr`), the Teacher's round-2 draft text was used verbatim since it was already
  content-matched to the current choice order. For `4h-mc2` the Teacher's draft was also used
  as-is. For `4a-mr`, `4d-mr`, and `4h-mr`, the rationale was written fresh against the final,
  post-Q6/Q7/Q8/Q9 choice text, per the fix spec's explicit instruction not to reuse a draft written
  against choices that later changed.
- **Q2 (`4d-mc` choice d): done, Teacher's version used.** Replaced "Sort the set alphabetically
  first; it becomes indexable" with `` Reference the set element by a string key, such as
  `var.names["second"]` ``. Rewrote the rationale's closing sentence: "A set has no named keys the
  way a map does, so there is nothing to reference by string key -- 'named labels' is what
  distinguishes a map/object, not a set." This is real practice pattern people try (treating a set
  like a map with named entries) and it is wrong for a reason the lesson states verbatim: a set "do
  not have any secondary identifiers," while map/object is "a group of values identified by named
  labels." The AWS `values()` alternative was not used, per the fix spec, because `values()` is
  untaught.
- **Q3 (`4e-mc2` key): done.** Changed `` `can`, boolean-only `` to bare `` `can` ``. All four
  choices are now bare function names with no annotation. Left the `try` distractor unpadded per
  the fix spec's explicit instruction not to compensate by lengthening it. Consequence (reported,
  not padded around): `q1_batch_check.py` now shows shortest-is-key at 12% (2/16: `4e-mc2`'s `can`
  and one other pre-existing case), still under the 35% cap, so no further action was needed.
- **Q4 (`4b-mc2` choices a, b): done, both reviewers' shared proposal + the directionality
  variant.** Choice a -> "Terraform infers no ordering between the two resources, because a `name`
  value is plain data with no dependency implication" (real belief: is a real practice, wrong
  because 4b teaches that *any* attribute reference, regardless of the argument's own name, creates
  the implicit dependency). Choice b -> "Terraform infers that the instance is created before the
  instance profile, because the resource holding the reference is processed first" (real belief: a
  plausible but backwards mental model of "whoever reads it goes first"; wrong because 4b/4f teach
  that the *referenced* resource is created first, not the resource holding the reference). Kept
  choice c (redundant `depends_on` belief) and the key (d) unchanged. Rewrote the rationale to
  explain all four by content, no letters.
- **Q5 (`4f-mc2`, all four choices rebuilt): done.** Final choices: `` `prevent_destroy = true` ``
  (kept), `` `replace_triggered_by = [aws_lb_target_group.old]` `` (new, replacing the invalid-syntax
  `ignore_changes = [all]`), `` `ignore_changes = all` `` (new, correct bare-keyword syntax,
  replacing the self-answering `count = 2 (...)` choice), `` `create_before_destroy = true` `` (key,
  kept). All four are now genuine `lifecycle` arguments in the same category as the stem asks
  about. `replace_triggered_by` is real (verified against `meta-arguments/lifecycle` this turn,
  same quote used for lesson L4) and wrong here because it forces a replacement on an unrelated
  trigger rather than sequencing create-before-destroy for this resource's own replacement, a
  reason L4 now teaches. `ignore_changes = all` is real and wrong here because it stops Terraform
  from planning updates at all; it has nothing to do with replacement ordering, also newly taught by
  L4. `citationIds` updated to add `cite-tf-g4-lifecycle` alongside the existing `cite-tf-g4-resource`.
- **Q6 (`4h-mr` choice c): done, AWS's replacement used.** Replaced "Calling `nonsensitive()` on a
  value that was never marked sensitive quietly returns that same value with no warning" (which is
  actually *true* under the current `functions/nonsensitive` page, re-verified this turn: "nonsensitive
  will make no changes to values that aren't marked as sensitive, even though such a call may be
  redundant and potentially confusing") with "`nonsensitive()` converts the value to a different
  type, the same way `tostring()` or `tonumber()` would." This is a real category of function
  (`tostring`/`tonumber` exist and do convert types) misapplied to `nonsensitive`, wrong for a
  reason the lesson already states: `nonsensitive` "only lifts the CLI/UI redaction... it does not
  touch state, does not make a value ephemeral" -- i.e., it changes a marking, not a type. Per the
  fix spec, no error-on-unmarked-value claim was added to the lesson.
- **Q7 (`4h-mr` choice d): done, new real misconception, verified false this turn.** Replaced the
  "Vault-issued credentials are stored directly as Terraform language keywords" caricature with
  "Using the Vault provider's data source by itself keeps the issued credentials out of state, with
  no further configuration needed." Verified false two ways this turn: (1) the lesson's own Vault
  paragraph states Vault-issued credentials "are typically consumed as ephemeral or write-only
  values in the configuration that uses them," i.e. Vault alone is not one of those state-excluding
  mechanisms; (2) HashiCorp's own Vault/Terraform tutorial (`tutorials/secrets/secrets-vault`,
  re-fetched this turn) retrieves Vault-issued AWS credentials through an ordinary `data` block
  (`vault_aws_access_credentials.creds`), not an ephemeral- or write-only-flagged one. This is a
  real, plausible misconception (conflating "short-lived" with "excluded from state") and is not the
  banned negation of the `sensitive`-credentials key (choice e), since it makes a claim about the
  Vault provider's own default behavior, not about static credentials' lifetime.
- **Q8 (`4a-mr`, stem + choices + keys rebuilt): done.** The old keys duplicated `4a-mc`'s
  read-only fact and `4a-mc2`'s deferral fact. Rewrote the stem to drop the "unresolved until
  apply" framing (which pointed at nothing once the deferral key was removed) and now introduces
  both `data` blocks and `terraform_data` as the scenario's subject. New key pair: "A
  `terraform_data` resource is a `resource` block that stores a value under the managed-resource
  lifecycle without creating any real infrastructure" (lesson row 82, `terraform_data`'s own
  paragraph in 4a) and "Terraform re-reads a data source's value on every ordinary run, rather than
  caching it permanently after the first read" (lesson row 84, added this round by L2). Kept the
  two existing distractors ("placeholder object in state," "appears as add/change/destroy") per the
  fix spec, and replaced the old "locked and can never be refreshed" distractor (now the direct
  negation of the new key, which would have been a giveaway) with a new one: "A `terraform_data`
  resource can only be declared alongside another managed resource of the same type; it cannot
  stand on its own in a configuration" -- wrong for a lesson-taught reason (`terraform_data` exists
  "for triggering provisioners when there is no other logical managed resource in which to place
  them"). `selectCount` stays 2. `citationIds` updated to `cite-tf-g4-data-sources` +
  `cite-tf-g4-terraform-data`.
- **Q9 (`4d-mr` choice d): done, replaced with a taught, non-duplicating misconception.**
  Case-insensitive regex over `bodyMarkdown` confirmed the lesson does not teach list<->tuple
  conversion as a distinct operation (only that the two terms are used interchangeably in
  documentation, which choice e already tests and which was not touched), so that route was not
  used. Replaced the documentation-wording choice with "`for_each` accepts a plain `list` value
  directly, the same way it accepts a `map` or a `set`, without needing any conversion" -- real
  (a common count/for_each confusion) and wrong for a reason 4d's own prose states: "A `for_each`
  argument (4e) needs a map or a set precisely because those are the two types with no meaningful
  'position'..." -- a plain list needs conversion first. This does not duplicate `4d-mc`'s key
  (converting a *set* to a list before indexing). `citationIds` gained `cite-tf-g4-for-each`.
- **Q10 (`4c-mc2`): no choice change, as directed.** The existing rationale already correctly
  states "Terraform only reads environment variables carrying the TF_VAR_ prefix," which now points
  at L3's new lesson sentence; left unedited since it needed no rewording.

## Round 3 checks (whole files, not diffs)

- `content_lint.py`: PASS (`questions 429 aws 310 tf 119`, `lessons 23`).
- `q1_batch_check.py tf-g4`: PASS -- `task tf-g4: 24 questions`; longest-is-key 1/16 (6%);
  shortest-is-key 2/16 (12%, both under the 35% cap -- see Q3 above for why this moved from 0%);
  MC key positions a:4/b:4/c:4/d:4; MR key slots a:3/b:3/c:4/d:3/e:3, all 8 key-letter-sets distinct;
  duplicate 6-word openings: none; citations unresolved: none.
- `distractor_type_audit.py tf-g4`: PASS -- highest type is `depends_on`/`precondition` at 12% each
  (cap 15%); `terraform_data` rose from 1 to 2 questions (8%) because of Q8's rewrite, still under
  cap; `for_each` appears for the first time (1 question, 4%) because of Q9.
- `stem_echo_check.py tf-g4`: PASS -- `0 unwaived giveaway, 0 waived, 0 bulk echo, of 24 questions`.
  The prior advisory bulk-echo flag on `4a-mr` is gone because Q8 rewrote that stem entirely.
- `claim_prose_check.py tf-g4`: PASS -- `9 distinct numbers in lesson prose`, every claim-table
  number still appears in lesson prose (this script checks the lesson, not the questions; re-run to
  confirm the round-2 lesson edits didn't break it).
- `key_text_diff.py tf-g4 db11570`: **reports 2 expected mismatches, not a defect.** `4a-mr`'s two
  correct-answer texts differ from the db11570 baseline because Q8 deliberately retargeted both keys
  onto new facts (the fix spec's explicit instruction, not an accidental reorder) -- the script
  cannot distinguish an approved content retarget from the reorder bug it exists to catch. `4e-mc2`'s
  key text differs because Q3 shortened `` `can`, boolean-only `` to bare `` `can` `` -- same choice
  id, same underlying correct answer, wording only. No other question in the task shows a mismatch;
  all reorders elsewhere are clean. Reported here per RULES.md "report it; do not pad" rather than
  reverting an approved fix to force a script pass.

## Letter-reference and distractor verification (RULES.md "After applying a fix" #3, #4)

Grepped all 24 rationale strings for a standalone single letter `a`-`e` not part of a word,
backtick-quoted identifier, or code token (the article "a" excluded from the scan since it is not a
choice reference): zero hits in `b`-`e`, confirming no rationale in the task names a choice by
letter.

Two-question check for every new or rewritten distractor this round:

- `4d-mc` choice d (string-key reference): real practice someone might try? **Yes** -- treating a
  set like a map with a named key is a natural (if wrong) instinct. Taught reason it's wrong? **Yes**
  -- lesson states a set has "no secondary identifiers," unlike map/object's "named labels."
- `4b-mc2` choice a (no ordering, name is plain data): real belief? **Yes** -- assuming a `name`
  argument's own semantic content (or lack of it) determines whether Terraform tracks a dependency.
  Taught reason wrong? **Yes** -- 4b teaches any attribute reference creates the implicit dependency,
  regardless of what the argument is named.
- `4b-mc2` choice b (reference processed first): real belief? **Yes** -- a plausible but backwards
  "whoever holds the reference must run first" mental model. Taught reason wrong? **Yes** -- 4b/4f
  both teach the *referenced* resource completes first, not the resource containing the reference.
- `4f-mc2` choice b (`replace_triggered_by`): real practice? **Yes** -- a genuine `lifecycle`
  argument, verified against `meta-arguments/lifecycle` this turn. Taught reason wrong here? **Yes**
  -- newly taught by L4: it forces a replacement on a trigger, not create-before-destroy sequencing.
- `4f-mc2` choice c (`ignore_changes = all`): real practice? **Yes** -- the documented bare-keyword
  form, verified this turn. Taught reason wrong here? **Yes** -- newly taught by L4: it stops planned
  updates, unrelated to replacement ordering.
- `4h-mr` choice c (type conversion): real practice? **Yes** -- `tostring()`/`tonumber()` are real,
  taught (4d) type-conversion functions; applying that shape to `nonsensitive` is a plausible
  confusion. Taught reason wrong? **Yes** -- the lesson's own `nonsensitive` paragraph says it "does
  not touch state, does not make a value ephemeral" and only "lifts the CLI/UI redaction," i.e.
  changes a marking, not a type.
- `4h-mr` choice d (Vault data source keeps credentials out of state): real practice/belief? **Yes**
  -- conflating "short-lived credential" with "excluded from state" is a plausible practitioner
  error, and the underlying mechanism (a `data` block reading Vault-issued credentials) is real,
  verified against HashiCorp's own Vault tutorial this turn. Taught reason wrong? **Yes** -- the
  lesson states Vault-issued credentials "are typically consumed as ephemeral or write-only values,"
  meaning Vault alone is not one of the state-excluding mechanisms.
- `4a-mr` choice a (new key, `terraform_data`): not a distractor, this is a key; verified against
  lesson row 82, unchanged content from the existing `4a-mc` distractor of the same wording.
- `4a-mr` choice c (new key, re-read each run): not a distractor, this is a key; verified against
  new lesson row 84 (L2, this round).
- `4a-mr` choice e (new distractor, `terraform_data` cannot stand alone): real belief? **Yes** --
  assuming any `resource` block needs a "real" resource of the same kind nearby is a plausible
  category confusion. Taught reason wrong? **Yes** -- lesson row 82's own text says `terraform_data`
  is for cases with "no other logical managed resource in which to place them."
- `4d-mr` choice d (`for_each` accepts a plain list): real practice/belief? **Yes** -- assuming
  `for_each` works like `count` with any ordered collection is a common beginner error. Taught
  reason wrong? **Yes** -- 4d's own prose: `for_each` "needs a map or a set precisely because those
  are the two types with no meaningful 'position'."
