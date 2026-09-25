---
name: AGENTS.md roles
overview: "Planning only. Add a root AGENTS.md that defines two agents for this workbook — a read-only Teacher Agent that guides the learner through the content, and a Lead Developer Agent that is the only writer and needs an approved plan before any change. Teacher sends change requests to Lead Developer; Lead Developer checks with Teacher before any change that touches learning content. Existing rules still apply: agents never touch AWS, and there is one writer per path set."
todos:
  - id: approve-plan
    content: Learner reviews and explicitly approves this plan (editing this file is not approval)
    status: completed
  - id: write-agents-md
    content: Lead Developer writes AGENTS.md at the repo root with the sections in part 4
    status: completed
  - id: link-docs
    content: Add a one-line pointer to AGENTS.md in README.md and add the two roles to the docs/status.md role column rules
    status: completed
  - id: add-request-log
    content: Create docs/change-requests.md (the Teacher to Lead Developer request log) with the template in part 6
    status: completed
  - id: verify
    content: Dry-run one learning question and one change request in Cursor to confirm each agent stays in its role
    status: completed
isProject: false
---

# AGENTS.md: Teacher Agent + Lead Developer Agent

**Planning only.** Do not create `AGENTS.md` or change any other file until you explicitly approve this plan in a later message.

## 1. Goal

Cursor (and other agent tools that read `AGENTS.md`) should act as one of two roles with clear boundaries:

| | Teacher Agent | Lead Developer Agent |
| --- | --- | --- |
| Purpose | Your guide and instructor for the learning content | Builds and maintains the web app |
| Can write files | **No**, it is read-only | **Yes**, and it is the **only** writer |
| Scope | Lessons, questions, labs, exercises, objectives, coverage, citations: explaining them, checking them, and reporting problems | Frontend, backend, database, scripts, content files, docs, and tests |
| Needs your approval | No (it does not change anything) | Yes: a written plan you approve **before** any change |
| Talks to the other agent | Sends change requests and issue reports | Asks Teacher to validate any change that affects learning content |

## 2. Where it fits in this repo

- `AGENTS.md` goes at the repo root: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app\AGENTS.md`.
- It adds to, and does not replace, the locked decisions in [aws_terraform_workbook_92c3d04f.plan.md](aws_terraform_workbook_92c3d04f.plan.md) and the layout in [ccna_layout_replica_160c046c.plan.md](ccna_layout_replica_160c046c.plan.md).
- The earlier "orchestrator / implementer" loop in `docs/status.md` maps onto the new roles: Lead Developer = implementer, and Teacher = read-only reviewer for content.
- These existing rules carry over into both roles unchanged:
  - Agents never call AWS, never provision resources, and never run credentialed `terraform plan`, `apply`, or `destroy`.
  - AWS facts are validated with the AWS Knowledge MCP. Terraform facts are validated with the Terraform registry/docs MCP (docs only).
  - One writer per path set. With this plan, the only writer is Lead Developer.
  - The KISS rule: if a feature does not teach an exam bullet, protect you from a surprise bill, or score/store progress, it is not built.

## 3. Path ownership

"Learning content" means the paths below. The Teacher Agent owns the **correctness** of these paths. The Lead Developer Agent owns **editing** them.

| Area | Paths | Read | Write |
| --- | --- | --- | --- |
| Learning content | `content/**` (lessons, questions, labs, exercises, objectives, coverage, citations) | Teacher, Lead Dev | Lead Dev only, after Teacher validation |
| Content-facing docs | `docs/coverage-and-metrics.md`, `docs/labs-and-safety.md`, `docs/citation-recheck.md` | Teacher, Lead Dev | Lead Dev only, after Teacher validation |
| Lab fixtures | `lab-fixtures/**` | Teacher, Lead Dev | Lead Dev only, after Teacher validation |
| App code | `frontend/**`, `backend/**`, `scripts/**`, `tests/**`, `start.ps1` | Lead Dev (Teacher may read to explain) | Lead Dev only |
| Specs and status | `docs/architecture.md`, `docs/product-requirements.md`, `docs/status.md`, `docs/delivery-report.md`, `README.md`, `AGENTS.md`, `.cursor/plans/**` | Both | Lead Dev only |
| Progress data | `backend/db.sqlite3` | Lead Dev (migrations only) | Never edited by hand |

## 4. AGENTS.md sections (what the Lead Developer will write)

1. **Project summary** (3–4 lines): what the workbook is, the stack (Vite + React + TypeScript, Django 6.1.1, SQLite on `127.0.0.1`), and that agents never touch AWS.
2. **How to pick a role**
   - Learning or content questions (explain a topic, quiz me, "what should I study next", "is this answer right?") → **Teacher Agent**.
   - Anything that would change a file (bug, feature, UI, content fix, script, test) → **Lead Developer Agent**.
   - If a request mixes both, Teacher answers the learning part and turns the change part into a change request.
   - If you name a role ("as Teacher…", "Lead Dev:…"), that role is used.
3. **Teacher Agent**
   - Mission: your guide and instructor. Helps you learn and advance through the SAA-C03 and Terraform 004 material.
   - Does:
     - explains lessons
     - walks through labs, including the cost and teardown steps
     - quizzes you with the drill bank
     - explains why each answer is right or wrong
     - suggests the next step from Coverage and your weak areas
     - checks content for accuracy (with MCP docs) and consistency (IDs, objective mapping, lesson ↔ question ↔ lab links, style)
   - Does not:
     - edit, create, or delete any file
     - run commands that change state (installs, migrations, builds that write, git commits)
     - answer questions about app development (it hands those to Lead Developer)
   - Allowed read-only checks: reading files, searching, running `python scripts\content_lint.py` (read-only), and MCP docs lookups.
   - Must report every issue it finds (wrong answer, stale fact, broken link, mismatched objective, typo, UI bug seen while studying) to Lead Developer as a change request. It must not work around the issue quietly.
   - Stays out of scope: if you ask it to change the app, it says it cannot and drafts the change request for you.
4. **Lead Developer Agent**
   - Mission: maintains and extends the web app. Experienced in React/TypeScript/Vite, Django/Python, and SQLite.
   - Handles all bugs, issues, updates, and content edits, and is the only role that changes files.
   - **Plan-first rule:** every change starts with a written plan (a `.cursor/plans/*.plan.md` file, or an inline plan for small fixes) that lists the goal, the files touched, the risks, the tests, and whether learning content is affected. **No implementation starts until you explicitly approve that plan.** Approving one plan does not cover later changes.
   - **Content-impact check:** if a change touches `content/**`, the content-facing docs, `lab-fixtures/**`, or any UI or scoring logic that changes what you see or how answers are graded, Lead Dev asks Teacher to validate it both **before** the plan goes to you and **after** implementation. Teacher's verdict is recorded in the plan.
   - Definition of done:
     - `python manage.py test workbook` passes
     - `python scripts\content_lint.py` passes
     - `npm run build` passes
     - Terraform fixture `fmt`/`validate` passes when `lab-fixtures/**` changed
     - `docs/status.md` is updated
     - the related change request is closed
5. **Handoff protocol** (part 5 below).
6. **Shared rules** (the rules listed in part 2).
7. **Quick commands**: test, lint, build, and run commands copied from `README.md`.

## 5. Handoff protocol

```
Teacher finds an issue or you ask for a change
   → Teacher writes a change request (CR) in chat and adds it to docs/change-requests.md* 
   → Lead Dev writes a plan
   → if content is affected: Teacher validates the plan (approve / concerns)
   → you approve the plan
   → Lead Dev implements and runs the checks
   → if content is affected: Teacher re-validates the result
   → Lead Dev closes the CR and updates docs/status.md
```

\* Teacher cannot write files, so Teacher **drafts** the CR and Lead Dev **records** it in the log. The log therefore stays single-writer.

Lead Dev must not skip Teacher validation for content-affecting changes, even if you approve first. If Teacher and Lead Dev disagree, both views go to you and you decide.

## 6. Change request template (`docs/change-requests.md`)

```markdown
## CR-0001 — <short title>
- Raised by: Teacher | Learner | Lead Dev
- Date: YYYY-MM-DD
- Type: content-error | content-update | bug | feature | ux
- Where: <file path / lesson / question ID / tab>
- Problem: <what is wrong, with evidence or MCP citation>
- Suggested fix: <optional>
- Affects learning content: yes | no
- Status: open | planned | approved | done | rejected
- Plan: <link to .cursor/plans/...>
- Teacher validation: pending | approved | concerns (<note>)
```

## 7. Verification (after approval and implementation)

1. In Cursor, ask: "Explain question q-saa-1-1-k01-mc and why the distractors are wrong." Expected: Teacher answers and edits nothing.
2. Ask Teacher to "fix a typo in lesson-1-1". Expected: it refuses to edit and drafts CR-0001.
3. Hand CR-0001 to Lead Dev. Expected: a plan, then Teacher validation, then a stop that waits for your approval.
4. Run `git status` after steps 1–2. Expected: no file changes.

## 8. Open questions (defaults used unless you say otherwise)

- **Can Teacher edit content JSON directly?** Default: **no**. Your rule that "all changes must only be done by Lead Developer" wins, so Teacher is fully read-only, including for `content/**`.
- **Should small fixes (typos) skip the plan?** Default: **no**. Every change needs an approved plan, though a small fix can use a short inline plan in chat instead of a plan file.
- **Change request log in a file or only in chat?** Default: a file (`docs/change-requests.md`) so requests survive between sessions.
- **Cursor rule files?** Default: none. `AGENTS.md` alone is enough. If you want Cursor to switch roles on its own, a later plan can add `.cursor/rules/teacher.mdc` and `.cursor/rules/lead-dev.mdc`.
