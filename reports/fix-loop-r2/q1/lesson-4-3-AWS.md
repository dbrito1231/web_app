# Lesson 4.3 - Senior AWS Solutions Architect review (Round 1)

Reviewed against:
- `content/lessons/lesson-4-3.json`
- `reports/fix-loop-r2/q1/lesson-4-3-impl.md` (claim table)
- `reports/fix-loop-r2/q1/RULES.md`

## Per-objective teach-before-test readiness

- SAA-4.3-K01: **Ready** - discount scope and commitment mechanics are explicit (RDS Reserved DB instances vs Compute Savings Plans scope).
- SAA-4.3-K02: **Ready** - Cost Explorer vs Budgets vs CUR decision boundaries are concrete and exam-usable.
- SAA-4.3-K03: **Ready** - DAX vs ElastiCache and consistency constraints are clearly distinguishable.
- SAA-4.3-K04: **Ready** - retention windows and snapshot expiration behavior are concrete across RDS, Aurora, and DynamoDB PITR.
- SAA-4.3-K05: **Ready** - RCU/WCU definitions, on-demand scaling rules, ACU sizing, and switch limits are specific enough for option elimination.
- SAA-4.3-K06: **Ready** - proxy use cases and failover behavior are clear and separable from replica/caching patterns.
- SAA-4.3-K07: **Ready** - homogeneous vs heterogeneous migration and endpoint constraints are explicit.
- SAA-4.3-K08: **Ready** - read replica vs Multi-AZ standby purpose, replication mode, and failover timing are explicit.
- SAA-4.3-K09: **Ready** - relational/non-relational selection and pricing-mode contrasts are specific with thresholds.
- SAA-4.3-S01: **Ready** - backup-policy design tradeoffs and service-specific retention/PITR details are taught concretely.
- SAA-4.3-S02: **Not ready** - section stays high-level and lacks at least one concrete, doc-grounded engine differentiator (see AWS-L43-001).
- SAA-4.3-S03: **Ready** - workload-shape-to-pricing-mode mapping is explicit, including commitment compatibility.
- SAA-4.3-S04: **Ready** - time-series vs columnar vs transactional/key-value distinctions are explicit and status-aware.
- SAA-4.3-S05: **Ready** - migration sequencing and cross-engine risk framing are concrete enough for question design.

## Issues

- **AWS-L43-001 (medium)**  
  **Location:** `SAA-4.3-S02`, phrase `"specific extension or SQL behavior need"`  
  **Problem:** The section describes engine choice in general terms but does not provide a concrete, verifiable engine distinction that question writers can test directly from lesson prose.  
  **Doc-verified fix (add sentence):** `"RDS for PostgreSQL supports many PostgreSQL extensions."`  
  **Source:** `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.FeatureSupport.Extensions.html`

## Claim table verification results

Rows verified: **all 40 rows** (including every number-bearing row).  
Outcome: **all 40 rows verified** (quote verbatim and claim support confirmed).

- Row 1: verified.
- Row 2: verified.
- Row 3: verified.
- Row 4: verified.
- Row 5: verified.
- Row 6: verified.
- Row 7: verified.
- Row 8: verified.
- Row 9: verified.
- Row 10: verified.
- Row 11: verified.
- Row 12: verified.
- Row 13: verified.
- Row 14: verified.
- Row 15: verified.
- Row 16: verified.
- Row 17: verified.
- Row 18: verified.
- Row 19: verified (capacity range is version-dependent in source doc; lesson already notes compatibility context).
- Row 20: verified.
- Row 21: verified.
- Row 22: verified.
- Row 23: verified.
- Row 24: verified.
- Row 25: verified.
- Row 26: verified.
- Row 27: verified.
- Row 28: verified.
- Row 29: verified.
- Row 30: verified.
- Row 31: verified.
- Row 32: verified.
- Row 33: verified.
- Row 34: verified.
- Row 35: verified.
- Row 36: verified.
- Row 37: verified.
- Row 38: verified.
- Row 39: verified.
- Row 40: verified.

## Additional lesson checks

- Objective coverage: all 14 objectives (`K01-K09`, `S01-S05`) have dedicated sections in order.
- Exam tips: each objective section ends with useful `**Exam tip:**` guidance.
- Markdown subset: valid for established pattern (single `##` lesson title retained intentionally; no prohibited tables/links/numbered lists found).
- Retired/closed/renamed status:
  - Timestream for LiveAnalytics is correctly labeled as closed to new customers effective 2025-06-20.
  - Additional check performed for QLDB closure status; no AWS availability-change notice found in reviewed docs search results.

Lesson 4.3: not yet

Overall: concerns
