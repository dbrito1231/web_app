# Q1 rewrite: shared rules for every writer and reviewer

Plans: `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` (Amendments 2–3) and `.cursor/plans/q1_remaining_budget_plan_20260926.plan.md`. Roles are defined in `AGENTS.md`.

## Hard bans

- Never call AWS, provision anything, or run credentialed terraform.
- Never call `ExecuteTerraformCommand` or `ExecuteTerragruntCommand`.
- No git commands (including `git stash`) unless the prompt says otherwise.
- No servers, no Playwright, no scripted POSTs.
- Never click Reset or Import.
- Edit only the files your prompt names. The Teacher writes no files.

## Tools

- **AWS facts:** load `mcp__MCP_DOCKER__mcp-exec` via ToolSearch (`select:mcp__MCP_DOCKER__mcp-exec`). Call it with `name: "search_documentation"` (`{"search_phrase": ..., "limit": 5}`), then `"read_documentation"` (`{"url": ...}`) or `"read_sections"`. Fall back to WebFetch on docs.aws.amazon.com.
- **Terraform facts:** WebFetch on developer.hashicorp.com. For AWS provider resources, use `SearchAwsProviderDocs` through `mcp-exec`.
- **Python:** `backend\.venv\Scripts\python.exe`.
- **Helper scripts:** put them in `C:\Users\dbadmin\AppData\Local\Temp\claude\C--Users-dbadmin-Desktop-GitServ-ccna-web-app\a6f21a3f-b237-427b-b80d-d927c3db310e\scratchpad`, with a unique prefix.
- **Lint:** `backend\.venv\Scripts\python.exe scripts\content_lint.py` must PASS.
- **Batch check:** `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py <task>` (e.g. `3-1` or `tf-g1`) must show no FAIL.

## Budget

- Read only what you need.
- Don't re-read files you already have in context.
- Keep your final reply to 5 lines or fewer. Detail goes in your report file.

## JSON format

Load with `json.load`. Write with `json.dumps(data, indent=2, ensure_ascii=True) + "\n"` in text mode, `encoding="utf-8"`.

## Lessons

- **Structure:**
  - One `###` section per objective bullet, in id order.
  - Clear for a college IT student.
  - Contrast the options people confuse.
  - Each section ends with an `**Exam tip:**` line.
- **Markdown subset:** `###`/`####` headings, `- ` bullets, `**bold**` and backticks. No tables, links or numbered lists, and no single-asterisk italics.
- **drillIds:** list every question id for the task, both `-mc` and `-mr`, in objective order.
- **Citations:** one file per doc page, `cite-saa-<task>-*.json` or `cite-tf-<g>-*.json`, with `accessed: "2026-09-26"`. The `note` names, in one sentence, the specific claim the page backs. List each id in `citationIds`.
- **Claim table:** the writer's impl report must contain one. It lists every fact and number, with its section, doc URL, and a verbatim quote of 20 words or fewer. Reviewers verify against this table.

## Retired, end-of-support or closed services

Never use these as a correct answer or as current advice. Mention one only if you clearly label its status.

- AWS Copilot CLI: end of support 2026-06-12.
- AWS Snow Family (Snowball Edge, Snowcone, Snowmobile): closed to new customers.
- FSx File Gateway: closed to new customers.
- Timestream for LiveAnalytics: closed to new customers (2025-06-20).
- Renamed services: use the current name and give the old one once, e.g. "Amazon Data Firehose (formerly Kinesis Data Firehose)", "Amazon Managed Service for Apache Flink (formerly Kinesis Data Analytics)", "Amazon Quick Sight (formerly QuickSight)".
- Check anything else before naming it, for example QLDB, Timestream for LiveAnalytics, CodeCommit, Cloud9 and CodeStar. Add new finds to this list in your report.

## Questions

- **Keep unchanged:** `id`, `type`, `module`, `objectiveIds` and `selectCount`. Each question tests its own objective.
- **Stem:**
  - A realistic scenario with a company, a constraint and a requirement.
  - No two stems in a task may share their first 6 words.
  - Never paste objective text.
  - MR stems say "(Select TWO.)" or the right count.
- **Choices:**
  - MC has 4 choices; MR has 5.
  - All real and current, from the same area.
  - No choice refers to another choice.
  - Exactly one best answer (MC), or exactly `selectCount` answers (MR).
- **Every distractor is a real AWS or Terraform option** that meets every stated requirement but one. That requirement must be stated in the stem.
- **No strawmen:** no anti-pattern or manual non-service action that no candidate would pick. Examples: "run it on one instance", "an engineer does it by hand", "hardcode an IP", "copy files manually", "wait until next time".
- **No giveaway wording in choices:** `since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`. No key that restates the stem's requirement or justifies itself. Keys should be about as long as the distractors.
- **MR stems:** don't join two unrelated needs unless every distractor plausibly answers one of them.
- **Duplicates:** no two questions in a task may test the identical fact.
- **Teach-before-test:** the key AND the reason each distractor is wrong must be taught in the task's lesson. If a question needs a fact the lesson lacks, write the exact doc-verified sentence under "Lesson additions requested" instead of assuming it is taught.
- **Distractor diversity:** no distractor *type* in more than 15% of the task's questions. Include a type table in the report.
- **Balance:**
  - The right answer is the longest choice in 35% or fewer of MC questions.
  - MC keys are spread evenly across a/b/c/d.
  - MR key slots are spread across a–e.
- **Rationale:** explains the key and every distractor by content. No letter references.
- **Citations:** each question has `citationIds`, `mcpStatus: "verified"` and `reviewedOn: "2026-09-26"`.

## Reviews

- **Round 1 (lesson):** AWS and the Teacher each review the lesson.
  - Verify the writer's claim table. AWS spot-checks at least 8 rows and the Teacher at least 6, plus any row that looks wrong.
  - Check coverage, the exam tips, format and teach-before-test readiness.
  - Issues are recorded as `AWS-Lxx-###` or `TEACHER-Lxx-###`, each with severity, location and an exact doc-verified fix.
  - End with the line "Lesson x.y: approve for question writing" or "not yet".
- **Round 2 (lesson fixes + questions):** the same reviewer is resumed and does four things:
  - (a) marks each of its own lesson findings Gone or not gone;
  - (b) gives the second-role check on the other reviewer's lesson findings;
  - (c) reviews every question for key, distractors, rationale, stem and citations; the Teacher also checks teach-before-test and fairness;
  - (d) verifies every number used in a key.
  - Issues are recorded as `AWS-Qxx-###` or `TEACHER-Qxx-###`.
  - End with the line "Task x.y: close" or "not yet".
- **Every report ends with** `Overall: approve` or `Overall: concerns`.
- **Closure:** an item closes only when its reporter and a second role both mark it Gone.
- **Student:** answers from the text packet in the scratchpad before opening the answers file. Records each answer and a one-line reason first, then judges fairness. The target is 90% or better.
