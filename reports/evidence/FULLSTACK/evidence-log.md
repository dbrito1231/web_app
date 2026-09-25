# Evidence log — FULLSTACK

| ID | Time (UTC-4) | Type | Locator | Excerpt (≤30 words, verbatim) | Tool / command |
|----|--------------|------|---------|----------------------------------|----------------|
| EV-FULLSTACK-201 | 2026-09-25 | API | `reports/evidence/api/question-q-saa-1-1-k01-mc.json` | `"rationale": "Option A aligns with the published objective wording…"` on GET | Orchestrator API snapshot |
| EV-FULLSTACK-202 | 2026-09-25 | UI | `/exam`, `reports/evidence/ui/exam.md` | Mock exam control **disabled**; "Coming after Phase 4 Locked" | Browser page text |
| EV-FULLSTACK-203 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:39-58` | `summary.questions.map(async (id) => { … await api.question(id)` | Read |
| EV-FULLSTACK-204 | 2026-09-25 | file | `frontend/src/App.tsx:26-28,92-94` | Unknown `tabSlug` → `PATH_TO_TAB[tabSlug ?? ''] ?? 'labs'`; `*` → `/labs` only | Read |
| EV-FULLSTACK-205 | 2026-09-25 | UI | `reports/evidence/ui/start.md` | Skip link; tablist with four tabs; headings h1–h3 | Browser a11y snapshot |
| EV-FULLSTACK-206 | 2026-09-25 | file | `frontend/src/components/Header.tsx:27-38` | `role="tablist"` / `role="tab"`; no `tabpanel` or `aria-controls` | Read |
| EV-FULLSTACK-207 | 2026-09-25 | file | `frontend/src/hooks/useWorkbookBootstrap.ts:69-69` | `reloadLabs(sum.labs)` — parallel GET every lab id on bootstrap | Read |
| EV-FULLSTACK-208 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:80-104,148-149,290` | Submit enabled when `selected.size === 0` false only; no `selectCount` match | Read |
| EV-FULLSTACK-209 | 2026-09-25 | file | `ExamDrillsTab.tsx:42-47` + `:89` | Catalog effect and active-question effect both call `api.question(activeQuestionId)` | Read |
| EV-FULLSTACK-210 | 2026-09-25 | file | `backend/workbook/content_loader.py:45-48` | `public_question` pops `correctAnswerIds` only; rationale retained | Read |
| EV-FULLSTACK-211 | 2026-09-25 | UI | `reports/evidence/ui/exam.md` | Sidebar "All drills **429**"; modules A0–T4 with counts | Browser page text |
| EV-FULLSTACK-212 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:227-234` | `disabled title="Mock exam in a later phase"`; copy "Coming after Phase 4" | Read |
| EV-FULLSTACK-213 | 2026-09-25 | file | `frontend/src/components/LabCard.tsx:123-134` | Header `role="button"` `aria-expanded`; no `aria-label` on lab title | Read |
| EV-FULLSTACK-214 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:311-315` | Rationale panel `role="status"` (not `aria-live`) | Read |
| EV-FULLSTACK-215 | 2026-09-25 | file | `frontend/src/utils/markdown.tsx:68-77` | List parser only handles flat `- ` lines; no nested indent | Read |
| EV-FULLSTACK-216 | 2026-09-25 | command | `frontend/`, `npx eslint src` | Exit code **0**; stdout empty (no violations) | Shell Phase 3 |
| EV-FULLSTACK-217 | 2026-09-25 | file | `frontend/src/api/client.ts:31-39` | Non-OK responses surface `err.error` or status text to UI | Read |
| EV-FULLSTACK-218 | 2026-09-25 | file | `docs/architecture.md:60` | Spec lists "mock exam entry" on Exam drills tab | Read |
| EV-FULLSTACK-219 | 2026-09-25 | UI | `reports/evidence/ui/labs.md` | "All **42** labs · 0 %" — large lab DOM on first paint | Browser page text |
| EV-FULLSTACK-220 | 2026-09-25 | command | Playwright headless @ 127.0.0.1:5173 | Tab+Enter on four `role=tab`; skip link Tab+Enter; exam Space+Enter → `Forbidden` | `$env:TEMP` node harness |
| EV-FULLSTACK-221 | 2026-09-25 | command | Playwright routing checks | `/exam` deep+refresh OK; `/` → `/labs`; `/not-a-tab` shows Labs, URL unchanged | Same harness |
| EV-FULLSTACK-222 | 2026-09-25 | file | `frontend/src/components/*.tsx` | Inventory: header 4 tabs+skip; Labs filters+42×(head, steps, cost); Exam 429 cards+choices | Read (Phase 3) |
| EV-FULLSTACK-223 | 2026-09-25 | command | `frontend/` `npx eslint src` | **eslint excerpt:** *(no output)* exit 0 | Shell 2026-09-25 Phase 3 |
| EV-FULLSTACK-224 | 2026-09-25 | UI | Exam keyboard submit (Gate 0) | No `role=status` rationale panel after submit; `[role=alert]` only `Forbidden` | Paper-feedback mode |
| EV-GATE0-001 | 2026-09-25T18:00Z | UI | POST /api/attempts q-a0-mc-001 | 403 CSRF Origin checking failed http://127.0.0.1:5173 | browser click + CDP fetch hook |
| EV-GATE0-002 | 2026-09-25T18:01Z | UI | POST gl-01/checkpoints | 403 same CSRF origin failure | browser click GL-01 step |

**Sample coverage (`reports/evidence/sample.md`):** drill interaction scope includes sampled question IDs consumed via shared API snapshots (e.g. `q-saa-1-1-k01-mc` in EV-FULLSTACK-201) and `/exam` UI (EV-FULLSTACK-202, EV-FULLSTACK-211). Full 429-ID bank referenced through `content-summary` count in app-map, not individually re-fetched in this log.

**DB actions:** none (read-only frontend/API review for this role).

**Phase 3 keyboard pass summary (EV-FULLSTACK-220):** Skip link reachable on first Tab; each header tab activated with focus+Enter (no pointer); URLs `/labs`, `/exam`, `/coverage`, `/start` with `aria-selected=true`. Exam: first radio Space selects; Enter on **Check answers** → alert `Forbidden` (no scored feedback UI). Labs: first `.lab-card-head` Enter toggles `aria-expanded` true→false. Gaps: no Left/Right roving tabindex on tablist (see FULLSTACK-206); Coverage/Start side nav buttons mostly decorative except domain filters.

**Phase 3 routing summary (EV-FULLSTACK-221):** Deep link `/exam` and hard refresh keep `/exam`; `/coverage` loads objectives sidebar; `/` redirects to `/labs`; unknown slug `/not-a-tab` renders Labs while address bar stays `/not-a-tab` (FULLSTACK-204).
