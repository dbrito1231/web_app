# Amendment 2 — Batch F5 implementation log (frontend)

Scope: `frontend/src/**` only. No git, server, install, or Playwright actions taken. Reset/Import were not clicked.

## Changes

1. **FS-R3-001** (sticky header hides scrolled-to heading/Study link)
   - `frontend/src/components/Header.tsx`: added a `ref` on `<header className="top">` and a `ResizeObserver` effect that sets `document.documentElement.style.setProperty('--header-h', ...)` to the header's live `offsetHeight` (runs once on mount and on every resize/wrap change).
   - `frontend/src/styles/app.css:169`: `.pbq-heading{scroll-margin-top:80px}` → `scroll-margin-top:calc(var(--header-h, 176px) + 12px)`.
   - Verified: `/exam?q=q-saa-3-2-s01-mc` at 1024×768 — header 114.9px, heading top 223.8px, Study link top 264.9px (both clear of the header). At mobile preset (375×812) — header 176.0px, heading top 186.8px, Study link top 228.0px; `elementFromPoint` at the heading's top-left returns `pbq-heading` (not the header).

2. **FS-R3-002** (stale scroll flag on same-card click)
   - `frontend/src/components/ExamDrillsTab.tsx` card `onClick` (~line 262): now checks `q.id !== activeQuestionId`. Only then does it set `scrollToQuestion.current = true` and change `activeQuestionId`; if the id is unchanged, the ref is set to `false` and the heading is scrolled/focused immediately in the click handler instead.
   - Verified in the browser: clicking a different card then re-clicking the already-selected card moves `scrollY` from 0 straight to the heading (62865 at mobile), not the previous "next unrelated click jumps" bug.

3. **FS-R3-003** (Study link before heading in DOM/tab order)
   - `frontend/src/components/ExamDrillsTab.tsx` (~line 312): `<StudyLink>` moved to after `<h2 ref={questionHeading} ...>` so it follows the heading in both DOM order and tab order.

4. **FS-R3-004** (Study link causes full reload) + `?lesson=` on in-app nav
   - `frontend/src/components/ExamDrillsTab.tsx`: `StudyLink` now renders `<Link to={...}>` from `react-router-dom` instead of a plain `<a href>`.
   - `frontend/src/components/StartHereTab.tsx`: switched from a one-time `useState(() => new URLSearchParams(window.location.search).get('lesson'))` read to `useSearchParams()`, plus a `useEffect` that adopts `searchParams.get('lesson')` whenever it changes (covers Link navigation, not just first load).
   - Verified: from `/exam?q=q-a0-mc-001`, clicking the rendered Study link (`href="/start?lesson=a0-lab-safety"`) navigated to `/start?lesson=a0-lab-safety` with a `window.__marker` set before the click still present after (no reload), and the lesson body updated to "A0 — Lab safety and local threat model".

5. **FS-R2-2-003** (sticky header hides linked lab card head)
   - `frontend/src/styles/app.css:266`: added `scroll-margin-top:calc(var(--header-h, 176px) + 12px)` to `.lab-card`.
   - Verified: `/labs?lab=gl-08` at mobile preset — card top 188.4px; `elementFromPoint` on the card head returns `lab-card-head`, not the header.

6. **FS-R2-2-004** (stale lab filter after navigating to plain `/labs`)
   - `frontend/src/components/LabsTab.tsx`: `linkedLab` is now read via `useSearchParams()` (reactive to route changes) instead of a one-time `window.location.search` read; added a `useEffect(() => setMainQuery(linkedLab), [linkedLab])` so the search box follows the `lab` param, including clearing to `''` when the param disappears.
   - Verified: navigated to `/labs?lab=gl-08` (search box = `gl-08`), then clicked the in-app "Labs" tab button (`#tab-labs`, no full navigation) — URL became `/labs` and the search box value became `''`.

7. **FS-R2-2-005** (Start here scrolls sideways at 375px)
   - `frontend/src/styles/app.css`: `.prose` max-width clamped to `min(76ch,100%)`; added `.prose p,.prose li,.prose a{overflow-wrap:anywhere}`; added `.lesson-picker{display:flex;flex-direction:column;gap:4px;max-width:100%;margin:10px 0}` and `.lesson-picker select{max-width:100%}`.
   - Verified: `/start?lesson=lesson-1-1` at 375×812 — `document.documentElement.scrollWidth === window.innerWidth === 375`.

8. **FS-R2-2-006** (lesson picker doesn't update `?lesson=`)
   - `frontend/src/components/StartHereTab.tsx`: added a `setLessonId(id)` wrapper (used by the `<select onChange>`) that updates local state and calls `setSearchParams(prev => {...set('lesson', id)}, { replace: true })`.
   - Verified: changing the picker's value via a `change` event updated `location.href` to `/start?lesson=a0-lab-safety` immediately.

9. **FS-R2-2-007** (`?q=` not updated after picking another drill)
   - `frontend/src/components/ExamDrillsTab.tsx`: added `useSearchParams()`; the card `onClick` now calls `setSearchParams({ q: q.id }, { replace: true })` for both the "different id" and "same id" branches.
   - Verified: clicking another card changed `location.href` to `/exam?q=q-a0-mc-001` (matching the newly selected drill).

10. **FS-R2-2-008** (confirmation message lost after Import/Reset reload)
    - `frontend/src/hooks/useWorkbookBootstrap.ts`: added `notice` state plus `reloadWithNotice(message)` (runs `bootstrap()` then sets `notice`) and `clearNotice()`. `notice` lives in the hook, one level above `StartHereTab`, so it survives the tab's unmount/remount while `loading` is true during a reload.
    - `frontend/src/App.tsx`: passes `notice`, `onDismissNotice={clearNotice}`, and `onReload={(message) => void reloadWithNotice(message)}` to `StartHereTab`.
    - `frontend/src/components/StartHereTab.tsx`: `onReload` signature changed to `(message: string) => void`; `importProgress`/`resetProgress` now call `onReload('Import completed')` / `onReload('Progress reset')` instead of setting local state before reloading. The success banner renders `message ?? notice`. A `useEffect` auto-clears `notice` after 5s via `onDismissNotice()`.
    - **Not exercised live** — Import and Reset are off-limits for this batch (they write state). Verified by code inspection only: `notice` is hook/App-level state, unaffected by `App.tsx`'s `{!loading && summary && (...)}` unmount of `StartHereTab` during `bootstrap()`.

## Verification summary

- `npx eslint src` in `frontend/`: clean, no output, exit 0.
- `npm run build` in `frontend/`: `tsc -b && vite build` succeeded (dist output produced, no errors).
- Browser checks (own tab `tab-4`, http://127.0.0.1:5173, backend on :8000; viewport reset to desktop at the end):
  - `/exam?q=q-saa-3-2-s01-mc` at 1024×768 and mobile preset (375×812): heading and Study link both land fully below the sticky header (see item 1 evidence above).
  - `/labs?lab=gl-08` then in-app `/labs`: card head clear of header at mobile; filter clears on in-app nav.
  - `/start?lesson=lesson-1-1` at 375×812: no horizontal scroll (`scrollWidth === innerWidth === 375`).
  - No Check answers, Reset, or Import clicks were made.

## Unresolved / out of scope

- FS-R2-2-008 (notice-survives-reload) was verified by code review only, not by clicking Import/Reset, per the batch's no-state-changing-action constraint. A future review pass with permission to exercise Import/Reset should confirm the banner text ("Import completed" / "Progress reset") actually appears after the reload completes.
- The "Back to Start here" link and the lesson's "Drills for this lesson" / "Labs for this lesson" links in `StartHereTab.tsx` remain plain `<a>` tags (full reload). Only the Study link on the Exam drills page was in scope (FS-R3-004); the others were not listed in this batch's fix list.
