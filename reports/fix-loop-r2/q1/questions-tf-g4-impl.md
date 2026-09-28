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
