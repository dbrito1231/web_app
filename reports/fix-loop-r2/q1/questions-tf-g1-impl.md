# Questions tf-g1 (lesson-tf-g1, tf.004.1a/1b/1c) — implementation report

9 questions: 3 per objective (`-mc`, `-mc2`, `-mr`), `id`/`type`/`module`/`objectiveIds`/`selectCount` unchanged from the placeholder files. `citationIds` set to all 7 of lesson-tf-g1's citations, `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` on every question.

## Per-question fact and teach-before-test map

| Question | Discriminator tested | Taught in lesson at |
|---|---|---|
| 1a-mc | IaC = versioned file stating desired end result vs. wiki runbook / imperative script / spreadsheet | 1a §1–2 |
| 1a-mc2 | The plan stage previews every proposed change before anything is applied | 1a's new core-workflow paragraph |
| 1a-mr | IaC (versioned, reused) + declarative (states end result, not ordered steps) as two independent properties | 1a §2–3 |
| 1b-mc | Resource graph walks a node once its dependencies finish, giving true parallelism vs. serial script / nightly rebuild / team-boundary split | 1b's graph paragraph (incl. the concurrency-default-10 fact) |
| 1b-mc2 | State-backed comparison (drift detection) before a plan vs. blind reapplication / alerting / backup | 1b's new drift paragraph |
| 1b-mr | VCS pull-request review + shared visibility of built infrastructure vs. email / one-laptop / unsynced copies | 1b's collaboration/HCP Terraform paragraph |
| 1c-mc | Provider plugin model (one config, one workflow, multiple vendor APIs) vs. pairing CloudFormation with a second vendor's native tool / post-hoc config management / manual-only | 1c's CloudFormation paragraph |
| 1c-mc2 | Service-agnostic = plugin for any API (cloud, on-prem, or non-cloud SaaS) vs. hardcoded cloud list / scope limited to compute+storage / no-plugin auto-conversion | 1c's new "concretely, that reach spans more than clouds" paragraph |
| 1c-mr | Hybrid = declare an on-prem provider next to a cloud provider in one config/workflow, because the same engine calls whichever plugin matches the resource's platform | 1c's hybrid-cloud sentence |

No two questions in this task test the identical fact; 1a-mc and 1a-mr both touch "versioned file," but 1a-mc tests it alone against non-file alternatives while 1a-mr pairs it with the separate declarative property against imperative/manual-drift alternatives.

## Round 2 — distractor pass (caricatures replaced with real practices)

Lead Dev's pre-check flagged 9 distractors across 6 questions as strawmen (spreadsheet, emailing the file, home-directory copies with a sync reminder, a comment addressed to a human, manual racking, a checklist grouped by team, console-then-wiki, console-clicks-never-written-back) — real teams do not do these, so a student could eliminate them without understanding IaC. Replaced all 9 with practices from the coordinator's in-bounds list (click-ops, imperative CLI scripts, golden images, native single-vendor template languages, configuration-management tools that act after servers exist, manual runbooks), keeping every key unchanged:

| Question | Old distractor(s) | New distractor(s) |
|---|---|---|
| 1a-mc | b: console + wiki doc; d: spreadsheet | b: console click-ops from memory; d: golden image (opaque, not diffable) |
| 1a-mr | a: console-clicks checklist; e: console edits never written back | a: documented manual runbook (ordered steps, not a file); e: golden image + manual in-place patches (drifts from the image) |
| 1b-mc | b: nightly full rebuild; d: checklist grouped by team | b: vendor's native template tool, strictly serial by design; d: config-management tool converging existing servers on a schedule |
| 1b-mr | b: email the file; e: home-directory copies + sync reminder | b: config-management tool pushed straight from a laptop, no review gate; e: applied from one laptop with the built-record kept only there |
| 1c-mc | d: comment addressed to a human | d: one vendor's native template language plus a general-purpose script calling the other vendor's CLI (two languages, two toolchains) |
| 1c-mr | b: manually rack and configure on-premises servers | b: cloud vendor's native tool for the cloud side, a config-management tool for the on-premises side (configures existing machines, does not provision them) |

Rationale text for each changed choice was rewritten to match its new wrong-answer reason. One new stem/key giveaway appeared as a side effect (1a-mr: replacing the old "infrastructure was created once from a file..." distractor removed the only other occurrence of the word "infrastructure," leaving it shared by only the stem and key b); fixed by adding "infrastructure" into the reworded choice a instead of waiving it. Re-ran `stem_echo_check.py tf-g1` after every substitution.

## Distractor type table (`distractor_type_audit.py tf-g1`)

| Term | Count | % of 9 | Questions |
|---|---|---|---|
| snapshot | 1 | 11% | q-tf-004-1b-mc2 |
| CloudFormation | 1 | 11% | q-tf-004-1c-mc |

Cap is 1 question (15% of 9) per curated term; both terms sit at the cap. `resource graph` and `HCP Terraform` appear only as correct-answer text (excluded from the distractor count by design). Added `CloudFormation`, `HCP Terraform`, `required_providers`, `provider block`, `dependency lock file`, `resource graph`, `terraform.tfstate`, `random_pet`, `random provider` to `scripts/distractor_type_audit.py`'s `TERMS` list (previously AWS-only) so this task's distractor terms are actually screened.

## Stem/key wording

`stem_echo_check.py tf-g1`: 0 unwaived giveaway, 0 waived, 0 bulk echo — clean. No waivers file entries needed or added (I do not edit that file). During drafting, 6 tokens surfaced as stem/key-only overlaps (`desired`, `approve`, `against`, and a cluster of shared operational words in the original 1b-mr draft, plus `workflow` in 1c-mc/1c-mr); all were resolved by rewording rather than waived, since each was a genuine paraphrase gap, not a structural scenario reference:
- 1a-mc: stem's "desired setup" → "target setup".
- 1a-mc2: key's "approve it" → "sign off on it".
- 1b-mc2: key's "against the desired configuration" → "with the configuration they are supposed to match".
- 1b-mr: rewrote the stem and both keys from scratch (original draft's stem and keys both reused "application code," "already built," "record," "whole team," verbatim — a genuine echo, not a scenario reference).
- 1c-mc / 1c-mr: key's "same workflow" / "plan/apply workflow" → "same process" / "plan-and-apply sequence" (no distractor used "workflow," so this removed the overlap rather than needing one added).

## `distractor_type_audit.py` script change

Also fixed a pre-existing bug while wiring this up: both `distractor_type_audit.py` and `stem_echo_check.py` selected question files with `glob(f"q-*-{task}-*.json")`, which matches SAA filenames (`q-saa-4-4-*`) but not this task's filenames (`q-tf-004-1a-mc.json`, etc. — there is no `-tf-g1-` token in any filename). Both scripts now fall back to selecting questions by the lesson's own `objectiveIds` (the same approach `q1_batch_check.py` already used) whenever `content/lessons/lesson-<task>.json` exists, which is backward-compatible with the old glob for any task where it already worked.

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g1`: PASS (0 FAIL, 0 WARN) — no tell words, no giveaway wording, no template stems, no duplicate 6-word openings, longest-is-key 2/6 = 33% (≤35%), MC key positions {a:2,b:2,c:1,d:1}, MR key slots {a:1,b:1,c:2,d:1,e:1}, MR key sets all distinct.
- `distractor_type_audit.py tf-g1`: PASS (table above).
- `stem_echo_check.py tf-g1`: PASS (0 unwaived giveaway).
- `claim_prose_check.py tf-g1`: unaffected by this step (lesson-only check); still PASS from the lesson-fix step.
