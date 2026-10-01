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

---

# Teacher round 2 — tf-g5 (f97c818)

Saved by the Lead Dev from the Teacher's reply (condensed; fixes verbatim).

## (a) Round-1 Teacher findings
- **Gone:** TEACHER-Lg5-001, 002, 003, 004, 005 and 007.
- **006 (fact ownership): followed.** The one exception is acceptable: "init after a source edit" sits in 5a-mr, and 5a is its first owner.

## (b) Second-role check
AWS-Lg5-001 to 008 are all applied and correct, so all are Gone. 007 needed no lesson change.

## (c) Questions
- **Three facts per objective:** passes everywhere, with no duplicate fact.
  - 5a: shape, `ref`, and archive plus re-init.
  - 5b: arguments, locals, outputs.
  - 5c: shape, location, update.
  - 5d: registry-only, `~>`, lock file.
- **Distractors:** real, and refuted by lesson sentences, except as noted below.
- **New 5a-mc2 "Append `//v2.3.0`":** accepted. It is real and taught, and it removes the 5d duplicate.
- **5a-mr "only after `.terraform` is deleted and recreated":** accepted. It is real, and the init sentence refutes it.
- **Echo and strawmen:** no stem/key echo defects. The only caricature is in 5c-mc.

## (d) Numbers
5d-mc2: 1.0.10 is correct. The other figures are consistent with the lesson.

## (e) LD-Qg5-005 ruling and findings
- **TEACHER-Qg5-001 (medium, 5c-mc2): confirmed, and worse than a pair.** Only the key says "kept out of version control"; the other three say "committed". The fix:
  - choice b becomes "In a `modules` folder beside the root `.tf` files, kept out of version control and recreated by `init`";
  - choice d becomes "In the user's home directory, shared by every project, so there is nothing to commit";
  - a and c stay;
  - the rationale is updated to name why b and d are wrong by location. The key rests on "a .terraform subdirectory of the current working directory".
- **TEACHER-Qg5-002 (low, 5c-mr).** The stem gives away the plain-`init` option.
  - New stem: "... A registry module has since published a newer release that its `version` constraint allows, and the team wants the installed copies refreshed. Which two actions do that?"
  - Rationale: "modules are installed and updated by `init` and `get`", replacing an untaught claim about apply.
- **TEACHER-Qg5-003 (low, 5c-mc, optional).** Replace the caricature distractor ("map keyed by output name with list values") with "A set of the two site keys, with the outputs readable only through each key".
- **TEACHER-Qg5-004 (low, 5b-mc).** No change needed. An optional lesson sentence: "`-var`, `.tfvars` files and `TF_VAR_` names set root module variables; a child receives its inputs as arguments."

Task tf-g5: not yet (fix 001; 002–004 may ride along) · Overall: concerns

---

# Teacher round 2b — tf-g5 (d688f95)

Saved by the Lead Dev (condensed).

- **TEACHER-Qg5-001: Gone.** The commit clause now varies across 5c-mc2's options, so it no longer picks the key; the location does, and the lesson quotes it.
- **TEACHER-Qg5-002: Gone.** The 5c-mr stem no longer refutes plain `init`.
- **TEACHER-Qg5-003: Gone.** The writer used the AWS replacement ("A set of objects ... no keys"). It is real (`for_each` takes a set) and is refuted by "a map of objects", which makes it better than the Teacher's own alternative.
- **Second-role check on AWS-Qg5-001 to 008:** all applied correctly.
  - 008's new 5d-mr distractor tests a different fact, refuted in 5c.
  - 006's new lesson 5c sentence is sound and well placed, and asserts no more than its two quotes.
- **LD-Qg5-006: Gone.** The keys are now parallel "Running …" options.
- **Changed choices:** all real, all refuted by a lesson sentence, no giveaways.

Task tf-g5: close · Overall: approve
