# HANDOFF: Q1 lesson-first content rewrite (as of 2026-09-26)

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

**Status: 11 of 22 tasks closed.** Next up is lesson 4.2. The user said to continue in "sittings" of about 3 tasks, then **stop and wait for the user's GO**.

## Plans and records (source of truth)

| File | Purpose |
|---|---|
| `.cursor/plans/q1_remaining_budget_plan_20260926.plan.md` | **Current plan (approved).** Budget-aware workflow and the user's decisions (§9) |
| `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` | Earlier amendments 1–3; question rules originate here |
| `reports/fix-loop-r2/q1/RULES.md` | **Shared rules for every writer and reviewer** (bans, tools, format, question rules, retired/renamed services, review procedure). Point every agent prompt here |
| `reports/fix-loop-r2/q1/progress.md` | Per-task tracker (LW/LR/LF/QW/QR/QF/Closed). Update after every step |
| `reports/fix-loop/issue-register.md` | Closed-items table and "Still open" (L1/Q1, ISS-010) |
| `reports/fix-loop-r2/q1/*` | Per-task reports: `lesson-X-impl.md` (with claim table), `lesson-X-AWS.md`, `lesson-X-TEACHER.md`, `questions-X-impl*.md`, `questions-X-AWS.md`, `questions-X-TEACHER.md`, `questions-X-STUDENT.md` |

## User decisions still in force

- **Models:**
  - Subagents run **Sonnet 5**; no subagent may use Opus.
  - **Haiku 4.5** may be used for the Student text-packet check.
- **Concurrency:** at most **2 subagents at a time**.
- **Pacing:** about **3 tasks per sitting**, then stop, report, and wait for GO.
- **Student check:**
  - Per task, use the **text packet** (see Tools), not the browser.
  - Run one browser smoke test at the very end.
- **Closure rule:** an item closes only when its **reporter and a second role** both mark it Gone.
- **Deferred:** D6 and the small screen items. PY-R5-001 to 003 are won't-fix.

## Hard rules (from AGENTS.md and the user)

- Agents never call AWS, never provision anything, and never run credentialed terraform.
- The `aws-terraform` MCP exposes `ExecuteTerraformCommand` / `ExecuteTerragruntCommand`. **Never call them.**
- No servers, no Playwright, no scripted POSTs. Never click Reset or Import.
- Subagents run no git and no `git stash`. Lead Dev commits after every step.
- If anything submits drills in the app, restore the DB to baseline:
  - run the restore snippet below;
  - check `scripts/db_fingerprint.py backend/db.sqlite3`, which must print sha `930f0e72…`.
  - The text-packet Student check does not touch the DB.
- Commit messages end with a `Co-Authored-By:` line naming the model you are running as.

## Tools

- **AWS docs MCP:**
  - Load `mcp__MCP_DOCKER__mcp-exec` via ToolSearch (`select:mcp__MCP_DOCKER__mcp-exec`).
  - Call it with `name: "search_documentation"` (`{"search_phrase","limit"}`), `"read_documentation"` (`{"url"}`) or `"read_sections"` (`{"url","section_titles"}`).
  - Fall back to WebFetch.
- **Terraform docs:** WebFetch on developer.hashicorp.com, plus `SearchAwsProviderDocs` through `mcp-exec`.
- **`scripts/q1_batch_check.py <task>`** (e.g. `4-2`, `tf-g1`): a read-only checker. It covers:
  - lesson format;
  - `drillIds` vs the questions (matched by `objectiveIds`);
  - tell words (giveaway wording);
  - retired names;
  - 6-word openings;
  - longest-is-key;
  - key positions;
  - citations resolve.

  Expect FAIL on placeholder questions until they are rewritten. Lesson Snowball WARNs are expected; the lessons label it as closed.
- **`scripts/make_student_packet.py <task> <n>`:** writes `student-packet-<task>.md` (lesson + questions, no keys) and `student-answers-<task>.md` to `%TEMP%\q1-packets`. **Always pass n = the task's total question count.**
- **`scripts/db_fingerprint.py backend/db.sqlite3`:** a read-only DB fingerprint.
- **Python:** `backend\.venv\Scripts\python.exe`. Lint: `scripts\content_lint.py` must PASS.
- **JSON writes:** `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, utf-8.
- **DB restore** (only if needed; run from `web_app`):

  ```
  backend/.venv/Scripts/python.exe -c "import sqlite3; s=sqlite3.connect('file:../eval-baseline/db.sqlite3.bak?mode=ro',uri=True); d=sqlite3.connect('backend/db.sqlite3'); s.backup(d); d.close(); s.close()"
  ```

## Per-task pipeline (what worked, cheapest first)

1. **Lesson writer** (new Sonnet agent). The prompt says: read RULES.md; rewrite `content/lessons/lesson-X.json`; add new `cite-<saa-X|tf-gN>-*.json` citations; delete the old placeholder citation only if grep shows nothing else uses it (**`cite-tf-004` is shared, keep it**); write `lesson-X-impl.md` with a **claim table** (every fact and number, doc URL, verbatim quote of 20 words or fewer); set `drillIds` to all question ids; return 4 lines or fewer; stay available. Model the prompt on a recent approved lesson (3.3, 3.4 or 4.1).
2. **Commit.** Then run **AWS round 1** (new Sonnet agent). It verifies the claim table and writes `lesson-X-AWS.md` ending in "approve for question writing / not yet".
3. **Teacher round 1** (new Sonnet agent). It gives the same kind of verdict, in its reply; Lead Dev saves it as `lesson-X-TEACHER.md`.
4. **Resume the same writer** (SendMessage) to apply both reviewers' fixes, and then write the questions.
   - For more than 25 questions, split the work. **Writer A** (the lesson writer) takes the `k*` files, with stems that start with a company or team noun phrase. **Writer B** (a new agent) takes the `s*` files, with other openings.
   - Give each writer its own distractor-type cap: A at most 2 per type, B at most 3, so the task total stays at 15% or less.
5. **Lead Dev pre-check:** run `q1_batch_check.py`. **Also count repeated distractor types across the whole task.** The script doesn't do this yet, and it was the most common reviewer finding. Send the writer back before review if any type exceeds 15%.
6. **Round 2:** **resume** the same AWS agent, then the same Teacher agent. Each marks its own lesson findings Gone, gives the second-role check on the other's findings, and reviews every question. Small fixes (a citation, one distractor) can be done by Lead Dev directly; then ask the reporter for a 2-line confirmation.
7. **Student:** run `make_student_packet.py X <total>`, then start a **Haiku** agent that may open only those two files. The target is 90% or better. Save its report as `questions-X-STUDENT.md`.
8. **Close:** update `progress.md` and the issue register ("Closed" row, plus the "Still open" counts). Commit.

## Recurring problems to prevent (tell writers up front)

- **Strawman distractors** ("do it by hand", "one instance", "hardcode an IP").
- **Self-explaining choices** ("since…", "even though…").
- **One distractor type reused too often.** Seen so far: DataBrew 10/24, EFS 7/35, Snowball 2/8, reserved concurrency 3/16.
- **Made-up features**, e.g. "Kinesis broker nodes".
- **Distractors whose "why wrong" isn't taught in the lesson.** Either teach it (add a doc-verified lesson sentence plus a citation) or pick another distractor.
- **Retired, closed or renamed services** (full list in RULES.md):
  - retired: Copilot CLI;
  - closed to new customers: Snow Family, FSx File Gateway, Timestream for LiveAnalytics;
  - renamed: Data Firehose, Managed Service for Apache Flink, Quick Sight.

## Exactly where things stand

| # | Task | Qs | State |
|---|---|---:|---|
| 0–10 | 1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1 | 283 | **Closed** |
| 11 | lesson 4.2 Cost-optimized compute (15 objectives) | 24 | **Next.** Not started; the placeholder citation is `cite-4-2` |
| 12 | lesson 4.3 Cost-optimized databases (14 objectives) | 22 | Not started |
| 13 | lesson 4.4 Cost-optimized networks (14 objectives) | 23 | Not started |
| 14–21 | Terraform g1 (9), g2 (12), g3 (21), g4 (24), g5 (12), g6 (12), g7 (9), g8 (20) | 119 | Not started |

Terraform question files are named `q-tf-004-*`. The checker matches questions to a lesson by `objectiveIds`, so `q1_batch_check.py tf-g1` works.

**Suggested sittings:**
- Next: 4.2, 4.3, 4.4.
- Then TF g1+g2 (one writer), g3, g4.
- Then g5+g6 (one writer), g7, g8.

**Final sitting:**
- a browser Student smoke test of about 10 questions across tasks 3.1 to TF g8, then restore the DB;
- close L1/Q1 and ISS-010 in the register;
- update `docs/status.md`;
- run `python manage.py test workbook`, `scripts\content_lint.py` and `npm run build`.

**The working tree is clean** apart from this handoff and the two helper scripts moved into `scripts/`. The DB is at baseline. No agents are running.
