# Fix-loop r2 — Full-Stack (round-1)

Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Role: Full-Stack  
Date: 2026-09-25  
App code: not modified. No Playwright. No POST attempts/checkpoints. Servers not started (already up).

## Scope

- **R4** — `frontend/src/components/StartHereTab.tsx` lesson picker: titles (not raw ids) for all index lessons; keyboard; screen-reader labels.
- **R5** — Lesson drill links → `/exam?q=<id>`; `ExamDrillsTab.tsx` opens that question; bad id shows a clear message; back works.

**Browser:** Cursor browser MCP was unavailable for a usable session (tab create returned a `viewId`, then `browser_navigate` reported the view missing / “No browser tab available”). Live checks used `GET http://127.0.0.1:8000/api/content/summary` and code review; frontend `GET http://127.0.0.1:5173/start` returned 200.

---

## R4

**Verdict: Pass**

### Titles for all lessons in the index

- API `GET /api/content/summary` returns `lessonIndex` with **23** rows; `lessons` length is also **23**.
- Every row has a non-empty `title`, and **none** equal the raw `id` (`title_eq_id_or_empty = 0`). Sample: `a0-lab-safety` → `A0 — Lab safety and local threat model`; `lesson-1-1` → `A1 — Secure access to AWS resources`.
- Backend builds that list in `backend/workbook/content_loader.py:75-80` (`title` from lesson JSON, fallback to id only if missing).
- UI prefers `summary.lessonIndex` and renders `row.title` in each `<option>`:

```207:215:frontend/src/components/StartHereTab.tsx
          <label className="lesson-picker">
            Lesson
            <select value={lessonId} onChange={(e) => setLessonId(e.target.value)}>
              {lessonIndex.map((row) => (
                <option key={row.id} value={row.id}>
                  {row.title}
                </option>
              ))}
```

- Load path: `StartHereTab.tsx:26-32` — `api.contentSummary()` then `setLessonIndex(summary.lessonIndex)` when present.

### Keyboard support

- Control is a native `<select>` (`StartHereTab.tsx:209`). Platform keyboard (focus, arrows, typeahead, Enter/Space to open) applies; no custom widget blocking keys.

### Screen-reader labels (aria)

- Visible text **Lesson** wraps the `<select>` inside `<label className="lesson-picker">` (`StartHereTab.tsx:207-209`). That is a valid implicit label association; the control’s accessible name is “Lesson” without needing a separate `aria-label`.
- Aside already has `aria-label="Start here nav"` (`StartHereTab.tsx:128`).

---

## R5

**Verdict: Fail**

### Code path (lesson → exam)

1. Lesson body lists drills as plain anchors: `StartHereTab.tsx:222-225` — `<a href={`/exam?q=${encodeURIComponent(id)}`}>`.
2. Routing: `App.tsx:13,105,121` — path `/exam` → `ExamDrillsTab`.
3. On mount, catalog load reads `q`: `ExamDrillsTab.tsx:52-56` — `URLSearchParams(...).get('q')`, find in catalog, `setActiveModule(null)` + `setActiveQuestionId(pick.id)`.
4. Second effect loads the question: `ExamDrillsTab.tsx:82-106` — `api.question(activeQuestionId)`.

**Valid id:** Pass (code). Example drill from A0 content: `q-a0-mc-001` is present in `/api/content/catalog` (429 questions; id confirmed).

### Bad id → clear message

**Fail.** If `q` is set but not in the catalog, the code does **not** set an error or empty state; it falls through to the first catalog row:

```52:59:frontend/src/components/ExamDrillsTab.tsx
        const requested = new URLSearchParams(window.location.search).get('q');
        const pick = rows.find((row) => row.id === requested);
        if (pick) {
          setActiveModule(null);
          setActiveQuestionId(pick.id);
        } else if (rows[0]) {
          setActiveQuestionId(rows[0].id);
        }
```

No branch distinguishes “missing `q`” from “unknown `q`”. URL can still show `?q=bad-id` while another question is shown. `error` / `role="alert"` (`ExamDrillsTab.tsx:245-248`) only covers `api.question` failures, not unknown catalog ids.

### Back button

**Fail (no control to verify).** There is no in-app Back / “Study: …” control in `ExamDrillsTab.tsx` (repo grep: no `history.back`, `navigate(-1)`, or “Study:” link; O6 remains open for drill→lesson). Browser history Back after a real `<a href="/exam?q=…">` navigation is plausible but was **not** exercised (browser unavailable). Acceptance “the back button works” is not met by current UI.

---

## New issues (Low+)

| ID | Severity | Location | Note |
|----|----------|----------|------|
| FS-R2-R1-001 | Low | `StartHereTab.tsx:224` | Drill list link text is the raw question id (`{id}`), not stem/title. |
| FS-R2-R1-002 | Low | `StartHereTab.tsx:33-35` | If `lessonIndex` were empty, picker falls back to `title: id` (raw ids). Live API currently supplies full `lessonIndex`, so R4 still Pass. |

R5 bad-`q` silent fallback and missing back/Study control are the R5 Fail criteria above (not re-listed as separate new issues).
