# Retroactive approval (B5)

There is no git history. `master` has zero commits, so this is not a diff. Paths below are reconstructed from `docs/status.md`, `reports/fix-loop/round-final/`, and the files those reports name.

Decision **D2** (2026-09-25): you approved this pass-1 work as-is.

`docs/change-requests.md` marks CR-0009–CR-0016 **done**. That means the pass-1 edits were recorded. It does not mean the issue register rows are Closed. See `reports/fix-loop/issue-register.md`.

## WP4 — drill bank (CR-0009)

- `content/questions/*.json` — banned stem removed; openings later split into eight phrases; choice keys rotated so no module is over 45% one letter
- `scripts/content_lint.py` — drill IDs must exist; old stem banned; key-letter cap

Not a real scenario rewrite. That work is Q1. Student round-final: **Still present**. Teacher: banned stem **Gone**, leftover wording **Informational**.

## WP5 — lab commands (CR-0010)

- `content/labs/gl-05.json` — NACL protocol 6, port 22
- `content/labs/gl-07.json` — volume uses `$Az`
- `content/labs/gl-08.json` — user-data script (later edited again; see follow-ups)
- `content/labs/gl-17.json` — Athena `CREATE EXTERNAL TABLE` (later edited again)
- `content/labs/gl-18.json` — `file://network.json`
- `content/labs/gl-19.json` — comma-joined subnets
- `content/labs/gl-20.json` — Terraform required; fixture path
- `content/labs/gl-21.json` — title still mentions HCP Terraform
- `content/labs/ul-01.json` — GL-03 optional
- `content/labs/ul-05.json` — tag `ul-05`
- `content/labs/ul-*.json` — `beforeYouStart` filled in

Still open inside this WP: GL-07 has no EFS steps (O8), GL-21 title (O8), sidecar templates and repeated s12–s15 text (O9).

## WP6 — teardown scan (CR-0011)

- `scripts/scan_lab_placeholders.py` — unset teardown variables fail the scan; `gl-01` is skipped (decision D7)
- Many lab JSON files set unused teardown names to `$null` so the scan passes. Those labs still do not create the named resources.

## WP7 — lesson navigation (CR-0012)

- `frontend/src/components/StartHereTab.tsx` — lesson list
- Lesson `a0` permissions-boundary text
- Later follow-up: picker titles and `/exam?q=` links (not reviewed)

Still open: drill-to-lesson link (O6), lesson-to-lab and exercise links (O7).

## WP8 — front end (CR-0013)

- `frontend/src/components/ExamDrillsTab.tsx` — catalog, mock copy, select-count gate, aria-live, best scores, `?q=`
- `frontend/src/App.tsx` — unknown slug redirect, lab load error, labs fetched when the Labs tab opens
- `frontend/src/hooks/useWorkbookBootstrap.ts`
- `frontend/src/components/Header.tsx`
- `frontend/src/components/LabCard.tsx` — `aria-label` added after the review
- `frontend/src/api/client.ts` — catalog client (save message was WP1)

Still to validate: tab keyboard pattern (O3), markdown gaps (O4), 375px layout (O5). O1 and O2 were patched after the review and still need a new check.

## WP9 — API checks (CR-0014)

- `backend/workbook/views.py` — unknown choice ids return 400
- `backend/workbook/tests/test_scoring_and_api.py`
- Corrupt JSON still becomes a bare 500 (O10). Not fixed.

`DEBUG` and the hard-coded `SECRET_KEY` were left as-is. That is decision D3, not an approved by-design close.

## WP10 — citations (CR-0015)

- Lessons 4.2–4.4: the repeated "Cite official docs before labbing" sentence was replaced after the review
- Bullets still share a lesson citation file. They do not each have their own official URL.
- `content/coverage/saa_registry.json` — all 189 rows still `implemented_unverified`
- Question `mcpStatus` still mostly `pending_recheck`

## WP11 — docs (CR-0016)

- `docs/labs-and-safety.md` — sandbox paragraph. IT Manager: **Gone** for that note.
- Dated pricing snapshot and templated design exercises were not changed (D6).
- Audit-grade metrics were not built (D4).

## WP12

Live AWS runs of the 21 guided labs were not done. Agents do not call AWS (D5).

## Edits made after round-final

These were written into reviewer reports as "Lead Dev follow-up". Round 2 does not treat that as a review. They need R1–R6.

| ID | Files | What changed |
|----|-------|----------------|
| R1 | `content/labs/gl-17.json` | Second DDL bullet removed. Table is `(name string, value int)`. |
| R2 | `content/labs/gl-08.json` | Steps tell the learner to write `user-data.sh` with `Set-Content`, then pass `file://user-data.sh`. Line endings are not forced to LF. |
| R3 | `content/questions/*.json` | About 226 stems use eight openings. Recorded as not a fix. |
| R4 | `frontend/src/components/StartHereTab.tsx` | Picker shows lesson titles. |
| R5 | `StartHereTab.tsx`, `ExamDrillsTab.tsx` | Drill links use `/exam?q=<id>`. |
| R6 | `content/lessons/` domain 4 | Citation sentence replaced in lessons 4.2–4.4. |
| (with O1) | `App.tsx`, `useWorkbookBootstrap.ts` | Lab GETs run when the Labs tab is open, not on every cold start. |
| (with O2) | `LabCard.tsx` | Card button `aria-label` is `` `${chip}. ${lab.title}` ``. |
