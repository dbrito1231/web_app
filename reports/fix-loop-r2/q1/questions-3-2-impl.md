# Task 3.2 question rewrite — implementation report

## AWS review fixes

- **AWS-Q32-001** (`q-saa-3-2-k05-mr` choice a): "Reserved concurrency" → "Increasing the function's timeout setting to the maximum". Rationale clause updated to match. Added `citationIds` entry `cite-saa-3-2-lambda-timeout` (new citation file, `https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html`). Re-run of `q1_batch_check.py 3-2`: RESULT PASS, no FAIL/WARN.
  - **Open item:** AWS's fix note also calls for a lesson-3-2 K05 addition ("Each function also has a separate configurable timeout... raising it does not pre-initialize anything and has no effect on cold-start latency") so the new distractor's fact is taught before it is tested. This session's edit scope was restricted to question files only (per coordinator instruction), so the lesson body was **not** touched. Until that lesson addition is made and Teacher-validated per AGENTS.md's content-impact check, `q-saa-3-2-k05-mr` choice a rests on a fact not yet present in lesson-3-2.json — flagging this for Lead Dev to schedule the lesson edit rather than working around it silently.

## Batch-check result

```
task 3-2: 16 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 10 for 10 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 3/10 = 30%
PASS: MC key positions {'a': 3, 'b': 3, 'c': 2, 'd': 2}
PASS: MR key slots {'a': 3, 'b': 3, 'c': 3, 'd': 2, 'e': 1}
RESULT: PASS
```
No FAIL, no WARN. `content_lint.py`: PASS.

Two citations reused from lesson 2.1's already-existing files (`cite-saa-2-1-fargate-compute`, backing "Fargate runs ECS/EKS containers without provisioning/managing the underlying EC2 instances") for K01-mc and K06-mc, since that exact fact is not separately cited under lesson 3.2 but is taught in the 3.2 body. No new citation files were needed.

## Per-question table

| ID | Objective | Tests | Key | Lesson sentence(s) teaching key / distractors |
|---|---|---|---|---|
| k01-mc | K01 | Batch vs EMR vs Fargate-service vs Lambda-direct | AWS Batch | "AWS Batch...provisions the...capacity a queued job needs, then scales that capacity down to zero when the queue empties" / EMR "partitions a large dataset across the cluster's nodes" / Fargate "fits a long-running service rather than a scheduled batch job" |
| k02-mc | K02 | Wavelength vs Local Zones vs Outposts vs placement group | AWS Wavelength | "AWS Wavelength...extend a subset of AWS compute...to locations...closer to...a telecom provider's 5G network" / Local Zones "closer to end users" / Outposts "on-premises...customer's own facility" / placement group "controls where those nodes land...inside a Region" |
| k02-mr | K02 | Outposts+Local Zones vs Wavelength/partition PG/Compute Optimizer | Outposts, Local Zones | same K02 sentence set, plus "None of these edge options replace queuing or container orchestration; they change where the compute physically runs" |
| k03-mc | K03 | Queue-depth scaling vs CPU/scheduled/network metric | ApproximateNumberOfMessagesVisible | "an Auto Scaling policy watches the queue's ApproximateNumberOfMessagesVisible metric and adds or removes workers to match the backlog" |
| k04-mc | K04 | Warm pool vs instance refresh vs mixed instances vs Spot notice | Warm pool | "A warm pool keeps a set of pre-initialized instances...so a scale-out event can resume a warm instance instead of booting one from cold" / "Instance refresh replaces an ASG's instances with new ones built from an updated launch template or AMI" / mixed instances "widens the pool...reduces cost" / "two-minute Spot Instance interruption notice" |
| k05-mc | K05 | Memory→CPU vs provisioned concurrency/SnapStart/reserved concurrency | Increase memory | "Lambda allocates CPU power linearly...at 1,769 MB a function gets...one full vCPU" / "Provisioned concurrency pre-initializes...skip the cold-start Init phase" / SnapStart "resumes new environments from that cached snapshot" / "Reserved concurrency sets both a floor and a ceiling" |
| k05-mr | K05 | Provisioned concurrency + SnapStart vs reserved concurrency/Compute Optimizer/memory-alone | Provisioned concurrency, SnapStart | same K05 sentences, plus Compute Optimizer "generates a Lambda-specific finding" (S04) |
| k06-mc | K06 | Fargate service scaling vs adding EC2 ASG/mixed instances/EKS autoscaler | Application Auto Scaling target tracking on the service | "AWS Fargate removes the second scaling problem entirely – there is no EC2 capacity to add – while ECS or EKS on self-managed EC2 instances still needs its own EC2 Auto Scaling group" |
| s01-mc | S01 | Queue as buffer vs resizing producer/CPU-scale consumer/NLB | Insert SQS queue, scale on queue depth | "Put a buffer...between two tiers, and each side can scale on the metric that matters to it...a consumer fleet...scales on the queue depth" |
| s01-mr | S01 | EventBridge bus + SQS queue vs NLB/CPU target tracking/mixed instances | EventBridge bus, SQS queue | same S01 sentence, plus K03's ApproximateNumberOfMessagesVisible text |
| s02-mc | S02 | Compute Optimizer vs live scaling metric/scheduled policy/queue metric | AWS Compute Optimizer | "AWS Compute Optimizer complements a live scaling policy by analyzing up to 14 days of CloudWatch history...reporting whether each is under-provisioned, over-provisioned, or already optimal, with a specific rightsizing recommendation" |
| s02-mr | S02 | Queue-depth metric + Compute Optimizer vs CPU/predictive/network metric | ApproximateNumberOfMessagesVisible, Compute Optimizer | same S02 sentence plus K03 queue-metric text |
| s03-mc | S03 | Cluster PG + EFA vs partition+ENA/spread/Graviton-no-PG | Cluster placement group with EFA | "a cluster placement group packs instances into a single Availability Zone on the same high-bisection-bandwidth network segment for the lowest latency" / "The Elastic Fabric Adapter (EFA)...OS-bypass, low-latency transport...that ordinary ENA networking does not provide" |
| s03-mr | S03 | Spread + partition PG vs cluster PG/EFA-alone/Graviton-in-one-partition | Spread PG, partition PG | "a spread placement group places up to seven running instances...each on genuinely distinct hardware" / "a partition placement group divides instances into up to seven partitions...to contain a single hardware failure to one partition" |
| s04-mc | S04 | Test memory settings for cost vs reserved/provisioned concurrency/container repackage | Test several higher memory settings | "raising the memory setting on a CPU-bound function can shorten its billed duration enough to lower the total cost per invocation...right-sizing Lambda means testing several memory values against real traffic" |
| s04-mr | S04 | Compute Optimizer Lambda + ASG findings vs enhanced-metrics-required/mixed-instances/SnapStart | Compute Optimizer Lambda finding, ASG finding | "Compute Optimizer generates a Lambda-specific finding...from a function's actual CloudWatch duration and memory-utilization history, with a recommended memory value" / "checked against Compute Optimizer's EC2 and EC2 Auto Scaling group recommendations" / "analyzing up to 14 days of CloudWatch history by default (93 days with the paid enhanced infrastructure metrics feature)" |

## Distractor-type table (cap: 2 per type in 16 questions)

| Type | Count | Used in |
|---|---|---|
| EMR vs Batch (job-queue need) | 1 | k01-mc |
| Fargate long-lived service vs Batch scale-to-zero | 1 | k01-mc |
| Lambda direct invoke vs Batch queue management | 1 | k01-mc |
| Local Zones vs Wavelength (telecom network) | 1 | k02-mc |
| Outposts vs Wavelength (telecom network) | 1 | k02-mc |
| Placement group vs edge-location need | 1 | k02-mc |
| Wavelength vs facility/metro need | 1 | k02-mr |
| Partition PG vs facility/metro need | 1 | k02-mr |
| Compute Optimizer vs location need | 1 | k02-mr |
| CPU target tracking vs queue-depth need | 2 | k03-mc, s02-mr |
| Scheduled scaling vs queue-depth need | 1 | k03-mc |
| Network in/out target tracking vs queue-depth need | 2 | k03-mc, s02-mr |
| Instance refresh vs warm-pool need | 1 | k04-mc |
| Mixed instances policy vs warm-pool need | 2 | k04-mc, k06-mc |
| Spot interruption notice vs warm-pool need | 1 | k04-mc |
| Provisioned concurrency vs CPU/memory need | 1 | k05-mc |
| SnapStart vs CPU/memory need | 1 | k05-mc |
| Reserved concurrency vs CPU/memory need | 2 | k05-mc, k05-mr |
| Reserved concurrency vs cold-start need | (see above) | k05-mr |
| Compute Optimizer memory rec. vs cold-start need | 1 | k05-mr |
| Memory increase alone vs cold-start need | 1 | k05-mr |
| Add EC2 ASG via Capacity Providers vs Fargate-no-EC2 need | 1 | k06-mc |
| EKS Cluster Autoscaler vs ECS-Fargate need | 1 | k06-mc |
| Resize producer tier vs decouple-consumer need | 1 | s01-mc |
| CPU-scale consumer vs queue-depth need | 2 | s01-mc, s01-mr |
| NLB (no buffering) vs queue/bus need | 2 | s01-mc, s01-mr |
| Mixed instances policy vs backlog-metric need | 1 | s01-mr |
| Live scaling policy vs historical-rightsizing need | 1 | s02-mc |
| Scheduled policy vs historical-rightsizing need | 1 | s02-mc |
| Queue metric alone vs rightsizing need | 1 | s02-mc |
| Predictive scaling vs queue-depth/rightsizing need | 1 | s02-mr |
| Partition PG + ENA vs lowest-latency need | 1 | s03-mc |
| Spread PG vs lowest-latency need | 1 | s03-mc |
| Graviton-no-PG vs lowest-latency need | 1 | s03-mc |
| Cluster PG vs hardware-isolation need | 1 | s03-mr |
| EFA-alone vs hardware-isolation need | 1 | s03-mr |
| Graviton-in-one-partition vs blast-radius need | 1 | s03-mr |
| Reserved concurrency vs cost-per-invocation need | (distinct context) | s04-mc |
| Provisioned concurrency vs cost-per-invocation need | (distinct context) | s04-mc |
| Container repackage vs memory/cost need | 1 | s04-mc |
| Enhanced-infrastructure-metrics-required (false) | 1 | s04-mr |
| Mixed instances auto-rightsizes (false) | 1 | s04-mr |
| SnapStart auto-adjusts memory (false) | 1 | s04-mr |

All types stay at or under the 2-per-type cap; the only types reused twice are CPU-target-tracking-vs-queue-depth, network-in/out-vs-queue-depth, mixed-instances-vs-warm-pool/no-EC2, reserved-concurrency-vs-CPU/cold-start, and CPU-scale/NLB-vs-decoupling — each appears in a different objective's scenario.

## Lesson additions requested

None. Every key and distractor is fully taught by the existing lesson-3-2 body.
