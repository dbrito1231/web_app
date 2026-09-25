# Fix-loop round 5: Senior Full-Stack Engineer review

Scope: commit `fbe0193` (change log `reports/fix-loop-r2/amendment-2/impl-F9.md`). It targets FS-R4-001 to 005 from `reports/fix-loop-r2/round-4/FULLSTACK.md`.

Method: read-only. I used my own Claude Browser tab (`tab-5`) against http://127.0.0.1:5173, with the API on :8000. I tested at 1280×800, 1024×768 and the mobile preset (375×812), and reset the viewport to desktop at the end. I did not submit attempts, click Reset or Import, POST anything, or edit files (apart from this report). I read `StartHereTab.tsx`, `ExamDrillsTab.tsx`, `Header.tsx`, `LabCard.tsx` and `App.tsx` to cross-check behavior against source.

To prove a navigation did not reload the page, I set `window.__marker` before it and read the marker back afterwards. I also checked `history.length` and the network log for `/api/*` calls.

`npx eslint src` in `frontend/`: **PASS** (no output, exit 0).

## Verdicts

| ID | Verdict | Evidence |
|----|---------|----------|
| FS-R4-001 (Study link opened Start here scrolled to the bottom, focus lost) | **Gone** (Confirmed) | `StartHereTab.tsx:82` initializes `scrollToLesson` from `Boolean(searchParams.get('lesson'))`, covering the fresh-mount case. Tested at all three viewports, each from a fresh `/exam?q=...` navigation with `window.__marker=1` set beforehand:<br>• **1280×800**: `q-saa-1-1-k01-mr` → Study link → `/start?lesson=lesson-1-1`. Heading top **76.2** (64px header + 12px), `activeElement` is the `H2` "A1 — Secure access to AWS resources", marker intact.<br>• **1024×768**: `q-saa-1-1-k03-mc` → Study link → `/start?lesson=lesson-1-1`. Heading top **127.5** (115 + 12), focused, marker intact.<br>• **375×812**: `q-saa-4-4-s03-mc` → Study link → `/start?lesson=lesson-4-4`. Heading top **188.1** (176 + 12), text "A4 — Cost-optimized networks", focused, marker intact, `scrollWidth === innerWidth === 375` (no sideways scroll). |
| FS-R4-002 (lesson picker fetched lesson + summary three times per change) | **Gone** (Confirmed) | `StartHereTab.tsx:70` makes `?lesson=` the only source of truth; `setLessonId` (`:104-113`) only calls `setSearchParams`. Fresh-loaded `/start?lesson=lesson-2-1`, then changed the picker to the untouched `lesson-3-4` via `form_input`. `read_network_requests` filtered to `lessons/lesson-3-4` showed **exactly one** request, no repeats, no reversion to `lesson-2-1`. |
| FS-R4-003 (module / "All drills" change left `?q=` pointing at the old drill) | **Gone** (Confirmed) | `ExamDrillsTab.tsx:161-172` syncs `?q=` on every `activeQuestionId` change. From `/exam?q=q-saa-1-1-k03-mc` at 1024×768, clicked the "Terraform 1–3" (T1) sidebar module: URL became `/exam?q=q-tf-004-1a-mc`. Clicking "All drills" afterwards correctly left `?q=` unchanged (the drill is still in the unfiltered list, so no fallback fires — this matches the original repro, which was specifically about a module filter dropping the current drill). Reloading `/exam?q=q-tf-004-1a-mc` reopened the same drill (heading text `q-tf-004-1a-mc`), confirming the URL is durable for sharing/reload. |
| FS-R4-004 ("Module …" eyebrow clipped ~5px at 375) | **Gone** (Confirmed) | `app.css` adds `scroll-margin-top` to `.pbq` (the article), and `ExamDrillsTab.tsx` scrolls that ref instead of just the heading. At 375, loading `/exam?q=q-saa-4-4-s03-mc` gave `.pbq` top **187.75** and its eyebrow top **208.75**, both fully below the 176px header — no clipping. |
| FS-R4-005 ("Back to Start here" and lesson drill/lab links did full reloads) | **Gone** (Confirmed) | All four link sites now use `<Link>`/react-router navigation and preserve `window.__marker`:<br>• "Back to Start here" from `/exam?q=q-tf-004-1a-mc`: `href="/start?lesson=lesson-tf-g1"` (keeps the originating lesson, not a bare `/start`); landed with `T1 — IaC with Terraform` heading, marker intact.<br>• Start here → drill link (`/exam?q=q-saa-1-1-k01-mc`) from `/start?lesson=lesson-1-1`: marker intact.<br>• Start here → lab link (`/labs?lab=gl-01`) from `/start?lesson=lesson-1-1`: marker intact. |

All five FS-R4 items are closed. No regressions found in the targeted areas.

## Regression sweep

- **Routing / deep links**: `/start?lesson=lesson-2-2` → `/exam?q=q-saa-2-2-k01-mc` → `/labs?lab=gl-08` (three full navigations, equivalent to refreshes) each rendered the correct deep-linked state (lab card open and filtered to 1, correct question loaded, correct lesson loaded) with no console errors. Browser **Back** from `/labs?lab=gl-08` returned to `/exam?q=q-saa-2-2-k01-mc`, then to `/start?lesson=lesson-2-2`; **Forward** returned correctly to `/exam?q=q-saa-2-2-k01-mc`. No stuck history entries.
- **Unknown route**: `/nope-does-not-exist` redirects to `/labs` via the catch-all `<Route path="*" element={<Navigate to="/labs" replace />} />` in `App.tsx:129`. This is a deliberate fallback, not a crash; no console errors.
- **Desktop/mobile layout across all four tabs**: at 375×812, Labs, Exam drills, Coverage, and a plain `/exam` load (which synced `?q=` to `q-a0-mc-001` on mount) all rendered with `document.documentElement.scrollWidth === window.innerWidth === 375` — no horizontal scroll on any tab.
- **Keyboard-only use**:
  - Tab order from a blank focus: skip-link → active view tab (`role="tab"`, roving `tabIndex`) → sidebar filter buttons → drill/lab cards. Verified `Header.tsx`'s tablist correctly uses `aria-selected`/`tabIndex={0/-1}` with `ArrowRight`/`ArrowLeft`/`Home`/`End` handling (`onTabKeyDown`); pressing `ArrowRight` from the focused "Labs" tab moved focus to "Exam drills" and activated it (`location.href` became `/exam?q=...`) in one step — correct ARIA tablist pattern, not a defect.
  - Exam drill cards: `Enter` on a focused `pbq-card` selects it, moves the URL to that drill's `?q=`, and lands focus on the question `<h2>`, matching the FS-R3-003/FS-R4-001 fix. Tab order from there is heading → Study link → answer choices; `Space` on a focused checkbox toggled `checked` to `true`. (Did not press "Check answers", per the read-only rules.)
  - Lab cards: `LabCard.tsx:123-135` uses a semantic `<header role="button" tabIndex={0} aria-expanded aria-label>` with an `onKeyDown` handler for `Enter`/`Space` — a correct accessible-disclosure pattern, confirmed by source read (not a regression; initially looked odd in a screenshot check but the code is sound).
  - Lesson picker: native `<select>`, verified `ArrowDown` after focusing it moves to the next option and fires `onChange`, updating `?lesson=` correctly (`lesson-1-1` → `lesson-1-2`).
- **Console**: no errors or warnings across the whole session (`read_console_messages` showed only Vite HMR/dev-server debug lines and the React DevTools info banner).
- **Network**: after 2 seconds idle on a loaded page, zero new requests fired — no polling loop. No repeated/looping requests were seen outside the already-fixed FS-R4-002 pattern.

## New issues

None found. The five FS-R4 items are closed and the regression sweep (routing, deep-link refresh, back/forward, unknown route, responsive layout, keyboard access on tabs/cards/choices/picker, console, network) turned up nothing new.
