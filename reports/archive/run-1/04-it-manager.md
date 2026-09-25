# IT Manager Evaluation (Corporate Training Lens)

## Evaluation Scope

- Routes `/start`, `/labs`, `/exam`, `/coverage` — desktop UI excerpts in `reports/evidence/ui/`
- Shared evidence: `reports/evidence/app-map.md`, `intended-design.md`, `inventory.md`, `content-scan.md`, `lab-commands.md`
- API snapshots: `reports/evidence/api/progress.json`, `metrics-readiness.json`, `coverage.json`, `question-q-saa-1-1-k01-mc.json`
- Error paths: `frontend/src/hooks/useWorkbookBootstrap.ts`, `frontend/src/api/client.ts`, `frontend/src/App.tsx`
- Progress/readiness UX: `StartHereTab.tsx`, `Header.tsx`, `frontend/src/utils/progress.ts`
- Cross-reports read: `reports/01-college-it-student.md`, `reports/02-teacher.md`, `reports/03-senior-aws-solutions-architect.md`, `reports/05-senior-fullstack-engineer.md`, `reports/06-senior-python-developer.md`

## Corporate Training Fit Summary

**Verdict (Subjective Observation):** Strong as a **personal, local certification workbook** for engineers who already have a sanctioned AWS sandbox and time for self-study. **Weak as an enterprise L&D platform** without additional process: there is no authentication, no central progress store, no manager rollup, and drill integrity has a confirmed technical gap (PYTHON-001 / FULLSTACK-001) that undermines using practice metrics for compliance-style reporting.

**Time to first value:** Acceptable. Start here orients learners (A0 safety, GL-01 path, four-tab model). Brief “Connecting to local API…” on bootstrap is normal when the stack is healthy (`reports/evidence/ui/*.md`).

**Professionalism:** Header, tab shell, and CCNA-style layout read as a coherent internal tool, not a throwaway demo. Stale mock-exam copy (FULLSTACK-002) is a polish gap, not a blocker for drill-and-lab use.

**Operational model:** Per-machine install (Vite + Django + SQLite), content shipped in-repo, progress export JSON (`schemaVersion` 1) suitable for **individual backup** but not HRIS integration without a separate pipeline.

## Confirmed Issues

### ITMGR-001 — Readiness and exam metrics are not audit-grade for management reporting

- **Severity:** High
- **Category:** security-local, api
- **Location:** Drill bank + `GET /api/questions/<id>`; Start here readiness cards
- **Evidence:** EV-ITMGR-009, EV-ITMGR-007, EV-ITMGR-020, EV-ITMGR-021
- **Description:** Backend returns full question rationales on GET before any attempt. The UI hides them until submit, but any learner or script on localhost can prefetch all 429 explanations. Readiness API honestly returns `insufficient_evidence` with zero first attempts in the baseline snapshot, but once attempts exist, managers cannot treat “exam first attempt” counts as tamper-evident.
- **Impact:** **Confirmed defect impact (not subjective):** Using this app’s drill statistics for mandatory training attestation, audit samples, or “exam ready” HR flags would be misleading until PYTHON-001 is fixed.
- **Reproduction / Validation:** See PYTHON-001 reproduction; network panel on `/exam` load.
- **Recommended Improvement:** Fix PYTHON-001/FULLSTACK-001; document for L&D that metrics are self-study signals only; if corporate rollout is ever considered, add server-side gating and aggregated reporting outside SQLite.
- **Confidence:** Confirmed
- **Related:** PYTHON-001, FULLSTACK-001, FULLSTACK-003 (amplifies prefetch surface)

## Probable Concerns

### ITMGR-002 — Silent omission of failed lab loads distorts header progress

- **Severity:** Medium
- **Category:** ux, frontend-bug
- **Location:** `useWorkbookBootstrap.reloadLabs` (empty catch)
- **Evidence:** EV-ITMGR-010, EV-ITMGR-013
- **Description:** Bootstrap loads every lab ID from content summary in parallel; any failed `api.lab(id)` is skipped without surfacing an error. Header “% steps · labs done” is computed only over labs that loaded into `labsById`.
- **Impact:** A partial API or content glitch could show inflated completion percentages — progress looks healthier than reality (Likely; not reproduced in this pass).
- **Reproduction / Validation:** Code review of `useWorkbookBootstrap.ts:42-49`; simulate 404 on one lab ID and compare header denominator.
- **Recommended Improvement:** Aggregate load failures into bootstrap error or a non-blocking banner listing missing lab IDs; keep partial UI usable.
- **Confidence:** Likely
- **Related:** FULLSTACK-008 (42-lab bootstrap load), FULLSTACK-003 (429-question fetch); silent per-lab skip remains ITMGR-002-specific

### ITMGR-003 — Scan suggests widespread “longest choice” pattern across the drill bank

- **Severity:** Medium (pending content confirmation)
- **Category:** drill-design, content-accuracy
- **Location:** Question bank (429 items); `reports/evidence/content-scan.json`
- **Evidence:** EV-ITMGR-017, EV-ITMGR-018
- **Description:** Automated scan flagged **380 / 429** questions with `heuristic_longest_correct`. Plan rules treat heuristics as triage only, but at ~88% of the bank this is a **systemic** signal that distractors may be guessable even without rationale prefetch — especially harmful if employees shortcut drills before labs.
- **Impact:** **Subjective unless TEACHER/AWS confirm:** If confirmed as real answer leakage, wrong learning and false confidence scale to the whole cohort; combined with ITMGR-001, drills offer little integrity.
- **Reproduction / Validation:** Teacher/AWS sample review of flagged IDs (see `content-scan.md` sample list); compare choice length and stem templates.
- **Recommended Improvement:** Teacher-led stem/distractor rewrite for flagged clusters; extend `content_lint.py` with longest-choice rule once validated.
- **Confidence:** Needs Verification
- **Related:** Teacher F-02 (Confirmed template stems), F-01 (broken lesson drill linkage), `pending_recheck` on 427 questions (EV-ITMGR-018)

### ITMGR-004 — Coverage registry visible to learners is entirely “implemented_unverified”

- **Severity:** Medium
- **Category:** coverage-gap, consistency
- **Location:** Coverage tab / `GET /api/coverage`
- **Evidence:** EV-ITMGR-008, EV-ITMGR-004
- **Description:** Registry rows in the API snapshot carry `status: "implemented_unverified"` and gaps such as “MCP re-check and Phase 6 verification pending.” The UI exposes this registry for self-study planning — appropriate for developers — but a **manager interpreting Coverage as sign-off** would over-read completeness.
- **Impact:** **Subjective Observation:** Risk of stakeholders treating “implemented” in the UI as validated curriculum without reading `gap` fields.
- **Reproduction / Validation:** Open `/coverage`; inspect row status in `coverage.json`.
- **Recommended Improvement:** Rename or badge status for learner-facing copy (“Mapped, not verified”); keep internal owner fields for authors only if corporate packaging is added.
- **Confidence:** Confirmed (status field in API)
- **Related:** TEACHER-002 on citation/`mcpStatus` (427 questions `pending_recheck` per EV-ITMGR-018)

### ITMGR-005 — Live AWS labs in company accounts need explicit sandbox policy

- **Severity:** High (organizational / policy)
- **Category:** lab-cost, lab-sequence
- **Location:** 42 labs; 16 marked hourly in `inventory.md`; `docs/labs-and-safety.md`
- **Evidence:** EV-ITMGR-016, EV-ITMGR-019, EV-ITMGR-002, `reports/evidence/lab-commands.md`
- **Description:** Labs are **live_aws** CLI workflows (IAM, VPC, NAT, EC2, ALB, etc.) run in the learner’s own terminal — not simulated. Product includes cost panels, $10 **warning** (not stop), typed cost-risk gates on eight GL labs, teardown steps, and A0/kill-switch narrative on Start here. Unguided UL pairs appear in the same Labs tab without separate “sandbox only” enforcement in software.
- **Impact:** **Subjective Observation with high organizational stakes:** Approving this workbook for employees without dedicated sandbox accounts, SCPs, and billing alerts could create real AWS spend and security boundary issues; the app correctly disclaims agent AWS access but **cannot enforce** account choice.
- **Reproduction / Validation:** Read GL-06+ cost-risk requirements in `labs-and-safety.md`; UI shows stop-charges panels (`ui/labs.md`).
- **Recommended Improvement:** Corporate rollout checklist: sandbox OU, no production profiles, mandatory GL-01 budget lab, forbid shared root, track hourly lab completion in change windows; keep product warnings visible in manager comms.
- **Confidence:** Subjective Observation (product behaves as designed; risk is deployment context)
- **Related:** AWS-001/002 (hourly lab failure modes), AWS-005 (teardown hygiene), inventory 16 hourly pairs

### ITMGR-006 — Unguided labs lack `beforeYouStart` blocks (21/21 UL)

- **Severity:** Low
- **Category:** lab-sequence, pedagogy
- **Location:** UL-01 … UL-21
- **Evidence:** EV-ITMGR-018
- **Description:** Content scan flags all unguided labs for missing `beforeYouStart`. Guided labs include preflight bullets; UL pairs may rely on GL prerequisites — intended for advanced learners but unclear for employees assigned “complete all labs.”
- **Impact:** **Subjective Observation:** Extra friction or skipped preflight for employees who jump to UL cards beside GL in the UI.
- **Reproduction / Validation:** Scan JSON lab entries; compare GL-01 `beforeYouStart` in API reveal snapshot vs UL content.
- **Recommended Improvement:** UI hint linking UL to paired GL preflight, or shared A0 panel; align with TEACHER-003 if omission stays intentional.
- **Confidence:** Needs Verification (may be intended pair design per `intended-design.md`)
- **Related:** TEACHER-003, STUDENT-001

## Items Requiring Verification

- **ITMGR-003:** Heuristic longest-choice counts tied to **Teacher F-02** (Confirmed pedagogy); **F-01** adds navigation breakage risk for lesson-driven drills.
- **ITMGR-006:** UL `beforeYouStart` omission — align with **TEACHER-003** design concern unless product adds UL preflight.

## Subjective Observations

- **Backend-down behavior (good):** Bootstrap failure surfaces a clear page-level error with remediation text (EV-ITMGR-011, EV-ITMGR-012). Evaluators did not stop the server; this is code + design review aligned with `app-map.md`.
- **Progress clarity:** Header shows self-reported checkpoint steps and lab completion counts (EV-ITMGR-013). This is honest for self-study but is **not** verified lab execution — managers should not equate checkbox progress with AWS lab completion.
- **Readiness clarity:** Start here explains insufficient evidence and per-bucket “need N more” when thresholds are unmet (EV-ITMGR-014, EV-ITMGR-007) — good anti-gaming messaging for individuals; still not aggregateable for teams.
- **SQLite, no auth (intended):** Single-user local DB, CORS locked to localhost Vite ports, CSRF on mutating APIs (EV-ITMGR-015, EV-ITMGR-023). Acceptable for solo study; **corporate blockers** include shared machines (progress bleed if same Windows profile), no SSO, and export/import/reset available to whoever sits at the keyboard — not multi-tenant data loss, but no accountability.
- **Export for records:** `export_progress()` returns structured attempts, checkpoints, cost entries, settings (EV-ITMGR-022). Suitable for learner-owned backup; IT would need a policy for storing JSON exports if used as evidence.
- **Mock exam UX:** Disabled control with outdated “Phase 4 Locked” label (EV-ITMGR-003) — see FULLSTACK-002; confusing for a program advertising SAA-C03 prep.
- **Content lint passed** preflight (`preflight.md`) — reduces but does not eliminate scan-flagged pedagogical patterns.

## Strengths

- Clear four-tab information architecture and onboarding narrative (A0, cost, teardown) suitable for security-aware engineers.
- Separation of **coverage registry** vs **readiness metrics** avoids implying a single “pass probability” score — aligned with honest corporate comms if explained.
- Lab catalog documents hourly cost risk and product-level cost-risk typing for the highest-spend guided labs.
- Localhost-only API guardrails match a single-user threat model for SQLite progress.
- Bootstrap and tab-level error strings give actionable recovery when Django is unreachable.

## Adoption Recommendations (Subjective)

1. **Do not** use current drill attempt/readiness data for compliance reporting until ITMGR-001 / PYTHON-001 is resolved.
2. **Do** require dedicated AWS sandbox accounts and written lab policy before assigning GL/UL pairs at scale.
3. **Do** treat Coverage status fields as author workflow, not executive sign-off, until Teacher/AWS verification reports land.
4. **Consider** keeping deployment local-only; hosting would compound SQLite/no-auth issues without a redesign.

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| ITMGR-001 | Confirmed High (audit / attestation) | XF-001 |
| ITMGR-002 | Likely Medium | XF-008 (with FULLSTACK-008) |
| ITMGR-003 | Linked Teacher F-02 Confirmed | XF-003 |
| ITMGR-004 | Confirmed Medium (API status semantics) | XF-007 |
| ITMGR-005 | Subjective High (deployment policy) | XF-006 |
| ITMGR-006 | Needs Verification / design concern | — |
