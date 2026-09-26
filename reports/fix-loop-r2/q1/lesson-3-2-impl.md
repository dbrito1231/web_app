# Lesson 3.2 rewrite — implementation notes

## Section outline (one `###` per objective, in id order)

1. K01 — AWS compute services with appropriate use cases: AWS Batch (job queues + compute environments, scales to zero), Amazon EMR (distributed Hadoop/Spark cluster), AWS Fargate (refers back to Lesson 2.1 K12).
2. K02 — Distributed computing concepts supported by AWS global infrastructure and edge services: distributed frameworks need short network hops (placement groups, S03); edge services (AWS Local Zones, AWS Wavelength, AWS Outposts) bring compute physically closer to data sources/users.
3. K03 — Queuing and messaging concepts: refers back to Lesson 2.1 K11 for SQS/SNS/EventBridge fundamentals; here ties queue depth (`ApproximateNumberOfMessagesVisible`) to scaling a worker/batch fleet independently of the producer.
4. K04 — Scalability capabilities: EC2 Auto Scaling vs. the unified AWS Auto Scaling service; ASG mechanics — warm pools (Stopped/Running/Hibernated pre-init instances), instance refresh (rolling AMI/launch-template replacement with min healthy % and auto rollback), mixed instances policies (multiple instance types + On-Demand/Spot mix).
5. K05 — Serverless technologies and patterns: Lambda memory (128 MB–10,240 MB, 1 MB increments) linearly drives CPU (1 vCPU at 1,769 MB, up to 6 vCPUs at max); reserved concurrency (fixed floor+ceiling carved from account pool) vs. provisioned concurrency (pre-initialized environments, low latency); SnapStart (Firecracker snapshot resume, Java 11+/Python 3.12+/.NET 8+, sub-second cold starts, AWS recommends provisioned concurrency for stricter SLAs than SnapStart covers).
6. K06 — Container orchestration: refers back to Lesson 2.1 K14 (ECS vs EKS); focuses on Service Auto Scaling (task/pod count) as distinct from EC2 capacity scaling underneath, and how Fargate removes the latter entirely.
7. S01 — Decoupling workloads to scale independently: buffer (queue/topic/bus/load balancer) lets each tier scale on its own metric instead of upstream traffic.
8. S02 — Identifying metrics and conditions to scale: CloudWatch metrics matched to the actual bottleneck (CPU, network, custom app metric, SQS queue depth); AWS Compute Optimizer (14-day default lookback, 93-day with paid enhanced infrastructure metrics) for EC2/ASG/Lambda/EBS/ECS-on-Fargate rightsizing findings.
9. S03 — Selecting compute options/features: EC2 instance type naming convention (series/generation/options/size), AWS Graviton (Arm-based, ~20% lower cost / 20%+ performance vs. comparable Intel), placement groups (cluster = single AZ high-bisection-bandwidth; partition = max 7 partitions/AZ; spread = max 7 running instances/AZ, distinct hardware), Enhanced Networking/ENA vs. Elastic Fabric Adapter (EFA, OS-bypass low-latency transport for HPC/MPI).
10. S04 — Selecting resource type/size: Lambda memory right-sizing tied back to K05 (more memory can lower total cost by cutting duration); Compute Optimizer's Lambda- and EC2-specific findings as the check rather than guessing.

Ends with the standard Warnings block (root user, teardown, budget alerts) and a citation-list pointer, matching the Lesson 2.1/2.2 format.

## Concepts per current question (all placeholders, now backed by the rewritten body)

- q-saa-3-2-k01-mc → AWS Batch/EMR/Fargate use cases (K01 section)
- q-saa-3-2-k02-mc/mr → distributed computing + edge services (K02 section)
- q-saa-3-2-k03-mc → queuing/messaging for elastic compute (K03 section)
- q-saa-3-2-k04-mc → EC2 Auto Scaling / AWS Auto Scaling, warm pools, instance refresh, mixed instances (K04 section)
- q-saa-3-2-k05-mc/mr → Lambda memory/CPU coupling, concurrency, SnapStart (K05 section)
- q-saa-3-2-k06-mc → ECS/EKS scaling mechanics (K06 section)
- q-saa-3-2-s01-mc/mr → decoupling for independent scaling (S01 section)
- q-saa-3-2-s02-mc/mr → scaling metrics + Compute Optimizer (S02 section)
- q-saa-3-2-s03-mc/mr → instance families/Graviton/placement groups/ENA/EFA (S03 section)
- q-saa-3-2-s04-mc/mr → Lambda/EC2 right-sizing (S04 section)

Only `bodyMarkdown`, `citationIds`, and `drillIds` were touched in `content/lessons/lesson-3-2.json`; no question file was edited (all 16 remain placeholders for the question-writer pass), and no other lesson file was touched.

## Doc URLs used (all `accessed: "2026-09-26"`, verified via the AWS Documentation MCP)

- https://docs.aws.amazon.com/batch/latest/userguide/batch_components.html
- https://docs.aws.amazon.com/prescriptive-guidance/latest/amazon-emr-hardware/introduction.html
- https://docs.aws.amazon.com/wavelength/latest/developerguide/what-is-wavelength.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html (Local Zones)
- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html
- https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-warm-pool.html
- https://docs.aws.amazon.com/autoscaling/ec2/userguide/start-instance-refresh.html
- https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-mixed-instances-group-manual-instance-type-selection.html
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html
- https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
- https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html
- https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-strategies.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html (Graviton ~20%/20% claim)
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking-ena.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html (2-minute Spot interruption notice)

## Retired or closed services encountered

None of the objective's named services (AWS Batch, Amazon EMR, AWS Fargate, EC2 Auto Scaling/AWS Auto Scaling, AWS Lambda, ECS/EKS) are retired or closed to new customers. No mention of AWS Copilot CLI or Snow Family was needed for this task, so no retirement callout was required in the lesson body. AWS Graviton, SnapStart, warm pools, instance refresh, and mixed instances policies are all current, actively documented features as of the 2026-09-26 doc checks above.

## Verification performed

- Word count: 2,442 (target 2,200–2,800).
- 0 stray single-asterisk spans; no tables, numbered lists, or markdown links in `bodyMarkdown`.
- All 18 `citationIds` resolve to files in `content/citations/`; all 16 `drillIds` resolve to files in `content/questions/`.
- `python scripts\content_lint.py` → PASS (429 questions, 23 lessons, 21+21 labs).
- Deleted `content/citations/cite-3-2.json` after confirming (via grep) it was referenced only by the old `lesson-3-2.json` body being replaced.

## Fixes (AWS-L32-001..003, TEACHER-L32-001), applied by Lead Dev

- **AWS-L32-001:** `cite-saa-3-2-graviton` now points to `prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html`, which states the 20%/20% figure; the title and note were updated. The lesson sentence is unchanged.
- **AWS-L32-002 / TEACHER-L32-001:** this sentence was added to K04 after the mixed instances policy sentence, using the reviewer's doc-verified wording: "Because Spot capacity can be reclaimed, Amazon EC2 sends a **two-minute Spot Instance interruption notice** as an EventBridge event and an instance metadata item before interrupting a Spot Instance, and it can send an earlier **rebalance recommendation** when a Spot Instance is at elevated risk of interruption; an Auto Scaling group or fleet can use either signal to drain work and launch a replacement before the hard interruption."
  - The new citation `cite-saa-3-2-spot-rebalance` backs the rebalance recommendation part.
  - The `cite-saa-3-2-spot-interruption` note is re-scoped to K04.
- **AWS-L32-003 (optional):** the S02 Compute Optimizer list now adds "(it also covers several database, cache, and other resource types beyond compute)".
