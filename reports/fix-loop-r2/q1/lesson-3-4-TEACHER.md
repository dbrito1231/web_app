# Teacher review — Lesson 3.4 (Round 1)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**AWS-L34-001 (misattribution, Lesson 2.2→2.1):** Agree. Confirmed lesson-2-2.json has zero CloudFront/Global Accelerator mentions; that contrast is in lesson-2-1.json K07. Fix as AWS stated.

**Claim table:** Spot-checked 7 rows AWS didn't emphasize (2 Origin Shield, 5 RFC1918, 6 subnet /28–/16, 8 CIDR non-resizable, 11 endpoint service definition, 16 LAG/LACP, 18 Local Zone definition) — verified 2, 11, 16 live via `search_documentation`; all others match known stable AWS wording exactly. No discrepancies.

**Coverage:** All 8 `SAA-3.4-*` objectives present as `###` sections in id order, each fully taught with an `**Exam tip:**` line. Matches `objectiveIds`.

**Teaching quality:** Clear for a college IT student. Required contrasts all present and correct: peering vs Transit Gateway vs PrivateLink (K04/S02), gateway vs interface endpoints (K04), DX vs VPN including VPN-over-DX and DX+VPN-backup patterns (K04), CloudFront vs Global Accelerator (K01, consistent with 2.1 K07). No filler. Checked against lessons 2.1, 2.2, 3.2 — no contradictions (the K01 lesson-2.2 reference is the one misattribution, already covered above; Local Zones/Wavelength framing in S03 is consistent with 3.2 K02).

**Length/format:** 2,315 words is fine, no filler. However `q1_batch_check.py 3-4` reports:
```
FAIL: lesson single-asterisk spans: 3
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
```
The 3 stray asterisks are the wildcard glyphs in `` `/images/*` `` and `` `/api/*` `` (K01, first paragraph) — literal `*` characters inside backticks that the linter can't distinguish from italics markup.

- **TEACHER-L34-002** (minor, format/lint-blocking) — Section K01, first paragraph, the sentence with `` `/images/*` `` and `` `/api/*` ``. Fix: reword to avoid a bare single asterisk, e.g. "a path prefix such as `/images/` for static assets or `/api/` for API calls" (drop the trailing wildcard character; meaning is unchanged). Must be fixed before `q1_batch_check.py 3-4` can show no FAIL.

**Teach-before-test:** All 13 drillIds' objectives (K01–K04, S01–S04, mc/mr) have sufficient depth and distinct facts taught to support their questions and distractors — no additions requested at this time. Will re-check once questions are drafted, per Round 2.

**Retired/closed services:** None used; no new finds for the RULES.md list.

Lesson 3.4: not yet (blocked only on TEACHER-L34-002 lint fix; content itself is sound)

Overall: concerns
