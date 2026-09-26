# Task 2.1 questions — writer A implementation report

Scope: the 21 knowledge questions `content/questions/q-saa-2-1-k*.json` (k01–k16, including the k02-mr, k05-mr, k08-mr, k11-mr, k14-mr variants). Writer B owns the `s*` files in parallel; no `s*` file or `content/lessons/lesson-2-1.json` was touched.

## Metrics (script-verified, `wA_verify.py`)

| Check | Result |
|---|---|
| Question count | 21 (16 MC + 5 MR) |
| Unique 6-word stem openings | PASS — no duplicates |
| All stems open with a company/team noun phrase (never "A solutions architect…") | PASS |
| MR stems state how many to pick | PASS — every MR stem ends "(Select TWO.)" |
| Choice count | MC = 4, MR = 5 — PASS all 21 |
| `correctAnswerIds` length matches `selectCount` | PASS all 21 |
| Letter references in rationale ("choice a", "option b", etc.) | 0 found |
| Objective text pasted into a choice | 0 found |
| Choice-to-choice cross references | 0 found |
| Citations present, `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` | PASS all 21 |
| MC key distribution (a/b/c/d) | a:4, b:4, c:4, d:4 — perfectly even |
| MR key-slot distribution (a–e) | a:2, b:2, c:2, d:2, e:2 — perfectly even |
| Longest choice is the key (MC only) | 4 / 16 = 25.0% (≤ 35% target, after the Lead Dev fix round below) |
| `python scripts\content_lint.py` | **PASS** (429 questions, 310 AWS / 119 TF, 21+21 labs, 23 lessons) |
| All 21 files parse with `json.load` | PASS |

Two fixes were applied after the first draft to hit the balance targets:
- Shortened the key choice text in k01-mc, k02-mc, k03-mc, k04-mc (kept the same meaning; the trimmed detail — e.g. OIDC/OAuth 2.0 support for k01 — is still covered in the rationale) so the longest-choice-is-key rate dropped from 9/16 (56%) to 5/16 (31%).
- Reordered (relabeled a–e) the choices in all five MR questions so correct-answer letters spread evenly instead of clustering at a/b.

A second round of fixes (Lead Dev pre-review, see "## Lead Dev review fixes" below) replaced several strawman/self-explaining distractors; that round happened to drop the longest-is-key rate further, to 4/16 (25%), with no separate action needed for that metric.

## Per-question table

| ID | Objective | Tests | Key | Lesson sentence (K-section) | Doc(s) |
|---|---|---|---|---|---|
| q-saa-2-1-k01-mc | SAA-2.1-K01 | HTTP API vs REST API vs WebSocket API fit for a low-cost, low-latency Lambda backend | a | K01: "An HTTP API targets Lambda or any publicly routable HTTP backend with lower latency and lower cost than a REST API… but it does not support usage plans, API keys, or request validation…" | apigw-overview |
| q-saa-2-1-k02-mc | SAA-2.1-K02 | Secrets Manager automatic rotation vs Parameter Store (no rotation), Secrets Manager with rotation left off, and AWS AppConfig (wrong purpose) | b | K02: "AWS Secrets Manager stores credentials and can automatically rotate them on a schedule… something a flat configuration file cannot do." | secrets-manager-rotate |
| q-saa-2-1-k02-mr | SAA-2.1-K02 | Picking Transfer Family (partner SFTP) + Secrets Manager (credential rotation) for two stated needs at once | a, c | K02: Transfer Family sentence above + "AWS Transfer Family is a fully managed SFTP, FTPS, FTP, or AS2 endpoint in front of Amazon S3 or Amazon EFS — partners keep their existing file-transfer clients…" | transfer-family-what-is, secrets-manager-rotate |
| q-saa-2-1-k03-mc | SAA-2.1-K03 | Redis OSS durability/failover vs Memcached, CloudFront edge cache, API Gateway stage cache | c | K03: "Redis OSS adds persistence (snapshots and append-only files), replication with Multi-AZ automatic failover… pick it when the cached data needs durability or a replica for read scaling." | elasticache-overview |
| q-saa-2-1-k04-mc | SAA-2.1-K04 | Stateless design (externalized session state) vs sticky sessions, local session memory, vertical resize | d | K04: "A stateless service keeps no session data on the instance that handled a request — it externalizes session state to a shared store such as DynamoDB or ElastiCache — so an Application Load Balancer can send the next request… to any healthy instance." | microservices-whitepaper |
| q-saa-2-1-k05-mc | SAA-2.1-K05 | Event-driven (EventBridge rule) vs a fixed-rate EventBridge Scheduler invocation, synchronous GetItem calls, and manually polled DynamoDB Streams | a | K05: "Amazon EventBridge is the router for this pattern: rules match incoming events against a pattern and deliver matches to up to five targets each…" | eventbridge-bus |
| q-saa-2-1-k05-mr | SAA-2.1-K05 | EventBridge pattern matching + default event bus already receiving AWS service events, vs SQS pattern matching (false), custom bus requirement (false), polling | b, d | K05: pattern-match sentence above + "…every AWS account has a default event bus that automatically receives events from AWS services." | eventbridge-bus |
| q-saa-2-1-k06-mc | SAA-2.1-K06 | Horizontal scaling (ASG) vs vertical scaling by launch-template replacement, an ASG with no scaling policy attached, and fleet consolidation | b | K06: "Horizontal scaling (scaling out and in) adds or removes instances behind a load balancer; it can happen with no downtime and has no real upper limit as long as the architecture is stateless." | asg-dynamic-scaling |
| q-saa-2-1-k07-mc | SAA-2.1-K07 | Global Accelerator (static IP, UDP, health-based routing) vs CloudFront caching, Route 53 DNS failover, API Gateway cache | c | K07: "AWS Global Accelerator… uses static anycast IP addresses and the AWS global network to improve availability and performance for TCP/UDP traffic, including non-cacheable and non-HTTP workloads, by routing to the healthiest endpoint — it does not cache content the way CloudFront does." | k-global-accelerator (new) |
| q-saa-2-1-k08-mc | SAA-2.1-K08 | App2Container automated lift-and-shift vs AWS Copilot (still needs a hand-written Dockerfile), a Lambda rewrite, and AWS MGN (rehosts but doesn't containerize) | d | K08: "AWS App2Container analyzes an application already running on a server… and generates the deployment artifacts… without requiring source code changes." | app2container |
| q-saa-2-1-k08-mr | SAA-2.1-K08 | What App2Container actually does (analysis + artifact generation) vs source rewrite, manual Dockerfile, overstated automation | a, e | K08: analysis sentence above + "This targets lift-and-shift containerization of an existing Java or .NET application rather than a from-scratch microservices rewrite." | app2container |
| q-saa-2-1-k09-mc | SAA-2.1-K09 | ALB path-based routing vs NLB (layer 4), Gateway Load Balancer (appliance inspection), Route 53 weighted routing | a | K09: "An Application Load Balancer (ALB) operates at the application layer (HTTP/HTTPS): it supports path- and host-based routing…" | alb-elb |
| q-saa-2-1-k10-mc | SAA-2.1-K10 | Multi-tier isolation (own subnet/SG per tier) vs a two-tier merge of the web and logic tiers, a database placed in a public subnet, and an ALB-to-Lambda design with no data tier | b | K10: "A classic multi-tier (three-tier) design separates a presentation tier… a logic/application tier… and a data tier… with each tier in its own subnet or security group boundary so it can scale, fail, and be secured independently." | multitier-whitepaper |
| q-saa-2-1-k11-mc | SAA-2.1-K11 | SQS FIFO (exactly-once, strict order) vs SQS standard, SNS fan-out, Kinesis | c | K11: "SQS FIFO queues add exactly-once processing and strict per-group ordering, at lower raw throughput than standard…" | sqs-types |
| q-saa-2-1-k11-mr | SAA-2.1-K11 | SNS fan-out mechanics (one topic, independent per-subscriber delivery) vs direct sequential calls, shared-queue polling, Kinesis overkill | c, e | K11: "Amazon SNS is publish/subscribe: a fan-out pattern publishes one message to a topic that pushes it to many subscribed SQS queues, Lambda functions, or other endpoints for independent, parallel processing." | sns-fanout |
| q-saa-2-1-k12-mc | SAA-2.1-K12 | Fargate for a 40-minute container job vs Lambda's hard 15-minute ceiling, provisioned concurrency (doesn't lift ceiling), unmanaged EC2 | d | K12: "A function has a hard maximum execution timeout of 900 seconds (15 minutes) per invocation, so work that could run longer belongs on Fargate, EC2, or in a Step Functions workflow instead." | lambda-timeout, fargate-compute |
| q-saa-2-1-k13-mc | SAA-2.1-K13 | EFS shared concurrent mount vs an EBS Multi-Attach volume (capped at 16 Nitro instances, one AZ), instance store, S3 FUSE workaround | a | K13: "File storage (Amazon EFS for Linux, or Amazon FSx…) is a shared, network-mounted filesystem that many instances can mount concurrently — something a single EBS volume cannot do." | ec2-storage-options |
| q-saa-2-1-k14-mc | SAA-2.1-K14 | EKS managed Kubernetes control plane vs ECS (no Kubernetes API), self-managed control plane, Fargate-for-ECS (still not Kubernetes) | b | K14: "Amazon EKS runs a managed Kubernetes control plane, so it fits a team that already standardizes on Kubernetes APIs, manifests, and the broader Kubernetes ecosystem, including multi-cloud portability." | eks-concepts, ecs-welcome |
| q-saa-2-1-k14-mr | SAA-2.1-K14 | ECS (AWS-native, no separate control plane) + Fargate (no EC2 to provision) vs EKS, ECS-on-EC2, self-managed Kubernetes | b, d | K14: "Amazon ECS is AWS's own container orchestrator… with an AWS-native scheduler and no separate control plane to run or patch. Both can run tasks or pods… on Fargate, which removes the EC2 layer entirely." | ecs-welcome, fargate-compute |
| q-saa-2-1-k15-mc | SAA-2.1-K15 | Read replica for read offload vs Multi-AZ (not for reads), vertical resize, off-peak scheduling | c | K15: "An Amazon RDS read replica is an asynchronous, read-only copy of a source DB instance, created to offload read-heavy traffic from the primary… This is different from a Multi-AZ standby, which replicates synchronously purely for automatic failover." | rds-read-replicas |
| q-saa-2-1-k16-mc | SAA-2.1-K16 | Step Functions Standard (long-running, auditable) vs Express (5-min cap), chained SQS delay queues (14-day retention cap, no audit trail), chained Express workflows (still 5-min per link) | d | K16: "Standard workflows give exactly-once execution, run up to one year, and keep full execution history for auditing and debugging. Express workflows give at-least-once execution, run up to five minutes…" | step-functions-welcome |

## Distractor-type table (writer A's 21 questions, post Lead Dev fixes)

Format: type — count (question IDs). Cap is 3 per type among writer A's 21; none exceed it (max is now 2, after the LD-Q21-001 fixes below split up what had been three uses of `vertical-scale-misfit` and three of `lambda-timeout-exceeded`).

| Type | Count | Questions |
|---|---:|---|
| vertical-scale-misfit | 2 | k04-mc, k15-mc |
| lambda-timeout-exceeded | 2 | k12-mc (×2) |
| param-store-no-rotation | 2 | k02-mc, k02-mr |
| apigw-cache-wrong-layer | 2 | k03-mc, k07-mc |
| manual-dockerfile-rewrite / rewrite-not-lift-shift note | 2 each | k08-mc, k08-mr (see below) |
| kinesis-overkill | 2 | k11-mc, k11-mr |
| ecs-not-kubernetes | 2 | k14-mc (×2) |
| self-managed-k8s-control-plane | 2 | k14-mc, k14-mr |
| rest-vs-http-overkill | 1 | k01-mc |
| websocket-not-needed | 1 | k01-mc |
| quota-increase-not-cost | 1 | k01-mc |
| rotation-disabled (new, replaces manual-process-not-managed) | 1 | k02-mc |
| appconfig-not-credential-store (new, replaces wrong-service-category) | 1 | k02-mc |
| self-managed-alternative | 1 | k02-mr |
| datasync-misuse | 1 | k02-mr |
| memcached-no-durability | 1 | k03-mc |
| cloudfront-wrong-layer | 1 | k03-mc |
| sticky-sessions-stateful | 1 | k04-mc |
| local-session-state | 1 | k04-mc |
| synchronous-coupling | 1 | k05-mc |
| scheduler-not-event-driven (new, replaces polling-instead-of-event) | 1 | k05-mc |
| stream-polled-manually (new, replaces batch-not-realtime) | 1 | k05-mc |
| polling-instead-of-event | 1 | k05-mr |
| sqs-no-pattern-match | 1 | k05-mr |
| unnecessary-custom-bus | 1 | k05-mr |
| vertical-via-replacement (new, replaces manual-vertical-toil) | 1 | k06-mc |
| scaling-policy-missing (new) | 1 | k06-mc |
| fewer-larger-instances | 1 | k06-mc |
| cloudfront-wrong-protocol | 1 | k07-mc |
| dns-routing-too-slow | 1 | k07-mc |
| copilot-still-manual-dockerfile (new, replaces manual-dockerfile-rewrite@k08-mc) | 1 | k08-mc |
| rewrite-not-lift-shift | 1 | k08-mc |
| mgn-no-containerize (new, replaces no-containerization) | 1 | k08-mc |
| manual-dockerfile-rewrite | 1 | k08-mr |
| rewrite-not-lift-shift | 1 | k08-mr |
| overstated-automation | 1 | k08-mr |
| nlb-wrong-layer | 1 | k09-mc |
| gwlb-wrong-purpose | 1 | k09-mc |
| dns-not-path-routing | 1 | k09-mc |
| two-tier-not-three (new, replaces tier-collapse) | 1 | k10-mc |
| db-in-public-subnet (new, replaces tier-collapse) | 1 | k10-mc |
| alb-lambda-no-data-tier (new, replaces bypass-tier-security) | 1 | k10-mc |
| standard-queue-no-ordering | 1 | k11-mc |
| sns-wrong-purpose | 1 | k11-mc |
| direct-sync-calls | 1 | k11-mr |
| shared-queue-not-fanout | 1 | k11-mr |
| unmanaged-ec2 | 1 | k12-mc |
| ebs-multiattach-limited (new, replaces ebs-not-shared) | 1 | k13-mc |
| s3-wrong-access-model | 1 | k13-mc |
| instance-store-ephemeral | 1 | k13-mc |
| eks-not-ecs-native | 1 | k14-mr |
| ecs-on-ec2-not-fargate | 1 | k14-mr |
| multiaz-not-for-reads | 1 | k15-mc |
| no-offload-solution | 1 | k15-mc |
| express-duration-too-short | 1 | k16-mc |
| sqs-delay-not-durable-enough (new, replaces lambda-timeout-exceeded@k16-mc) | 1 | k16-mc |
| express-chain-no-continuous-audit (new, replaces custom-orchestration-not-managed) | 1 | k16-mc |

Total tagged distractor instances: 63 (16 MC × 3 + 5 MR × 3). Max per type after the fix round: 2. This table is meant to be merged with writer B's `s*` table by Lead Dev to confirm the task-wide cap (≤5 of 35 per type). None of writer A's new distractor ideas (AWS AppConfig, EventBridge Scheduler, DynamoDB Streams polled manually, launch-template vertical replacement, an ASG with no scaling policy, AWS Copilot, AWS Application Migration Service, a two-tier merge, a database in a public subnet, ALB→Lambda with no data tier, EBS Multi-Attach, SQS delay queues, chained Express workflows) appear on the coordinator's list of ideas writer B is already using (monolith, target tracking/step/scheduled/predictive scaling, Fargate vs Lambda, Reserved/On-Demand EC2, EFS/EBS/S3/instance store as a set, Global Accelerator, NLB for path routing, Transfer Family, S3 presigned URLs, Parameter Store rotation), so there is no new overlap to flag.

## New citation added

- `content/citations/cite-saa-2-1-k-global-accelerator.json` — AWS Global Accelerator "how it works" doc page, fetched via the AWS Documentation MCP (`search_documentation` / confirmed against `introduction-how-it-works.html`), used by q-saa-2-1-k07-mc. The lesson's existing `citationIds` list had no Global Accelerator source even though K07's body discusses it, so this fills that gap without editing the lesson file itself.

## Lead Dev review fixes

Applied against `reports/fix-loop-r2/q1/questions-2-1-LEADDEV.md`. Only the items naming writer A's k* files are addressed here (LD-Q21-003 is s*-only, for writer B). Every new distractor below is a real, current, doc-verified AWS service or configuration, checked live against the AWS Documentation MCP during this fix round (EBS Multi-Attach, EventBridge Scheduler, AWS AppConfig, AWS Application Migration Service, and AWS Copilot were each looked up and confirmed before use). Rationales were rewritten to match every changed choice; ids, `objectiveIds`, `module`, `type`, and `selectCount` were left untouched.

### LD-Q21-001 — strawman distractors replaced with real AWS options

| Question | Choice | Old (strawman) | New (real AWS option, wrong for one stated requirement) |
|---|---|---|---|
| k02-mc | c | "Have an engineer manually change the password and update every application config file once a quarter" | "Store the password in AWS Secrets Manager, but leave automatic rotation turned off and update it from the console when needed" — real Secrets Manager configuration, fails only the "automatic" requirement |
| k02-mc | d | "Configure an AWS Transfer Family endpoint in front of the database so partners can retrieve the current password over SFTP" | "Store the password as an AWS AppConfig configuration profile and deploy updates to it through AppConfig" — real service, wrong purpose (deploys config, not credential rotation) |
| k05-mc | b | "Run a scheduled job on EC2 that queries the tracking table for changes every minute" | "Create an EventBridge Scheduler schedule that invokes the billing service on a fixed one-minute rate" — real, current AWS service, still time-driven rather than reacting to the actual change |
| k05-mc | d | "Run a nightly batch job that reconciles shipment statuses against billing once a day" | "Enable DynamoDB Streams on the tracking table and have the billing service call GetRecords against the stream on a fixed interval" — real feature, misused via manual polling instead of an event trigger |
| k06-mc | a | "Resize every web instance to the largest available instance type before each sale" | "Update the launch template to a larger instance type and run an instance refresh across the fleet before the sale" — real ASG mechanism, still a rolling per-instance outage with the same size ceiling |
| k06-mc | c | "Manually stop and restart each instance with a larger instance type ahead of the sale" | "Increase the Auto Scaling group's maximum capacity, without attaching a scaling policy that would launch new instances as demand rises" — real, common ASG misconfiguration (capacity ceiling raised, nothing triggers it) |
| k08-mc | a | "Have engineers manually inspect the server and hand-write a Dockerfile from scratch" | "Use AWS Copilot to deploy the application to ECS from a Dockerfile the team writes based on the existing server's dependencies" — real AWS CLI tool, still requires the team to author the Dockerfile itself |
| k08-mc | c | "Leave the application running unchanged on an EC2 instance with no containerization" | "Use AWS Application Migration Service (MGN) to rehost the application on a new EC2 instance without containerizing it" — real migration service, rehosts to EC2 rather than producing a container image |
| k10-mc | a | "Run the web server, application logic, and database together on a single monolithic EC2 instance" | "Combine the presentation and logic tiers behind one Auto Scaling group, with only the data tier in its own subnet and security group" — real two-tier design, merges only two of the three required boundaries |
| k10-mc | c | "Put the database in the same security group as the web tier so the two can reach each other freely" | "Place the database tier in a public subnet alongside the web tier, restricting access with a security group rule that allows only the app tier" — real (if risky) configuration; SG control exists, but the subnet itself is internet-routable |
| k10-mc | d | "Route internet traffic directly to the database tier to reduce the number of hops before a query" | "Route requests from an Application Load Balancer directly to AWS Lambda functions with no separate data tier, keeping state in the functions' own memory" — real serverless pattern, simply omits the persistent data tier |
| k13-mc | b | "A single Amazon EBS volume attached to one of the render nodes and shared informally over the network" | "Enable EBS Multi-Attach on a single io2 volume so it can attach directly to the render nodes" — real EBS feature, capped at 16 Nitro instances in one AZ and needs a cluster-aware filesystem, far short of 200 nodes |
| k16-mc | b | "A single Lambda function containing an internal loop with sleep calls between approval steps" | "Chain Amazon SQS delay queues between the approval steps, with each queue holding the claim until the next stage begins" — real SQS pattern, but 14-day max retention and no execution history for audits |
| k16-mc | c | "A cron-triggered script that polls a database periodically to check each claim's approval status" | "Chain several Step Functions Express workflows together, starting the next one when the previous one finishes" — real Step Functions capability, still 5 minutes per link with a separate execution record for each |

k06-mc's fourth choice ("Consolidate the fleet onto fewer, larger instances…") was left as written; it was not one of the three "make it bigger" repeats Lead Dev flagged (that was a, c, and the old d-adjacent manual-resize choice), and it now sits alongside two distinctly different flaws (a rolling vertical replacement, and a missing scaling policy) rather than three copies of the same idea.

### LD-Q21-002 — self-explaining / absolute-worded choices made neutral

| Question | Choice | Old (gives away the answer) | New (neutral) |
|---|---|---|---|
| k01-mc | b | "A REST API with usage plans and API keys configured, even though the team does not need to meter or key individual callers" | "A REST API with usage plans and API keys configured for the mobile backend" |
| k02-mc | a | "Store the password in AWS Systems Manager Parameter Store, which keeps configuration values but does not rotate them on a schedule" | "Store the password as an AWS Systems Manager Parameter Store SecureString parameter" |
| k03-mc | a | "Amazon ElastiCache for Memcached, since it is the simplest cache to operate" | "Amazon ElastiCache for Memcached" |
| k11-mr | a | "The publisher must call the SQS queue and then invoke the Lambda function directly, one after the other, to guarantee delivery" | "The publisher calls the SQS queue and then invokes the Lambda function directly, one after the other" |
| k11-mr | b | "A single SQS queue with both the indexer and the alerting logic polling it satisfies the requirement" | "A single SQS queue, with both the indexer and the alerting logic polling it" |
| k11-mr | d | "Kinesis Data Streams must be used here because more than one consumer will read the same message" | "Amazon Kinesis Data Streams, with the indexer and the alerting logic each reading from the stream independently" |

All six rationales were rewritten to carry the "why it's wrong" reasoning that used to live inside the choice text.

### Re-verified metrics after the fix round

- 6-word stem openings: still unique (stems were not touched in this round, only choices/rationale).
- Longest-is-key (MC): 4/16 = 25.0% (down from 5/16; no separate action needed — a side effect of the replaced choices' lengths).
- MC key balance: a4/b4/c4/d4 (unchanged — no keys moved).
- MR key-slot balance: a2/b2/c2/d2/e2 (unchanged — no keys moved).
- Letter references in rationale: 0.
- `python scripts\content_lint.py`: **PASS** (429 questions, 310 AWS / 119 TF, 21+21 labs, 23 lessons).
- Distractor-type cap: max 2 per type among writer A's 21 (see the updated table above), well under the 3-per-type share and the task-wide 5-of-35 cap.
- No overlap with writer B's listed distractor ideas (monolith, scaling-policy types, Fargate/Lambda, Reserved/On-Demand EC2, EFS/EBS/S3/instance store, Global Accelerator, NLB path routing, Transfer Family, S3 presigned URLs, Parameter Store rotation) was introduced by any of the new choices.

## Lesson additions requested

The original 21 questions needed none. The Lead Dev fix round introduced a handful of more specific AWS facts to replace strawman distractors; these are real and doc-verified (checked live against the AWS Documentation MCP during this round) but go a level deeper than `lesson-2-1.json`'s current text, so they are listed here rather than assumed taught:

- **K13 (storage types):** the lesson currently says only "block storage… attaches to a single EC2 instance." Suggested addition, doc-verified: "A Provisioned IOPS (io1/io2) EBS volume can use **Multi-Attach** to attach to up to 16 Nitro-based instances at once in a single Availability Zone, but only with a cluster-aware filesystem — it is not the same as EFS's many-instance sharing model." (Source: `https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes-multi.html`.)
- **K05 (event-driven architectures):** the lesson does not yet mention Amazon **EventBridge Scheduler** as distinct from EventBridge rules. Suggested addition: "EventBridge Scheduler creates one-time or recurring invocations of a target on a schedule; it is time-driven, unlike a rule, which reacts to an event the moment it arrives." (Source: `https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html`.)
- **K08 (migrating into containers):** the lesson covers App2Container but not the adjacent tools a candidate might substitute for it. Suggested addition: "**AWS Copilot** deploys an already-containerized application to ECS or Fargate from a Dockerfile or image the team supplies; it does not analyze a running server the way App2Container does. **AWS Application Migration Service (MGN)** rehosts a server onto a new EC2 instance as-is; it does not produce a container image." (Sources: `https://docs.aws.amazon.com/AmazonECS/latest/developerguide/copilot-deploy.html`, `https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-database-rehost-tools/mgn.html`.)
- **K16 (workflow orchestration):** the lesson does not mention SQS message retention as a contrast point. Suggested addition: "A queue is not a workflow: an SQS message's maximum retention is 14 days, far short of what a Standard Step Functions workflow's one-year run time allows, and a queue keeps no execution history for an audit." (Source: `https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html`, already cited elsewhere in this lesson.)
- **K02 (managed services):** the lesson does not mention AWS AppConfig. Suggested addition: "**AWS AppConfig** deploys configuration and feature-flag data to an application on a controlled rollout schedule; it has no credential-rotation capability, unlike Secrets Manager." (Source: `https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html`.)

None of these are required for the questions to be answerable — each rationale explains the fact inline — but Lead Dev may want to fold one or more sentences in during the next lesson revision pass for completeness.

## Files touched

- `content/questions/q-saa-2-1-k01-mc.json` … `q-saa-2-1-k16-mc.json` (16 files) — full rewrite from the placeholder template stems to scenario-based questions.
- `content/questions/q-saa-2-1-k02-mr.json`, `k05-mr.json`, `k08-mr.json`, `k11-mr.json`, `k14-mr.json` (5 files) — full rewrite, same treatment.
- `content/citations/cite-saa-2-1-k-global-accelerator.json` (new).
- `reports/fix-loop-r2/q1/questions-2-1-impl-A.md` (this report).

`id`, `type`, `module`, `objectiveIds`, and `selectCount` were left unchanged on every file per the writer-A instructions; only `stem`, `choices`, `correctAnswerIds`, `rationale`, `citationIds`, `reviewedOn`, and `mcpStatus` were rewritten.
