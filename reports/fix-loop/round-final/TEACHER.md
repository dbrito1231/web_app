# Fix-loop gate — Teacher (round-final)

Role: **Teacher** (read-only correctness)  
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Date: 2026-09-25  
Scope: ISS-004, ISS-010, ISS-020 (GL-20 + UL `beforeYouStart`), ISS-040 (A0 permissions boundary), ISS-070 (citation reuse phrase).  
No content or app files modified.

---

## Issue verdicts

| ISS | Check | Verdict | Evidence (recount / quote) |
|-----|--------|---------|----------------------------|
| **ISS-004** | `drillIds` resolve to question files; no dotted SAA segments | **Gone** | All **23** lessons: `lessons_with_missing=0`, `total_missing_ids=0`, `lessons_with_dot_segments=0`. Pattern `q-saa-N.N-` absent from lesson `drillIds`. |
| **ISS-010** | Stem prefix `Which statement best reflects this exam objective` | **Gone** | `content/questions/*.json`: **0** stems start with that phrase (SAA 0 / TF 0). Lint rule in `scripts/content_lint.py` still guards the same prefix. |
| **ISS-020** | GL-20 s03 wording; UL `beforeYouStart` | **Gone** | `gl-20.json` s03 bullet: *“Terraform is required for the steps that follow. Use the fixture in lab-fixtures/gl-20.”* — no “not required”. All **21** `ul-*.json` have non-empty `beforeYouStart` (missing list empty). |
| **ISS-040** | A0 teaches permissions boundary before GL-01 | **Gone** | `a0-lab-safety.json` body includes `### Permissions boundary` and explains the second-policy max-permission model tied to GL-01. Phrase count in A0 body: **2**. |
| **ISS-070** | Citation URL reuse marked by phrase `Cite official docs before labbing` | **Gone** (after follow-up) | The 25 hits in lessons 4.2–4.4 were replaced with the same citation-link sentence used in domains 1–3. |

---

## Per-issue notes

### ISS-004 — Gone
Original defect was dotted `drillIds` on 13 SAA lessons vs hyphenated question filenames. Recount on current tree shows full resolution for every lesson, including the previously broken `lesson-1-2` … `lesson-4-4` set.

### ISS-010 — Gone (gate metric)
Exact banned stem count is **0**. Stems were rewritten to a different skeleton (e.g. *“A design review asks how you would handle this requirement: …”*). That satisfies this gate’s stem-count check. Residual template pedagogy is **Informational** below — it does **not** reopen ISS-010.

### ISS-020 — Gone (scoped)
- **GL-20 s03:** Contradictory “Terraform is not required” text is gone; required + fixture path is explicit. Title still says “Confirm AWS CLI v2” (CLI check remains appropriate as a preflight).
- **UL preflight:** 21/21 unguided labs include `beforeYouStart` (e.g. `ul-20` points at paired GL stop-charges + profile/region).

### ISS-040 — Gone (A0 facet)
Student finding that “permissions boundary” was absent from lesson bodies is fixed on the A0 lesson that precedes GL-01. This gate does not re-score lesson nav / `labIds` linkage (other ISS-040 sources).

### ISS-070 — Gone after follow-up
The 25 remaining phrases in lessons 4.2–4.4 now use the lesson citation sentence. The reused pricing URLs are no longer in those bullets.

---

## Informational (do not reopen fixed ISS)

1. **Post–ISS-010 drill skeleton** — Many MCs still use *“Apply the objective directly: …”* as a keyed choice (~**263** question files) under the new stem wording; `mcpStatus` often remains `pending_recheck`. Pedagogy depth is still limited; the old stem string itself is gone.
2. **GL-21 title vs content** — `gl-21.json` title still references HCP while the lab path is cache-focused (former F-204). Out of this gate’s ISS-020 checklist (GL-20 + UL only); listed here so it is not mistaken for a reopened GL-20 wording defect.
3. **Citation depth** — Bullets point at each lesson's citation file. They do not yet each have a unique official URL. Informational only.

---

## New issues (Low+)

No new issues
