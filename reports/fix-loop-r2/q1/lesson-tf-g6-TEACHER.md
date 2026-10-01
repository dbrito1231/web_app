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
