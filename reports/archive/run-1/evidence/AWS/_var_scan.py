import json, re
from pathlib import Path
LABS = Path(__file__).resolve().parents[3] / "content" / "labs"
VAR_REF = re.compile(r"\$([A-Za-z][A-Za-z0-9_]*)")
issues = []
for path in sorted(LABS.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    lab_id = data.get("id", path.stem)
    steps = data.get("steps") or []
    step_text = json.dumps(steps)
    step_vars = set(VAR_REF.findall(step_text))
    td = data.get("teardown") or {}
    deletes = td.get("orderedDeletesPowerShell") or []
    delete_text = "\n".join(deletes)
    teardown_vars = set(VAR_REF.findall(delete_text))
    allowed = {"AccountId", "CreatedAt", "ExpiresAt", "Bucket", "Suffix"}
    missing = []
    for v in teardown_vars:
        if v.startswith("env:"):
            continue
        if v not in step_vars and v not in allowed:
            missing.append(v)
    if missing:
        issues.append((lab_id, sorted(set(missing))))
print("TEARDOWN_VAR_GAPS")
for lab_id, vars in issues:
    print(lab_id, vars)
print("COUNT", len(issues))
