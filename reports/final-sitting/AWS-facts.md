# Technical review — AWS facts for CR-0019 and D6-FU (2026-10-01)

Saved by the Lead Dev (condensed). All pages were fetched with curl; no WebFetch was used.

## CR-0019: confirmed
- https://docs.aws.amazon.com/glue/latest/dg/awsglue-ray-jobs-availability-change.html: "we decided to close AWS Glue for Ray to new customers starting April 30, 2026." and "Existing customers can continue to use the service as normal."
- https://docs.aws.amazon.com/glue/latest/dg/ray-jobs-section.html carries the banner "AWS Glue for Ray is no longer open to new customers."
- The status is "closed to new customers", not deprecated, and no end-of-support date was seen. how-it-works-engines.html (the K04 cite target) still lists Ray with no banner, so the cite note should say so. Python shell ("on a single Amazon EC2 instance") has no closure notice.
- Proposed RULES closed-list entry: "AWS Glue for Ray: closed to new customers (2026-04-30)."
- Proposed replacements: Glue Python shell in all four questions. **Lead Dev ruling:** use the Teacher's four varied replacements instead. Python shell in four of task 3.5's 24 questions would exceed the 15% distractor-type cap.

## D6-FU 4.4 K05: supported, with conditions
- vpn-limits.html: "you can use ECMP to get higher VPN bandwidth by aggregating multiple VPN tunnels." and "ECMP is not supported on VPN connections that use static routing."
- VPNTunnels.html: "Traffic from AWS to the on-premises network prefers one of the tunnels."
- "Both tunnels of one connection" is **not confirmed** word for word; the docs say "multiple tunnels".
- Doc-backed sentence: "By default AWS-to-on-premises traffic prefers one tunnel; with a transit gateway, dynamic (BGP) routing and ECMP enabled, multiple tunnels can carry traffic at once, which raises throughput beyond the 1.25 Gbps of a single tunnel."

## Optional items
- **3.3 S01 ReplicaLag alarm:** backed by two pages. USER_ReadRepl.Monitoring.html says "You can monitor replication lag in Amazon CloudWatch by viewing the Amazon RDS ReplicaLag metric." creating_alarms.html says "You can create a CloudWatch alarm that sends an Amazon SNS message when the alarm changes state." No single page states "alarm on ReplicaLag". Recommendation: do it, but only as a half-sentence.
- **4.4 Regional NAT gateway:** this exists. nat-gateways-regional.html says "A regional NAT gateway automatically expands across Availability Zones based on your workload presence." Recommendation: skip, because the lesson teaches zonal NAT gateways per AZ.
- **4.2-s05 r7:** the issue is confirmed. The rubric item is a floor only, so an oversized fleet passes. Fix (AWS-DE3-021): append ", and neither fleet keeps more vCPUs or memory than its utilisation plus the headroom the record states".
