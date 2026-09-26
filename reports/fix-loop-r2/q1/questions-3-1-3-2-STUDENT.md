# Q1 Fairness Review: Tasks 3-1 and 3-2

## Task 3-1: High-performing storage (7 questions)

| Q ID | My Answer | Reason | Right? | Fair? | Notes |
|------|-----------|--------|--------|-------|-------|
| Q1 (K01) | a, c | DataSync for online bulk transfer; S3 File Gateway for local SMB + S3 backing | ✓ | Yes | Snowball Edge inclusion tests awareness of retirement; distractors address both requirements separately |
| Q2 (K02) | c | FSx Lustre with data repository association: terabytes/sec throughput, thousands of instances, S3-linked objects | ✓ | Yes | Technical requirement (data repository association) not found in distractors; clear learning value in each explanation |
| Q3 (K03) | a | io2 Block Express: 256K IOPS, sub-millisecond latency, 99.999% durability for mission-critical DB | ✓ | Yes | Lesson has explicit exam tip matching this scenario; distractors show IOPS ceiling differences clearly |
| Q4 (S01) | d | S3 Transfer Acceleration: routes through CloudFront edge + AWS backbone, cuts distance-driven latency | ✓ | Yes | All distractors are valid S3 techniques but for different problems (throughput, request rate); distinction is clear |
| Q5 (S01) | b, d | EFS Max I/O + Elastic for many parallel small ops; st1 HDD for sequential streaming throughput | ✓ | Yes | Perfect split: one file service for parallel, one block service for sequential; each distractor tests understanding of EFS modes or HDD tiers |
| Q6 (S02) | b | S3: unlimited capacity, no provisioning, no resize operations needed | ✓ | Yes | All options involve some form of scaling/provisioning except S3; EFS and EBS would still require management |
| Q7 (S02) | c, e | EBS Elastic Volumes for live resize; DataSync scales via parallel tasks/agents (not physical devices) | ✓ | Yes | Tests understanding of scalability mechanisms; instance store and single-prefix distractors teach capacity limits |

**Fairness: 7/7 = 100%** ✓

All questions are answerable from the lesson alone, each has one defensible answer set, no wording giveaways, and distractors teach why they don't fit. Explanations consistently map back to lesson content with specific caps/numbers.

**Anything confusing:** No. Lesson structure (K01–K03, S01–S02 codes) matches question tags. Exam tips directly address question scenarios. Progression from storage gateway/FSx (K01–K02) to performance tuning (S01) to growth planning (S02) is logical.

**Task 3-1: close** ✓

---

## Task 3-2: High-performing compute (8 questions)

| Q ID | My Answer | Reason | Right? | Fair? | Notes |
|------|-----------|--------|--------|-------|-------|
| Q1 (K02) | a, c | Outposts for on-premises facility (data-residency); Local Zones for AWS-operated metro locations | ✓ | Yes | Wavelength (5G telecom network) and placement groups are clear distractors; Compute Optimizer has zero relevance |
| Q2 (K03) | c | ApproximateNumberOfMessagesVisible metric tracks queue backlog, not CPU or fixed schedule | ✓ | Yes | CPU, scheduled, and network metrics all serve real purposes but not for this scenario; queue-depth lesson is explicit |
| Q3 (K05) | b, d | Provisioned concurrency pre-initializes; SnapStart snapshots for cold-start elimination on first invoke | ✓ | Yes | Timeout, memory, and Optimizer all improve performance but don't eliminate Init-phase cold start; distinction is clear |
| Q4 (K06) | b | Application Auto Scaling on ECS service; Fargate removes need for EC2 capacity management entirely | ✓ | Yes | All three distractors mistakenly add EC2 layer (Capacity Providers, mixed instances, Cluster Autoscaler); lesson explicitly covers this |
| Q5 (S01) | c | SQS queue decouples tiers; fulfillment fleet scales on queue depth independently of web tier spikes | ✓ | Yes | All distractors assume shared scaling or direct connection; decoupling and SQS queue pattern is explicit in lesson |
| Q6 (S02) | c, e | ApproximateNumberOfMessagesVisible for backlog-driven scaling; Compute Optimizer validates instance type sizing | ✓ | Yes | Question tests two separate concerns (metric + rightsizing); lesson section S02 explicitly distinguishes them |
| Q7 (S03) | d | Cluster placement group (lowest latency in one AZ) + EFA (OS-bypass MPI collective communication) | ✓ | Yes | Partition (rack isolation), spread (hardware isolation), and Graviton (processor type) each serve different purposes; lesson contrasts clearly |
| Q8 (S03) | a, c | Spread for isolated critical instances; partition for HDFS with rack-failure blast-radius containment | ✓ | Yes | Cluster and EFA are distractors from different placement concerns; single-partition Graviton tests understanding that partitions need distribution |

**Fairness: 8/8 = 100%** ✓

All questions are answerable from the lesson alone, each has one defensible answer set, no wording giveaways, and distractors test specific lesson distinctions. Explanations walk through why each option does or does not match the scenario.

**Anything confusing:** No. Lesson structure (K01–K06, S01–S04) matches question tags. Exam tips directly address the core scenarios. Progression from services (K01–K02) to scaling mechanics (K03–K06) to optimization (S01–S04) is logical and builds on earlier lessons.

**Task 3-2: close** ✓

---

## Summary

**Overall: approve**

Both tasks (3-1 and 3-2) achieved 100% fairness (15/15 questions). All questions are answerable from the lesson without guessing, each has a single defensible answer, distractors are reasonable and teach why they don't fit, and explanations reinforce lesson content with specifics (numbers, feature names, exam tips). No wording giveaways, no unfair length/complexity biases, and no unanswerable ambiguity. Ready to close both.
