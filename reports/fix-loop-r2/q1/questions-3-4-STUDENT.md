# Student Fairness Review: Task 3.4 Questions

## Summary Table

| Q | My Answer | Reason (before reveal) | Correct? | Fair? | Notes |
|---|-----------|------------------------|----------|-------|-------|
| Q1 | a | Origin Shield consolidates cache misses to reduce origin load | ✓ | ✓ | Clear lesson mechanism; wrong answers are genuinely wrong |
| Q2 | b | 10.0.0.0/16 fits need, within /16-/28 AWS limits, RFC 1918 | ✓ | ✓ | Lesson explicitly states /16 is max size; /8 violates that |
| Q3 | c | NLB: millions of packets/sec, UDP support, static IP per AZ | ✓ | ✓ | No ambiguity; ALB doesn't support UDP, GWLB is for appliances |
| Q4 | a, b | Cross-zone fixes ALB imbalance; NLB for high-throughput tier | ✓ | ✓ | Two distinct problems, two distinct solutions taught in lesson |
| Q5 | d | Private VPN over DX meets encryption, bandwidth, no-internet needs | ✓ | ✓ | Exact scenario from lesson ("VPN over Direct Connect through TGW") |
| Q6 | a | Private subnets with no IGW route; route table, not SG, controls reachability | ✓ | ✓ | Distinguishes route table from security group; subnet-AZ mapping clear |
| Q7 | c, d | VPN as DX backup; CloudFront/GA for global entry points | ✓ | ✓ | Lesson explicitly covers both patterns; choices are clean |
| Q8 | b | Primary CIDR can't be resized; add secondary non-overlapping block | ✓ | ✓ | Constraint is stated plainly; no tricks |
| Q9 | b, e | Transit Gateway for scaling VPCs; DX gateway attachment | ✓ | ✓ | Both taught as scaling solutions; full mesh is clearly inferior |
| Q10 | c | Wavelength embedded in carrier's 5G network (exact lesson language) | ✓ | ✓ | Local Zone and standard Region are teaching foils, not traps |
| Q11 | a, e | NAT needs public subnet + IGW route; Local Zone for gaming | ✓ | ✓ | NAT placement is unambiguous; Wavelength vs Local Zone distinction clear |
| Q12 | d | NLB for custom TCP, static IP per AZ, lowest latency | ✓ | ✓ | No gray area; ALB adds Layer 7 overhead; Classic LB is deprecated |
| Q13 | b, d | Cross-zone for uneven distribution; enhanced networking for packet performance | ✓ | ✓ | Both mechanisms are taught; wrong answers don't fix real problem |

## Fairness Assessment

**Fairness: 13/13 = 100%**

## Details

### What went well
- Every question is answerable from the lesson alone—no AWS knowledge beyond what was taught required.
- Each correct answer has only one defensible choice (or choice pair in multi-select).
- No "longer answer = right answer" wording giveaway.
- Wrong answers are genuinely wrong, not trick answers designed to penalize a careful reader.
- Explanations matched the lesson and teaching intent precisely.

### Anything confusing
None. The lesson's structure (K01–K04 for concepts, S01–S04 for scenarios) maps cleanly to the questions. Terminology is consistent (e.g., "cross-zone load balancing" appears in both lesson and questions).

### Notable teaching moments
- Q2 clarifies AWS's /16-to-/28 limit for VPC sizing (rules out /8 cleanly).
- Q5 drives home "VPN over Direct Connect" as the encryption + private-line combo.
- Q6 reinforces that route tables (not security groups) determine public/private.
- Q11 distinguishes Local Zone (metro, AWS-operated) from Wavelength (inside carrier's 5G).

---

**Task 3.4: close**

**Overall: approve**
