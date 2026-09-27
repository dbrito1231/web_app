# Teacher review — Lesson/Task 4.4, round 2

## (a) Round-1 Teacher findings — status

- **TEACHER-L44-001 (Origin Shield unnamed): Gone.** S04 prose now reads "When multiple CDNs sit in front of the same origin, CloudFront Origin Shield adds an additional caching layer in front of the origin to consolidate requests from the different providers and further reduce origin load." The feature is named in the prose itself, not just the claim table.
- **TEACHER-L44-002 (NLB/GWLB undefined): Gone.** K03 now reads "Network Load Balancer (NLB) operates at the transport layer (layer 4)..." and "Gateway Load Balancer (GWLB) operates at the network layer (layer 3)...", both spelled out before either abbreviation is used alone later in the section and in the exam tip.
- **TEACHER-L44-003 (undefined "egress"): Gone.** S01 now reads "...keeps one AZ's failure from taking down egress (outbound internet traffic) for the whole VPC."
- **Lesson addition — CloudFront-vs-Global-Accelerator HTTP-only discriminator: landed in prose.** New S04 paragraph: "CloudFront caches and accelerates HTTP and HTTPS content only. A non-HTTP application, such as a custom TCP/UDP protocol, a multiplayer game backend, or VoIP traffic, that still needs a fixed entry-point IP address is a Global Accelerator scenario, not a CloudFront one..." Exam tip extended to match. Backed by two new, accurate citations (verified below).
- **Lesson addition — explicit gateway-vs-interface-endpoint rule: landed in prose.** S03's endpoint paragraph now leads with "The selection rule is direct: use a gateway endpoint when the target is Amazon S3 or DynamoDB, because there is no additional charge for using gateway endpoints; use an interface endpoint, which relies on AWS PrivateLink and is billed at standard PrivateLink rates, for any other AWS service that supports it."

## (b) Second-role check on AWS-L44-001/002/003

All three are sourcing-only fixes (no fact changed); I re-fetched each new citation URL and confirm the quotes are verbatim and on-topic:
- **AWS-L44-001 (Gone):** `elasticloadbalancing/latest/gateway/introduction.html` confirmed verbatim "A Gateway Load Balancer operates at the third layer of the Open Systems Interconnection (OSI) model, the network layer." `elasticloadbalancing/latest/classic/elb-listener-config.html` confirmed verbatim "Layer 4 is the transport layer that describes the Transmission Control Protocol (TCP) connection..." and "Layer 7 is the application layer that describes the use of Hypertext Transfer Protocol (HTTP) and HTTPS." Old CLI-reference citation file is deleted.
- **AWS-L44-002 (Gone):** `vpc/latest/tgw/what-is-transit-gateway.html`'s own Pricing section confirmed verbatim "You are charged hourly for each attachment on a transit gateway, and you are charged for the amount of traffic processed on the transit gateway." Old Solutions-sample-table citation file is deleted; row 20 now correctly points at the same page as row 19.
- **AWS-L44-003 (Gone):** `vpc/latest/privatelink/privatelink-access-aws-services.html` confirmed verbatim "You are billed for each hour that your interface VPC endpoint is provisioned in each Availability Zone. You are also billed per GB of data processed." This is the canonical VPC PrivateLink guide, not the unrelated IoT dev-guide page.

## Claim-table re-sweep (item 2 from your message)

Spot-checked the writer's re-sweep beyond row 32: rows 4, 19/20, 24, 27, 34 all still carry their full substance in prose (RI discount-sharing toggle in K01; TGW hub definition and now-correct billing claim in K06; interface/gateway endpoint guidance in S03; inter-Region charges in S03/S05; CUDOS Dashboards named in S05). No second instance of the "row 32" defect class (a named AWS feature sitting in the claim table but never named in the prose) turned up in this spot-check. The two new rows (41, CloudFront `Introduction.html`; 42, Global Accelerator `introduction-components.html`) both reach prose as the new HTTP-only discriminator paragraph.

## (c) Question review — 23 questions

**Citations:** every `citationIds` entry across all 23 question files resolves to an existing citation file (checked programmatically) — no missing files.

**Teach-before-test:** confirmed against the current lesson text, not just the writer's mapping table — every key and every distractor's stated failure reason traces to a fact or discriminator actually in `lesson-4-4.json` (NAT gateway/instance trade-off, per-AZ NAT redundancy, DC/VPN/internet, DC and VPN bandwidth tiers, peering/TGW, gateway/interface endpoints plus the new selection rule, CloudFront/Global Accelerator plus the new HTTP-only discriminator and now-named Origin Shield, ALB/NLB/GWLB by layer, Route 53 routing policies vs load balancing/CDN, tag activation, Cost Explorer/Budgets/CUR, API Gateway throttling types). No question needs a fact the lesson doesn't teach — no "Lesson additions requested" this round.

**Numbers in keys:** all verified against source docs — s07-mc (3 Gbps sustained → 10 Gbps dedicated DC tier, correctly picked from the 1/10/100/400 Gbps tiers) and s07-mr (800 Mbps → hosted DC's 50 Mbps–25 Gbps range; 40 Gbps → 100 Gbps dedicated tier; standard VPN tunnel ceiling of 1.25 Gbps correctly rules out choice c) are both internally consistent with the lesson's own cited numbers. No number in any key or rationale contradicts a source doc.

**Distractor-type audit judgment (item asked about):** read all five types tied at the 3-question cap (ALB, NLB, GWLB, NAT Gateway, Global Accelerator) across their nine occurrences. None read as recycled/copy-pasted — each occurrence states a distinct, question-specific reason the option fails (e.g., GWLB is wrong in k03-mr because it has no client-facing static IP, wrong in k04-mc because it's for inspection not egress pricing, wrong in k07-mc because it doesn't choose between Regional endpoints by latency). This is what a 14-bullet networking lesson with a handful of named services looks like; agree with your and AWS's read that the cap-ties are structural, not lazy.

### New findings — stem-paraphrase rule (your item 1)

I read all 23 stems against the lesson's wording, not the advisory script. Three genuinely fail the new rule — a reader can reach the key by spotting a word the stem and only the key share, without knowing the underlying service behavior:

**TEACHER-Q44-001 (Major)** — `q-saa-4-4-k03-mc`.
Stem: "insert a scaling fleet of third-party intrusion-detection appliances so every IP packet crossing a set of VPCs is inspected at one entry point." Key (c): "Place a Gateway Load Balancer in front of the **appliance fleet**." "Fleet" + "appliance(s)" appear in the stem and, of the four choices, only in the key — none of NLB/ALB/Route 53 mention them. This isn't a business scenario in the stem's own words; it restates GWLB's AWS-doc definition ("deploy, scale, and manage virtual appliances," "a single entry and exit point for all traffic") almost feature-for-feature. The writer already fixed the *key* side of this exact question for the same defect (changed "Insert" to "Place") but the stem itself still carries the lesson's distinctive language.
Fix: reword the stem to describe the requirement operationally without "fleet"/"appliance," e.g. "Fenwick Robotics needs every packet between a growing group of VPCs to pass through a set of third-party network-security boxes that AWS scales automatically, before any of it reaches a workload." Keep choices as-is (they no longer need to change).

**TEACHER-Q44-002 (Moderate)** — `q-saa-4-4-k04-mc`.
Stem: "...its two-person ops team has agreed to **patch and manage a device** themselves to get there." Key (d): "Launch a right-sized EC2 NAT instance and manage its **patching**." "Patch/patching" is the lesson's own word for a NAT instance's operational burden ("you accept that you manage its patching, sizing, and failover yourself") and appears only in the stem and the key; none of the three NAT-gateway/GWLB distractors mention patching.
Fix: reword the stem's closing clause to avoid "patch," e.g. "...its two-person ops team has agreed to take on the day-to-day upkeep of a self-run device to get there."

**TEACHER-Q44-003 (Moderate)** — `q-saa-4-4-s06-mr`.
Stem: "gets an unpredictable **burst** of traffic from one internal reporting job every night..." Key (c): "Configure a stage-level **burst limit** sized to absorb the nightly reporting job's traffic pattern." "Burst" is API Gateway's own term (token-bucket "burst limit") and appears only in the stem and the correct choice; none of the other four choices use it.
Fix: reword the stem to use a non-AWS-term synonym, e.g. "gets an unpredictable **spike** of traffic from one internal reporting job every night..."

No other stem showed a unique stem/key word-share; the remaining 20 read as genuine operational paraphrases (e.g. `k02-mc`'s "on pace to exceed... nobody checking a dashboard" for Budgets, `s02-mr`'s clean separation of "dedicated, non-internet path" from the word "Direct Connect," `k07-mc`'s "responds fastest" for latency-based routing) — these match the RULES.md "Good" example pattern.

## Lesson additions requested

None. Every question's key and every distractor's failure reason is already taught in the current lesson text.

Task 4.4: not yet

Overall: concerns
