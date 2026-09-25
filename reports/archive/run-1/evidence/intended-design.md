# Intended design (locked decisions)

Sources: `AGENTS.md`, `.cursor/plans/aws_terraform_workbook_92c3d04f.plan.md`, `.cursor/plans/ccna_layout_replica_160c046c.plan.md`, `docs/labs-and-safety.md`.

Evaluators must treat the following as **intended**, not defects. Disputes file as *design concern*.

## Product shape

- Local-only workbook: Vite + React on `127.0.0.1:5173`, Django 6.1.1 on `127.0.0.1:8000`, SQLite progress in `backend/db.sqlite3`.
- Four tabs only: Labs, Exam drills, Coverage, Start here (CCNA-style layout replica).
- No login, no hosting, no AWS calls from the app, no credentials in the app, no LLM API, no browser terminal.
- KISS: features must teach an exam bullet, protect from surprise AWS bill, or score/store progress.

## Curriculum

- SAA-C03: 189 atomic tracking IDs; Terraform Associate 004: 37 lettered objectives.
- Path: A0 → A1–A4 (AWS) → T1–T4 (Terraform).
- Drill bank: MC/MR only; design exercises for bullets without live labs.
- Services not run in labs (Direct Connect, Outposts, CloudHSM, etc.) stay in lessons/exercises by design.

## Labs

- 21 guided (GL-01…GL-21) + 21 unguided (UL-01…UL-21) pairs; unguided hides solution until gate.
- PowerShell-first CLI; learner runs AWS/Terraform in their own terminal; agents never execute AWS.
- Cost panels, `beforeYouStart`, teardown, and hourly-cost warnings are required product behavior.
- `$10` is a warning threshold, not a hard stop.
- CR-0005 rewrites (2026-09-25) aimed at runnable steps and ordered teardown; post-CR lab quality is in scope for evaluation, not “template labs are OK.”

## Agents / content workflow

- Teacher: read-only correctness owner; findings → change requests (Lead Dev writes `docs/change-requests.md`).
- Lead Dev: only writer; plan-first for changes.

## UI / progress

- Export/import and reset exist for local backup; no multi-user tracking by design.
- Readiness and coverage are separate from “pass probability”; no scaled exam score from practice accuracy.

## Closed change requests (do not re-report unless regressed)

- CR-0001 lesson 1-1 drill ID hyphens — done for `lesson-1-1` only; **regression:** 20 other SAA lessons still use dotted `drillIds` (Teacher F-01, eval 2026-09-25)
- CR-0002 GL-01 beforeYouStart rendering — done
- CR-0003 unguided labs on Labs tab — done
- CR-0004 superseded by CR-0005 — done
- CR-0005 lab rewrites batches A–E — done in log; Teacher + AWS post-review **concerns**: placeholder scan PASS is not full teardown proof (AWS-005); confirmed blockers on GL-05/08/17 (AWS-001–003); Teacher F-03–F-07 in `02-teacher.md`
