# Teacher pre-validation — final sitting items 1–4 (2026-10-01)

Saved by the Lead Dev (condensed). The Teacher read the plan, AGENTS.md, lessons 3.3, 3.5, 4.4, tf-g2, tf-g3, tf-g4, tf-g6, the seven stems, the four 3.5 questions, the RULES closed list and the 4.2-s05 exercise. It edited nothing and ran nothing.

## Item 2, CR-0021
lesson-tf-g3 contains no "sensitive" or "secret" text. Replace "Treat any state file containing sensitive or ephemeral-adjacent resources as itself sensitive, per group 3's state-security guidance." with:

> Treat any state file as itself sensitive: group 2 teaches that local state is plain JSON, not encrypted, so it "can contain sensitive values" in readable text, and group 6's Warnings add that state "contains extremely sensitive information" and must never be committed to version control.

Fallback, if the quotes are too long for the bullet: "Treat any state file as itself sensitive, as groups 2 and 6 teach: state is plain text that can contain secrets and must never be committed to version control."

## Item 4, LD-Qg7-002 (append after the existing final full stop)

| File | Append |
|---|---|
| q-tf-004-1a-mr | Which two observations provide that evidence? |
| q-tf-004-1b-mr | Which two actions meet both needs? |
| q-tf-004-1c-mr | Which two approaches meet this goal? |
| q-tf-004-2a-mr | Which two statements about the constraints are correct? |
| q-tf-004-2b-mr | Which two statements are correct? |
| q-tf-004-2d-mr | Which two statements describe those jobs? |
| q-tf-004-4a-mc | Which approach should they use? |

## Item 1, CR-0019 (if the closure is confirmed)
- Ray appears in lesson 3.5 **K04 and S05** and in the note of `cite-saa-3-5-glue-job-engines`. Drop it from the engine list ("one of two engines") and add it to the RULES closed list.
- Replacement distractors:
  - k04-mr d: "An AWS Glue Python shell job for the schema discovery"
  - k07-mr b: "AWS DataSync for delivering the copy to S3"
  - s01-mc c: "Run an AWS Glue crawler so each analyst group sees only its own tables"
  - s04-mc d: "Schedule an AWS Glue DataBrew job that writes a CSV extract to S3 each morning"
- Avoid MSK for k07-mr, and avoid Athena CTAS or EMR Serverless for s04.

## Item 3, D6-FU
- **4.4 K05 (do):** draft "When the connection ends on a Transit Gateway with equal-cost multi-path (ECMP) routing enabled, both tunnels can carry traffic at once; otherwise treat the second tunnel as redundancy." Pending technical confirmation.
- **3.3 S01 (do):** draft "...and monitor replica lag with a CloudWatch alarm on the replica-lag metric, since a replica that falls too far behind can return noticeably stale data to read-only clients." Metric names pending technical confirmation.
- **4.2-s05 r7 (do):** draft label "Each new fleet is sized to the vCPUs and memory its stated utilisation requires, with only the headroom the record states, and the vCPU and GiB totals before and after are stated for both services." This is a rubric change and needs Teacher re-validation.
- **4.4 Regional NAT gateway (skip):** it would blur the taught "one NAT gateway per AZ" exam signal. Log it as an optional future CR.

**Verdict: approve plan with these concerns folded in** — fix both Ray mentions; use the CR-0021 wording above; do not ship the K05 and 3.3 wordings until the technical reviewer confirms them; Teacher re-validates the r7 rubric edit; skip the Regional NAT gateway item.
