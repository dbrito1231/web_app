# Lesson 4.2 — Senior AWS Solutions Architect review (Round 1)

Reviewed against:
- `content/lessons/lesson-4-2.json`
- `reports/fix-loop-r2/q1/lesson-4-2-impl.md` (claim table)
- `reports/fix-loop-r2/q1/RULES.md`

## Per-objective teach-before-test readiness

- SAA-4.2-K01: **Ready** — activation timing, tag activation requirement, and org discount sharing are taught with distinguishing detail.
- SAA-4.2-K02: **Ready** — Cost Explorer vs Budgets vs CUR roles are clearly separated by decision intent.
- SAA-4.2-K03: **Ready** — Region/AZ/Local Zone/Wavelength distinctions and multi-AZ reliability guidance are explicit.
- SAA-4.2-K04: **Ready** — On-Demand vs Spot vs RI vs Savings Plans contrasts include interruption and term/coverage details.
- SAA-4.2-K05: **Ready** — distributed/edge placement tradeoffs are clear enough for option elimination.
- SAA-4.2-K06: **Ready** — Outposts vs Local Zones vs Wavelength distinction is explicit and exam-usable.
- SAA-4.2-K07: **Not ready** — family/generation/options are taught, but virtualization distinction is missing (see AWS-L42-004).
- SAA-4.2-K08: **Ready** — Lambda/Fargate/EC2 utilization framing plus billing/time constraints are taught.
- SAA-4.2-K09: **Ready** — target tracking and hibernation vs scaling concepts are clearly separated.
- SAA-4.2-S01: **Ready** — ALB/NLB/GWLB selection by layer and routing/static-IP needs is clear.
- SAA-4.2-S02: **Ready** — horizontal vs vertical vs hibernation strategy selection is explicit.
- SAA-4.2-S03: **Ready** — Lambda vs Fargate vs EC2 mapping to execution model and cost profile is explicit.
- SAA-4.2-S04: **Ready** — production vs non-production availability tradeoffs are taught with decision framing.
- SAA-4.2-S05: **Ready** — family selection by bottleneck profile is explicit.
- SAA-4.2-S06: **Ready** — size-rightsizing method and family-step sizing examples are explicit.

## Issues

- **AWS-L42-001 (medium)**  
  **Location:** `SAA-4.2-K04`, claim table row 22, phrase `"Reserved Instances terms are one or three years"`  
  **Problem:** Row 22 quote in the table (`"payment options are available for Reserved Instances"`) is not the quoted evidence for term length.  
  **Doc-verified fix:** Replace row 22 quote with: `"You can purchase a Reserved Instance for a one-year or three-year commitment"` from `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html`.

- **AWS-L42-002 (medium)**  
  **Location:** `SAA-4.2-S03`, claim table row 53, phrase `"On-Demand allows per-second pay-as-you-go compute"`  
  **Problem:** Row 53 quote (`"pay-as-you-go pricing with no long-term commitments"`) does not contain the per-second granularity part of the claim.  
  **Doc-verified fix:** Replace row 53 quote with: `"pay only for the compute time you use, with billing granularity as low as per-second for Linux, RHEL, and Windows instances"` from `https://docs.aws.amazon.com/decision-guides/latest/decision-guides/ec2-purchasing-options-aws-how-to-choose.html`.

- **AWS-L42-003 (low)**  
  **Location:** lesson body root heading, phrase `"## Cost-optimized compute"`  
  **Problem:** RULES markdown subset for lessons allows `###`/`####` headings only; `##` is out of subset.  
  **Doc-verified fix:** Change the heading to `### Cost-optimized compute` (or remove it) to stay inside the allowed subset defined in `reports/fix-loop-r2/q1/RULES.md`.

- **AWS-L42-004 (medium)**  
  **Location:** `SAA-4.2-K07`, phrase `"Instance naming has family and size components"`  
  **Problem:** Objective text includes virtualization, but lesson does not teach the bare-metal (`.metal`) distinction needed to separate virtualized vs bare-metal options in questions.  
  **Doc-verified fix (add sentence):** `"After the period (\`.\`) is the instance size, such as \`small\` or \`4xlarge\`, or \`metal\` for bare metal instances."`  
  Source: `https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html`.

## Claim table verification results

Rows verified (37 total, including all number-bearing rows found): 1, 2, 6, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 29, 30, 31, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54.

- Row 1: verified (quote exact; claim accurate).
- Row 2: verified (quote exact; claim accurate: up to 24h + up to 24h).
- Row 6: verified (quote exact; claim accurate: 12-month history and 12-month forecast).
- Row 12: verified (quote exact; claim accurate: at least two AZs for production).
- Row 13: verified (quote exact; claim accurate: hourly + per-GB processed NAT charges).
- Row 14: verified (quote exact; claim accurate: same-AZ guidance for NAT-related transfer reduction).
- Row 15: verified (quote exact; claim accurate: one-second increments, 60-second minimum).
- Row 16: verified (quote exact; claim accurate: two-minute Spot notice).
- Row 18: verified (quote exact; claim accurate: 1-year/3-year Savings Plans term).
- Row 19: verified (quote exact; claim accurate: Compute Savings Plans up to 66%).
- Row 20: verified (quote exact; claim accurate: EC2 Instance Savings Plans up to 72%).
- Row 21: verified (quote exact; claim accurate: EC2 + Fargate + Lambda coverage).
- Row 22: **claim accurate but quote mismatch** (see AWS-L42-001).
- Row 23: verified (quote exact; claim accurate: All/Partial/No Upfront).
- Row 24: verified (quote exact; claim accurate: single-digit millisecond latency).
- Row 25: verified (quote exact; claim accurate: ultralow-latency 5G design target).
- Row 29: verified (quote exact; claim accurate: first position indicates series).
- Row 30: verified (quote exact; claim accurate: second position indicates generation).
- Row 31: verified (quote exact; claim accurate: third position indicates options).
- Row 35: verified (quote exact; claim accurate: per-second billing, 1-minute minimum).
- Row 36: verified (quote exact; claim accurate: Windows container 5-minute minimum).
- Row 37: verified (quote exact; claim accurate: Lambda priced by requests + duration).
- Row 38: verified (quote exact; claim accurate: default timeout 3 seconds).
- Row 39: verified (quote exact; claim accurate: maximum timeout 900 seconds/15 minutes).
- Row 40: verified (quote exact; claim accurate: target tracking adds/removes capacity near target).
- Row 41: verified (quote exact; claim accurate: above target scale out, below target scale in).
- Row 42: verified (quote exact; claim accurate: hibernation saves RAM to EBS root volume).
- Row 43: verified (quote exact; claim accurate: no instance usage charge while hibernated).
- Row 44: verified (quote exact; claim accurate: EBS storage charges continue).
- Row 45: verified (quote exact; claim accurate: ALB Layer 7, HTTP/HTTPS).
- Row 46: verified (quote exact; claim accurate: NLB Layer 4, TCP/TLS/UDP/QUIC).
- Row 47: verified (quote exact; claim accurate: GWLB Layer 3).
- Row 50: verified (quote exact; claim accurate: `c7g.large` is 2 vCPU, 4 GiB).
- Row 51: verified (quote exact; claim accurate: `c7g.xlarge` is 4 vCPU, 8 GiB).
- Row 52: verified (quote exact; claim accurate: `c7g.2xlarge` is 8 vCPU, 16 GiB).
- Row 53: **claim accurate but quote mismatch** (see AWS-L42-002).
- Row 54: verified (quote exact; claim accurate: Spot up to 90% discount).

## Additional lesson checks

- Objective coverage: all 15 objectives (K01-K09, S01-S06) have a dedicated section in order.
- Exam tips: each objective section ends with an `**Exam tip:**` and tips are generally useful and scenario-oriented.
- Retired/renamed/closed services: no banned services used as current advice; Snow Family is correctly labeled as closed to new customers.
- Technical accuracy: no direct factual contradiction found in lesson text for reviewed claims.

Lesson 4.2: not yet

Overall: concerns
