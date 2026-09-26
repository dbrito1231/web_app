# Lesson 3.4 implementation report — Determine high-performing and/or scalable network architectures

## Files touched

- `content/lessons/lesson-3-4.json` — rewritten (was a placeholder body).
- `content/citations/cite-saa-3-4-cloudfront-cache-behaviors.json` — new
- `content/citations/cite-saa-3-4-origin-shield.json` — new
- `content/citations/cite-saa-3-4-global-accelerator-how-it-works.json` — new
- `content/citations/cite-saa-3-4-vpc-cidr-blocks.json` — new
- `content/citations/cite-saa-3-4-subnet-sizing.json` — new
- `content/citations/cite-saa-3-4-vpc-peering-transitive.json` — new
- `content/citations/cite-saa-3-4-privatelink-concepts.json` — new
- `content/citations/cite-saa-3-4-vpc-endpoints-gateway.json` — new
- `content/citations/cite-saa-3-4-vpn-tunnel-bandwidth.json` — new
- `content/citations/cite-saa-3-4-dx-lag.json` — new
- `content/citations/cite-saa-3-4-local-zones.json` — new
- `content/citations/cite-saa-3-4-wavelength.json` — new
- `content/citations/cite-3-4.json` — deleted (only reference was the old lesson body; grep confirmed no other file referenced it before deletion).

`cite-saa-3-2-enhanced-networking` (existing file from lesson 3.2) is reused, unmodified, in this lesson's `citationIds` for the brief K05/S03-style callback to enhanced networking in the S04 section — no new file needed since it is the same doc page already on file.

## Word count

2,315 words in `bodyMarkdown` (target 2,000–2,600).

## Section outline

1. **K01 — Edge networking services**: refers back to Lesson 2.2's CloudFront-vs-Global-Accelerator overview, then covers CloudFront cache behaviors (per-path-pattern origin/TTL/protocol rules) and Origin Shield (extra consolidating cache layer), and Global Accelerator's anycast static-IP entry point for non-HTTP traffic.
2. **K02 — Network architecture design**: VPC/subnet CIDR sizing (`/16`–`/28`), RFC 1918 ranges, one-subnet-per-AZ-per-tier, the 5 reserved addresses per subnet, and route tables as what actually makes a subnet public or private.
3. **K03 — Load balancing concepts**: brief callback to Lesson 2.1's ALB/NLB/GWLB coverage, then the performance angle (Layer 4 vs Layer 7 cost) and cross-zone load balancing.
4. **K04 — Network connection options**: Site-to-Site VPN (1.25 Gbps standard / 5 Gbps Large Bandwidth Tunnel), Direct Connect (dedicated line speeds, LAG), VPN-over-DX and DX+VPN-backup patterns, PrivateLink interface endpoints vs. no-cost S3/DynamoDB gateway endpoints.
5. **S01 — Network topology for various architectures**: global (CloudFront/Global Accelerator + Route 53), hybrid (Direct Connect/VPN + transit gateway or DX gateway), multi-tier (public/private subnets per AZ).
6. **S02 — Scaling network configurations**: CIDR blocks can't be resized (only supplemented), VPC peering's non-transitive limitation causing full-mesh growth pain, Transit Gateway as the hub-and-spoke fix.
7. **S03 — Resource placement**: subnet placement recap, then Local Zones (metro-area extension of a parent Region) and Wavelength (embedded in telco 5G) as narrow, brief-reference edge-placement options.
8. **S04 — Load balancing strategy selection**: matches load balancer type to traffic shape, ties in cross-zone load balancing, and closes with a brief callback to Lesson 3.2 S03's enhanced networking (ENA) as a target-side bottleneck check.

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---------|-------|---------|--------------------|
| 1 | K01 | A cache behavior maps a path pattern to its own origin/TTL/protocol settings | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistValuesCacheBehavior.html | "Configure CloudFront cache behavior options including path patterns, TTL values, protocol policies, and origin routing" |
| 2 | K01 | Origin Shield consolidates all CloudFront caching-layer requests to a single location before the origin | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html | "When you use Origin Shield, all requests from all of the CloudFront caching layers to your origin come from a single location" |
| 3 | K01 | Global Accelerator's static IPs are fixed entry points routed over the AWS global network to the optimal endpoint | https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html | "static IP addresses provided by AWS Global Accelerator serve as single fixed entry points for your clients" |
| 4 | K02 | VPC IPv4 CIDR block allowed size is /16 (65,536 IPs) to /28 (16 IPs) | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html | "The allowed block size is between a /16 netmask (65,536 IP addresses) and /28 netmask (16 IP addresses)" |
| 5 | K02 | AWS recommends an RFC 1918 private range for a VPC's CIDR block | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html | "we recommend that you specify a CIDR block from the private IPv4 address ranges as specified in RFC 1918" |
| 6 | K02 | Subnet IPv4 CIDR allowed size is /28 to /16 netmask | https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html | "The allowed IPv4 CIDR block size for a subnet is between a /28 netmask and /16 netmask" |
| 7 | K02 | Every subnet reserves its first four addresses and its last address | https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html | "The first four IP addresses and the last IP address in each subnet CIDR block are not available" |
| 8 | S02 | A VPC's CIDR block cannot be resized, only supplemented with additional non-overlapping blocks | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html | "You cannot increase or decrease the size of an existing CIDR block" |
| 9 | S02 / K04 | VPC peering does not support transitive peering relationships | https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html | "VPC peering does not support transitive peering relationships" |
| 10 | K04 | An interface VPC endpoint uses PrivateLink to enable private connectivity without traversing the internet | https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html | "interface VPC endpoint...enables private connectivity to FinSpace APIs without traversing the internet" |
| 11 | K04 | An endpoint service is a PrivateLink-powered service other accounts reach via interface endpoints, not full VPC peering | https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html | "PrivateLink-powered service created from a user's own application in a VPC that other AWS principals can connect to via interface VPC endpoints" |
| 12 | K04 | Gateway endpoints are free; interface endpoints bill hourly plus per-GB data processing | https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html | "Gateway endpoints are available at no additional charge. Interface endpoints incur an hourly charge and a per-GB data-processing charge" |
| 13 | K04 | Standard Site-to-Site VPN tunnel bandwidth is up to 1.25 Gbps | https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html | "The default VPN tunnel bandwidth capacity of up to 1.25 Gbps per tunnel" |
| 14 | K04 | A Large Bandwidth Tunnel supports up to 5 Gbps per tunnel on a Transit Gateway/Cloud WAN attachment | https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html | "A VPN tunnel configuration that supports up to 5 Gbps bandwidth per tunnel, available for Transit Gateway or Cloud WAN attachments" |
| 15 | K04 | Direct Connect dedicated connections come in 1, 10, 100, or 400 Gbps port speeds | https://docs.aws.amazon.com/directconnect/latest/UserGuide/lags.html | "All connections must be dedicated connections and have a port speed of 1 Gbps, 10 Gbps, 100 Gbps, or 400 Gbps" |
| 16 | K04 | A LAG uses LACP to aggregate multiple same-bandwidth connections at one endpoint into one managed connection | https://docs.aws.amazon.com/directconnect/latest/UserGuide/lags.html | "logical interface that uses the Link Aggregation Control Protocol (LACP) to aggregate multiple connections at a single Direct Connect endpoint" |
| 17 | K04 | All connections in a LAG must use the same bandwidth and terminate at the same endpoint | https://docs.aws.amazon.com/directconnect/latest/UserGuide/lags.html | "All connections in the LAG must use the same bandwidth" / "must terminate at the same Direct Connect endpoint" |
| 18 | S03 | A Local Zone extends AWS Region infrastructure to a location near users, connected to its parent Region | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html | "An extension of an AWS Region in geographic proximity to users that provides low-latency access to compute and storage resources" |
| 19 | S03 | AWS Wavelength embeds AWS infrastructure within a telecommunications carrier's network | https://docs.aws.amazon.com/wavelength/latest/developerguide/what-is-wavelength.html | "An infrastructure deployment embedded within a telecommunications carrier's network at a specific location" (page title/concept, matches lesson 3.2's existing citation) |
| 20 | S04 (callback) | Enhanced networking (ENA) raises per-flow bandwidth and packet-per-second performance | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking-ena.html (cite-saa-3-2-enhanced-networking, reused) | reused from Lesson 3.2's already-verified citation; no new fetch performed, claim unchanged from that lesson |

Rows 1–19 are freshly re-checked against AWS docs during this task (2026-09-26). Row 20 reuses Lesson 3.2's already-verified fact and citation without re-fetching, since it is only a one-sentence callback and the source page/claim are unchanged from that lesson's own review.

## Retired or closed services found

None of the retired/closed/EOL services in RULES.md (Copilot CLI, Snow Family, FSx File Gateway) appear in this lesson. No other services requiring a status check (QLDB, Timestream, CodeCommit, Cloud9, CodeStar) were mentioned. No new finds to add to the retired-services list.

## Checks run

- `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 3-4`: lesson lines PASS (`lesson citations unresolved: []`, `drillIds match questions`, `exam tips 8 for 8 objectives`). All FAILs are on the 13 unmodified placeholder questions, as expected — they will be addressed when the questions are written.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py`: PASS (`questions 429 aws 310 tf 119`, `labs 21 + 21`, `lessons 23`).

## Notes for reviewers

- drillIds are in objective order (K01, K02, K03-mc, K03-mr, K04, S01-mc, S01-mr, S02-mc, S02-mr, S03-mc, S03-mr, S04-mc, S04-mr), matching the existing placeholder question IDs exactly.
- The lesson does not re-teach ALB/NLB/GWLB fundamentals, cross-zone mechanics in detail, Global Accelerator vs. CloudFront basics, or Route 53 policies — those stay in Lessons 2.1/2.2 and are only referenced back to, per the task brief.
