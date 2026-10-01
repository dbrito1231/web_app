# Teacher round 1 — lesson-tf-g7

Saved by the Lead Dev from the Teacher's reply (condensed; fixes verbatim).

**Method.** All 104 quotes were fetched with curl and matched: 103 are verbatim, and row 34 is a stitched list (006). Twelve rows were also read in context. The cross-references to g3 3d, g4 4h and g6 6d were checked with a regex, and all hold.

## Findings
- **TEACHER-Lg7-001 (medium, 7c, Saving the log).** The lesson says `TF_LOG` must be set. The troubleshooting tutorial pairs `TF_LOG_PATH` with `TF_LOG_CORE` or `TF_LOG_PROVIDER` instead.
  - After "TF_LOG must be set" add: "The troubleshooting tutorial instead says 'If your TF_LOG_CORE or TF_LOG_PROVIDER environment variables are enabled, the TF_LOG_PATH variable will create the specified file' (a level is still needed; the exam answer is TF_LOG)." Add a row and a cite.
  - Keep "a level variable such as `TF_LOG`" in the exam tip.
- **TEACHER-Lg7-002 (medium, 7b push).** "Lineage" and "serial" are not glossed. Replace "The first refuses… being pushed" with: "A differing lineage 'suggests that the states are completely different and you may lose data'; a higher serial 'suggests that data is in the destination state that isn't accounted for in the local state being pushed'." Add rows.
- **TEACHER-Lg7-003 (low, 7a).**
  - Merge the plan and apply bullets ("plan shows 'Plan: 1 to import…'; apply performs it"); this re-teaches 6d.
  - Gloss the `east` alias: "an alias is a second named configuration of the same provider, for example another region".
  - Change "6d showed the two blocks involved" to "the `import` block and the resource block".
- **TEACHER-Lg7-004 (low, 7c).** `TF_LOG_PROVIDER` has no sentence or row. Add "`TF_LOG_PROVIDER` covers 'All providers and provider SDKs used during the run'." with a row.
- **TEACHER-Lg7-005 (low, 7c inference).** The labelled advice is acceptable, but the Warnings repeat it unlabelled.
  - In 7c: "Our own advice, not a doc claim: read a log before you attach it, and keep it out of version control, as you would a state file."
  - In Warnings: "This lesson's advice: …".
  - Questions must not test it.
- **TEACHER-Lg7-006 (low, table).**
  - Row 34: use the single span "It cannot determine: the health of the infrastructure."
  - Rows 91–92: quote only "Does not include providers." and "Overrides all other logging environment variables."
- **TEACHER-Lg7-007 (low, 7b).** "Treat both as sensitive" blurs two claims. Change it to "`show -json` prints sensitive state values in plain text; a saved plan 'can contain sensitive data'." No question may claim plain `show` redacts or reveals.

**Teaching quality.** Contrasts are present; `TF_LOG_PROVIDER` is thin (004), and the PATH-with-level point is tangled (001). Overlap with g6: the lesson goes deeper and does not re-teach, except the plan and apply bullets (003). There are no contradictions. The exam tips are accurate.

## Three facts per objective, with ownership
- **7a (ample).**
  - mc: generated configuration as a pruned draft that can still produce a replace. Not the existence of the flag; 6d owns that.
  - mc2: `for_each` on the import block.
  - mr: the ID from the provider docs, known at plan time; `id` and `identity` exclusive; no relationships; whole lifecycle including destroy.
- **7b (ample after 002).**
  - mc: `state list -id=` and module filtering.
  - mc2: `-raw` vs `-json`, root-only, named-output redaction, ephemeral omission.
  - mr: `show planfile`, `pull` vs `push`, lineage and serial, `-force`.
  - Plain `state list`/`show` are spare options only (6d owns them). "-json/-raw print sensitive values" is never the key (4h owns it).
- **7c (ample after 001 and 004).**
  - mc: the level order, `TF_LOG=JSON`, and stderr by default.
  - mc2: CORE vs PROVIDER, and `TF_LOG` precedence.
  - mr: `TF_LOG_PATH` appends and does nothing alone; TRACE for bugs.
  - Do not test the inference or the tutorial's CORE/PROVIDER-with-PATH detail.

Lesson tf-g7: not yet (fix 001–002; 003–007 may ride along) · Overall: concerns
