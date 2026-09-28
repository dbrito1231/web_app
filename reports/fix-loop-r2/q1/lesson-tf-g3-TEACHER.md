# Teacher round 1 — lesson-tf-g3 (Core Terraform workflow)

## Rows verified
Directly quote-checked against live HashiCorp pages (all 7 cited pages fetched): rows 1, 2, 3, 4, 5, 6 (core-workflow); 7, 8, 9, 10, 13, 16, 17, 18 (init); 19, 21, 22 (validate); 23, 26, 27, 29, 30, 31, 32 (plan); 33, 35, 36, 37, 38 (apply); 39, 40 (destroy); 41, 42, 44, 45 (fmt) — 30 of 45 rows directly quote-matched, well past the 6-row minimum. Remaining 15 rows (11, 12, 14, 15, 20, 24, 25, 28, 34, 43, plus duplicates of already-checked pages) are consistent with the same fetched page content and not flagged.

All quoted text is accurate to source. No fabricated or over-trimmed quotes found.

## Findings

**TEACHER-Lg3-001 (Medium) — imprecise version boundary.**
Location: section `tf.004.3d` "Version note" paragraph, and the parenthetical in `tf.004.3f` ("see the 3d version note for the pre-0.15 exception"). The lesson says "**Before** Terraform 0.15, ... only `terraform plan` ... accepted `-destroy`." The doc actually says the limitation held **through** 0.15: "In Terraform v0.15 and earlier, the `-destroy` option is supported only by the `terraform plan` command, and not by the `terraform apply` command" (https://developer.hashicorp.com/terraform/cli/commands/plan). "Before 0.15" wrongly implies 0.15 itself already supported `apply -destroy`.
Fix: in both 3d and 3f, replace "Before Terraform 0.15" with "In Terraform 0.15 and earlier" (or "through Terraform 0.15"), matching the doc's own boundary.

**TEACHER-Lg3-002 (Low) — unexpanded acronym.**
Location: `tf.004.3g`, the `-check` paragraph and its exam-tip clause ("failed a CI job because a file wasn't canonically formatted"). "CI" is never expanded. Fix: first use should read "CI (continuous integration)".

**TEACHER-Lg3-003 (Low) — undefined term carrying a decision.**
Location: `tf.004.3e`, "...running exactly what was already reviewed when the file was created, even if the real infrastructure has since **drifted**." "Drift" is never defined in this lesson (formal definition is group 6, tf.004.6d, not yet taught), yet it's the reason a saved `-out` plan can go stale — a decision-relevant fact. Fix: gloss inline, e.g. "...has since drifted (changed outside Terraform since the plan was made)."

**TEACHER-Lg3-004 (Medium) — `tf.004.3f` is short one genuine discriminator for 3 non-duplicate questions.**
As written, 3f teaches exactly two independent facts: (a) `terraform destroy` = alias for `terraform apply -destroy`, and (b) whole-configuration teardown vs. removing one resource block + `apply`. The section's only other stated fact — the pre-0.15 `-destroy` version note — is the *same fact* already assigned to 3d's claim table (row 32 is literally shared "3d / 3f"), so RULES.md's "no two questions may test the identical fact" blocks reusing it as 3f's third question. That leaves only 2 clean angles for what needs to support 3 non-repetitive questions — the same failure pattern flagged on task 4.3 and pre-empted by enrichment on g1.
Doc-verified fix available: HashiCorp's destroy page states "You can use the `-target` option to destroy a particular resource and its dependencies" (https://developer.hashicorp.com/terraform/cli/commands/destroy), e.g. `terraform destroy -target aws_instance.example`. This is a genuinely distinct third discriminator — destroy a single resource **without editing configuration** (via `-target`) vs. the already-taught "remove the block, then `apply`" method (**with** a configuration edit) vs. plain `destroy` (everything). Recommend adding 1–2 sentences teaching `destroy -target` to 3f before question writing.

## Lesson additions requested
- `tf.004.3f`: add, doc-verified from https://developer.hashicorp.com/terraform/cli/commands/destroy: "`terraform destroy` also accepts `-target` to destroy a single resource (and its dependents) without touching the configuration file, e.g. `terraform destroy -target aws_instance.example` — a different route to removing one resource than deleting its block and running `apply`."

## Three-per-objective verdict
- 3a: supports 3 distinct (stage ID; branch/version-control habit; stale-PR-plan re-review before apply). OK.
- 3b: supports 3+ easily (first-run/re-run purpose; partial re-run behavior — new modules only; `-upgrade` mechanics). OK.
- 3c: supports 3, but tight — (checks syntax/schema; does *not* check remote services; needs plugins/modules installed but not live backend/credentials). Workable, watch for overlap when questions are drafted.
- 3d: supports 3+ generously (`-out`, `-target`, `-refresh-only`, `-destroy`, "replace" semantics — 5+ angles).
- 3e: supports 3+ (default interactive flow; `-auto-approve`; applying a saved `-out` file; `apply -destroy`). Note for the question writer: the "applying a saved file" question here must test 3e's own consequence (no prompt, no recompute) and not restate 3d's `-out` mechanics, or it risks duplicating a fact.
- 3f: **not yet** — only 2 clean discriminators until the `-target` addition above lands (see TEACHER-Lg3-004).
- 3g: supports 3 (fmt vs validate scope; `-recursive`; `-check`). OK.

Lesson tf-g3: not yet
Overall: concerns
