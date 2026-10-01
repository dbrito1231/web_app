# Lead Dev pre-check before round 2 — tf-g7 questions

The lesson round 1 fix pass appended the writer's report correctly. `TF_LOG_PATH` now teaches only what every page agrees on: a level variable must be set alongside the path. The claim table has 118 rows.

**Audit TERMS for g7.** Added: `TF_LOG_PATH`, `TF_LOG_CORE`, `TF_LOG_PROVIDER`, `-raw`, `-json`, `state pull`, `state push`, `identity`, `terraform show`, `terraform output`, `-force`.
- The Lead Dev first also added bare `TF_LOG` and `TRACE`. They flagged 7c-mc and 7c-mc2 as over cap, but they are 7c's own subject vocabulary, so they were removed, with a comment in the script, by the same rule HANDOFF applies to bare `version` in 5d.
- tf-g5 and tf-g6 still PASS with the new terms.

**Chain:** all PASS.
- `content_lint`.
- `q1_batch_check`: longest-is-key 17%, shortest-is-key 17%, keys spread.
- `distractor_type_audit`: every type in at most 1 of 9 questions.
- `stem_echo_check` 0, `claim_prose_check`, `test_q1_letter`.

**Read every choice.** Keys are correct. Rationales explain by content with no letters. Distractors are real and refuted by taught text. No distractor-only justification clauses. Ownership was followed:
- the generate-config flag is not tested (6d owns it);
- plain `state list` and `state show` appear only as options;
- "-json/-raw print sensitive" is not a key.

## Findings
- **LD-Qg7-001 (low, fixed by the Lead Dev).** Five stems stated a need without asking a question: 7a-mc2, 7b-mc, 7b-mc2, 7c-mc and 7c-mc2. Each now ends with a short question ("Which command finds it?" and similar). The echo check and 6-word-opening check still pass.
- **LD-Qg7-002 (observation, for the final sitting).** A scan of all Terraform questions finds the same question-less stem in closed tasks: tf-g1 (1a-mr, 1b-mr, 1c-mr), tf-g2 (2a-mr, 2b-mr, 2d-mr) and tf-g4 (4a-mc). It also appears in three tf-g8 placeholders, which will be rewritten. This is not a correctness defect. Consider a `q1_batch_check` rule that flags a stem not ending in "?".
