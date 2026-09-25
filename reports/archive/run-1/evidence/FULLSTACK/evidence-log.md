# Evidence log — FULLSTACK

| ID | Time (UTC-4) | Type | Locator | Excerpt (≤30 words, verbatim) | Tool / command |
|----|--------------|------|---------|----------------------------------|----------------|
| EV-FULLSTACK-001 | 2026-09-25 | API | `reports/evidence/api/question-q-saa-1-1-k01-mc.json` | `"rationale": "Option A aligns with the published objective wording…"` on GET | Orchestrator API snapshot |
| EV-FULLSTACK-002 | 2026-09-25 | UI | `/exam`, `reports/evidence/ui/exam.md` | Mock exam control **disabled**; "Coming after Phase 4 Locked" | Browser page text |
| EV-FULLSTACK-003 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:39-58` | `summary.questions.map(async (id) => { … await api.question(id)` | Read |
| EV-FULLSTACK-004 | 2026-09-25 | file | `frontend/src/App.tsx:26-28,92-94` | Unknown `tabSlug` → `PATH_TO_TAB[tabSlug ?? ''] ?? 'labs'`; `*` → `/labs` only | Read |
| EV-FULLSTACK-005 | 2026-09-25 | UI | `reports/evidence/ui/start.md` | Skip link; tablist with four tabs; headings h1–h3 | Browser a11y snapshot |
| EV-FULLSTACK-006 | 2026-09-25 | file | `frontend/src/components/Header.tsx:27-38` | `role="tablist"` / `role="tab"`; no `tabpanel` or `aria-controls` | Read |
| EV-FULLSTACK-007 | 2026-09-25 | file | `frontend/src/hooks/useWorkbookBootstrap.ts:69-69` | `reloadLabs(sum.labs)` — parallel GET every lab id on bootstrap | Read |
| EV-FULLSTACK-008 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:80-104,148-149,290` | Submit enabled when `selected.size === 0` false only; no `selectCount` match | Read |
| EV-FULLSTACK-009 | 2026-09-25 | file | `ExamDrillsTab.tsx:42-47` + `:89` | Catalog effect and active-question effect both call `api.question(activeQuestionId)` | Read |
| EV-FULLSTACK-010 | 2026-09-25 | file | `backend/workbook/content_loader.py:45-48` | `public_question` pops `correctAnswerIds` only; rationale retained | Read |
| EV-FULLSTACK-011 | 2026-09-25 | UI | `reports/evidence/ui/exam.md` | Sidebar "All drills **429**"; modules A0–T4 with counts | Browser page text |
| EV-FULLSTACK-012 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:227-234` | `disabled title="Mock exam in a later phase"`; copy "Coming after Phase 4" | Read |
| EV-FULLSTACK-013 | 2026-09-25 | file | `frontend/src/components/LabCard.tsx:123-134` | Header `role="button"` `aria-expanded`; no `aria-label` on lab title | Read |
| EV-FULLSTACK-014 | 2026-09-25 | file | `frontend/src/components/ExamDrillsTab.tsx:311-315` | Rationale panel `role="status"` (not `aria-live`) | Read |
| EV-FULLSTACK-015 | 2026-09-25 | file | `frontend/src/utils/markdown.tsx:68-77` | List parser only handles flat `- ` lines; no nested indent | Read |
| EV-FULLSTACK-016 | 2026-09-25 | command | `frontend/`, `npx eslint src` | Exit code 0; no rule violations printed | Shell (read-only) |
| EV-FULLSTACK-017 | 2026-09-25 | file | `frontend/src/api/client.ts:31-39` | Non-OK responses surface `err.error` or status text to UI | Read |
| EV-FULLSTACK-018 | 2026-09-25 | file | `docs/architecture.md:60` | Spec lists "mock exam entry" on Exam drills tab | Read |
| EV-FULLSTACK-019 | 2026-09-25 | UI | `reports/evidence/ui/labs.md` | "All **42** labs · 0 %" — large lab DOM on first paint | Browser page text |

**Sample coverage (`reports/evidence/sample.md`):** drill interaction scope includes sampled question IDs consumed via shared API snapshots (e.g. `q-saa-1-1-k01-mc` in EV-FULLSTACK-001) and `/exam` UI (EV-FULLSTACK-002, EV-FULLSTACK-011). Full 429-ID bank referenced through `content-summary` count in app-map, not individually re-fetched in this log.

**DB actions:** none (read-only frontend/API review for this role).
