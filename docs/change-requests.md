# Change requests

Teacher drafts each request in chat. Lead Developer records it here. The log stays single-writer.

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

## CR-0005 — Rewritten labs still cannot be completed end to end
- Raised by: Teacher
- Date: 2026-09-25
- Type: content-error
- Where: `content/labs/gl-02.json` through `gl-21.json`, `content/labs/ul-01.json` through `ul-21.json`
- Problem: Follow-up review of the CR-0004 rewrite. GL-06 through GL-21 steps are outlines without runnable commands ("Use minimal VPC with two public subnets", literal `aws lambda create-function ...`). Steps s12–s15 are the same boilerplate on every lab, including "ENIs, then VPC" on labs with no VPC. Teardown on most labs references variables no step sets (`$EndpointId`, `$IgwId`, `$NaclId`, `$AlbArn`, `$ZoneId`) and misses resources, so `delete-vpc` fails on GL-05, GL-06, GL-08, GL-14, GL-16, GL-18, GL-21 and UL-05, UL-06, UL-16. Roles that teardown deletes are never created (GL-10, GL-11 Lambda role; GL-12 Step Functions role; GL-19 EKS role). Wrong commands: `{{Key=...}}` tag syntax (GL-05, GL-06, GL-07); `LocationConstraint=us-east-1` (GL-02, invalid in us-east-1); single-quoted `$CreatedAt` never expands (GL-02); unclosed backtick (GL-04, GL-10, GL-13, GL-18); `aws macie2 disable-macie --status DISABLED` (UL-02; use `update-macie-session --status PAUSED`). GL-02 teardown leaves delete markers, so a versioned bucket will not delete. GL-06 has no internet gateway. GL-20 omits `-var bucket_suffix`, the out-of-band change, and refresh from the catalog. UL-01 criteria mention users and MFA devices UL-01 never creates, and a GL-01 budget that GL-01 teardown deletes. UL teardown is one to four lines for multi-resource labs.
- Suggested fix: Rewrite each lab to GL-01 depth: every created resource has a command that captures its id into a variable, teardown deletes exactly those in dependency order, and each step names what success looks like. Fix the listed command errors.
- Affects learning content: yes
- Status: done
- Plan: CR-0005 batches A–E (2026-09-25); `scripts/scan_lab_placeholders.py` added
- Teacher validation: pending post-implementation re-review

## CR-0004 — Labs are not ready to work on
- Raised by: Teacher
- Date: 2026-09-25
- Type: content-error
- Where: `content/labs/gl-02.json` through `gl-21.json`, `content/labs/ul-01.json` through `ul-21.json`, `frontend/src/components/LabCard.tsx`
- Problem: Only GL-01 is followable. GL-02 through GL-21 keep generic template steps ("Create the primary resource for …") with "Step N" titles and no service commands. All 21 unguided labs use placeholder criteria ("Criterion N: demonstrate … requirement #N") and a generic scenario. Teardown on 41 labs is a tag search plus comments, not real deletes. Each unguided teardown searches `LabId=gl-NN` instead of its own id. Every lab says 90 minutes, and every lab from GL-02 through GL-19 is module A1, both contradicting `docs/labs-and-safety.md`. No lab has `difficulty`, so all show two pips. The cost chip reads "See lab guide" on 41 labs because the card ignores `sameHourEstimateUsd`.
- Suggested fix: Rewrite each guided lab to the GL-01 standard from the catalog note, write real unguided scenarios and criteria, write real ordered teardown per lab, correct times and modules, add difficulty, and show the stored cost.
- Affects learning content: yes
- Status: superseded
- Plan: batch 1 done 2026-09-25 (cost chip, minutes, module, difficulty, UL teardown LabId); batches 2–4 done 2026-09-25 (`scripts/cr0004_rewrite_labs.py` merged guided steps and UL scenarios/criteria/teardown for gl-02–gl-21 and ul-01–ul-21; GL-01 unchanged)
- Teacher validation: superseded by CR-0005 (2026-09-25)

## CR-0003 — Unguided labs are not on the Labs tab
- Raised by: Learner
- Date: 2026-09-25
- Type: ux
- Where: Labs tab; `frontend/src/data/curriculum.ts`; `content/labs/ul-01.json` through `ul-21.json`
- Problem: 42 lab files exist. The curriculum lists only GL-01 through GL-21, so UL-01 through UL-21 never render. Those files have acceptance criteria, not steps, and the card only draws steps.
- Suggested fix: List each UL beside its GL pair, and render acceptance criteria as the checkable list, with the scenario, hints, rubric, and teardown. Keep the solution gated. Add the hourly UL ids to the cost-risk set.
- Affects learning content: yes
- Status: done
- Plan: inline plan in chat, approved by the learner on 2026-09-25 ("approved")
- Teacher validation: approved after implementation (UL-01 through UL-21 sit beside their guided pairs; criteria are checkable; placeholder wording was left as written)

## CR-0002 — GL-01 Before you start runs together, and the steps are not followable
- Raised by: Learner
- Date: 2026-09-25
- Type: ux
- Where: Labs tab, GL-01; `frontend/src/components/LabCard.tsx`; `content/labs/gl-01.json`
- Problem: The card shows one run-on line: "Set $env:AWS_PROFILE and $env:AWS_REGION='us-east-1'Run aws sts get-caller-identityReview same-hour and 24-hour estimates". The JSON already has those as three strings. `LabCard` puts the whole array in one `<li>`, and the type says `beforeYouStart` is a string. The same array shape is on all 21 guided labs. Separately, GL-01 steps are placeholders ("Create the primary resource for Identity, budget, and preflight") and do not tell the learner how to create the IAM user, MFA, alert-only budget, tags, permission boundary, or kill-switch snippet described in `docs/labs-and-safety.md`.
- Suggested fix: Render each `beforeYouStart` string as its own list item. Rewrite GL-01 steps so each one names the action, the command or console path, and what success looks like.
- Affects learning content: yes
- Status: done
- Plan: inline plan in chat, approved by the learner on 2026-09-25 ("Plan approved")
- Teacher validation: approved after implementation (list items render separately; GL-01 steps name the IAM user, MFA, boundary, alert-only budget, tags, and ordered teardown)

## CR-0001 — Lesson 1-1 drill IDs use dots
- Raised by: Teacher
- Date: 2026-09-25
- Type: content-error
- Where: `content/lessons/lesson-1-1.json` `drillIds`
- Problem: All 11 drill IDs used a dot (`q-saa-1.1-k01-mc`). Question files use hyphens (`q-saa-1-1-k01-mc`).
- Suggested fix: Replace the dot with a hyphen in each `drillIds` entry.
- Affects learning content: yes
- Status: done
- Plan: inline plan, approved by the learner on 2026-09-25 ("Fix the ID mismatch")
- Teacher validation: approved (hyphenated IDs match the 11 question files)

## CR-0006 — CSRF trusted origins block drill and checkpoint saves
- Raised by: Lead Dev (run-2 FULLSTACK-230, PYTHON-230, ITMGR-230, STUDENT-211)
- Date: 2026-09-25
- Type: bug
- Where: `backend/config/settings.py`, `frontend/src/api/client.ts`, `backend/workbook/tests/test_scoring_and_api.py`
- Problem: Browser POSTs from Vite send Origin `http://127.0.0.1:5173`. Django CSRF rejects them because `CSRF_TRUSTED_ORIGINS` was unset. UI showed bare "Forbidden".
- Suggested fix: Set `CSRF_TRUSTED_ORIGINS` from CORS origins; test POST with Origin; plain 403 message.
- Affects learning content: no
- Status: done
- Plan: `.cursor/plans/lead_dev_fix_loop_20260925.plan.md` WP1
- Teacher validation: n/a (not content)

## CR-0007 — Question GET returns rationale before submit
- Raised by: Lead Dev (FULLSTACK-201, PYTHON-201, PYTHON-203, ITMGR-201)
- Date: 2026-09-25
- Type: bug
- Where: `backend/workbook/content_loader.py` `public_question`
- Problem: GET `/api/questions/<id>` included `rationale` after stripping only `correctAnswerIds`.
- Suggested fix: Strip `rationale` on GET; return it only from `POST /api/attempts`. UI already uses the attempt result.
- Affects learning content: no
- Status: done
- Plan: WP2
- Teacher validation: n/a

## CR-0008 — Thirteen lessons still use dotted drill IDs
- Raised by: Teacher (F-201)
- Date: 2026-09-25
- Type: content-error
- Where: `content/lessons/lesson-1-2.json` through `lesson-4-4.json`
- Problem: `drillIds` used `q-saa-1.2-…` while question files are `q-saa-1-2-…`. Recount: 13 lessons, 178 IDs.
- Suggested fix: Hyphenate those IDs. Lint rule: every `drillIds` entry must exist as a question file.
- Affects learning content: yes
- Status: done
- Plan: WP3
- Teacher validation: approved (hyphen-only; no prose change; lint PASS)

## CR-0009 — Template drill bank
- Raised by: Teacher (F-202)
- Date: 2026-09-25
- Type: content-update
- Where: `content/questions/q-*.json`
- Problem: Shared stem skeletons and answer-position bias.
- Suggested fix: Rewrite the shared stem, rotate keys, lint the old skeleton and per-module key share.
- Affects learning content: yes
- Status: done
- Plan: WP4
- Teacher validation: concerns (stems are no longer identical, but many still share one scenario frame)

## CR-0010 — Lab command and sequence defects
- Raised by: AWS Architect / Teacher
- Date: 2026-09-25
- Type: content-error
- Where: `content/labs/gl-05.json`, `gl-07.json`, `gl-08.json`, `gl-17.json`, `gl-18.json`, `gl-19.json`, `gl-20.json`, `gl-21.json`, `ul-01.json`, `ul-05.json`
- Problem: Run-2 confirmed CLI and sequence issues (user data, NACL, Athena DDL, EFS, tags, GL-20 wording).
- Suggested fix: WP5 JSON edits after Teacher pre-validation.
- Affects learning content: yes
- Status: done
- Plan: WP5
- Teacher validation: approved for the listed command edits (GL-05/07/08/17/18/19/20/21, UL-01/05). Broader lab rewrites were not redone.

## CR-0011 — Teardown variable scan is a no-op
- Raised by: AWS Architect (AWS-205)
- Date: 2026-09-25
- Type: bug
- Where: `scripts/scan_lab_placeholders.py`
- Problem: Cleanup-variable check is disabled (`pass`).
- Suggested fix: WP6.
- Affects learning content: yes
- Status: done
- Plan: WP6
- Teacher validation: approved (scanner flags unset teardown variables; unused ids are initialized to $null)

## CR-0012 — Lessons not reachable from the app
- Raised by: Student (STUDENT-203)
- Date: 2026-09-25
- Type: ux
- Where: Start / Labs navigation
- Problem: Only A0 is rendered in the UI; other lessons are API-only.
- Suggested fix: WP7, within the locked layout plan.
- Affects learning content: yes
- Status: done
- Plan: WP7
- Teacher validation: approved (Start here lesson picker; permissions-boundary paragraph on A0)

## CR-0013 — Front-end quality (mock exam, N+1, routing, a11y)
- Raised by: Full-Stack
- Date: 2026-09-25
- Type: ux
- Where: `frontend/src/**`
- Problem: FULLSTACK-202 through 213 still open.
- Suggested fix: WP8.
- Affects learning content: no
- Status: done
- Plan: WP8
- Teacher validation: n/a

## CR-0014 — Selected-id validation and JSON errors
- Raised by: Python
- Date: 2026-09-25
- Type: bug
- Where: `backend/workbook/views.py`, `scoring.py`
- Problem: PYTHON-204/205. PYTHON-202/206 need a product call.
- Suggested fix: WP9.
- Affects learning content: no
- Status: done
- Plan: WP9
- Teacher validation: n/a. PYTHON-202 and PYTHON-206 stay local-only by design.

## CR-0015 — Citations and coverage status
- Raised by: Teacher / IT Manager
- Date: 2026-09-25
- Type: content-update
- Where: `content/citations/**`, `content/coverage/saa_registry.json`
- Problem: Reused citation URL; registry rows `implemented_unverified`; `mcpStatus` pending.
- Suggested fix: WP10 with MCP batches.
- Affects learning content: yes
- Status: done
- Plan: WP10
- Teacher validation: concerns (repeated wrong doc URLs removed from lesson bodies; bullets do not yet have unique official URLs)

## CR-0016 — Training policy docs and audit metrics
- Raised by: IT Manager
- Date: 2026-09-25
- Type: feature
- Where: `docs/labs-and-safety.md`
- Problem: Sandbox guidance, pricing footnotes, and whether audit-grade metrics stay in scope (KISS).
- Suggested fix: WP11 after you decide scope.
- Affects learning content: yes
- Status: done
- Plan: WP11
- Teacher validation: approved for the sandbox note. Audit-grade multi-user metrics stay out of scope (KISS).

## Template

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
