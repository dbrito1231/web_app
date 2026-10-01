# Teacher round 1 — lesson-tf-g6

Saved by the Lead Dev from the Teacher's reply (condensed; fixes verbatim).

## Method
- All 120 claim-table quotes were fetched with curl, stripped in Python and checked: 120 of 120 are verbatim, none over-trimmed or failed.
- 11 key rows were also read in context:
  - the 1.7 floor;
  - the `removed` default (destroy; `destroy` is the only lifecycle argument; `destroy = false` keeps the object);
  - the `init` options;
  - the `import` command;
  - `state mv` (same type only).
- The cross-references to g2, g3 and g4 were checked with a regex. No WebFetch was used and no files were written.

## Findings
- **TEACHER-Lg6-001 (medium, 6d `removed`).** Show the nesting. After "Set destroy to false ...", add "In configuration that is `removed { from = <address> lifecycle { destroy = false } }`." Use "`lifecycle { destroy = false }`" in the discriminator and the exam tip.
- **TEACHER-Lg6-002 (medium, 6d import).** The block and the command are not contrasted. After `terraform import ADDRESS ID`, add "Before you run it you must write the resource block yourself, and it changes state at once with no plan preview and cannot generate configuration; the `import` block can be reviewed in `plan` and can generate configuration with `-generate-config-out`." Also add the command page's "To import multiple resources, use the import block."
- **TEACHER-Lg6-003 (medium, 6d `moved` vs `state mv`).** The reason to prefer the block is missing. Add "`state mv` changes state immediately and is a legacy command; a `moved` block lives in the configuration, appears in the plan, and records the rename for others who use the module". Quote the refactor page for it, or drop the claim if no row backs it.
- **TEACHER-Lg6-004 (medium, 6d density).** The section is 878 words over four topics. Split it with `####` headings: "Drift and refresh-only", "Importing", "Renaming and forgetting", "Inspecting state". Also fix the garbled opening (`or "drift," from`): the docs call the gap "drift", and manual changes leave state out of sync with real infrastructure.
- **TEACHER-Lg6-005 (low, overlap with g3 §3d).** Open the refresh paragraph with "3d introduced `-refresh-only`; here is how it handles drift."
- **TEACHER-Lg6-006 (low, undefined terms).** In 6a, gloss "workspace" ("one named copy of state for a configuration; the default workspace is used unless you create others"), or keep `workspace_dir` to one clause and out of the tip. In 6b, gloss "HCP Terraform" at first use as "HashiCorp's hosted service".
- **TEACHER-Lg6-007 (low, a g4 overclaim, not g6).** g4's Warnings cite "group 3's state-security guidance", which g3 does not contain. Log a change request against g4. No g6 change is needed.
- **TEACHER-Lg6-008 (low).** The intro's references to g2 and g3 are accurate. No fix needed.

## Contrasts and exam tips
- **Contrasts present:** local vs remote; `-lock-timeout`, `-lock=false` and `force-unlock`; `backend` vs `cloud`; `-migrate-state` vs `-reconfigure`; refresh-only vs a normal apply; `removed` vs `state rm`.
- **Contrasts thin:** the import forms (002) and `moved` vs `state mv` (003).
- **Exam tips:** accurate. The 6d tip needs the `lifecycle` fix.

## Three facts per objective, with ownership
- **6a, thin but supportable.**
  - mc: no `backend` block means local, with `path` and the `.backup` file.
  - mc2: what it lacks, meaning loss, latest-state and single-machine locking.
  - mr: the legacy flags and migrating back.
  - Sharing belongs to 6c.
- **6b, ample.**
  - mc: automatic and backend-dependent locking.
  - mc2: `-lock-timeout` vs `-lock=false`.
  - mr: `force-unlock` and the S3 `use_lockfile` vs DynamoDB split.
  - The S3 facts belong to the mr only.
- **6c, ample.**
  - mc: block limits and `backend` vs `cloud`.
  - mc2: partial configuration, `-backend-config` and credentials. The `.terraform` credentials fact belongs here only.
  - mr: `-migrate-state`, `-reconfigure` and `-force-copy`.
- **6d, ample after 001–004.**
  - mc: refresh-only vs a normal apply, and the `refresh` deprecation.
  - mc2: `import` block vs command.
  - mr: rename vs forget (`moved` and `state mv` vs `removed` and `state rm`), and no hand edits.
  - The one-to-one rule appears in one question at most. `state list`/`show` are spare mr options only.

Lesson tf-g6: not yet (fix 001–004; 005–008 may ride along) · Overall: concerns

---

# Teacher round 2 — tf-g6 (60cbddc)

Saved by the Lead Dev from the Teacher's reply (condensed; fixes verbatim).

## (a) Own round-1 findings
- **Gone:** TEACHER-Lg6-001, 003, 004, 005 and 006. 007 is Gone for g6 (it is CR-0021 against g4), and 008 needed no change.
- **002 (import block vs command): partly Gone.** The lesson does not teach that the command imports one resource per run.
  - The sentence the writer dropped, "To import multiple resources, use the import block.", **is** on `https://developer.hashicorp.com/terraform/cli/import`, the overview page. The writer had checked the command page.
  - **Optional lesson addition:** after "…at the given ADDRESS.", add: The command overview page says "To import multiple resources, use the import block." Add a claim row for it.

## (b) Second-role check
- **AWS-Lg6-001, 002 and 004:** Gone.
- **AWS-Lg6-003:** Gone, with one nit (TEACHER-Qg6-006).

## (c) Findings
- **TEACHER-Qg6-001 (medium, 6d-mc2).** The refutation of distractor d is only partly taught. There are three fixes:
  - Fix 1, rationale: replace the last sentence with "The `terraform import ADDRESS ID` command names one address and one ID per invocation, and the docs steer readers to the `import` block when importing several resources and reviewing the import in plan." Do not claim "no preview".
  - Fix 2, lesson (recommended): add the verified sentence from (a).
  - Fix 3, distractor d: "Run `terraform import` with the resource address and bucket ID for each bucket, then run `terraform plan` to confirm".
  - Also trim the distractor-a rationale to "Resource blocks alone do not import anything; importing needs an `import` block or the command."
- **TEACHER-Qg6-002 (medium, 6a-mc2).** "Version control does not offer state locking or secure access control" is untaught.
  - Choice d: "There is none: committing the state file to the shared repository gives the pair a shared, versioned copy".
  - Rationale: "Storing state in version control can lead to data loss or exposure of secrets, so committing the file is not a fix."
- **TEACHER-Qg6-003 (low, 6b-mc rationale).** End the sentence at "because locking covers all operations that could write state." This drops the untaught claim about the flags on the `state` subcommands.
- **TEACHER-Qg6-004 (low, 6d-mr choice e).** The hand-edit option is close to a manual-action strawman, but it is taught. Acceptable; keep it.
- **TEACHER-Qg6-005 (low).** The `.terraform`-commit fact is a distractor in both 6a-mc and 6c-mc2. Acceptable at two uses; do not add a third.
- **TEACHER-Qg6-006 (low, lesson).** The quote "Instead, use the terraform state mv CLI command" has no antecedent. Write "(on versions older than 1.1 the page says "Instead, use the terraform state mv CLI command")", after checking the page's context.

**Fact ownership** was followed. There are no self-justifying keys, no repeated facts beyond 005, and no echo. Both two-need MR stems are fair.

## (d) Numbers
`0s` and `1.5` are verbatim and taught. 1.1, 1.7 and 0.15.4 do not appear in any question.

## (e) LD-Qg6-002
Fair, and the key is unambiguous. The refutation needs Fixes 1 and 3, and Fix 2 makes it clean.

Task tf-g6: not yet · Overall: concerns

---

# Teacher round 2b — tf-g6 (7e68d75)

Saved by the Lead Dev (condensed).

- **The Teacher's own question findings:** TEACHER-Qg6-001, 002 and 003 are Gone.
  - 001: the lesson now carries the import-overview sentence and the usage line. Distractor d has "then run `terraform plan`", so the keyword tell is gone. The rationale claims only taught facts.
- **Second-role check:** AWS-Qg6-001 to 005 are all Gone. Dropping the untaught "locking and access control" clause was right.
- **Fairness:** every changed choice is real and refuted by a lesson sentence. The new sentences come from verified rows 137–140.
- **TEACHER-Qg6-006:** the Teacher reported it "still not fixed", which was **incorrect**. The Lead Dev checked the lesson at 7e68d75. It reads `Moved blocks need Terraform 1.1 or later (...); (on versions older than 1.1 the page says "Instead, use the terraform state mv CLI command")`, which is exactly the Teacher's requested fix. **006 is Gone.** The Teacher marked it non-blocking either way.

Task tf-g6: close · Overall: approve
