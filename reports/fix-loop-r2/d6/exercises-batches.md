# D6 Part B — exercise batch assignment (fixed before writing)

Rule (Teacher (d), plan `d6_iss080_pricing_and_exercises_20260929.plan.md`): each exercise goes to the batch of the domain of its **first** `objectiveIds` entry. The lists are fixed on 2026-09-29, before any exercise is rewritten.

## Batch 1 — domains 1–2 (20)
- 1.1: de-federation, de-multi-account
- 1.2: de-direct-connect, de-saa-1.2-s03
- 1.3: de-cloudhsm, de-saa-1.3-s01, de-saa-1.3-s03, de-saa-1.3-s05, de-saa-1.3-s07
- 2.1: de-saa-2.1-s02, de-saa-2.1-s03, de-saa-2.1-s04, de-saa-2.1-s06, de-saa-2.1-s07
- 2.2: de-multi-region-dr, de-saa-2.2-s01, de-saa-2.2-s02, de-saa-2.2-s04, de-saa-2.2-s07, de-saa-2.2-s08

## Batch 2 — domain 3 (16)
- 3.1: de-saa-3.1-s01, de-saa-3.1-s02
- 3.2: de-saa-3.2-s04
- 3.3: de-saa-3.3-s01, de-saa-3.3-s03
- 3.4: de-cdn, de-saa-3.4-s01, de-saa-3.4-s02, de-saa-3.4-s03
- 3.5: de-data-lake, de-emr-glue, de-saa-3.5-s03, de-saa-3.5-s06, de-snow, de-streaming, de-visualization

**Note for batch 2:** `de-snow` covers AWS Snow Family, which is closed to new customers (RULES "Retired, end-of-support or closed services"). The scenario must state that status clearly and must not present Snow Family as current advice. `de-direct-connect` (batch 1) and `de-outposts` (batch 3) are current services, but they cannot be provisioned in a personal lab. That is what `constraint_reason` covers.

## Batch 3 — domain 4 (24)
- 4.1: de-saa-4.1-s01, s02, s04, s05, s06, s08, s09, s10, de-storage-migration
- 4.2: de-outposts, de-purchasing, de-saa-4.2-s01, s02, s03, s04, s05
- 4.3: de-db-migration, de-saa-4.3-s02, de-saa-4.3-s04
- 4.4: de-saa-4.4-s03, s05, s07, de-tgw, de-throttling
