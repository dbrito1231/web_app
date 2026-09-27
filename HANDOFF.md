# HANDOFF: Q1 lesson-first content rewrite (as of 2026-09-27, sitting 4 finished)

Read this first, then `AGENTS.md`, then `reports/fix-loop-r2/q1/RULES.md`.

## What this work is

The SAA-C03 and Terraform 004 workbook has 22 lessons, and each one comes with a set of drill questions. The old lessons were boilerplate and the old questions were template placeholders ("Which action is the right fit for this requirement: …"). We are rewriting **one task at a time, lesson first**:
1. Write the lesson.
2. Review it.
3. Fix it.
4. Write the questions.
5. Review the questions.
6. Fix them.
7. Close the task.

The user must approve each change under the `AGENTS.md` roles:
- **Lead Dev** is the only role that writes files.
- **The Teacher** reviews but writes no files; Lead Dev saves the Teacher's reports.
- **An AWS reviewer and a Student reviewer** also check the work.

**Status: 14 of 22 tasks closed. Tasks 4.3 and 4.4 both closed in sitting 4.** Nothing is paused mid-task. HEAD is `3a495f8`, the working tree is clean apart from this handoff, the DB is at baseline, and no agents are running.

**Two decisions are waiting on the user** before the Terraform tasks start — see "Open decisions" below. Neither blocks starting g1, but both get cheaper if taken first.

## Plans and records (source of truth)

| File | Purpose |
|---|---|
| `.cursor/plans/q1_remaining_budget_plan_20260926.plan.md` | **Current plan (approved).** Budget-aware workflow, user decisions (§9), model substitution (§10) |
| `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` | Earlier amendments 1–3; question rules originate here |
| `reports/fix-loop-r2/q1/RULES.md` | **Shared rules.** Point every agent prompt here. Now includes the **stem-paraphrase rule** (from task 4.4) |
| `reports/fix-loop-r2/q1/progress.md` | Per-task tracker. Rows 0–13 closed |
| `reports/fix-loop/issue-register.md` | Closed-items table and "Still open" (L1/Q1, ISS-010) |
| `reports/fix-loop-r2/q1/*` | Per-task reports |

## User decisions still in force

- **Models:** the plan's `gpt-5.3-codex` and `composer-2.5-fast` **do not exist in this harness** — the subagent model list is sonnet / opus / haiku / fable. Per the user's standing memory rule, **all subagents run Sonnet**; the main session is Opus. Do not pass `inherit`.
  - Consequence to keep stating: the Student check now runs on a *stronger* model than the one that closed tasks 3.1–4.2, so a high score is weaker evidence than it was there. The guessable-stem count does not depend on the model being weak, which is why it matters more.
- **Agent resume:** agent ids from earlier harnesses are not resumable. Start fresh reviewers and hand them the round-1 reports; never rewrite a lesson or questions from scratch to recover.
- **Concurrency:** at most **2 subagents at a time**.
- **Pacing:** about **3 tasks per sitting**, then stop, report, and wait for GO.
- **Student check:** text packet per task, not the browser. One browser smoke test at the very end.
- **Closure rule:** an item closes only when its **reporter and a second role** both mark it Gone.
- **Deferred:** D6 and the small screen items. PY-R5-001 to 003 are won't-fix.

## Open decisions for the user

1. **Split the Student's guessable-stem question into two numbers.** On 4.4 the Student reported 9 of 23, statistically the same as the 9 of 22 that prompted the rule — but reading them showed two classes: *avoidable leakage* (stem uses the key's own distinctive word; a real defect, 2 found and fixed) and *structural scenario reference* (the key names something the scenario introduced; not a defect and not removable without making keys vaguer). One number mixes them, so it will sit near 9 regardless of quality. The Teacher's exact proposed replacement wording is in this sitting's notes below and in `questions-4-4-TEACHER-recheck.md`; its operative test is **"does the shared term also appear in at least one distractor?"** If yes, not diagnostic.
2. **Tighten `stem_echo_check.py` and make it a gate.** It already implements exactly the Teacher's test. It is currently ADVISORY because it over-flags on generic vocabulary ("availability", "billing", "daily"). Filtering those (for example, dropping tokens that appear in more than a quarter of the task's stems) would let it fail a task instead of only producing a reading list. Pairs with decision 1.

## Hard rules (from AGENTS.md and the user)

- Agents never call AWS, never provision anything, and never run credentialed terraform.
- The `aws-terraform` MCP exposes `ExecuteTerraformCommand` / `ExecuteTerragruntCommand`. **Never call them.**
- No servers, no Playwright, no scripted POSTs. Never click Reset or Import.
- Subagents run no git and no `git stash`. Lead Dev commits after every step.
- If anything submits drills in the app, restore the DB to baseline and check `scripts/db_fingerprint.py backend/db.sqlite3` prints sha `930f0e72…`. The text-packet Student check does not touch the DB.
- Commit messages end with a `Co-Authored-By:` line naming the model you are running as.

## Tools

- **AWS docs:** `mcp__MCP_DOCKER__search_documentation`, `read_documentation`, `read_sections` — load all three in **one** ToolSearch `select:` call. Fall back to WebFetch. Prefer **user-guide** pages; a CLI command reference cannot support a selection-criteria claim.
- **Terraform docs:** WebFetch on developer.hashicorp.com, plus `mcp__MCP_DOCKER__SearchAwsProviderDocs`.
- **Python:** `backend\.venv\Scripts\python.exe`. Lint: `scripts\content_lint.py` must PASS.
- **JSON writes:** `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, utf-8.
- **`scripts/q1_batch_check.py <task>`** — lesson format, `drillIds`, tell words, retired names, 6-word openings, longest-is-key, MC/MR key positions, MR key **sets**, citations. Lesson Snowball WARNs are expected. Task `1-1` FAILs because the glob also matches two demo `q-a0-*` files; pre-existing.
- **`scripts/distractor_type_audit.py <task>`** — non-key choices against a curated service list, 15% cap. **Now matches plural suffixes**; the singular-only guard had hidden "read replicas" at 6/22 and "snapshots" at 4/22 in task 4.3. The leading guard still prevents the old "RDS inside shards/records" bug. Add terms as new tasks introduce them.
  - **Caution:** `TERMS` grows per task, so re-running this on a *closed* task measures it against a list that did not exist then. Nine of the twelve closed tasks now report over cap; this was verified to be pre-existing under the old matcher too, and it counts topic-central services (Glue at 50% in an analytics lesson). **Not a reason to reopen closed tasks.**
- **`scripts/claim_prose_check.py <task>`** — numbers in the claim table vs prose. WARN. Known false positive: the `20` in a date like `2025-06-20`. Blind spot: **non-numeric** claim rows, which only the Teacher catches.
- **`scripts/key_text_diff.py <task> <git-rev>`** — after any choice reorder, confirms the set of correct option texts is unchanged. A deliberate key rewrite will show as a MISMATCH; say so rather than treating it as a regression.
- **`scripts/stem_echo_check.py <task>`** — **new, ADVISORY.** Reports tokens shared by the stem and the key but by no distractor. Over-flags (15 of 22 on 4.3 where the Student found 9), so it is a reading list, not a verdict. See open decision 2.
- **`scripts/make_student_packet.py <task> <n>`** — writes the packet and answers to `%TEMP%\q1-packets`. **Always pass n = the task's total question count.**
- **`scripts/db_fingerprint.py backend/db.sqlite3`** — read-only.
- **DB restore** (only if needed; run from `web_app`):

  ```
  backend/.venv/Scripts/python.exe -c "import sqlite3; s=sqlite3.connect('file:../eval-baseline/db.sqlite3.bak?mode=ro',uri=True); d=sqlite3.connect('backend/db.sqlite3'); s.backup(d); d.close(); s.close()"
  ```

## Per-task pipeline (what works, cheapest first)

1. **Lesson writer** (new Sonnet agent). Prompt: read RULES.md; rewrite `content/lessons/lesson-X.json`; add citations; delete the placeholder citation only if grep shows nothing else uses it (**`cite-tf-004` is shared, keep it**); write `lesson-X-impl.md` with a **claim table** (every fact and number, doc URL, quote of 20 words or fewer that **actually asserts that claim**); set `drillIds`; return 4 lines or fewer; stay available. Model the prompt on **4.4** (closed, cleanest run so far).
2. **Lead Dev:** `content_lint.py`, `q1_batch_check.py` (lesson lines), `claim_prose_check.py`. Also check directly for **duplicated sentences** and confirm exactly one `##` title.
3. **Commit.** Then **AWS round 1** and **Teacher round 1** in parallel (2-agent cap).
4. **Resume the same writer** to apply both reviewers' fixes, then write the questions. Split writers only above 25 questions.
5. **Lead Dev pre-check before round 2:** `q1_batch_check.py`, `distractor_type_audit.py`, `stem_echo_check.py`, and **read every distractor** — no script sees a category-error strawman.
6. **Round 2:** resume both reviewers. Each marks its own findings Gone, second-role-checks the other's, and reviews every question.
7. **Student:** `make_student_packet.py X <total>`, then a Sonnet agent that may open **only** those two files and must commit all answers in writing before opening the answers file.
8. **Close:** `progress.md`, issue register, DB fingerprint, commit.

## Recurring problems to prevent (tell writers up front)

- **Category-error strawmen:** a real service in a job it was never built for. Fails *none* of the stated requirements, so a student eliminates it on sight. Task 4.3 had ~24 in its first draft and two more survived into round 2.
- **Turning off the safety control** ("Remove all throttling settings"). Same family as "do it by hand". One of these survived all three reviewers plus a Lead Dev pre-check on 4.4 (`s06-mr`) and was only caught on a re-read.
- **Absolutism tells:** `as the only`, `alone as the`. Four instances on 4.3, one more on 4.4.
- **Self-explaining choices:** `since`, `even though`, `because`, `by default`.
- **One distractor type reused too often.** Count with `distractor_type_audit.py` *before* writing, not after — a networking task ties five types at the cap naturally.
- **Claim-table facts never written into prose.** Numbers are scripted; **non-numeric rows are the Teacher's catch** (the DMS endpoint rule on 4.3, Origin Shield on 4.4). Ask the writer to re-sweep all rows, not just the reported one.
- **Quotes that are verbatim but support a different statement** than the claim beside them (3 of these on 4.4, all citation-sourcing).
- **Fix passes that append a sentence already present.** Task 4.3 ended with the same sentence duplicated in three sections, one of them stated three times.
- **Stem/key keyword echo** (the new rule). Fixing only the key is not enough — on 4.4's `k03-mc` the key was reworded and the stem still carried the lesson's language, and the whole stem restated GWLB's doc definition. **Check the stem against all choices.**
- **Reviewer-suggested replacements that duplicate an existing choice.** Accept the concern, pick a distinct option.
- **Made-up features**, e.g. "Kinesis broker nodes".
- **Retired / closed / renamed** — see RULES.md.
- **Do not "fix" the `##` lesson title** to `###`, and do not report the `### Warnings` section. Both are standard in all 22 lessons.

## Sitting 4 — what landed

### Task 4.3 — **closed** (`aba7f5e`)

Cost-optimized databases, 22 questions. AWS close, Teacher close, Student **22/22**.

Teacher's `TEACHER-Q43-001` (high) was the one that mattered: `k07-mc` was a near-clone of `s02-mc`, testing S02's MySQL/PostgreSQL fact with near-identical key text, so one fact was tested three times while K07's own objective (homogeneous vs heterogeneous migration) went untested. Rewritten onto K07 with the key kept in slot c to preserve the MC spread. AWS reviewed the same 22 questions and found nothing.

Also fixed: duplicated prose in S02, S05 and K05 (K05 stated one limit three times; neither reviewer caught that one), an `s03-mc` strawman, and four "as the only" tells. Then the plural-matching bug in `distractor_type_audit.py` surfaced read replica at 6/22 and snapshot at 4/22 — both fixed, and the two k08 snapshot distractors turned out to be strawmen themselves.

Student flagged 9 of 22 stems keyword-guessable. That prompted the rule below.

### RULES change — stem-paraphrase rule (`41945c1`)

User-approved, applying **from 4.4 onward**; closed tasks are not reopened. Stems state the requirement in the scenario's own operational language, not the lesson's distinctive keywords, and the key must not echo the stem; a stem-echoing distractor is equally bad.

### Task 4.4 — **closed** (`3a495f8`)

Cost-optimized networks, 23 questions. AWS close, Teacher close, Student **23/23**. The cleanest run so far: MR key sets came out 9 of 9 distinct with no reorder pass, and the distractor audit passed first time with five types tied at the cap.

Findings: 3 AWS citation-sourcing on the lesson, 3 Teacher (Origin Shield table-but-not-prose, NLB/GWLB undefined, "egress" undefined) plus 2 lesson additions, `AWS-Q44-001` on the CloudFront "only" claim, and `TEACHER-Q44-001`–`003` stem echoes. Lead Dev found the `s06-mr` strawman and two avoidable stem leaks after the Student.

**On the new rule:** the Student's count did not move (9 of 23 vs 9 of 22). Reading them showed the two classes described in "Open decisions" above. The Teacher independently read 20 of 23 stems as genuine paraphrases, so the rule worked on what it targets — the single metric just cannot show it.

## Exactly where things stand

| # | Task | Qs | State |
|---|---|---:|---|
| 0–13 | 1.1–4.4 | 352 | **Closed** |
| 14 | lesson-tf-g1 | 9 | **Start here.** Not started |
| 15–21 | TF g2 (12), g3 (21), g4 (24), g5 (12), g6 (12), g7 (9), g8 (20) | 110 | Not started |

Terraform question files are named `q-tf-004-*`. The checker matches questions to a lesson by `objectiveIds`, so `q1_batch_check.py tf-g1` works. For TF lessons the Teacher checks against HashiCorp docs and AWS checks only the AWS-provider parts.

**Suggested sittings:**
- Next: TF g1+g2 (one writer), then g3.
- Then g4, g5+g6 (one writer).
- Then g7, g8.

**Final sitting:**
- a browser Student smoke test of about 10 questions across tasks 3.1 to TF g8, then restore the DB;
- close L1/Q1 and ISS-010 in the register;
- update `docs/status.md`;
- run `python manage.py test workbook`, `scripts\content_lint.py` and `npm run build`.

## Optional later (not blocking)

- `q1_batch_check.py 1-1` FAIL from demo `q-a0-*` files: fix the glob or exclude those ids.
- `claim_prose_check.py` does not cover non-numeric claim-table rows.
- Citations and `reviewedOn` are all `2026-09-26`, including task 4.4 written on the 27th, because the batch checker enforces that date. If it should track the real date, change it as one sweep rather than letting the corpus split across two dates.
