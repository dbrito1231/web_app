---
name: Evaluation redo (extensive, six roles)
overview: "Planning only. Redo the full six-role, read-only evaluation of the SAA-C03 + Terraform 004 workbook with deeper coverage, stricter evidence gates, a two-round discussion, and computed (not hand-typed) summary counts. The app is NOT fixed first: the answer/checkpoint save failure (missing CSRF_TRUSTED_ORIGINS) is reviewed as-is, and learner feedback is checked in 'paper-feedback mode'. Supersedes run 1 (reports/ as of 2026-09-25)."
todos:
  - id: approve-plan
    content: User reviews and explicitly approves this plan (editing this file is not approval)
    status: completed
  - id: phase-0-gates
    content: Pre-flight, archive run 1, DB baseline, manifest, MCP check, save-failure confirmation (Gate 0)
    status: completed
  - id: phase-1-2-recon
    content: Repository + application reconnaissance, full content scan, 50% stratified sample, shared evidence pack
    status: completed
  - id: phase-3-reviews
    content: Six independent role reviews (parallel workflow agents)
    status: completed
  - id: phase-4-report-gate
    content: Report quality gate (structure lint + evidence cross-check); redo any failing role
    status: completed
  - id: phase-5-discussion
    content: Discussion round A (responses), round B (rebuttals), moderator transcript
    status: completed
  - id: phase-6-revalidation
    content: Neutral revalidation of disputed and Critical/High items
    status: completed
  - id: phase-7-synthesis
    content: Synthesis with script-computed counts; integrity checks; DB restore and fingerprint match
    status: completed
isProject: false
---

# Evaluation redo — extensive, six roles

**Planning only.** No evaluation starts until you approve this plan in a later message.

This plan re-uses the rules in `.cursor/plans/c-users-dbadmin-downloads-claude-web-ap-imperative-boot.md` (run-1 plan, "base plan"): hard constraints §3, role personas §7, severity and confidence §12, duplicates §13, disagreements §14. Anything below **overrides or adds to** the base plan. Where the two differ, this plan wins.

## 1. Why a redo

Run 1 produced useful results, but it had these gaps:

| Gap in run 1 | Fix in this run |
|---|---|
| Student "answers" came from a script picking the first choice, or from direct API POSTs; no feedback was ever seen | Student answers by reading, one question at a time, with no scripted clicking. Feedback is checked in paper-feedback mode (§4) |
| The answer-save failure ("Forbidden") was blamed on the test browser, with the wrong cause | Gate 0 captures the real server response and settles the cause with evidence |
| Reports skipped required sections and finding fields | Phase 4 report gate: a structure lint plus an evidence cross-check. Reports that fail are redone |
| Summary counts were typed by hand and wrong (lesson link count given as 20 instead of 13; "5 Confirmed" did not match the list) | Counts are computed by a script from the reports |
| About 25% question sample; 15 exercises; Student read lessons only as JSON | 50% question sample plus all flagged items; all 60 exercises; all 23 lessons read **in the app** |
| One discussion round, with a moderator summarising | Two rounds (responses, then rebuttals). The moderator may only quote |
| Run-1 findings were carried forward without re-checking | Run-1 findings are **hypotheses only**. Each must be re-verified from scratch before it is reported again |

## 2. Hard constraints (base §3, plus these)

1. **No app fixes.** The missing `CSRF_TRUSTED_ORIGINS` is reported, not fixed. Nothing outside `reports/**`, the baseline folder and this plan file is written.
2. **No scripted learner actions.** `javascript_tool` / CDP evaluate may only *read* (DOM text, computed styles, console). Every learner action (choosing an answer, clicking Check answers, expanding labs, ticking a checkpoint) is a single `computer` click or `form_input` done after reading the screen.
3. **No direct POSTs** from curl, PowerShell, or scripts to any `/api/*` route. POSTs may happen only by clicking the app's own buttons. Never click Reset or Import.
4. **Servers:** use the existing `127.0.0.1:5173` and `127.0.0.1:8000` only. Record their PIDs before and after. Never start a server, vite preview, or Playwright.
5. **DB:** restore the baseline before the first click; log every click that could write; restore at the end; the fingerprint must match (base §3.5). Because saving currently fails, few or no writes are expected, but the restore still runs.
6. **Report-only writes:** each agent writes only its own report, `reports/evidence/<ROLE>/`, and `reports/discussion/**`. Helper scripts go in the session scratchpad, **not** `reports/`.

## 3. Phase 0 — Gates (orchestrator, main session)

1. **Pre-flight.** Record the ports and PIDs for 5173 and 8000 and the `/api/health` response in `reports/evidence/preflight.md`. If either server is down, stop and ask the user.
2. **Archive run 1.** Move `reports/*` into `reports/archive/run-1/`. These are report files, so moving them is allowed; nothing is deleted. New reports start empty.
3. **DB baseline.** Reuse `C:\Users\dbadmin\Desktop\GitServ\ccna\eval-baseline\db.sqlite3.bak` if its fingerprint equals the current DB. Otherwise take a new backup-API snapshot into `eval-baseline/run-2/`. Record the fingerprint (iterdump SHA-256, row counts, integrity_check).
4. **Manifest.** Take a SHA-256 manifest of the repo (base plan exclusions) and save it as `eval-baseline/run-2/manifest-before.txt`.
5. **MCP check.** Confirm the Terraform MCP with `get_latest_provider_version`. For AWS docs, use `mcp-find`; **ask the user** before any `mcp-add`. Fallback is WebFetch of `docs.aws.amazon.com`.
6. **Gate 0 — confirm the save failure.** In a new built-in-browser tab:
   - Open `http://127.0.0.1:5173/exam` and select A0 question `q-a0-mc-001`.
   - Pick an answer by clicking, then click **Check answers** once.
   - Use `read_network_requests` to capture the `POST /api/attempts` request: its status, the response body (Django's reason text, e.g. "Origin checking failed …" vs the guard's "Origin not allowed"), and the request `Origin` header.
   - Repeat once for a lab checkpoint tick on GL-01.
   - Record everything in `reports/evidence/gate0-save-failure.md`.
   - Result A (403 with the CSRF origin reason): the save failure is **Confirmed**, and paper-feedback mode applies to all roles.
   - Result B (the save succeeds): stop, restore the DB, and tell the user. The failure was environment-specific, and the plan switches to normal UI feedback mode.

## 4. Paper-feedback mode (applies while saving fails)

The app cannot show results or explanations. Every role that judges drills does this for **each** item, in this order:
1. Read the question in the app. Write down your chosen answer(s) and your reasoning in the evidence log **before** looking at any key.
2. Click **Check answers** and record what the screen shows. The expected result is an error; record its exact wording.
3. Only then open `content/questions/<id>.json` to read the key and rationale. Record right or wrong, and whether the rationale would have taught you why.
4. Anything about how the feedback *screen* looks or behaves is **Needs Verification** (it cannot be seen while saving fails). Record it as a gap, not a finding.

Lab checkpoints are handled the same way: read the step in the app, try the tick, record the result, then continue on paper.

## 5. Phases 1–2 — Reconnaissance (orchestrator)

Same as base §5–§6, with these changes:

- **Full scan** (scratchpad script → `reports/evidence/content-scan.{json,md}`). Everything in the base plan, plus:
  - lesson `drillIds` compared exactly with the question file names (report the exact count per lesson)
  - HCL blocks in questions and labs, extracted to `reports/evidence/hcl-snippets.md`
  - PowerShell variables used before they are set, and cleanup variables that are never set, for every lab
  - glossary pass: technical terms that appear in questions or labs but not in any lesson
- **Sample** (seed `20260926`, recorded in `sample.md`):
  - Questions: **50% of every domain-task × type cell** (about 215), plus every scan-flagged item and every item containing code, CLI, or HCL.
  - Every lesson (23), lab (42), exercise (60), and citation (16) is in scope, as is the full coverage registry (189 rows).
- **Shared evidence pack:** every route at desktop, tablet, and mobile size. Each route gets `get_page_text`, an interactive `read_page`, console output, and network output. Unknown routes, deep links, and refresh on every tab are included. All API GET routes are captured, including error cases.

## 6. Role assignments (deeper than run 1)

Each agent: opens its own tab, starts from the shared pack, keeps its own evidence log, and uses finding IDs `<ROLE>-2xx` (the 2xx series marks run 2).

| Role | Must cover | Minimum volume |
|---|---|---|
| **1 Student** (base §7) | Cold start: the first 20 minutes with no instructions, logging every hesitation. Find and read **every lesson in the app** in curriculum order. Answer drills in paper-feedback mode. Before each question, check whether it was taught earlier (lesson text search). Keep a jargon log (term, first seen, where it is defined, if anywhere). Walk labs on paper, following them literally: GL-01, 02, 03, 05, 06, 08, 10, 17, 20, 21 and UL-01, 05, 20; say at which step you would get stuck. Complete one design exercise as a student would. Use the Coverage and readiness screens to decide "what next" | 60 drills: both A0; 3 per SAA task across 14 tasks (mixed mc/mr); 2 per TF group g1–g8. All 23 lessons. 13 labs. 1 exercise |
| **2 Teacher** (AGENTS.md persona, unchanged) | All 23 lessons for sequence and objective fit. Every objective in both objective files traced lesson → drill → lab (a coverage matrix). Every sampled question for how well it tests its objective and for rationale quality. All 60 exercises' rubrics. All 21 guided labs for objective fit. **Primary owner of Terraform accuracy**: all sampled TF questions, all HCL snippets, GL/UL-20/21, and the fixture, checked against HashiCorp docs and the registry MCP. Draft a CR for each confirmed issue | Full trace matrix; ≥60 TF items validated; ≥25 TF doc lookups |
| **3 AWS Architect** | Every SAA lesson. Every sampled SAA question's key, checked against docs. **Every** AWS CLI command in all 42 labs (flags checked against the CLI reference). Cleanup completeness and order for all 42 labs. Cost estimates checked against pricing pages. Scenario realism in all 60 exercises. SAA-C03 weights compared with mock-50 | All 42 labs command-reviewed; ≥50 AWS doc lookups |
| **4 IT Manager** | Adoption walk-through as a new employee and as a manager reading progress. Impact of the save failure on tracking. Scale of wrong-content risk (using the scan counts and the other roles' confirmed items). Cost and safety policy needs. Operational model (single-user local app, updates, backups via Export). Readiness to use for training: go / no-go with conditions | A go/no-go table with evidence |
| **5 Full-Stack** | Confirm the save-failure root cause end to end: browser → `client.ts` → Django middleware order → CSRF. Also cover: routing (unknown routes, deep links, refresh, back button); all interactive states in the drills and lab cards; how errors are shown (the bare "Forbidden" text); accessibility (keyboard-only drill run, focus order, labels, aria-live, contrast from computed styles); layout at 3 sizes; console and network warnings; eslint | Every interactive control inventoried; keyboard-only pass on all 4 tabs |
| **6 Python** | Middleware and CSRF interaction (why the Django tests missed the failure: the test client sends no Origin header). Every view: method guards, input checks, 404 vs 500 on bad input (GET only). `scoring.py` edge cases, by code reading plus existing tests. `readiness.py` maths. `content_loader.py` path handling. Gaps in the tests. Blind spots of `content_lint.py` compared with the scan | Every view function and every module reviewed; `manage.py test workbook` output attached |

Overlaps, and who owns each: same as the base §7 table, plus **save failure**: Full-Stack (UI and root cause) is primary; Python (server and tests), Student (impact), and IT Manager (tracking) are secondary.

## 7. Evidence rules (base §9, stricter)

- Every finding cites ≥1 `EV-` row. An EV row must contain the tool call or command that was actually run, with a verbatim excerpt of ≤30 words.
- **"Confirmed"** needs direct observation (screen, network, command output) **or**, for content accuracy, a cited doc. Code reading alone gives at most **Likely** for anything about runtime behaviour.
- Every **count** in a finding must come from a command or script whose output is saved in evidence.
- Every finding that re-uses a run-1 finding must list the run-1 ID as `Prior:` **and** carry fresh evidence.

## 8. Phase 3 — Independent reviews

Run six agents in parallel in one Workflow; about 22–26 agents in total across all phases. Agents may not read `reports/archive/run-1/` until their own report is done; after that, they may read it only to fill in `Prior:` links. Each report must follow the base plan's required structure exactly, including every heading and every finding field.

## 9. Phase 4 — Report quality gate (new)

A scratchpad script checks each report for:
- all required headings present;
- every finding has all 9 fields plus `Confidence` from the allowed list;
- every EV ID it cites exists in that role's evidence log;
- no "Confirmed" finding that rests only on code reading about runtime behaviour;
- the minimum volumes from §6 are met (counted from the evidence logs).

A report that fails goes back to the same agent with the failure list, for at most 2 retries. If it still fails, the report is flagged in the summary rather than silently accepted.

## 10. Phase 5 — Discussion (two rounds)

- **Round A (responses):** base §15 Round A. Each role answers every other role's Critical/High findings and every finding in its own area with AGREE / DISPUTE / REFINE / EXTEND and evidence.
- **Round B (rebuttals):** each role gets the Round A replies aimed at *its own* findings. It must accept, rebut with new evidence, or withdraw. Withdrawn findings stay in the report, struck through, with the reason.
- **Moderator:** builds `reports/discussion/group-discussion.md` per XF cluster, **only quoting** Round A and B text. It answers the 10 required discussion questions and outputs the revalidation queue.

## 11. Phase 6 — Revalidation

Two neutral verifier agents (one for content and AWS/TF, one for app and engineering) handle every disputed item and every Critical/High item not yet Confirmed. Verdicts go in `reports/discussion/revalidation.md`, and each report gets an appended `## Post-discussion status` table.

## 12. Phase 7 — Synthesis and close

1. A script computes all counts (by severity × confidence × role, XF clusters, disagreements) from the reports into `reports/evidence/summary-counts.json`. The synthesis agent may only copy numbers from that file.
2. The synthesis agent writes `reports/00-evaluation-summary.md` using the base plan's headings, plus **"Changes since run 1"** (new, dropped, and re-rated findings, each with its ID).
3. Orchestrator close:
   - restore the DB and confirm the fingerprint matches;
   - take a new manifest and confirm it matches the old one (outside `reports/`);
   - confirm the server PIDs are unchanged;
   - reset the browser viewports;
   - append `## Evaluation Integrity` to the summary.

## 13. Deliverables

```text
reports/
├── 00-evaluation-summary.md
├── 01-college-it-student.md … 06-senior-python-developer.md
├── discussion/{round-a/*, round-b/*, group-discussion.md, revalidation.md}
├── evidence/{preflight, gate0-save-failure, intended-design, inventory, sample, app-map,
│            content-scan.{json,md}, lab-commands, hcl-snippets, summary-counts.json,
│            api/*, ui/*, <ROLE>/{evidence-log, db-actions, …}}
└── archive/run-1/   (the previous run, unchanged)
C:\Users\dbadmin\Desktop\GitServ\ccna\eval-baseline\run-2\  (DB backup, fingerprints, manifests)
```

## 14. Acceptance criteria

- Gate 0 result recorded with the network evidence.
- All six reports pass the Phase 4 gate, or are flagged as failed in the summary.
- The §6 minimum volumes are met and shown by evidence-log counts.
- Every sampled ID appears in at least one evidence log.
- Two discussion rounds are complete; disagreements are preserved.
- Summary numbers match `summary-counts.json` exactly.
- DB fingerprint equals the baseline; no manifest changes outside `reports/`; server PIDs unchanged; no forbidden commands and no direct POSTs in any log.

## 15. Risks

| Risk | Mitigation |
|---|---|
| High token and time cost (about 24 agents, around 215 questions, 42 labs) | Phases can be resumed (Workflow resume). The user can cut the sample to 35% at approval time |
| The save failure hides the real feedback screen | Paper-feedback mode; the feedback screen is listed under "Needs Verification" until a fix lands |
| Several agents share one browser | One tab per agent; only Full-Stack resizes, and only its own tab |
| Enabling the AWS docs MCP changes config | Ask the user first; WebFetch fallback |
| Workflow agents drift from their persona | The persona text is pasted verbatim into each prompt; the Phase 4 gate checks the result |

## Learning content impact

None. This is an evaluation only: no content, UI, or scoring changes. Fixes found here go to the Lead Developer as separate CRs and plans.
