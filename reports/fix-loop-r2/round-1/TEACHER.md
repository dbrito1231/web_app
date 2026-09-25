# Teacher review — run-loop-r2 / round-1 (R3, R6)

Role: Teacher (read-only). Wrote only this file. No installs, migrations, builds, git, AWS API, or credentialed Terraform.

Date: 2026-09-25

## Scope

| ID | Target | Question |
|----|--------|----------|
| **R3** | `content/questions/*.json` | Do practice stems still use a small set of repeated openings, with many choices saying "Apply the objective directly"? (Recorded as **not a fix** — confirm, do not treat eight reworded openings as an exam-style rewrite.) |
| **R6** | `content/lessons/lesson-4-2.json`, `lesson-4-3.json`, `lesson-4-4.json` | Does each bullet cite the correct official doc for its own topic, or do bullets still share one generic citation sentence? Sample ≥6 bullets. |

## R3

**Verdict: Not a fix (expected)**

Counts from all **429** question JSON files under `content/questions/`:

### Repeated stem openings

Stems still use a small template bank. Numbered openings for the SAA-style bank (objective pasted after a colon / framing clause):

| # | Opening (normalized) | Count |
|---|----------------------|------:|
| 1 | Select TWO actions that support this requirement: | 156 |
| 2 | A teammate asks how to meet this requirement: | 35 |
| 3 | Pick the action that …: | 31 |
| 4 | The workload needs this …: | 30 |
| 5 | An exam scenario centers on: | 28 |
| 6 | You must choose one approach for: | 28 |
| 7 | During an architecture review …: | 27 |
| 8 | Which action is the right fit for this requirement: | 26 |
| 9 | In a design review …: | 21 |

- **Eight openings (rows 1–8):** **361** stems  
- **Nine openings (rows 1–9):** **382** stems  
- Remainder: Terraform **"Quick check …"** (~37), **"HCP Terraform practice check …"** (8), plus 2 lab-safety / CLI outliers  

Eight (or nine) reworded wrappers around the objective text are **not** an exam-style rewrite. Scenario depth, distractor quality, and rationale quality remain template-shaped.

### "Apply the objective directly"

- Choice text containing **"Apply the objective directly"**: **263** hits  
- Distinct question files with that choice: **263** of 429 (~61%)  

Correct answers commonly rest on that phrase plus the objective wording; distractors still recycle the same three safety anti-patterns (root user, leave hourly resources running, treat budget alerts as a hard stop).

**Conclusion:** R3 remains **Not a fix**, as expected. Counts confirm the small opening set and widespread "Apply the objective directly" choices.

## R6

**Verdict: Fail**

Lessons 4.2–4.4 still do **not** give each bullet its own topic-correct official doc. Pattern:

1. Every knowledge bullet repeats the same **Tradeoffs** paragraph ending in: *"Use this lesson's citation link at the bottom before you lab."*  
   - Hits: **9** (4.2) + **9** (4.3) + **7** (4.4) = **25**  
   - Unique Tradeoffs text per lesson: **1**  
2. Skill bullets share one **"Applied practice"** sentence (no per-bullet URL).  
3. Each lesson has a **single** bottom citation line and a single `citationIds` entry pointing at one pricing marketing URL:

| Lesson | `citationIds` | Shared bottom URL |
|--------|---------------|-------------------|
| 4.2 | `cite-4-2` | https://aws.amazon.com/ec2/pricing/ |
| 4.3 | `cite-4-3` | https://aws.amazon.com/rds/pricing/ |
| 4.4 | `cite-4-4` | https://aws.amazon.com/vpc/pricing/ |

Citation JSON files mirror those same three URLs only.

### Sample (≥6 bullets) — topic vs shared citation

| Bullet | Topic (lesson text) | Shared citation | Topic-appropriate official doc (MCP search; not invented) | Fit? |
|--------|---------------------|-----------------|-----------------------------------------------------------|------|
| SAA-4.2-K01 | Cost allocation tags / multi-account billing | EC2 pricing | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html | No |
| SAA-4.2-K06 | Hybrid compute / AWS Outposts | EC2 pricing | https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html | No |
| SAA-4.3-K03 | Caching strategies | RDS pricing | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/BestPractices.html | No |
| SAA-4.4-K03 | Load balancing / ALB | VPC pricing | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html | No |
| SAA-4.4-K05 | Network connectivity (private/dedicated lines, VPNs) | VPC pricing | https://aws.amazon.com/compare/direct-connect-and-vpn/ (also Direct Connect / Site-to-Site VPN user guides) | No |
| SAA-4.4-S04 | CDNs and edge caching | VPC pricing (lesson-level only; skill has no bullet URL) | https://aws.amazon.com/cloudfront/getting-started/ | No |

Replacing the old "Cite official docs before labbing" phrase with the generic "lesson's citation link" sentence does **not** satisfy per-bullet, topic-correct citations. One domain pricing page per lesson is still the wrong doc for most bullets.

**Conclusion:** R6 **Fail**.

## New issues (Low+)

| Severity | Finding | Notes |
|----------|---------|-------|
| Low | Ninth stem opening ("In a design review …", 21 stems) sits beside the documented "eight openings" set | Still template reuse; reinforces R3 Not a fix rather than a new defect class |
| Low | Skill bullets in 4.2–4.4 have no citation sentence at all (only the shared lesson footer) | Same root cause as R6; no separate CR needed if R6/CR-0015 covers per-bullet URLs |

No Medium/High issues beyond the scoped R3/R6 findings.

## Verdicts (summary)

| ID | Verdict |
|----|---------|
| **R3** | **Not a fix (expected)** — 361–382 stems on 8–9 openings; 263 "Apply the objective directly" choices |
| **R6** | **Fail** — bullets still share one generic citation sentence + one lesson pricing URL; sampled bullets do not match topic-correct official docs |
