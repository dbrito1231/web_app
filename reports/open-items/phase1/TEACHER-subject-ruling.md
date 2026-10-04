# Teacher ruling — subject terms for the distractor audit (Phase 1, plan P2, 2026-10-04)

Saved by the Lead Dev (condensed). A term counts as SUBJECT only when a bullet in that same task names it or the service it stands for. SUBJECT terms are held to a 40% cap; REUSE terms stay at 15%.

| Task | SUBJECT (bullet) | REUSE (reason) |
|---|---|---|
| 1-2 | NAT Gateway (1.2-S01 "...route tables, network ACLs, NAT gateways") | — |
| 2-1 | Lambda (2.1-K12 "...AWS Fargate, AWS Lambda"; S05) | — |
| 2-2 | Multi-AZ (2.2-S02 "...across ... Availability Zones"; S04, K06). This is the weakest call: Multi-AZ is a feature, not a service | RDS 6/32 (only "RDS Proxy" is named, in K09); Auto Scaling (a 3.2-K04 term); read replica (2.1-K15, 3.3); Aurora (3.3-S04) |
| 3-1 | Storage Gateway (3.1-K01 "Hybrid storage solutions"); EFS (3.1-K02) | FSx 3/8 (not in 3.1-K02, which lists S3, EFS and EBS) |
| 3-2 | Lambda (3.2-K05); Auto Scaling (3.2-K04) | Compute Optimizer (in no 3.2 bullet) |
| 3-3 | RDS (3.3-S03 "MySQL compared with PostgreSQL"; K06), **still over 40% (9/21)**; read replica (K07); ElastiCache (K02); DynamoDB and Aurora (S04) | Redshift 4/21 (a data warehouse, which belongs to 3.5; not covered by K08) |
| 3-4 | Application Load Balancer (K03); Direct Connect (K04); CloudFront (K01); Gateway Load Balancer (S04, borderline) | NAT Gateway 3/13 (a 1.2-S01 and 4.4 subject) |
| 3-5 | Glue (K04), **still over 40% (11/24)**; EMR (S05); Athena (K01) | — |
| 4-1 | EBS, FSx, EFS (4.1-K04); S3 Glacier (K10, S06) | — |

**Minimum-N:** agreed, with a condition. Below 10 questions an over-cap task reports `WARN (small N)` and still prints every term. The 3-1 FSx repeat (3/8, REUSE) is probably real; the Teacher proposes a CR to add questions to 3-1.

**Predicted result after the change:** 1-2, 2-1 and 4-1 go to PASS. 2-2, 3-2, 3-3, 3-4 and 3-5 stay FAIL on real reuse or over-use; 3-1 becomes WARN. The actual run matched this exactly (`audit-after.txt`).

## Post-check (Teacher, after implementation): close
- The SUBJECT map matches the ruling exactly, and no REUSE term was exempted.
- The exam split removed no flagged term. The only term that disappeared is `validation` in 4-3, a Terraform-only term that was matching "SQL dialect validation" (by design).
- Terraform tasks are unchanged, and a rerun matches `audit-after.txt` exactly.
- The remaining FAILs and the WARN are real reuse or over-use, logged as CR-0024.
