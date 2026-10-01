# Lead Dev pre-check before round 2 — tf-g8 lesson fixes and 20 questions

**What happened to the lesson.** The user's commit `53f1beb` (2026-09-30) turned out to apply most of the round 1 lesson fixes itself, not just one citation. It covered the hard-mandatory override, layered execution-mode defaults, the `#### Remote state and workspace locking` split, the Stacks gloss, conditional speculative plans and the cost/policy stage conditions. A text diff of `53f1beb^` → `53f1beb` → working tree confirms that every span the commit added is still in the lesson. The writer then:
- re-checked every round 1 finding against that file;
- added claim rows 220–234, including row 228 for `cite-tf-g8-projects-manage`;
- added an unrequested `#### Enforcement levels` split in 8b;
- appended a "Round 1 fix pass" section to `lesson-tf-g8-impl.md`.

The lesson is 4,861 words; it was 4,851 at `53f1beb`. Round 2 must check the fixes as one lesson change, whoever wrote them. AWS-Lg8-010 (density trimming, optional) was not applied.

**Chain:** all PASS.
- `content_lint`.
- `q1_batch_check tf-g8`: longest-is-key 25%, shortest-is-key 19%, MC keys 4/4/4/4, MR key sets all different.
- `distractor_type_audit tf-g8`: "HCP Terraform" is at exactly 3/20 = 15%.
- `stem_echo_check` 0, `claim_prose_check`, `test_q1_letter`.
- tf-g5, tf-g6 and tf-g7 still pass.

**Read every choice.** All 20 keys are correct as far as the lesson goes. No rationale names a choice by letter. I found no distractor-only "as…/because…" clauses: the trailing clauses in extra-00, 8b-mc and 8a-mc2 appear on the key and on the distractors alike.

I checked the distractors whose refutation was not obvious:
- **8d-mr a** (`TF_WORKSPACE` creates the workspace): refuted by a taught quote ("HCP Terraform will not create a new workspace from this variable").
- **extra-04 a** (immediate lock failure): the "6b covered" cross-reference is true. 6b teaches the `-lock-timeout` default of 0s, which "causes immediate failure".
- **extra-06** (`-var` precedence): the key is a taught quote.
- **extra-07 c** (`.terraformignore`): the lesson teaches it only as a filter on the CLI upload. The distractor is wrong in practice, because it does not choose which commits trigger runs. Low risk; reviewers should confirm.

## Findings
- **LD-Qg8-001 (low, for round 2).** In 8b-mc, distractor c (Read "does not include queuing plans") rests on the role ladder ("Each role builds upon the previous level") plus the Plan role description, not on a quoted Read sentence. The writer flagged this too. Reviewers should decide whether that is taught enough or needs a quoted sentence.
- **LD-Qg8-002 (observation).** The writer proposed eight tf-g8 TERMS for `distractor_type_audit` and did not edit the script. That is deferred to round 2 fixes, because adding terms could move the audit result.
- **HANDOFF correction:** HANDOFF described `53f1beb` as "adds a citation and rewords part of bodyMarkdown". It is a substantial lesson fix pass. HANDOFF is updated.
