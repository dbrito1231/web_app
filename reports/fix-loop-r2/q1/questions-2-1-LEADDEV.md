# Task 2.1 questions: Lead Dev pre-review (before the Teacher, AWS and Student reviews)

These are the combined metrics over all 35 files. All pass:
- 6-word openings: 35/35 unique.
- Longest-is-key: 7/23 MC (30%).
- MC keys: a6, b6, c6, d5.
- MR key slots: a5, b5, c4, d5, e5.
- All citations resolve, `verified`, `2026-09-26`.
- 0 letter references.

The metrics pass, but reading the choices shows the batch misses the Amendment 2 bar ("real distractors, each wrong for exactly one requirement") that tasks 1.2 and 1.3 met. So it goes back to the writers before the review round.

## LD-Q21-001 (Medium): strawman distractors

These choices are anti-patterns or non-AWS actions that no candidate would pick. They are not real AWS options that miss one requirement.

| Question | Strawman choices |
|---|---|
| k02-mc | c (engineer changes password manually), d (Transfer Family serving passwords over SFTP) |
| k05-mc | b, d (polling / nightly batch) |
| k06-mc | a, c, d are all "make instances bigger", which is one idea three times |
| k08-mc | a (hand-write Dockerfile), c (leave it on EC2, no containers) |
| k10-mc | a (single monolithic instance), c (DB in web SG), d (route internet to DB) |
| k13-mc | b (EBS "shared informally over the network") |
| k16-mc | b (Lambda with sleep loop), c (cron script polling) |
| s01-mc | b (monolith) |
| s01-mr | b (one shared subnet/SG), e (ephemeral local storage for persistent records) |
| s02-mr | d (manual operator scaling) |
| s03-mc | a (bigger instance), b (merge the services) |
| s03-mr | b (hardcoded private IP), e (shared direct DB connection) |
| s04-mc | c (EC2 "with no container runtime involved") |
| s04-mr | a (self-managed K8s for a short function), c ("no runtime isolation at all"), e (VM image copied manually) |
| s05-mc | d (self-managed K8s kept warm) |
| s06-mr | e (EC2 manually inspecting paths) |
| s07-mr | c (hand-written polling Lambda), d (copying config files with credentials) |

Fix: replace each one with a real, current AWS service or configuration from the same area that satisfies every requirement but one. For example:
- k06: a scheduled action that changes the instance type through a launch template update, or predictive scaling with a vertical resize;
- k10: a two-tier design with the DB in a public subnet, or ALB → Lambda without a data tier;
- k16: Amazon SQS delay queues, or an EventBridge Scheduler chain;
- s03-mr: SQS standard with multiple consumers, or an NLB;
- s07-mr: AWS AppConfig, or Parameter Store SecureString without rotation.

Keep the 15% cap (≤5 of 35 per type across the task).

## LD-Q21-002 (Medium): distractors that explain themselves or give away the answer

These choices carry the reason they are wrong, or echo the stem's requirement, which gives the answer away.

| Question | Choice | Problem |
|---|---|---|
| k01-mc | b | "even though the team does not need to meter or key individual callers" |
| k02-mc | a | "which keeps configuration values but does not rotate them on a schedule" |
| k03-mc | a | "since it is the simplest cache to operate" |
| k11-mr | a, b, d | "must … to guarantee", "must be used": absolutes as tells |
| s04-mr | d | "since there is nothing to containerize" (key gives its own justification) |
| s05-mr | b, d, e | "despite its per-invocation execution limit", "requiring a container image to be built", "since no container image is wanted" |
| s06-mc | d | "which are lost whenever that instance stops or terminates" |

Fix: state each choice neutrally, as a candidate would see it on the exam. The rationale explains why it fails.

## LD-Q21-003 (Low): stems joining two unrelated needs

`s03-mr`, `s04-mr`, `s05-mr` and `s06-mr` each pair two unrelated needs so that one key answers each half. `s06-mr` pairs Lambda with ALB path routing, and its Global Accelerator distractor is for the "event-triggered function". This is allowed for skill objectives, but each distractor must be a plausible answer to one of the two halves. Global Accelerator for an event-triggered function is not. Tighten these so every distractor plausibly answers one half.
