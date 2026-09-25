# UI journey — `/start` (cold start, ~0–20 min)

**URL:** http://127.0.0.1:5173/start  
**Tool:** Orchestrator UI capture cross-check + `GET /api/lessons/a0-lab-safety` (MCP `cursor-ide-browser` could not open a tab this session).

## Cold-start narrative (~20 minutes)

| Minutes | What I did | Student reaction |
|--------:|------------|------------------|
| 0–3 | Landed on `/labs` (default redirect), found **Start here** tab | Expected a syllabus; relieved to see plain-language setup |
| 3–8 | Read hero **Learn it by building it**, GL-01 callout, export/import + RESET warning | Understood local-only progress and $10 guardrail |
| 8–14 | Read embedded **A0 — Lab safety** markdown (only lesson rendered on this tab) | Clear: *I* run AWS CLI; agents never touch my account |
| 14–17 | Readiness panel: AWS + Terraform **Insufficient evidence** | Motivating but vague on what “practice thresholds” means |
| 17–20 | Sidebar **0.0 Lab safety A0**; clicked **Labs** mentally planned GL-01 | Ready to try drills; no link to A1–A4/T1–T4 lesson readers |

## Visible copy (excerpt)

- Threat model: SQLite on disk, no keys in repo, teardown emphasis.
- Workflow: GL → UL → exam drills → coverage.
- Progress JSON export/import with typed `RESET` confirmation.

## Gaps noticed early

- Only **one** lesson body in the app shell; remaining 22 lessons exist on API only (see `lessons.md`).
- No in-app glossary for IAM acronyms (started jargon log in main report).

## Evidence IDs

EV-STUDENT-201, EV-STUDENT-230
