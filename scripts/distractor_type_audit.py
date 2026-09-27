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
]


def main(task: str) -> int:
    files = sorted((ROOT / "content/questions").glob(f"q-*-{task}-*.json"))
    if not files:
        print(f"no question files for task {task}")
        return 1

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
            for t in TERMS:
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

    cap = int(len(files) * CAP)
    over = [t for t, c in cnt.items() if c > cap]
    print(f"task {task}: {len(files)} questions; 15% cap = {cap} questions\n")
    for t, c in cnt.most_common():
        flag = "   <-- OVER CAP" if c > cap else ""
        print(f"{t:28}{c:3d}{c / len(files) * 100:5.0f}%  {','.join(where[t])}{flag}")
    print(f"\nRESULT: {'FAIL' if over else 'PASS'}" + (f" ({', '.join(over)})" if over else ""))
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
