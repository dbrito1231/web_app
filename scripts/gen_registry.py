import re
import json
import pathlib
from collections import Counter

src = pathlib.Path(r"c:\Users\dbadmin\Downloads\cursor_saa_c03_exam_objectives_coverage.md").read_text(
    encoding="utf-8"
)
rows = []
current_pages = None
domain_map = {
    "1": ("d1", "Design Secure Architectures", 30),
    "2": ("d2", "Design Resilient Architectures", 26),
    "3": ("d3", "Design High-Performing Architectures", 24),
    "4": ("d4", "Design Cost-Optimized Architectures", 20),
}
for line in src.splitlines():
    m = re.match(r"### Task (\d)\.(\d): (.+)", line)
    if m:
        continue
    m = re.match(r"Source: printed p\. ([^.]+)\.", line)
    if m:
        current_pages = m.group(1).strip()
        continue
    m = re.match(r"- \[ \] \*\*(SAA-(\d)\.(\d)-([KS]\d+))\*\*: (.+)", line)
    if m:
        oid, d, t, suffix, text = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        did, dtitle, weight = domain_map[d]
        rows.append(
            {
                "objective_id": oid,
                "task_id": f"{d}.{t}",
                "domain_id": did,
                "domain_title": dtitle,
                "domain_weight": weight,
                "bullet_kind": "knowledge" if suffix.startswith("K") else "skill",
                "source_file": "solutions-architect-associate-03.pdf",
                "printed_pages": current_pages or "",
                "source_text": text,
                "lesson_refs": [],
                "drill_refs": [],
                "guided_refs": [],
                "unguided_refs": [],
                "exercise_refs": [],
                "practice_mode": None,
                "constraint_reason": None,
                "validation_refs": [],
                "status": "missing",
                "gap": "No lesson, assessment, or practice evidence yet",
                "owner": "phase-3/4/5",
                "next_action": "Author lesson and mapped assessment",
            }
        )

assert len(rows) == 189, len(rows)
c = Counter(r["domain_id"] for r in rows)
assert c["d1"] == 32 and c["d2"] == 43 and c["d3"] == 50 and c["d4"] == 64, c

root = pathlib.Path(r"C:\Users\dbadmin\Desktop\GitServ\ccna\web_app")
(root / "content" / "coverage" / "saa_registry.json").write_text(
    json.dumps(
        {
            "schemaVersion": 1,
            "source": "supplied SAA-C03 PDF",
            "accessed": "2026-09-23",
            "total": 189,
            "rows": rows,
        },
        indent=2,
    ),
    encoding="utf-8",
)
obj = [
    {
        "id": r["objective_id"],
        "task_id": r["task_id"],
        "domain_id": r["domain_id"],
        "kind": r["bullet_kind"],
        "text": r["source_text"],
        "printed_pages": r["printed_pages"],
    }
    for r in rows
]
(root / "content" / "objectives" / "saa_c03.json").write_text(json.dumps(obj, indent=2), encoding="utf-8")
print("ok", len(rows), dict(c))
