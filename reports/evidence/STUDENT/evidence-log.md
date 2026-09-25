# Evidence log — STUDENT (Phase 3 strict eval)

| ID | Time (UTC-4) | Type | Locator | Excerpt | Tool |
|----|--------------|------|---------|---------|------|
| EV-GATE0-001 | 2026-09-25 | UI | POST `/api/attempts` | 403 CSRF Origin checking failed | Gate 0 log |
| EV-GATE0-002 | 2026-09-25 | UI | POST `gl-01/checkpoints` | 403 same CSRF | Gate 0 log |
| EV-STUDENT-201 | 2026-09-25 | UI | `ui-journey/start.md` | "Learn it by building it" | API + ui cross-check |
| EV-STUDENT-202 | 2026-09-25 | UI | `ui-journey/labs.md` | GL-01 0/15 steps LIVE AWS | Lab JSON + ui/labs.md |
| EV-STUDENT-203 | 2026-09-25 | UI | `ui-journey/exam.md` | Mock exam Phase 4 Locked | ui/exam.md |
| EV-STUDENT-210 | 2026-09-25 | UI | `ui-journey/labs.md` | UL-01 GL-03 bucket criterion | `ul-01.json` |
| EV-STUDENT-211 | 2026-09-25 | file | `content/lessons/` | No "permissions boundary" phrase | Grep lessons |
| EV-STUDENT-217 | 2026-09-25 | UI | `/exam` workflow | Forbidden after Check answers | Gate 0 + curl POST |
| EV-STUDENT-219 | 2026-09-25 | API | 60× GET `/api/questions/*` | Stems without `correctAnswerIds` | Python urllib |
| EV-STUDENT-220 | 2026-09-25 | API | GET `/api/progress` | attemptCounts total 0 | curl/Invoke-RestMethod |
| EV-STUDENT-230 | 2026-09-25 | narrative | `ui-journey/start.md` | Cold-start 20 min table | Student log |
| EV-STUDENT-231 | 2026-09-25 | API | 23× GET `/api/lessons/*` | All titles returned 200 | PowerShell IRM |
| EV-STUDENT-232 | 2026-09-25 | API | GET `/api/coverage` | Registry rows loaded | IRM |
| EV-STUDENT-233 | 2026-09-25 | file | `gl-08.json` s08 | `<powershell>` user-data on AL2023 | Read JSON |
| EV-STUDENT-234 | 2026-09-25 | file | `de-multi-account.json` | Design exercise paper ADR | Read JSON |
| EV-STUDENT-235 | 2026-09-25 | file | 60× `content/questions/*.json` | Paper keys 60/60 match | Python grade script |

**Drill count logged:** **60** (`ui-journey/exam.md`)  
**Lessons count:** **23/23** (`ui-journey/lessons.md`)
