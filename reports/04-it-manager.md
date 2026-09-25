# IT Manager Evaluation (Corporate Training Lens)

**Run-2 Phase 3 — Strict eval.** Gate 0 Result A: **paper-feedback mode** for all drill submits and lab checkpoints until CSRF trusted origins are fixed.

## Evaluation Scope

| Area | Inspected | Evidence |
|------|-----------|----------|
| Routes | `/start`, `/labs`, `/exam`, `/coverage` (desktop UI text) | `reports/evidence/ui/*.md` |
| Bootstrap / errors | App shell, API client, lab reload hook | `app-map.md`, `useWorkbookBootstrap.ts`, `client.ts`, `App.tsx` |
| Progress & readiness | Header, Start here cards, export schema | `Header.tsx`, `StartHereTab.tsx`, `progress.py`, API snapshots |
| Content triage | Automated scan counts | `content-scan.md`, `content-scan.json` |
| Gate 0 | POST attempts + GL-01 checkpoint | `gate0-save-failure.md`, EV-GATE0-001/002 |
| Cross-role Confirmed | Engineering + AWS + Student reports (read-only) | `05`, `06`, `03`, `01` reports; EV-ITMGR-220/221 |

## Corporate Training Fit Summary

**Subjective Observation:** The product is a **credible personal certification workbook** for engineers with a sanctioned AWS sandbox and time for self-directed study. It is **not ready** as an enterprise L&D system with mandatory completion, manager attestation, or audit-grade drill metrics until **ITMGR-230** (Critical) and **ITMGR-201** (High, Confirmed with PYTHON-201) are addressed.

**Time to first value:** Good when Django + Vite are running — Start here orients A0 safety, GL-01 path, and the four-tab model (EV-ITMGR-201).

**Professionalism:** CCNA-style shell and consistent tab chrome read as an internal tool; stale mock-exam copy (FULLSTACK-202, Confirmed) is a comms gap for programs advertising full SAA-C03 mock exams.

**Operational model:** Per-machine install, SQLite on disk, no login, progress via Export JSON (`schemaVersion` 1) — suitable for **individual backup**, not HRIS or manager rollups without a separate pipeline (EV-ITMGR-215, EV-ITMGR-222).

## Training readiness — Go / No-Go

| Use case | Verdict | Conditions (all must hold) | Primary evidence |
|----------|---------|----------------------------|------------------|
| Mandatory completion tracking / LMS integration | **No-Go** | Fix **ITMGR-230** so POST attempts and lab checkpoints persist; add trusted origins and regression test | EV-GATE0-001, EV-GATE0-002 |
| Manager attestation (“employee finished drills/labs”) | **No-Go** | Same as above **plus** fix **ITMGR-201** / PYTHON-201 (no prefetch of full rationales); document that header % is self-reported checkpoints, not verified AWS execution | EV-ITMGR-209, EV-ITMGR-220 |
| Compliance-style reporting on exam readiness scores | **No-Go** | ITMGR-230 + ITMGR-201; treat readiness API as self-study signal only until tamper-evident scoring exists | EV-ITMGR-207, EV-ITMGR-214 |
| Voluntary self-study (engineer-owned laptop, no HR tracking) | **Conditional Go** | Written **sandbox-only AWS policy** (ITMGR-205); employees skip using Coverage as executive sign-off (ITMGR-204); L&D accepts template-heavy drill bank until Teacher F-202 rewrite | EV-ITMGR-216, EV-ITMGR-219, EV-ITMGR-208 |
| Assigning live hourly labs (16 pairs) in company accounts | **Conditional Go** | Dedicated sandbox OU/accounts, SCPs, billing alerts, forbid production profiles; complete GL-01 budget lab first; acknowledge **AWS-201–203** Confirmed lab defects may inflate debug time and spend | AWS-201–203; EV-ITMGR-202 |
| Corporate-wide “exam ready” campaign from drill stats alone | **No-Go** | ITMGR-230 + content integrity stack (scan + Confirmed engineering/content findings below) | EV-ITMGR-217, EV-ITMGR-218 |

**Overall workforce rollout verdict:** **No-Go** for tracked corporate training; **Conditional Go** for optional, sandbox-governed self-study on local installs after CSRF fix and explicit policy comms.

## Adoption walkthrough

### New employee — first session (learner lens)

1. **Install and start stack** — Clone repo; run backend on `127.0.0.1:8000` and frontend on `127.0.0.1:5173` per project docs. If Django is down, the app shows a page-level error with remediation (EV-ITMGR-211, EV-ITMGR-212).
2. **Land on Start here (`/start`)** — Reads “Learn it by building it,” A0 threat model (local SQLite, $10 warning, agents never call AWS), and module workflow (EV-ITMGR-201). Readiness cards show **insufficient_evidence** until practice thresholds are met — honest for a new hire (EV-ITMGR-207).
3. **Open Labs** — Sees all **42** labs at 0%; guided cards expose cost/stop panels (EV-ITMGR-202). Employee runs CLI in **their own terminal** in a **sanctioned sandbox** — the app does not enforce account choice (ITMGR-205).
4. **Tick GL-01 checkpoints** — **Run-2 blocker:** each POST returns **403 Forbidden** / CSRF origin failure; UI shows bare `Forbidden` (ITMGR-230). Progress header does not advance from persisted data in this build.
5. **Exam drills (`/exam`)** — **429** questions listed; mock exam control disabled with “Phase 4 Locked” (EV-ITMGR-203, FULLSTACK-202). **Check answers** fails like labs (ITMGR-230); learner must grade on paper until fix.
6. **Coverage (`/coverage`)** — Registry of **189** objective rows for self-planning; every sampled row is `implemented_unverified` with gap text about MCP re-check (ITMGR-204). New hire should **not** read this as “company certified the curriculum.”
7. **Backup habit** — Export JSON from Start here for personal records; IT should define whether exports may be stored as “evidence” (EV-ITMGR-222).

**First-week expectation (Subjective Observation):** With CSRF fixed and sandbox policy in place, a motivated engineer can reach GL-01 + A0 drills + one module path in a few evenings; **without** the fix, the app behaves like a read-only content browser with misleading interactive controls.

### Manager — “how do I see progress?” (no dedicated manager UI)

There is **no manager dashboard, SSO, or multi-user store** (EV-ITMGR-215). A line manager today can only:

| What manager wants | What the product actually offers | Caveat |
|--------------------|----------------------------------|--------|
| “Did they finish the program?” | Ask employee to **Export progress** JSON or show local app | Same Windows profile = shared SQLite; no identity |
| “Percent complete” | Header: “Saved in this browser” + **% steps · labs done** (EV-ITMGR-213) | Denominator may omit labs that failed to load (ITMGR-202); checkpoints are self-reported, not verified in AWS |
| “Exam ready for SAA?” | Start here readiness cards + `/api/metrics/readiness` | Baseline snapshot: insufficient_evidence, zero attempts (EV-ITMGR-206, EV-ITMGR-207); **not** tamper-evident (ITMGR-201) |
| “Which objectives are covered?” | Coverage tab / export of registry | Status is author workflow, not validation (ITMGR-204) |
| “Prove they passed drills” | Attempt history inside export | **Blocked run-2:** no new attempts persist (ITMGR-230); prefetchable rationales undermine integrity (ITMGR-201) |

**Manager comms template (Subjective Observation):** Position the workbook as **self-study with optional JSON export**, not as a system of record, until ITMGR-230 and ITMGR-201 are closed.

## Wrong-content and integrity risk at workforce scale

Counts are from saved scan output (EV-ITMGR-217, EV-ITMGR-218), not hand-typed.

| Signal | Count | Denominator | IT interpretation |
|--------|-------|-------------|-------------------|
| Question bank size | 429 | — | Full cohort exposed to same items |
| Scan finding rows | 721 | 429 questions + labs | Triage volume; not 721 unique defects |
| `heuristic_longest_correct` | **380** | 429 (~**88.6%**) | Systemic “guess longest answer” risk if pattern is real |
| `has_cli_or_code_snippet` (review flag) | 320 | 429 | Higher support burden; needs author review |
| UL missing `beforeYouStart` | **21** | 21 UL labs | Preflight gap for employees assigned “all labs” |
| Citation `pending_recheck` | **427** | question/citation records | No MCP-verified accuracy claim for whole bank |

**Cross-reference — other roles’ Confirmed items (corroboration, not automatic severity upgrade):**

| ID | Role | Confirmed issue | Workforce scale if unfixed |
|----|------|-----------------|---------------------------|
| PYTHON-201 / FULLSTACK-201 | Python / Full-Stack | GET question payloads include full **rationales** before attempt | Any learner or script on localhost can harvest **429** explanations — drills unsuitable for proctored or compliance use (ITMGR-201) |
| FULLSTACK-230 / PYTHON-230 | Full-Stack / Python | Same CSRF root cause as ITMGR-230 | **Zero** reliable completion data for entire cohort |
| AWS-201 | AWS | GL-08 AL2023 + PowerShell user data | Hourly ALB/EC2 debug spend, failed validation across anyone assigned networking capstone |
| AWS-202 | AWS | GL-05 NACL deny-all ingress semantics | Wrong networking mental model at scale |
| AWS-203 | AWS | GL-17 missing Athena DDL | Blocked analytics lab path |
| AWS-204, AWS-205 | AWS | Teardown / variable hygiene (Confirmed) | Elevated orphaned-resource risk in shared sandboxes |
| STUDENT-201 | Student | UL-01 assumes GL-03 bucket off lesson path | Silent failure mode for employees skipping GL order |
| STUDENT-211 | Student | Exam submit **Forbidden** in UI (now explained by Gate 0) | Same as ITMGR-230 for all employees on standard Vite origin |
| FULLSTACK-202 | Full-Stack | Mock exam disabled / stale label | Program credibility gap for “full exam prep” messaging |

**Teacher findings (Likely, not Confirmed — still scale the risk):** **F-202** (~227 template MC stems) explains most of the **380** longest-choice hits; **F-201** (**13** lessons with drill ID dot/hyphen mismatch) breaks lesson-driven drill paths for a subset of modules. Together with Confirmed rationale leak, L&D should assume **most drill attempts do not measure exam-realistic judgment** until content and API fixes land.

## Confirmed Issues

### ITMGR-230 — Save failure blocks completion tracking (Gate 0)

- **Severity:** Critical
- **Category:** api, ux
- **Location:** `POST /api/attempts`, `POST /api/labs/<id>/checkpoints` from `http://127.0.0.1:5173`
- **Evidence:** EV-GATE0-001, EV-GATE0-002; `reports/evidence/gate0-save-failure.md`
- **Description:** Gate 0 reproduces **403 Forbidden** with Django text `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins` on drill submit and GL-01 checkpoint tick. UI `[role=alert]` shows `Forbidden`. `CORS_ALLOWED_ORIGINS` includes Vite; **`CSRF_TRUSTED_ORIGINS` is missing** the same origin.
- **Impact:** **Workforce-scale:** No persisted attempts, checkpoints, cost entries tied to POST paths, or trustworthy header progress for **any** employee on the standard dev URL. Mandatory training records are impossible. Managers see stale or zero SQLite data while UI implies interactivity. Drills and lab checklists become read-only; only paper grading works (plan §4 paper-feedback mode).
- **Reproduction / Validation:** Follow steps in `gate0-save-failure.md` (exam **Check answers** + GL-01 first checkpoint).
- **Recommended Improvement:** Add `http://127.0.0.1:5173` (and 5174 if used) to `CSRF_TRUSTED_ORIGINS`; add API test that POST from allowed Origin succeeds; document in corporate rollout checklist as release gate.
- **Confidence:** Confirmed
- **Related:** FULLSTACK-230, PYTHON-230, STUDENT-211

### ITMGR-201 — Readiness and exam metrics are not audit-grade for management reporting

- **Prior:** ITMGR-001 (run-1); re-verified run-2 with EV-ITMGR-209 and PYTHON-201.

- **Severity:** High
- **Category:** security-local, api
- **Location:** `GET /api/questions/<id>`; Start here readiness (`/api/metrics/readiness`)
- **Evidence:** EV-ITMGR-209, EV-ITMGR-207, EV-ITMGR-220, EV-ITMGR-221
- **Description:** API snapshot for a sample question includes a full **rationale** on GET (no `correctAnswerIds` in payload, but explanations are prefetchable). UI hides text until submit, but localhost clients are not restricted. Readiness honestly reports `insufficient_evidence` when attempts are zero (EV-ITMGR-207); once attempts exist, counts are not tamper-evident.
- **Impact:** Using drill statistics or “first attempt” readiness for **compliance reporting, audits, or manager sign-off** would be misleading and easy to game (Confirmed defect tied to direct GET observation + PYTHON-201).
- **Reproduction / Validation:** Open `reports/evidence/api/question-q-saa-1-1-k01-mc.json`; compare PYTHON-201 reproduction in `06-senior-python-developer.md`.
- **Recommended Improvement:** Strip or gate rationales server-side until after scored attempt; document for L&D that metrics are self-study signals only; any future hosted deployment needs auth and aggregated reporting outside SQLite.
- **Confidence:** Confirmed
- **Related:** PYTHON-201, FULLSTACK-201, FULLSTACK-203

### ITMGR-204 — Coverage registry exposed to learners is entirely `implemented_unverified`

- **Prior:** ITMGR-004 (run-1).

- **Severity:** Medium
- **Category:** coverage-gap, consistency
- **Location:** Coverage tab; `GET /api/coverage`
- **Evidence:** EV-ITMGR-208, EV-ITMGR-204
- **Description:** API snapshot shows **189** registry rows; sampled rows carry `status: "implemented_unverified"` and gap strings such as MCP re-check pending. UI presents the registry for learner planning.
- **Impact:** Stakeholders may treat “implemented” language as **validated curriculum** without reading `gap` fields — executive over-confidence in coverage completeness (Subjective Observation on misread risk; status itself is Confirmed via API).
- **Reproduction / Validation:** Open `/coverage`; inspect `reports/evidence/api/coverage.json`.
- **Recommended Improvement:** Learner-facing badge “Mapped, not verified”; keep verification fields for authors; manager training deck should show a sample row with gap text.
- **Confidence:** Confirmed
- **Related:** TEACHER citation/`pending_recheck` (427 records, EV-ITMGR-218)

## Probable Concerns

### ITMGR-202 — Silent omission of failed lab loads distorts header progress

- **Prior:** ITMGR-002 (run-1).

- **Severity:** Medium
- **Category:** ux, frontend-bug
- **Location:** `frontend/src/hooks/useWorkbookBootstrap.ts` (`reloadLabs` empty catch)
- **Evidence:** EV-ITMGR-210, EV-ITMGR-213
- **Description:** Bootstrap loads every lab ID in parallel; failed `api.lab(id)` calls are skipped without surfacing which IDs failed. Header “% steps · labs done” uses only labs present in `labsById`.
- **Impact:** Partial API or content failures could show **inflated** completion percentages — managers trusting header % without export review get a false green signal (Likely; not reproduced with a simulated 404 in this pass).
- **Reproduction / Validation:** Code review at `useWorkbookBootstrap.ts:42-49`; inject 404 for one lab ID and compare header denominator.
- **Recommended Improvement:** Non-blocking banner listing missing lab IDs; keep partial UI usable.
- **Confidence:** Likely
- **Related:** FULLSTACK-208, FULLSTACK-203

### ITMGR-203 — Scan flags ~88% of questions with longest-choice heuristic

- **Prior:** ITMGR-003 (run-1); scan counts refreshed run-2 (380/429).

- **Severity:** Medium
- **Category:** drill-design, content-accuracy
- **Location:** Question bank; `reports/evidence/content-scan.json`
- **Evidence:** EV-ITMGR-217, EV-ITMGR-218
- **Description:** **380 / 429** questions flagged `heuristic_longest_correct` (**721** total scan rows including other kinds). Teacher **F-202** (Likely) attributes most hits to template MC stems and repeated distractors — independent pedagogy review, not IT re-verification.
- **Impact:** If employees shortcut drills, **cohort-wide** false confidence and poor exam transfer; pairs with ITMGR-201 so integrity is weak even before guessing heuristics.
- **Reproduction / Validation:** Run content scan script output in `content-scan.md`; sample IDs in Teacher F-202; spot-check 5 IDs from sample list.
- **Recommended Improvement:** Phased drill rewrite (F-202); after Teacher validates heuristic, extend `content_lint.py`; L&D set expectations that current bank is coverage mapping, not exam simulation.
- **Confidence:** Needs Verification
- **Related:** Teacher F-202, F-201; PYTHON-201

### ITMGR-205 — Live AWS labs require explicit corporate sandbox policy

- **Prior:** ITMGR-005 (run-1).

- **Severity:** High
- **Category:** lab-cost, lab-sequence
- **Location:** 42 labs; **16** hourly IDs in inventory; `docs/labs-and-safety.md`
- **Evidence:** EV-ITMGR-216, EV-ITMGR-219, EV-ITMGR-202, `reports/evidence/lab-commands.md`
- **Description:** Labs are **live_aws** CLI in the learner’s terminal. Product provides cost panels, $10 warning, typed cost-risk gates on eight GL labs, teardown narrative — but **no** enforcement of sandbox account or spend caps in software.
- **Impact:** Approving company-wide lab assignment without OU/SCP/billing guardrails risks **real AWS spend and security boundary violations**; hourly pairs plus **AWS-201** failure modes increase debug time and cost.
- **Reproduction / Validation:** Read REQ-L06 in `labs-and-safety.md`; confirm cost panels in `ui/labs.md`.
- **Recommended Improvement:** Publish corporate checklist: sandbox only, no prod profiles, billing alarms, GL-01 first, change windows for hourly labs; link AWS Confirmed defects in comms to trainers.
- **Confidence:** Subjective Observation
- **Related:** AWS-201, AWS-202, AWS-203, AWS-205

### ITMGR-206 — All 21 unguided labs lack `beforeYouStart` blocks

- **Prior:** ITMGR-006 (run-1).

- **Severity:** Low
- **Category:** lab-sequence, pedagogy
- **Location:** UL-01 … UL-21
- **Evidence:** EV-ITMGR-218
- **Description:** Content scan flags **21** `missing_beforeYouStart` on UL labs. Guided labs include preflight bullets; UL pairs may assume GL prerequisites — design may be intentional.
- **Impact:** Employees assigned “complete all labs” may skip preflight and hit **STUDENT-201**-style ordering gaps (Subjective Observation).
- **Reproduction / Validation:** Inspect scan JSON lab entries; compare GL-01 API reveal vs UL JSON.
- **Recommended Improvement:** UI link UL cards to paired GL preflight or shared A0 panel; align with Teacher F-205 if omission stays intentional.
- **Confidence:** Needs Verification
- **Related:** TEACHER F-205, STUDENT-201

## Items Requiring Verification

- **ITMGR-203:** Confirm with Teacher whether **380** longest-choice flags reflect real guessability vs template length artifact (F-202).
- **ITMGR-206:** Confirm with Teacher/product whether UL omission of `beforeYouStart` is intentional pair design per `intended-design.md`.

## Subjective Observations

- **Backend-down behavior (positive):** Clear page-level error when API unreachable (EV-ITMGR-211, EV-ITMGR-212).
- **Progress honesty (partial):** Header labels browser-local save; readiness explains insufficient evidence (EV-ITMGR-214) — good for individuals, not aggregatable.
- **SQLite, no auth (intended):** Acceptable solo; corporate blockers = shared profiles, no SSO, Export/RESET on keyboard (EV-ITMGR-215, EV-ITMGR-223).
- **Export for records:** Structured export suitable for learner backup; IT policy needed if JSON is stored as training evidence (EV-ITMGR-222).
- **Mock exam UX:** Disabled control with outdated Phase 4 label (EV-ITMGR-203, FULLSTACK-202).
- **Content lint PASS** in preflight reduces structural defects but not pedagogic patterns (EV-ITMGR-217 context).

## Strengths

- Four-tab architecture and Start here onboarding (A0, cost, teardown) fit security-aware engineers.
- Separation of **coverage registry** vs **readiness metrics** avoids a single fake “pass probability” if explained to managers.
- Hourly lab cost-risk typing on highest-spend guided labs (EV-ITMGR-219).
- Localhost CORS/CSRF design matches single-user SQLite threat model **once trusted origins are configured**.
- Actionable bootstrap errors when Django is stopped.

## Adoption Recommendations (Subjective)

1. **Block** mandatory tracked rollout until **ITMGR-230** is fixed and verified in browser (not curl-only).
2. **Block** compliance use of drill metrics until **ITMGR-201** / PYTHON-201 is fixed.
3. **Require** sandbox OU policy before assigning GL/UL hourly pairs; reference **AWS-201–203** in trainer notes.
4. **Train** managers that Coverage status is author state, not executive sign-off (**ITMGR-204**).
5. **Keep** deployment local-only; hosting would compound no-auth/SQLite issues without redesign.

## Post-discussion status

Run-2 strict Phase 5–6 (see `reports/discussion/round-b/ITMGR.md`, `revalidation.md`).

| Finding ID | Pre-discussion confidence | Final status | Notes |
|------------|---------------------------|--------------|-------|
| ITMGR-230 | Confirmed | **Confirmed Critical** | Gate 0 CSRF cluster |
| ITMGR-201 | Confirmed | **Confirmed High** (XF-201) | Rationale prefetch; separate from CSRF |
| ITMGR-204 | Confirmed | **Confirmed Medium** (XF-207) | Coverage comms |
| ITMGR-202 | Likely | **Likely Medium** | Silent lab skip (FULLSTACK-208) |
| ITMGR-203 | Needs Verification | **Needs Verification** | Heuristic vs F-202 template |
| ITMGR-205 | Subjective Observation | **Subjective Observation** | Round B WITHDRAW product-bug label; policy checklist |
| ITMGR-206 | Needs Verification | **Needs Verification** | UL beforeYouStart intentional? |
