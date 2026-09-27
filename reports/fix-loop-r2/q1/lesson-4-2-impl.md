# Lesson 4.2 rewrite ? implementation report

## Outline

- Replaced placeholder content with a full lesson for all 15 objectives in order: K01?K09, S01?S06.
- Kept one `###` section per objective and ended each section with an `**Exam tip:**` line.
- Preserved the required `### Warnings` block text and removed the trailing placeholder citation line.
- Added explicit high-confusion contrasts required by task scope: Spot vs Reserved Instances vs Savings Plans vs On-Demand; Compute Savings Plans vs EC2 Instance Savings Plans; horizontal vs vertical scaling; stop vs hibernate; ALB vs NLB vs GWLB; Lambda vs Fargate vs EC2; Outposts vs Local Zones vs Wavelength; instance family letters and size doubling.
- Updated `drillIds` to the exact 24-item ordered list provided by the prompt.
- Replaced placeholder `citationIds` with new `cite-saa-4-2-*` files based on AWS official docs.
- Confirmed `cite-4-2` was referenced only by lesson 4.2, then deleted `content/citations/cite-4-2.json`.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | K01 | User-defined cost allocation tags must be activated for billing reports | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html | "For tags to appear on your billing reports, you must activate them." |
| 2 | K01 | Tag keys can take up to 24 hours to appear and another 24 to activate | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html | "it can take up to 24 hours ... It can then take up to 24 hours" |
| 3 | K01 | Consolidated billing lets organization accounts share RI cost benefit | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html | "treats all the accounts in the organization as one account" |
| 4 | K01 | RI discount sharing can be turned off by management account | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html | "You can turn off Reserved Instance discount sharing" |
| 5 | K02 | Cost and Usage Report includes comprehensive cost and usage data | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "contains a comprehensive set of AWS cost and usage data" |
| 6 | K02 | Cost Explorer provides up to 12 months historical and 12 months forecast | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "view data for up to the last 12 months, forecast ... the next 12 months" |
| 7 | K02 | Budgets can alert on actual or forecasted over-threshold usage/cost | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "actual or forecasted cost and usage exceed your budget threshold" |
| 8 | K03 | AWS locations include Regions, AZs, Local Zones, Wavelength Zones | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | "composed of AWS Regions, Availability Zones, Local Zones, and Wavelength Zones" |
| 9 | K03 | Region is separate geographic area | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | "Each Region is a separate geographic area." |
| 10 | K03 | AZs are isolated locations within a Region | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | "Availability Zones are isolated locations within each Region." |
| 11 | K03 | Single-AZ failure example causes all instances there to be unavailable | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | "if you host all of your EC2 instances in a single Availability Zones ... none ... would be available" |
| 12 | K03 | Production workloads should run in at least two AZs | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_multiaz_region_system.html | "Deploy and operate all production workloads in at least two Availability Zones" |
| 13 | K03 | NAT gateway pricing includes hourly and per-GB processed charges | https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html | "charged for each hour ... and each gigabyte of data that it processes" |
| 14 | K03 | Same-AZ resource placement with NAT gateway helps reduce transfer cost | https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html | "ensure that the resources are in the same Availability Zone as the NAT gateway" |
| 15 | K04 | On-Demand supports hour or second billing with 60-second minimum | https://aws.amazon.com/ec2/pricing/ | "billed in one-second increments, with a minimum of 60 seconds" |
| 16 | K04 | Spot interruption notice is two minutes | https://aws.amazon.com/ec2/spot/getting-started/ | "Spot Instances receive a two-minute notice" |
| 17 | K04 | Savings Plans commitment measured in usage per hour | https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html | "measured per hour" |
| 18 | K04 | Savings Plans terms are one or three years | https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html | "one or three year period" |
| 19 | K04 | Compute Savings Plans can save up to 66 percent | https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-ris.html | "Compute Savings Plans provide savings up to 66% off On-Demand" |
| 20 | K04 | EC2 Instance Savings Plans can save up to 72 percent | https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-ris.html | "EC2 Instance Savings Plans offer savings up to 72% off of On-Demand" |
| 21 | K04 | Compute Savings Plans apply to EC2, Fargate, Lambda | https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-ris.html | "automatically reduce your cost on EC2 instance usage, Fargate, and Lambda" |
| 22 | K04 | Reserved Instances terms are one or three years | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html | "You can purchase a Reserved Instance for a one-year or three-year commitment" |
| 23 | K04 | Reserved payment options include all/partial/no upfront | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html | "All Upfront ... Partial Upfront ... No Upfront" |
| 24 | K05 | Local Zones target single-digit millisecond latency | https://aws.amazon.com/about-aws/global-infrastructure/localzones/faqs/ | "Local Zones ... run workloads that require single-digit millisecond latency" |
| 25 | K05 | Wavelength is for ultralow-latency 5G applications | https://aws.amazon.com/about-aws/global-infrastructure/localzones/faqs/ | "Wavelength is designed to deliver ultralow-latency applications to 5G devices" |
| 26 | K06 | Outposts extends AWS infrastructure/services to on-premises/edge locations | https://aws.amazon.com/outposts/ | "delivering AWS infrastructure and services to virtually any on-premises or edge location" |
| 27 | K06 | Outposts supports running native AWS services on premises | https://aws.amazon.com/outposts/ | "extend and run native AWS services on-premises" |
| 28 | K07 | Instance names include family and size | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "Instance types are named based on their instance family and instance size" |
| 29 | K07 | First family position indicates series | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "The first position ... indicates the series" |
| 30 | K07 | Second family position indicates generation | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "The second position indicates the generation" |
| 31 | K07 | Third family position indicates options | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "The third position indicates the options" |
| 55 | K07 | Instance sizes include `metal` for bare metal instances | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "or `metal` for bare metal instances." |
| 32 | K07 | `C` series means compute optimized | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "C - Compute optimized" |
| 33 | K07 | `R` series means memory optimized | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "R - Memory optimized" |
| 34 | K07 | `M` series means general purpose | https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-type-names.html | "M - General purpose" |
| 35 | K08 | Fargate is billed per second with 1-minute minimum | https://aws.amazon.com/fargate/pricing/ | "Pricing is calculated per second with a 1-minute minimum" |
| 36 | K08 | Windows containers on Fargate have 5-minute minimum | https://aws.amazon.com/fargate/pricing/ | "For Windows containers ... per second with a 5-minute minimum" |
| 37 | K08 | Lambda functions priced by requests and duration | https://aws.amazon.com/lambda/pricing/ | "priced based on the number of requests served and the duration your code runs" |
| 38 | K08 | Lambda timeout default is 3 seconds | https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html | "default value for this setting is 3 seconds" |
| 39 | K08 | Lambda timeout max is 900 seconds (15 minutes) | https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html | "maximum value of 900 seconds (15 minutes)" |
| 56 | K08 | Lambda timeout can be set from 1 to 900 seconds for standard functions | https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html | "adjust this in increments of 1 second up to a maximum value of 900 seconds" |
| 40 | K09 | Target tracking adds/removes capacity to keep metric near target | https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html | "adds and removes capacity ... to keep the metric at ... the specified target value" |
| 41 | K09 | Above target scales out; below target scales in | https://docs.aws.amazon.com/autoscaling/application/userguide/target-tracking-scaling-policy-overview.html | "above the target value ... scales out ... below the target value ... scales in" |
| 42 | K09/S02 | Hibernation saves RAM to EBS root volume | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html | "Hibernation saves the contents from the instance memory (RAM) to ... EBS root volume" |
| 43 | K09/S02 | Hibernated instances are not charged for instance usage | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html | "not charged for instance usage for a hibernated instance" |
| 44 | K09/S02 | EBS storage charges continue for hibernated instance volumes | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html | "You are charged for storage of any EBS volumes" |
| 45 | S01 | ALB is layer 7 and supports HTTP/HTTPS | https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html | "Application Load Balancer - Operates at the application layer (layer 7)" |
| 46 | S01 | NLB is layer 4 and supports TCP/TLS/UDP/QUIC | https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html | "Network Load Balancer - Operates at the transport layer (layer 4)" |
| 47 | S01 | GWLB operates at network layer (layer 3) | https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html | "Gateway Load Balancer - Operates at the network layer (layer 3)." |
| 48 | S01 | ALB supports host-based and path-based routing | https://docs.aws.amazon.com/help-panel/elasticbeanstalk/latest/helppanel/f-load-balancer-type.html | "advanced features like host-based routing, path-based routing" |
| 49 | S01 | NLB provides static IP addresses | https://docs.aws.amazon.com/help-panel/elasticbeanstalk/latest/helppanel/f-load-balancer-type.html | "provides ultra-high performance with static IP addresses" |
| 57 | S01 | Classic Load Balancer is previous-generation and not recommended for new environments | https://docs.aws.amazon.com/help-panel/elasticbeanstalk/latest/helppanel/f-load-balancer-type.html | "is not recommended for new environments." |
| 50 | S06 | c7g.large has 2 vCPU and 4 GiB memory | https://aws.amazon.com/ec2/instance-types/c7g/ | "c7g.large | 2 | 4" |
| 51 | S06 | c7g.xlarge has 4 vCPU and 8 GiB memory | https://aws.amazon.com/ec2/instance-types/c7g/ | "c7g.xlarge | 4 | 8" |
| 52 | S06 | c7g.2xlarge has 8 vCPU and 16 GiB memory | https://aws.amazon.com/ec2/instance-types/c7g/ | "c7g.2xlarge | 8 | 16" |
| 53 | S03 | On-Demand allows per-second pay-as-you-go compute | https://docs.aws.amazon.com/decision-guides/latest/decision-guides/ec2-purchasing-options-aws-how-to-choose.html | "pay only for the compute time you use, with billing granularity as low as per-second for Linux, RHEL, and Windows instances" |
| 54 | S03 | EC2 Spot can be up to 90 percent lower than On-Demand | https://aws.amazon.com/ec2/pricing/ | "discount of up to 90% compared to On-Demand prices" |

## New citation files

- `content/citations/cite-saa-4-2-activating-tags.json`
- `content/citations/cite-saa-4-2-cloud-financial-tools.json`
- `content/citations/cite-saa-4-2-ri-behavior.json`
- `content/citations/cite-saa-4-2-savingsplans-overview.json`
- `content/citations/cite-saa-4-2-ec2-purchasing-guide.json`
- `content/citations/cite-saa-4-2-savingsplans-vs-ri.json`
- `content/citations/cite-saa-4-2-spot-interruptions.json`
- `content/citations/cite-saa-4-2-reserved-instances.json`
- `content/citations/cite-saa-4-2-regions-azs.json`
- `content/citations/cite-saa-4-2-localzone-faq.json`
- `content/citations/cite-saa-4-2-outposts-overview.json`
- `content/citations/cite-saa-4-2-instance-names.json`
- `content/citations/cite-saa-4-2-c7g-table.json`
- `content/citations/cite-saa-4-2-ec2-pricing.json`
- `content/citations/cite-saa-4-2-hibernate.json`
- `content/citations/cite-saa-4-2-fargate-pricing.json`
- `content/citations/cite-saa-4-2-lambda-pricing.json`
- `content/citations/cite-saa-4-2-lambda-timeout.json`
- `content/citations/cite-saa-4-2-target-tracking.json`
- `content/citations/cite-saa-4-2-multiaz-reliability.json`
- `content/citations/cite-saa-4-2-nat-gateway-pricing.json`
- `content/citations/cite-saa-4-2-load-balancer-type.json`
- `content/citations/cite-saa-4-2-elbv2-overview.json`

## Retired / renamed / closed-to-new-customers findings

- Re-checked required list item used in lesson language: **AWS Snow Family is closed to new customers**.
- No additional new retired/renamed/closed findings were introduced in this lesson rewrite.
