# HANDOFF: Q1 lesson-first content rewrite (as of 2026-10-01)

Read this first, then `AGENTS.md`, then `reports/fix-loop-r2/q1/RULES.md`.

## What this work is

The SAA-C03 and Terraform 004 workbook has 22 lessons, each with a set of drill questions. The old lessons were boilerplate and the old questions were template placeholders ("Which action is the right fit for this requirement: …"). We are rewriting **one task at a time, lesson first**:
1. Write the lesson. 2. Review it. 3. Fix it. 4. Write the questions. 5. Review the questions. 6. Fix them. 7. Close the task.

Roles are in `AGENTS.md`: **Lead Dev** is the only role that writes files, **the Teacher** reviews and writes none (Lead Dev saves its reports), and a **technical reviewer** and a **Student** also check the work.

**Status: 21 of 22 tasks closed (tf-g7 closed 2026-10-01). tf-g8 is in flight: lesson fixed, 20 questions written, Lead Dev pre-check done, round 2 running.** D6/ISS-080 closed and CR-0018 done. The DB is at baseline (`930f0e72…`). **After tf-g7 and tf-g8: the final sitting (date sweep, register reconciliation, CR-0019, CR-0021, D6-FU, LD-Qg7-002, browser smoke test).**

The plan in force is `.cursor/plans/q1_remaining_budget_plan_20260926.plan.md` (see its Amendment 11 for the current rules and what is left), under `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` Amendment 3.

## Where tf-g7 and tf-g8 stand (resume here; updated 2026-10-01)

The two tasks ran in parallel, one writer each (3 subagents allowed at once). **tf-g7 is closed; resume at the tf-g8 column.**

| Step | tf-g7 (maintain infrastructure, 9 Qs) | tf-g8 (HCP Terraform, 20 Qs) |
|---|---|---|
| Lesson written | Done `a6aee0c`: 2,442 words, 104 claim rows; builds on 6d | Done `c1a80ac`: 4 objectives, 4,495 words, 219 claim rows |
| Round 1 review | Done. Tech: approve (`c1a80ac`). Teacher: not yet, 2 medium (`TF_LOG_PATH`, lineage/serial) (`451a144`); fact ownership in `lesson-tf-g7-TEACHER.md` | Done. Both not yet, 2 medium each, matching: hard-mandatory override and execution-mode defaults (`ff2af38`, `9665ee8`). Teacher set fact ownership for all 20 Qs in `lesson-tf-g8-TEACHER.md` |
| Lesson fix pass | Done `9372747`: 118 claim rows; `TF_LOG_PATH` now teaches only what every page agrees on | Done: most fixes came in the user's `53f1beb`; the writer re-checked all findings and added rows 220–234 (AWS-Lg8-010 optional, not applied) |
| Questions written | Done `9372747`: 9 questions | Done: 20 questions (`q-tf-004-8a…8d-*`, `q-tf-004-8-extra-00…07-mc`); `questions-tf-g8-impl.md` |
| Lead Dev pre-check | Done `9372747` (`questions-tf-g7-leaddev-precheck.md`): whole chain PASS, g7 TERMS added, LD-Qg7-001 (5 stems with no question) fixed | Done (`questions-tf-g8-leaddev-precheck.md`): whole chain PASS; LD-Qg8-001 (8b-mc Read distractor rests on the role ladder) and LD-Qg8-002 (proposed TERMS) go to round 2 |
| Round 2 | Done. Both not yet (`92bafd8`, `71951bf`): AWS-Qg7-001–005, TEACHER-Qg7-001–007. Fix pass `1b16cf3` (output-page rows 119–120 added; 005 accepted). Round 2b: **both close** (`7f26131`, `abd3a08`) | **Running** (fresh tech and Teacher reviewers) |
| Student, then close | **Closed 2026-10-01**: Student 9/9 fair; 2 stems counted keyword-guessable, ruled structural by Lead Dev and Teacher (`questions-tf-g7-STUDENT.md`) | — |

**`53f1beb` (2026-09-30, the user's own commit):** adds the citation `cite-tf-g8-projects-manage` and applies most of the round 1 lesson fixes (hard-mandatory override, layered execution-mode defaults, the locking split, Stacks gloss). It was made outside the writer/review pipeline. The writer kept every span of it (diff-checked by the Lead Dev) and added claim row 228 for the new citation; round 2 reviews it as part of the lesson fix pass. Do not add a `Co-Authored-By:` trailer to it.

## tf-g5 and tf-g6 closed (2026-09-30)

The two tasks ran in parallel, one writer each.

| Step | tf-g5 (modules, 12 Qs) | tf-g6 (state, 12 Qs) |
|---|---|---|
| Lesson written | Done `2d5469d`: 2,399 words, 83 claim rows, 15 cites | Done `a7cd16f`: 2,684 words, 120 claim rows, 25 cites |
| Lead Dev pre-check | Done; lesson-only checks PASS (question lines fail only on the 12 placeholders) | Done; same. Cross-references to g2, g3 and g4 checked with a regex and true |
| Round 1 review | Done. Tech: approve, 2 medium + 6 low (`lesson-tf-g5-AWS.md`). Teacher: not yet, 3 medium + 4 low (`lesson-tf-g5-TEACHER.md`) | Done. Tech: approve, 1 medium + 3 low. Teacher: not yet, 4 medium + 4 low (`removed` nesting, import contrast, `moved` vs `state mv`, split 6d with `####`). TEACHER-Lg6-007 logged as CR-0021 against g4 |
| Lesson fix pass | Done `29230f0`: all 15 findings applied, 87 claim rows | Done `23ceea2`: all findings applied, 136 rows; 6d split with `####`; 5 unsupported proposed sentences dropped |
| Questions written | Done `f97c818`: pre-check findings fixed, audit PASS. `./` kept in 2 questions by Lead Dev decision. LD-Qg5-005 (a pair tell in 5c-mc2) is left to round 2 | Done (same writer; fact ownership from `lesson-tf-g6-TEACHER.md` was binding) |
| Round 2 (lesson findings Gone, plus questions) | **Closed** `6f1b81b`: round 2 fix pass `d688f95` (incl. a lesson 5c sentence and LD-Qg5-006 parallel form); tech and Teacher round 2b both close | Done: all lesson findings Gone. Questions not yet: 6d-mc2 refutation untaught (AWS-Qg6-001, TEACHER-Qg6-001; the import overview page has "To import multiple resources, use the import block", which the writer re-verifies and adds), 6a-mc2 untaught locking claim, plus rationale wording. Fix pass done `7e68d75` (the import-overview sentence verified and added as rows 137–140). Round 2b: **both close** (`f924a10`). Teacher misread 006 as unfixed; the Lead Dev verified it Gone |
| Student, then close | **Closed 2026-09-30** `65d51ff`: Student 12/12, 0 keyword-guessable | **Closed 2026-09-30**: Student 12/12; distractor-only justification clauses and 1 echo fixed |

**Carry forward.**
- **Safeguard stop (2026-10-01):** a Student prompt that asked the agent to write its answers "in your reasoning" was stopped by an API safeguard (`reasoning_extraction`). Ask the Student to save its answers to a scratchpad file with Write before opening the key instead.
- **Cloud session:** `backend/db.sqlite3` is not tracked, so it does not exist in a fresh cloud clone and `db_fingerprint.py` cannot run there. Nothing in a text-packet run touches it; check the fingerprint on the local machine.
- **tf-g5 fact ownership (TEACHER-Lg5-006), for the question writer:** 5b owns `module.<name>.<output>` and "child must declare an output"; 5c owns the output shape and `init -upgrade`; 5d owns the lock file, the exact pin and registry-only `version`.
- **tf-g5 `version` Warning:** the Lead Dev's "version on a non-registry source errors" came from memory and is **not doc-backed**. Use the reviewer's wording, which makes no claim about the outcome.
- **tf-g6 `removed` block:** the docs page contradicts itself (the intro says infrastructure is unchanged; the lifecycle section says destroy is the default). The technical reviewer rules on it in round 1.
- **tf-g6:** the S3 `use_lockfile` default and the DynamoDB-locking deprecation must be stated exactly as the page states them.
- **`distractor_type_audit` TERMS** gained g5 constructs at `23ceea2`. A bare `./` path is not matchable, so count it by hand. g6 constructs were added at `60cbddc` (24 terms). g7 constructs were added at `9372747`; bare `TF_LOG` and `TRACE` were left out as 7c's own subject vocabulary. tf-g8 will need its own terms in its pre-check.
- **New tell found by the Student in tf-g6:** "as …"/"because …" justification clauses on distractors only, which let a reader spot the keys by form. **Check for this in every future pre-check.**
- **Both:** if a fresh session resumes, start new agents and hand them the impl and review reports. Session agent ids do not carry over.

## tf-g4 closed (2026-09-28)

Both reviewers close/approve, Student 24/24 (0 keyword-guessable, 10 structural). It took rounds 2, 2b and 2c. Reports: `lesson-tf-g4-AWS.md` (rounds 1–2c), `questions-tf-g4-TEACHER.md` (2–2c), `questions-tf-g4-leaddev-precheck.md`, `questions-tf-g4-fixspec.md`, `questions-tf-g4-STUDENT.md`.

**What this task taught, which should go into the next pre-check:**
- **Letter references in rationales, shifted by a key-balance reorder.** 10 of 24 rationales named choices by letter, and after the reorder two of them called a correct key "wrong". No script checks for this; `q1_batch_check` should (a script change, so it needs a plan). Until then, grep every rationale for a lone `[a-e]` followed by "is"/"misstates"/"reverses", and watch for false hits like "account B invoke".
- **Check that a distractor is actually wrong in practice, not only by the doc's wording.** `sort()` on a set returns a list, so "sort it first" was a working answer.
- **Version-sensitive behaviour.** The `nonsensitive()` behaviour on an unmarked value flipped after v1.5. Pinned doc pages (`/v1.5.x/`) show the history.
- **Reviewer replacement proposals repeat the defect classes.** Of about 12 proposed replacements, 6 were rejected: they were untaught, version-sensitive, possibly true, or a true/false pair that points at the key. Put the proposals through the same two-question test.
- **A fix can break an MR join.** A replacement distractor must answer one of the stem's stated needs.

## Shortest-is-key reopen (closed 2026-09-29)

Plan: `.cursor/plans/q1_shortest_key_reopen_20260929.plan.md`. Reports: `reopen-shortest-key-{impl,review,STUDENT}.md`.
- 11 keys were rebalanced by wording only; shortest-is-key went from 57/48/45% to 29/29/18%.
- `q1_batch_check`'s letter check was rewritten, with a self-test in `scripts/test_q1_letter.py`.
- **`key_text_diff` is the wrong proof when keys are reworded on purpose.** Compare `correctAnswerIds`, the stem and the choice order field by field instead.

**Key-length rank: open, for the user.** **New evidence (Student, reopen run):** "never pick the longest" was right 15 of 15 times, against about 75% by chance. 13 of 16 MC keys are neither the longest nor the shortest option. The Teacher reads this as partly a real cross-task tell; the technical reviewer reads it as the arithmetic of the two caps. Neither blocks.

## Decisions taken by the user on 2026-09-28

1. **Shortest-is-key: reopen `4-3`, `4-1` and `1-3`** (~50 MC questions) and rebalance them through the full review pipeline. `3-1` and `3-5` stay closed with their figures recorded. Apply the 35% shortest cap to all new work.
2. **D6 / ISS-080: do it next sitting**, before g5/g6.
3. **Date literal: one sweep at the end.** Keep `2026-09-26` until tf-g8 closes, then set one final date across the corpus in a single commit and update `q1_batch_check` to match.

Background to those decisions follows.

1. **shortest-is-key in five closed tasks.** `q1_batch_check` now checks both length tells. Six tasks exceed the 35% cap on *shortest*: `4-3` 57% (8/14), `3-1` 60% (only 5 MC, noisy), `4-1` 48%, `1-3` 45%, `3-5` 36%, and `tf-g4` which was fixed in flight. On task 4.3 a reader who always picks the shortest option scores 57% against 25% by chance. This is **not** a metric artifact — it is a real tell in shipped content, caused by a rule that capped only one direction. Options: fix forward from g5 and record the closed figures, or reopen `4-3`, `4-1` and `1-3` (~50 MC questions). Lead Dev leans to fixing forward; every one of those tasks passed a blind Student run.
2. **`D6 / ISS-080`** — dated pricing snapshot and templated design exercises. The user chose "fix" on 2026-09-25 and it was never started. This is accepted work sitting idle, not a stale finding.
3. **Date drift.** Every citation and `reviewedOn` says `2026-09-26` because `q1_batch_check` enforces that literal, including tasks written on the 27th. Better as one deliberate sweep at the end than a corpus split across two dates.

## User decisions in force

- **Models:** the plan's `gpt-5.3-codex` and `composer-2.5-fast` do not exist in this harness (the list is sonnet / opus / haiku / fable). Per the standing memory rule **all subagents run Sonnet**; the main session is Opus. Never pass `inherit`.
  - Consequence to keep restating: the Student check runs on a *stronger* model than the one that closed tasks 3.1–4.2, so a high score is weaker evidence than it was there. The guessable-stem counts do not depend on the model being weak, which is why they matter more.
- **Agent resume:** ids from earlier harnesses are not resumable, and ids below are scoped to the session that created them. Start fresh reviewers and hand them the round-1 reports; never rewrite content to recover.
- **Concurrency:** at most **3 subagents at a time**. The user asked for a third writer on 2026-09-30, which matches the standing memory rule (max 3); it was 2 before. **Pacing:** about **3 tasks per sitting**, then stop and wait for GO.
- **Student check:** text packet per task. One browser smoke test at the very end.
- **Closure rule:** an item closes only when its **reporter and a second role** both mark it Gone.
- **Stem-paraphrase rule (2026-09-27):** applies from task 4.4 onward; closed tasks are not reopened.
- **Register reconciliation (2026-09-27):** fold into the final sitting — detail in the final-sitting list below.

## Hard rules

- Agents never call AWS, never provision anything, never run credentialed terraform.
- The MCP exposes `ExecuteTerraformCommand` / `ExecuteTerragruntCommand`. **Never call them.** No `terraform` run of any kind, including `fmt` and `validate` — lessons are written *about* these commands, verified from docs.
- No servers, no Playwright, no scripted POSTs. Never click Reset or Import.
- Subagents run no git. Lead Dev commits after every step.
- If anything submits drills, restore the DB and check `scripts/db_fingerprint.py backend/db.sqlite3` prints sha `930f0e72…`. The text-packet Student check does not touch the DB.
- Commit messages end with a `Co-Authored-By:` line naming the model. **Do not add it to a commit of the user's own work** — their README rewrite is committed under their authorship at `0161bb9` with no trailer.

## Tools

**Local Windows machine only.** The paths below (`backend\.venv\Scripts\python.exe`, `../eval-baseline/db.sqlite3.bak`) and the `mcp__MCP_DOCKER__*` AWS docs tools exist on the user's PC. A Claude Code cloud session (Linux, fresh clone) has none of them: no venv, no DB backup, no MCP_DOCKER tools, and a shallow git history (older commits such as `0161bb9` are not in the clone). In a cloud session, do docs-only work and leave DB restores, the Django tests and Student browser checks for the local machine.

- **AWS docs:** `mcp__MCP_DOCKER__search_documentation`, `read_documentation`, `read_sections` — load all three in one ToolSearch `select:` call. Prefer user-guide pages.
- **Terraform docs:** `developer.hashicorp.com`. **Read the rendered page text, not WebFetch.** WebFetch answers through a summarising model that can paraphrase a quote into something plausible, which is the most likely cause of g3's fabricated quote. The g4 writer switched method and 56 of its 75 quotes were then verified verbatim by a reviewer with no fabrication.
- **Python:** `backend\.venv\Scripts\python.exe`. **JSON:** `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, utf-8.

### The check suite — run the whole chain against the whole file after any fix

| Script | What it does, and what it cannot see |
|---|---|
| `content_lint.py` | Must PASS. |
| `q1_batch_check.py <task>` | Lesson format, drillIds, tell words, retired names, 6-word openings, MC/MR key positions, MR key sets, **and both key-length tells** (longest and shortest, 35% each). Task `1-1` FAILs because its glob also matches two demo `q-a0-*` files; pre-existing. |
| `distractor_type_audit.py <task>` | Non-key choices against a curated `TERMS` list, 15% cap. Matches plural suffixes. **Bare subject vocabulary is deliberately excluded** — not "provider" in a providers lesson, not bare command names, not "resource"/"data"/"variable" — because a term the lesson is *about* is not a reused distractor type. Add new named constructs per task. |
| `stem_echo_check.py <task>` | **A gate from tf-g1 onward.** Flags tokens in the stem and the key but in no distractor. Cannot tell leakage from a structural scenario reference, so a reviewer classifies each and the Lead Dev records structural ones in `stem-echo-waivers.json` with a citation. **The waiver file is still empty; keep it that way where a reword will do.** |
| `claim_prose_check.py <task>` | Claim-table numbers absent from prose, and **quotes over 20 words**. Blind to non-numeric claim rows — the single biggest gap in the suite. |
| `key_text_diff.py <task> <rev>` | Confirms which option *texts* are correct across a revision. **Give it a meaningful baseline:** diffing against a commit that predates the questions reports every question as changed. |
| `make_student_packet.py <task> <n>` | Pass n = the task's full question count. |
| `db_fingerprint.py backend/db.sqlite3` | Read-only. |

**DB restore** (only if needed, from `web_app`):

```
backend/.venv/Scripts/python.exe -c "import sqlite3; s=sqlite3.connect('file:../eval-baseline/db.sqlite3.bak?mode=ro',uri=True); d=sqlite3.connect('backend/db.sqlite3'); s.backup(d); d.close(); s.close()"
```

**Two cautions about the suite itself.** Three scripts had a filename glob that silently matched zero files on Terraform tasks and printed a confident PASS; all are fixed, but check a new script prints how many files it compared. And a substring grep is not proof a term is untaught — `can(` missed a lesson that teaches `` `can` `` in backticks, and the Lead Dev reported a false gap to two reviewers on the strength of it.

## Per-task pipeline

1. **Lesson writer** (new Sonnet agent). Model the prompt on **tf-g4**, the most thoroughly reviewed so far. Require: one `###` per objective ending in `**Exam tip:**`, the standard `### Warnings` section, one `##` title, citations with `accessed: "2026-09-26"`, full `drillIds` (every placeholder lesson has a stale short list), and a claim table with quotes **copy-pasted from a page fetched that turn**.
2. **Lead Dev pre-check:** run the whole chain yourself. Do not trust the writer's summary — one reported "lesson-only lines PASS" while a lesson line was failing.
3. **Commit.** Then round 1: technical reviewer and Teacher in parallel (2-agent cap).
4. **Resume the writer** for fixes, then the questions.
5. **Lead Dev pre-check before round 2:** scripts, then **read every distractor**. No script sees a strawman, a false claim, or a contradiction.
6. **Round 2:** resume both reviewers; each marks its own findings Gone and second-role-checks the other's.
7. **Student:** text packet, Sonnet agent, only the two packet files, all answers committed in writing before opening the key.
8. **Close:** `progress.md`, issue register, DB fingerprint, commit.

## The defect classes that have actually cost time

Ordered by how much trouble each has caused.

- **Real but untaught.** A distractor or rationale resting on a fact that is true and never taught, so a lesson-only reader cannot eliminate it. Four occurrences across g1–g3. Ask "is this real?" and "is the reason it is wrong taught here?" as **two separate questions**.
- **A repair introducing a new defect.** Four in g1/g2 alone, which is why RULES gained the **"After applying a fix"** section: re-run the whole chain against the whole file, re-read the new fragment in isolation, and re-check both distractor properties. Every one of those regressions was something an existing script already caught globally — they were missed by verifying only the changed field.
- **Quote defects**, in three flavours: attached to the wrong claim; scoped wrongly (both too broad and too narrow have occurred); and **fabricated** — text in quotation marks that is not on the page. One fabrication in 45 rows on g3.
- **Caricature distractors.** Nine rejected in g1, two more found by the Student in g2 that the Lead Dev had noticed and not acted on, three in g3. A distractor must be a practice a real team uses **and** wrong for a taught reason.
- **Contradiction inside a lesson**, carried into a key. g3's 3f asserted both directions of the same dependency rule.
- **Duplicate-fact questions.** Task 4.3's worst finding: three questions testing one fact while an objective went untested. Ask the Teacher up front whether every objective supports three distinct questions.
- **Stem/key keyword echo.** Fixing only the key is not enough — check the stem against all choices.
- **Directionality.** `-target` extends to what a resource **depends on**, not to what depends on it. The Lead Dev asserted the opposite and a writer corrected it from the docs.
- **Do not "fix"** the `##` lesson title, the `### Warnings` section, or objective-id headings. All are standard.

## Exactly where things stand

| # | Task | Qs | State |
|---|---|---:|---|
| 0–16 | 1.1–4.4, tf-g1, tf-g2, tf-g3 | 373 | **Closed** (4-3, 4-1, 1-3 reopened and re-closed 2026-09-29 for shortest-is-key) |
| 17 | lesson-tf-g4 | 24 | **Closed** 2026-09-28 |
| 18 | lesson-tf-g5 | 12 | **Closed** 2026-09-30 |
| 19 | lesson-tf-g6 | 12 | **Closed** 2026-09-30 |
| 20 | lesson-tf-g7 | 9 | **Closed** 2026-10-01 |
| 21 | lesson-tf-g8 | 20 | **In flight**: lesson fixed, 20 questions written, Lead Dev pre-check PASS. Round 2 running |

Terraform question files are named `q-tf-004-<group><letter>-*`; every script matches them by the lesson's `objectiveIds`, not by filename.

**Next:** tf-g8 round 2, Student and close. Then the final sitting.

**Final sitting:**
- **date sweep (user decision 3, 2026-09-28):** set one final date across every citation and `reviewedOn` in a single commit, and update the `2026-09-26` literal in `q1_batch_check` to match;
- **CR-0019** (lesson 3.5 and four 3.5 questions present AWS Glue for Ray as current) and **CR-0021** (tf-g4 Warnings cite guidance tf-g3 does not contain), both in `docs/change-requests.md`; **D6-FU** lesson follow-ups (register row);
- **LD-Qg7-002:** stems with no question in closed tasks tf-g1 (1a-mr, 1b-mr, 1c-mr), tf-g2 (2a-mr, 2b-mr, 2d-mr) and tf-g4 (4a-mc). Not a correctness defect. Decide whether to fix them and whether `q1_batch_check` should flag a stem not ending in "?" (a script change, so it needs a plan);
- **`distractor_type_audit` regression on closed task 1-1 (found 2026-10-01):** the tf-g7 term `identity` (added at `9372747`) also matches IAM "identity" in 1-1, which is 1-1's own subject (6 of 21, 29%). 1-1 passed before `9372747`. `identity` appears in only one tf-g7 question, so removing it (or scoping TERMS per exam) loses nothing; that is a script change for the user to approve. Separately, SAA tasks 1-2, 2-1, 2-2 and 3-1 to 4-1 already FAILed the audit on service names before this session — decide whether the global TERMS list should be split per exam;
- browser Student smoke test, ~10 questions across 3.1 to tf-g8, then restore the DB;
- **reconcile the register (user-approved).** `reports/fix-loop/issue-register.md` lists **53 rows under "Still open"** and the number is not real. Close with a reason: `L1` ("lessons don't teach") is what the rewrite fixed; `N8` (133 rationales naming wrong letters) — those questions were all rewritten; `R6 / ISS-070` already says "folded into the lesson and question rewrites"; `Q1-T2/T3/T4` are pilot-era findings against content that no longer exists. Genuinely live and independent of the rewrite: `FS-R3-001` (header hidden behind an 80px scroll margin), `AWS-R3-002` (GL-14/19/21 subnet lookup returns a tab-joined string, breaking cluster creation), `TEACHER-R3-001/002/003` (lab criteria), `PY-R3-002/003` (scanner), and `D6 / ISS-080`. Leave a true open list;
- close `L1` and `ISS-010`;
- update `docs/status.md`;
- run `python manage.py test workbook`, `scripts\content_lint.py` and `npm run build`.

## Session-scoped agent ids (this session only)

None in flight. Agent ids never carry across sessions; start fresh agents and hand them the reports.

## Optional later

- `q1_batch_check.py 1-1` FAILs because its glob matches two demo `q-a0-*` files.
- `claim_prose_check.py` cannot see non-numeric claim rows, which is why that defect has recurred on four tasks and depends entirely on the Teacher.
- The README at `0161bb9` is the user's own work, committed under their authorship.
