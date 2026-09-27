# Teacher round 1 — lesson-tf-g1 / lesson-tf-g2

## Claim rows verified (7, WebFetch on developer.hashicorp.com)

| Row | Lesson | Quote checked | Result |
|---|---|---|---|
| g1 #1 | g1 | "Terraform is an infrastructure as code tool..." (/terraform/intro) | Verbatim match |
| g1 #3 | g1 | "declarative... describe the end state" (/terraform/intro) | Verbatim match |
| g1 #9 | g1 | "orchestrate an AWS and OpenStack cluster simultaneously... Cloudflare and DNSimple" (/terraform/intro/vs/cloudformation) | Verbatim match |
| g2 #4 | g2 | `~> 1.0.4` allows 1.0.5/1.0.10 not 1.1.0 (/terraform/language/expressions/version-constraints) | Verbatim match |
| g2 #8 | g2 | "ensure Terraform always installs the same provider versions..." | Quote is verbatim, but lives on **/terraform/language/providers/requirements** (Version Constraints section), not on the cited page `/terraform/cli/commands/providers/lock`. That page has no such sentence. **Citation URL is wrong** — see TEACHER-Lg2-001. |
| g2 #16 | g2 | "provider block without an alias argument is the default configuration" (/terraform/language/providers/configuration) | Verbatim match |
| g2 #22 | g2 | "stores each workspace's state in a local file named `terraform.tfstate`" (/terraform/language/state) | Verbatim match |

All other rows spot-checked by eye against prose (all 11 g1 rows and all 22 g2 rows) do make it into the lesson body — no repeat of the "claim table has it, prose doesn't" pattern from 4.3/4.4.

## Findings

- **TEACHER-Lg2-001** (moderate) — `content/citations/cite-tf-g2-providers-lock.json`: `url` is `https://developer.hashicorp.com/terraform/cli/commands/providers/lock` (the CLI command reference for `terraform providers lock`). The quoted sentence backing claim row 8 is not on that page. It is on `https://developer.hashicorp.com/terraform/language/providers/requirements`, in the "Version Constraints" section, verified verbatim by WebFetch. Fix: change `url` to `https://developer.hashicorp.com/terraform/language/providers/requirements` and `title` to something like "Provider Requirements — Version Constraints" (or re-quote from `/terraform/language/files/dependency-lock`, but that page does not contain this exact sentence, so the requirements page is the correct citation).
- **TEACHER-Lg2-002** (minor) — "workspace" is used twice in the 2d prose ("your workspace's managed infrastructure," "Terraform stores each workspace's state...") but is never defined. Terraform workspace has a specific technical meaning (the current named state environment) distinct from a plain "project," and it is on the AGENTS.md jargon-watch list by implication (state-adjacent term used to make a decision about where state lives). Fix: add a short parenthetical at first use, e.g. "(a workspace is the working directory's current state environment; named workspaces are a later objective)."
- **TEACHER-Lg2-003** (minor) — "module" appears once in 2c ("...individual resources, data sources, or modules") with no definition anywhere in g1 or g2, even though it is one of the terms the round explicitly asks me to check. Fix: add a brief parenthetical, e.g. "modules (reusable packaged Terraform configurations, covered later)."
- No findings against g1's claim-to-citation accuracy or jargon; IaC, HCL, declarative/imperative, provider, and service-agnostic are all defined before use.

## Lesson additions requested

- **tf-g1:** none required to close round 1, but see the thinness verdict below — recommend (not a hard finding) adding one concrete anchor per objective (e.g., naming one real single-cloud-only tool alongside CloudFormation in 1c, or one concrete "same steps, different manual procedure" example in 1b) to give question writers more distractor material.
- **tf-g2:** none.

## g1 thinness verdict

g1 has only 3 objectives, 11 claim rows, and no syntax/command-level detail (unlike g2's operators, blocks, and file names), yet must carry 9 questions (3 per objective, including one MR needing 5 defensible choices per objective). Each objective does have a real, usable discriminator, so round 1 is not blocked — but the margin for 9 non-duplicate, well-taught questions without repeating the same discriminator sentence three times is thin. This is worth fixing now: I'd ask Lead Dev to weigh whether 1b and 1c's MR items have enough distinct, lesson-taught wrong-answer material, or whether the additions above should be made before questions are drafted.

Lesson tf-g1: approve for question writing
Lesson tf-g2: approve for question writing
Overall: approve
