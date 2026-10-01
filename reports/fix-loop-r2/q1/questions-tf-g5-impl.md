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

## Pre-check fix pass

Applied LD-Qg5-001 to 004. Key positions are unchanged (5a-mc2 d; 5a-mr b,e; 5c-mc2 a; 5d-mr a,c). 5c-mr is kept as the owner of install behaviour, 5a-mc and 5d-mc keep their `./` distractor as directed.

Old and new text:

- **LD-Qg5-003 (5a-mc2 choice)**
  - Old: 'Add a `version = "2.3.0"` argument to the module block'
  - New: 'Append `//v2.3.0` to the repository address'

- **LD-Qg5-003 (5a-mc2 rationale)**
  - Old: The `version` argument applies only to registry modules, so it does not select a revision of a GitHub repository.
  - New: A double slash marks a folder inside the package, not a revision, so a slash-delimited tag name would be read as a folder path instead of selecting the tag.

- **LD-Qg5-002 (5a-mr choice)**
  - Old: 'The address has to begin with `./` because the file is fetched to local disk first'
  - New: 'The address can use the three-part `<NAMESPACE>/<NAME>/<PROVIDER>` shape, with the bucket name as the namespace'

- **LD-Qg5-001 (5a-mr choice)**
  - Old: '`terraform plan` fetches the newer file by itself, because sources are evaluated at plan time'
  - New: 'The new file is picked up only after the `.terraform` directory has been deleted and recreated'

- **LD-Qg5-001 + LD-Qg5-002 (5a-mr rationale)**
  - Old: A leading `./` marks a local path to files already on disk, not a packaged file in a bucket. Plan does not fetch module code; sourcing happens at install time, not at plan time.
  - New: The three-part `NAMESPACE/NAME/PROVIDER` shape is a registry address, while a bucket object is addressed with the `s3::` prefix. Nothing requires deleting the `.terraform` directory: re-running init after the edit is what installs the new code.

- **LD-Qg5-001 (5c-mc2 choice)**
  - Old: 'Nowhere on disk, because Terraform reads each source remotely again at plan time'
  - New: 'In a `.terraform` subdirectory of the working directory, committed so teammates skip the download'

- **LD-Qg5-001 (5c-mc2 rationale)**
  - Old: Modules are cloned at initialization and read from the local copy afterwards; sourcing does not happen at plan time.
  - New: The `.terraform` directory itself should not be committed, even though that is where the copies land.

- **LD-Qg5-004 (5d-mr stem)**
  - Old: wants every CI run to install the identical release of a registry module.
  - New: wants every CI run, each starting from a fresh clone, to install the identical release of a registry module.

Two-question check for each new distractor (Real? and Taught?):

- **5a-mc2 `Append //v2.3.0 to the repository address`:** Real? yes, people reuse the double slash they have seen in sources and expect it to take a revision. Taught? yes, the lesson says a double slash marks a folder inside the package and that `ref` is what selects a revision. Not a working answer: it names a folder that does not exist.
- **5a-mr `three-part <NAMESPACE>/<NAME>/<PROVIDER> shape with the bucket name as namespace`:** Real? yes, a plausible way to shorten an S3 address. Taught? yes, that shape is the registry shape, and the lesson teaches `s3::` for bucket objects. Not a working answer: it would be read as a registry address. Answers the packaging/address need.
- **5a-mr `picked up only after the .terraform directory has been deleted and recreated`:** Real? yes, a common folk remedy. Taught? yes, the lesson says changing `source` needs a fresh `terraform init` so that Terraform can update the local code; nothing requires deleting the directory. Not a working answer as worded ("only after"): re-running init alone installs the code. Answers the edit need.
- **5c-mc2 `.terraform subdirectory, committed so teammates skip the download`:** Real? yes, teams do consider committing it. Taught? yes, "Don't commit this directory to your version control repository". Not a working answer: the stem asks whether the copies belong in the repository. It shares its first half with the key, so the question's difference is the commit decision only; the stem asks both parts.
- **5d-mr stem:** now "each starting from a fresh clone", so distractor d (a range keeps the first release on every later run) is false because a fresh install selects the newest release the range allows, which the lesson teaches.

Rationales were rewritten by content (the replaced sentences are above); none refers to a choice by letter.

Counts after the pass:

- The audit no longer shows `version =` or `plan time` over cap: `version =` is 1 (5d-mr), and "plan time" appears in no choice. Plan appears only as a distractor in 5c-mr.
- A bare `./` distractor (counted by hand, the script cannot match it): 5a-mc and 5d-mc, 2 of 12. This is above the 1-question cap for 12; the Lead Dev's instruction was to keep both (5a-mc owns source shapes and 5d-mc owns "local paths do not support `version`"), so the over-cap is accepted and flagged here.
- Key length ranks unchanged for the edited MC: 5a-mc2 key is rank 3 (the replaced choice is short), 5c-mc2 key is rank 2. Longest-is-key 1/8 (12%), shortest-is-key 2/8 (25%).

Final chain, whole files: `content_lint.py` PASS; `q1_batch_check.py tf-g5` PASS (details above); `distractor_type_audit.py tf-g5` PASS (every type at 1 of 12); `stem_echo_check.py tf-g5` PASS (0 giveaways, 0 bulk echoes); `claim_prose_check.py tf-g5` PASS; `test_q1_letter.py` PASS (12 bad, 10 good, 0 failures).

## Round 2 fix pass

Applied AWS-Qg5-001 to 008 and TEACHER-Qg5-001 to 003 as decided by the Lead Dev; TEACHER-Qg5-004 needs no change. Choice ids and key positions are unchanged (5a-mc b, 5a-mc2 d, 5a-mr b/e, 5b-mc a, 5b-mc2 c, 5b-mr a/d, 5c-mc d, 5c-mc2 a, 5c-mr c/e, 5d-mc c, 5d-mc2 b, 5d-mr a/c). Rationales were rewritten by content with no letters. The lesson addition requested by AWS-Qg5-006 is recorded in `lesson-tf-g5-impl.md`.

Old and new text:

- **AWS-Qg5-001 (5a-mc stem).** Old: "...Only the module in the `modules/vpc` folder is wanted." New: "...The module is not published to any registry, and only the one in the `modules/vpc` folder is wanted." The rationale's claim that the module is not in a registry is now stated by the stem.
- **AWS-Qg5-002 (5a-mc2 rationale).** Old: "...so a slash-delimited tag name would be read as a folder path instead of selecting the tag." New: "...so `//v2.3.0` would be read as a folder named v2.3.0 inside the repository, which does not exist, instead of selecting the tag."
- **AWS-Qg5-003 (5a-mc2 choice c).** Old: "Rewrite the address as `git::https://github.com/acme/queue-module.git` with nothing else changed". New: "Rewrite the address in the explicit `git::https://github.com/acme/queue-module.git` form".
- **AWS-Qg5-004 + TEACHER-Qg5-003 (5c-mc choice c).** Old: "A map keyed by output name, whose values are lists with one entry per instance". New: "A set of objects, one per module instance, with no keys to look instances up by" (AWS's replacement; the Teacher's alternative, "a set of the two site keys...", was not used because it describes outputs readable only through a key, which no taught sentence addresses, while the AWS wording contradicts the taught "map of objects" directly). Rationale rewritten: the last sentence now says a set of objects with no keys is not what Terraform returns because the lesson describes a map of objects, so instances are looked up by key.
- **LD-Qg5-005 + TEACHER-Qg5-001 + AWS pair-tell finding (5c-mc2).** Old b: "In a `modules` folder beside the root `.tf` files, committed so everyone has identical code". New b: "In a `modules` folder beside the root `.tf` files, kept out of version control and recreated by `init`". Old d: "In a `.terraform` subdirectory of the working directory, committed so teammates skip the download". New d: "In the user's home directory, shared by every project, so there is nothing to commit". a and c unchanged. Old rationale ended with ".terraform itself should not be committed, even though that is where the copies land." New rationale explains by location: the copies land in `.terraform` of the current working directory; a `modules` folder beside the root files is not where they land whether or not it is committed; the home directory is not used because the copies sit in each configuration's working directory; the lock file records provider selections only. Only the lock-file distractor still mentions committing, so the commit decision no longer picks the key; the location does.
- **AWS-Qg5-005 + TEACHER-Qg5-002 (5c-mr stem).** Old: "...that its `version` constraint allows, but routine initialization keeps leaving the old copy in place. Which two actions would move the installed modules forward?" New: "...that its `version` constraint allows. Which two actions would move the installed modules forward?" (AWS's rewrite as the Lead Dev decided.) Rationale: the last sentence now reads "Installing and provisioning are separate steps: init installs the module code, and plan and apply work with the modules already installed, so neither moves an installed module forward." This is the sentence now taught in lesson 5c (see lesson note), so it replaces the Teacher's alternative wording.
- **AWS-Qg5-007 (5d-mc2 rationale).** Old: "...and 1.0.3 is below the stated lower bound." New: "...and 1.0.3 is older than the 1.0.4 the constraint starts from, and in any case it is not the newest qualifying release."
- **AWS-Qg5-008 (5d-mr choice b).** Old: "Committing the lock file freezes the module release, because it lists every external dependency". New: "Running `terraform init -upgrade` in each CI job keeps the module on the release chosen the first time". Rationale rewritten: the upgrade flag moves modules to the newest release the constraint allows; a range moves because nothing remembers the first pick; `!=` only excludes one exact version.
- **TEACHER-Qg5-004:** no change.

Two-question check for each changed or new distractor (Real? / which lesson sentence refutes it):

- 5a-mc2 c (explicit `git::` form): Real? yes, an equivalent spelling of the same repository. Refuted by: "Terraform defaults to the default branch referenced by HEAD in the repository." (5a). It is not a working answer: no `ref` is given.
- 5c-mc c (set of objects with no keys): Real? yes, a reader who remembers `for_each` accepts a set and assumes the module result is a set. Refuted by: the 5c line "With `for_each`, ... the value will be a map of objects". Not a working answer: the lesson says a map.
- 5c-mc2 b (`modules` folder beside the root files, kept out of version control and recreated by `init`): Real? yes, a plausible expectation (and a common `.gitignore` habit). Refuted by: "The modules are downloaded into a .terraform subdirectory of the current working directory." Not a working answer: it names the wrong location.
- 5c-mc2 d (user's home directory, shared by every project): Real? yes, people expect a shared cache the way provider plugins can be cached. Refuted by the same `.terraform` sentence (the working directory, not a shared location). Not a working answer.
- 5d-mr b (`init -upgrade` in each CI job keeps the module on the first-chosen release): Real? yes, `-upgrade` is routinely mistaken for "refresh the lock". Refuted by: 5c "init -upgrade ... updates all modules to the latest available source code (within any `version` constraint ...)". Not a working answer: it moves modules forward, the opposite of holding a release. It answers the stem's single need (identical release on every CI run).

Distractor audit effect: `-upgrade` appears once (5d-mr, a distractor) and as a key once (5c-mr); `lock file` is no longer in a choice.

Key-length ranks after the pass: 5a-mc 2, 5a-mc2 3, 5b-mc 2, 5b-mc2 4, 5c-mc 4, 5c-mc2 2 or 3, 5d-mc 3, 5d-mc2 1 (bare version numbers, tie); `q1_batch_check` shows longest-is-key 12% and shortest-is-key 25%.

Each changed choice was re-read alone: every one is valid as written, none uses a banned giveaway word ("so that", "since", "despite", "which does not", "must", "even though", "requiring", "without changing"), and none refers to another choice.

Whole-file chain after the fix: `content_lint.py` PASS; `q1_batch_check.py tf-g5` PASS (longest-is-key 12%, shortest-is-key 25%, MC keys a2/b2/c2/d2, MR slots a2/b1/c2/d1/e2, MR sets distinct, no duplicate openings); `distractor_type_audit.py tf-g5` PASS (every type at 1 of 12); `stem_echo_check.py tf-g5` PASS (0 giveaways, 0 bulk echoes); `claim_prose_check.py tf-g5` PASS; `test_q1_letter.py` PASS (12 bad, 10 good, 0 failures).
