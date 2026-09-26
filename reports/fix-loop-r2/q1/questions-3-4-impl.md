# Task 3.4 question-writing implementation report

## Batch-check result

`backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 3-4`:

```
task 3-4: 13 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 8 for 8 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 0/8 = 0%
PASS: MC key positions {'a': 2, 'b': 2, 'c': 2, 'd': 2}
PASS: MR key slots {'a': 1, 'b': 3, 'c': 2, 'd': 2, 'e': 2}
RESULT: PASS
```

Zero FAILs, zero WARNs (no tell-word or retired-service WARNs on any choice).

`backend\.venv\Scripts\python.exe scripts\content_lint.py`: `PASS` (`questions 429 aws 310 tf 119`, `labs 21 + 21`, `lessons 23`).

## Per-question table

| Question | Objective | What it tests | Key | Key — lesson quote | Distractors — lesson quotes for why each is wrong |
|---|---|---|---|---|---|
| `q-saa-3-4-k01-mc` | K01 | Origin Shield vs. cache behaviors vs. Global Accelerator for reducing origin load on a global cache-miss spike | a: Add Origin Shield | "Origin Shield consolidates those requests into a single location before they reach the origin...reduces origin load" | b — "cache behavior matches a request's path pattern...to its own origin, TTL...and viewer protocol policy" (routes paths, doesn't consolidate misses); c — "Global Accelerator...traffic is routed to the healthiest, closest regional endpoint...rather than being cached" (no caching at all); d — region choice affects round-trip time, not the origin-load mechanism Origin Shield fixes |
| `q-saa-3-4-k02-mc` | K02 | VPC CIDR sizing range (/16–/28) and the RFC 1918 recommendation | b: `10.0.0.0/16` | "allowed block size is between a /16 netmask (65,536 IP addresses) and /28 netmask" + RFC 1918 recommendation | a — /8 is outside the /16-to-/28 allowed range; c — right size but not an RFC 1918 private range; d — /30 (4 addresses) is far short of the needed headroom |
| `q-saa-3-4-k03-mc` | K03 | Selecting NLB for UDP/high-throughput/static-IP over ALB, GWLB, or a cross-zone tweak | c: Deploy an NLB | Lesson: NLB "can handle millions of requests per second with microsecond latency because it does not parse the request" | a — ALB "Layer 7 processing...costs some latency" and is HTTP-based, no UDP; b — GWLB "inserts third-party virtual appliances transparently," not client traffic; d — cross-zone load balancing "spread[s] requests evenly," it doesn't add UDP/static-IP support |
| `q-saa-3-4-k04-mc` | K04 | Encrypted, private, high-bandwidth on-prem connectivity: VPN-over-DX vs. plain VPN, plain DX, or PrivateLink | d: Private VPN over DX through a transit gateway | "a private-IP Site-to-Site VPN over Direct Connect through a transit gateway" for "private, high-bandwidth connectivity and encryption in transit" | a — standard VPN "builds an IPsec tunnel over the public internet," capped bandwidth; b — DX alone "is not encrypted"; c — PrivateLink "exposes one specific service," not a whole network |
| `q-saa-3-4-s01-mc` | S01 | Route table (not security group) as what makes a subnet reachable from the internet; subnet-per-AZ | a: Private subnets, no IGW route, 3 AZs | "a route table entry pointing at an internet gateway...is what actually gives a subnet its public, private...reachability" | b — security group filters instances, not the underlying route; c — "a subnet maps to exactly one Availability Zone," so one subnet can't span three; d — NAT gateway gives an outbound path toward the internet gateway, conflicting with "never reachable" |
| `q-saa-3-4-s02-mc` | S02 | VPC CIDR blocks can't be resized, only supplemented with a secondary block | b: Add a secondary CIDR block | "can only be supplemented with additional, non-overlapping secondary CIDR blocks" | a — "cannot be resized after creation"; c — subnets "cannot overlap"; d — peering "connects two VPCs' networks," doesn't lend address space |
| `q-saa-3-4-s03-mc` | S03 | Wavelength (inside carrier network) vs. Local Zone, standard Region, CloudFront for ultra-low-latency compute placement | c: Run on Wavelength | "AWS Wavelength...embeds AWS infrastructure inside a telecommunications provider's 5G network itself" | a — Local Zone is "an AWS-operated metro location," not inside the carrier's own network; b — standard Region is farther, fails the latency target; d — CloudFront "caching...does not run the inference compute itself any closer" |
| `q-saa-3-4-s04-mc` | S04 | Load balancer selection (NLB) for a TCP protocol needing lowest latency + static per-AZ IP, vs. ALB, Route 53 weighted routing, Classic LB | d: Deploy an NLB | Lesson: NLB fits "the lowest achievable added latency" and "a static IP per AZ" for a custom TCP protocol | a — ALB "Layer 7 processing" overhead, no inherent static per-AZ IP; b — Route 53 weighted routing "splits traffic at the DNS layer," not a load-balancer-level fix; c — Classic LB is "the previous generation," doesn't match NLB's profile |
| `q-saa-3-4-k03-mr` | K03 | Cross-zone load balancing for an uneven target split + NLB for a high-throughput tier, vs. adding a 2nd ALB, GWLB, or dereg delay | a, b | Cross-zone: "spread requests evenly across targets in every enabled AZ rather than only the targets in the AZ that received the request"; NLB: "can handle millions of requests per second" | c — a 2nd ALB is a new load balancer, doesn't fix the existing one's imbalance; d — GWLB is for "third-party virtual appliances," not client traffic; e — deregistration delay is unrelated to cross-AZ distribution |
| `q-saa-3-4-s01-mr` | S01 | VPN-as-DX-backup + CloudFront/Global Accelerator for global entry, vs. VPC peering to on-prem, cross-Region TGW peering, or NAT for inbound | c, d | "a common resilience pattern also keeps a Site-to-Site VPN as an automatic backup path"; Global Accelerator/CloudFront give "a fixed entry point closest to your users" | a — VPC peering only connects two VPCs, not an on-prem network; b — TGW peering connects "transit gateways in different Regions," unrelated to on-prem failover; e — NAT gateway is for outbound access, not inbound global routing |
| `q-saa-3-4-s02-mr` | S02 | Transit Gateway as the scalable hub for both VPC-to-VPC and DX-to-many-VPCs, vs. full-mesh peering, hub-via-peering, or per-VPC DX | b, e | "adding the Nth VPC means one new attachment instead of N-1 new peering connections"; TGW "fan[s] that single connection out to many VPCs" | a — full mesh "becomes hard to manage past a handful of VPCs"; c — relies on peering's transitive routing, but "VPC peering does not support transitive peering relationships"; d — one DX connection per VPC repeats the dedicated line instead of fanning one out |
| `q-saa-3-4-s03-mr` | S03 | Private subnets (no IGW route) + Local Zone for a general metro audience, vs. SG-only public subnets, Wavelength (carrier mismatch), or DX for end users | c, e | Private subnet/no-IGW-route quote (same as S01-mc); Local Zone "extends an AWS Region to a location...closer to a population center...for latency-sensitive workloads" | a — public subnet still has the IGW route, SG doesn't remove it; b — Wavelength needs a carrier-network tie-in the scenario doesn't state; d — Direct Connect connects on-premises networks, not a public audience |
| `q-saa-3-4-s04-mr` | S04 | Cross-zone load balancing + enhanced networking (K03/3.2 callback) to fix imbalance and packet loss, vs. idle timeout, single-AZ, or target-type change | b, d | Cross-zone quote (same as K03-mr); "enhanced networking...raises the packet-per-second ceiling" (3.2 S03 callback) | a — idle timeout is connection-duration, unrelated to packet loss; c — single-AZ removes multi-AZ resilience; e — target type (instance vs. IP) doesn't raise the PPS ceiling |

## Distractor-type table

Each row is one confusable pair taught in Lesson 3.4 (or its 2.1/3.2 callbacks). No type is used more than twice across the 13 questions, per the "at most 2 per distractor type" instruction.

| # | Distractor type | Used in | Count |
|---|---|---|---|
| 1 | Cache behavior (path routing) vs. Origin Shield (origin-load reduction) | k01-mc.b | 1 |
| 2 | Global Accelerator vs. CloudFront caching | k01-mc.c | 1 |
| 3 | Region placement (latency) vs. Origin Shield (origin load) | k01-mc.d | 1 |
| 4 | VPC CIDR block too large / outside allowed range (/8) | k02-mc.a | 1 |
| 5 | RFC 1918 private range vs. public/documentation range | k02-mc.c | 1 |
| 6 | CIDR too small for stated headroom | k02-mc.d | 1 |
| 7 | NLB (L4/UDP/throughput) vs. ALB (L7/HTTP) | k03-mc.a, s04-mc.a | 2 |
| 8 | GWLB (transparent appliance insertion) vs. NLB/ALB (client-facing) | k03-mc.b, k03-mr.d | 2 |
| 9 | Cross-zone load balancing vs. an unrelated load-balancer action (2nd LB) | k03-mc.d, k03-mr.c | 2 |
| 10 | Classic Load Balancer (legacy) vs. current-generation NLB/ALB | s04-mc.c | 1 |
| 11 | Route 53 weighted routing (DNS layer) vs. load-balancer-level fix | s04-mc.b | 1 |
| 12 | Site-to-Site VPN over the internet vs. Direct Connect (no-internet requirement) | k04-mc.a | 1 |
| 13 | Direct Connect alone (unencrypted) vs. VPN-over-DX | k04-mc.b | 1 |
| 14 | PrivateLink (single service) vs. full on-prem network connectivity | k04-mc.c | 1 |
| 15 | Security group (instance-level) vs. route table (subnet reachability) | s01-mc.b, s03-mr.a | 2 |
| 16 | Subnet-to-AZ mapping (one subnet = one AZ) | s01-mc.c | 1 |
| 17 | NAT gateway (outbound path exists) vs. fully private subnet | s01-mc.d | 1 |
| 18 | VPC CIDR block cannot be resized | s02-mc.a | 1 |
| 19 | Subnet/CIDR overlap not allowed | s02-mc.c | 1 |
| 20 | VPC peering misused for address-space borrowing | s02-mc.d | 1 |
| 20b | VPC peering misused to reach an on-premises network | s01-mr.a | 1 |
| 21 | VPC peering non-transitive vs. hub-via-peering misconception | s02-mr.c | 1 |
| 22 | Full-mesh VPC peering doesn't scale vs. Transit Gateway | s02-mr.a | 1 |
| 23 | Cross-Region Transit Gateway peering vs. on-premises VPN backup | s01-mr.b | 1 |
| 24 | Per-VPC Direct Connect vs. Transit Gateway fan-out | s02-mr.d | 1 |
| 25 | NAT gateway (outbound-only) vs. CloudFront/Global Accelerator (inbound edge entry) | s01-mr.e | 1 |
| 26 | Local Zone vs. Wavelength context mismatch (either direction) | s03-mc.a, s03-mr.b | 2 |
| 27 | Standard Region/AZ vs. edge placement (Local Zone/Wavelength) for latency | s03-mc.b | 1 |
| 28 | CloudFront caching vs. compute placement | s03-mc.d | 1 |
| 30 | Reducing to a single AZ sacrifices stated multi-AZ resilience | s04-mr.c | 1 |
| 31 | Real but unrelated load-balancer setting (idle timeout / dereg delay) vs. the actual fix | k03-mr.e, s04-mr.a | 2 |
| 32 | Direct Connect (on-premises link) misapplied to a public end-user audience | s03-mr.d | 1 |
| 33 | NLB target-type change (instance vs. IP) vs. enhanced networking | s04-mr.e | 1 |

No distractor invokes a retired or closed service (Copilot, Snow Family, FSx File Gateway, QLDB, etc.) — confirmed by the `RETIRED` regex check built into the writing script (zero matches) and by `q1_batch_check.py`'s own retired-service scan producing no WARNs.

## Notes for reviewers

- All 13 `objectiveIds`, `type`, `module`, and `selectCount` values were left unchanged from the placeholder files, as required.
- Every key and every distractor's wrongness is taught in Lesson 3.4 itself, except the ALB/NLB/GWLB layer distinction and cross-zone load balancing (taught in Lesson 2.1, referenced back to by Lesson 3.4's K03/S04 sections) and the enhanced-networking callback (Lesson 3.2 S03, referenced back to by Lesson 3.4's S04 section) — both call-backs are explicit in the lesson body, and the corresponding citation ids (`cite-saa-2-1-alb-elb`, `cite-saa-2-1-classic-lb-intro`, `cite-saa-2-1-alb-cross-zone`) are attached to the relevant questions.
- No two stems share their first six words (script-verified); no MC choice is the longest option (0/8); MC keys are evenly spread a:2/b:2/c:2/d:2; MR key slots touch all five letters (a:1, b:3, c:2, d:2, e:2).
- No tell words (`since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`, `so that`) appear in any choice text — verified programmatically before writing the files, and confirmed by zero WARNs in `q1_batch_check.py`.
