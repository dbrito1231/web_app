# Task 4.4 — AWS reviewer report (Round 2)

## (a) My own Round-1 findings

**AWS-L44-001 — Gone.** `cite-saa-4-4-elbv2-overview` (CLI reference) was split into `cite-saa-4-4-gwlb-overview` (`elasticloadbalancing/latest/gateway/introduction.html`) and `cite-saa-4-4-elb-layers` (`elasticloadbalancing/latest/classic/elb-listener-config.html`). Re-fetched both: the gateway guide states verbatim "A Gateway Load Balancer operates at the third layer of the Open Systems Interconnection (OSI) model, the network layer," and the classic listener guide states "Layer 4 is the transport layer that describes the Transmission Control Protocol (TCP) connection... Layer 7 is the application layer that describes the use of Hypertext Transfer Protocol (HTTP) and HTTPS." Both are prose user-guide pages, not a CLI reference, and both assert exactly the claims attached to them. Confirmed.

**AWS-L44-002 — Gone.** `cite-saa-4-4-transit-gateway` now points to the TGW page's own **Pricing** section instead of the Solutions sample cost table; `cite-saa-4-4-tgw-cost-sample` is deleted. Re-fetched `vpc/latest/tgw/what-is-transit-gateway.html`: its Pricing section states verbatim "You are charged hourly for each attachment on a transit gateway, and you are charged for the amount of traffic processed on the transit gateway" — matches the claim exactly. Confirmed.

**AWS-L44-003 — Gone.** `cite-saa-4-4-vpc-endpoints-interface` now points to `vpc/latest/privatelink/privatelink-access-aws-services.html` instead of the unrelated IoT Managed Integrations page. Re-fetched: its Pricing section states verbatim "You are billed for each hour that your interface VPC endpoint is provisioned in each Availability Zone. You are also billed per GB of data processed." This is a stronger and more specific match than the original "standard PrivateLink rates" quote. Confirmed.

## (b) Second-role check on Teacher's findings

**TEACHER-L44-001 (major) — Gone.** S04 now names the feature: "CloudFront Origin Shield adds an additional caching layer in front of the origin to consolidate requests from the different providers and further reduce origin load." The behavior and the name are now in the same sentence. Confirmed against the already-cited `gamecost02-bp01.html`, which supports the mechanism.

**TEACHER-L44-002 (minor) — Gone.** K03 now reads "Network Load Balancer (NLB) operates at the transport layer (layer 4)..." and "Gateway Load Balancer (GWLB) operates at the network layer (layer 3)...", both spelled out before either abbreviation is used alone later in the section (and later in the Exam tip, and in `q-saa-4-4-k03-mr`'s choices).

**TEACHER-L44-003 (minor) — Gone.** S01 now reads "...keeps one AZ's failure from taking down egress (outbound internet traffic) for the whole VPC."

**Full-sweep spot check (Teacher asked for a re-sweep of all 40 rows, not just row 32):** I re-read the writer's claim-table re-check note and independently re-verified a sample of 6 non-obvious rows against current prose: row 19/20 (TGW hub + billing), row 25/26a/26b (gateway vs interface endpoint pricing — now stated as an explicit selection rule in S03, addressing the second lesson-addition request), row 28 (Global Accelerator static IPs), and the two new rows 41/42 below. All six carry their full claim in prose, not just as a number. No second table-but-not-prose defect found.

**Lesson addition 1 (CloudFront-vs-Global-Accelerator HTTP-only discriminator) — added, mostly supported.** New S04 text: "CloudFront caches and accelerates HTTP and HTTPS content only... because Global Accelerator operates on TCP and UDP traffic generally rather than caching HTTP objects." Citation `cite-saa-4-4-global-accelerator-listener` → `global-accelerator/latest/dg/introduction-components.html` is fully verified: I re-fetched the page's "Listener" definition and it states verbatim "A listener can be configured for TCP, UDP, or both TCP and UDP protocols." — exact match. See **AWS-Q44-001** below for the CloudFront side of this pair.

**Lesson addition 2 (gateway-vs-interface endpoint selection rule) — added, verified.** S03 now states the rule directly ("use a gateway endpoint when the target is Amazon S3 or DynamoDB... use an interface endpoint... for any other AWS service"), backed by the already-verified rows 25/26a/26b. Confirmed.

## New finding

**AWS-Q44-001 (Low)** — Location: S04 lesson prose, "CloudFront caches and accelerates HTTP and HTTPS content only," cited to `cite-saa-4-4-cloudfront-intro` (`AmazonCloudFront/latest/DeveloperGuide/Introduction.html`).
Issue: I re-fetched this page. It states CloudFront "is a web service that speeds up distribution of your static and dynamic web content" — this supports "CloudFront is a web/HTTP-content service" but does not itself assert the stronger "HTTP and HTTPS content **only**" (i.e., it doesn't exclude other protocols). The claim is true (CloudFront has no non-HTTP(S) delivery mode) but the cited quote doesn't carry the exclusivity.
Doc-verified fix: add a second citation to `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HTTPandHTTPSRequests.html` ("How CloudFront processes HTTP and HTTPS requests"), whose scope (HTTP/HTTPS request handling only, with no other protocol described anywhere in the CloudFront developer guide) is the closest documented support for the "only" framing. This is non-blocking: the underlying fact is correct and no question's key or rationale depends on the word "only" — `q-saa-4-4-s04-mc`'s rationale says GA "does not cache HTTP objects," which is independently true and already covered by the verified `cite-saa-4-4-global-accelerator-listener` citation.

## (c) Question review — 23 of 23

All 14 objective bullets have exactly one MC (`-mc`) and, for the 9 that also carry an `-mr`, exactly one MR, matching `lesson-4-4.json`'s `drillIds` (23 entries) and `objectiveIds`. Read every stem, every choice, every rationale, and every citation set against the fixed lesson.

- **Citations:** every question's `citationIds` resolve to an existing citation file (including the four new ones from round 2: `cite-saa-4-4-elb-layers`, `cite-saa-4-4-gwlb-overview`, `cite-saa-4-4-cloudfront-intro`, `cite-saa-4-4-global-accelerator-listener`), each `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`.
- **Teach-before-test:** the key AND the reason every distractor is wrong trace to lesson prose for every question I read, including the two newly-added rules (Origin Shield named in S04; gateway-vs-interface endpoint rule stated in S03) which now directly back `q-saa-4-4-s04-mr` (Origin Shield key) and `q-saa-4-4-s03-mc`/`s03-mr`/`s01-mr` (gateway-endpoint keys).
- **No strawmen:** every distractor is a real, current AWS option that fails the stem's stated requirement on a specific, taught dimension (e.g., `q-saa-4-4-k04-mc`'s "NAT gateway in every AZ" distractor is a real, legitimate pattern that simply doesn't minimize cost for the stated single-subnet, steady-low-traffic scenario — not an anti-pattern no candidate would pick).
- **Paraphrase/echo rule (new for 4.4):** ran the advisory `scripts/stem_echo_check.py 4-4` — 15 of 23 flagged, consistent with the tool's documented over-flagging (15/22 on 4.3 against the Student's 9). I read every flagged pair by hand. All 15 are generic operational or service-name words (`billing`, `email`, `fleet`, `manage`, `daily`, `connectivity`, `availability`, `backup`, `audit`, `dedicated`, `gateway`, `burst`, `region`, `partner`, `separate`) that either name the already-established entity in context (e.g., `q-saa-4-4-s04-mr`'s stem already states CloudFront is deployed, so the key naming "CloudFront Origin Shield" isn't a giveaway) or are common English words shared across multiple choices, not a distinctive technical phrase unique to the key. I separately checked `q-saa-4-4-k06-mc` by hand (stem says "avoid re-architecting the **hub**"): the word "hub" appears in *both* the key ("Transit Gateway hub") and a distractor ("existing hybrid gateway... without a transit **hub**"), so a reader cannot pattern-match on that word alone — they must still know which hub design actually avoids re-architecture. No genuine stem-echo violation found in any of the 23 questions.
- **Distractor diversity / balance / structure:** per the coordinator's pre-check, `q1_batch_check.py 4-4`, `distractor_type_audit.py 4-4`, and `claim_prose_check.py 4-4` all PASS. I independently tabulated key-letter spread: MC keys are a:4 b:4 c:3 d:3 across 14 questions; MR key-pairs are a:4 b:3 c:4 d:4 e:3 across 9 questions (18 slots) — both reasonably even, no letter dominating.

## (d) Numbers in every key — verified

Every numeric figure that determines a correct answer, checked against the same doc pages verified in round 1:

- `q-saa-4-4-s07-mc` key (b): "10 Gbps tier" for a 3 Gbps-and-growing factory link — correct, dedicated Direct Connect tiers are 1/10/100/400 Gbps (`hybrid-networking-lens/aws-direct-connect.html`), 10 Gbps is the right next tier with headroom.
- `q-saa-4-4-s07-mr` key (a): hosted Direct Connect for an 800 Mbps site — correct, hosted range is 50 Mbps–25 Gbps, comfortably covers it; distractor (b) "400 Gbps dedicated" for the same site is correctly rejected as oversized.
- `q-saa-4-4-s07-mr` key (d): "100 Gbps tier" dedicated port for a 40 Gbps site — correct, next dedicated tier above 40 Gbps (10 Gbps would be insufficient); distractor (c) "single standard VPN tunnel" for 40 Gbps is correctly rejected since standard VPN tops out at 1.25 Gbps/tunnel, and distractor (e) "shared 10 Gbps port for both sites" is correctly rejected as undersized for the 40 Gbps site.
- No key in this task states a per-GB, per-hour, ingress/egress, or cross-AZ/cross-Region dollar figure — the only numeric facts driving a key are the Direct Connect/VPN bandwidth tiers above, all of which I re-confirmed match the cited pages' actual tier boundaries and direction (dedicated vs. hosted, standard vs. Large Bandwidth Tunnel). No unit or direction errors found.

## Retired/renamed/closed services

No question or added citation names a retired, closed-to-new-customers, or incorrectly-renamed service. No new finds for the RULES.md list.

Task 4.4: close

Overall: approve

## Round 2 recheck

**Second-role verdicts:**

- **TEACHER-Q44-001 (`k03-mc`) — Gone.** Stem no longer says "fleet" or "appliance" and no longer tracks the GWLB doc definition; it now reads "...pass through a set of third-party network-security boxes that AWS scales automatically...". Only choice (c) still contains "appliance fleet" (in the choice text, which is expected and unchanged), and no stem word is now exclusive to one choice. Re-checked the logic: "every packet... pass through... boxes... before any of it reaches a workload" still rules out NLB (layer-4 connection distribution, not transparent all-IP-packet insertion) and ALB (HTTP/HTTPS only, not "every packet") on facts the K03 lesson section and `cite-saa-4-4-gwlb-overview` teach; Route 53 weighted routing is DNS, not an inspection point. Key (c) is still the unambiguous best answer.
- **TEACHER-Q44-002 (`k04-mc`) — Gone.** "patch/patching" removed from the stem; it now ends "...has agreed to take on the day-to-day upkeep of a self-run device to get there." No word in the stem now matches key (d)'s "manage its patching" exclusively (or at all). Logic re-checked: single subnet, steady/low/predictable traffic, lowest bill, team willing to run the device itself still uniquely signals a self-managed NAT instance over a NAT gateway (fixed hourly charge regardless of low usage) or a misapplied GWLB appliance fleet.
- **TEACHER-Q44-003 (`s06-mr`) — Gone.** "burst" in the stem changed to "spike"; only choice (c) now contains "burst" ("stage-level burst limit"). Logic re-checked: "unpredictable spike... every night" plus "never exceed the account-level throttling limit" still correctly keys to (c) stage-level burst limit and (e) usage-plan quota below the account limit, and still correctly excludes resizing EC2 (a), removing throttling (b), and relying on the fixed account-level limit alone (d).
- **AWS-Q44-001 (own finding) — Gone.** New citation `cite-saa-4-4-cloudfront-http-only` → `AmazonCloudFront/latest/DeveloperGuide/HTTPandHTTPSRequests.html`. Re-fetched the page: it states "CloudFront accepts requests in both HTTP and HTTPS protocols for objects in a CloudFront distribution" and, as the writer's note observes, the entire page frames CloudFront's request handling exclusively in HTTP/HTTPS terms with no other protocol mentioned anywhere in the CloudFront developer guide (consistent with what I found searching the guide in round 2). This is an inference from a page that only discusses HTTP/HTTPS, not an explicit "CloudFront supports HTTP/HTTPS and nothing else" sentence, but combined with the original `cite-saa-4-4-cloudfront-intro` citation and the fact that no key or rationale in this task's 23 questions depends on the literal word "only," this is adequate support. Claim table row 41b's quote ("CloudFront accepts requests in both HTTP and HTTPS protocols for objects in a CloudFront distribution") is verbatim-accurate against the live page.

**Echo re-check (item 3):** Confirmed no residual stem-only-in-key token in `k03-mc` or `k04-mc` (both reworded stems share no distinctive word exclusively with their key). In `s06-mr`, the only stem/choice overlaps left are "region" and "traffic" (in stem: "the account-level throttling limit AWS enforces for the Region"; "unpredictable spike of traffic") — both generic and each appears in more than one choice's implied context (multiple choices deal with "traffic"/timing; account-level vs. usage-plan vs. stage-level all relate to "the Region's" limit), so neither is a single-choice giveaway.

**Claim table re-verification (item 4):** Row 41b (new) confirmed above against the live page. Re-checked rows 41 (`cite-saa-4-4-cloudfront-intro`, "web service...static and dynamic web content") and 42 (`cite-saa-4-4-global-accelerator-listener`, "A listener can be configured for TCP, UDP, or both TCP and UDP protocols") are both still accurate and unaffected by this round's edits — no lesson prose touching either claim changed. No other claim-table rows were touched by the citation change.

Task 4.4: close

Overall: approve

## Round 2 recheck — addendum: `q-saa-4-4-s06-mr` choices b/d replaced

Re-fetched `apigateway/latest/developerguide/api-gateway-request-throttling.html` to verify new choice (b).

1. **Realism check:** Both replacements are real actions a competent architect might actually propose, each failing exactly one stated requirement rather than being a strawman. (b) "Request an AWS Support increase to the Region's account-level throttling limit" is a legitimate, commonly-used lever — it just doesn't give *this API* its own configured ceiling, it raises the shared ceiling for every API in the account/Region. (d) "Leave throttling at the account-level default with no stage or usage-plan settings configured" is the plausible do-nothing/default state — it fails the "configured ceiling" requirement by definition, not because it's an absurd action.
2. **Choice (b) fact-check — confirmed accurate.** The doc states verbatim: "To request an increase of account-level throttling limits per Region, contact the AWS Support Center," and separately, "By default, API Gateway limits the steady-state requests per second (RPS) across all APIs within an AWS account, per Region." This exactly matches the choice's two assertions: the increase path is an AWS Support request, and the limit it changes is account-wide per Region (i.e., shared across every API in that account/Region), not scoped to one API. No factual error.
3. **Rationale accuracy — confirmed.** "Raising the account-level limit through Support moves the ceiling upward for every API in the Region rather than giving this API a ceiling of its own" matches the doc's account-wide, per-Region scope exactly. "Leaving throttling at the account-level default means no stage or usage-plan setting exists to absorb the nightly spike, and the account-level limit is set by AWS and cannot be tuned per API" is also accurate and consistent with (2) — the account-level limit can only be raised account/Region-wide (via choice b's mechanism), never tuned for a single API, which is exactly why neither (b) nor (d) gives Overbrook Data a per-API ceiling the way (c) and (e) do.
4. **No duplication:** (b) is an active request to raise the shared account/Region limit; (d) is passively leaving the default with no additional configuration. Distinct actions, neither overlaps (a) (EC2 resizing, unrelated to throttling), (c) (stage-level burst limit), or (e) (usage-plan quota).

Task 4.4: close

Overall: approve
