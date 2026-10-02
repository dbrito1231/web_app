# Plan P4: Drill list UI (N4 raw IDs, N9 long card grid)

Author: Lead Developer. Status: **draft, awaiting user approval.** Phase 4 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-02)

- **N4:** on Start here, "Drills for this lesson" lists each drill by its raw ID (`StartHereTab.tsx` renders `{id}`, for example `q-saa-3-5-k07-mr`). A learner cannot tell what a drill is about.
- **N9:** on Exam drills with "All drills" selected, the grid renders a card for every drill (429), and the question appears **below** the grid (`ExamDrillsTab.tsx`). The `?q=` link scrolls to the question, so it works, but the page is very long (about 117,000 px measured in round 2) and a card click jumps far down.

## Options for N4 (KISS)

1. **Show a stem preview plus type (recommended).** Display "MC · first ~80 characters of the stem…" with the ID kept as a small muted label. The catalog already carries `stem`, as the Exam cards show `stem.slice(0, 90)`.
2. **Number them.** "Drill 1 (MC)", "Drill 2 (MR)". Short, but it says nothing about content.
3. **Keep IDs and add a tooltip** with the stem. Minimal change, but the stem is hidden on touch devices.

## Options for N9 (KISS)

1. **Show the question above the grid when one is open (recommended).** Render the question article before the card grid whenever a question is active, and keep the grid below. No scroll jump, and the `?q=` scroll code can be simplified.
2. **Default to a module filter.** Open Exam drills on the first module instead of "All", so at most about 35 cards show. Fewer cards, but "All" is still long.
3. **Collapse the grid.** Show 24 cards with a "Show all" button. Simple, but it adds state and hides drills.

## Recommended approach (N4 option 1, N9 option 1)

1. N4: in `StartHereTab.tsx`, look up each drill in the already-loaded catalog or summary and render the type plus a stem preview, with the ID as a muted label. Leave the link target (`/exam?q=`) unchanged.
2. N9: in `ExamDrillsTab.tsx`, move the `{question && <article…>}` block above `.pbq-grid`. Keep the "Back to Start here" link above it. Check that the keyboard focus moves to the question heading, as it does now.
3. Update the existing Playwright tests in `frontend/tests/e2e/` that assert on drill IDs or on the card and question order, and add one test for each change.

## Files

`frontend/src/components/StartHereTab.tsx`, `frontend/src/components/ExamDrillsTab.tsx`, and possibly `frontend/src/styles` for the muted label; the register.

## Risks

- A layout change can break the `?q=` deep link and focus behaviour that round 5 fixed (FS-R2-2-001, R5). The smoke test must cover a `?q=` link, a card click, keyboard focus and the 375 px width.
- No grading logic changes.

## Tests

`npm run build`; `npm run test:e2e`; a browser smoke test on a throwaway DB (as in the final sitting: `?q=` deep link, card click, answer grading, a 375 px viewport, no horizontal scroll); `manage.py test workbook`.

## Learning content affected

No content changes. The UI changes what the learner sees (how drills are labelled and placed), so per AGENTS.md the Teacher validates before and after, and a Student checks the screens.
