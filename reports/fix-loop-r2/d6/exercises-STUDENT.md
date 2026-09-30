# Student run — D6 design exercises (12): run 1 (partial)

The Student was a Sonnet agent working from a text packet: 11 lessons and 12 exercises (4 per batch), shuffled. The run stopped partway with an API error: a false-positive safety flag, `[reasoning_extraction]`, not a content problem. Saved by the Lead Dev from the partial output.

## Designs (committed before reading the intended designs)
All 12 designs were committed first. All 12 match the intended designs; self-grades were 13–14 of 14.
- **E1 (2.1-s03):** SNS fan-out to one SQS queue per team.
- **E2 (4.3-s04):** time-series, columnar and relational stores.
- **E3 (purchasing):** a Compute Savings Plan for the floor, Spot for the render job, On-Demand for the rest.
- **E4 (4.4-s07):** 2 VPN connections (4 tunnels) with ECMP to the Transit Gateway.
- **E5 (snow):** Data Transfer Terminal for the bulk load, then DataSync.
- **E6 (4.1-s05):** Glacier Instant Retrieval plus lifecycle and noncurrent-version rules.
- **E7 (3.1-s01):** io2 and st1.
- **E8 (multi-region-dr):** pilot light plus a quota increase requested in advance.
- **E9 (visualization):** SPICE, and Athena with direct query.
- **E10 (1.3-s05):** replication with RTC plus Batch Replication, and AWS Backup by tag.
- **E11 (direct-connect):** 10 Gbps Direct Connect, a VPN pilot and VPN backup.
- **E12 (3.4-s02):** Transit Gateway plus a secondary CIDR.

## Comparison (E1–E5 completed before the stop)

**E1**
- A mild second design (EventBridge with SQS targets). Both reviewers had already accepted either mechanism.
- The requirement wording spells out fan-out.

**E2**
- Athena on Parquet is a plausible alternative for the survey data, but lesson 4.3 S04 names only Redshift.
- The run-rate cap cannot be checked because no prices are given, although the rubric item itself can be.

**E3**
- The design is unique.
- The requirement wording points to a Compute Savings Plan and Spot.

**E4**
- Slightly untaught: the lesson does not say that both tunnels of one VPN connection carry traffic under ECMP.
- The scenario names "BGP and equal-cost multi-path".

**E5**
- The Enterprise Support restriction is untaught, but the scenario states the plan, so nothing depends on it.
- "an AWS facility that accepts physical uploads" points to the Data Transfer Terminal.

**E6–E12:** not compared, because the run stopped.

## Lead Dev reading of the "giveaway" flags
Most of the flagged phrases are the requirement the design has to meet, such as "saves its progress every 15 minutes" or "each team must receive every order". This is the design-exercise equivalent of a structural scenario reference, not leakage. Two are closer to real hints and go to the re-run and the reviewers:
- E4's "router supports BGP and equal-cost multi-path"; the writer added it as context after AWS-DE3-017.
- E5's "an AWS facility that accepts physical uploads"; the reviewer added it in AWS-DE2-002, and the Teacher accepted it because the learner still has to name the service.

---

# Student run 2 — E6–E12 (completes the comparison)

This was a fresh Sonnet agent. It wrote its designs before reading the intended ones. Saved by the Lead Dev (condensed).

- **Match:** 7 of 7. E11 has a variant (hosted 5 Gbps against dedicated 10 Gbps DX, LBT against ECMP tunnels) that the rubric already accepts.
- **Completable from the lessons alone:** 7 of 7. Small untaught edges, none needed to pass:
  - E11: whether an LBT can be combined with a private-IP VPN over DX.
  - E9: QuickSight's own pricing model.
  - E12: the spoke route-table detail.
- **Solution pointers beyond the stated requirement:** none clear. Two mild ones, both requirement-level: E8's "a continuously running replicated database there is acceptable" and E9's "each full read of the sales files has a cost".
- **Figure inconsistencies:** none.
- **Uncheckable rubric items:** none.
- **One ambiguity, in E6 (de-saa-4.1-s05):** "Finance wants none of that waste kept longer than 7 days" could be read as covering the superseded copies, which r7 requires to go at day 60. **Fixed at c47c3de:** "Finance wants those broken upload leftovers gone within 7 days." The Teacher's second-role check is pending.

Student verdict (run 2): fair

## Combined result across both runs
- **Designs:** 12 of 12 match the intended designs. No second design goes beyond what the reviewers already accepted (E1 fan-out mechanism, E11 variants).
- **Two borderline hints, from run 1, recorded rather than changed:** E4's "router supports BGP and equal-cost multi-path" and E5's "an AWS facility that accepts physical uploads". The reviewers accepted both as context.
- **Untaught details:** one (E4: both tunnels of one VPN connection carry traffic under ECMP). It is recorded for the final-sitting lesson follow-ups.
