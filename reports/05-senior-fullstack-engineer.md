# Senior Full-Stack Engineer Evaluation (Phase 3 strict eval)

**Run:** 2026-09-25 Phase 3 — FULLSTACK role re-verification (draft did not read `reports/archive/run-1/**`).

## Evaluation Scope

**Routes and UI (desktop):** `/start`, `/labs`, `/exam`, `/coverage` — shared snapshots in `reports/evidence/ui/{start,labs,exam}.md`; routing logic in `frontend/src/App.tsx`.

**Frontend files reviewed:** `App.tsx`, `components/{ExamDrillsTab,LabsTab,LabCard,Header,StartHereTab,CoverageTab}.tsx`, `api/client.ts`, `hooks/useWorkbookBootstrap.ts`, `utils/markdown.tsx`, `styles/app.css`.

**API cross-check:** `reports/evidence/api/question-q-saa-1-1-k01-mc.json`, Gate 0 `reports/evidence/gate0-save-failure.md`, EV-GATE0-001/002.

**Tooling:** `npx eslint src` from `frontend/` (EV-FULLSTACK-216, EV-FULLSTACK-223).

**Paper-feedback mode (Gate 0 Result A):** All learner POSTs fail CSRF origin check. Drill score/rationale panels, lab checkpoint success states, and post-submit **Retry** flows were **not verified in the UI** this pass (EV-FULLSTACK-224). Keyboard submit still reaches the error surface (`Forbidden`).

**Phase 3 additions:** Interactive control inventory; keyboard-only pass on four tabs (EV-FULLSTACK-220); routing/deep link/refresh (EV-FULLSTACK-221); eslint re-run.

## Finding template (nine fields)

- **Severity:** Critical / High / Medium / Low / Informational
- **Category:** tags (`api`, `frontend-bug`, `a11y`, `ux`, …)
- **Location:** file and symbol
- **Evidence:** EV-FULLSTACK-### / EV-GATE0-###
- **Description:** behavior vs expectation
- **Impact:** learner or product effect
- **Reproduction / Validation:** command, browser, or code path
- **Recommended Improvement:** minimal fix
- **Confidence:** Confirmed / Likely / Needs Verification / Subjective Observation
- **Related:** (optional) cross-agent IDs

## Interactive controls inventory (Phase 3)

| Area | Control type | Count / notes | Keyboard |
|------|----------------|---------------|----------|
| **Header** (`Header.tsx`) | Skip link `#main` | 1 | Tab + Enter (EV-FULLSTACK-220) |
| | Primary nav `role=tab` | 4 (Labs, Exam drills, Coverage, Start here) | focus + Enter switches route |
| | Stats strip | display only | n/a |
| **Labs** (`LabsTab.tsx`, `LabCard.tsx`) | Sidebar filter buttons | 1 “All labs” + 6 domain + ~20 group buttons | focus + Enter |
| | Search / selects | 1 search, 2 `<select>` (difficulty, status) | native tab order |
| | GL-01 jump | 1 `linkish` button → `/labs` scroll | Enter |
| | Lab card header | 42× `role=button` disclosure | Enter/Space toggles `aria-expanded` |
| | Cost-risk gate | hourly labs: text input per card | Tab into field |
| | Step toggles | 42× N step `button.step-check` | Enter toggles (POST blocked Gate 0) |
| | Teardown | pre/code only (no app buttons) | n/a |
| **Exam** (`ExamDrillsTab.tsx`) | Sidebar module filters | 1 “All drills” + A0–T4 module buttons | focus + Enter |
| | Question cards | up to 429 `button.pbq-card` | Enter selects active drill |
| | Mock exam | 1 disabled button | skipped (not in tab order usefully) |
| | Choices | MC radio / MR checkbox in `fieldset` | Space toggles |
| | Submit / retry | Check answers, Retry | Enter on focused button |
| **Coverage** (`CoverageTab.tsx`) | Domain sidebar | 1 “All objectives” + 4 domain buttons | focus + Enter |
| | Table body | read-only status badges | n/a |
| **Start here** (`StartHereTab.tsx`) | Sidebar | 2 decorative nav buttons (single lesson) | focusable, no route change |
| | Progress I/O | textarea + Export / Import / Reset + RESET field | Tab order through form |
| **Markdown** (`markdown.tsx`) | Copy on code fences | per fenced block in lessons | Enter on Copy |

Source trace: EV-FULLSTACK-222.

---

## Confirmed Issues

### FULLSTACK-230 — POST attempts/checkpoints fail CSRF trusted-origin check (Gate 0)

- **Severity:** Critical
- **Category:** backend-bug, api, ux
- **Location:** Django `CSRF_TRUSTED_ORIGINS` unset; `POST /api/attempts`, `POST /api/labs/<id>/checkpoints`; UI shows bare `Forbidden`
- **Evidence:** EV-GATE0-001, EV-GATE0-002; `reports/evidence/gate0-save-failure.md`; EV-FULLSTACK-220 (keyboard submit → `Forbidden`)
- **Description:** Gate 0 clicked **Check answers** on `q-a0-mc-001` and a GL-01 checkpoint; both returned **403** with Django CSRF HTML: `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins.` Phase 3 keyboard path reproduces the same alert text. UI `[role=alert]` text is only `Forbidden`.
- **Impact:** No drill or lab progress writes; learners cannot see scored feedback in the UI until settings include Vite origins in `CSRF_TRUSTED_ORIGINS`.
- **Reproduction / Validation:** Steps in `gate0-save-failure.md`; Phase 3: focus radio → Space → Enter on **Check answers** (EV-FULLSTACK-220).
- **Recommended Improvement:** Add `CSRF_TRUSTED_ORIGINS` matching `CORS_ALLOWED_ORIGINS`; improve client error text when response is HTML 403.
- **Confidence:** Confirmed
- **Related:** PYTHON-230, ITMGR-230

### FULLSTACK-201 — Question GET delivers rationales before submit

- **Severity:** High
- **Category:** frontend-bug, api, security-local
- **Location:** `ExamDrillsTab` → `api.question()`; backend `public_question()` in `backend/workbook/content_loader.py:45-48`; `views.question_detail`
- **Evidence:** EV-FULLSTACK-201, EV-FULLSTACK-210; related PYTHON-201
- **Description:** The exam UI hides rationale until after "Check answers", but opening `/exam` triggers `GET /api/questions/<id>` responses that include full `rationale` text. Only `correctAnswerIds` is stripped server-side.
- **Impact:** Local integrity of exam-mode practice is illusory; DevTools, a script, or a modified client can prefetch explanations for all 429 items without submitting attempts.
- **Reproduction / Validation:** Inspect saved GET body for `q-saa-1-1-k01-mc` or Network tab on `/exam` load → any question detail response includes `"rationale":`.
- **Recommended Improvement:** Omit `rationale` (and other post-submit fields) from `public_question`; return rationale only from `POST /api/attempts`. Add a frontend contract test and API regression test.
- **Confidence:** Confirmed

### FULLSTACK-202 — Mock exam control disabled with stale Phase 4 copy

- **Severity:** Medium
- **Category:** ux, consistency
- **Location:** `frontend/src/components/ExamDrillsTab.tsx:227-234` (`disabled`, `title="Mock exam in a later phase"`, "Coming after Phase 4")
- **Evidence:** EV-FULLSTACK-202, EV-FULLSTACK-212, EV-FULLSTACK-218
- **Description:** Browser shows a disabled "Mock exam" card labeled "Coming after Phase 4" / "Locked". Product architecture and `docs/status.md` record Phase 4 complete with `mock-saa-50.json` delivered, but the UI does not expose mock exam entry.
- **Impact:** Learners believe mock exam is future work; readiness workflow described in architecture is not reachable from the tab that should host it.
- **Reproduction / Validation:** Navigate to `http://127.0.0.1:5173/exam` → scroll question grid → disabled Mock exam card with Phase 4 text (see `reports/evidence/ui/exam.md`).
- **Recommended Improvement:** Implement mock-exam flow from `content/coverage/mock-saa-50.json` or update copy/disabled state to match shipped scope.
- **Confidence:** Confirmed

---

## Probable Concerns

### FULLSTACK-203 — Exam tab N+1 question fetch storm on mount

- **Severity:** Medium
- **Category:** maintainability, frontend-bug
- **Location:** `ExamDrillsTab.tsx:35-63`
- **Evidence:** EV-FULLSTACK-203, EV-FULLSTACK-211
- **Description:** On first render, `Promise.all(summary.questions.map(id => api.question(id)))` loads **429** full question documents to build module filters and card stems. UI shows "All drills 429" only after this completes.
- **Impact:** Slow first paint, hundreds of localhost requests, and **429× amplification** of FULLSTACK-201 (every response carries rationale). Poor experience on slower machines.
- **Reproduction / Validation:** Code review; open `/exam` with Network panel filtered to `/api/questions/` (count ≈429 on cold visit).
- **Recommended Improvement:** Add a lightweight catalog endpoint (id, module, type, stem preview only, no rationale) or embed catalog metadata in `/api/content/summary`.
- **Confidence:** Likely

### FULLSTACK-204 — Invalid URL slugs render Labs without correcting the address

- **Severity:** Low
- **Category:** ux, frontend-bug
- **Location:** `App.tsx:26-28` (`/:tabSlug` with fallback `?? 'labs'`), contrast `Navigate` on `path="*"` only after non-matching paths
- **Evidence:** EV-FULLSTACK-204, EV-FULLSTACK-221
- **Description:** Visiting `/not-a-tab` matches `/:tabSlug`, maps unknown slug to tab `labs`, and renders Labs content while the browser bar still shows `/not-a-tab`. True unknown paths outside that pattern redirect to `/labs`.
- **Impact:** Broken deep links, confusing back/forward history, and harder support ("I'm on /foo but see Labs").
- **Reproduction / Validation:** Playwright goto `http://127.0.0.1:5173/not-a-tab` → `.labs-main` visible, URL still `/not-a-tab` (EV-FULLSTACK-221).
- **Recommended Improvement:** Redirect unknown slugs to `/labs` with `replace`, or render a 404 shell.
- **Confidence:** Likely

### FULLSTACK-205 — MR drills do not enforce `selectCount` before submit

- **Severity:** Medium
- **Category:** drill-design, frontend-bug
- **Location:** `ExamDrillsTab.tsx:148-149,290-291`
- **Evidence:** EV-FULLSTACK-208
- **Description:** UI displays "Select {n}" from `promptNote` / regex but enables "Check answers" whenever `selected.size > 0`. Learners can submit one choice on a "Select TWO" MR item.
- **Impact:** Scoring returns 0% without explaining the selection-count rule; frustrating UX and unlike real exam constraints.
- **Reproduction / Validation:** Open any MR drill → select one checkbox → submit succeeds (backend scores exact set); blocked from UI scoring while Gate 0 active.
- **Recommended Improvement:** Disable submit until `selected.size === Number(selectCount)` for `type === 'mr'`.
- **Confidence:** Likely

### FULLSTACK-206 — Incomplete tabs ARIA pattern

- **Severity:** Medium
- **Category:** a11y
- **Location:** `Header.tsx:27-38`; main tab panels in `App.tsx` / tab components (no `role="tabpanel"`)
- **Evidence:** EV-FULLSTACK-205, EV-FULLSTACK-206, EV-FULLSTACK-220
- **Description:** Skip link and `tablist` with four tabs present. Tabs use `role="tab"` and `aria-selected` but lack paired `tabpanel` roles, `aria-controls`, and `id` wiring. Keyboard pass used programmatic focus + Enter on each tab (not Arrow-key roving tabindex).
- **Impact:** Screen-reader users may not perceive which panel belongs to the selected tab; arrow-key tab widgets behave like plain buttons.
- **Reproduction / Validation:** Accessibility tree on `/start` + Header source; Phase 3 keyboard pass notes missing roving pattern (EV-FULLSTACK-220).
- **Recommended Improvement:** Implement WAI-ARIA tabs pattern (tab ↔ panel ids, `aria-labelledby`, roving tabindex).
- **Confidence:** Likely

### FULLSTACK-207 — Per-question "best" scores live only in component state

- **Severity:** Low
- **Category:** ux, consistency
- **Location:** `ExamDrillsTab.tsx:31,131-134,151-155,221`
- **Evidence:** EV-FULLSTACK-203 (no progress API usage in this file)
- **Description:** Sidebar meters and card "Best %" use `bestScores` state updated after submit, not `/api/progress` attempt history.
- **Impact:** Refreshing `/exam` resets module progress meters to 0/total despite stored attempts in SQLite; header stats and drill sidebar disagree.
- **Reproduction / Validation:** Submit a drill, note "Best 100%", hard refresh `/exam` → "Not tried" on cards (inferred from state design); submit UI blocked under Gate 0.
- **Recommended Improvement:** Derive best scores from progress snapshot or attempts API on tab mount.
- **Confidence:** Likely

### FULLSTACK-208 — Bootstrap eagerly loads all 42 lab payloads

- **Severity:** Medium
- **Category:** maintainability
- **Location:** `useWorkbookBootstrap.ts:40-53,69`
- **Evidence:** EV-FULLSTACK-207, EV-FULLSTACK-219
- **Description:** Initial bootstrap `Promise.all`s `api.lab(id)` for every lab ID before first paint of any tab. Labs tab evidence shows full 42-lab DOM immediately.
- **Impact:** Up-front cost even when learner only uses Exam or Start; pairs with large JSON payloads and checkpoint UI.
- **Reproduction / Validation:** Code review; `/labs` first visit issues ~42 GET `/api/labs/<id>` (expected from bootstrap, not isolated in network log here).
- **Recommended Improvement:** Lazy-load lab bodies when Labs tab activates or when a module expands.
- **Confidence:** Likely

### FULLSTACK-209 — Duplicate GET for the active question

- **Severity:** Low
- **Category:** maintainability
- **Location:** `ExamDrillsTab.tsx` catalog effect (lines 42-47) and active-question effect (lines 89-91)
- **Evidence:** EV-FULLSTACK-209
- **Description:** The first catalog fetch already retrieves full question JSON (including choices) for every ID; selecting the active question triggers a second identical GET.
- **Impact:** Extra latency when switching drills; doubles rationale exposure for the visible item.
- **Reproduction / Validation:** Select a question in Network panel → two GETs for same id on initial load (first from catalog batch, second from active effect).
- **Recommended Improvement:** Cache question payloads in a ref/Map from the catalog pass; active effect reads cache first.
- **Confidence:** Likely

### FULLSTACK-210 — Lab card disclosure control lacks concise accessible name

- **Severity:** Low
- **Category:** a11y
- **Location:** `LabCard.tsx:123-134`
- **Evidence:** EV-FULLSTACK-213, EV-FULLSTACK-220 (keyboard toggle works)
- **Description:** Expand/collapse header is a single `role="button"` grid without `aria-label` combining lab id and title. Visible text exists but nested structure may produce verbose or ambiguous announcements.
- **Impact:** Screen-reader users scanning many GL/UL pairs get weaker landmarks than the visual chip/title pairing.
- **Reproduction / Validation:** Keyboard Enter toggles `aria-expanded` on first card (EV-FULLSTACK-220); tree review on `/labs` snapshot.
- **Recommended Improvement:** Set `aria-label={`${chip}: ${lab.title}`}` on the header control.
- **Confidence:** Likely

### FULLSTACK-211 — Post-submit feedback may not be announced

- **Severity:** Low
- **Category:** a11y
- **Location:** `ExamDrillsTab.tsx:311-315` (`role="status"`)
- **Evidence:** EV-FULLSTACK-214, EV-FULLSTACK-224
- **Description:** Rationale block uses `role="status"` without `aria-live="polite"`. Under **paper-feedback mode**, successful submit path never rendered — only `[role=alert] Forbidden` after keyboard submit — so live-region behavior for correct/incorrect copy was **not observed**.
- **Impact:** After CSRF fix, blind learners may still miss rationale unless AT picks up `role="status"` consistently.
- **Reproduction / Validation:** Code review; Gate 0 blocks UI feedback verification (EV-FULLSTACK-224).
- **Recommended Improvement:** Use `aria-live="polite"` on the rationale container or move focus to the feedback heading once POST succeeds.
- **Confidence:** Likely

### FULLSTACK-212 — Markdown helper limited for lesson/lab bodies

- **Severity:** Low
- **Category:** maintainability, ux
- **Location:** `utils/markdown.tsx:68-77`
- **Evidence:** EV-FULLSTACK-215
- **Description:** Custom renderer supports flat `-` lists and `#`/`##` headings only; nested lists and richer markdown are not parsed.
- **Impact:** If lesson JSON uses nested bullets, UI may flatten or mis-render teaching content (severity depends on content; not validated per-lesson here).
- **Reproduction / Validation:** Compare lesson JSON fences against rendered output on Start here (Needs spot-check).
- **Recommended Improvement:** Adopt a maintained markdown library or extend parser for nested lists and links.
- **Confidence:** Likely

---

## Items Requiring Verification

### FULLSTACK-213 — Mobile exam grid usability at 375px

- **Severity:** Medium
- **Category:** responsive
- **Location:** `styles/app.css:215-225,295-298` (`max-width:900px` shell collapse)
- **Evidence:** CSS review only; Phase 3 desktop keyboard pass only
- **Description:** Breakpoint stacks sidebar above main content; `pbq-grid` auto-fill may produce long scroll through 429 cards on narrow viewports.
- **Impact:** Drill discovery on phone-sized viewports may be tedious.
- **Reproduction / Validation:** Resize browser to mobile preset and traverse `/exam` module filter + card list.
- **Recommended Improvement:** Module-first navigation by default on small screens; virtualize card grid.
- **Confidence:** Needs Verification

---

## Subjective Observations

- Bootstrap surfaces a clear error when API is unreachable (`App.tsx:61-64`, `client.ts:31-39`) without requiring server shutdown — appropriate for local IT learners (EV-FULLSTACK-217).
- Exam choice list uses `fieldset` + visually hidden `legend` — good baseline for MC/MR groups.
- **Keyboard pass (Phase 3):** All four primary tabs reachable without pointer; skip link works; exam and lab primary actions operable from keyboard; mock exam disabled control is a dead end by design (EV-FULLSTACK-220).
- **Routing (Phase 3):** Deep links and refresh on `/exam` and `/coverage` behave; root redirects to `/labs` (EV-FULLSTACK-221).
- `npx eslint src` exit **0**, empty stdout (EV-FULLSTACK-216 / EV-FULLSTACK-223).

---

## Strengths

- React Router deep links for the four primary tabs (`/labs`, `/exam`, `/coverage`, `/start`) align with the CCNA layout replica and orchestrator app-map.
- CSRF-aware POST helper and `ensureSession()` before bootstrap mutations reduce accidental 403s once trusted origins are configured.
- Lab UX integrates cost-risk gating, teardown commands, and checkpoint toggles in one card (`LabCard.tsx`) consistent with safety-first product goals.
- Visual design tokens, skip link, and `:focus-visible` styles in `app.css` show intentional accessibility baselines.
- eslint passes with zero reported violations on the full `src` tree (EV-FULLSTACK-216).

---

## Post-discussion status

Run-2 strict Phase 5–6 (see `reports/discussion/round-b/FULLSTACK.md`, `revalidation.md`).

| Finding ID | Pre-discussion confidence | Final status | Notes |
|------------|---------------------------|--------------|-------|
| FULLSTACK-230 | Confirmed | **Confirmed Critical** | Gate 0 CSRF; STUDENT-211 symptom |
| FULLSTACK-201 | Confirmed | **Confirmed High** (XF-201) | GET rationale leak |
| FULLSTACK-202 | Confirmed | **Confirmed Medium** (XF-202) | Mock exam UI |
| FULLSTACK-203 | Likely | **Likely Medium** | N+1 amplifies XF-201 |
| FULLSTACK-204 | Likely | **Likely Low** | Invalid slug URL |
| FULLSTACK-205 | Likely | **Likely Medium** (XF-209) | MR selectCount |
| FULLSTACK-206 | Likely | **Likely Medium** | Tabs ARIA |
| FULLSTACK-207 | Likely | **Likely Low** | Best scores not from API |
| FULLSTACK-208 | Likely | **Likely Medium** | Eager 42-lab load; ITMGR-202 |
| FULLSTACK-209 | Likely | **Likely Low** | Duplicate question GET |
| FULLSTACK-210 | Likely | **Likely Low** | Lab card aria-label |
| FULLSTACK-211 | Likely | **Likely Low** | Post-submit live region |
| FULLSTACK-212 | Likely | **Likely Low** | Markdown subset |
| FULLSTACK-213 | Needs Verification | **Needs Verification** | Mobile 375px |
