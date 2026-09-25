# Application map (Phase 2)

## Shell

- Header: product title + tablist (`Labs` | `Exam drills` | `Coverage` | `Start here`)
- Routes: `/labs`, `/exam`, `/coverage`, `/start` (React Router)
- Bootstrap: `useWorkbookBootstrap` loads summary, progress, readiness, coverage

## Tabs and primary controls

| Tab | Purpose | Key controls | DB writes |
|-----|---------|--------------|-----------|
| Start here | Onboarding, A0 lesson sidebar, readiness, export/import/reset | Lesson nav, progress textbox, Copy/export, Import, Reset (typed RESET) | Import/reset POST only if user clicks (eval forbidden) |
| Labs | 42 lab cards (GL+UL pairs), steps/criteria, checkpoints, cost/stop panels | Module sidebar, expand lab, checkpoint toggles, reveal solution | `POST /api/labs/<id>/checkpoints` |
| Exam drills | 429-question catalog, module filter, MC/MR UI | Question list, choices, Check answers | `POST /api/attempts` |
| Coverage | SAA registry status, drill-down | Domain/task filters | none (read-only) |

## Learner flows

1. **Drill:** pick module → pick question → select choice(s) → Check answers → rationale panel (from POST response).
2. **Lab:** pick lab → read before you start / steps → tick checkpoints → optional reveal for solution/teardown detail.
3. **Coverage:** find `missing` bullets → link back to lessons/drills (via IDs in registry data).

## API surface (GET samples in `evidence/api/`)

- Health, content summary, coverage, progress, readiness, export
- Lesson/question/lab detail; lab `?reveal=1` exposes solution
- Question GET strips `correctAnswerIds` but **includes `rationale`** (see PYTHON-001 / FULLSTACK-001)

## Error handling (sample)

- Unknown lesson/question/lab IDs return JSON error bodies (snapshots in `api/lesson-unknown.json`, etc.)
