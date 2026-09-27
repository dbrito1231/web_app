# Teacher review — Lesson 4.4, round 1

## Claim rows verified (8, plus context reads)

- Row 9/10/11/12 (K04, NAT gateway vs NAT instance): `docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html` confirms verbatim: "We recommend that you use NAT gateways because they provide better availability and bandwidth and require less effort on your part to administer," NAT instance cost is "Charged depending on the number of NAT instances that you use, duration of usage, and instance type and size," and "Scale up to 100 Gbps." All four rows match. Good.
- Row 17/18 (K06, VPC peering pricing): `docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html` confirms verbatim: "There is no charge to create a VPC peering connection. All data transfer over a VPC peering connection that stays within an Availability Zone is free... Charges apply for data transfer over VPC peering connections that cross Availability Zones and Regions." Matches.
- Row 25 (S03, gateway endpoints no charge): `docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html` confirms verbatim "There is no additional charge for using gateway endpoints." Matches. Page also confirms "Gateway VPC endpoints... do not use AWS PrivateLink, unlike other types of VPC endpoints" — consistent with the lesson's gateway/interface contrast.
- Row 26 (S03, interface endpoint PrivateLink billing): source page (`iot-mi/latest/devguide/vpc-endpoints-pricing.html`) is a generic boilerplate AWS PrivateLink pricing block reused across many service guides — content is accurate ("charged per endpoint-hour and per GB of data processed") but it is an odd citation target for a general claim. Not a factual problem, just a weak source; a canonical PrivateLink pricing page would be better if the writer wants to swap it, not required.
- Row 30/31 (S04, CloudFront cost claims): `docs.aws.amazon.com/wellarchitected/latest/games-industry-lens/gamecost02-bp01.html` confirms verbatim "it costs less to deliver your content from CloudFront points-of-presence than directly from Regions, and CloudFront does not charge origin retrieval fees for AWS-based origins, such as Amazon EC2 and Amazon S3." Matches.
- Row 35/36 (S06, API Gateway throttling): `docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html` confirms verbatim "token bucket algorithm, where a token counts for a request" and "Clients may receive `429 Too Many Requests` error responses." Matches.
- Row 38/39 (S07, VPN tunnel bandwidth): `docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html` confirms verbatim "Standard bandwidth: Up to 1.25 Gbps per tunnel (default)," "Large Bandwidth Tunnel (LBT): Up to 5 Gbps per tunnel," and "Large Bandwidth Tunnels are available only for VPN connections attached to Transit Gateway or Cloud WAN." Matches.
- Row 32 (S04, Origin Shield): source page confirms the mechanism verbatim ("provide an additional layer of caching to consolidate and reduce the number of origin requests from different providers") but see TEACHER-L44-001 below — the lesson never names the AWS feature this claim is about.
- Objective coverage: all 14 `SAA-4.4-K01..K07, S01..S07` bullets exist in `content/objectives/saa_c03.json` and each has a matching `###` section in the lesson, in id order. Format (single `##` title, `### Warnings` at end) matches established pattern — not reported per the known false alarm.

## Findings

**TEACHER-L44-001 (Major)** — Claim-table row 32 never reaches the prose by name.
Location: S04 section, third paragraph ("When multiple CDNs sit in front of the same origin, an additional caching layer in front of the origin consolidates requests from the different providers and further reduces origin load.").
Problem: this sentence describes CloudFront Origin Shield's behavior but never names the feature. A question that asks "which CloudFront capability reduces origin load when multiple CDNs sit in front of the same origin" would have "Origin Shield" as its key, and nothing in this lesson lets a student connect the described behavior to that term. This is the exact defect class flagged from task 4.3 (a claim-table fact that never surfaces in taught prose).
Fix (doc-verified, from `docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html`, cited already by the writer's row-32 source page): append to that sentence — "This capability is called CloudFront Origin Shield, an additional caching layer you enable per distribution to reduce requests reaching the origin."

**TEACHER-L44-002 (Minor)** — "NLB" and "GWLB" used before being defined as abbreviations.
Location: K03 section. The heading defines `Application Load Balancer [ALB]` in brackets, but the prose only ever spells out "Network Load Balancer" and "Gateway Load Balancer" in full — the abbreviations "NLB" and "GWLB" first appear later ("an NLB avoids the extra application-layer processing...", and in the Exam tip "...to ALB, NLB, or GWLB") with no prior bracket definition.
Fix: in the K03 body, change "Network Load Balancer operates at the transport layer (layer 4)" to "Network Load Balancer (NLB) operates at the transport layer (layer 4)", and "Gateway Load Balancer operates at the network layer (layer 3)" to "Gateway Load Balancer (GWLB) operates at the network layer (layer 3)".

**TEACHER-L44-003 (Minor)** — "egress" used without definition.
Location: S01, second paragraph: "...keeps one AZ's failure from taking down egress for the whole VPC." No prior sentence defines "egress" as outbound traffic to the internet.
Fix: change to "...keeps one AZ's failure from taking down egress (outbound internet traffic) for the whole VPC," or define it once at first NAT mention in K04 ("...outbound internet access for private subnets (egress)...").

## Lesson additions requested

- CloudFront vs. Global Accelerator discriminator could be sharper for non-HTTP scenarios. The lesson already states GA "improves performance and availability for TCP and UDP traffic" (correctly implying it isn't HTTP-only), but never states outright that CloudFront is HTTP/HTTPS-only. Suggested addition to S04 or S03's exam tip, doc-verified from `docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html` context: "CloudFront caches and accelerates HTTP and HTTPS content only; a non-HTTP application (custom TCP/UDP protocols, gaming, VoIP) that still needs a fixed entry-point IP is a Global Accelerator scenario, not a CloudFront one." This closes the gap for a likely question pattern ("static IP for a non-HTTP protocol").
- Gateway vs. interface endpoint selection rule is inferable but not stated as a rule. Suggested one-line addition to S03: "Use a gateway endpoint when the target is Amazon S3 or DynamoDB (no additional charge); use an interface endpoint, billed at standard AWS PrivateLink rates, for any other AWS service." This turns the current implicit contrast into an explicit, quotable discriminator for question writing.

## Stem-paraphrase readiness

No additional concept found that is explained in only one phrasing where a paraphrased stem would leave the student with nothing to connect (beyond the Origin Shield gap above, which is a coverage problem, not a paraphrase problem). The named-feature contrasts (NAT gateway/instance, peering/Transit Gateway, DC/VPN/internet, ALB/NLB/GWLB, gateway/interface endpoint, CloudFront/Global Accelerator, stage-throttle/usage-plan) are all taught with an operational discriminator, not just a label, so a paraphrased stem describing the scenario should still let a prepared student pick the right feature by its behavior.

## Teach-before-test / discriminator check

All eight required pairs (NAT gateway vs NAT instance, per-AZ vs shared NAT, Direct Connect vs VPN vs internet, VPC peering vs Transit Gateway, gateway vs interface endpoints, CloudFront vs Global Accelerator, ALB vs NLB vs GWLB) have a usable decision rule a student could apply to a scenario, not just a true-but-inert sentence. Weakest of the eight is gateway-vs-interface endpoint (implicit rather than stated as a rule — see additions above) and CloudFront-vs-Global-Accelerator for non-HTTP cases (see additions above); both are addressable with small prose additions rather than a structural rewrite.

Lesson 4.4: not yet

Overall: concerns
