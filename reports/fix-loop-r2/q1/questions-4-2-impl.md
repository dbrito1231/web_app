# Questions 4.2 rewrite ? implementation report

## Accepted lesson/report fixes applied

- Updated claim-table row 22 quote to: "You can purchase a Reserved Instance for a one-year or three-year commitment".
- Updated claim-table row 53 quote to: "pay only for the compute time you use, with billing granularity as low as per-second for Linux, RHEL, and Windows instances".
- Added K01 sentence: management account can turn off RI and Savings Plans discount sharing for account-level isolation.
- Added K01 sentence: user-defined tag-key activation timing (up to 24 hours to appear, up to another 24 hours to activate).
- Added K07 sentence: size comes after the period and includes `metal` for bare metal instances.
- Added K08 sentence: Lambda timeout defaults to 3 seconds and is configurable from 1 to 900 seconds for standard functions.
- Added K09 plain-language definitions at first use: SLO (service quality target) and blast radius (size of affected scope during failure).
- Added claim-table rows for newly taught facts: `metal` size and Lambda 1-to-900 second configurability.

## Per-question key and one-line justification

- `q-saa-4-2-k01-mc` ? **a**: only option that satisfies both tag-based chargeback visibility and account-level discount isolation.
- `q-saa-4-2-k02-mc` ? **c**: Cost Explorer is the direct forecast-and-breakdown view by account and tag.
- `q-saa-4-2-k02-mr` ? **b,d**: Budgets provides alarming; CUR provides raw line-item export to S3.
- `q-saa-4-2-k03-mc` ? **b**: multi-AZ with load balancing addresses single-AZ failure requirement.
- `q-saa-4-2-k04-mc` ? **d**: commitments cover stable baseline while Spot fits interruptible batch.
- `q-saa-4-2-k05-mc` ? **a**: Wavelength is purpose-built for ultra-low-latency 5G edge use cases.
- `q-saa-4-2-k05-mr` ? **a,e**: Local Zone for latency-sensitive tier, parent Region for broad-service core tier.
- `q-saa-4-2-k06-mc` ? **c**: Outposts is the AWS-native on-prem hybrid model.
- `q-saa-4-2-k07-mc` ? **b**: `metal` is the bare-metal size needed for direct host access.
- `q-saa-4-2-k08-mc` ? **d**: Lambda best matches short event-driven burst workloads with idle gaps.
- `q-saa-4-2-k08-mr` ? **c,d**: Fargate removes host patching; independent microservice scaling reduces idle overprovision.
- `q-saa-4-2-k09-mc` ? **a**: hibernation preserves warm state while Auto Scaling handles daytime elasticity.
- `q-saa-4-2-s01-mc` ? **c**: ALB provides Layer 7 host/path routing with TLS termination.
- `q-saa-4-2-s01-mr` ? **b,e**: GWLB plus appliance target groups is the inline virtual appliance pattern.
- `q-saa-4-2-s02-mc` ? **b**: horizontal Auto Scaling fits stateless traffic variability.
- `q-saa-4-2-s02-mr` ? **a,c**: horizontal scaling addresses spikes; hibernated cache tier reduces warm-up delay.
- `q-saa-4-2-s03-mc` ? **d**: Lambda for short events and Fargate for long-running containers best matches execution shape.
- `q-saa-4-2-s03-mr` ? **a,d**: Lambda for short handlers, Fargate for >15-minute jobs with no host management.
- `q-saa-4-2-s04-mc` ? **a**: production gets multi-AZ resilience while QA is right-sized to lower criticality.
- `q-saa-4-2-s04-mr` ? **a,b**: aligns availability investment to business impact by environment class.
- `q-saa-4-2-s05-mc` ? **c**: compute-optimized family matches sustained CPU bottleneck profile.
- `q-saa-4-2-s05-mr` ? **c,e**: C family for CPU-bound tier and R family for memory-bound tier.
- `q-saa-4-2-s06-mc` ? **b**: next size step (`xlarge`) is smallest practical uplift after `large` saturation.
- `q-saa-4-2-s06-mr` ? **b,d**: downsize with verified headroom while retaining Auto Scaling for peak protection.

## Distractor type table

Pre-check note (Lead Dev, before round-2 review): I removed recycled Outposts wording, replaced off-area Outposts/Local Zones distractors in `s03-mr`, `s04-mc`, and `s06-mr`, and replaced the likely strawman in `s06-mr`.

Counting method: counted **distractor choices only** (not correct answers). Each distractor is assigned one primary wrong-answer concept, then grouped across all 24 questions.

| Distractor type | Count | Question IDs |
|---|---:|---|
| Cost visibility vs control tool confusion | 3 | k01-mc, k02-mc, k02-mr |
| Availability topology underfit | 3 | k03-mc, s04-mc, s04-mr |
| Purchase model misuse | 3 | k04-mc, k09-mc, s06-mr |
| Edge and hybrid placement misalignment | 3 | k05-mc, k05-mr, k06-mc |
| Instance taxonomy and family mismatch | 3 | k07-mc, s05-mc, s05-mr |
| Serverless and container execution-shape mismatch | 3 | k08-mc, k08-mr, s03-mr |
| Load balancer layer and appliance mismatch | 2 | s01-mc, s01-mr |
| Scaling method mismatch | 2 | s02-mc, s02-mr |
| Mixed compute service mapping and sizing mismatch | 2 | s03-mc, s06-mc |

- Highest distractor-type count: **3** (15% cap = 3 for 24 questions).
- Placement-subtype check: Outposts distractors = **3** (`k03-mc`, `k05-mc`, `k05-mr`), Local Zone distractors = **3** (`k03-mc`, `k05-mc`, `k06-mc`).

## Balance stats

- Longest-is-key (MC): **4/15 = 27%**.
- MC key distribution: **a=4, b=4, c=4, d=3**.
- MR key-slot distribution: **a=4, b=4, c=3, d=4, e=3**.

## Validation

- `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 4-2` -> **RESULT: PASS**.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` -> **PASS**.

## Round-2 fixes (post-review)

- **AWS-Q42-001 (`s03-mr`)**: tightened the stem to require the lowest-cost fit for bursty short handlers while still avoiding server management; kept key `a,d`.
- **TEACHER-Q42-001 (`s01-mc`)**: chose the "teach it" remedy; kept Classic Load Balancer distractor and added a lesson S01 sentence that CLB is previous-generation and not recommended for new environments.
- **TEACHER-Q42-002 (`s01-mr`)**: chose the "replace distractor" remedy; replaced Global Accelerator with `Classic Load Balancer for inline firewall traffic` to avoid near-duplicate ALB/NLB choices and keep a distinct, taught wrong reason.
- **TEACHER-Q42-003 (`s04-mr`)**: replaced `Store the checkout database on instance store volumes only` with `Run checkout in one Availability Zone with larger instances`, which fails the explicitly taught production multi-AZ requirement.
