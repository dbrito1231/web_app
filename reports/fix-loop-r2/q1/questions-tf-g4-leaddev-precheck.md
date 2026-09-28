# Lead Dev pre-check before round 2 — tf-g4 (HEAD a56bbd0, content at db11570)

All five scripts PASS and each inspected 24 questions (lint 429 questions; batch check "task tf-g4: 24 questions"; distractor audit 24; stem echo 24 with 1 advisory bulk echo on `4a-mr`; claim-prose 9 numbers). The findings below were found by reading every choice. No script sees any of them.

"Untaught" below was checked with a case-insensitive regex over `bodyMarkdown`, not a backtick-sensitive substring. Zero hits in this lesson for: `ignore_changes`, `TF_VAR`, `environment variable`, `sort` as a function, `refresh`/`re-read`/`every run`, and nonsensitive-on-an-unmarked-value. `ignore_changes` and `TF_VAR` appear in no lesson at all.

## Questions

- **LD-Qg4-001 (high) — letter references in 10 rationales, and the letters are wrong.** RULES: "No letter references." Affected: `4a-mr`, `4b-mr`, `4c-mr`, `4d-mr`, `4e-mr`, `4f-mc`, `4f-mr`, `4g-mr`, `4h-mc2`, `4h-mr`. The letters are shifted, which is consistent with choices being reordered for key balance after the rationales were written. Examples: in `4a-mr` "c misstates data blocks as managing a stateful placeholder" describes choice b; in `4h-mc2` "b names a real version floor … check blocks" describes choice a. A learner reading the rationale is told the wrong option is wrong. A scan of all 429 files found this only in tf-g4 (three SAA hits were false positives: "account B invoke", "SSE-C still", "AZ-C is not"). Fix: rewrite each rationale to name options by content.
- **LD-Qg4-002 (high) — `4d-mc` choice d may be a correct answer.** "Sort the set alphabetically first; it becomes indexable." `sort()` returns a list, so `sort(var.names)[1]` indexes the result. The rationale's claim "a set is still not indexable, sorted or not" looks false. `sort` is also not taught in the lesson. Reviewer: verify against the `sort` function page and say whether this is a second correct answer.
- **LD-Qg4-003 (high) — `4f-mc2` two bad distractors.** (i) `ignore_changes = [all]`: `ignore_changes` is untaught in any lesson (real but untaught), and the documented special form is `ignore_changes = all`, so the bracketed form may be invalid syntax as written. (ii) `count = 2 (creates two independent instances instead of sequencing …)`: the parenthetical refutes itself (giveaway), and `count` is not a `lifecycle` argument although the stem asks "Which lifecycle argument fits?".
- **LD-Qg4-004 (high) — `4e-mc2` key is self-justifying.** The key reads "`can`, boolean-only", which echoes the stem's "plain true/false result" and annotates only the key.
- **LD-Qg4-005 (medium) — `4h-mr` choices c and d.** c depends on how `nonsensitive()` behaves on a value that was never marked sensitive. That is untaught, and the rationale asserts it is "documented as an error". Verify against the current function page, because this behaviour may have changed in a later release. d ("Vault-issued credentials are stored directly as Terraform language keywords") is not a belief anyone holds, so it is a caricature.
- **LD-Qg4-006 (medium) — `4c-mc2` choice c rests on the `TF_VAR_` prefix,** which is untaught. It is real but untaught. d (reusing the previous apply's value) is also not taught, although it is plausible to eliminate.
- **LD-Qg4-007 (medium) — `4b-mc2` choices a and b are caricatures.** a is "the instance profile depending on the instance's IP address"; b is "pointing to whichever object is destroyed first". No practitioner believes either. Only c (a `depends_on` is also required) is a real misconception.
- **LD-Qg4-008 (low) — absolutist strawmen.** `4d-mr` d: "behave differently in every situation … can never be used interchangeably in Terraform's own documentation". `4a-mr` e: "locked and can never be refreshed". Also check whether re-reading on each run is taught at all.

## Lesson

- **LD-Lg4-009 (medium) — 4g contradicts itself.** It opens with "Three condition mechanisms check different things…", and later says "`check` blocks are the fourth mechanism, the newest of the four".
- **LD-Lg4-010 (medium) — 4h miscounts the sources of ephemeral values.** "There are three ways to get one" lists a write-only argument as one of them. A write-only argument receives an ephemeral value; it does not produce one. The next paragraph states that correctly ("how an ephemeral value reaches…").
- **LD-Lg4-011 (low) — 4h, "in the writer's own words"** means the documentation's words.
- **LD-Lg4-012 (low) — 4a has a doubled "but"**: "Terraform normally reads a data source during planning, but "Terraform attempts …," but "it may defer …"".

## Observation for the reviewers (from HANDOFF, not yet raised)

After the key-length rebalance, 94% of MC keys sit at length rank 2 or 3 of 4, against 50% by chance. Both caps pass (6% longest, 0% shortest). Is "eliminate the longest and the shortest" a real tell, or over-fitting a metric?
