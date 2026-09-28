# Drill record: tf-g3 (Core Terraform workflow, 21 questions)

## Committed answers (written before opening the key)

**Q1** — a) Write. Editing `.tf` files with nothing on the account changed yet is the write stage by definition.

**Q2** — b) Each engineer works on a separate branch. This is the literal team-workflow recommendation for avoiding collisions.

**Q3** (select two) — b, d. Reviewing the plan in the PR, and re-reviewing a fresh plan immediately before applying the merged branch, are the two collaboration steps the lesson calls out.

**Q4** — c) terraform init. Missing provider plugins is exactly what init installs; it's also the standard first command after a clone.

**Q5** — d) Leaves already-installed modules alone, retrieves only the new module's source. Matches "will install the sources for any modules that were added... but will not change any already-installed modules."

**Q6** (select two) — a, c. `-upgrade` disregards the lock file's recorded selections (a) and installs the newest version matching constraints (c) — that combination explains the version mismatch between the two teammates.

**Q7** — a) terraform validate. No-credentials, fast check of attribute names/types is validate's defined job.

**Q8** — b) validate does not validate remote services (state/provider APIs), so it can't know a security group vanished from the real account.

**Q9** (select two) — c, e. validate needs an initialized directory with plugins/modules (c), and it runs without a working backend or live credentials (e).

**Q10** — c) -refresh-only. Reconciles state to match manual out-of-band changes without proposing any real-infrastructure change.

**Q11** — d) Covers aws_instance.example and the security group it references, since -target pulls in dependencies.

**Q12** (select two) — a, d. Forced recreation shows as one "replace" action (a); a saved -out file can later be applied exactly as computed, without recomputing (d).

**Q13** — c) -auto-approve. Directly removes the interactive confirmation, which is what an unattended pipeline needs.

**Q14** — b) Applying a saved plan file performs exactly what's recorded, no regeneration, no prompt.

**Q15** (select two) — b, e. apply -destroy builds a full-teardown plan and runs it like a normal apply (b); without -auto-approve it still prompts (e).

**Q16** — c) terraform destroy. Removes everything the configuration manages, ending in empty state — matches the ask directly.

**Q17** — d) terraform destroy -target aws_db_instance.old. No config edit, and the "fine with dependents also removed" condition matches destroy -target's wider blast radius exactly (ruling out the block-deletion route, which requires an edit).

**Q18** (select two) — a, b. destroy -target also takes out the dependency (a); deleting only the instance's block and applying leaves the security group untouched (b), since plan only removes what the edited config stopped describing.

**Q19** — a) -recursive. Explicitly documented as processing subdirectories in addition to the current directory.

**Q20** — b) File is left as-is, exit status non-zero, filename listed. That's -check's defined behavior, the opposite of a rewrite.

**Q21** (select two) — c, d. fmt and validate check unrelated properties (c); a file can be perfectly formatted and still fail validate on something like a bad attribute name (d).

No guesses on this drill — every answer was a direct match to a discriminator or exam-tip line in the lesson text; none required a coin-flip between two live options.

## Marking

Checked against `student-answers-tf-g3.md`. All 21 match the key.

**Score: 21/21**

## Fairness judgement

No wrong answers and no flagged guesses, so there is nothing to adjudicate under "wrong or guessed" — but a clean score is itself worth scrutinizing for whether the questions were too easy to game rather than genuinely testing understanding. See the counts below.

## Keyword-guessable (defect) vs structural scenario reference

**Keyword-guessable:** `Q1`. The stem's action ("opens an editor and writes new `.tf` files") shares the word "write(s)" with option (a) "Write," and no wrong option (Apply / Plan / Initialize) contains that word anywhere. A student could answer purely by string-matching "write" in the stem to "Write" in the options, without knowing that write/plan/apply is a three-stage model at all.

**Structural scenario reference (not a defect):**
- `Q5` — "module" appears in the stem and in options (a), (b), and (d), not just the correct one — a real distinction has to be made among them.
- `Q6` — "lock file" and "-upgrade" both appear across correct and wrong options.
- `Q9` — "backend" and "credentials" appear in both correct and wrong options (a, b, c, e all use them).
- `Q11`, `Q14`, `Q15`, `Q17`, `Q18` — these all reuse the specific command/flag/resource name the stem itself introduced (`-target`, `aws_instance.example`, `infra.tfplan`, `-destroy`, `aws_db_instance.old`) across multiple options; that's the stem's own scenario vocabulary recurring, not a leak isolated to the key.
- `Q20` — "-check" is named directly by the stem as the command under test; every option is about the consequence of that named flag, not a hidden lexical tell.
- `Q21` — "canonically formatted" appears in both a wrong option (e) and the correct one (d).

So: **1 keyword-guessable stem (Q1)**; the rest of the apparent term overlaps are structural.

## Eliminable-on-sight distractors

- `Q2(c)` "lock the entire repository until one change is finished" — no real team workflow does this; dismissed without needing branch/plan knowledge.
- `Q2(d)` / `Q3(e)` "apply directly from an individual's laptop instead of the shared/reviewed branch" — obviously defeats the point of a shared-state, PR-reviewed workflow; dismissed on practice grounds alone.
- `Q3(c)` "merge with no plan review at all, trusting the tool automatically" — contradicts the entire premise of the stem (a team that reviews every PR); eliminable without deep knowledge.
- `Q4(d)` "terraform destroy" as the fix for missing provider plugins — a destroy command has no plausible connection to installing anything; eliminated on sight.
- `Q9(d)` "validate cannot run until the configuration has already been deployed once" — backwards on its face for a pre-deploy sanity check; eliminable.
- `Q13(d)` "-check" offered as a way to skip an apply confirmation — a student who merely recalls "-check is fmt's flag" can eliminate it without reasoning about apply at all.
- `Q15(d)` "apply -destroy does nothing unless a resource address is separately supplied" — an oddly specific negative claim with no support anywhere in the lesson; eliminable by elimination rather than knowledge.
- `Q16(b)` "terraform init -backend=false" as the way to tear down a whole environment — init never removes resources; eliminated instantly.
- `Q18(e)` "deleting the instance's block also removes the security group's block" — no mechanism does that; illogical on its face.

## Untaught facts

None found. Every question resolves from a discriminator sentence or exam-tip line printed in the lesson body above the questions (including the 0.15.2 version-boundary fact in Q15, and the dependency-lock-file behavior in Q6) — nothing required outside CLI experience, a version boundary not stated in the text, or a command's exact output format that wasn't already quoted.

## Match-the-name questions

- `Q1` — pure name match. "Write" literally echoes the stem's verb; no understanding of the stage's *boundaries* was needed to answer it (see keyword-guessable finding above).
- `Q4` — functional. Choosing `init` over `fmt`/`validate`/`destroy` requires knowing what each command *does* (only init installs providers), not just recognizing a name.
- `Q7` — functional. Requires knowing validate's specific scope (attribute names/types, no credentials) versus fmt/init/destroy's different jobs.
- `Q10` — functional. `-refresh-only` vs `-destroy`/`-out`/`-target` requires understanding what each plan mode actually reconciles, not just its name.
- `Q13` — borderline. `-auto-approve` is fairly nameable ("auto" + "approve" almost states its function), but distinguishing it from `-check` (a different command's flag) still requires knowing which command each flag belongs to.
- `Q19` — borderline/name-leaning. `-recursive` is close to self-describing ("nested subdirectories" -> "recursive"), so this leans toward vocabulary recognition, though the wrong options (`-check`, no-flag, `validate`) still require knowing fmt's own scope to eliminate.
- `Q20` — functional. Requires knowing -check's specific behavior (no rewrite, non-zero exit, filenames listed), which is a behavioral fact, not a name lookup.
- Most select-two questions (Q3, Q6, Q9, Q12, Q15, Q18, Q21) require reasoning about *what happens*, not matching a name to a description, since the wrong options are behavioral misstatements rather than name swaps.

## Summary

21/21. One stem (Q1) is keyword-guessable by strict definition, though it is also the simplest possible question on this drill (naming the write stage) so the defect has low practical stakes. No untaught facts. A handful of distractors (listed above) are eliminable by real-world implausibility rather than lesson knowledge, which is normal and expected for a well-built drill, not a flaw. Two questions (Q1, and to a lesser extent Q19) lean on name-recognition rather than functional understanding; the rest of the single-answer and all of the select-two items required actually knowing what each command/flag does.
