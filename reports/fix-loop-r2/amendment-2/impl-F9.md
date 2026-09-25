# Amendment 2, batch F9: round-4 Full-Stack fixes (Study link scroll, lesson fetch dedup, ?q= sync, in-app links)

Batch F9 closes `reports/fix-loop-r2/round-4/FULLSTACK.md` items FS-R4-001 through FS-R4-005. Files touched: `frontend/src/components/StartHereTab.tsx`, `frontend/src/components/ExamDrillsTab.tsx`, `frontend/src/styles/app.css`. No other files edited. Learning content is not affected (app code only).

`npx eslint src`: **PASS** (no output). `npm run build`: **PASS** (`tsc -b && vite build`, 50 modules, no errors).

## 1. FS-R4-001 — Study link opened Start here scrolled to the bottom, focus lost

- `frontend/src/components/StartHereTab.tsx:70` — `lessonId` is now read directly from `searchParams` each render (see item 2) instead of separate state, so a lesson change is detectable via a `previousLessonId` ref.
- `StartHereTab.tsx:76-97` — added `scrollToLesson` ref, `lessonHeading` ref, and two effects: one that flags `scrollToLesson.current = true` whenever `lessonId` differs from the previous render's value (covers a picker change and a repeat in-app nav while the tab stays mounted), and one that, once `lesson` has loaded, calls `heading.scrollIntoView({ block: 'start' })` then `heading.focus({ preventScroll: true })`.
- Because `StartHereTab` only renders while `App.tsx`'s `tab === 'start'` (`frontend/src/App.tsx:109-116`), navigating in from the Exam drills Study link is a **fresh mount**, not a same-instance `lessonId` change — a ref that starts at `false` and only flips on a later change never fires for this, the primary case in FS-R4-001. Fixed by initializing `scrollToLesson` to `Boolean(searchParams.get('lesson'))` (`StartHereTab.tsx:79`), so a mount that already carries a `?lesson=` param (Study link, drill/lab "back" link) also scrolls and focuses once the lesson loads.
- `StartHereTab.tsx:290-292` — the lesson `<h2>` now has `ref={lessonHeading}`, `tabIndex={-1}`, and `className="lesson-heading"`.
- `frontend/src/styles/app.css:169-174` — added `.lesson-heading{scroll-margin-top:calc(var(--header-h, 176px) + 12px)}` and a matching `:focus` outline rule, reusing the same measured `--header-h` variable the exam tab's `.pbq-heading` uses.
- **Verified** (own tab `tab-7`, http://127.0.0.1:5173): at 1280×800, clicking "Study: A1 — Secure access to AWS resources" from `/exam?q=q-saa-1-1-k01-mr` landed on `/start?lesson=lesson-1-1` with the lesson `<h2>` at `getBoundingClientRect().top === 76.2` (header 64px + 12px margin), `document.activeElement` the `H2` with text "A1 — Secure access to AWS resources", and `window.__marker` (set before the click) still `1` (no reload). At the mobile preset (375×812) from `/exam?q=q-saa-1-1-k03-mc`, the heading landed at `top === 188.1` (header 176px + 12px), focused, marker intact.

## 2. FS-R4-002 — lesson picker fetched lesson + summary three times per change

- `StartHereTab.tsx:67-70` — removed the separate `lessonId` state and the URL-sync effect that reverted it (the old ping-pong: `setLessonIdState` fires, `setSearchParams` lands a render later, the sync effect saw `fromUrl !== lessonId` and reverted, then the URL update re-applied). `?lesson=` (or `a0-lab-safety` as default) is now the **only** source of truth: `const lessonId = searchParams.get('lesson') || 'a0-lab-safety';`.
- `StartHereTab.tsx:99-108` — `setLessonId` (called by the picker's `onChange`) now only calls `setSearchParams`; it no longer also sets local state.
- The fetch effect (`StartHereTab.tsx:~127`, unchanged besides the dependency source) still depends on `[lessonId]`, which is now the single derived value, so one URL change causes exactly one fetch pair.
- **Verified**: loaded `/start?lesson=lesson-2-1` fresh (2× `lessons/lesson-2-1` + 2× `content/summary` — expected React 18 StrictMode dev double-effect, matches the baseline noted in FULLSTACK.md for a fresh mount), then changed the picker to `lesson-3-1` via `form_input`. `read_network_requests` filtered to `/api/lessons/` showed exactly one new request: `GET /api/lessons/lesson-3-1 → 200 OK`, no repeats and no reversion to `lesson-2-1`.

## 3. FS-R4-003 — module / "All drills" change left `?q=` pointing at the old drill

- `frontend/src/components/ExamDrillsTab.tsx:49` — `useSearchParams()` destructure now keeps `searchParams` (previously discarded).
- `ExamDrillsTab.tsx:158-172` — new effect: whenever `activeQuestionId` changes and `searchParams.get('q')` doesn't already match it, `setSearchParams` replaces `q` with the new id. This covers every path that changes `activeQuestionId` — card clicks, the list-effect fallback when a module/All-drills filter drops the current drill (`ExamDrillsTab.tsx:109-121`, unchanged), and the initial catalog load — in one place, instead of only the card `onClick`.
- `ExamDrillsTab.tsx:293-305` — removed the now-redundant direct `setSearchParams({ q: q.id }, { replace: true })` call from the card `onClick`; the new effect handles it.
- **Verified**: from `/exam?q=q-saa-1-1-k03-mc` at 1024×768, clicked the "T1 — Terraform 1–3" module button in the sidebar. `location.href` became `http://127.0.0.1:5173/exam?q=q-tf-004-1a-mc` — `?q=` now follows the module's first drill instead of staying on the old id.

## 4. FS-R4-004 — "Module …" eyebrow clipped ~5px at 375

- `app.css:167` — added `scroll-margin-top:calc(var(--header-h, 176px) + 12px)` to `.pbq` (the question `<article>`, which contains the eyebrow above the `<h2>`).
- `ExamDrillsTab.tsx:64` — added a `questionArticle` ref; `ExamDrillsTab.tsx:343-347` attaches it to the `<article className="pbq">`.
- `ExamDrillsTab.tsx:149-156` and the card `onClick`'s "re-click same card" branch (`ExamDrillsTab.tsx:293-305`) now call `(questionArticle.current ?? heading).scrollIntoView({ block: 'start' })` — scrolling the article (whose top now carries the margin) — while still calling `heading.focus({ preventScroll: true })` so keyboard focus lands on the `<h2>` as before.
- **Verified**: at the mobile preset, loading `/exam?q=q-saa-1-1-k01-mr` fresh put `.pbq`'s top at `186.75` (176 + 12 margin, matches the header height) and the heading below it at `224.8`, with focus on the `<h2>` — the whole eyebrow is now within the scrolled-to region instead of the heading alone.

## 5. FS-R4-005 — "Back to Start here" and lesson drill/lab links did full reloads

- `ExamDrillsTab.tsx:17-24` — factored the Study-link lesson lookup into `findLessonForQuestion(question, summary)`, reused by `StudyLink` and the new `backToStartHref(question, summary)` (`ExamDrillsTab.tsx:36-39`), which returns `/start?lesson=<id>` when a lesson is found, else `/start`.
- `ExamDrillsTab.tsx:264-270` — `"Back to Start here"` is now `<Link to={question ? backToStartHref(question, summary) : '/start'}>`, so it also fixes the drop of the originating `?lesson=` noted in the FULLSTACK.md evidence (it used to always open A0).
- `frontend/src/components/StartHereTab.tsx:37` — the "Labs for this lesson" links are now `<Link to={...}>` instead of `<a href>`.
- `StartHereTab.tsx:305` (drill list) — the lesson's drill links are now `<Link to={...}>` instead of `<a href>`.
- **Verified** (marker set before each click, checked after): from `/exam?q=q-saa-4-4-s03-mc`, "Back to Start here" had `href="/start?lesson=lesson-4-4"` (not plain `/start`); clicking it landed with the lesson heading ("A4 — Cost-optimized networks") focused at `top === 127.5` (1024×768 header) and `window.__marker` intact. From `/start?lesson=lesson-1-1`, clicking a drill link (`/exam?q=q-saa-1-1-k01-mc`) and a lab link (`/labs?lab=gl-01`) each kept `window.__marker` set beforehand (no reload).

## Learning content affected

No — app code only (`frontend/src/**`). No Teacher validation required per the path-ownership table in `AGENTS.md`.
