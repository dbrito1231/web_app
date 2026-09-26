"""Build a Student fairness packet (no keys) and a separate answers file for a task.

Usage: python scripts/make_student_packet.py <task> <n> [out_dir]
  e.g. python scripts/make_student_packet.py 4-2 24
Pass n = the task's total question count so every question is in the packet.
Output goes to out_dir (default <system temp>/q1-packets), outside the repo.
"""
import json
import random
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"
task = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
OUT = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(tempfile.gettempdir()) / "q1-packets"
OUT.mkdir(parents=True, exist_ok=True)
lesson = json.loads((ROOT / "lessons" / f"lesson-{task}.json").read_text(encoding="utf-8"))
objs = set(lesson["objectiveIds"])
qs = sorted((json.loads(f.read_text(encoding="utf-8")) for f in (ROOT / "questions").glob("*.json")),
            key=lambda q: q["id"])
qs = [q for q in qs if objs & set(q.get("objectiveIds", []))]
if n < len(qs):
    random.seed(f"q1-{task}")
    qs = sorted(random.sample(qs, n), key=lambda q: q["id"])
packet = [f"# Student packet: task {task}\n", f"## Lesson: {lesson['title']}\n", lesson["bodyMarkdown"], "\n\n## Questions\n"]
answers = [f"# Answers: task {task}\n"]
for i, q in enumerate(qs, 1):
    packet.append(f"\n### Q{i} ({q['id']})\n\n{q['stem']}\n")
    packet.extend(f"- {c['id']}) {c['text']}" for c in q["choices"])
    answers.append(f"\n### Q{i} ({q['id']})\n\nCorrect: {', '.join(q['correctAnswerIds'])}\n\n{q['rationale']}\n")
(OUT / f"student-packet-{task}.md").write_text("\n".join(packet) + "\n", encoding="utf-8")
(OUT / f"student-answers-{task}.md").write_text("\n".join(answers) + "\n", encoding="utf-8")
print(f"{len(qs)} questions -> {OUT}")
