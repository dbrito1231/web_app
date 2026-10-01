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
- **Stem echo gate (from task tf-g1):** `scripts\stem_echo_check.py <task>` must show no FAIL. It
  reports each token that appears in the stem and in the key but in **no distractor** -- the test
  in the Student section above. It cannot tell keyword leakage from a structural scenario
  reference, so a reviewer classifies each flag and the Lead Dev records the structural ones in
  `reports/fix-loop-r2/q1/stem-echo-waivers.json`, citing the report that says so. Anything not
  waived fails. Do not add a waiver to silence a flag you have not had a role look at.

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
- **Markdown subset:** one `##` lesson title at the top, then `###`/`####` headings, `- ` bullets, `**bold**` and backticks. No tables, links or numbered lists, and no single-asterisk italics.
  - The single `##` title is the established pattern in all 22 lessons, including every closed one. Do not report it as a violation, and do not "fix" one lesson to `###` on its own.
- **drillIds:** list every question id for the task, both `-mc` and `-mr`, in objective order.
- **Citations:** one file per doc page, `cite-saa-<task>-*.json` or `cite-tf-<g>-*.json`, with `accessed: "2026-10-01"` (the corpus-wide date set by the final-sitting sweep; a future re-check sets a new date across the corpus in one commit). The `note` names, in one sentence, the specific claim the page backs. List each id in `citationIds`.
- **Claim table:** the writer's impl report must contain one. It lists every fact and number, with its section, doc URL, and a verbatim quote of 20 words or fewer. Reviewers verify against this table.

## Retired, end-of-support or closed services

Never use these as a correct answer or as current advice. Mention one only if you clearly label its status.

- AWS Copilot CLI: end of support 2026-06-12.
- AWS Snow Family (Snowball Edge, Snowcone, Snowmobile): closed to new customers.
- FSx File Gateway: closed to new customers.
- AWS Glue for Ray: closed to new customers (2026-04-30).
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
  - **Paraphrase; do not echo (applies from task 4.4 onward).** State the requirement in the
    scenario's own operational language, not in the lesson's distinctive keywords, and do not
    let the key repeat the stem's wording. If a reader can pick the key by spotting the one
    option that shares a distinctive term with the stem, the question tests reading, not
    knowledge. Closed tasks 1.1-4.3 were written before this rule and are not reopened.
    - Bad: stem says "needs advanced JSON handling and custom extensions", key says
      "PostgreSQL for advanced JSON handling and custom extensions".
    - Good: stem describes what the team actually does - "stores semi-structured claim
      documents and runs analysts' ad-hoc queries against them" - and the key names the
      service without repeating the stem.
    - This cuts both ways: a distractor that echoes the stem is just as bad, because it
      misleads a reader who has understood the material.
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
- **Citations:** each question has `citationIds`, `mcpStatus: "verified"` and `reviewedOn: "2026-10-01"`.

## After applying a fix

Three consecutive tasks had a repair introduce a new defect: task 4.3's fix pass
left one sentence stated three times, task 4.4's `k03-mc` had its key cleaned of an
echo while the stem kept carrying it, and tf-g1/g2 produced both a false claim about
a real tool and a quote trimmed until it asserted more than its source. So a fix is
not done when the diff looks right. Before marking any finding Gone:

1. **Re-run the whole automated chain against the whole file, not the diff.**
   `content_lint.py`, `q1_batch_check.py`, `distractor_type_audit.py`,
   `stem_echo_check.py` and `claim_prose_check.py`, every time, even for a
   one-clause change. Each of those three regressions is something one of these
   scripts already detects globally; they were missed because the fix was checked
   locally, against the field that changed, rather than against the file it now
   lives in.
2. **Read the new fragment in isolation and ask whether it still asserts its claim
   at the same strength** -- not a stronger or weaker one. Cover everything except
   the new quote, sentence or choice text and check it against the claim-table row
   or rationale it supports, without the surrounding context that was in your head
   but is not in the file. This is what catches an over-trim.
3. **For a rewritten distractor, ask two separate questions, not one:** is this a
   real practice, **and** is the reason it is now wrong taught in the lesson. These
   are different properties. The tf-g1 CloudFormation distractor passed the first
   (native template tools are real) and failed the second (its serial-provisioning
   claim was neither taught nor true). A fix aimed at one of these will keep letting
   the other slip through.

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
  The Student also reports on stem/key wording, as **two separate numbers**. For each stem,
  after recording the answer and reason, check every choice that shares a distinctive word or
  phrase with the stem. For each shared term, apply one test: **does that same word also
  appear in at least one distractor?**
  - **No** -- the term appears only in the stem and the key: count the stem as
    **keyword-guessable (defect)**.
  - **Yes** -- the term also appears in a wrong choice, or it simply names an object,
    resource, or job the stem itself introduced into the scenario: **not** a defect. Count it
    separately as a **structural scenario reference**.
  Report both: "N stems keyword-guessable (defect)" and "M stems with a structural scenario
  reference (not a defect)". Only N is a finding against the questions.
  This replaces a single combined count, which could not tell the two apart. On task 4.3 the
  Student reported 9 of 22, and on 4.4 -- the first task under the paraphrase rule -- 9 of 23.
  Reading those nine showed most were structural, and the Teacher independently read 20 of the
  23 stems as genuine paraphrases. One number scored a defect and a property we want the same.
