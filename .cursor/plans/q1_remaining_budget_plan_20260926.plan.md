# Q1 remaining items: budget-aware completion plan (2026-09-26)

Author: Lead Developer (main session). Status: **approved by user 2026-09-26 (GO).**

This plan adds to `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` (Amendments 1–3). The question rules in Amendment 2 and the lesson-first order in Amendment 3 still apply. This plan changes **how the work is run**, to use far fewer tokens per task.

## 1. What is left

| # | Item | Questions | State |
|---|---|---:|---|
| 5 | lesson 3.1 | 8 | Lesson approved; questions not written |
| 6 | lesson 3.2 | 16 | Lesson fixed, AWS re-check approved; Teacher re-check still needed; questions not written |
| 7 | lesson 3.3 | 21 | Draft written but uncommitted and unreviewed (1 lesson file, 16 citations) |
| 8–13 | lessons 3.4, 3.5, 4.1, 4.2, 4.3, 4.4 | 141 | Not started |
| 14–21 | Terraform g1–g8 | 119 | Not started |

That is 16 tasks and 305 questions.

## 2. Why the credits ran out

In this session, one task cost about **2 million subagent tokens**, plus Opus time in the main session. Tasks 2.1 and 2.2 each used about 12 Sonnet agent runs:

| Step | Agents | Tokens each (seen) |
|---|---:|---:|
| Lesson writer | 1 | 190–220k |
| AWS + Teacher lesson review | 2 | 120–150k |
| Lesson fix batch | 1 | 130k |
| AWS + Teacher lesson re-check | 2 | 95–110k |
| Question writers (split) + Lead Dev fix round | 2 + 2 resumes | 140–240k |
| AWS + Teacher question review | 2 | 150–175k |
| Student fairness (browser, ~130 tool calls) | 1 | 165–190k |
| Final re-checks | 1–2 | 95k |

Three things drove the cost:

1. **Every step started a new agent.** Each new agent re-read AGENTS.md, the plan, the model lessons and the model questions before it could start.
2. **Re-checks were separate agent runs,** even when the fix was two sentences.
3. **The Student check drove the browser.** That meant screenshots, page reads and clicks for every question, plus a DB restore afterwards.

At about 2M tokens per task, the 16 remaining tasks would need about 32M tokens. The monthly limit was hit three times on less than that.

## 3. The new way of running a task (target: about 0.8–1.0M tokens per task)

### 3.1 One writer agent per task, kept alive with SendMessage

The same Sonnet writer:
- writes the lesson;
- is resumed to apply the reviewers' lesson fixes;
- is resumed again to write the questions;
- is resumed again for question fixes.

It already holds the rules, the model files and the docs it read, so nothing is re-read.

### 3.2 Two review rounds per task instead of four

- **Round 1 (lesson):** AWS reviewer and Teacher each review the lesson.
- **Round 2 (lesson fixes + questions together):** the same AWS and Teacher agents are **resumed**, not newly started. Each checks that its own lesson findings are Gone, gives the second-role check on the other reviewer's lesson findings, and reviews the questions in the same pass.

The questions are written right after the lesson fixes, without waiting for a separate lesson re-check.
- Risk: questions built on a fix that a reviewer later rejects.
- Mitigation: lesson fixes are small by then, and round 2 checks both in one pass.

The closure rule is unchanged: the reporter plus a second role must mark every item Gone.

### 3.3 Reviewers verify the writer's claim table and don't search from scratch

The writer's impl report must include a **claim table**: each lesson fact and number, the doc URL, and a short quote. Reviewers:
- fetch only the URLs in that table;
- spot-check at least 8 claims (AWS) or 6 claims (Teacher), plus every number that appears in a question key;
- do their own searches only when a claim has no URL or the quote doesn't match.

### 3.4 Student fairness from a text packet, not the browser

Lead Dev generates two scratchpad files with a script:
- `student-packet-<task>.md`: the lesson text, plus 8 sampled questions with their stems and choices only (no keys, no rationales);
- `student-answers-<task>.md`: the keys and rationales.

The Student answers from the packet first, then opens the answers file and judges fairness. The target is still ≥90%.

This removes the browser, the screenshots, the database writes and the DB restore. A browser Student check runs once at the very end, as a smoke test of how the app shows 10 questions spread across all new tasks.

### 3.5 Lead Dev checks by script before anyone reviews

A reusable, read-only script, `scripts/q1_batch_check.py` (Lead Dev writes it once), runs over a task's questions. It checks:
- 6-word stem openings;
- longest-is-key rate;
- MC/MR key positions;
- letter references;
- tell words (`since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`);
- citations resolving;
- `mcpStatus` and `reviewedOn`;
- the lesson's `drillIds`;
- retired names (Copilot, Snowball as a key, FSx File Gateway, and any others found).

Lead Dev reads only the script's output and the lines it flags, not every choice. Anything flagged goes back to the writer in the same resumed session. This replaces the manual read-throughs that cost Opus tokens in tasks 2.1 and 2.2.

### 3.6 Terraform lessons g1–g8

- The Teacher checks against HashiCorp docs, through WebFetch on developer.hashicorp.com, plus `SearchAwsProviderDocs` for provider details.
- The AWS reviewer joins only the lessons that use the AWS provider in depth (g3, g4 and g8 are expected). For the other lessons, the Student's fairness check is the second role that closes items.
- `ExecuteTerraformCommand` and `ExecuteTerragruntCommand` stay forbidden.

### 3.7 Smaller prompts and smaller outputs

- **Prompts:** shared rules move into one file, `reports/fix-loop-r2/q1/RULES.md` (MCP use, bans, format, question rules, anti-strawman list, retired-service list). Prompts point to it instead of repeating ~3 KB of rules each time.
- **Final replies:** every agent's final reply is at most 5 lines. Full detail goes only into the report file.
  - The Teacher can't write files, so its full report goes in its reply, and Lead Dev saves it with a script without reading it in full.
- **Lead Dev's own messages:** shorter status updates, with no re-printed tables.

### 3.8 Pacing and checkpoints (so a limit hit costs nothing)

- **At most 2 Sonnet agents at once** (down from 3). This lowers the chance of a burst hitting the limit mid-step. It adds wall-clock time but not tokens.
- **Commits:** after every step. The tracker is updated after every step, so a stopped agent can be resumed with SendMessage and nothing is redone.
- **Budget per sitting:** about 3 tasks (about 3M tokens). After that, Lead Dev stops, reports, and waits for GO. You can change the number.
- **After an outage:** Lead Dev checks `git status`, resumes the same agents, and never relaunches from scratch unless an agent's transcript is lost.

## 4. Order of work

**Sitting 1:**
1. Teacher re-check of lesson 3.2. This is a resumed Teacher if possible; otherwise a new one with a short prompt.
2. Lesson 3.3: keep the draft, which is complete apart from its impl report. A new writer finishes the report and claim table, then continues on the 3.3 pipeline. (Alternative: discard it and rewrite. See the decisions below.)
3. Task 3.1 questions: one writer, 8 questions.
4. Task 3.2 questions.

**Sittings 2–5:** SAA lessons 3.4, 3.5, 4.1, 4.2, 4.3 and 4.4, about 3 per sitting.
- 4.1 (35 questions) keeps two question writers. Both are resumed writers of the same lesson: writer A is the lesson writer, writer B is new and reads only the lesson and RULES.md.
- The others use one writer.

**Sittings 6–8:** Terraform g1–g8. The small ones are paired: g1+g2, g5+g6 and g7 are each written by one writer agent covering two lessons.

**Final sitting:**
- Student browser smoke test (10 questions across tasks 3.1–TF g8), then DB restore.
- Close ISS-010 and L1 in the register.
- Update `docs/status.md`.
- Run `manage.py test`, `content_lint.py` and `npm run build`.

## 5. Expected cost

| | Before | After (estimate) |
|---|---:|---:|
| Agent runs per task | ~12 new | ~4 new + 4–6 resumes |
| Tokens per task | ~2.0M | ~0.8–1.0M |
| 16 remaining tasks | ~32M | ~14–16M |
| Sittings | n/a | ~8, about 3 tasks each |

These are estimates from this session's per-agent numbers. Lead Dev will report the real totals after sitting 1 and adjust the plan if the savings are smaller.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Resumed agents build up long context and slow down | Each writer handles one task only (or two small TF tasks); a new writer starts per task |
| Combined round-2 reviews miss a lesson-fix problem | The reviewer prompt requires an explicit Gone/not-gone line per lesson finding before the question review |
| The text packet hides UI problems | One browser smoke test at the end; UI screens were already closed in earlier rounds |
| Reviewer spot-checks miss a wrong number | Every number used in a question key must be verified, not sampled |
| Fewer parallel agents make it slower | Accepted: it lowers the risk of hitting limits, and tokens are the constraint, not time |

## 7. Files touched by this plan

- New:
  - `reports/fix-loop-r2/q1/RULES.md`;
  - `scripts/q1_batch_check.py` (read-only checker; Lead Dev writes it);
  - scratchpad student packets.
- Updated:
  - `content/lessons/*`, `content/questions/*` and `content/citations/*` for the remaining tasks;
  - `reports/fix-loop-r2/q1/progress.md`;
  - `reports/fix-loop/issue-register.md`;
  - `docs/status.md` at the end.
- The content is affected, so Teacher validation happens before and after, as today.

## 8. Decisions for you

1. **Lesson 3.3 draft:** keep it and review it (recommended, saves about 200k tokens), or discard it and rewrite?
2. **Concurrency:** 2 agents at a time (recommended) or keep 3?
3. **Budget per sitting:** about 3 tasks before stopping for your GO (recommended), or a different number?
4. **Student check:** the text packet plus one browser smoke test at the end (recommended), or keep the browser check per task?
5. **Models:** keep Sonnet 5 for everything (your current rule). Optionally, Haiku 4.5 could handle only the Student packet check and the RULES/metrics script runs, for a small extra saving. Say yes only if you want that.

## 9. User decisions (2026-09-26)

1. Keep the lesson 3.3 draft and review it.
2. At most **2** subagents at a time.
3. About **3 tasks per sitting**, then stop and wait for GO.
4. Student check from the text packet, plus one browser smoke test at the end.
5. **Haiku 4.5 is allowed** alongside Sonnet 5. Haiku is used for mechanical, low-judgment work: Student packet fairness checks and saving or formatting reports. Writers and the AWS and Teacher reviewers stay on Sonnet 5. No subagent uses Opus.

## 10. Amendment: model substitution (sitting 3, 2026-09-26)

Sonnet 5 and Haiku 4.5 are no longer offered as subagent models. The runtime's allowed list was checked directly and contains neither. Decision 5 above is therefore superseded for this sitting and until Sonnet 5 returns:

- **Writers and the AWS and Teacher reviewers:** `gpt-5.3-codex`.
- **Student packet fairness check:** `composer-2.5-fast`.
- The no-Opus rule for subagents is unchanged, so `inherit` must not be used.

Everything else — 2 subagents at a time, ~3 tasks per sitting, the text-packet Student check, the closure rule — is unchanged. Sitting 3 covers tasks 4.2, 4.3 and 4.4.

## 11. Amendment: status and rules in force (2026-10-01)

This amendment records the current state. It does not change the pipeline in section 3 or the closure rule. Where it conflicts with sections 1, 3.8, 9 or 10, this amendment wins. `HANDOFF.md` has the step-by-step detail.

**Rules now in force (user decisions after 2026-09-26):**
- **Models:** `gpt-5.3-codex` and `composer-2.5-fast` (section 10) do not exist in this harness. All subagents run **Sonnet**, per the standing memory rule. No subagent uses `inherit`.
- **Concurrency:** at most **3** subagents at a time (the user raised it from 2 on 2026-09-30).
- **Pacing:** still about 3 tasks per sitting, then stop and wait for GO.
- **Shortest-is-key:** the 35% cap applies to both longest and shortest key length on all new work (decision 2026-09-28; checked by `q1_batch_check`).
- **Stem-paraphrase rule** (2026-09-27): applies from task 4.4 onward.
- **New pre-check checks** learned since this plan: letter references in rationales, distractors that work in practice, version-sensitive behaviour, and distractor-only "as …"/"because …" justification clauses.

**What is left (replaces the section 1 table; updated at the end of 2026-10-01):**

| # | Task | Questions | State |
|---|---|---:|---|
| 0–19 | 1.1–4.4, tf-g1–tf-g6 | 421 | Closed (4-3, 4-1 and 1-3 reopened and re-closed 2026-09-29 for shortest-is-key) |
| 20 | tf-g7 | 9 | Closed 2026-10-01 (`2d09593`): both reviewers close, Student 9/9 |
| 21 | tf-g8 | 20 | Closed 2026-10-01 (`bf43307`): both reviewers close, Student 20/20. Most round 1 lesson fixes came from the user's commit `53f1beb`, reviewed in round 2 |

**Final sitting (replaces the section 4 list):**
- one date sweep across all citations and `reviewedOn`, and update `q1_batch_check` to match;
- CR-0019, CR-0021 and the D6-FU lesson follow-ups;
- LD-Qg7-002 (stems with no question in tf-g1, tf-g2 and tf-g4): decide whether to fix it;
- reconcile `reports/fix-loop/issue-register.md`, closing L1 and ISS-010 with reasons;
- Student browser smoke test (about 10 questions across 3.1 to tf-g8), then DB restore and fingerprint check;
- update `docs/status.md`;
- run `manage.py test workbook`, `content_lint.py` and `npm run build`.

Learning content is not changed by this amendment, so no Teacher validation is needed for it.

**Update, end of 2026-10-01:** tf-g7 (`2d09593`) and tf-g8 (`bf43307`) are closed, so all 22 tasks (450 questions) are done. Only the final sitting above remains, and it waits for the user's GO.
