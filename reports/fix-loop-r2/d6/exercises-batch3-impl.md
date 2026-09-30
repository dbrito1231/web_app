# D6 Part B batch 3 (domains 4.1 and 4.2, 16 exercises): writer report

Scope changed mid-task: only the 16 exercises of 4.1 and 4.2. The 8 files of 4.3 and 4.4 (de-db-migration, de-saa-4.3-s02, de-saa-4.3-s04, de-saa-4.4-s03, s05, s07, de-tgw, de-throttling) were NOT edited by me.

Method: read the plan, RULES, batch-1 review, lessons 4.1 and 4.2. AWS facts checked with the AWS docs MCP: AWS Backup cold storage needs 90 days and is not offered for RDS (backup-feature-availability and plan-options pages); EC2 hibernation needs a Linux instance under 150 GiB of RAM (hibernating-prerequisites). Everything else is the lesson's own wording. No dollar prices of AWS services appear; budgets are relative or caps.

## de-saa-4.1-s01

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Teasel Weather Network has 4,000 roadside stations, and each writes a 2 KB reading every 10 seconds as its own object in a storage bucket; the request line of the monthly bill now exceeds the storage line. Forecasters need a reading to be queryable within 2 hours of capture, and a station can hold at most 60 minutes of readings in its memory. Separately, the 40 stations with wave sensors upload one 60 GB raw file each night over a poor mobile link: about one upload in ten breaks off partway and the station starts the whole file again, and the storage line includes data from broken attempts that no object listing shows. Finance will not pay for that leftover data for longer than 7 days.
- Added constraints: Field staff cannot be sent to a station to clear failed uploads | Every reading must still be stored; none may be dropped to save requests | Finance wants the request-count part of the bill cut by at least 90 percent
- r6: Request volume for sensor readings falls by at least 90 percent while every reading is still queryable within 2 hours of capture and no station holds more than 60 minutes of readings
- r7: A broken 60 GB upload does not resend the portions already delivered, and storage held by abandoned attempts is gone within 7 days with no staff action
- Decisive figures: 2 KB reading every 10 s; 2-hour freshness; 60-minute station buffer; 90 percent request cut (hourly batches give 96,000 objects/day vs 34.56M, a 99.7 percent cut); 1 in 10 uploads breaks; 7-day leftover limit.
- Why one best design: Only grouping readings meets both the cut and the 2-hour limit; the nightly file needs resumable parts plus expiry of abandoned parts.
- Services/options named or needed, and the lesson sentence: batching, multipart upload, S3 Lifecycle: 'multipart upload so parts transfer in parallel and a failed part only needs to be retried'; 'expire incomplete uploads'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s02

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Bellhaven Dairy Co-op is moving its ERP database to a single new server with one block volume. The database holds 1.1 TB today and has grown by about 40 GB a month for three years. The old server carried a 4 TB volume 'to be safe', and Finance now refuses to pay for capacity that will not hold data within the next 90 days. The database may be stopped only during a quarterly maintenance window, and the volume type and performance settings stay as they are.
- Added constraints: Finance pays only for capacity needed within the next 90 days | The database cannot be stopped outside the quarterly maintenance window | The data-platform engineer reviews capacity once a month and has no time to rebuild servers
- r6: The initial volume is no larger than 1.5 TB, derived from today's 1.1 TB and 90 days of growth at 40 GB a month, with the margin stated
- r7: Making the volume larger later needs no database stop and no new server, and the record gives the monthly check that triggers it
- Decisive figures: 1.1 TB + 40 GB/month; 90-day funding rule (1.1 TB + 120 GB = 1.22 TB, cap 1.5 TB); stop only in quarterly window.
- Why one best design: Start near measured need and grow later with no stop; 4 TB is excluded by the 90-day rule and a rebuild by the stop rule.
- Services/options named or needed, and the lesson sentence: 'Elastic Volumes let you grow size, change type, or adjust performance later without downtime'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s04

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Tallowmere Podcasts keeps 9 TB of finished episode audio in object storage, growing by 1 TB a month. Its 12 editing servers share a file system that grew from 2 TB to 5 TB with no administrator action. Its publishing database sits on one 1 TB block volume holding 800 GB today; a bulk catalogue import of up to 150 GB, arriving about weekly, has twice filled that volume at 3 a.m. and stopped publishing until staff enlarged it by hand. Nobody is on call overnight.
- Added constraints: Nothing may depend on a person waking up to add storage | The platform team will not build automation for a store that already grows on its own | Capacity must not be bought ahead of need for any of the three stores
- r6: For each of the three stores the record states whether growth needs any design work and gives the reason from the scenario
- r7: A 150 GB import at 3 a.m. completes without publishing stopping and without a person acting
- Decisive figures: three stores: 9 TB object store, shared file system that grew with no action, block volume 800 GB of 1 TB with 150 GB weekly imports; no on-call.
- Why one best design: Only the block volume needs automation; the other two are excluded by the 'grows on its own' facts.
- Services/options named or needed, and the lesson sentence: 'S3 and EFS already scale ... EBS volumes do not auto-scale ... a CloudWatch alarm triggering a Lambda function'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s05

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Copperfield Survey Maps keeps 6 TB of scanned plot maps, averaging 5 MB each, in a versioned bucket. A scan is read several times a week for its first 30 days and then only a few times a year, yet a clerk at the counter must see it open in under a second; scans are kept for 7 years and then deleted. The bucket also holds about 400 million 30 KB thumbnails that clerks browse daily at any age. Each scan is re-saved about three times in its first month, the superseded copies are never read after 60 days, and large scan uploads over a poor link leave broken attempts behind. Finance wants none of that waste kept longer than 7 days.
- Added constraints: Scans older than 30 days must cost less to store than they do today | No rule may raise the storage or request cost of the thumbnails | Everything must run by rule; the records office has no spare staff for clean-up jobs
- r6: Scans older than 30 days sit on the option with the lowest storage cost that still opens in under a second and whose minimum storage period the 7-year retention clears, while thumbnail storage and request cost does not rise
- r7: Superseded scan copies are gone by day 60, broken upload leftovers within 7 days and scans at the 7-year mark, each with the day number stated
- Decisive figures: scans 5 MB, 30 days hot then few reads/year, instant open, 7 years; thumbnails 30 KB; 3 re-saves in month 1; old copies dead after 60 days; 7-day waste limit.
- Why one best design: Thumbnails under 128 KB must be left alone; scans go to the lowest-cost instant class (its 90-day minimum is cleared by 7 years).
- Services/options named or needed, and the lesson sentence: 'by default only objects of at least 128 KB transition'; Glacier Instant Retrieval '90 days ... 128 KB minimum billed object size'; expiration of noncurrent versions and incomplete multipart uploads.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s06

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Merrow Veterinary Group runs 60 clinics whose practice-management servers keep records on 14 block volumes and 2 shared file systems. The insurer requires every recovery point to be held for 7 years: daily points for the first 35 days, after which restores are needed only a few times a year and may wait up to a full working day. Today the team runs one scheduled script per resource type and cannot show the insurer one retention rule covering all of them. Merrow wants points older than 35 days to cost well below the price of the first 35 days' points.
- Added constraints: The insurer asks for one retention rule that covers every resource type | The operations team will not maintain per-resource scripts | Restores of points older than 35 days may take up to a full working day
- r6: Volumes and file systems follow one schedule and one retention rule, with no script per resource type
- r7: Points older than 35 days are stored at a lower rate than the first 35 days' points for the rest of the 7 years, and the day numbers for the change and for deletion are stated
- Decisive figures: 14 volumes + 2 file systems, 7 years, daily for 35 days, restore wait of a working day accepted.
- Why one best design: One cross-resource policy with a cold tier; native tools cover one type each. Only EBS and EFS used because AWS Backup cold storage is not offered for RDS (backup-feature-availability page).
- Services/options named or needed, and the lesson sentence: 'one policy, many services ... lifecycle can transition older recovery points to a cold storage tier'; 'at least 90 days'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s08

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Ashgrove Microscopy Library holds 300 TB of research images averaging 20 MB each. Some images are opened daily for months and then never again; others sit untouched for years and are suddenly requested when a paper is cited, and nobody can predict which. Every image must open in milliseconds whenever it is requested. The trustees have rejected any design whose monthly bill can jump because of retrieval charges or early-removal charges.
- Added constraints: No per-retrieval or early-removal charge may ever appear on the bill | The library has one part-time administrator, so there are no per-project tiering rules to maintain | All images stay in one Region
- r6: The monthly bill contains no retrieval or early-removal charge whichever images are opened in a month
- r7: Images untouched for long periods cost less to store than frequently opened ones, without anyone classifying the images
- Decisive figures: 300 TB, 20 MB objects, unpredictable access, milliseconds always, no retrieval or early-removal charges.
- Why one best design: Unpredictable access plus no retrieval charges leaves only the tier that moves data by observed access.
- Services/options named or needed, and the lesson sentence: 'unpredictable or changing access moves to S3 Intelligent-Tiering, which carries no retrieval fee in exchange for a small monitoring fee'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s09

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Quayside Clinical Trials must keep trial documents for 10 years and then delete them. Documents are read weekly for their first 30 days; from day 30 to day 90 they are read about once a month and must open in milliseconds; from day 90 to day 365 they are read a few times a year and a wait of up to 5 hours is fine; after a year they are read at most once a year and a wait of up to 12 hours is fine. The sponsor requires every stage to survive the loss of a whole data centre.
- Added constraints: Each stage must use the lowest-storage-cost option that meets its retrieval need | The trials office will not accept early-removal fees at any step | Deletion at the end of retention must happen without a person acting
- r6: Every stage has a stated day range and its retrieval time is checked against the scenario, and no object is charged an early-removal fee at any transition
- r7: Documents are deleted automatically at day 3,650 and every stage survives the loss of a whole data centre
- Decisive figures: stages: 0-30 weekly; 30-90 monthly in ms; 90-365 few per year, 5 h; 365+ yearly, 12 h; 10 years = day 3,650; data-centre loss survived.
- Why one best design: Day 30 Standard-IA (60 days clears the 30-day minimum; One Zone-IA out by the data-centre rule; Glacier Instant would breach its 90-day minimum), day 90 Flexible Retrieval (Standard 3-5 h), day 365 Deep Archive (Standard within 12 h), expire day 3,650.
- Services/options named or needed, and the lesson sentence: K10 minimums 30/90/180 days and retrieval times; S09 example schedule.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.1-s10

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Fenwick Geospatial has three data sets. The first is 500 TB of satellite tiles that batch jobs read through an object API, growing without a forecast. The second is a 2 TB team working directory that 8 Linux render servers must mount together as an ordinary folder, growing unpredictably. The third is a 200 GB database volume attached to one server that needs steady low-latency block access. Nothing at Fenwick runs on Windows, uses an HPC file system or depends on NetApp features, and Finance wants the lowest run-rate that meets every requirement.
- Added constraints: The platform team of two manages capacity for as few services as possible | Growth of the first two data sets must not need capacity planning | The database volume is sized to its measured need, not to a guess
- r6: Each data set lands on a storage service whose billing model matches its stated growth and access pattern
- r7: The number of distinct storage services used is the smallest that meets every stated access requirement
- Decisive figures: 500 TB object API; 2 TB POSIX dir mounted by 8 Linux servers, unpredictable growth; 200 GB single-server block; no Windows/HPC/NetApp.
- Why one best design: S3, EFS, EBS; FSx excluded by the stated absence of its engines.
- Services/options named or needed, and the lesson sentence: 'belongs on S3', 'Shared, POSIX-compliant file access ... belongs on EFS', 'single-instance database ... is EBS'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-storage-migration

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Dovecote Film Archive will retire its NAS array 60 days from now, after a one-off copy of 180 TB of masters from its NFS shares into cloud object storage; once the copy finishes the array is powered off. The studio's internet link is 1 Gbps and at least 700 Mbps of it is free at every hour of the day. Separately, a rights partner drops about 500 GB of files every week and will send them only over SFTP to an address Dovecote controls; today a server in the machine room, patched by the studio's one administrator, receives them.
- Added constraints: Finance funds no hardware for this project | The copy must be verified, and it must finish before the array is powered off at day 60 | The rights partner cannot change its SFTP client or the address it sends to
- r6: The 180 TB copy completes inside the 60 days at the 700 Mbps the scenario leaves free, and the record shows the days needed (about 24)
- r7: The partner's weekly files arrive with no studio-run server to patch
- Decisive figures: 180 TB with at least 700 Mbps free: 1,440,000 Gb / 0.7 Gbps = about 2.06M s = 23.8 days, under 60; partner SFTP 500 GB/week.
- Why one best design: The network copy fits the window, so no bulk-transfer device or terminal; the array is retired so not Storage Gateway; the SFTP partner is Transfer Family. Snow Family is not named.
- Services/options named or needed, and the lesson sentence: 'finish the migration and disconnect is DataSync'; 'external partners ... SFTP ... AWS Transfer Family'.
- constraint_reason: "Service unavailable or not disposable in a personal same-day lab" still holds (unchanged). No mismatch.

## de-outposts

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Kinloch Steelworks is rolling out a recipe-management application that commands furnace controllers on its plant network, and each command must be answered within 5 ms. Process recipes are classed as trade secrets and may not leave the building. The nearest AWS Region is over 400 km away with round trips near 40 ms, and no AWS-operated metro location is closer than 150 km. The plant's two platform engineers already manage everything else through AWS interfaces and will not run a second toolset.
- Added constraints: Recipes must stay on the plant's premises | One toolset must serve both the plant and the Regional workloads | The plant can give space and power to one rack-sized installation
- r6: The 5 ms controller limit is met with recipes never leaving the building, and the record shows why no AWS-operated location away from the plant can meet it
- r7: Plant workloads and Regional workloads are managed through the same interfaces, with no second toolset introduced
- Decisive figures: 5 ms vs 40 ms Region round trip; nearest metro location 150 km; recipes stay on premises; one toolset.
- Why one best design: Only hardware on the plant meets latency and residency with native AWS interfaces.
- Services/options named or needed, and the lesson sentence: 'if the workload must remain on-premises yet use native AWS APIs, Outposts is the direct fit'; Local Zones 'AWS-managed locations near end users, not your server room'.
- constraint_reason: "Service unavailable or not disposable in a personal same-day lab" still holds (unchanged). No mismatch.

## de-purchasing

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Marigold Animation Studio's platform has three compute needs. A web tier uses 40 vCPUs around the clock and has done so for 24 months, with every sign it will for at least 3 more years; half of its containers move to a serverless container service next year, and instance families change with each hardware generation. On top of that floor it adds up to 60 vCPUs for 4 hours a day when artists review shots, with no warning of the start. A nightly render job runs 6 hours on a fleet that saves its progress every 15 minutes and simply redoes the frames of any server it loses. The studio also runs a 2-week pilot of a new tool whose future is unknown.
- Added constraints: Finance wants the deepest discount on usage that has run steadily for 24 months and will last 3 more years | Nothing variable or of unknown future may be committed | The web tier and the pilot must never be interrupted
- r6: The long-term commitment is sized to the 40 vCPU steady floor, still applies after half of it moves to containers, and is not applied to the peak, the render job or the pilot
- r7: The render job loses no more than 15 minutes of progress per lost server, and the record shows why the web tier and the pilot are not exposed to the same risk
- Decisive figures: 40 vCPU floor for 24 months and 3 more years; half moves to containers; 60 vCPU 4 h unannounced peak; render job 15-minute checkpoints; 2-week pilot.
- Why one best design: Compute-wide commitment on the floor (it survives the move to containers), interruptible capacity for render, On-Demand for peak and pilot.
- Services/options named or needed, and the lesson sentence: 'Compute Savings Plans ... EC2, Fargate, and Lambda'; Spot 'two-minute interruption notice ... checkpointed'; 'On-Demand for burst and unknowns'.
- constraint_reason: "Service unavailable or not disposable in a personal same-day lab" still holds (unchanged). No mismatch.

## de-saa-4.2-s01

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Tern Harbour Logistics exposes three traffic flows. Its customer site and API share one domain, and requests for /api and /tracking must reach different server groups. A partner bank connects to a binary protocol on TCP port 8443 and allowlists exactly two fixed IP addresses that Tern Harbour must keep stable. Customs-clearance traffic must pass through a fleet of a vendor's virtual inspection appliances before it reaches the application, and that fleet must grow by adding appliances without reconfiguring the applications behind it. The company wants as few load balancers as will do the job.
- Added constraints: Finance will not fund one load balancer per URL path | The partner bank cannot change its allowlist or protocol | Inspection appliances are the vendor's virtual images and cannot be replaced
- r6: Each flow's requirement is met with a stated reason, and no flow uses a load balancer type that cannot meet it
- r7: The /api and /tracking paths are served through a single front door rather than one load balancer per path
- Decisive figures: three flows: path routing on one domain; TCP 8443 with two fixed IPs; appliance fleet; fewest balancers.
- Why one best design: One ALB, one NLB, one GWLB; none can stand in for another.
- Services/options named or needed, and the lesson sentence: ALB host/path routing, NLB 'static IP', GWLB 'virtual appliance insertion'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.2-s02

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Ebbfleet Shipping Brokers runs two workloads. Its quote API takes independent requests, varies between 20 and 900 requests per second during a day, and must stay available through spikes. Its rate-matching engine is one process holding a 96 GiB in-memory table on a Linux server; after any start it needs 25 minutes to rebuild the table, it is used only from 07:30 to 18:00 on weekdays, and brokers will wait at most 3 minutes from starting it in the morning to a usable engine. The engine cannot be split across servers.
- Added constraints: Finance does not want the engine billed for server time overnight or at weekends | The quote API must never need manual action to cope with a spike | The engine's table is not stored anywhere else and is expensive to rebuild
- r6: The engine is not billed for server time during its idle hours and is usable within 3 minutes of the 07:30 restart, without the 25-minute rebuild
- r7: The quote API's capacity follows its 20 to 900 requests-per-second swings with no staff action
- Decisive figures: API 20-900 rps independent requests; engine 96 GiB RAM, 25 min rebuild, 3 min tolerance, 07:30-18:00.
- Why one best design: Scale-out for the API; hibernation for the engine (a plain stop loses RAM and needs the 25-minute rebuild). 96 GiB is under the 150 GiB Linux limit (EC2 hibernation prerequisites page).
- Services/options named or needed, and the lesson sentence: 'Hibernation saves RAM to the EBS root volume ... you do not pay instance usage while stopped'; horizontal scaling with target tracking.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.2-s03

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Plumstead Photo Co-op operates three workloads. A resize step runs for about 300 ms whenever a member uploads a photo, is idle overnight, and receives bursts of a few thousand uploads after weekend events. A month-end book-layout job is packaged as a container, runs about 40 minutes once a night on five nights a month, and is idle otherwise. A print-routing service needs a vendor's kernel module and runs 24 hours a day at a steady load that has not changed in two years. The co-op's two engineers will not patch servers for the first two workloads.
- Added constraints: Nothing idle may be paid for on the first two workloads | The print-routing vendor requires control of the operating system | A long-term commitment is allowed only for load that is steady
- r6: The 40-minute layout job runs on a service whose maximum run time exceeds 40 minutes, with no host for the engineers to patch
- r7: Only the 24-hour print-routing service carries a long-term commitment; the two intermittent workloads are billed only while they run
- Decisive figures: 300 ms event function; 40-minute container job 5 nights/month; steady 24 h kernel-module service.
- Why one best design: Lambda, Fargate (40 minutes exceeds Lambda's 15), EC2 with commitment.
- Services/options named or needed, and the lesson sentence: 'Lambda ... up to 900 seconds (15 minutes)'; 'Use EC2 when you need full OS control ... continuously running workloads where commitments can lower cost'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.2-s04

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Gantry Insurance runs its claims portal in production and in four further copies for development, testing, staging and training. Every copy uses the same two-Availability-Zone layout at the same size, running 24 hours a day. Production must keep serving if one Availability Zone fails, with no manual action. The four non-production copies are used 10 hours on weekdays only, hold synthetic data, and the business accepts an outage of up to a full day in any of them. The finance chief wants the non-production run-rate at least 60 percent below today's.
- Added constraints: The production layout and its security controls are not to be weakened | Non-production copies may be unavailable for up to a full day | The non-production run-rate target is at least 60 percent below today's
- r6: Production keeps serving through the loss of one Availability Zone with no manual action
- r7: Non-production run-rate falls at least 60 percent below today's, with the change for each of the four copies stated and the saving worked out from the scenario's hours
- Decisive figures: prod two-AZ 24x7; four non-prod 10 h x 5 d = 50 of 168 h (70 percent off by hours alone); a day's outage tolerated; target at least 60 percent.
- Why one best design: Production stays two-AZ; non-production becomes single-AZ and scheduled off.
- Services/options named or needed, and the lesson sentence: 'Production ... at least two AZs'; 'Non-production ... lower redundancy ... strict schedules, and automatic teardown'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## de-saa-4.2-s05

- Old scenario: template text ("Design a solution that demonstrates skill: ..." or "You must design a solution addressing: ...").
- New scenario: Corbel Audio Analytics runs two services continuously on general-purpose servers that all provide 4 GiB of memory per vCPU. The transcription service uses 16 servers of 8 vCPUs and 32 GiB, and monitoring shows its CPU averaging 88 percent while memory averages 18 percent. The speaker-index service uses 4 servers of 16 vCPUs and 64 GiB, with CPU averaging 12 percent and memory at 90 percent. The company wants the run-rate of both services reduced without slowing either.
- Added constraints: Neither service may become slower | No application code changes are planned | Both services stay on the CPU architecture they run on today
- r6: Each service's server family follows the resource that monitoring shows is its limit, and the record cites the 88 percent CPU and 90 percent memory figures
- r7: New fleet sizes are derived from the measured peaks, with their resulting counts stated, rather than copied from today's 16 and 4 servers
- Decisive figures: transcription: CPU 88 percent, memory 18 percent; speaker-index: CPU 12 percent, memory 90 percent.
- Why one best design: Compute-optimized for the first, memory-optimized for the second, chosen by bottleneck.
- Services/options named or needed, and the lesson sentence: 'CPU is consistently high while memory is moderate, compute-optimized ... memory pressure dominates, memory-optimized'.
- constraint_reason: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" still holds (unchanged). No mismatch.

## Lesson additions requested

None. Every named or needed service and option is taught in the lesson for its objectives (regex check, case-insensitive, backticks stripped, whitespace tolerant). The only term not found was 'kernel' in de-saa-4.2-s03, which is scenario context for the OS-control requirement taught as 'full OS control'.

Notes for reviewers: (a) de-saa-4.1-s05 and -s09 depend on the class minimum durations in lesson 4.1 K10; (b) de-saa-4.1-s06 deliberately uses block volumes and file systems only, since AWS Backup cold storage does not cover RDS; (c) the retired/closed list was checked: no Snow Family, FSx File Gateway or other closed service is named; de-outposts is a current service that cannot be provisioned in a personal lab, which is what its constraint_reason covers.

## Script outputs

- content_lint.py: PASS (questions 429, labs 21 + 21, lessons 23).
- Scan of all 60 exercises (final run, see chat): duplicate 6-word openings none; duplicate organisation names (first two words) none at time of writing. Other writers were still editing.

## Fix pass

Applied AWS-DE3-001 to 012 and TEACHER-DE3-001 to 004, 008, 009 as they touch the 16 files of 4.1 and 4.2. Merged fields are marked in the finding id with the reason in the Note.

### AWS-DE3-001, de-saa-4.1-s06, scenario
- Old: The insurer requires every recovery point to be held for 7 years: daily points for the first 35 days, after which restores are needed only a few times a year and may wait up to a full working day.
- New: The insurer requires every recovery point to be held for 7 years: one point a month, restored often in its first 35 days and after that only a few times a year, when a wait of up to four days is acceptable.

### AWS-DE3-001, de-saa-4.1-s06, scenario
- Old: cost well below the price of the first 35 days' points
- New: cost well below the price of points in their first 35 days

### AWS-DE3-001, de-saa-4.1-s06, constraint 7
- Old: Restores of points older than 35 days may take up to a full working day
- New: Restores of points older than 35 days may take up to four days

### AWS-DE3-002 (used instead of TEACHER-DE3-003), de-saa-4.1-s04, scenario
- Old: one 1 TB block volume holding 800 GB today; a bulk catalogue import of up to 150 GB, arriving about weekly,
- New: one 1,000 GiB block volume holding 900 GiB today; a bulk catalogue import of up to 200 GiB, arriving about weekly,
- Note: Both fix the 800+150 < 1 TB arithmetic. AWS text also fixes units and makes the volume really overflow (900+200=1,100 GiB > 1,000 GiB); Teacher text (900 GB) leaves the import size unchanged and is covered by it.

### AWS-DE3-003, de-saa-4.1-s04, scenario
- Old: Nobody is on call overnight.
- New: The publishing database is self-managed software on that one server and stays there. Nobody is on call overnight.
- Note: Placed before the on-call sentence, not after "block volume", so it reads naturally after the volume sentence.

### AWS-DE3-002, de-saa-4.1-s04, r7
- Old: A 150 GB import at 3 a.m. completes without publishing stopping and without a person acting
- New: A 200 GiB import at 3 a.m. completes without publishing stopping and without a person acting

### TEACHER-DE3-004, de-saa-4.1-s04, r6
- Old: For each of the three stores the record states whether growth needs any design work and gives the reason from the scenario
- New: For each of the three stores the record says how its capacity grows and why, using the scenario's figures

### AWS-DE3-004, de-saa-4.1-s02, r6
- Old: The initial volume is no larger than 1.5 TB, derived from today's 1.1 TB and 90 days of growth at 40 GB a month, with the margin stated
- New: The initial volume is between 1.22 TB (today's 1.1 TB plus 90 days at 40 GB a month) and 1.5 TB, with any rounding or margin stated

### AWS-DE3-005, de-saa-4.1-s05, constraint 5
- Old: Scans older than 30 days must cost less to store than they do today
- New: Scans older than 30 days must be held at the lowest storage cost that still lets a clerk open one in under a second

### AWS-DE3-005 (used instead of TEACHER-DE3-002), de-saa-4.1-s05, r6
- Old: Scans older than 30 days sit on the option with the lowest storage cost that still opens in under a second and whose minimum storage period the 7-year retention clears, while thumbnail storage and request cost does not rise
- New: Scans older than 30 days are held at the lowest storage cost that still opens in under a second, the record shows no scan is charged an early-removal fee under the 7-year retention, and thumbnail storage and request cost does not rise
- Note: Both moved the selection rule out of r6. The Teacher's text says only 'costs less than today', which still admits two classes; with 'lowest' moved to constraint 5 (AWS) the technical text is determinate and keeps the Teacher's no-giveaway and no-early-fee intent.

### AWS-DE3-006, de-saa-4.1-s05, scenario
- Old: the superseded copies are never read after 60 days
- New: the superseded copies are never read more than 60 days after being replaced

### AWS-DE3-006, de-saa-4.1-s05, r7
- Old: Superseded scan copies are gone by day 60, broken upload leftovers within 7 days and scans at the 7-year mark, each with the day number stated
- New: Superseded scan copies are gone 60 days after they are replaced, broken upload leftovers within 7 days and scans at the 7-year mark, each with the day number stated

### AWS-DE3-007, de-saa-4.1-s09, scenario
- Old: trial documents for 10 years and then delete them.
- New: trial documents of about 3 MB each for 10 years (count 3,650 days) and then delete them.

### AWS-DE3-008, de-saa-4.1-s10, r7
- Old: The number of distinct storage services used is the smallest that meets every stated access requirement
- New: No data set is placed on a service priced for a feature it does not need (for example, a managed file-system product with no Windows, HPC or NetApp requirement), and the record states the number of services used and why

### TEACHER-DE3-008, de-storage-migration, scenario
- Old: to an address Dovecote controls
- New: to a hostname in Dovecote's own domain

### TEACHER-DE3-008, de-storage-migration, r6
- Old: The 180 TB copy completes inside the 60 days at the 700 Mbps the scenario leaves free, and the record shows the days needed (about 24)
- New: The 180 TB copy completes inside the 60 days at the 700 Mbps the scenario leaves free, and the record shows the days needed

### AWS-DE3-009, de-purchasing, constraint 5
- Old: Finance wants the deepest discount on usage that has run steadily for 24 months and will last 3 more years
- New: Finance wants the steady 40 vCPUs discounted for the next 3 years and will not re-buy the commitment when its mix of containers and instance families changes

### AWS-DE3-009, de-purchasing, r6
- Old: The long-term commitment is sized to the 40 vCPU steady floor, still applies after half of it moves to containers, and is not applied to the peak, the render job or the pilot
- New: The long-term commitment is sized to the steady floor's hourly spend (40 vCPUs), still applies after half of it moves to containers, and is not applied to the peak, the render job or the pilot

### AWS-DE3-010, de-saa-4.2-s02, scenario
- Old: it is used only from 07:30 to 18:00 on weekdays, and brokers will wait at most 3 minutes from starting it in the morning to a usable engine.
- New: brokers open it at unpredictable times on weekdays between 07:30 and 18:00, sometimes with hours between uses, and never overnight or at weekends; each time they will wait at most 3 minutes from asking for it to a usable engine.

### AWS-DE3-010, de-saa-4.2-s02, constraint 5
- Old: Finance does not want the engine billed for server time overnight or at weekends
- New: Finance does not want the engine billed for server time while no broker is using it, including overnight and weekends

### AWS-DE3-010, de-saa-4.2-s02, constraint 7
- Old: The engine's table is not stored anywhere else and is expensive to rebuild
- New: The engine's table can be rebuilt only by re-reading every source feed, which takes 25 minutes

### AWS-DE3-010 + TEACHER-DE3-009 merged, de-saa-4.2-s02, r6
- Old: The engine is not billed for server time during its idle hours and is usable within 3 minutes of the 07:30 restart, without the 25-minute rebuild
- New: The engine is not billed for server time while idle and is usable at any start without the 25-minute rebuild, and the record says how the 3-minute start limit will be confirmed, including the root-volume throughput it assumes
- Note: AWS text fixes the determinacy (any start, not just 07:30, which removes the scheduled-start design); Teacher text removes the over-claim that 3 minutes is guaranteed. Merged: AWS scope plus the Teacher's 'says how the limit will be confirmed'. The scenario sentence before this one ('after any start it needs 25 minutes') is unchanged.

### AWS-DE3-011, de-saa-4.2-s04, scenario
- Old: The finance chief wants the non-production run-rate at least 60 percent below today's.
- New: The finance chief wants the non-production run-rate at least 75 percent below today's; count run-rate as proportional to server-hours.

### AWS-DE3-011, de-saa-4.2-s04, constraint 7
- Old: The non-production run-rate target is at least 60 percent below today's
- New: The non-production run-rate target is at least 75 percent below today's

### AWS-DE3-011, de-saa-4.2-s04, r7
- Old: Non-production run-rate falls at least 60 percent below today's, with the change for each of the four copies stated and the saving worked out from the scenario's hours
- New: Non-production run-rate falls at least 75 percent below today's, with the change for each of the four copies stated and the saving worked out from the scenario's hours

### TEACHER-DE3-001 (used instead of AWS-DE3-012), de-saa-4.2-s05, r7
- Old: New fleet sizes are derived from the measured peaks, with their resulting counts stated, rather than copied from today's 16 and 4 servers
- New: Each new fleet keeps at least the vCPUs and the memory that its stated utilisation requires, with the vCPU and GiB totals before and after stated for both services
- Note: AWS text fixed the same misleading '16 and 4' wording but printed the answers to the learner's arithmetic (about 113 of 128 vCPUs, about 230 of 256 GiB), which the fix-pass rule forbids; the Teacher's text asks for the same derivation without the numbers and is determinate.

### Re-checks

- content_lint.py: PASS.
- Teach-before-test on changed text: see chat/regex run; the only service-like terms in changed text (Elastic Volumes not named; root volume and hibernation-related wording; 'managed file-system product'; 'hourly spend' of a commitment; 'backoff' not used in my files) are taught in lessons 4.1/4.2.
