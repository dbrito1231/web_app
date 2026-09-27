# Lesson 4.4 rewrite — implementation report

## Outline

- Replaced the placeholder `bodyMarkdown` with a full lesson covering all 14 objectives in id order: K01–K07, S01–S07.
- One `###` section per objective, each ending with an `**Exam tip:**` line; single `##` lesson title kept (`## Cost-optimized networks`).
- Kept the required `### Warnings` block text unchanged.
- Direct contrasts taught per RULES teach-before-test requirement: NAT gateway vs NAT instance cost/ops model; single-shared vs per-AZ NAT gateway (AZ-independence blast radius); Direct Connect vs Site-to-Site VPN vs plain internet; VPC peering vs Transit Gateway cost/scale; gateway vs interface VPC endpoints (free vs PrivateLink-billed); CloudFront vs Global Accelerator (cost-reduction/caching vs performance/static-IP); ALB vs NLB vs GWLB by layer; stage/account throttle vs usage-plan throttle.
- `drillIds` left unchanged (the existing 14 `-mc` ids in objective order) — questions are a later step; batch-check correctly flags this list as incomplete relative to the full 23-question bank (`-mc` + `-mr` per bullet), which is expected to be fixed when questions are rewritten.
- Replaced `citationIds: ["cite-4-4"]` with 21 new `cite-saa-4-4-*` entries.
- Confirmed `cite-4-4` was referenced only by `lesson-4-4.json` (`grep -rl "cite-4-4" content/`), then deleted `content/citations/cite-4-4.json`.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---|---|---|---|
| 1 | K01 | Tags must be activated in Billing and Cost Management to appear on billing reports | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html | "For tags to appear on your billing reports, you must activate them." |
| 2 | K01 | Tag keys can take up to 24h to appear, then up to another 24h to activate | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html | "it can take up to 24 hours for the tag keys to appear on your cost allocation tags page" |
| 3 | K01 | Consolidated billing treats organization accounts as one account for commitment discounts | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html | "treats all the accounts in the organization as one account" |
| 4 | K01 | Management account can turn off RI/Savings Plans discount sharing | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html | "You can turn off Reserved Instance discount sharing on the Preferences page" |
| 5 | K02 | Cost Explorer shows up to 12 months history and forecasts spend | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "You can view data for up to the last 12 months, forecast how much you're likely to spend" |
| 6 | K02 | Budgets alerts when actual/forecasted cost or usage exceeds threshold | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "be alerted by email or Amazon SNS notification when actual or forecasted cost and usage exceed your budget threshold" |
| 7 | K02 | CUR contains comprehensive cost and usage data | https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-cloud-financial-management-services-and-tools.html | "contains a comprehensive set of AWS cost and usage data" |
| 8a | K03 | GWLB operates at the network layer (layer 3) | https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html | "A Gateway Load Balancer operates at the third layer of the Open Systems Interconnection (OSI) model, the network layer." |
| 8b | K03 | Layer 4 is TCP transport; layer 7 is HTTP/HTTPS application (ALB vs NLB) | https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-listener-config.html | "Layer 4 is the transport layer that describes the Transmission Control Protocol (TCP) connection between the client and your back-end instance" |
| 9 | K04 | NAT gateway billed per hour available plus per GB processed | https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html | "charged for each hour that your NAT gateway is available and each gigabyte of data that it processes" |
| 10 | K04 | AWS recommends NAT gateway over NAT instance for availability/bandwidth/admin effort | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html | "they provide better availability and bandwidth and require less effort on your part to administer" |
| 11 | K04 | NAT instance cost depends on instance type/size, not a managed data-processing fee | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html | "Charged depending on the number of NAT instances that you use, duration of usage, and instance type and size" |
| 12 | K04 | NAT gateway scales to 100 Gbps automatically | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html | "Scale up to 100 Gbps." |
| 13 | K05 | Direct Connect bypasses the public internet for a direct private connection | https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect.html | "can enable consistent, low latency, high bandwidth dedicated connectivity between your data centers" |
| 14 | K05 | Dedicated Direct Connect bandwidths are 1/10/100/400 Gbps | https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect.html | "with bandwidths of 1 Gbps, 10 Gbps, 100 Gbps, or 400 Gbps" |
| 15 | K05 | Hosted Direct Connect bandwidths range 50 Mbps–25 Gbps | https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect.html | "available bandwidths from 50 Mbps up to 25 Gbps" |
| 16 | K05/S07 | Each Site-to-Site VPN connection has two tunnels for redundancy | https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html | "Each Site-to-Site VPN connection has two tunnels, with each tunnel using a unique public IP address" |
| 17 | K06 | Creating a VPC peering connection has no charge | https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html | "There is no charge to create a VPC peering connection." |
| 18 | K06 | Same-AZ data transfer over VPC peering is free; cross-AZ/Region is charged | https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html | "All data transfer over a VPC peering connection that stays within an Availability Zone is free" |
| 19 | K06 | Transit Gateway is a network transit hub interconnecting VPCs and on-prem networks | https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html | "AWS Transit Gateway is a network transit hub used to interconnect virtual private clouds (VPCs) and on-premises networks" |
| 20 | K06 | Transit Gateway bills hourly per attachment plus for traffic processed | https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html | "You are charged hourly for each attachment on a transit gateway, and you are charged for the amount of traffic processed on the transit gateway." |
| 21 | K07 | A DNS service such as Route 53 maps domain names to IP addresses | https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/welcome-dns-service.html | "A DNS service such as Amazon Route 53 makes the connection between domain names and IP addresses." |
| 22 | S01 | A NAT gateway is redundant only within its own AZ | https://docs.aws.amazon.com/awssupport/latest/user/fault-tolerance-checks.html | "Each NAT Gateway operates within a designated Availability Zone (AZ) and is built with redundancy in that AZ only." |
| 23 | S01/S03 | Same-AZ resource placement with the NAT gateway reduces cross-AZ transfer charges | https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html | "ensure that the resources are in the same Availability Zone as the NAT gateway" |
| 24 | S03 | Interface or gateway endpoints for high-traffic services cut NAT processing charges | https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html | "consider creating an interface endpoint or gateway endpoint for these services" |
| 25 | S03 | Gateway endpoints (S3, DynamoDB) have no additional charge | https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html | "There is no additional charge for using gateway endpoints." |
| 26a | S03 | Interface endpoints are billed hourly per Availability Zone | https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html | "You are billed for each hour that your interface VPC endpoint is provisioned in each Availability Zone." |
| 26b | S03 | Interface endpoints are also billed per GB of data processed | https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html | "You are also billed per GB of data processed." |
| 27 | S03/S05 | Inter-Region data transfer typically incurs charges and should be a deliberate decision | https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/cost_data_transfer_optimized_components.html | "Data transfers between AWS Regions (from one Region to another) typically incur charges" |
| 28 | S03 | Global Accelerator's static IPs route traffic over the AWS global network from the nearest edge | https://docs.aws.amazon.com/global-accelerator/latest/dg/about-accelerators.eip-accelerator.html | "static IP addresses accept incoming traffic onto the AWS global network from the edge location that is closest to your users" |
| 29 | S04 | CloudFront speeds delivery using edge locations that cache content near users | https://docs.aws.amazon.com/hands-on/latest/deliver-content-faster/deliver-content-faster.html | "CloudFront speeds up content delivery by leveraging its global network of data centers, known as edge locations" |
| 30 | S04 | Delivering from CloudFront points-of-presence costs less than delivering directly from Regions | https://docs.aws.amazon.com/wellarchitected/latest/games-industry-lens/gamecost02-bp01.html | "it costs less to deliver your content from CloudFront points-of-presence than directly from Regions" |
| 31 | S04 | CloudFront does not charge origin retrieval fees for AWS-based origins such as EC2 and S3 | https://docs.aws.amazon.com/wellarchitected/latest/games-industry-lens/gamecost02-bp01.html | "CloudFront does not charge origin retrieval fees for AWS-based origins, such as Amazon EC2 and Amazon S3" |
| 32 | S04 | CloudFront Origin Shield (now named explicitly in the prose, not just described) consolidates requests when multiple CDNs sit in front of one origin | https://docs.aws.amazon.com/wellarchitected/latest/games-industry-lens/gamecost02-bp01.html | "provide an additional layer of caching to consolidate and reduce the number of origin requests" |
| 41 | S04 | CloudFront is a web service for static and dynamic web content (used for the CloudFront-vs-Global-Accelerator HTTP-only discriminator requested by Teacher) | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html | "Amazon CloudFront is a web service that speeds up distribution of your static and dynamic web content" |
| 42 | S04/S03 | Global Accelerator listeners are configured for TCP, UDP, or both, not HTTP specifically (Teacher's requested discriminator, other side) | https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-components.html | "A listener can be configured for TCP, UDP, or both TCP and UDP protocols." |
| 33 | S05 | CloudWatch and VPC flow logs are used to capture data-transfer and network usage details | https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/cost_data_transfer_optimized_components.html | "Use Amazon CloudWatch and VPC flow logs to capture details about your data transfer and network usage" |
| 34 | S05 | Cost Explorer, CUDOS Dashboards, or CloudWatch are used to understand a workload's data transfer cost | https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/cost_data_transfer_optimized_components.html | "AWS Cost Explorer, CUDOS Dashboards, or CloudWatch to understand data transfer cost of your workload" |
| 35 | S06 | API Gateway throttles using a token-bucket algorithm | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | "API Gateway throttles requests to your API using the token bucket algorithm, where a token counts for a request" |
| 36 | S06 | Exceeding throttle limits returns 429 Too Many Requests | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | "Clients may receive `429 Too Many Requests` error responses at this point." |
| 37 | S06 | Usage plans set per-client throttles and quotas | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | "you can enable usage plans to set throttles on client request submissions based on specified requests rates and quotas" |
| 38 | S07 | VPN standard bandwidth is up to 1.25 Gbps per tunnel by default | https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html | "Standard bandwidth: Up to 1.25 Gbps per tunnel (default)" |
| 39 | S07 | Large Bandwidth Tunnels reach up to 5 Gbps per tunnel, only on Transit Gateway/Cloud WAN | https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html | "Large Bandwidth Tunnels are available only for VPN connections attached to Transit Gateway or Cloud WAN." |
| 40 | S07 | Direct Connect dedicated/hosted bandwidth tiers apply directly to bandwidth-allocation sizing | https://docs.aws.amazon.com/wellarchitected/latest/hybrid-networking-lens/aws-direct-connect.html | "with bandwidths of 1 Gbps, 10 Gbps, 100 Gbps, or 400 Gbps" |

## New citation files (21)

cite-saa-4-4-activating-tags, cite-saa-4-4-ri-behavior, cite-saa-4-4-cloud-financial-tools, cite-saa-4-4-elbv2-overview, cite-saa-4-4-nat-gateway-pricing, cite-saa-4-4-nat-comparison, cite-saa-4-4-nat-az-independence, cite-saa-4-4-direct-connect-lens, cite-saa-4-4-vpn-tunnels, cite-saa-4-4-vpc-peering, cite-saa-4-4-transit-gateway, cite-saa-4-4-tgw-cost-sample, cite-saa-4-4-route53-dns, cite-saa-4-4-vpc-endpoints-gateway, cite-saa-4-4-vpc-endpoints-interface, cite-saa-4-4-data-transfer-cost, cite-saa-4-4-cloudfront-speed, cite-saa-4-4-cloudfront-gamecost, cite-saa-4-4-global-accelerator, cite-saa-4-4-global-accelerator-static-ip, cite-saa-4-4-apigateway-throttling.

## Retired / renamed / closed-to-new-customers findings

- No retired, end-of-support, or closed-to-new-customers services were named as current advice in this lesson (Classic Load Balancer is not mentioned here; NAT instances are taught only as a cost/ops contrast to NAT gateway, not recommended).
- No new finds to add to the RULES.md retired-services list.

## Note on `cite-saa-4-4-tgw-cost-sample`

Row 20's quote comes from a Solutions Implementation guidance sample cost table (US East N. Virginia, one month), not the canonical Transit Gateway pricing page — I could not find a docs.aws.amazon.com page stating the current per-hour/per-GB TGW rate in prose. The lesson prose deliberately does not assert these dollar figures as current global pricing; it only claims TGW "is billed separately for each VPC attachment-hour and for the data it processes," which this table's line-item structure supports. Flagging in case a reviewer wants a stronger source for the billing-dimension claim.

## Round 2 — reviewer fixes applied

**AWS-L44-001 (Gone):** Split `cite-saa-4-4-elbv2-overview` (CLI reference) into two prose-sourced citations: `cite-saa-4-4-gwlb-overview` (GWLB User Guide, layer-3 statement) and `cite-saa-4-4-elb-layers` (Classic ELB Listener Configurations guide, layer-4/layer-7 statement). No lesson prose change needed; numbers were already correct.

**AWS-L44-002 (Gone):** Repointed the K06 Transit Gateway billing claim from the Solutions sample cost table to the TGW page's own **Pricing** section (same page already cited for row 19): "You are charged hourly for each attachment on a transit gateway, and you are charged for the amount of traffic processed on the transit gateway." Deleted `cite-saa-4-4-tgw-cost-sample.json`; row 20 now cites `cite-saa-4-4-transit-gateway`.

**AWS-L44-003 (Gone):** Repointed `cite-saa-4-4-vpc-endpoints-interface` from the unrelated IoT Managed Integrations dev guide to the canonical VPC PrivateLink User Guide's own Pricing section (`privatelink-access-aws-services.html`), same doc family as the already-cited gateway-endpoints page.

**TEACHER-L44-001 (Gone, major):** Rewrote the S04 Origin Shield sentence to name the feature directly: "CloudFront Origin Shield adds an additional caching layer in front of the origin to consolidate requests from the different providers and further reduce origin load." Then re-read all 40 claim rows against the prose (see full re-check list below) — all 40 already had their substance in prose except this one.

**TEACHER-L44-002 (Gone):** K03 now reads "Network Load Balancer (NLB) operates..." and "Gateway Load Balancer (GWLB) operates..." at first spelled-out use, before either abbreviation is used alone later in the section.

**TEACHER-L44-003 (Gone):** S01 now reads "...taking down egress (outbound internet traffic) for the whole VPC."

**Lesson addition — CloudFront vs Global Accelerator HTTP-only discriminator (added):** New S04 paragraph: "CloudFront caches and accelerates HTTP and HTTPS content only. A non-HTTP application, such as a custom TCP/UDP protocol, a multiplayer game backend, or VoIP traffic, that still needs a fixed entry-point IP address is a Global Accelerator scenario, not a CloudFront one, because Global Accelerator operates on TCP and UDP traffic generally rather than caching HTTP objects." Backed by new claim rows 41 (CloudFront `Introduction.html`, "web service ... static and dynamic web content") and 42 (Global Accelerator `introduction-components.html`, "A listener can be configured for TCP, UDP, or both TCP and UDP protocols."). S04's exam tip extended with the non-HTTP branch. New citations: `cite-saa-4-4-cloudfront-intro`, `cite-saa-4-4-global-accelerator-listener`.

**Lesson addition — explicit gateway-vs-interface endpoint rule (added):** S03's endpoint paragraph rewritten (not appended) to lead with: "The selection rule is direct: use a gateway endpoint when the target is Amazon S3 or DynamoDB, because there is no additional charge for using gateway endpoints; use an interface endpoint, which relies on AWS PrivateLink and is billed at standard PrivateLink rates, for any other AWS service that supports it." Backed by existing rows 25/26a/26b (unchanged facts, no new citation needed).

## Re-read of all 40 claim rows against prose (Teacher's request)

Confirmed rows 1–31, 33–40 already carried their full substance (not just numbers) in the prose at the last submission; only row 32 (Origin Shield's name) was missing and is now fixed above. No duplicate sentences were introduced by any of these edits — each fix either replaced an existing sentence in place or added one genuinely new sentence/paragraph; re-read each edited paragraph after editing to confirm no repetition.

`citationIds` now has 23 entries (was 21): removed `cite-saa-4-4-elbv2-overview` and `cite-saa-4-4-tgw-cost-sample`; added `cite-saa-4-4-gwlb-overview`, `cite-saa-4-4-elb-layers`, `cite-saa-4-4-cloudfront-intro`, `cite-saa-4-4-global-accelerator-listener`.

Verification after fixes: `content_lint.py` PASS; `claim_prose_check.py 4-4` PASS (19 distinct numbers, all present); `q1_batch_check.py 4-4` lesson-only lines PASS (single-asterisk spans 0, tables/numbered lines 0, citations unresolved [], exam tips 14/14).
