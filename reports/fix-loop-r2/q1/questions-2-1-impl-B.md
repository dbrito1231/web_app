# Task 2.1 skill questions — writer B implementation report

**Scope:** the 14 skill questions `content/questions/q-saa-2-1-s01..s07-{mc,mr}.json`. Writer A owns the `k*` files; not touched here. No new citation files were created — every question reuses a `citationIds` entry already listed in `lesson-2-1.json`'s `citationIds` (all previously fetched and Teacher/AWS-approved for that lesson), so no new `cite-saa-2-1-s-*` files were needed. `content/lessons/lesson-2-1.json` was not edited; `drillIds` already lists all 14 files, so no lesson change was required there either.

## Metrics (scripted, over these 14 files only)

- Shape: all MC have 4 choices, all MR have 5; `selectCount` matches key length; every MR stem contains "(Select TWO.)"; every question has `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`, and a non-empty `citationIds` list.
- **0** choices contain "Apply the objective" or paste objective text verbatim.
- **0** letter references in any rationale (checked for "choice a/b/c/d/e", "option a/…", "answer a/…").
- **Stem openings (first 6 words):** all 14 unique, no collisions with each other. None start with a company noun phrase (writer A's pattern) — openings used: "A solutions architect is designing…", "The operations team at a retailer…", "An application's CPU utilization rises…", "During a traffic spike planning session,…", "A payment service currently calls a…", "A retailer needs one event producer…", "An application currently runs as a…", "A platform team is choosing compute…", "A workload runs in several short…", "A finance workload runs 24 hours…", "A new order-processing service needs several…", "A new architecture needs a compute…", "External partners need to upload files…", "A team's database credentials currently live…".
- **MC longest-is-key rate:** 2 of 7 (28.6%), within the ≤35% cap. (s01-mc and s04-mc have the key as the longest choice; s02, s03, s05, s06, s07 do not.)
- **MC key letter spread:** a:2, b:2, c:2, d:1.
- **MR key slot spread (across a–e, 14 correct-answer slots total):** a:3, b:3, c:2, d:3, e:3.
- **Distractor-type diversity, writer B's share:** 35 distractors across 14 questions, mapped to 35 distinct semantic types; the most-repeated types occur **exactly 2** times each (7 types at 2, the remaining 21 types at 1). No type exceeds the 2-per-writer-B cap. Full table below.
- `python scripts\content_lint.py` → `PASS` (questions 429, aws 310, tf 119, labs 21+21, lessons 23) — run after all 14 files were finalized, no writer-A collision observed.
- All `citationIds` used resolve to existing files in `content/citations/`.

## Per-question table

| ID | Objective | What it tests | Key | Lesson sentence taught before test | Doc URL(s) |
|---|---|---|---|---|---|
| q-saa-2-1-s01-mc | S01 | Choosing an event-driven design over sync calls, a monolith, or a stateful design for independent, reactive services | a | "In an event-driven architecture, a producer publishes an event... without knowing which consumers, if any, will act on it — this is what makes the design loosely coupled." (K05) | docs.aws.amazon.com/eventbridge (cite-saa-2-1-eventbridge-bus) |
| q-saa-2-1-s01-mr | S01 | Combining event-driven (publish, don't poll) and stateless-microservice (externalize session) design in one rebuild | a, d | K05 event-bus sentence above; K04 "it externalizes session state to a shared store... so an Application Load Balancer can send the next request from the same client to any healthy instance" | eventbridge-bus, microservices-whitepaper |
| q-saa-2-1-s02-mc | S02 | Picking target tracking for proportional, unscheduled traffic vs. scheduled/predictive/step | b | "Target tracking keeps a chosen CloudWatch metric... at a set value and is the recommended default for most variable web traffic." (S02) | docs.aws.amazon.com/autoscaling (cite-saa-2-1-asg-dynamic-scaling) |
| q-saa-2-1-s02-mr | S02 | Picking scheduled scaling (known date) + step scaling (breach-sized response) together | b, e | S02: "Scheduled scaling changes capacity at a known time..."; "Step scaling applies scaling adjustments sized to how far a CloudWatch alarm has been breached..." | asg-dynamic-scaling |
| q-saa-2-1-s03-mc | S03 | Recognizing a queue as the loose-coupling fix vs. vertical scaling, merging services, or adding retries to a sync call | c | "SQS buffers work between a producer and a consumer that runs at a different pace." (S03) | docs.aws.amazon.com/sqs (cite-saa-2-1-sqs-types) |
| q-saa-2-1-s03-mr | S03 | Matching SNS fan-out (many subscribers) and ALB (decouple client from instance) to two stated needs | a, c | S03: "SNS decouples one publisher from many subscribers."; "An ALB decouples clients from the specific backend instance handling a request." | sns-fanout, alb-elb |
| q-saa-2-1-s04-mc | S04 | Choosing App2Container for a no-rewrite lift-and-shift vs. rewriting into microservices, Lambda, or plain EC2 | d | "AWS App2Container analyzes an application already running on a server... and generates the deployment artifacts... without requiring source code changes." (K08) | docs.aws.amazon.com/app2container (cite-saa-2-1-app2container) |
| q-saa-2-1-s04-mr | S04 | Matching containers (consistent runtime) and Lambda (simple event-triggered function, nothing to containerize) to two needs | b, d | S04: "Choose containers when a workload needs a consistent runtime across environments..."; "...a short, simple, event-triggered function with no need for a custom runtime — Lambda has less to manage." | lambda-welcome |
| q-saa-2-1-s05-mc | S05 | Choosing Lambda for a bursty, idle-heavy workload with no servers/containers to patch, vs. Reserved/On-Demand EC2 or a self-managed cluster | a | "AWS Lambda runs your code on demand in response to an event, scales automatically from zero, and bills only for the compute time actually consumed." (K12); "Favor Lambda... when a workload is intermittent or spiky and paying for idle capacity is wasteful." (S05) | docs.aws.amazon.com/lambda (cite-saa-2-1-lambda-welcome) |
| q-saa-2-1-s05-mr | S05 | Matching Reserved-Instance EC2 (steady 24/7) and Lambda (short nightly job, no image) to two workloads | c, e | S05: "...utilization is high and constant enough that reserved... pricing beats per-invocation serverless pricing..."; K12 Lambda per-invocation billing; K12 "hard maximum execution timeout of 900 seconds" | lambda-welcome, lambda-timeout |
| q-saa-2-1-s06-mc | S06 | Picking EFS for a filesystem shared/mounted concurrently by many instances vs. EBS, S3, or instance store | b | "File storage (Amazon EFS for Linux... ) is a shared, network-mounted filesystem that many instances can mount concurrently — something a single EBS volume cannot do." (K13) | docs.aws.amazon.com EC2 storage guide (cite-saa-2-1-ec2-storage-options) |
| q-saa-2-1-s06-mr | S06 | Matching Lambda (short event-triggered compute) and ALB (URL-path routing) to two requirements at once | a, d | S06: "Compute: Lambda for short event-driven code..."; K09 "supports path- and host-based routing" (ALB) | lambda-welcome, alb-elb |
| q-saa-2-1-s07-mc | S07 | Choosing Transfer Family for a managed SFTP endpoint vs. a self-managed server, presigned URLs, or EFS mounted by outsiders | c | "AWS Transfer Family is a fully managed SFTP, FTPS, FTP, or AS2 endpoint in front of Amazon S3 or Amazon EFS — partners keep their existing file-transfer clients while you run no server infrastructure." (K02) | docs.aws.amazon.com/transfer (cite-saa-2-1-transfer-family-what-is) |
| q-saa-2-1-s07-mr | S07 | Matching Secrets Manager (auto rotation) and Step Functions (replace custom retry code) to two self-managed pain points | b, e | K02: "AWS Secrets Manager stores credentials and can automatically rotate them on a schedule..."; K16: "AWS Step Functions coordinates multiple steps... as a visual state machine instead of custom orchestration code you would otherwise have to write and retry yourself." | secrets-manager-rotate, step-functions-welcome |

## Distractor-type table (writer B's 14 questions, 35 distractors — post Lead Dev fix)

Superseded by the Lead Dev review (`LD-Q21-001`/`002`/`003`); this table reflects the current files. All types stay real, current AWS services or configurations, none is an anti-pattern strawman, and each is wrong for one stated requirement.

| Type | Count | Example question(s) |
|---|---|---|
| sync-call-blocks-event-driven | 2 | s01-mc, s01-mr |
| wrong-scaling-policy-predictive | 2 | s02-mc, s02-mr |
| standing-instance-not-event-triggered | 2 | s04-mr, s06-mr |
| continuous-fargate-container-image | 2 | s04-mr, s05-mc |
| wrong-mechanism-not-requested-protocol | 2 | s07-mc (×2) |
| central-orchestration-not-event-driven | 1 | s01-mc |
| stateful-session-affinity | 1 | s01-mc |
| db-polling-not-event-driven | 1 | s01-mr |
| local-instance-session-cache | 1 | s01-mr |
| wrong-scaling-policy-schedule | 1 | s02-mc |
| wrong-scaling-policy-step | 1 | s02-mc |
| wrong-scaling-policy-target-tracking | 1 | s02-mr |
| right-policy-wrong-date | 1 | s02-mr |
| redundancy-without-decoupling | 1 | s03-mc |
| co-located-containers-shared-lifecycle | 1 | s03-mc |
| retry-does-not-decouple-sync-call | 1 | s03-mc |
| single-target-routing-not-fanout | 1 | s03-mr |
| wrong-messaging-pattern-single-consumer | 1 | s03-mr |
| single-target-load-balancer | 1 | s03-mr |
| rewrite-not-migration | 1 | s04-mc |
| wrong-compute-service | 1 | s04-mc |
| unwanted-extra-refactor-step | 1 | s04-mc |
| manual-config-drift | 1 | s04-mr |
| reserved-instances-for-idle-workload | 1 | s05-mc |
| on-demand-continuous-idle-cost | 1 | s05-mc |
| on-demand-costlier-than-reserved-steady | 1 | s05-mr |
| exceeds-service-limit | 1 | s05-mr |
| unwanted-container-image-step | 1 | s05-mr |
| single-instance-storage-not-shared | 1 | s06-mc |
| api-storage-not-filesystem | 1 | s06-mc |
| ephemeral-storage-not-durable | 1 | s06-mc |
| wrong-load-balancer-no-path-routing | 1 | s06-mr |
| interval-polling-not-event-triggered | 1 | s06-mr |
| self-managed-server-software | 1 | s07-mc |
| wrong-service-no-auto-rotation | 1 | s07-mr |
| schedule-trigger-not-orchestration | 1 | s07-mr |
| right-service-rotation-off | 1 | s07-mr |

Max count per type in writer B's set: 2 (5 types at 2, the remaining 31 at 1). None of the retired writer-A distractor ideas listed in the coordinator's avoid list (Parameter Store without rotation — kept unchanged since Lead Dev did not flag it; sticky sessions, Memcached, CloudFront cache, API Gateway cache, Route 53 weighted/latency, NLB for path routing, GWLB, SQS standard, SNS as a distractor, Kinesis, Lambda timeout as a distractor mechanism, Lambda provisioned concurrency, Spot Fleet, EBS, instance store as a distractor idea beyond s06-mc's pre-existing one, S3 via FUSE, ECS vs EKS, self-managed Kubernetes, Multi-AZ standby for reads, vertical resize, Step Functions Express, DataSync, self-managed SFTP on EC2) were introduced in the new choices; new replacements use App2Container, ECS co-location, EventBridge single-target, ALB single-target, Auto Scaling minimum-capacity, Fargate continuous, Classic Load Balancer, and Secrets Manager/EventBridge scheduling instead.

Note for Lead Dev merge: check this table against writer A's k-file table so no *task-wide* type exceeds 5 of 35.

## Lesson additions requested

None. Every concept tested, including the Lead Dev fix-round replacements (AWS Step Functions state-machine orchestration, ECS task definitions, EventBridge single-target rules, ALB target groups with one registered instance, Auto Scaling minimum capacity, Fargate long-lived containers, Classic Load Balancer round-robin, and Secrets Manager rotation left off), is already taught in `lesson-2-1.json`'s K01–K16 and S01–S07 sections (Step Functions: K16; ECS: K14; EventBridge: K05; ALB/target groups: K09; Auto Scaling: S02; Fargate: K12; Secrets Manager rotation: K02). No new lesson sentence was needed.

## Lead Dev review fixes

Fixed `LD-Q21-001` (strawman distractors), `LD-Q21-002` (self-explaining/giveaway choices, including two keys), and `LD-Q21-003` (loosely paired MR halves) from `reports/fix-loop-r2/q1/questions-2-1-LEADDEV.md`. `s02-mc` and `s07-mc` were not flagged and are unchanged. Rationales were rewritten to match every changed choice; `id`, `objectiveIds`, and `selectCount` are unchanged everywhere. Re-ran all metric scripts after the fixes: 14/14 unique stem openings, MC longest-is-key 2/7 (28.6%), MC keys a:2/b:2/c:2/d:1, MR keys a:3/b:3/c:2/d:3/e:3, 0 rationale letter references, 0 giveaway markers left in choice text (scripted scan for "since/because/despite/so that/which are lost/requiring a container/…"), max 2-per-type in writer B's distractor table (above), and `content_lint.py` → PASS (429/310/119, labs 21+21, lessons 23).

| Question | Choice | Old → New | Reason |
|---|---|---|---|
| s01-mc | b | "A single monolithic application that performs all order logic in one deployable unit" → "AWS Step Functions with a single central state machine that calls each of the three services in a fixed sequence" | LD-Q21-001: real orchestration service, wrong because it's centrally sequenced rather than event-reactive |
| s01-mr | a (key) | "Publish order-status changes to an event bus so interested services react instead of polling for updates" → "Publish order-status changes to an event bus for interested services to consume" | LD-Q21-002: key restated the requirement ("instead of polling") |
| s01-mr | b | "Keep the presentation, logic, and data tiers on one shared subnet and security group so nothing has to cross a boundary" → "Each service repeatedly querying a shared database table to check for new order-status rows" | LD-Q21-001: real polling mechanism, still fails "without polling" |
| s01-mr | d (key) | "Externalize each service's session state to a shared store so any healthy instance can serve the next request" → "Externalize each service's session state to a shared data store such as DynamoDB or ElastiCache" | LD-Q21-002: key restated the requirement verbatim |
| s01-mr | e | "Store persistent order records only in each service instance's local, ephemeral storage" → "Each service instance caching its own local copy of a client's session data, refreshed from the database only when that instance restarts" | LD-Q21-001/003: real stateful-caching config, plausibly answers the session-affinity half |
| s02-mr | b (key) | "Scheduled scaling that changes capacity at the known calendar date" → "Scheduled scaling that changes capacity at a set date and time" | LD-Q21-002: trimmed echo of the stem's "known...in advance" wording |
| s02-mr | d | "Manual scaling changes applied by an operator when traffic looks high" → "A scheduled scaling action already configured for last year's peak sales date" | LD-Q21-001: real, taught feature (scheduled scaling) misapplied to the wrong date, instead of an "operator eyeballing traffic" anti-pattern |
| s02-mr | e (key) | "Step scaling that sizes its capacity change to how far the alarm was breached" → "Step scaling that sizes each capacity change to the alarm's breach amount" | Minor neutral rewording, same definitional fact |
| s03-mc | a | "Give the fraud-check service a larger EC2 instance type so it responds faster" → "Place two fraud-check service instances behind an Application Load Balancer that the payment service calls directly for every transaction" | LD-Q21-001: real ALB-fronted redundancy pattern, wrong because the call is still direct and synchronous |
| s03-mc | b | "Merge the payment and fraud-check logic into one combined process" → "Package the payment and fraud-check logic as two containers within the same ECS task definition" | LD-Q21-001: real ECS co-location config, still one shared failure domain, not decoupled |
| s03-mc | c (key) | "Insert a queue between the two services so the payment service can hand off work without waiting on the fraud-check service" → "Insert a queue between the payment service and the fraud-check service" | LD-Q21-002: key explained its own benefit |
| s03-mr | b | "A single synchronous call hardcoded to one backend instance's private IP address" → "An Amazon EventBridge rule that matches the event and delivers it to one target" | LD-Q21-001/003: real EventBridge config, plausibly answers the fan-out half (single target, not many subscribers) |
| s03-mr | e | "A direct database connection shared by every client" → "An Application Load Balancer with only one instance registered in its target group" | LD-Q21-001/003: real ALB misconfiguration, plausibly answers the healthy-instance half |
| s04-mc | c | "Move the application to an EC2 instance running the same operating system with no container runtime involved" → "Use AWS App2Container to containerize the application, then refactor its business logic into separate microservices before deploying" | LD-Q21-001: uses the correct tool but adds back the refactor step the team explicitly ruled out |
| s04-mr | a | "A self-managed Kubernetes cluster built from scratch on bare EC2 instances for the short file-triggered function" → "An EC2 instance configuration copied and reapplied by hand across the dev, test, and production environments" | LD-Q21-001/003: real manual-EC2-config drift, plausibly answers the consistent-runtime half |
| s04-mr | c | "An EC2 instance running the short function directly on the host OS with no runtime isolation at all" → "An EC2 Auto Scaling group with a minimum capacity of one instance kept running at all times to handle the file-triggered function" | LD-Q21-001/003: real standing-capacity config, plausibly answers the event-triggered-function half |
| s04-mr | d (key) | "AWS Lambda for the short function triggered when a file arrives, since there is nothing to containerize" → "AWS Lambda for the function triggered when a file arrives" | LD-Q21-002: key gave away its own justification |
| s04-mr | e | "One shared virtual machine image duplicated manually into every environment for the consistent-runtime workload" → "AWS Fargate running a long-lived container that continuously polls for new files to process" | LD-Q21-001/003: real Fargate config, plausibly answers the event-triggered-function half (still needs a container image) |
| s05-mc | d | "A self-managed Kubernetes cluster kept warm at all times for the bursts" → "AWS Fargate running one container kept running continuously to handle each burst" | LD-Q21-001: real, taught (K12) compute service, wrong for the idle-cost/no-container-to-manage requirement |
| s05-mr | b | "AWS Lambda for the steady, high-utilization 24-hour workload despite its per-invocation execution limit" → "AWS Lambda running the steady, high-utilization 24-hour workload" | LD-Q21-002: dropped the self-explaining "despite its...limit" clause |
| s05-mr | d | "Fargate containers, requiring a container image to be built, for the two-minute nightly job" → "AWS Fargate running the two-minute nightly job" | LD-Q21-002: dropped the self-explaining "requiring a container image" clause |
| s05-mr | e (key) | "AWS Lambda for the two-minute nightly job, since no container image is wanted" → "AWS Lambda running the two-minute nightly job" | LD-Q21-002: key gave away its own justification |
| s06-mc | d | "Instance store volumes physically attached to each individual instance's host, which are lost whenever that instance stops or terminates" → "Instance store volumes physically attached to each individual instance's host" | LD-Q21-002: dropped the self-explaining "which are lost..." clause (moved to rationale) |
| s06-mr | b | "A Network Load Balancer routing HTTP requests by URL path across the backend instances" → "An EC2 Auto Scaling group with a minimum capacity of one instance kept running to handle the triggering event" | LD-Q21-003/avoid-list: NLB-for-path-routing is a writer-A idea; replaced with a real standing-capacity config that plausibly answers the compute half |
| s06-mr | c | "AWS Global Accelerator for the short, event-triggered function" → "A Classic Load Balancer distributing requests round-robin across the backend instances" | LD-Q21-003: Global Accelerator could not plausibly answer either half; Classic Load Balancer plausibly answers the routing half (no path-based routing) |
| s06-mr | e | "An EC2 instance manually inspecting each request's path before forwarding it to another instance" → "An EC2 instance running a script that checks once a minute for the triggering condition" | LD-Q21-001/003: real interval-polling config, plausibly answers the event-triggered-function half |
| s07-mr | c | "A new hand-written Lambda function that polls each workflow step and retries failures itself" → "Amazon EventBridge invoking a Lambda function on a fixed schedule to advance the workflow to its next step" | LD-Q21-001: real, taught (K05) scheduling mechanism, wrong because it only triggers on a timer rather than tracking workflow state and retries |
| s07-mr | d | "Copying the same configuration file with the credentials to every server that needs it" → "AWS Secrets Manager storing the credentials, with automatic rotation left turned off" | LD-Q21-001: right service, real misconfiguration (rotation off), instead of an unrelated file-copying anti-pattern |
| s07-mr | e (key) | "AWS Step Functions replacing the custom retry and orchestration code for the workflow" → "AWS Step Functions coordinating the multi-step order workflow as a state machine" | LD-Q21-002: key explicitly named what it was "replacing" |

`a` in s07-mr (Parameter Store configured to auto-rotate) was left unchanged — it was not flagged in the Lead Dev report and is already a real-service-based distractor (a real, taught service used in a way it does not actually support), not a strawman.
