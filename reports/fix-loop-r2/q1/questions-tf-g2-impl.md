# Questions tf-g2 (lesson-tf-g2, tf.004.2a/2b/2c/2d) — implementation report

12 questions: 3 per objective (`-mc`, `-mc2`, `-mr`), `id`/`type`/`module`/`objectiveIds`/`selectCount` unchanged from the placeholder files. `citationIds` set to all 5 of lesson-tf-g2's citations, `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` on every question.

## Per-question fact and teach-before-test map

| Question | Discriminator tested | Taught in lesson at |
|---|---|---|
| 2a-mc | `~>` allows only the right-most component to increment, vs. `>=`, `=`, `!=` misapplied | 2a's operators paragraph |
| 2a-mc2 | A committed dependency lock file guarantees an identical build/checksum; a version constraint (even a tight `~>`) is still a range | 2a's lock-file paragraph + discriminator |
| 2a-mr | `!=` and `~>` definitions, contrasted with `>=`, `=`, `<=` misapplied | 2a's operators paragraph |
| 2b-mc | `provider` block (runtime settings, e.g. region) vs. `required_providers` (declares provider+version only) vs. resource block vs. lock file | 2b's discriminator paragraph |
| 2b-mc2 | The provider itself defines its resource types; Terraform core has no built-in catalog | 2b §1 |
| 2b-mr | Implied default source `registry.terraform.io/hashicorp/<LOCAL NAME>` and the `[<HOSTNAME>/]<NAMESPACE>/<TYPE>` address structure | 2b §2 |
| 2c-mc | A second configuration of the *same* provider (two Regions) needs `alias` + `provider = aws.<alias>`, vs. a second `required_providers` entry / an unrelated provider / a duplicated file | 2c's alias paragraph |
| 2c-mc2 | Distinct providers route to their own default configuration by resource-type ownership, with no `alias` needed for a single default | 2c §1 |
| 2c-mr | Compound local name (namespace-dash-type) resolves a naming collision; `required_providers` still needs one entry per provider regardless | 2c's naming-collision paragraph + 2b's required_providers fact |
| 2d-mc | State's mapping purpose links an already-created object to its resource block, avoiding a duplicate on re-apply | 2d §1 (mapping) |
| 2d-mc2 | Default state location is the local `terraform.tfstate` file, separate from `.tf` configuration | 2d §2 |
| 2d-mr | State's mapping purpose + metadata purpose, contrasted with data backup / access control / config-rewriting | 2d §1 |

No two questions test the identical fact; 2c-mr's `required_providers`-enables-one-provider key is a different sub-fact from 2b-mc/2b-mc2's use of `required_providers` (declaring vs. configuring a provider) and from 2c-mc's alias mechanism.

## Round 2 — two Student-flagged distractors replaced

The Student found two g2 distractors dismissible without knowing any Terraform. Both were mine (Lead Dev pre-check had left g2 alone), replaced with a real mechanism each, verified against developer.hashicorp.com in this turn rather than assumed:

- **`q-tf-004-2a-mc2` choice b** — was "Every machine runs `terraform init` on the same calendar day so they all see the same latest release" (pure coincidence, not a real practice). Replaced with "Have every engineer run `terraform init -upgrade` before each build, so each machine picks up the newest version that still matches the configured constraint." `-upgrade` is a real, commonly-reached-for flag. Per `developer.hashicorp.com/terraform/cli/commands/init`: "Upgrade all previously-selected plugins to the newest version that complies with the configuration's version constraints," and "This will cause Terraform to ignore any selections recorded in the dependency lock file, and to take the newest available version matching the configured version constraints." It fails the stem's stated "byte for byte, not merely a version that satisfies the same range" requirement for exactly the reason the lesson teaches: only the committed lock file pins an exact, reproducible build; `-upgrade` explicitly bypasses that lock file. Distinct from choice a's already-used "tight `~>` constraint is still a range" angle — this is a command that actively discards the lock file rather than a constraint that happens to be loose.
- **`q-tf-004-2c-mr` choice a** — was "Edit the second provider's local package name in its own source code so the two no longer collide" (not something a consuming configuration can do to a third-party provider; eliminable on sight). Replaced with "Give each provider a distinct `source` address in its own declared entry, but keep both entries under the same local name." Per `developer.hashicorp.com/terraform/language/providers/requirements`: "Terraform requires unique local names for each provider in a module, so you'll need to use a non-preferred name for at least one of them," and giving each a distinct source address alone does not change that — the page's own compound-local-name recommendation exists precisely because a distinct `source` is not sufficient. This is a real thing an engineer might try (assuming `source` disambiguates identity), and it fails for the taught reason (the lesson's naming-collision paragraph already says to use a compound local name "rather than relying on the plain local name for both," which is the same point). Distinct from choice b (deleting the version-constraint declaration) and choice c (giving both the same `alias`) — neither duplicated.

No key moved in either question (`correctAnswerIds` unchanged in both files, confirmed by diff against the pre-fix commit). The first draft of the `2c-mr` replacement literally said `` `required_providers` `` and pushed that term to 2 questions (over the 1-question cap); reworded to "its own declared entry" to stay at 1. No new named tool or product was introduced by either fix, so no `TERMS` addition was needed this round.

## Distractor type table (`distractor_type_audit.py tf-g2`)

| Term | Count | % of 12 | Questions |
|---|---|---|---|
| required_providers | 1 | 8% | q-tf-004-2b-mc |
| provider block | 1 | 8% | q-tf-004-2c-mc2 |
| dependency lock file | 1 | 8% | q-tf-004-2d-mc2 |

Cap is 1 question (15% of 12) per curated term; all three sit at the cap. This required rewording 8 distractors across 6 questions during drafting — the first pass had `required_providers` in 6 distractors, `dependency lock file` in 3, and `provider block` in 2 — each rewrite kept the same wrong-answer reasoning while describing the block/file by function ("the block that declares the provider and its version constraint," "the file that records installed provider versions and checksums") instead of repeating the exact term, so only one distractor per task still names each term directly.

## Stem/key wording

`stem_echo_check.py tf-g2`: 0 unwaived giveaway, 0 waived, 1 bulk echo (advisory only, not a defect per RULES.md) — clean. 4 tokens surfaced as stem/key-only overlaps during drafting and were resolved by rewording (not waived):
- 2a-mc2: stem's "exact ... checksum for checksum" → "identical ... byte for byte" (removed `checksum`/`exact`, which only the key otherwise carried).
- 2a-mr: stem's "know exactly which" → "know precisely which" (removed `exactly`, which only one key otherwise carried).
- 2c-mr: distractor (a) reworded to "Edit the second provider's local package name in its own source code..." so `local` now also appears in a distractor rather than only in the stem and one key.
- 2d-mc: key's "that specific resource block" → "that particular resource block" (removed `specific`).

The one advisory bulk-echo (`q-tf-004-2b-mc2`, key shares 3 stem tokens vs. best distractor's 2) was read per RULES.md guidance not to assume a defect: the shared tokens are `terraform`, `instance`/`instances`-family, and `provider`/`providers`, all of which are the scenario's own subject matter (a `resource "aws_instance"` block and why it works), not a keyword that lets a reader skip understanding the mechanism. Left as-is.

## Script changes

- `scripts/distractor_type_audit.py`: added a Terraform `TERMS` section (`CloudFormation`, `HCP Terraform`, `required_providers`, `provider block`, `dependency lock file`, `resource graph`, `terraform.tfstate`, `random_pet`, `random provider`), and fixed file selection to use the lesson's `objectiveIds` when `content/lessons/lesson-<task>.json` exists (the old `glob(f"q-*-{task}-*.json")` never matched `tf-g1`/`tf-g2`, since no question filename contains a `-tf-g1-`/`-tf-g2-` token — filenames are `q-tf-004-2a-mc.json` etc.).
- `scripts/stem_echo_check.py`: same file-selection fix, for the same reason.

## Checks (re-run against the whole file after the round-2 fix, per RULES.md "After applying a fix")

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g2`: PASS (0 FAIL, 0 WARN) — no tell words, no giveaway wording, no template stems, no duplicate 6-word openings, longest-is-key 1/8 = 12% (≤35%), MC key positions {a:3,b:2,c:2,d:1}, MR key slots {a:2,b:2,c:1,d:1,e:2}, MR key sets all distinct.
- `distractor_type_audit.py tf-g2`: PASS (table above, unchanged counts — both replacements avoided the curated terms already at cap).
- `stem_echo_check.py tf-g2`: PASS (0 unwaived giveaway; 1 advisory bulk echo, discussed above — unchanged by this round's edits).
- `claim_prose_check.py tf-g2`: PASS (7 distinct numbers in lesson prose, all present).

Also re-ran `q1_batch_check.py tf-g1` as a sanity check since both tasks share `distractor_type_audit.py`'s `TERMS` list: still PASS, g1 untouched (confirmed via `git diff --stat`, which showed only the two intended g2 files changed).
