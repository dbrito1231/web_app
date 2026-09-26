# Lesson 3.2 — AWS Solutions Architect review

Reviewed: `content/lessons/lesson-3-2.json` (commit `89081d4`, "rewritten for compute
performance/elasticity, 18 doc citations, all 16 drillIds"). Author notes:
`reports/fix-loop-r2/q1/lesson-3-2-impl.md`. Objectives: `SAA-3.2-K01..K06`, `SAA-3.2-S01..S04` in
`content/objectives/saa_c03.json`. Standard used: `reports/fix-loop-r2/q1/lesson-3-1-AWS.md`.
Method: AWS Documentation MCP (`search_documentation` / `read_documentation`) against
docs.aws.amazon.com, all fetches dated 2026-09-26 (today). No AWS calls, no edits made outside
this report.

## 1. Per-section verdict

| Section | Verdict | Notes |
|---|---|---|
| K01 — AWS compute services (Batch, EMR, Fargate) | Accurate | AWS Batch job-queue/compute-environment mechanics, scale-to-zero, and its three compute-environment types (EC2 including Spot, `ECS_MANAGED_INSTANCES`, Fargate) all confirmed against `batch_components.html` and the current Batch compute-environment-type docs — "Amazon ECS Managed Instances" is a real, current Batch compute environment type, not a fabricated name. EMR's distributed Hadoop/Spark/Hive/Presto description and Spot-eligible, stateless task nodes match `amazon-emr-hardware/introduction.html`. Fargate's no-EC2-management framing is consistent with Lesson 2.1. |
| K02 — Distributed computing + edge services | Accurate | Local Zones and Wavelength descriptions (metro-area extension vs. telecom 5G network extension) match their respective "what is" pages; Outposts framed correctly as on-premises. Placement-group forward-reference to S03 is consistent. |
| K03 — Queuing and messaging for elastic compute | Accurate | `ApproximateNumberOfMessagesVisible` is a real, current SQS CloudWatch metric name, and the queue-as-buffer framing matches the SQS CloudWatch metrics page. Correctly scoped as a callback to Lesson 2.1 K11 rather than re-teaching SQS/SNS/EventBridge basics. |
| K04 — Scalability capabilities (ASG mechanics) | Accurate | Warm pool states (`Stopped`/`Running`/`Hibernated`, default `Stopped`) confirmed verbatim against `ec2-auto-scaling-warm-pools.html`/`warm-pool-instance-lifecycle.html`. The warm-pool-instances-tried-before-cold-launch mechanic is confirmed verbatim against `create-warm-pool.html`'s "Instance type selection with mixed instance groups" section. Instance refresh's minimum-healthy-percentage-with-auto-rollback mechanic matches `instance-refresh-overview.html`. Mixed instances policy (multiple instance types, On-Demand+Spot) matches `create-mixed-instances-group-manual-instance-type-selection.html`. "AWS Auto Scaling" as the unified, cross-resource (EC2 ASG, ECS, DynamoDB, Aurora) target-tracking service is a real, current, separate offering from EC2 Auto Scaling — confirmed via the AWS Auto Scaling Plans docs' supported-resources list. |
| K05 — Serverless (Lambda memory/CPU, concurrency, SnapStart) | Accurate | Lambda memory range (128 MB–10,240 MB, 1 MB increments) and the 1,769 MB = 1 vCPU breakpoint match `configuration-memory.html` verbatim. The "up to six vCPUs at 10,240 MB" ceiling is confirmed (AWS's own indexed description: "full vCPU at 1.8 GB and up to 6 vCPUs at 10,240 MB"). Reserved concurrency (fixed floor+ceiling from the shared pool) vs. provisioned concurrency (pre-initialized environments) matches `lambda-concurrency.html`. SnapStart's Firecracker-snapshot mechanism, sub-second cold starts, and the exact supported-runtime cutoffs (Java 11+, Python 3.12+, .NET 8+) match `snapstart.html` verbatim, as does "use provisioned concurrency if your application has strict cold start latency requirements that can't be adequately addressed by SnapStart." |
| K06 — Container orchestration scaling | Accurate | Service Auto Scaling (task/pod count) as distinct from underlying EC2 capacity scaling, and Fargate's removal of the second problem, is consistent with Lesson 2.1 K14 and with how ECS Capacity Providers / EKS Cluster Autoscaler are documented to work. No contradiction found. |
| S01 — Decoupling for independent scaling | Accurate | Buffer-based decoupling (queue/topic/bus/load balancer) letting each tier scale on its own metric is a correct, generically stated architecture pattern; consistent with K03's SQS-metric framing. |
| S02 — Scaling metrics + Compute Optimizer | Accurate | CloudWatch metric selection (CPU, network, custom app metric, `ApproximateNumberOfMessagesVisible`) is correctly matched to bottleneck type. Compute Optimizer's 14-day default lookback and 93-day enhanced-infrastructure-metrics (paid) lookback are both confirmed verbatim against `what-is-compute-optimizer.html`. Its supported-resource list for this lesson's claim (EC2 instances, EC2 ASGs, Lambda functions, EBS volumes, ECS services on Fargate) matches the current docs' "Supported resources" list exactly (the current page adds several more resource types not claimed here — Aurora/RDS, NAT Gateway, DynamoDB, ElastiCache, MemoryDB, DocumentDB, WorkSpaces, SageMaker, commercial licenses — but the lesson's list is a correct subset, not an overreach). |
| S03 — Compute options and features (naming, Graviton, placement groups, ENA/EFA) | Accurate, one citation-source defect | Instance-type-name decoding (series/generation/options/size, with `a`=AMD, `g`=Graviton, `n`=network/EBS-optimized, `d`=instance store) matches `instance-type-names.html` verbatim, including the lesson's example series letters (M/C/R,X/I,D/G,P). Placement group limits are both confirmed verbatim against `placement-strategies.html`: partition = maximum 7 partitions per Availability Zone; spread = maximum 7 running instances per Availability Zone per group (with the doc's own worked example of 21 instances across 3 AZs). Cluster placement group's "single AZ, same high-bisection-bandwidth network segment" description matches the doc's own wording. ENA (per-flow bandwidth/PPS for a cluster placement group) and EFA (OS-bypass, low-latency inter-node transport beyond ENA, paired with cluster/partition groups for HPC/MPI) both match `enhanced-networking-ena.html` and `efa.html`. The Graviton price-performance claim ("around 20% lower cost and 20% or greater performance") is itself accurate AWS language — see AWS-L32-001 below for the citation-source problem. |
| S04 — Resource type/size (Lambda and EC2 right-sizing) | Accurate | Compute Optimizer's Lambda-specific under/over-provisioned/optimized findings and its memory recommendation are consistent with the S02 citation and with `configuration-memory.html`'s own guidance to monitor CloudWatch duration/memory and consider AWS Lambda Power Tuning. The more-memory-can-lower-total-cost-by-cutting-duration point is directly supported by Lambda's memory-proportional-CPU model confirmed in K05. |

## 2. Verifying the Graviton and Spot-interruption facts named in the review brief

- **Graviton price-performance claim (S03).** The lesson states Graviton delivers "around 20% lower
  cost and 20% or greater performance improvement... over comparable current-generation Intel-based
  instances." This exact figure **is genuine, current AWS-published language** — found verbatim on
  `https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html`:
  *"Not only are current Graviton processors 20 percent cheaper than their Intel counterparts, but
  they also deliver a 20 percent or greater performance boost."* That page also gives a worked
  hourly-pricing table (c6i.xlarge $0.17 vs. c6g.xlarge $0.136 = 20%) confirming the number is not
  overstated. **However**, the lesson's own citation, `cite-saa-3-2-graviton`, points to
  `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html`, and that page's actual
  "AWS Graviton processors" section contains **no percentage figure at all** — it only says Graviton
  is "designed to deliver the best price performance" and links out to the AWS marketing page. This
  is a source mismatch, not a factual error: the claim is right, but the citation doesn't back it.
  Separately, several other current AWS docs (Elastic Beanstalk release notes, the AWS Graviton
  performance-testing whitepaper, the containers-on-AWS whitepaper) describe Graviton2-family
  instances (M6g/C6g/R6g/X2gd) as delivering "**up to 40% better price/performance**" — a different,
  larger, and also-current figure for a narrower comparison (whole-instance price/performance ratio
  vs. the lesson's per-processor cost/performance split). The lesson's 20%/20% framing does not
  contradict the 40% figure — they are two different, both-accurate AWS statistics for different
  comparisons — but a question writer building a drill from this lesson should not mix the two
  numbers into one distractor. See AWS-L32-001.
- **The 2-minute Spot interruption notice and rebalance recommendations.** The lesson's citation list
  includes `cite-saa-3-2-spot-interruption`, whose `note` states it "confirms Amazon EC2 issues a
  two-minute Spot Instance interruption notice as an EventBridge event and an instance metadata item
  before reclaiming Spot capacity" for "Lesson 3.2 K01/S03." This claim is itself accurate and
  well-documented (`spot-instance-termination-notices.html`: "A two-minute advance warning issued by
  Amazon EC2 as an EventBridge event and instance metadata item before a Spot Instance is
  interrupted"), and EC2 rebalance recommendations are a real, distinct, current signal
  (`rebalance-recommendations.html`: "notifies you when a Spot Instance is at an elevated risk of
  interruption... before the two-minute interruption notice"). **But neither the two-minute notice
  nor rebalance recommendations appear anywhere in the lesson's `bodyMarkdown`.** K01 and K04 mention
  Spot only as a capacity/purchase option ("provisions the Amazon EC2 (including Spot)...", "combine
  On-Demand and Spot purchase options"), never its interruption behavior. This is exactly the kind of
  citation-without-supporting-claim gap the review brief asks about. See AWS-L32-002.

## 3. Issues

| # | Location | Severity | Problem | Fix | Doc URL |
|---|---|---|---|---|---|
| AWS-L32-001 | `content/citations/cite-saa-3-2-graviton.json`; lesson S03, Graviton sentence | Medium | The citation's `note` and URL (`AWSEC2/latest/UserGuide/instance-types.html`) claim to confirm the "20 percent lower cost and 20 percent or greater performance" figure, but that page contains no percentage at all for Graviton — it only names Graviton and links to the marketing page. The figure itself is accurate AWS language, just sourced from a different, uncited page. | Change the citation's `url` to `https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html` (section "Understand price variations between processor architectures," which states this exact 20%/20% figure with a worked pricing table), and update the `title` accordingly (e.g., "Select the right instance type for Windows workloads — processor architecture pricing"). Keep `instance-types.html` as a second citation only if it is re-scoped to support the instance-naming claim it actually backs (S03's `cite-saa-3-2-instance-type-naming` already covers that separately, so `instance-types.html` can simply be dropped from this citation). | https://docs.aws.amazon.com/prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html |
| AWS-L32-002 | K01/K04 Spot mentions; `content/citations/cite-saa-3-2-spot-interruption.json` | Medium | The review brief specifically names "the 2-minute Spot interruption notice and rebalance recommendations" as facts to check, and the lesson carries a dedicated citation for exactly this fact — but the lesson body never states the two-minute notice, never mentions it fires as an EventBridge event or instance-metadata item, and never mentions rebalance recommendations at all. A student reading only the lesson text has no way to answer a drill question built from this citation, and the citation itself is currently unsupported by any sentence in the body (a coverage/consistency gap, not a wrong fact). | Add one or two sentences to K04 (immediately after the mixed instances policy sentence, since that is where Spot capacity is already discussed) along the lines of: "Because Spot Instances can be reclaimed, Amazon EC2 gives a two-minute Spot Instance interruption notice as an EventBridge event and an instance metadata item before terminating a Spot Instance, and it can also send an earlier rebalance recommendation when a Spot Instance is at elevated risk of interruption — a fleet or Auto Scaling group can use either signal to drain work and replace the instance proactively instead of waiting for the hard interruption." This also gives S01/S02 a natural tie-in (rebalance recommendation as an early scaling/replacement trigger). | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html and https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/rebalance-recommendations.html |
| AWS-L32-003 | S02, Compute Optimizer sentence | Low (coverage, optional) | The lesson's Compute Optimizer resource list (EC2 instances, ASGs, Lambda, EBS, ECS on Fargate) is accurate but is a subset of the service's current supported-resource list, which also includes Aurora/RDS, DynamoDB, ElastiCache, MemoryDB, DocumentDB, NAT Gateway, WorkSpaces, SageMaker, and commercial software licenses. Not an error — SAA-3.2 is a compute objective, so limiting the list to compute-adjacent resources is defensible — but worth flagging so a question writer doesn't treat this five-item list as exhaustive when writing a distractor. | Optional: add a short clause, e.g., "...(Compute Optimizer also covers several database, cache, and other resource types beyond compute)." No citation change needed. | https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html |

No factual error was found in any EC2 instance-family/naming detail, any placement-group limit, ENA/EFA
description, warm pool/instance refresh/mixed-instances mechanic, Lambda memory-to-vCPU mapping,
reserved-vs-provisioned-concurrency distinction, SnapStart runtime list, AWS Batch or EMR description,
or the SQS scaling-metric name. Both issues found are citation-sourcing/coverage defects, not
wrong-direction factual errors: AWS-L32-001's number is correct AWS language attached to the wrong URL,
and AWS-L32-002's citation supports a real fact that the body text never actually states.

## 4. Exam tips

All 10 `**Exam tip:**` lines were checked against their paired section content and against current docs:

- K01's tip (Batch = queue/run-to-completion/scale-to-zero; EMR = petabyte-scale Spark/Hadoop; Fargate
  = always-on service) draws a correct, testable three-way distinction.
- K02's tip (Local Zones/Wavelength/Outposts keyed to metro AWS location vs. telecom 5G vs. customer
  facility) is correct and matches each service's own scope.
- K03's tip (queue-depth scaling vs. CPU-based target tracking) is correct and consistent with K04/S02.
- K04's tip (warm pool vs. instance refresh vs. mixed instances policy) is correct and matches the
  three confirmed mechanics in §1.
- K05's tip (provisioned concurrency/SnapStart for speed vs. reserved concurrency for concurrency
  ceiling) is a correct, frequently tested distinction and matches `lambda-concurrency.html`.
- K06's tip (task/pod count scaling vs. EC2 capacity scaling, collapsed under Fargate) is correct.
- S01's tip (queue/topic/bus for independent scaling, not one shared fleet) is correct.
- S02's tip (CloudWatch metric matched to bottleneck vs. Compute Optimizer for right-sizing) is correct
  and unaffected by AWS-L32-003.
- S03's tip (partition for large distributed systems isolating rack failures vs. spread for few
  critical instances vs. cluster for lowest latency) is correct and matches the confirmed 7-partition
  and 7-instance-per-AZ limits exactly.
- S04's tip (a fast-but-cheap-at-low-memory Lambda function is not necessarily well-sized) is a
  correct, testable point consistent with K05's memory-to-CPU-to-duration chain.

None of the exam tips are stale, overstated, or misleading.

## 5. Coverage and consistency

- All 10 `SAA-3.2-*` objective bullets (K01–K06, S01–S04) get their own `###` section, matching
  `content/objectives/saa_c03.json` exactly — no missing or extra objective.
- All 18 `citationIds` resolve to existing files under `content/citations/`. Every citation's `note`
  names a specific claim and section (`Lesson 3.2 <ids>`), consistent with the lesson-2-1/1-3/3-1
  standard. One citation (`cite-saa-3-2-graviton`) names the right claim but the wrong URL
  (AWS-L32-001); one citation (`cite-saa-3-2-spot-interruption`) names a real claim that the body text
  never actually states (AWS-L32-002). The other 16 citations were spot-checked against the URLs
  fetched in this review and each supports the specific sentence its `note` describes — no other
  orphaned or topically mismatched citation.
- All 16 `drillIds` resolve to existing `q-saa-3-2-*` files per the impl notes; these remain
  unrewritten placeholders restating the objective text, consistent with the impl notes' statement
  that question rewriting is a separate pass.
- No contradiction found with Lesson 2.1: Lambda's 900-second (15-minute) timeout is not restated
  here (correctly out of scope for this lesson), Fargate's "no EC2 management" framing in K01/K06
  matches Lesson 2.1's Fargate description, and the ECS-vs-EKS orchestration choice in K06 correctly
  defers to Lesson 2.1 K14 rather than re-arguing it. Lesson 2.1 S02's four Auto Scaling policy types
  (target tracking, step, scheduled, predictive) and horizontal-vs-vertical scaling are correctly
  treated as already covered and not repeated, only extended (warm pools, instance refresh, mixed
  instances policies, AWS Auto Scaling's cross-resource scope).
- No retired, renamed, or closed service was found: AWS Batch, Amazon EMR, AWS Fargate, EC2 Auto
  Scaling, AWS Auto Scaling, AWS Lambda (including SnapStart and both concurrency types), Amazon ECS,
  Amazon EKS, AWS Local Zones, AWS Wavelength, and AWS Outposts are all current, active AWS offerings
  as of the 2026-09-26 doc checks in this review. "Amazon ECS Managed Instances" (named in K01) is a
  real, current AWS Batch compute-environment type (`ECS_MANAGED_INSTANCES`), not a fabricated or
  stale name.

**Lesson 3.2: not yet**

## Overall: concerns

Every individual fact checked in this review — instance-type naming, placement-group limits, ENA/EFA,
warm pools, instance refresh, mixed instances policies, the Lambda memory-to-vCPU relationship and its
vCPU breakpoint, reserved vs. provisioned concurrency, SnapStart's supported runtimes, AWS Batch, EMR,
and Compute Optimizer's lookback periods — is accurate and matches current AWS documentation, including
the Graviton price-performance percentage, which is genuine AWS language and not overstated. The two
issues found are both citation-quality defects rather than wrong-direction errors: AWS-L32-001 attaches
a correct figure to a citation URL that doesn't actually contain it (the real source is a different,
easily substituted AWS page), and AWS-L32-002 is a citation for a real, exam-relevant fact (the 2-minute
Spot interruption notice and rebalance recommendations, both explicitly named in this review's brief)
that never made it into the lesson's own body text, leaving that citation unsupported and that fact
untaught. Both are small, mechanical fixes — a citation URL swap and one or two added sentences — with
no other change needed. Recommend Lead Dev apply AWS-L32-001 and AWS-L32-002 (AWS-L32-003 is optional),
then this lesson can be re-validated and approved.
