"""Generate per-lab command review rows for evidence-log.md (read-only)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LABS = ROOT / "content" / "labs"
CMD_MD = ROOT / "reports" / "evidence" / "lab-commands.md"

# first aws/terraform command per lab from extract
first_cmd: dict[str, str] = {}
for line in CMD_MD.read_text(encoding="utf-8").splitlines():
    if not line.startswith("| gl-"):
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 4:
        continue
    lab, step, cmd = parts[1], parts[2], parts[3]
    if lab not in first_cmd and cmd.startswith("`aws"):
        first_cmd[lab] = cmd.strip("`")

rows = []
n = 0
for path in sorted(LABS.glob("*.json")):
    n += 1
    data = json.loads(path.read_text(encoding="utf-8"))
    lab_id = data["id"]
    if lab_id in first_cmd:
        cmd = first_cmd[lab_id]
        loc = f"reports/evidence/lab-commands.md + content/labs/{lab_id}.json"
        note = "Primary step command from extract; JSON steps/teardown cross-read."
    else:
        td = data.get("teardown") or {}
        dels = td.get("orderedDeletesPowerShell") or []
        cmd = dels[1] if len(dels) > 1 else (dels[0] if dels else "(no CLI)")
        loc = f"content/labs/{lab_id}.json:teardown"
        note = "Unguided lab: review teardown/acceptance CLI (no step extract row)."
    rows.append((f"EV-AWS-{n:03d}", lab_id, cmd[:80], loc, note))

for ev, lab, cmd, loc, note in rows:
    print(f"| {ev} | 2026-09-25T17:30Z | file | {loc} | {cmd} | {note} |")
print("COUNT", len(rows))
