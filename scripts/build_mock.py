import json
from pathlib import Path
from collections import defaultdict

questions = [json.loads(p.read_text(encoding="utf-8")) for p in Path("content/questions").glob("q-*.json")]
by = defaultdict(list)
for q in questions:
    if q.get("type") in ("mc", "mr"):
        by[q.get("module")].append(q["id"])

need = {"A1": 15, "A2": 13, "A3": 12, "A4": 10}
picked = []
for mod, n in need.items():
    pool = sorted(by.get(mod, []))
    if len(pool) < n:
        raise SystemExit(f"not enough {mod}: {len(pool)}")
    picked.extend(pool[:n])

mock = {
    "id": "mock-saa-50",
    "title": "SAA-C03 style mock exam (50 items)",
    "note": "Curriculum design choice mirroring domain weights 15/13/12/10. Not a real exam form. Raw score only — never convert to a scaled score or compare to 720.",
    "allocation": need,
    "questionIds": picked,
}
Path("content/questions/mock-saa-50.json").write_text(json.dumps(mock, indent=2), encoding="utf-8")
print("mock", len(picked))
