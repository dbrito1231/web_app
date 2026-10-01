# Teacher round 1 — lesson-tf-g5

Saved by the Lead Dev from the Teacher's reply (condensed; fixes verbatim).

**Method.** The Teacher fetched developer.hashicorp.com page text with curl, stripped it in Python and searched it. No WebFetch was used and no files were written. 19 quotes were checked:
- 17 were exact substrings.
- 2 (rows 29 and 72) failed a mechanical match only because the stripper added spaces around link and code tags. On inspection the wording is identical.
- No row was wrong, over-trimmed or unsupported. Row 41 ("mutually exclusive") is thin but true.

## Findings
- **TEACHER-Lg5-001 (medium, 5b).** "the methods 4c covered (`-var`, `.tfvars` files, `TF_VAR_` names)" is false: 4c covers only `TF_VAR_` and the prompt. Fix: "`TF_VAR_` names were covered in 4c; `-var` and `.tfvars` files are the other methods in that list."
- **TEACHER-Lg5-002 (medium, 5b).** "cannot collide with the arguments a `module` block itself understands" is wrong, because the reserved list includes `lifecycle` and `locals`. Fix: "A variable cannot use any of these reserved names: ...". Drop the gloss and keep the row-27 quote.
- **TEACHER-Lg5-003 (medium, 5d against 5c).** "can move to a newer release the next time Terraform installs it" appears to contradict 5c's "init will not change already-installed modules". Fix: add "That happens on a fresh install (a new clone with no `.terraform`, or after `init -upgrade` / `get -update`), not on a repeat `init` of an installed module."
- **TEACHER-Lg5-004 (low, 5d Git bullet).** "Pin with a tag, branch or commit" is wrong because a branch moves. Fix: "Select a revision with `?ref=`: a tag or commit SHA fixes it, a branch name still moves."
- **TEACHER-Lg5-005 (low, 5a and intro).** "label" and "child module" are used before they are defined. Fix: add to the intro "A module is a folder of `.tf` files; the directory you run Terraform in is the root module, and any module it calls is a child."
- **TEACHER-Lg5-006 (low, planning).** Some facts repeat across objectives. Assign ownership when questions are written:
  - 5b: `module.<name>.<output>` and "child must declare an output".
  - 5c: the output shape (map or list), and `init -upgrade`.
  - 5d: the lock file, the exact pin, and registry-only `version`.
- **TEACHER-Lg5-007 (low, 5c).** The "rule for version control" lead-in introduces a location, not a rule. Fix: "The docs say where they land: ... And the rule: ...".

**Exam tips:** all four are accurate and add no new facts. **Contrasts:** all present. **Against tf-g4 §4c:** consistent.

## Three facts per objective
All four objectives are supportable. 5b is the thinnest (it has spares in name uniqueness and reserved names), and 5c and 5d are ample. The writer's plan is sound, given the ownership in TEACHER-Lg5-006.

Lesson tf-g5: not yet (fix 001–003; 004–007 may ride along) · Overall: concerns
