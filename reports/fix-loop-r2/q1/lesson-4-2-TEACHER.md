# Teacher review: lesson 4.2 (round 1)

Saved by Lead Dev from the Teacher's reply (`AGENTS.md`: Teacher is read-only and writes no files).

- **Claim-table verification completed (16 rows spot-checked):** rows `1, 2, 6, 7, 12, 13, 14, 19, 20, 22, 23, 35, 39, 45, 47, 50`.
- **Rows that pass as written:** `1, 2, 6, 7, 12, 13, 14, 19, 20, 23, 35, 45, 47, 50` (quotes are verbatim and support claim).
- **Rows with concern:** `22` (quote is verbatim but does not support the specific claim text), `39` (quote is verbatim, but claim wording is overly broad without scope caveat now present in docs).
- **MCP method compliance:** used `mcp-exec` with `search_documentation` and `read_documentation`; used WebFetch fallback for `aws.amazon.com` pages (`fargate`, `c7g`, `localzones`), per RULES.

## Coverage and pedagogy

- All 15 objectives (`K01-K09`, `S01-S06`) are present in order and each has a dedicated `###` section.
- High-confusion contrasts are explicitly taught: Spot vs RI vs Savings Plans vs On-Demand; Compute vs EC2 Instance Savings Plans; horizontal vs vertical; stop vs hibernate; ALB vs NLB vs GWLB; Lambda vs Fargate vs EC2; Outposts vs Local Zones vs Wavelength.
- Section flow is sensible for a new learner (cost controls -> infrastructure placement -> purchasing -> runtime/service choice -> scaling -> scenario skills).
- Beginner clarity is mostly good, but a few terms (`SLOs`, `blast radius`, `control plane`) appear without quick plain-language definition.

## Exam-tip check

- Every objective section ends with an `**Exam tip:**` line.
- Tips are mostly discriminators, not simple restatements; no critical tip-quality failures found.

## Teach-before-test readiness by objective

- `SAA-4.2-K01` - **Gap** (important facts in claim table are not fully taught in prose; see findings).
- `SAA-4.2-K02` - Ready.
- `SAA-4.2-K03` - Ready.
- `SAA-4.2-K04` - Ready.
- `SAA-4.2-K05` - Ready.
- `SAA-4.2-K06` - Ready.
- `SAA-4.2-K07` - Ready.
- `SAA-4.2-K08` - **Gap** (timeout default/min-max nuance not fully taught; see findings).
- `SAA-4.2-K09` - Ready.
- `SAA-4.2-S01` - Ready.
- `SAA-4.2-S02` - Ready.
- `SAA-4.2-S03` - Ready.
- `SAA-4.2-S04` - Ready.
- `SAA-4.2-S05` - Ready.
- `SAA-4.2-S06` - Ready.

## Format check (lesson markdown subset)

- Uses required `###` objective sections and bullet style.
- **Violation:** lesson begins with `## Cost-optimized compute`; RULES restrict headings to `###`/`####` only.

## Findings

- `TEACHER-L42-001` - **moderate**
  - **Location:** `SAA-4.2-K04`, claim table row 22: `"Reserved Instances terms are one or three years"` with quoted text `"payment options are available for Reserved Instances"`.
  - **Issue:** Quote is verbatim but does not support the claim being asserted.
  - **Doc-verified fix:** replace quote in claim table row 22 with exact support text from same doc: `"You can purchase a Reserved Instance for a one-year or three-year commitment"`.
  - **URL:** `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html`

- `TEACHER-L42-002` - **moderate**
  - **Location:** `SAA-4.2-K01`, phrase: `"discount sharing is on by default"`
  - **Issue:** Teach-before-test gap: lesson does not teach that RI discount sharing can be turned off, which is a common distractor discriminator in multi-account billing questions.
  - **Doc-verified fix (add exact sentence):** `For Reserved Instances in AWS Organizations, the management account can turn discount sharing off when chargeback policy requires account-level isolation.`
  - **URL:** `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html`

- `TEACHER-L42-003` - **low**
  - **Location:** `SAA-4.2-K01`, phrase: `"apply tags ... then separately activate those keys"`
  - **Issue:** Teach-before-test gap for timing distractors; activation delay numbers in claim table are not taught in lesson text.
  - **Doc-verified fix (add exact sentence):** `After you create and apply user-defined tags, it can take up to 24 hours for tag keys to appear for activation and up to another 24 hours to activate.`
  - **URL:** `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html`

- `TEACHER-L42-004` - **low**
  - **Location:** `SAA-4.2-K08`, phrase: `"Lambda has a maximum timeout of 900 seconds for standard functions"`
  - **Issue:** Teach-before-test gap: default timeout value is missing, making one common distractor family currently unfair.
  - **Doc-verified fix (add exact sentence):** `Lambda timeout defaults to 3 seconds, and for standard functions you can set it from 1 to 900 seconds (15 minutes).`
  - **URL:** `https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html`

- `TEACHER-L42-005` - **moderate**
  - **Location:** lesson opening heading: `"## Cost-optimized compute"`
  - **Issue:** Format noncompliance with RULES markdown subset (`###`/`####` headings only).
  - **Doc-verified fix:** change this heading to `### Cost-optimized compute` or remove heading and keep plain intro text.
  - **URL:** `reports/fix-loop-r2/q1/RULES.md` (binding format rule)

- `TEACHER-L42-006` - **low**
  - **Location:** `SAA-4.2-K09`, phrase includes `"SLOs"` and `"blast radius"` without definition
  - **Issue:** Minor pedagogy gap for no-background learners; terms appear before being learner-defined in this lesson.
  - **Doc-verified fix (add exact sentence):** `In this lesson, treat SLO as the target service quality (for example, response time and uptime) and blast radius as the size of impact when one component fails.`
  - **URL:** `https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_multiaz_region_system.html` (fault-isolation framing supports the concept)

Lesson 4.2: not yet
Overall: concerns

---

## Lead Dev note on TEACHER-L42-005 (disputed, not sent to the writer)

All 22 lessons in `content/lessons/`, including the 11 already reviewed and closed
(1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1), open with a single `##`
lesson title before the `###` objective sections. Lesson 4.2 follows that
established, approved pattern exactly.

Applying this finding to 4.2 alone would make it the only lesson in the workbook
with a different title level. Lead Dev is therefore **not** sending L42-005 to the
writer. The underlying issue is that the RULES.md markdown-subset line reads as
`###`/`####` only, which does not describe what every approved lesson actually does.

Proposed resolution, for the Teacher to rule on in round 2: amend RULES.md to read
"one `##` lesson title, then `###`/`####` headings" rather than change 4.2. If the
Teacher instead holds that `##` is wrong, that is a workbook-wide change affecting
22 lessons and needs its own plan and user approval, not a one-lesson edit here.
