# Lead Dev pre-check before round 2 — tf-g6 questions

The distractor audit had no g6 terms, so the writer counted distractor types by hand. The Lead Dev added 24 g6 constructs to `TERMS` (`-lock=false`, `force-unlock`, `use_lockfile`, `-migrate-state`, `-reconfigure`, `-refresh-only`, `terraform import`, `state rm` and so on). tf-g4 and tf-g5 still PASS with the new terms.

**Chain:** all PASS.
- `content_lint`, `stem_echo_check` (0) and `test_q1_letter` pass.
- `q1_batch_check`: longest-is-key 12%, shortest-is-key 0%, MC key positions a2/b2/c2/d2.
- `distractor_type_audit`: PASS after LD-Qg6-001.

All 12 questions and every choice were read. Keys are correct, rationales explain by content with no letters, and the distractors are real misconceptions refuted by the lesson.

## Findings
- **LD-Qg6-001 (low, fixed by the Lead Dev).** In 6b-mc, a distractor named `terraform state rm` / `terraform state mv` as examples, which put the `state rm` type in 2 of 12 questions (over cap; 6d-mr owns it). It now reads "Locking covers `apply` but not the `terraform state` subcommands that modify state". The meaning is unchanged, and the audit passes.
- **LD-Qg6-002 (for round 2).** 6d-mc2 has two weak points; the writer also flagged them.
  - The `terraform import` distractor ("once per bucket ... then continue") fails the stem's need of "adoption visible in the plan output". But the lesson sentence that would refute it most directly ("no plan preview") was dropped in the round 1 fix pass as unsupported.
  - The rationale's "works on one object per run" and "imports several resources in one reviewed run" may not be taught.
  - Reviewers should verify against the lesson and docs, and either confirm the refutation is taught or propose a fix.
