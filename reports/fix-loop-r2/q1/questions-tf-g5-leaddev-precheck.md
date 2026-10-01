# Lead Dev pre-check before round 2 — tf-g5 questions

**Chain results:**
- `content_lint` PASS.
- `q1_batch_check tf-g5` PASS: longest-is-key 12%, shortest-is-key 25%, MC key positions a2/b2/c2/d2, MR key slots spread.
- `stem_echo_check` 0 echoes.
- `test_q1_letter` PASS. No rationale uses a letter reference.
- `claim_prose_check` PASS.

**The distractor audit was blind for this task.** Its `TERMS` list had nothing for g5's constructs; the writer reported this. The Lead Dev added `TF_VAR`, `-var`, `tfvars`, `?ref`, `version =`, `lock file`, `plan time`, `init -upgrade` and `get -update`. tf-g3 and tf-g4 still PASS with the new terms. A bare `./` path cannot be matched by the script's word guard, so that type is counted by hand below.

All 12 questions and every choice were read. Keys and rationales are correct, and each distractor is a real option, wrong for a taught reason. The writer's four "thinnest" distractors hold up.

## Findings
- **LD-Qg5-001 (medium): the misconception "modules are fetched or read at plan time" is reused as a distractor in three questions.**
  - 5a-mr d: "`terraform plan` fetches the newer file by itself".
  - 5c-mc2 d: "Nowhere on disk, because Terraform reads each source remotely again at plan time".
  - 5c-mr b and d: plan and apply.
  - 5c owns install behaviour (TEACHER-Lg5-006), so keep it in 5c-mr. Replace the distractors in 5a-mr and 5c-mc2 with different real misconceptions that the lesson refutes.
- **LD-Qg5-002 (medium): a local `./` path is a distractor in three questions** (5a-mc c, 5a-mr c, 5d-mc a), over the 15% cap of one question for 12.
  - Keep 5a-mc, which owns source shapes.
  - Keep 5d-mc: "local paths do not support `version`" is a 5d fact.
  - Replace 5a-mr c.
- **LD-Qg5-003 (medium): duplicate fact.** 5a-mc2 a ("Add a `version = "2.3.0"` argument") tests "`version` is registry-only", which is 5d-mc's key fact and owned by 5d. Replace it with a 5a-owned misconception about selecting a Git revision. It also brings `version =` under the cap.
- **LD-Qg5-004 (low): 5d-mr d** ("A range such as `version = "~> 6.0"` keeps the first release installed on every later run"). It is false for CI only because each run is a fresh install. 5c teaches that a plain repeat `init` does not change an installed module. Add "fresh" to the stem ("every CI run, each starting from a fresh clone") so the reason is determinate.

## After the pre-check fix pass
All four findings were applied. `distractor_type_audit` passes: every type is in at most 1 of 12 questions.
- **Lead Dev exception, recorded:** a bare `./` local path stays a distractor in 5a-mc (5a owns source shapes) and 5d-mc (5d owns "local paths do not support `version`"). That is 2 of 12, kept deliberately because each tests a different owned fact.
- **New issue for round 2 (LD-Qg5-005):** 5c-mc2's replacement distractor ("`.terraform` subdirectory, committed so teammates skip the download") pairs with the key ("`.terraform` subdirectory ... kept out of version control"). The two differ only in commit versus don't-commit, which points at the key; the same true/false-pair pattern was rejected in D6. The reviewers should rule on it and propose a replacement.

## After the round 2 fix pass
- **LD-Qg5-006 (low, fixed by the Lead Dev):** in 5c-mr the three distractors began "Running …" and the two keys were bare commands, so the shape alone picked the keys. Both keys now read "Running `terraform init -upgrade`" and "Running `terraform get -update`". This is wording only; the key ids are unchanged. The batch check and echo check still pass. It goes to the round 2 confirmation.
