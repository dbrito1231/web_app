# D6 Part A pricing claims (read 2026-09-29)

Method (second pass): the rate tables of aws.amazon.com pricing pages are embedded iframes from https://c0.b0.p.awsstatic.com/#/<service>/<plan>. After scrolling a page, the iframe src was read; the iframe URL was opened in the browser tool, the Region button was set to US East (N. Virginia) and its label was read back. Pages without such an iframe (VPC, EFS, EBS, ELB, WAF, CloudWatch, RDS pricing) were read as curl text; their page-level tables never rendered. Every page fetched with `curl -sL` and stripped to text with Python. The region price tables are loaded by JavaScript; the built-in browser (VPC and EC2 pages) rendered them empty, so those rates could not be read as page text. Rates below are static page text (tables, worked examples, footnotes). No Price List JSON, no API, no calculator, no credentials. Rows marked "worked example; region not named" come from a pricing example that does not name the Region. Rows marked NOT VERIFIED were not read; the labs keep their earlier figure and say so.

Rules used everywhere: (1) same-hour keeps every resource running for the whole `estimatedMinutes`, including tasks that exit on their own; this is deliberately conservative; (2) hours are billed in full where the page says so (NAT, ALB), fractional otherwise; (3) month = 720 h for prorating GB-month and per-month fees; (4) data transfer, LCU, WAF request, log and per-GB NAT data charges are excluded; (5) rounded up to the cent.

## Claim table

| Service | Resource / size | Rate | URL | Verbatim quote (<=20 words) | Method | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VPC | Public IPv4 address, in use | $0.005/h | https://aws.amazon.com/vpc/pricing/ | "Hourly charge for In-use Public IPv4 Address $0.005" | curl (static text) | verified |
| VPC | Public IPv4 billing granularity | one-second increments, 60 s min | https://aws.amazon.com/vpc/pricing/ | "calculated in one-second increments, with a minimum of 60 seconds" | curl | verified |
| VPC | NAT gateway hourly | $0.045/h | https://aws.amazon.com/vpc/pricing/ | "For this region, the rate is $0.045 per hour." | curl; browser (page table empty, no widget iframe) | example is US East (Ohio); NOT verified for us-east-1 |
| VPC | NAT gateway partial hour | full hour | https://aws.amazon.com/vpc/pricing/ | "Each partial NAT Gateway-hour consumed is billed as a full hour." | curl | verified |
| EC2 | t3.micro Linux On-Demand, US East (N. Virginia) | $0.0104/h | https://c0.b0.p.awsstatic.com/#/ec2/on-demand-plan (iframe of https://aws.amazon.com/ec2/pricing/on-demand/) | row "t3.micro $0.0104000000" with Region button "US East (N. Virginia)" | widget (browser) | verified us-east-1 |
| EC2 | t3.small Linux On-Demand, US East (N. Virginia) | $0.0208/h | same widget | row "t3.small $0.0208000000" | widget (browser) | verified us-east-1 |
| EC2 | t3.medium Linux On-Demand, US East (N. Virginia) | $0.0416/h | same widget | row "t3.medium $0.0416000000" (first pass had $0.0418 from the T3 marketing page, which differs) | widget (browser) | verified us-east-1 |
| RDS PostgreSQL | db.t3.micro Single-AZ On-Demand, US East (N. Virginia) | $0.0180/h | https://c0.b0.p.awsstatic.com/#/rds/postgresql-reserved-instances-plan (iframe of https://aws.amazon.com/rds/postgresql/pricing/) | row "db.t3.micro | $54.00 | $4.53 | $0.012 | 31% | $0.0180" (On-Demand rate column), deployment Single-AZ | widget (browser) | verified us-east-1 |
| RDS PostgreSQL | io1 storage, US East (N. Virginia) example | $0.125/GB-month | https://aws.amazon.com/rds/postgresql/pricing/ | "in US East (N. Virginia), an io1 Dedicated Log Volume ... would cost $0.125 x 1024 GiB" | curl | verified for io1 only; used as an upper bound for gp2/gp3 |
| RDS PostgreSQL | gp2 / gp3 storage per GB-month | n/a | https://aws.amazon.com/rds/postgresql/pricing/ | price token only; the page has no storage widget iframe | curl; browser | NOT VERIFIED on 2026-09-29 |
| ElastiCache | cache.t3.micro Redis On-Demand, US East (N. Virginia) | $0.0170/h | https://c0.b0.p.awsstatic.com/#/elasticache/reserved-instances-plan (iframe of https://aws.amazon.com/elasticache/pricing/) | row "cache.t3.micro $0.00 $8.76 $0.012000 29% $0.0170 Redis" (On-Demand rate column) | widget (browser) | verified us-east-1 |
| ElastiCache | cache.t3.micro Valkey On-Demand (comparison) | $0.0136/h | same widget | row "cache.t3.micro ... $0.0136 Valkey" | widget (browser) | verified us-east-1; not used (labs create Redis) |
| ElastiCache | partial node-hour | full hour | https://aws.amazon.com/elasticache/pricing/ | "Each partial node-hour consumed will be billed as a full hour." | curl | verified |
| EFS | Standard storage GB-month | n/a | https://aws.amazon.com/efs/pricing/ | price token only; no widget iframe on the page | curl; browser | NOT VERIFIED on 2026-09-29 |
| EBS | gp3 storage | $0.08/GB-month | https://aws.amazon.com/ebs/pricing/ | "General Purpose SSD (gp3) - Storage $0.08/GB-month" | curl; reviewer read the rendered page with Region read back as US East (N. Virginia) | verified N. Virginia (AWS-PA-003) |
| EBS | Snapshot Standard storage | $0.05/GB-month | https://aws.amazon.com/ebs/pricing/ | "Standard $0.05/GB-month" | curl; reviewer rendered page (N. Virginia) | verified N. Virginia (AWS-PA-003) |
| EBS | gp2 storage (note only) | $0.10/GB-month | https://aws.amazon.com/ebs/pricing/ | "General Purpose SSD (gp2) Volumes $0.10 per GB-month of provisioned storage" | reviewer rendered page (N. Virginia) | verified; not used by these labs |
| EBS | billing granularity | per second, 60 s minimum | https://aws.amazon.com/ebs/pricing/ | "billed in per-second increments, with a 60-second minimum" | reviewer rendered page | verified |
| EKS | create-nodegroup defaults | instance type t3.medium; root disk 20 GiB | https://docs.aws.amazon.com/eks/latest/APIReference/API_CreateNodegroup.html | "then `t3.medium` is used, by default"; "default disk size is 20 GiB for Linux" | AWS docs MCP | verified; default desired size not documented on that page or NodegroupScalingConfig |
| ELB | ALB hourly | $0.0225/h | https://aws.amazon.com/elasticloadbalancing/pricing/ | "using pricing in the US-East-1 Region as follows" then "Adding the hourly charge of $0.0225, the total Application Load Balancer costs are" | curl (text); reviewer re-read | verified us-east-1 (example names US-East-1; AWS-PA-003) |
| ELB | ALB partial hour | full hour | https://aws.amazon.com/elasticloadbalancing/pricing/ | "Each partial Application Load Balancer hour used is billed as a full hour." | curl | verified |
| WAF | Web ACL | $5.00/month prorated hourly | https://aws.amazon.com/waf/pricing/ | "Web ACL charges = $5.00 * 1 = $5.00"; "Monthly fees are prorated hourly." | curl | worked example; NOT verified for us-east-1 ("Pricing may vary across AWS Regions") |
| WAF | Managed rule group / rule | $1.00/month prorated hourly | https://aws.amazon.com/waf/pricing/ | "$1.00 per month (prorated hourly) for each rule group or each managed rule group" | curl | text verified; NOT verified for us-east-1 |
| WAF | Requests | $0.60/million | https://aws.amazon.com/waf/pricing/ | "Request charges = $0.60/million * 10 million = $6.00" | curl | excluded from figures |
| Fargate | Linux/x86 vCPU, memory (N. Virginia) | $0.000011244/vCPU-s; $0.000001235/GB-s | https://aws.amazon.com/fargate/pricing/ | "Linux/X86 pricing for US East (N. Virginia) Region where CPU cost: $0.000011244 per vCPU second" | curl | verified |
| Fargate | Billing granularity | per second, 1-minute min | https://aws.amazon.com/fargate/pricing/ | "Pricing is calculated per second with a 1-minute minimum." | curl | verified |
| EKS | Cluster, standard support | $0.10/cluster-hour | https://aws.amazon.com/eks/pricing/ | "You pay $0.10 per hour for each Amazon EKS cluster that you create." | curl | verified |
| CloudWatch | Standard alarm | $0.10/alarm metric/month | https://aws.amazon.com/cloudwatch/pricing/ | "Four standard resolution alarms = $0.10 per alarm metric * 4 = $0.40 per month" | curl | worked example ("US East"); NOT verified for us-east-1 |
| RDS PostgreSQL | db.t3.micro instance-hour; storage | n/a | https://aws.amazon.com/rds/postgresql/pricing/ | price tables render empty ({priceOf!...} tokens in source) | curl | NOT VERIFIED on 2026-09-29 |
| EFS | Standard storage GB-month | n/a | https://aws.amazon.com/efs/pricing/ | "{priceOf!efs/...}" token only | curl | NOT VERIFIED on 2026-09-29 |
| ElastiCache | cache.t3.micro node-hour | n/a | https://aws.amazon.com/elasticache/pricing/ | no small-node rate in static text | curl | NOT VERIFIED on 2026-09-29 |

Counts (after fix pass): verified in us-east-1 = t3.micro, t3.small, t3.medium, RDS db.t3.micro, ElastiCache cache.t3.micro (Redis and Valkey), Fargate vCPU/memory, ALB, EBS gp3 and snapshot; page-stated flat rates = public IPv4, EKS; not verified for us-east-1 (worked example, Ohio, or table unreadable) = NAT, WAF web ACL/rule, CloudWatch alarm, RDS gp2/gp3, EFS.

## Per lab

### gl-06 (75 min)

Resources: 1 NAT gateway; 1 Elastic IP (public IPv4) on the NAT; VPC, subnets, IGW, route tables free.

Same-hour arithmetic (qty x rate/h x hours):
- NAT gateway (billed in full hours): 1 x 0.045 x 2 h = 0.09000
- public IPv4 (NAT Elastic IP): 1 x 0.005 x 1.25 h = 0.00625
- Sum 0.09625 -> rounded up 0.10
24 h arithmetic:
- NAT gateway (billed in full hours): 1 x 0.045 x 24 h = 1.08000
- public IPv4 (NAT Elastic IP): 1 x 0.005 x 24 h = 0.12000
- Sum 1.20000 -> rounded up 1.20

Old -> new: same-hour 0.05 -> 0.10; forgotten 24 h 1.2 -> 1.20

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 NAT gateway $0.045/h (billed in full hours), 1 public IPv4 for its Elastic IP $0.005/h. This run ≈ $0.10; forgotten 24 h ≈ $1.20 (at least; data transfer and NAT per-GB processing not included). The NAT gateway rate is not verified for us-east-1; check its pricing page before you run. Re-check current pricing before you run.

stopChargesPanel:

> Delete NAT gateway, wait deleted, release EIP, then tear down VPC components. Forgotten 24 h: at least $1.20 (see the cost basis).

### gl-07 (120 min)

Resources: 1 t3.micro; 1 auto-assigned public IPv4 (default subnet); 8 GB gp3 root (AMI default); 8 GB gp3 data volume; 1 snapshot (<= 8 GB).

Same-hour arithmetic (qty x rate/h x hours):
- t3.micro: 1 x 0.0104 x 2 h = 0.02080
- public IPv4 (default subnet): 1 x 0.005 x 2 h = 0.01000
- 8 GB gp3 root volume: 1 x 0.000888889 x 2 h = 0.00178
- 8 GB gp3 data volume: 1 x 0.000888889 x 2 h = 0.00178
- EBS snapshot (upper bound 8 GB): 1 x 0.000555556 x 2 h = 0.00111
- Sum 0.03547 -> rounded up 0.04
24 h arithmetic:
- t3.micro: 1 x 0.0104 x 24 h = 0.24960
- public IPv4 (default subnet): 1 x 0.005 x 24 h = 0.12000
- 8 GB gp3 root volume: 1 x 0.000888889 x 24 h = 0.02133
- 8 GB gp3 data volume: 1 x 0.000888889 x 24 h = 0.02133
- EBS snapshot (upper bound 8 GB): 1 x 0.000555556 x 24 h = 0.01333
- Sum 0.42560 -> rounded up 0.43

Old -> new: same-hour 0.03 -> 0.04; forgotten 24 h 0.72 -> 0.43

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 t3.micro $0.0104/h, 1 public IPv4 $0.005/h, 2 x 8 GB gp3 volumes (root and data) $0.08/GB-month, 1 snapshot up to 8 GB $0.05/GB-month. This run ≈ $0.04; forgotten 24 h ≈ $0.43 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Terminate the instance and wait, detach and delete the gp3 volume, then delete the snapshot tagged gl-07. Forgotten 24 h: at least $0.43 (see the cost basis).

### gl-08 (90 min)

Resources: 1 ALB in 2 subnets (2 public IPv4); 1 t3.micro with no public IPv4 (create-subnet does not auto-assign; run-instances sets none); 8 GB gp3 root; target group, SG, VPC free.

Same-hour arithmetic (qty x rate/h x hours):
- ALB (billed in full hours): 1 x 0.0225 x 2 h = 0.04500
- public IPv4 on ALB (one per AZ subnet): 2 x 0.005 x 1.5 h = 0.01500
- t3.micro target: 1 x 0.0104 x 1.5 h = 0.01560
- 8 GB gp3 root volume: 1 x 0.000888889 x 1.5 h = 0.00133
- Sum 0.07693 -> rounded up 0.08
24 h arithmetic:
- ALB (billed in full hours): 1 x 0.0225 x 24 h = 0.54000
- public IPv4 on ALB (one per AZ subnet): 2 x 0.005 x 24 h = 0.24000
- t3.micro target: 1 x 0.0104 x 24 h = 0.24960
- 8 GB gp3 root volume: 1 x 0.000888889 x 24 h = 0.02133
- Sum 1.05093 -> rounded up 1.06

Old -> new: same-hour 0.04 -> 0.08; forgotten 24 h 0.96 -> 1.06

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 Application Load Balancer $0.0225/h (billed in full hours) with 2 public IPv4 (one per subnet) $0.005/h each, 1 t3.micro $0.0104/h, 8 GB gp3 root volume $0.08/GB-month. This run ≈ $0.08; forgotten 24 h ≈ $1.06 (at least; LCU (traffic) charges and data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Delete the load balancer (this removes its listener) and wait, delete the target group, terminate the EC2 instance and wait, then disassociate and delete the route table, delete both subnets, detach and delete the internet gateway, and delete the security group and VPC. Forgotten 24 h: at least $1.06 (see the cost basis).

### gl-09 (75 min)

Resources: ASG desired 1: 1 t3.micro, auto-assigned public IPv4 (default subnet), 8 GB gp3 root; launch template and ASG free.

Same-hour arithmetic (qty x rate/h x hours):
- t3.micro: 1 x 0.0104 x 1.25 h = 0.01300
- public IPv4 (default subnet): 1 x 0.005 x 1.25 h = 0.00625
- 8 GB gp3 root volume: 1 x 0.000888889 x 1.25 h = 0.00111
- Sum 0.02036 -> rounded up 0.03
24 h arithmetic:
- t3.micro: 1 x 0.0104 x 24 h = 0.24960
- public IPv4 (default subnet): 1 x 0.005 x 24 h = 0.12000
- 8 GB gp3 root volume: 1 x 0.000888889 x 24 h = 0.02133
- Sum 0.39093 -> rounded up 0.40

Old -> new: same-hour 0.03 -> 0.03; forgotten 24 h 0.72 -> 0.40

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 t3.micro $0.0104/h, 1 public IPv4 $0.005/h, 8 GB gp3 root volume $0.08/GB-month (the Auto Scaling group itself is free). This run ≈ $0.03; forgotten 24 h ≈ $0.40 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Scale the ASG to 0 and force-delete it, wait until it is gone (its instances terminate with it), then delete the launch template. This lab uses the default VPC and creates no security group or subnet. Forgotten 24 h: at least $0.40 (see the cost basis).

### gl-14 (120 min)

Resources: 1 RDS PostgreSQL db.t3.micro single-AZ, 20 GB storage, 1-day backup retention, not publicly accessible; DB subnet group free. Instance rate verified; storage priced at the io1 upper bound.

Same-hour arithmetic (qty x rate/h x hours):
- RDS db.t3.micro Single-AZ (billed in full hours): 1 x 0.018 x 2 h = 0.03600
- 20 GB storage at io1 upper-bound rate: 1 x 0.00347222 x 2 h = 0.00694
- Sum 0.04294 -> rounded up 0.05
24 h arithmetic:
- RDS db.t3.micro Single-AZ (billed in full hours): 1 x 0.018 x 24 h = 0.43200
- 20 GB storage at io1 upper-bound rate: 1 x 0.00347222 x 24 h = 0.08333
- Sum 0.51533 -> rounded up 0.52

Old -> new: same-hour 0.5 -> 0.05; forgotten 24 h 12.0 -> 0.52

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 RDS db.t3.micro Single-AZ $0.018/h, 20 GB storage (no public IPv4). This run ≈ $0.05; forgotten 24 h ≈ $0.52. Storage is priced at the higher io1 rate because the gp2/gp3 rate was not read, so real cost is likely slightly lower. Not included: data transfer. Re-check pricing before you run.

stopChargesPanel:

> Delete the DB instance without a final snapshot, wait until it is deleted, then delete the DB subnet group. This lab uses the default VPC security group. RDS bills every hour until deleted. Forgotten 24 h ≈ $0.52 (see the cost basis; check current pricing).

### gl-18 (90 min)

Resources: 1 Fargate task 0.25 vCPU / 0.5 GB with public IPv4 (assignPublicIp ENABLED); cluster, task definition, IAM role free; the container exits on its own.

Same-hour arithmetic (qty x rate/h x hours):
- Fargate 0.25 vCPU: 1 x 0.0101196 x 1.5 h = 0.01518
- Fargate 0.5 GB memory: 1 x 0.002223 x 1.5 h = 0.00333
- public IPv4 on task: 1 x 0.005 x 1.5 h = 0.00750
- Sum 0.02601 -> rounded up 0.03
24 h arithmetic:
- Fargate 0.25 vCPU: 1 x 0.0101196 x 24 h = 0.24287
- Fargate 0.5 GB memory: 1 x 0.002223 x 24 h = 0.05335
- public IPv4 on task: 1 x 0.005 x 24 h = 0.12000
- Sum 0.41622 -> rounded up 0.42

Old -> new: same-hour 0.2 -> 0.03; forgotten 24 h 4.8 -> 0.42

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 Fargate task: 0.25 vCPU at $0.0405 per vCPU-hour + 0.5 GB at $0.00445 per GB-hour ≈ $0.0124/h, plus 1 public IPv4 $0.005/h. This run ≈ $0.03; forgotten 24 h ≈ $0.42 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Stop tasks, delete service if any, deregister task defs, delete cluster. Forgotten 24 h: at least $0.42 (see the cost basis).

### gl-19 (120 min)

Resources: 1 EKS cluster on standard support, no nodes; 2 subnets; IAM role free.

Same-hour arithmetic (qty x rate/h x hours):
- EKS control plane (standard support): 1 x 0.1 x 2 h = 0.20000
- Sum 0.20000 -> rounded up 0.20
24 h arithmetic:
- EKS control plane (standard support): 1 x 0.1 x 24 h = 2.40000
- Sum 2.40000 -> rounded up 2.40

Old -> new: same-hour 0.2 -> 0.20; forgotten 24 h 4.8 -> 2.40

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): EKS control plane $0.10/cluster-hour (no nodes). This run ≈ $0.20; forgotten 24 h ≈ $2.40 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Delete the cluster and wait (EKS removes the cluster security group and network interfaces it created), then the IAM role; control plane bills hourly. Forgotten 24 h: at least $2.40 (see the cost basis).

### gl-21 (120 min)

Resources: 1 ElastiCache Redis cache.t3.micro, 1 node; subnet group free.

Same-hour arithmetic (qty x rate/h x hours):
- ElastiCache cache.t3.micro Redis (billed in full hours): 1 x 0.017 x 2 h = 0.03400
- Sum 0.03400 -> rounded up 0.04
24 h arithmetic:
- ElastiCache cache.t3.micro Redis (billed in full hours): 1 x 0.017 x 24 h = 0.40800
- Sum 0.40800 -> rounded up 0.41

Old -> new: same-hour 0.2 -> 0.04; forgotten 24 h 4.8 -> 0.41

beforeYouStart (replaced generic item):

> Cost basis (us-east-1, priced 2026-09-29): 1 ElastiCache cache.t3.micro (Redis) node $0.017/h, billed in full hours (no public IPv4). This run ≈ $0.04; forgotten 24 h ≈ $0.41 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Delete the cache cluster, wait until it is deleted, then delete the cache subnet group; ElastiCache is hourly. Forgotten 24 h: at least $0.41 (see the cost basis).

### ul-06 (75 min)

Resources: Same as gl-06 from its own criteria: 1 NAT gateway, 1 Elastic IP associated only with the NAT.

Same-hour arithmetic (qty x rate/h x hours):
- NAT gateway (billed in full hours): 1 x 0.045 x 2 h = 0.09000
- public IPv4 (NAT Elastic IP): 1 x 0.005 x 1.25 h = 0.00625
- Sum 0.09625 -> rounded up 0.10
24 h arithmetic:
- NAT gateway (billed in full hours): 1 x 0.045 x 24 h = 1.08000
- public IPv4 (NAT Elastic IP): 1 x 0.005 x 24 h = 0.12000
- Sum 1.20000 -> rounded up 1.20

Old -> new: same-hour 0.05 -> 0.10; forgotten 24 h 1.2 -> 1.20

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): 1 NAT gateway $0.045/h (billed in full hours), 1 public IPv4 for its Elastic IP $0.005/h. This run ≈ $0.10; forgotten 24 h ≈ $1.20 (at least; data transfer and NAT per-GB processing not included). The NAT gateway rate is not verified for us-east-1; check its pricing page before you run. Re-check current pricing before you run.

stopChargesPanel:

> Delete the NAT gateway and wait until it is deleted, release the Elastic IP, then remove both route tables, both subnets, the IGW and the VPC for ul-06. Forgotten 24 h: at least $1.20 (see the cost basis).

### ul-07 (120 min)

Resources: 1 EC2 instance (type not stated, t3.micro assumed); 1 public IPv4; 8 GB gp3 root; 1 encrypted EFS file system with 1 mount target and a test file (EFS rate not verified).

Same-hour arithmetic (qty x rate/h x hours):
- t3.micro: 1 x 0.0104 x 2 h = 0.02080
- public IPv4 (default subnet): 1 x 0.005 x 2 h = 0.01000
- 8 GB gp3 root volume: 1 x 0.000888889 x 2 h = 0.00178
- Sum 0.03258 -> rounded up 0.04
24 h arithmetic:
- t3.micro: 1 x 0.0104 x 24 h = 0.24960
- public IPv4 (default subnet): 1 x 0.005 x 24 h = 0.12000
- 8 GB gp3 root volume: 1 x 0.000888889 x 24 h = 0.02133
- Sum 0.39093 -> rounded up 0.40; kept at 0.72 because EFS storage is unverified (max of earlier and computed)

Old -> new: same-hour 0.03 -> 0.04; forgotten 24 h 0.72 -> 0.72

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): t3.micro $0.0104/h (smallest assumed), 1 public IPv4 $0.005/h, 8 GB gp3 root, plus EFS storage. The EFS rate was not read on 2026-09-29, so check the EFS pricing page before you run. This run ≈ $0.04 (EFS not included); forgotten 24 h ≈ $0.72, a cautious figure, not a calculated one (the parts we could price come to about $0.39). Not included: data transfer.

stopChargesPanel:

> Unmount EFS on the instance, delete the mount targets and wait until none remain, delete the EFS file system, terminate the EC2 instance, then delete the mount-target SG and the instance SG for ul-07. Forgotten 24 h ≈ $0.72 (cautious, not calculated; see the cost basis).

### ul-08 (90 min)

Resources: gl-08 pattern (ALB in 2 AZs, t3.micro assumed) plus 1 WAF web ACL with 1 managed rule group (AWSManagedRulesCommonRuleSet).

Same-hour arithmetic (qty x rate/h x hours):
- ALB (billed in full hours): 1 x 0.0225 x 2 h = 0.04500
- public IPv4 on ALB (one per AZ subnet): 2 x 0.005 x 1.5 h = 0.01500
- t3.micro target: 1 x 0.0104 x 1.5 h = 0.01560
- 8 GB gp3 root volume: 1 x 0.000888889 x 1.5 h = 0.00133
- WAF web ACL ($5/month, partial hour billed as full hour): 1 x 0.00694444 x 2 h = 0.01389
- 1 managed rule group ($1/month, partial hour as full hour): 1 x 0.00138889 x 2 h = 0.00278
- Sum 0.09360 -> rounded up 0.10
24 h arithmetic:
- ALB (billed in full hours): 1 x 0.0225 x 24 h = 0.54000
- public IPv4 on ALB (one per AZ subnet): 2 x 0.005 x 24 h = 0.24000
- t3.micro target: 1 x 0.0104 x 24 h = 0.24960
- 8 GB gp3 root volume: 1 x 0.000888889 x 24 h = 0.02133
- WAF web ACL ($5/month, partial hour billed as full hour): 1 x 0.00694444 x 24 h = 0.16667
- 1 managed rule group ($1/month, partial hour as full hour): 1 x 0.00138889 x 24 h = 0.03333
- Sum 1.25093 -> rounded up 1.26

Old -> new: same-hour 0.04 -> 0.10; forgotten 24 h 0.96 -> 1.26

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): 1 ALB $0.0225/h (full hours), 2 public IPv4 $0.005/h each, 1 t3.micro $0.0104/h, 8 GB gp3 root $0.08/GB-month, 1 WAF web ACL $5.00/month, 1 managed rule group $1.00/month. This run ≈ $0.10; forgotten 24 h ≈ $1.26 (at least; LCU (traffic) charges, data transfer and WAF request charges ($0.60 per million) not included). The WAF rate is not verified for us-east-1; check its pricing page before you run. Re-check current pricing before you run.

stopChargesPanel:

> Disassociate the WAF web ACL from the ALB and delete the web ACL, then delete the listener, ALB, target group, EC2 instance, Elastic IP (if allocated), both public subnets and their route table, the IGW, the SG and the VPC for ul-08. Forgotten 24 h: at least $1.26 (see the cost basis).

### ul-09 (75 min)

Resources: ASG at peak 2 instances (t3.micro assumed): 2 public IPv4, 2 x 8 GB gp3 root, 2 CloudWatch alarms created by target tracking.

Same-hour arithmetic (qty x rate/h x hours):
- t3.micro: 2 x 0.0104 x 1.25 h = 0.02600
- public IPv4 (default subnet): 2 x 0.005 x 1.25 h = 0.01250
- 8 GB gp3 root volume: 2 x 0.000888889 x 1.25 h = 0.00222
- CloudWatch standard alarm (target tracking makes 2): 2 x 0.000138889 x 1.25 h = 0.00035
- Sum 0.04107 -> rounded up 0.05
24 h arithmetic:
- t3.micro: 2 x 0.0104 x 24 h = 0.49920
- public IPv4 (default subnet): 2 x 0.005 x 24 h = 0.24000
- 8 GB gp3 root volume: 2 x 0.000888889 x 24 h = 0.04267
- CloudWatch standard alarm (target tracking makes 2): 2 x 0.000138889 x 24 h = 0.00667
- Sum 0.78853 -> rounded up 0.79

Old -> new: same-hour 0.03 -> 0.05; forgotten 24 h 0.72 -> 0.79

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): 2 t3.micro at peak $0.0104/h each, 2 public IPv4 $0.005/h each, 2 x 8 GB gp3 root volumes $0.08/GB-month, 2 CloudWatch alarms $0.10/month each. This run ≈ $0.05; forgotten 24 h ≈ $0.79 (at least; data transfer not included). The CloudWatch alarm rate is not verified for us-east-1; check its pricing page before you run. Re-check current pricing before you run.

stopChargesPanel:

> Scale the ASG to 0, force-delete it and wait for its instances to terminate, then delete the CloudWatch alarm (if you created one), the launch template and the lab SG for ul-09. Forgotten 24 h: at least $0.79 (see the cost basis).

### ul-14 (120 min)

Resources: Source db.t3.micro (assumed, "smallest class") + restored copy db.t3.micro (priced as two instances) + manual snapshot; 20 GB each; not publicly accessible.

Same-hour arithmetic (qty x rate/h x hours):
- RDS db.t3.micro Single-AZ x2 (source + restored copy, full hours): 2 x 0.018 x 2 h = 0.07200
- 3 x 20 GB storage (2 instances + manual snapshot) at io1 upper-bound rate: 1 x 0.0104167 x 2 h = 0.02083
- Sum 0.09283 -> rounded up 0.10
24 h arithmetic:
- RDS db.t3.micro Single-AZ x2 (source + restored copy, full hours): 2 x 0.018 x 24 h = 0.86400
- 3 x 20 GB storage (2 instances + manual snapshot) at io1 upper-bound rate: 1 x 0.0104167 x 24 h = 0.25000
- Sum 1.11400 -> rounded up 1.12

Old -> new: same-hour 0.5 -> 0.10; forgotten 24 h 12.0 -> 1.12

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): 2 RDS db.t3.micro Single-AZ (source and restored copy) $0.018/h each, 60 GB storage (two 20 GB instances and one 20 GB snapshot; no public IPv4). This run ≈ $0.10; forgotten 24 h ≈ $1.12. Storage is priced at the higher io1 rate because the gp2/gp3 rate was not read, so real cost is likely slightly lower. Not included: data transfer. Re-check pricing before you run.

stopChargesPanel:

> Delete the restored copy, then the source RDS instance (wait for each), then the manual snapshot, the DB subnet group and the lab SG for ul-14. RDS bills every hour until deleted. Forgotten 24 h ≈ $1.12 (see the cost basis; check current pricing).

### ul-18 (90 min)

Resources: 2 Fargate tasks: 0.25 vCPU / 0.5 GB, then next tier 0.5 vCPU / 1 GB, each with a public IPv4 (assumed); optional log group not included.

Same-hour arithmetic (qty x rate/h x hours):
- Fargate 0.25 vCPU: 1 x 0.0101196 x 1.5 h = 0.01518
- Fargate 0.5 GB memory: 1 x 0.002223 x 1.5 h = 0.00333
- public IPv4 on task: 1 x 0.005 x 1.5 h = 0.00750
- Fargate 0.5 vCPU (2nd task): 1 x 0.0202392 x 1.5 h = 0.03036
- Fargate 1 GB memory (2nd task): 1 x 0.004446 x 1.5 h = 0.00667
- public IPv4 on 2nd task: 1 x 0.005 x 1.5 h = 0.00750
- Sum 0.07054 -> rounded up 0.08
24 h arithmetic:
- Fargate 0.25 vCPU: 1 x 0.0101196 x 24 h = 0.24287
- Fargate 0.5 GB memory: 1 x 0.002223 x 24 h = 0.05335
- public IPv4 on task: 1 x 0.005 x 24 h = 0.12000
- Fargate 0.5 vCPU (2nd task): 1 x 0.0202392 x 24 h = 0.48574
- Fargate 1 GB memory (2nd task): 1 x 0.004446 x 24 h = 0.10670
- public IPv4 on 2nd task: 1 x 0.005 x 24 h = 0.12000
- Sum 1.12867 -> rounded up 1.13

Old -> new: same-hour 0.2 -> 0.08; forgotten 24 h 4.8 -> 1.13

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): 2 Fargate tasks at $0.0405 per vCPU-hour and $0.00445 per GB-hour: 0.25 vCPU + 0.5 GB ≈ $0.0124/h and 0.5 vCPU + 1 GB ≈ $0.0247/h, each plus 1 public IPv4 $0.005/h, assumed running together. This run ≈ $0.08; forgotten 24 h ≈ $1.13 (at least; data transfer and logs not included). Re-check current pricing before you run.

stopChargesPanel:

> Scale services to 0 and delete them, stop running tasks, deregister task definitions, delete the cluster, log group, security group and IAM role for ul-18. Forgotten 24 h: at least $1.13 (see the cost basis).

### ul-19 (120 min)

Resources: EKS cluster + 2 managed nodes at the create-nodegroup defaults (t3.medium, 20 GiB disk, 2 nodes assumed because the docs do not state a default size), public IPv4 on each node, 2 x 20 GB gp3.

Same-hour arithmetic (qty x rate/h x hours):
- EKS control plane (standard support): 1 x 0.1 x 2 h = 0.20000
- t3.medium managed nodes (create-nodegroup default type, 2 nodes): 2 x 0.0416 x 2 h = 0.16640
- public IPv4 on nodes: 2 x 0.005 x 2 h = 0.02000
- 20 GB gp3 node root volumes: 2 x 0.00222222 x 2 h = 0.00889
- Sum 0.39529 -> rounded up 0.40
24 h arithmetic:
- EKS control plane (standard support): 1 x 0.1 x 24 h = 2.40000
- t3.medium managed nodes (create-nodegroup default type, 2 nodes): 2 x 0.0416 x 24 h = 1.99680
- public IPv4 on nodes: 2 x 0.005 x 24 h = 0.24000
- 20 GB gp3 node root volumes: 2 x 0.00222222 x 24 h = 0.10667
- Sum 4.74347 -> rounded up 4.75

Old -> new: same-hour 0.2 -> 0.40; forgotten 24 h 4.8 -> 4.75

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): EKS control plane $0.10/cluster-hour, plus 2 t3.medium nodes (the create-nodegroup default) $0.0416/h each, 2 public IPv4 $0.005/h each, 2 x 20 GB gp3 node disks $0.08/GB-month. This run ≈ $0.40; forgotten 24 h ≈ $4.75 (at least; data transfer not included). Choosing 1 x t3.micro lowers this to about $0.24 / $2.83. Re-check current pricing before you run.

stopChargesPanel:

> Delete the node group or Fargate profile and wait, delete the EKS cluster and wait, then the cluster log group and the ul-19 IAM roles. Forgotten 24 h: at least $4.75 (see the cost basis).

### ul-21 (120 min)

Resources: AWS path: 1 cache.t3.micro cache cluster (as gl-21); HCP path no-charge.

Same-hour arithmetic (qty x rate/h x hours):
- ElastiCache cache.t3.micro Redis (billed in full hours): 1 x 0.017 x 2 h = 0.03400
- Sum 0.03400 -> rounded up 0.04
24 h arithmetic:
- ElastiCache cache.t3.micro Redis (billed in full hours): 1 x 0.017 x 24 h = 0.40800
- Sum 0.40800 -> rounded up 0.41

Old -> new: same-hour 0.2 -> 0.04; forgotten 24 h 4.8 -> 0.41

beforeYouStart (line added):

> Cost basis (us-east-1, priced 2026-09-29): AWS path only: 1 ElastiCache cache.t3.micro (Redis assumed) node $0.017/h, billed in full hours (no public IPv4); the HCP path costs nothing. This run ≈ $0.04; forgotten 24 h ≈ $0.41 (at least; data transfer not included). Re-check current pricing before you run.

stopChargesPanel:

> Delete ElastiCache and AWS tags for ul-21; remove local terraform tokens from shell. Forgotten 24 h: at least $0.41 (see the cost basis).

## Mismatches found

- gl-08 / ul-08: the plan draft counted 3 public IPv4. Per the steps the instance gets none (subnets made with create-subnet have no auto-assign; run-instances has no public-IP flag), so only the ALB has 2. ul-08 stop panel mentions an 'Elastic IP (if allocated)' that no criterion creates; not priced.
- gl-08: the cost checkpoint step lists ALB and t3.micro only; it does not mention that the ALB also carries public IPv4 charges.
- gl-18 / ul-18: the task exits on its own (hello-world), so a forgotten-24h cost only arises if a service or long-running task is created. ul-18 criteria mention an ECS service and 'next tier' without fixing sizes.
- gl-19: old 24 h figure (4.80) assumed $0.20/h, double the EKS $0.10/h standard rate.
- gl-14 / ul-14 / gl-21 / ul-21: the old flat figures (0.50/12.00 and 0.20/4.80) were far above the verified cost and are corrected from the widget rates. ul-14 runs two DB instances plus a manual snapshot (priced as two instances and 60 GB); its old figure equalled gl-14's.
- ul-07: criteria do not state an instance type, EBS data volume or snapshot (gl-07 does); priced as root volume only. ul-09: instance type not stated (t3.micro assumed). ul-19: node type not stated (t3.micro assumed; t3.medium is $0.0416/h).
- gl-07 / gl-09: the steps never say the default-subnet instance gets a billable public IPv4; the cost checkpoints do not mention it.
- The page-level region tables (NAT, ALB, WAF, EBS, CloudWatch, EFS, RDS storage) do not render in the browser tool and those pages have no rate-widget iframe. Those rates stay unverified for us-east-1 and the learner lines say so.

## Second pass

Changes: (1) rate widgets (c0.b0.p.awsstatic.com iframes) used for EC2, RDS PostgreSQL instances and ElastiCache, Region button read back as US East (N. Virginia); (2) gl/ul-14 and gl/ul-21 repriced from their own steps, ul-14 as two DB instances plus 60 GB storage; (3) t3.medium corrected to $0.0416 (widget) from $0.0418 (T3 marketing page); (4) "assume it is higher" removed everywhere; unverified rates now say "rate not verified on 2026-09-29; re-check the pricing page before running"; (5) the same-hour assumption is stated once, in the method section.

Figures now: gl-14 0.50/12.00 -> 0.05/0.52; ul-14 0.50/12.00 -> 0.10/1.12; gl-21 and ul-21 0.20/4.80 -> 0.04/0.41. Marked with an asterisk in the lab lines as not verified for us-east-1: NAT, ALB, WAF, EBS gp3 and snapshot, CloudWatch alarm, RDS storage (io1 upper bound used), EFS (UL-07 keeps its earlier conservative 24 h figure).

## Fix pass (review)

Inputs: `pricing-review.md` (AWS-PA-*) and `pricing-review-TEACHER.md` (TEACHER-PA-*). The coordinator's instructions won where they differed. All 16 basis lines were rewritten to the Teacher's template (32 to 79 words; longest ul-08 at 79 words). Every figure was recomputed a second time by an independent script from the rates written in the basis text (all 16 match; ul-07 keeps 0.72 by design, computed part 0.40).

| Finding | What changed |
| --- | --- |
| LD-PA-001 (withdrawn) | No change. gl-08 stays 0.08, gl-09 0.03, ul-09 0.05 (EC2, EBS, public IPv4 and Fargate bill per second). |
| AWS-PA-001 | ul-19 now prices the `create-nodegroup` defaults: t3.medium and 20 GiB disk confirmed in the AWS docs; the default desired size is NOT stated in CreateNodegroup or NodegroupScalingConfig, so 2 nodes is assumed as the conservative case. 2 x t3.medium + 2 IPv4 + 2 x 20 GB gp3 + EKS = 0.40 / 4.75 (was 0.24 / 2.83). The basis adds "Choosing 1 x t3.micro lowers this to about $0.24 / $2.83." |
| AWS-PA-002 | ul-08 same-hour 0.09 -> 0.10 (WAF partial hour billed as a full hour, since the page says only "prorated hourly"). 24 h stays 1.26. |
| AWS-PA-003 | Unverified markers removed for ALB and EBS (gp3, snapshot). ALB and EBS rows added or updated in the claim table with URL and verbatim text; docs table updated. |
| AWS-PA-004, TEACHER-PA-001 | "floor" wording and the generic "LCU/usage" exclusion removed. Exclusions per lab: default "data transfer not included"; gl-08 and ul-08 "LCU (traffic) charges and data transfer not included"; ul-08 adds "WAF request charges ($0.60 per million)"; gl/ul-06 add NAT per-GB processing; ul-18 adds logs. "LCU" now appears only in gl-08 and ul-08. |
| AWS-PA-005, TEACHER-PA-003 | ul-07 uses the Teacher's exact basis and panel text: 0.72 is "cautious, not calculated"; the priced parts come to about $0.39. |
| TEACHER-PA-002 | gl-14 and ul-14 use the Teacher's basis and panel texts (ul-14: 2 instances, 60 GB, $0.10 / $1.12). No "at least" on these figures because io1 storage overstates them; "costly" removed from the gl-14 panel. |
| TEACHER-PA-004 | All other panels read "Forgotten 24 h: at least $Y (see the cost basis)." |
| TEACHER-PA-005, LD-PA-003 | The "rate rate" wording is gone with the rewrite. |
| LD-PA-002 | gl/ul-18 use "per vCPU-hour" and "per GB-hour" and state the task cost: 0.25 vCPU + 0.5 GB ≈ $0.0124/h (ul-18 also 0.5 vCPU + 1 GB ≈ $0.0247/h). |
| Footnotes and assumptions | Asterisks, "worked-example rate" wording, the AMI default and other assumption detail moved to `docs/labs-and-safety.md` (Example rates, notes per service). |

Caveat sentences remain only where a rate is unverified: NAT (gl/ul-06), WAF (ul-08), CloudWatch alarm (ul-09), EFS (ul-07, Teacher's wording) and the RDS storage note (gl/ul-14).
