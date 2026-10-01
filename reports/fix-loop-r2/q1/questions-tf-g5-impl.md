# Questions tf-g5 (Terraform modules) -- implementation report

## What was written

12 questions, 3 per objective (`-mc`, `-mc2`, `-mr`) in `content/questions/q-tf-004-5{a,b,c,d}-{mc,mc2,mr}.json`. `id`, `type`, `module`, `difficulty`, `objectiveIds` and `selectCount` are unchanged. `stem`, `choices`, `correctAnswerIds`, `rationale` and `citationIds` were rewritten, with `mcpStatus: "verified"` and `reviewedOn: "2026-09-26"`. Choices were ordered and key positions set before the rationales were written; no rationale refers to a choice by letter (`test_q1_letter.py` passes). Every fact comes from the lesson as fixed in round 1. Fact ownership follows TEACHER-Lg5-006: 5b owns `module.<label>.<output>` and "child must declare an output"; 5c owns the output shape and `init -upgrade` / `get -update`; 5d owns the lock file, the exact pin and registry-only `version`.

## Per-question entries

"Real?" asks whether a practitioner would genuinely consider the option or whether it exists. "Taught?" asks whether the lesson teaches the reason it is wrong. They are separate questions and both are answered for every distractor.

### 5a

- **q-tf-004-5a-mc** (fact: `//` marks the module folder inside a Git package; key b `git::...network.git//modules/vpc`)
  - a `git::...network.git/modules/vpc?ref=main` (single slash): Real? yes, people write a plain path in a URL. Taught? yes, the lesson says to mark the folder with a double slash and that `ref` selects a revision. It is not a working answer: no folder marker.
  - c `./network.git//modules/vpc`: Real? yes, a local path with `//` is a common half-remembered form. Taught? yes, `./` or `../` is for files already on disk; the stem says nothing is checked out.
  - d `acme/network/aws//modules/vpc`: Real? yes, a registry address with a subdirectory. Taught? yes, registry shape is `NAMESPACE/NAME/PROVIDER` and the stem's module is on a Git server.
- **q-tf-004-5a-mc2** (fact: a Git source without `ref` follows the default branch; pin with a tag using `?ref=`; key d `?ref=v2.3.0`)
  - a `version = "2.3.0"` argument: Real? yes, the most common mistake. Taught? yes, `version` is registry-only (5d section of the same lesson, and the Warnings bullet). Not a working answer for a GitHub source.
  - b `?ref=main`: Real? yes. Taught? yes, a branch keeps moving as commits arrive (lesson 5d Git bullet; `ref` accepts a branch name per 5a).
  - c explicit `git::https://github.com/acme/queue-module.git`: Real? yes, an equivalent form of the same repository. Taught? yes, without `ref` the default branch at HEAD is used.
- **q-tf-004-5a-mr** (facts: an S3 object must be an archive; changing `source` needs a fresh `terraform init`; keys b, e)
  - a loose-folder source works like a packaged file: Real? yes, teams try to point at a bucket prefix of `.tf` files. Taught? yes, the S3 object must be an archive. Answers the packaging need.
  - c address has to begin with `./`: Real? yes, confusion about local paths. Taught? yes, `./` is a local path for files already on disk. Answers the packaging need.
  - d `plan` fetches the newer file by itself: Real? yes. Taught? yes, "sourcing happens at install time, not at plan time". Answers the edit need.

### 5b

- **q-tf-004-5b-mc** (fact: a child's input arrives as an argument in the `module` block; key a)
  - b `-var 'replicas=3'`: Real? yes, a normal way to set variables. Taught? yes, `-var` and `TF_VAR_` set root variables, not a child's.
  - c `TF_VAR_replicas`: Real? yes. Taught? same lesson sentence.
  - d `terraform.tfvars` in the child's folder: Real? yes. Taught? yes, `.tfvars` files are listed among the root-module methods. The lesson does not say what Terraform does with a file in a child's folder; the reason it is wrong is that the parent hands values down as arguments. Flagged for the Teacher as the thinnest distractor.
- **q-tf-004-5b-mc2** (fact: a local is invisible to the child, but its value can be passed as an argument; key c)
  - a `local.name_prefix` used directly in the child: Real? yes. Taught? yes, "not in other modules".
  - b an identically named `locals` block in the child: Real? yes, people copy it. Taught? yes, each module is its own scope; a local is defined and visible only in its own module, so a copy is a separate definition.
  - d child `output "prefix"` read from the root: Real? yes, direction confusion. Taught? yes, outputs carry values out of a child, not in.
- **q-tf-004-5b-mr** (facts: the child must declare an `output`; the root reads `module.<label>.<output name>`; keys a, d)
  - b `module.network.aws_subnet.main.id`: Real? yes, the most common attempt. Taught? partly: the lesson says a module is a self-contained group, outputs are the channel, and there is "no documented way" to read a child resource directly (and the Warnings say not to rely on it). It is an error in Terraform but the lesson deliberately does not assert the error text.
  - c a `locals` block read as `module.network.subnet_id`: Real? yes. Taught? yes, locals do not cross the boundary.
  - e a `variable` default read as `module.network.subnet_id`: Real? yes, inputs and outputs confused. Taught? yes, a variable carries a value into a child.

### 5c

- **q-tf-004-5c-mc** (fact: `for_each` on a module block gives a map of objects; key d)
  - a single object with one attribute per output: Real? yes, that is the no-meta-argument shape. Taught? yes.
  - b list of objects: Real? yes, the `count` shape. Taught? yes.
  - c map keyed by output name with list values: Real? weak, it is a plausible mix-up of the two shapes but not a shape anyone has seen. Taught? only by the lesson's "a map of objects". Flagged as the weakest distractor on the task; if the Teacher calls it a caricature, replace it with "a set of the instances' labels".
- **q-tf-004-5c-mc2** (fact: modules land in `.terraform` and the directory is not committed; key a)
  - b a committed `modules` folder: Real? yes, vendoring is a real practice. Taught? yes, the lesson says `.terraform` is where they land and not to commit it.
  - c `.terraform.lock.hcl`: Real? yes. Taught? yes, the lock file tracks only providers (5d).
  - d nowhere on disk, read at plan time: Real? yes, a plausible belief. Taught? yes, sourcing is at install time and modules are cloned into `.terraform`.
- **q-tf-004-5c-mr** (fact: `init -upgrade` and `get -update` refresh installed modules; keys c, e)
  - a plain `terraform init`: Real? yes. Taught? yes, "will not change any already-installed modules".
  - b `terraform plan`: Real? yes. Taught? yes, sourcing is at install time, not at plan time.
  - d `terraform apply` on an unchanged configuration: Real? yes. Taught? same sentence as b (module code is installed by `init`/`get`, not by apply). Slightly weaker than b: the lesson never mentions apply fetching nothing; it says only that plan and apply "work as usual" after install.

### 5d

- **q-tf-004-5d-mc** (fact: only a registry source takes `version`; key c `acme-corp/billing/aws`)
  - a `./modules/billing`: Real? yes. Taught? yes, local paths do not support `version`.
  - b `git::https://git.example.com/billing.git`: Real? yes. Taught? yes, Git pins with `?ref=`.
  - d `s3::...billing.zip`: Real? yes. Taught? yes, `version` applies only to registry modules.
- **q-tf-004-5d-mc2** (fact: `~> 1.0.4` plus newest-qualifying selection; releases 1.0.3, 1.0.5, 1.0.10, 1.1.10; key 1.0.10)
  - 1.1.10: Real? yes, someone reading `~>` as "at least". Taught? yes, `~> 1.0.4` does not allow 1.1.0.
  - 1.0.5: Real? yes, correct range but not newest. Taught? yes, the newest qualifying release is installed.
  - 1.0.3: Real? yes, a reader unsure of the lower bound. Taught? the lesson says `~>` allows 1.0.5 and 1.0.10; the lower bound of 1.0.4 is implied by the constraint's own number rather than stated.
- **q-tf-004-5d-mr** (facts: the lock file tracks only providers; an exact `version` is the pin; keys a, c)
  - b committing the lock file freezes the module: Real? yes, the standard misconception. Taught? yes, the lock file tracks only providers. It is the direct opposite of key a; accepted because the misconception is the point of the objective.
  - d `~> 6.0` keeps the first release: Real? yes. Taught? yes, a range can move to a newer release because Terraform does not remember module selections.
  - e `!=` holds a single release: Real? yes, a mix-up of operators. Taught? yes, `!=` excludes one exact version; `=` allows only one.

## Self-check on the three failure classes named for this task

- **Wrong-letter rationales:** none; `test_q1_letter.py` passes and every rationale names options by content.
- **A distractor that is a working answer:** each distractor was checked. The nearest calls were 5c-mr "plan"/"apply" (neither installs or updates modules) and 5a-mc2 `?ref=main` (pins to a branch, which is not a fixed version and still pulls the unfinished change, as the stem states it was merged to the primary branch).
- **Rationale true only for older Terraform versions:** no version-specific claims are made. Version floors for the quoted features are not used.
- **Invalid syntax in a choice:** all code in choices is valid HCL or CLI syntax as written: `-var 'replicas=3'`, `module.network.<output_name>` (placeholder syntax from the docs), `?ref=v2.3.0`, `version = "~> 6.0"`.
- **Self-justifying keys / giveaways:** none; `stem_echo_check` has 0 giveaways and 0 bulk echoes.
- **Duplicate facts:** none within an objective. Across objectives `init -upgrade` appears as a distractor in none and as a key only in 5c-mr.
- **MR distractors answering neither need:** every MR distractor is labelled above with the need it answers.

## Distractor-type table (`distractor_type_audit.py tf-g5`)

| Type | Count | % of 12 | Questions |
|---|---|---|---|
| for_each | 1 | 8% | q-tf-004-5c-mc |

Cap is 15% (1 question for 12). During the pass `-upgrade` was at 2 (5a-mc2, 5d-mr) and over the cap; both distractors were replaced (a `version` argument and a `!=` condition). The audit has no TERMS for several constructs named in this task's distractors: `version` argument, `?ref=`, `.terraform.lock.hcl`, `get -update`, `-var`, `TF_VAR_`, `terraform.tfvars`, `locals`, `output`, `s3::`, `git::`. Reported rather than added to the script, as instructed. A manual count of the repeated ones: `?ref=` in 2 questions (5a-mc, 5a-mc2), the lock file in 2 (5c-mc2 distractor, 5d-mr), `version` argument in 2 (5a-mc2 distractor, 5d-mr), root-only variable methods in 1 (5b-mc, three distractors). None is above 2 of 12 apart from 5b-mc; Lead Dev decision whether to add TERMS for these.

## Key-position and length tables

| Question | Key | Key length rank (1 = longest of 4) |
|---|---|---|
| 5a-mc | b | 2 |
| 5a-mc2 | d | 3 |
| 5b-mc | a | 2 |
| 5b-mc2 | c | 4 |
| 5c-mc | d | 4 |
| 5c-mc2 | a | 2 |
| 5d-mc | c | 3 |
| 5d-mc2 | b | 1 (tie at 6 characters with another choice; all four choices are bare version numbers) |

- MC key positions: a 2, b 2, c 2, d 2.
- MR key sets: 5a-mr b,e; 5b-mr a,d; 5c-mr c,e; 5d-mr a,c. Slots: a 2, b 1, c 2, d 1, e 2.
- Longest-is-key 1/8 (12%), shortest-is-key 2/8 (25%), both under the 35% cap. Choices were not padded; the two changes made for length were a longer wrong Git path in 5a-mc (it adds `?ref=main`) and a shorter key in 5b-mc and 5c-mc2.

## Teach-before-test notes for reviewers

- 5b-mc distractor d (`terraform.tfvars` in the child's folder), 5c-mc distractor c (map keyed by output name), 5c-mr distractor d (apply) and 5d-mc2 distractor 1.0.3 are the four thinnest on teaching. No lesson addition is requested unless a reviewer calls one untaught; if so, the proposed sentence for d: "Variable definition files and `-var` apply to root module variables only (the doc says root module variables can be assigned by several methods and child modules receive inputs as arguments)."
- 5d-mc2 uses numeric ordering of 1.0.10 against 1.0.5; the lesson's quote "newest installed version" and its `1.2 and 1.10` example both rely on ordinary version ordering.

## Final chain, whole files

- `content_lint.py`: PASS (429 questions, 23 lessons).
- `q1_batch_check.py tf-g5`: PASS (lesson lines unchanged; drillIds match 12/12; exam tips 4/4; duplicate 6-word openings []; longest-is-key 12%; shortest-is-key 25%; MC keys a2 b2 c2 d2; MR slots a2 b1 c2 d1 e2; MR sets all distinct).
- `distractor_type_audit.py tf-g5`: PASS (highest type 1 of 12).
- `stem_echo_check.py tf-g5`: PASS (0 giveaways, 0 waivers, 0 bulk echoes).
- `claim_prose_check.py tf-g5`: PASS (16 numbers in lesson prose; every claim-table number appears in it).
- `test_q1_letter.py`: PASS (12 bad, 10 good, 0 failures).
