"""Count how many questions in a task reuse the same service as a DISTRACTOR.

RULES caps any one distractor type at 15% of a task. `q1_batch_check.py` does not
measure this, and it has been the most common reviewer finding (DataBrew 10/24,
EFS 7/35, and a recycled Outposts option in task 4.2).

Two things this gets right that are easy to get wrong:
  - correct answers are excluded via `correctAnswerIds`; counting them as
    distractors inflates every figure;
  - matching uses a curated service list rather than generic capitalised-phrase
    extraction, which otherwise counts ordinary words like "Replace" as services.

A service absent from TERMS is simply not counted, so this is a screen, not a
proof. Add new services as tasks introduce them.

Read-only. Usage: distractor_type_audit.py <task>   e.g. 4-3, tf-g1
"""

import collections
import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = 0.15
SUBJECT_CAP = 0.40  # plan p2_audit_terms_scope_20261002
MIN_N = 10  # below this, an over-cap task reports WARN (small N), not FAIL

# Plan P2 (.cursor/plans/p2_audit_terms_scope_20261002.plan.md): a term that is
# the task's own subject vocabulary is not a reused distractor type, so it is
# held to SUBJECT_CAP instead of CAP. It is still counted and printed, so heavy
# over-use shows. Each entry was ruled by the Teacher against the task's own
# objective bullets (reports/open-items/phase1/TEACHER-subject-ruling.md).
SUBJECT = {
    "1-2": ["NAT Gateway"],                                  # 1.2-S01
    "2-1": ["Lambda"],                                       # 2.1-K12, S05
    "2-2": ["Multi-AZ"],                                     # 2.2-S02, S04, K06
    "3-1": ["Storage Gateway", "EFS"],                       # 3.1-K01, K02
    "3-2": ["Lambda", "Auto Scaling"],                       # 3.2-K05, K04
    "3-3": ["RDS", "read replica", "ElastiCache", "DynamoDB", "Aurora"],  # 3.3-S03, K07, K02, S04
    "3-4": ["Application Load Balancer", "Direct Connect", "CloudFront",
            "Gateway Load Balancer"],                        # 3.4-K03, K04, K01, S04
    "3-5": ["Glue", "EMR", "Athena"],                        # 3.5-K04, S05, K01
    "4-1": ["EBS", "FSx", "EFS", "S3 Glacier"],              # 4.1-K04, K10
}

TERMS = [
    # compute / placement (4.2)
    "Outpost", "Local Zone", "Wavelength", "Savings Plan", "Reserved Instance",
    "Spot", "On-Demand", "Auto Scaling", "Lambda", "Fargate", "Graviton",
    "Compute Optimizer", "hibernat", "Global Accelerator", "Classic Load Balancer",
    "Application Load Balancer", "Network Load Balancer", "Gateway Load Balancer",
    "Dedicated Host", "Elastic Beanstalk", "App Runner", "Lightsail", "Batch",
    # databases (4.3)
    "Aurora Serverless", "Aurora I/O-Optimized", "Aurora", "RDS Proxy", "RDS",
    "DynamoDB Accelerator", "DAX", "DynamoDB", "ElastiCache", "Redshift",
    "Neptune", "DocumentDB", "Keyspaces", "MemoryDB", "Timestream", "QLDB",
    "Athena", "Glue", "EMR", "Database Migration Service", "DMS",
    "Multi-AZ DB cluster", "Multi-AZ", "read replica", "Standard-Infrequent Access",
    "Standard-IA", "point-in-time recovery", "snapshot",
    # networking / storage that recur as distractors
    "CloudFront", "Direct Connect", "NAT Gateway", "VPC endpoint", "Transit Gateway",
    "S3 Glacier", "EFS", "EBS", "FSx", "DataSync", "Storage Gateway",
    # Terraform (tf-g1, tf-g2)
    "CloudFormation", "HCP Terraform", "required_providers", "provider block",
    "dependency lock file", "resource graph", "terraform.tfstate", "random_pet",
    "random provider",
    # Terraform core workflow flags (tf-g3). Flags are distinctive enough to
    # be a distractor "type"; the bare command names are not, and are
    # deliberately absent. "terraform apply" appears incidentally in choices
    # that are not about apply at all ("...allowed to run terraform apply"),
    # and counting those tripped the cap on tf-g2 over two passing mentions.
    # Same call as leaving the bare word "provider" out for a providers
    # lesson, and RDS for a databases lesson: subject vocabulary is not a
    # reused distractor type.
    "-upgrade", "-auto-approve", "-out", "-target", "-refresh-only", "-destroy",
    "-check", "-recursive", "-backend=false",
    # Terraform configuration language named constructs (tf-g4). Named
    # meta-arguments, lifecycle arguments, functions, and mechanisms are
    # distinctive enough to be a distractor "type", the same call as the
    # tf-g3 flags above. Bare words already covered by ordinary subject
    # vocabulary (resource, data, variable, local, output) are deliberately
    # left out, the same way bare command names were left out for tf-g3.
    "for_each", "depends_on", "create_before_destroy", "prevent_destroy",
    "ignore_changes", "precondition", "postcondition", "validation",
    "check block", "terraform_data", "nonsensitive", "ephemeral",
    "write-only", "tolist", "tomap", "toset",
    # tf-g5 (modules). A bare `./` local path cannot be matched by the word
    # guard below, so that distractor type is counted by hand in the pre-check.
    "TF_VAR", "-var", "tfvars", "?ref", "version =", "lock file",
    "plan time", "init -upgrade", "get -update",
    # tf-g6 (state)
    "-lock=false", "-lock-timeout", "force-unlock", "use_lockfile",
    "dynamodb_table", "-migrate-state", "-reconfigure", "-force-copy",
    "-backend-config", "cloud block", "-refresh-only", "terraform refresh",
    "terraform import", "import block", "moved block", "removed block",
    "state rm", "state mv", "state list", "state show", "-generate-config-out",
    "-state-out", "-backup", "workspace_dir",
    # tf-g7 (maintain infrastructure). Bare `TF_LOG` and the level names
    # (TRACE, DEBUG ...) are 7c's own subject vocabulary and are left out,
    # the same way bare `version` was left out for tf-g5's 5d.
    # `identity` was removed in the final sitting: it appeared in one tf-g7
    # question only and matched IAM "identity", task 1-1's own subject.
    "TF_LOG_PATH", "TF_LOG_CORE", "TF_LOG_PROVIDER",
    "-raw", "-json", "state pull", "state push", "terraform show",
    "terraform output", "-force",
    # tf-g8 (HCP Terraform), per the Teacher's round 2 ruling. Sentinel, OPA
    # and bare "HCP Terraform" stay out as 8b's and the group's own subject
    # vocabulary; terms that appear in at most one question add nothing.
    "run trigger", "variable set",
]


def main(task: str) -> int:
    files = sorted((ROOT / "content/questions").glob(f"q-*-{task}-*.json"))
    lesson_path = ROOT / f"content/lessons/lesson-{task}.json"
    if lesson_path.exists():
        # Objective-group tasks (e.g. tf-g1) don't have a filename token that
        # matches the task id directly, so select by the lesson's own
        # objectiveIds instead -- the same approach q1_batch_check.py uses.
        objs = set(json.loads(lesson_path.read_text(encoding="utf-8"))["objectiveIds"])
        files = sorted(
            f for f in (ROOT / "content/questions").glob("q-*.json")
            if objs & set(json.loads(f.read_text(encoding="utf-8")).get("objectiveIds", []))
        )
    if not files:
        print(f"no question files for task {task}")
        return 1

    # Exam split: SAA tasks use only the AWS service terms (everything before
    # the first Terraform-only term); Terraform tasks keep the full list, so
    # their results are unchanged. This stops cross-exam hits such as the
    # tf-g7 term `identity` matching IAM "identity" in task 1-1.
    terms = TERMS if task.startswith("tf-") else TERMS[: TERMS.index("HCP Terraform")]
    subject = set(SUBJECT.get(task, []))

    cnt: collections.Counter = collections.Counter()
    where = collections.defaultdict(list)
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        keys = set(d["correctAnswerIds"])
        seen = set()
        for ch in d["choices"]:
            if ch["id"] in keys:
                continue
            low = ch["text"].lower()
            for t in terms:
                # Word-boundary match: a bare "RDS" must not match inside
                # "shards" or "records". The trailing guard allows a plural
                # suffix, because it previously hid "read replicas" (6 of 22
                # questions in task 4.3) behind the singular "read replica".
                if re.search(
                    rf"(?<![a-z0-9]){re.escape(t.lower())}(?:es|s)?(?![a-z0-9])", low
                ):
                    seen.add(t)
        short = d["id"].replace(f"q-saa-{task}-", "").replace(f"q-tf-004-{task}-", "")
        for t in seen:
            cnt[t] += 1
            where[t].append(short)

    n = len(files)
    cap = int(n * CAP)
    scap = int(n * SUBJECT_CAP)
    over = [t for t, c in cnt.items() if c > (scap if t in subject else cap)]
    print(f"task {task}: {n} questions; 15% cap = {cap} questions"
          + (f"; subject-term cap (40%) = {scap}" if subject else "") + "\n")
    # Sort ties by name so the output is stable across runs and diffs cleanly.
    for t, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        lim = scap if t in subject else cap
        flag = "   <-- OVER CAP" if c > lim else ""
        tag = "  [subject]" if t in subject else ""
        print(f"{t:28}{c:3d}{c / n * 100:5.0f}%  {','.join(where[t])}{tag}{flag}")
    if not over:
        print("\nRESULT: PASS")
        return 0
    if n < MIN_N:
        print(f"\nRESULT: WARN (small N: {n} < {MIN_N}) ({', '.join(over)})")
        return 0
    print(f"\nRESULT: FAIL ({', '.join(over)})")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
