# Student review — fix-loop-r2 round-1

Role: College IT Student (learner check)  
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Checked: 2026-09-25  
Servers: assumed already running (Vite PID 28264, Django PID 46208) — not started by this review.  
UI method: Cursor browser MCP failed repeatedly (`No browser tab available` / `Browser view not found` even after `browser_tabs` new + `browser_navigate`). Did **not** use Playwright. Judged R4/R5 from live API + frontend/source + lesson JSON.  
Did **not** submit exam answers or lab checkpoints (no progress DB writes).

---

## Scope

Learner re-check of R1–R5 only: GL-17 Athena followability, GL-08 user-data LF/readability, drill-stem “rewording,” Start here lesson picker titles, and lesson→exam deep links. Write-only deliverable: this file.

---

## R1

**Verdict: Fail**

Read `content/labs/gl-17.json` as a learner.

**Can follow Athena create/query?** Mostly. s07 has a real CLI path:

> `CREATE DATABASE IF NOT EXISTS gl17`

> `CREATE EXTERNAL TABLE IF NOT EXISTS gl17.sample (name string, value int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION 's3://$Bucket/data/' TBLPROPERTIES ('skip.header.line.count'='1')`

s08 `SELECT * FROM gl17.sample LIMIT 10` matches that table. s09 is **not** a followable Athena CLI step — only:

> `Run \`DROP TABLE gl17.sample\`.`

No `aws athena start-query-execution` wrapper, unlike every other Athena step.

**Columns vs CSV?** Match. s06 uploads:

> `'name,value\\nfoo,1' | Out-File -Encoding ascii gl17.csv`

Header/columns are `name`, `value`; DDL is `(name string, value int)`. (Separate Low note: PowerShell single-quoted `\n` may not create a real newline.)

**Cleanup drops table and database?** No. s09 is incomplete SQL-only text; Stop charges / teardown only empties and deletes S3 buckets:

> `aws s3 rm s3://$Bucket --recursive` … `aws s3api delete-bucket --bucket $ResultsBucket`

There is **no** `DROP TABLE` / `DROP DATABASE` in `teardown.orderedDeletesPowerShell`. Glue/Athena `gl17` catalog leftover is expected.

**Second conflicting DDL line?** No. Only one `CREATE EXTERNAL TABLE` remains (the old conflicting second bullet is gone).

Fail because teardown/cleanup does not drop the table and database, and the drop step is not a runnable Athena command.

---

## R2

**Verdict: Fail**

Read `content/labs/gl-08.json` s08 (browser Labs screen unavailable).

**Readable (not one collapsed line)?** Yes in the JSON the learner would see — the step spells out line breaks:

> `Run \`@'\` then a new line \`#!/bin/bash\` then a new line \`python3 -m http.server 80\` then a new line \`'@ | Set-Content -Encoding ascii user-data.sh\`.`

That is no longer a single collapsed `--user-data "#!/bin/bash python3…"` paste trap.

**LF line endings?** No. The instructed writer is still:

> `Set-Content -Encoding ascii user-data.sh`

On Windows PowerShell, `Set-Content` / default `Out-File` write **CRLF**, which breaks `#!/bin/bash` shebang handling on Amazon Linux. Nothing in the step forces LF (no `[IO.File]::WriteAllText` with `` "`n" ``, no `unix2dos` inverse, no `-NoNewline` + explicit LF joins).

Readable: pass. LF-safe: fail → overall **Fail**.

---

## R3

**Verdict: Not a fix**

Stem “rewording” only swaps one template bank for another. Across the drill bank, openings still cluster hard (examples counted live from `content/questions/*.json`): ~156× `Select TWO actions that support…`, ~35× `A teammate asks how to meet…`, ~31× `Pick the action that satisfies:`, ~30× `The workload needs this outcome:`, plus the other repeated frames. Correct choices still often say **`Apply the objective directly: …`** (~263 choice texts). As a learner this still reads generated, not scenario-based exam practice — renaming the stem opener is not a content fix.

---

## R4

**Verdict: Pass**

Browser failed, so judged from `GET http://127.0.0.1:8000/api/content/summary` → `lessonIndex` (23 rows) plus `frontend/src/components/StartHereTab.tsx` and `content/lessons/*.json`.

API returns human titles for all 23 lessons (not raw ids). Examples: `A0 — Lab safety and local threat model`, `A1 — Secure workloads and applications`, `T4 — HCP Terraform concepts`. The picker maps `row.title` into `<option>`:

> `{lessonIndex.map((row) => (` … `{row.title}` … `))}`

Fallback to raw id only if `lessonIndex` is missing (`summary.lessons.map((id) => ({ id, title: id }))`) — live API does supply titles. Accessible name from markup: `<label className="lesson-picker">Lesson <select>…` → accessible name **“Lesson”**. Keyboard: native `<select>` (arrow/typeahead) — not verified in browser.

**Missing/wrong titles:** none found among the 23. (JSON uses U+2014 em dash in titles; that is fine.)

---

## R5

**Verdict: Fail**

Lesson drill links are correct in code (`StartHereTab.tsx`):

> `<a href={\`/exam?q=${encodeURIComponent(id)}\`}>{id}</a>`

`ExamDrillsTab.tsx` reads `?q=` on load and, when the id is in the catalog, sets that question active — so a **good** id should open that drill. Browser back should work because these are real `<a href>` navigations (history entry). Did not click Check answers.

**Bad id:** Fail. If `?q=` is absent from the catalog, the UI **silently** falls through to the first catalog row — no learner-facing message:

> `const pick = rows.find((row) => row.id === requested);`  
> `if (pick) { … } else if (rows[0]) { setActiveQuestionId(rows[0].id); }`

The API itself returns a clear error (`GET /api/questions/does-not-exist-xyz` → `{"error": "Question not found"}`), but the deep-link path never shows that. A bad link looks like a normal first-card open.

---

## New issues (Low+)

| Severity | Issue |
| --- | --- |
| Low | GL-17 s09 `DROP TABLE gl17.sample` is not an `aws athena start-query-execution` command; learners cannot mirror s07/s08. |
| Low | GL-17 Stop charges / teardown never drops Glue/Athena database `gl17` (or the table) — only S3. |
| Low | GL-17 CSV create uses PowerShell single-quoted `\n` with `Out-File`; may write a literal `\n` instead of a newline. |
| Low | Exam `?q=` unknown id silently opens the first drill instead of surfacing “Question not found.” |
| Low | ~263 choices still begin with `Apply the objective directly:` (ties to R3; not a separate stem fix). |
| Info | Cursor browser MCP unavailable this session; Labs GL-08 UI and Start here/Exam keyboard paths not visually confirmed. |

---

## Verdict summary

| ID | Verdict |
| --- | --- |
| R1 | **Fail** |
| R2 | **Fail** |
| R3 | **Not a fix** |
| R4 | **Pass** |
| R5 | **Fail** |
