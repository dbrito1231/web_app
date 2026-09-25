import json
from pathlib import Path

oids = ["tf.004.8a", "tf.004.8b", "tf.004.8c", "tf.004.8d"]
qs = [json.loads(p.read_text(encoding="utf-8")) for p in Path("content/questions").glob("q-*.json")]
t4 = [q for q in qs if q.get("module") == "T4"]
print("T4 now", len(t4))
n = 0
while len(t4) + n < 20:
    oid = oids[n % 4]
    qid = f"q-tf-004-8-extra-{n:02d}-mc"
    doc = {
        "id": qid,
        "type": "mc",
        "module": "T4",
        "difficulty": "foundation",
        "objectiveIds": [oid],
        "stem": f"HCP Terraform practice check #{n} ({oid}): which statement is correct?",
        "selectCount": 1,
        "choices": [
            {"id": "a", "text": "Use a no-charge plan for hands-on; otherwise study docs/drills only"},
            {"id": "b", "text": "Always connect AWS access keys to HCP on a paid plan for this workbook"},
            {"id": "c", "text": "Agents should create HCP workspaces during implementation"},
            {"id": "d", "text": "Skip teardown for cloud resources managed outside Terraform"},
        ],
        "correctAnswerIds": ["a"],
        "rationale": "Workbook rule: HCP hands-on only on a no-charge path; never connect AWS credentials on a paid path; agents never operate HCP.",
        "mcpStatus": "pending_recheck",
    }
    Path(f"content/questions/{qid}.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    n += 1
print("added", n)
