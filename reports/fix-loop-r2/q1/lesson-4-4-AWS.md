# Lesson 4.4 — AWS reviewer report (Round 1)

## Claim table rows verified (17 of 40, all facts confirmed accurate; 2 sourcing findings below)

Verified against live AWS docs (quotes matched verbatim or in substance):

- #1, #2 (K01, tag activation / 24h+24h) — `awsaccountbilling/.../activating-tags.html` confirmed verbatim.
- #8 (K03, ALB/NLB/GWLB layers 7/4/3) — numbers are correct, but see AWS-L44-001 (sourcing).
- #9 (K04, NAT gateway hourly + per-GB) — `vpc-nat-gateway-pricing.html` confirmed verbatim, including the two cost-reduction bullets (same-AZ placement, endpoints) that back S01/S03.
- #10, #11, #12 (K04, NAT gateway vs NAT instance table: availability/bandwidth/admin, cost basis, 100 Gbps scale) — `vpc-nat-comparison.html` table confirmed verbatim.
- #13, #14, #15 (K05, Direct Connect bypasses internet, dedicated 1/10/100/400 Gbps, hosted 50 Mbps–25 Gbps) — `hybrid-networking-lens/aws-direct-connect.html` confirmed verbatim.
- #16, #38, #39 (K05/S07, VPN two tunnels/unique public IPs; standard 1.25 Gbps default; LBT 5 Gbps, TGW/Cloud WAN only) — `vpn/latest/s2svpn/VPNTunnels.html` confirmed verbatim.
- #17, #18 (K06, peering free to create; same-AZ transfer free, cross-AZ/Region charged) — `vpc/latest/peering/what-is-vpc-peering.html` confirmed verbatim.
- #19 (K06, TGW is a network transit hub) — `vpc/latest/tgw/what-is-transit-gateway.html` confirmed verbatim. See AWS-L44-002 for a better source for the adjacent billing claim (#20).
- #26 (S03, interface endpoints billed at standard PrivateLink rates) — quote is accurate but sourced from an unrelated service's page; see AWS-L44-003.
- #28 (S03, Global Accelerator static IPs / nearest edge) — `global-accelerator/.../about-accelerators.eip-accelerator.html` confirmed verbatim.
- #30, #31, #32 (S04, CloudFront cheaper than Region delivery / no origin retrieval fee for EC2+S3 / Origin Shield consolidates multi-CDN requests) — `wellarchitected/latest/games-industry-lens/gamecost02-bp01.html` confirmed verbatim; this Well-Architected lens page is a legitimate general-purpose source (it states the CloudFront facts generically, not as game-specific pricing), so no finding here.
- #35, #36, #37 (S06, token-bucket algorithm, 429 response, usage plans) — `apigateway/.../api-gateway-request-throttling.html` confirmed verbatim.
- #40 (S07, dedicated DC 1/10/100/400 Gbps) — same page as #14, confirmed.

That is 17 distinct rows spot-checked (exceeds the 8-row minimum), covering every head-to-head comparison called out in the prompt (NAT gateway vs instance, per-AZ vs shared NAT via #9's cost-reduction bullets, DC vs VPN vs internet, peering vs TGW, gateway vs interface endpoints, CloudFront vs Global Accelerator, ALB/NLB/GWLB, throttling types) and every data-transfer/per-hour pricing row. No factual, directional, or unit errors found in any row's number or claim.

## Findings

**AWS-L44-001** — Severity: Low (sourcing, not fact)
Location: Claim table row 8, K03 section, ALB/NLB/GWLB layer discriminator.
Issue: The citation (`cite-saa-4-4-elbv2-overview` → `https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html`) is an AWS CLI command reference page. Per this review's instructions, a CLI command reference cannot support a selection-criteria claim, even though the quoted text ("Application Load Balancer - Operates at the application layer (layer 7)...") is accurate.
Doc-verified fix: Replace the citation with the Gateway Load Balancer User Guide, which states the layer-3 fact in prose in its own overview section: `https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html` — "A Gateway Load Balancer operates at the third layer of the Open Systems Interconnection (OSI) model, the network layer." For the layer-7/layer-4 half of the claim, add a second citation to `https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-listener-config.html`, which states: "Layer 4 is the transport layer that describes the Transmission Control Protocol (TCP) connection... Layer 7 is the application layer that describes the use of Hypertext Transfer Protocol (HTTP) and HTTPS... connections." Update `cite-saa-4-4-elbv2-overview` (or split into two citation files) accordingly; no change to lesson prose is needed since the stated numbers are correct.

**AWS-L44-002** — Severity: Low (sourcing)
Location: Claim table row 20, K06 section, "Transit Gateway is billed per VPC-attachment-hour and per GB processed."
Issue: The writer's own note flags this — the citation is a Solutions Implementation sample cost table (`solutions/latest/centralized-network-inspection-on-aws/cost.html`), not a canonical pricing statement, and the writer could not find a docs.aws.amazon.com prose statement of the billing dimensions.
Doc-verified fix: One exists on the exact same page already cited for row 19. `https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html` has a "Pricing" section stating verbatim: "You are charged hourly for each attachment on a transit gateway, and you are charged for the amount of traffic processed on the transit gateway." Repoint `cite-saa-4-4-tgw-cost-sample`'s citation file to this URL/section instead of the Solutions Implementation sample table — no separate citation file is even needed since it's the same page as `cite-saa-4-4-transit-gateway`.

**AWS-L44-003** — Severity: Low (sourcing)
Location: Claim table row 26, S03 section, "Interface endpoints are billed at standard AWS PrivateLink rates."
Issue: The citation (`cite-saa-4-4-vpc-endpoints-interface` → `https://docs.aws.amazon.com/iot-mi/latest/devguide/vpc-endpoints-pricing.html`) is an AWS IoT Managed Integrations dev-guide page whose "Pricing" section happens to contain generic PrivateLink pricing boilerplate. The quote is accurate but the source is an unrelated, narrow service page, not a networking user guide — a odd anchor for a general VPC-endpoints claim.
Doc-verified fix: Repoint the citation to `https://docs.aws.amazon.com/vpc/latest/privatelink/full.html`, the canonical VPC PrivateLink user guide, which has its own "Pricing" section covering interface endpoint billing generically (confirmed present via AWS documentation search: rank_order 4, section title "Pricing").

No retired/renamed/closed-to-new-customers services are used incorrectly. Confirmed the lesson does not name Snow Family, FSx File Gateway, Timestream for LiveAnalytics, or AWS Copilot CLI as current advice, and does not misname a renamed service. No new retired/renamed services to add to RULES.md.

## Coverage, format, teach-before-test

- All 14 objective bullets (K01–K07, S01–S07) present as `###` sections in id order, matching `objectiveIds` in the lesson and `content/objectives/saa_c03.json` verbatim text.
- Every section ends with a `**Exam tip:**` line; each exam tip states an applicable discriminator (a condition/keyword pattern a student can match), not a vague true sentence — confirmed for all 8 head-to-head comparisons named in the prompt.
- Markdown format matches RULES.md subset: single `##` title (established pattern, not a finding), `###` sections, `**Exam tip:**`, no tables/links/numbered lists/single-asterisk italics, standard `### Warnings` block.
- Teach-before-test: lesson teaches both the key fact and the reason for each contrast (e.g., NAT gateway vs instance covers both the cost model and the operational-burden reasoning that would eliminate a NAT-instance distractor); ready for question writing once the three sourcing findings are addressed.

Lesson 4.4: approve for question writing

Overall: concerns
