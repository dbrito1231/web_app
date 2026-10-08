"""Verify each row of content/coverage/saa_registry.json against the Q1 evidence.

Plan: .cursor/plans/p1_coverage_registry_verify_20261002.plan.md (Phase 3).

A row PASSES when all of these hold:
  - it has a lesson (all 14 SAA lessons are closed in progress.md);
  - drill_refs equals the questions whose objectiveIds name the row (the demo
    q-a0-* questions are excluded from both sides);
  - there is at least one drill, and every drill is mcpStatus "verified" with citations;
  - the task's distractor_type_audit result is PASS (WARN and FAIL both keep the
    row unverified and name CR-0024);
  - the task has paper-review reports (Technical reviewer, Teacher, Student) that exist
    on disk; the 1-1 pilot is evidenced by its progress.md line only.

"Verified" means reviewed on paper. It never means tested, exam-ready or run in AWS.

Read-only by default (prints a per-row table). --write applies the changes.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "content" / "coverage" / "saa_registry.json"
Q1 = ROOT / "reports" / "fix-loop-r2" / "q1"
PROGRESS = "reports/fix-loop-r2/q1/progress.md"
DEMO = re.compile(r"^q-a0-")
PILOT = "1.1"
LIVE_NOTE = "paper review only; not run in AWS (D5)"
# The 4.2 technical review of all 24 questions is section (c) of the round-2 lesson report.
QUESTION_REVIEW_EXTRA = {"4.2": {"AWS": ["reports/fix-loop-r2/q1/lesson-4-2-AWS-round2.md"]}}


def load_questions() -> dict:
    out = {}
    for p in (ROOT / "content" / "questions").glob("q-*.json"):
        q = json.loads(p.read_text(encoding="utf-8"))
        out[q["id"]] = q
    return out


def audit_result(task: str) -> str:
    key = task.replace(".", "-")
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "distractor_type_audit.py"), key],
        capture_output=True, text=True, cwd=ROOT,
    )
    m = re.search(r"RESULT: (PASS|WARN|FAIL)", r.stdout)
    return m.group(1) if m else "ERR"


def review_files(task: str) -> dict:
    """Review reports for a task, by kind. Combined files (questions-3-1-3-2-*) count for both."""
    found = {"lesson": {"AWS": [], "TEACHER": []}, "questions": {"AWS": [], "TEACHER": [], "STUDENT": []}}
    pat = re.compile(r"^(lesson|questions)-((?:\d-\d-?)+?)-?(AWS|TEACHER|STUDENT)[^/]*\.md$")
    for p in sorted(Q1.glob("*.md")):
        m = pat.match(p.name)
        if not m:
            continue
        kind, tasks, who = m.groups()
        nums = re.findall(r"\d-\d", tasks)
        if task.replace(".", "-") in nums and who in found[kind]:
            found[kind][who].append(p.relative_to(ROOT).as_posix())
    for who, files in QUESTION_REVIEW_EXTRA.get(task, {}).items():
        found["questions"][who] += files
    return found


def evaluate(rows: list, qs: dict):
    by_obj = {}
    for q in qs.values():
        if DEMO.match(q["id"]):
            continue
        for o in q.get("objectiveIds", []):
            by_obj.setdefault(o, set()).add(q["id"])
    audits = {}
    results = []
    for row in rows:
        task = row["task_id"]
        if task not in audits:
            audits[task] = audit_result(task)
        reasons = []
        refs = {d for d in row["drill_refs"] if not DEMO.match(d)}
        expect = by_obj.get(row["objective_id"], set())
        if refs != expect:
            reasons.append(f"drill_refs mismatch (+{sorted(expect - refs)} -{sorted(refs - expect)})")
        if not expect:
            reasons.append("no real drill")
        for d in sorted(expect):
            q = qs[d]
            if q.get("mcpStatus") != "verified" or not q.get("citationIds"):
                reasons.append(f"{d} not verified/cited")
        if not row["lesson_refs"]:
            reasons.append("no lesson")
        a = audits[task]
        if a != "PASS":
            reasons.append(f"audit {a} (CR-0024)")
        ev = []
        if task == PILOT:
            ev = [PROGRESS]
        else:
            rf = review_files(task)
            for kind in ("lesson", "questions"):
                for who, files in rf[kind].items():
                    if not files:
                        reasons.append(f"no {kind} {who} review report")
                    ev += files
            ev = list(dict.fromkeys([PROGRESS] + ev))
        for path in ev:
            if not (ROOT / path).exists():
                reasons.append(f"missing {path}")
        results.append({"row": row, "ok": not reasons, "reasons": reasons, "evidence": ev,
                        "drills": sorted(expect), "audit": a})
    return results


def apply(res: dict):
    row = res["row"]
    row["drill_refs"] = res["drills"]
    if res["ok"]:
        row["status"] = "verified"
        row["validation_refs"] = res["evidence"]
        row["owner"] = "lead-dev"
        row["next_action"] = ""
        row["gap"] = LIVE_NOTE if row["practice_mode"] == "live_aws" else ""
    else:
        row["status"] = "implemented_unverified"
        row["validation_refs"] = []
        row["gap"] = "Not verified: " + "; ".join(res["reasons"])
        row["next_action"] = "Close CR-0024, then re-run scripts/registry_verify.py --write"


def main() -> int:
    write = "--write" in sys.argv
    reg = json.loads(REG.read_text(encoding="utf-8"))
    results = evaluate(reg["rows"], load_questions())
    print(f"{'row':14} {'mode':15} {'drills':>6} {'audit':5} result")
    for r in results:
        row = r["row"]
        tail = "PASS" if r["ok"] else "FAIL " + "; ".join(r["reasons"])
        print(f"{row['objective_id']:14} {row['practice_mode']:15} {len(r['drills']):>6} {r['audit']:5} {tail}")
    n_ok = sum(r["ok"] for r in results)
    print(f"\n{n_ok} PASS / {len(results) - n_ok} FAIL of {len(results)}")
    if write:
        for r in results:
            apply(r)
        REG.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("registry written")
    else:
        print("read-only run; pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
