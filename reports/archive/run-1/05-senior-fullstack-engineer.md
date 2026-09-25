# Senior Full-Stack Engineer Evaluation

## Evaluation Scope

**Routes and UI (desktop):** `/start`, `/labs`, `/exam`, `/coverage` — shared snapshots in `reports/evidence/ui/{start,labs,exam}.md`; routing logic in `frontend/src/App.tsx`.

**Frontend files reviewed:** `App.tsx`, `components/{ExamDrillsTab.tsx,LabCard.tsx,Header.tsx}`, `api/client.ts`, `hooks/useWorkbookBootstrap.ts`, `utils/markdown.tsx`, `styles/app.css`.

**API cross-check:** `reports/evidence/api/question-q-saa-1-1-k01-mc.json`, `content-summary.json` (429 question IDs), `app-map.md`.

**Tooling:** `npx eslint src` from `frontend/` (EV-FULLSTACK-016).

**Out of scope this pass:** mobile/tablet viewport resize, full keyboard-only drill completion, network waterfall capture (inferred from code + catalog count).

---

## Confirmed Issues

### FULLSTACK-001 — Question GET delivers rationales before submit

- **Severity:** High
- **Category:** frontend-bug, api, security-local
- **Location:** `ExamDrillsTab` → `api.question()`; backend `public_question()` in `backend/workbook/content_loader.py:45-48`; `views.question_detail`
- **Evidence:** EV-FULLSTACK-001, EV-FULLSTACK-010; related PYTHON-001
- **Description:** The exam UI hides rationale until after "Check answers", but opening `/exam` triggers `GET /api/questions/<id>` responses that include full `rationale` text. Only `correctAnswerIds` is stripped server-side.
- **Impact:** Local integrity of exam-mode practice is illusory; DevTools, a script, or a modified client can prefetch explanations for all 429 items without submitting attempts.
- **Reproduction / Validation:** Inspect saved GET body for `q-saa-1-1-k01-mc` or Network tab on `/exam` load → any question detail response includes `"rationale":`.
- **Recommended Improvement:** Omit `rationale` (and other post-submit fields) from `public_question`; return rationale only from `POST /api/attempts`. Add a frontend contract test and API regression test.
- **Confidence:** Confirmed

### FULLSTACK-002 — Mock exam control disabled with stale Phase 4 copy

- **Severity:** Medium
- **Category:** ux, consistency
- **Location:** `frontend/src/components/ExamDrillsTab.tsx:227-234` (`disabled`, `title="Mock exam in a later phase"`, "Coming after Phase 4")
- **Evidence:** EV-FULLSTACK-002, EV-FULLSTACK-012, EV-FULLSTACK-018
- **Description:** Browser shows a disabled "Mock exam" card labeled "Coming after Phase 4" / "Locked". Product architecture and `docs/status.md` record Phase 4 complete with `mock-saa-50.json` delivered, but the UI does not expose mock exam entry.
- **Impact:** Learners believe mock exam is future work; readiness workflow described in architecture is not reachable from the tab that should host it.
- **Reproduction / Validation:** Navigate to `http://127.0.0.1:5173/exam` → scroll question grid → disabled Mock exam card with Phase 4 text (see `reports/evidence/ui/exam.md`).
- **Recommended Improvement:** Implement mock-exam flow from `content/coverage/mock-saa-50.json` or update copy/disabled state to match shipped scope.
- **Confidence:** Confirmed

---

## Probable Concerns

### FULLSTACK-003 — Exam tab N+1 question fetch storm on mount

- **Severity:** Medium
- **Category:** maintainability, frontend-bug
- **Location:** `ExamDrillsTab.tsx:35-63`
- **Evidence:** EV-FULLSTACK-003, EV-FULLSTACK-011
- **Description:** On first render, `Promise.all(summary.questions.map(id => api.question(id)))` loads **429** full question documents to build module filters and card stems. UI shows "All drills 429" only after this completes.
- **Impact:** Slow first paint, hundreds of localhost requests, and **429× amplification** of FULLSTACK-001 (every response carries rationale). Poor experience on slower machines.
- **Reproduction / Validation:** Code review; open `/exam` with Network panel filtered to `/api/questions/` (count ≈429 on cold visit).
- **Recommended Improvement:** Add a lightweight catalog endpoint (id, module, type, stem preview only, no rationale) or embed catalog metadata in `/api/content/summary`.
- **Confidence:** Likely

### FULLSTACK-004 — Invalid URL slugs render Labs without correcting the address

- **Severity:** Low
- **Category:** ux, frontend-bug
- **Location:** `App.tsx:26-28` (`/:tabSlug` with fallback `?? 'labs'`), contrast `Navigate` on `path="*"` only after non-matching paths
- **Evidence:** EV-FULLSTACK-004
- **Description:** Visiting `/not-a-tab` matches `/:tabSlug`, maps unknown slug to tab `labs`, and renders Labs content while the browser bar still shows `/not-a-tab`. True unknown paths outside that pattern redirect to `/labs`.
- **Impact:** Broken deep links, confusing back/forward history, and harder support ("I'm on /foo but see Labs").
- **Reproduction / Validation:** Navigate to `http://127.0.0.1:5173/invalid-slug` → Labs UI with wrong URL (code path; browser not re-run in this pass).
- **Recommended Improvement:** Redirect unknown slugs to `/labs` with `replace`, or render a 404 shell.
- **Confidence:** Likely

### FULLSTACK-005 — MR drills do not enforce `selectCount` before submit

- **Severity:** Medium
- **Category:** drill-design, frontend-bug
- **Location:** `ExamDrillsTab.tsx:148-149,290-291`
- **Evidence:** EV-FULLSTACK-008
- **Description:** UI displays "Select {n}" from `promptNote` / regex but enables "Check answers" whenever `selected.size > 0`. Learners can submit one choice on a "Select TWO" MR item.
- **Impact:** Scoring returns 0% without explaining the selection-count rule; frustrating UX and unlike real exam constraints.
- **Reproduction / Validation:** Open any MR drill → select one checkbox → submit succeeds (backend scores exact set).
- **Recommended Improvement:** Disable submit until `selected.size === Number(selectCount)` for `type === 'mr'`.
- **Confidence:** Likely

### FULLSTACK-006 — Incomplete tabs ARIA pattern

- **Severity:** Medium
- **Category:** a11y
- **Location:** `Header.tsx:27-38`; main tab panels in `App.tsx` / tab components (no `role="tabpanel"`)
- **Evidence:** EV-FULLSTACK-005, EV-FULLSTACK-006
- **Description:** Start-here snapshot shows skip link and `tablist` with four tabs. Tabs use `role="tab"` and `aria-selected` but lack paired `tabpanel` roles, `aria-controls`, and `id` wiring. Content swaps via conditional render only.
- **Impact:** Screen-reader users may not perceive which panel belongs to the selected tab; focus management on tab change is unspecified.
- **Reproduction / Validation:** Accessibility tree on `/start` (orchestrator snapshot) + Header source review.
- **Recommended Improvement:** Implement WAI-ARIA tabs pattern (tab ↔ panel ids, `aria-labelledby`, optional roving tabindex).
- **Confidence:** Likely

### FULLSTACK-007 — Per-question "best" scores live only in component state

- **Severity:** Low
- **Category:** ux, consistency
- **Location:** `ExamDrillsTab.tsx:31,131-134,151-155,221`
- **Evidence:** EV-FULLSTACK-003 (no progress API usage in this file)
- **Description:** Sidebar meters and card "Best %" use `bestScores` state updated after submit, not `/api/progress` attempt history.
- **Impact:** Refreshing `/exam` resets module progress meters to 0/total despite stored attempts in SQLite; header stats and drill sidebar disagree.
- **Reproduction / Validation:** Submit a drill, note "Best 100%", hard refresh `/exam` → "Not tried" on cards (inferred from state design).
- **Recommended Improvement:** Derive best scores from progress snapshot or attempts API on tab mount.
- **Confidence:** Likely

### FULLSTACK-008 — Bootstrap eagerly loads all 42 lab payloads

- **Severity:** Medium
- **Category:** maintainability
- **Location:** `useWorkbookBootstrap.ts:40-53,69`
- **Evidence:** EV-FULLSTACK-007, EV-FULLSTACK-019
- **Description:** Initial bootstrap `Promise.all`s `api.lab(id)` for every lab ID before first paint of any tab. Labs tab evidence shows full 42-lab DOM immediately.
- **Impact:** Up-front cost even when learner only uses Exam or Start; pairs with large JSON payloads and checkpoint UI.
- **Reproduction / Validation:** Code review; `/labs` first visit issues ~42 GET `/api/labs/<id>` (expected from bootstrap, not isolated in network log here).
- **Recommended Improvement:** Lazy-load lab bodies when Labs tab activates or when a module expands.
- **Confidence:** Likely

### FULLSTACK-009 — Duplicate GET for the active question

- **Severity:** Low
- **Category:** maintainability
- **Location:** `ExamDrillsTab.tsx` catalog effect (lines 42-47) and active-question effect (lines 89-91)
- **Evidence:** EV-FULLSTACK-009
- **Description:** The first catalog fetch already retrieves full question JSON (including choices) for every ID; selecting the active question triggers a second identical GET.
- **Impact:** Extra latency when switching drills; doubles rationale exposure for the visible item.
- **Reproduction / Validation:** Select a question in Network panel → two GETs for same id on initial load (first from catalog batch, second from active effect).
- **Recommended Improvement:** Cache question payloads in a ref/Map from the catalog pass; active effect reads cache first.
- **Confidence:** Likely

### FULLSTACK-010 — Lab card disclosure control lacks concise accessible name

- **Severity:** Low
- **Category:** a11y
- **Location:** `LabCard.tsx:123-134`
- **Evidence:** EV-FULLSTACK-013
- **Description:** Expand/collapse header is a single `role="button"` grid without `aria-label` combining lab id and title. Visible text exists but nested structure may produce verbose or ambiguous announcements.
- **Impact:** Screen-reader users scanning many GL/UL pairs get weaker landmarks than the visual chip/title pairing.
- **Reproduction / Validation:** Inspect accessibility tree on expanded lab card in `/labs` snapshot log (not fully exercised here).
- **Recommended Improvement:** Set `aria-label={`${chip}: ${lab.title}`}` on the header control.
- **Confidence:** Likely

### FULLSTACK-011 — Post-submit feedback may not be announced

- **Severity:** Low
- **Category:** a11y
- **Location:** `ExamDrillsTab.tsx:311-315` (`role="status"`)
- **Evidence:** EV-FULLSTACK-014
- **Description:** Rationale block uses `role="status"` without `aria-live="polite"` (or assertive). Some AT combinations treat status regions inconsistently compared to explicit live regions.
- **Impact:** After submit, blind learners may miss rationale unless they manually explore the article.
- **Reproduction / Validation:** Code review; keyboard submit flow not fully recorded in this pass.
- **Recommended Improvement:** Use `aria-live="polite"` on the rationale container or move focus to the feedback heading.
- **Confidence:** Likely

### FULLSTACK-012 — Markdown helper limited for lesson/lab bodies

- **Severity:** Low
- **Category:** maintainability, ux
- **Location:** `utils/markdown.tsx:68-77`
- **Evidence:** EV-FULLSTACK-015
- **Description:** Custom renderer supports flat `-` lists and `#`/`##` headings only; nested lists and richer markdown are not parsed.
- **Impact:** If lesson JSON uses nested bullets, UI may flatten or mis-render teaching content (severity depends on content; not validated per-lesson here).
- **Reproduction / Validation:** Compare lesson JSON fences against rendered output on Start here (Needs spot-check).
- **Recommended Improvement:** Adopt a maintained markdown library or extend parser for nested lists and links.
- **Confidence:** Likely

---

## Items Requiring Verification

### FULLSTACK-013 — Mobile exam grid usability at 375px

- **Severity:** Medium
- **Category:** responsive
- **Location:** `styles/app.css:215-225,295-298` (`max-width:900px` shell collapse)
- **Evidence:** CSS review only; Phase 2 mobile pass not duplicated in FULLSTACK tab
- **Description:** Breakpoint stacks sidebar above main content; `pbq-grid` auto-fill may produce long scroll through 429 cards on narrow viewports.
- **Impact:** Drill discovery on phone-sized viewports may be tedious.
- **Reproduction / Validation:** Resize agent-owned browser to mobile preset and traverse `/exam` module filter + card list.
- **Recommended Improvement:** Module-first navigation by default on small screens; virtualize card grid.
- **Confidence:** Needs Verification

---

## Subjective Observations

- Bootstrap surfaces a clear error when API is unreachable (`App.tsx:61-64`, `client.ts:31-39`) without requiring server shutdown — appropriate for local IT learners (EV-FULLSTACK-017).
- Exam choice list uses `fieldset` + visually hidden `legend` — good baseline for MC/MR groups (EV-FULLSTACK-005 context).
- `eslint` reports clean on `src/`; no console-error capture on `/exam` in shared UI pack (not interpreted as absence of runtime warnings).

---

## Strengths

- React Router deep links for the four primary tabs (`/labs`, `/exam`, `/coverage`, `/start`) align with the CCNA layout replica and orchestrator app-map.
- CSRF-aware POST helper and `ensureSession()` before bootstrap mutations reduce accidental 403s on checkpoints and attempts.
- Lab UX integrates cost-risk gating, teardown commands, and checkpoint toggles in one card (`LabCard.tsx`) consistent with safety-first product goals.
- Visual design tokens, skip link, and `:focus-visible` styles in `app.css` show intentional accessibility baselines.
- eslint passes with zero reported violations on the full `src` tree (EV-FULLSTACK-016).

---

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| FULLSTACK-001 | Confirmed High | XF-001 (with PYTHON-001) |
| FULLSTACK-002 | Confirmed Medium | XF-002 |
| FULLSTACK-003 | Likely Medium | — |
| FULLSTACK-004 | Likely Low | — |
| FULLSTACK-005 | Likely Medium | — |
| FULLSTACK-006 | Likely Medium | — |
| FULLSTACK-007 | Likely Low | — |
| FULLSTACK-008 | Likely Medium | — |
| FULLSTACK-009 | Likely Low | — |
| FULLSTACK-010 | Likely Low | — |
| FULLSTACK-011 | Likely Low | — |
| FULLSTACK-012 | Likely Low | — |
| FULLSTACK-013 | Needs Verification | — |
