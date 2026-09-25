# UI journey — `/exam` (60-drill paper batch)

**URL:** http://127.0.0.1:5173/exam  
**Stems:** `GET /api/questions/{id}` (answers stripped server-side) — same payload the Exam tab loads.  
**Keys:** `content/questions/{id}.json` opened **after** each choice + reasoning (paper-feedback mode).  
**Submit:** **Check answers** → UI `[role=alert]` **Forbidden** / HTTP **403** (Gate 0 CSRF); no rationale in UI.

## Shell observations

- Sidebar: module filters A0, A1–A4, T1–T4; **429** questions catalogued.
- Mock exam control visible but disabled (**Phase 4 Locked** label).
- No links from a missed objective to lessons.

## Drill batch summary

| Metric | Value |
|--------|------:|
| IDs file | `reports/evidence/STUDENT/drill-60-ids.txt` |
| Questions logged | **60** |
| Paper score (vs JSON keys) | **60/60** |
| UI feedback received | **0/60** (Forbidden) |

**Pattern note:** After ~4 template SAA MC cards, every MC with “Apply the objective directly…” + three anti-patterns became trivial; MR cards always rewarded `{a,b}` vs `{c,d,e}` distractors. Real content exceptions: A0 pair + `q-tf-004-8-extra-04-mc`.

## Per-question log

| # | ID | Type | Chosen | Reason (pre-key) | UI submit | Key | Result |
|---|-----|------|--------|------------------|-----------|-----|--------|
| 1 | `q-a0-mc-001` | mc | `b` | A0 on /start says I run aws in my terminal; app never gets keys. | Forbidden (403) | `b` | OK |
| 2 | `q-a0-mr-001` | mr | `a,c` | Teardown when done; budgets warn but do not auto-stop spend. | Forbidden (403) | `a,c` | OK |
| 3 | `q-saa-1-1-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 4 | `q-saa-1-1-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 5 | `q-saa-1-1-k01-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 6 | `q-saa-1-2-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 7 | `q-saa-1-2-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 8 | `q-saa-1-2-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 9 | `q-saa-1-3-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 10 | `q-saa-1-3-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 11 | `q-saa-1-3-k01-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 12 | `q-saa-2-1-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 13 | `q-saa-2-1-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 14 | `q-saa-2-1-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 15 | `q-saa-2-2-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 16 | `q-saa-2-2-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 17 | `q-saa-2-2-k03-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 18 | `q-saa-3-1-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 19 | `q-saa-3-1-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 20 | `q-saa-3-1-k01-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 21 | `q-saa-3-2-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 22 | `q-saa-3-2-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 23 | `q-saa-3-2-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 24 | `q-saa-3-3-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 25 | `q-saa-3-3-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 26 | `q-saa-3-3-k01-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 27 | `q-saa-3-4-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 28 | `q-saa-3-4-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 29 | `q-saa-3-4-k03-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 30 | `q-saa-4-1-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 31 | `q-saa-4-1-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 32 | `q-saa-4-1-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 33 | `q-saa-4-2-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 34 | `q-saa-4-2-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 35 | `q-saa-4-2-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 36 | `q-saa-4-3-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 37 | `q-saa-4-3-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 38 | `q-saa-4-3-k02-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 39 | `q-saa-4-4-k01-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 40 | `q-saa-4-4-k02-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 41 | `q-saa-4-4-k03-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 42 | `q-tf-004-1a-mc2` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 43 | `q-tf-004-1a-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 44 | `q-tf-004-2a-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 45 | `q-tf-004-2d-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 46 | `q-tf-004-3c-mc2` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 47 | `q-tf-004-3f-mc2` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 48 | `q-tf-004-4b-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 49 | `q-tf-004-4g-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 50 | `q-tf-004-5a-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 51 | `q-tf-004-5a-mc2` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 52 | `q-tf-004-6b-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 53 | `q-tf-004-6c-mc2` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 54 | `q-tf-004-7b-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 55 | `q-tf-004-7c-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 56 | `q-tf-004-8-extra-04-mc` | mc | `a` | Workbook HCP guidance: free tier / docs-only path. | Forbidden (403) | `a` | OK |
| 57 | `q-tf-004-8b-mr` | mr | `a,b` | Reject keys in git/root; pick design + docs validation pair again. | Forbidden (403) | `a,b` | OK |
| 58 | `q-saa-1-1-k03-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 59 | `q-saa-2-1-k03-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |
| 60 | `q-saa-4-4-k03-mc` | mc | `a` | Same four choices as prior cards; pick Apply-the-objective line. | Forbidden (403) | `a` | OK |

## Evidence

EV-STUDENT-217, EV-STUDENT-219, EV-STUDENT-220
