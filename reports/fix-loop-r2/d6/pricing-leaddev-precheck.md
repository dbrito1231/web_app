# D6 Part A — Lead Dev pre-check (before review)

I recomputed both figures for all 16 labs from each lab's own basis line. Billed hours are ceil(estimatedMinutes/60) where the basis says "billed in full hours". Storage is prorated at /730 h per month.

## Correct
gl-06, ul-06 ($0.05/h × 2 h = $0.10; × 24 = $1.20); gl-07; gl-14 ($0.036 + storage = $0.043 → $0.05; 24 h $0.514 → $0.52); ul-14; gl-18 and ul-18 (figures only; see wording); gl-19; ul-19 ($0.1176/h → $0.24; 24 h $2.82 → $2.83); gl-21; ul-21. All 24 h figures reconcile, except that ul-07 is kept at $0.72 by design (EFS rate unread).

## Findings

**LD-PA-001 (medium): four same-hour figures are below their own basis.** The plan says to round up, never down.

| Lab | Stated | Recomputed | Should be |
|---|---|---|---|
| gl-08 | $0.08 | (0.0225 + 2×0.005 + 0.0104) × 2 h = 0.0858, plus gp3 ≈ 0.0876 | $0.09 |
| ul-08 | $0.09 | gl-08 + WAF $6/month (≈ $0.0082/h) × 2 h ≈ 0.104 | $0.11 |
| gl-09 | $0.03 | 0.0154 × 2 h = 0.0308, plus gp3 ≈ 0.0326 | $0.04 |
| ul-09 | $0.05 | the basis says 2 instances at peak: 2 × 0.0154 × 2 h = 0.0616, plus storage and alarms | $0.07 (or restate the basis as 1 instance most of the run and 2 briefly) |

**LD-PA-002 (low): the gl-18/ul-18 basis wording.** "0.25 vCPU at $0.000011244/vCPU-second ($0.0405/h)" reads as if $0.0405/h were the cost of 0.25 vCPU. It is the rate per vCPU-hour; 0.25 vCPU costs about $0.0101/h. The figures are correct. Reword to "($0.0405 per vCPU-hour)" and "($0.00445 per GB-hour)".

**LD-PA-003 (low): typo.** In gl-06/ul-06, "N. Virginia rate rate not verified" should read "N. Virginia rate not verified".

**LD-PA-004 (note): same-hour for gl-18.** The basis says the task exits on its own. The same-hour figure of $0.03 uses 1.5 h of Fargate at 0.25 vCPU, so it is still an upper bound. No change needed.

**LD-PA-005 (note for the reviewers): unverified rates.** NAT, ALB, WAF, EBS gp3/snapshot, RDS storage, EFS and CloudWatch are marked as not verified in us-east-1. The page tables did not render and there was no widget iframe. Each is marked in the learner-facing text. Reviewers: if you can read any of these pages, confirm or correct the rate.
