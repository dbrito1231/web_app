# AWS review — Lesson 3.4 (High-performing network architectures), Round 1

## Per-section verdicts

- Intro: fine — correctly says "Lessons 2.1 and 2.2" cover the callback list as a group.
- K01 (edge networking): accurate content, but misattributes its callback (see AWS-L34-001).
- K02 (network architecture design): accurate — CIDR sizing, RFC 1918, reserved addresses, route-table-defines-public/private all verified.
- K03 (load balancing concepts): accurate, correctly attributed to Lesson 2.1.
- K04 (connection options): accurate — VPN bandwidth, DX speeds/LAG, PrivateLink/gateway-vs-interface endpoints all verified against docs.
- S01 (topology): accurate, consistent with 2.1/2.2/3.2.
- S02 (scaling configs): accurate — CIDR non-resizable, peering non-transitive, Transit Gateway hub model verified.
- S03 (resource placement): accurate — Local Zones/Wavelength descriptions consistent with lesson 3.2's own K02 treatment of the same services.
- S04 (load balancing strategy): accurate; the enhanced-networking callback to 3.2 S03 correctly reuses that lesson's verified fact and citation.

## Claim table check

Spot-checked 10 of 20 rows (1, 3, 4, 7, 9, 12, 13, 14, 15, 17) directly against `search_documentation` results this round; all quotes and numbers verified as stated. Table has 20 rows, well above the 8-row minimum.

## Issues

- **AWS-L34-001** (minor, factual misattribution) — Section K01, first paragraph: "Lesson 2.2 already contrasts CloudFront with Global Accelerator at a high level." This content is actually in **Lesson 2.1, section K07** ("How to appropriately use edge accelerators"), not Lesson 2.2. Lesson 2.2 contains no mention of CloudFront or Global Accelerator (verified: 0 occurrences of either string in `content/lessons/lesson-2-2.json`). Fix: change "Lesson 2.2" to "Lesson 2.1" in that sentence.

No other contradictions found against lessons 2.1, 2.2, or 3.2. The K04/S02 peering, PrivateLink, and Transit Gateway material has no overlapping/conflicting mentions in 2.1 or 2.2 (both are silent on those topics), and the enhanced-networking callback to 3.2 S03 matches that lesson's wording exactly.

## Coverage

All 8 objectives (SAA-3.4-K01–K04, S01–S04) present as `###` sections in id order, each ending with an `**Exam tip:**` line. `objectiveIds` in the lesson JSON match all 8 ids from `content/objectives/saa_c03.json`.

## Lint / checks

- `scripts/content_lint.py`: PASS (`questions 429 aws 310 tf 119`, `labs 21 + 21`, `lessons 23`).
- `q1_batch_check.py 3-4` (per writer's report): lesson lines PASS; remaining FAILs are on the still-unwritten placeholder questions, out of scope for this round.

## Retired/closed services

None used. No new finds to add to the RULES.md list.

Lesson 3.4: approve for question writing

Overall: concerns
