"""Confirm a choice reorder preserved WHICH OPTION TEXTS are correct.

Reordering choices to fix key-position bias means renumbering `correctAnswerIds`
in lockstep. Get that wrong and the file publishes a wrong answer while every
other check still passes, because the JSON stays structurally valid.

This compares the SET OF CORRECT-ANSWER TEXTS at a git revision against the
working tree. Key letters are expected to change; the texts must not.

Read-only. Usage: key_text_diff.py <task> <git-rev>   e.g. 4-3 affd274
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def key_texts(doc: dict) -> set[str]:
    keys = set(doc["correctAnswerIds"])
    return {c["text"].strip() for c in doc["choices"] if c["id"] in keys}


def main(task: str, rev: str) -> int:
    bad = moved = 0
    for path in sorted((ROOT / "content/questions").glob(f"q-*-{task}-*.json")):
        rel = path.relative_to(ROOT).as_posix()
        old_raw = subprocess.run(
            ["git", "show", f"{rev}:{rel}"], capture_output=True, text=True,
            encoding="utf-8", cwd=ROOT,
        )
        if old_raw.returncode != 0:
            print(f"SKIP {rel} (not present at {rev})")
            continue
        old, now = json.loads(old_raw.stdout), json.loads(path.read_text(encoding="utf-8"))
        qid = now["id"]
        o, n = key_texts(old), key_texts(now)
        if o != n:
            bad += 1
            print(f"MISMATCH {qid}")
            for t in sorted(o - n):
                print(f"     was correct, now not: {t[:95]}")
            for t in sorted(n - o):
                print(f"     now correct, was not: {t[:95]}")
        elif old["correctAnswerIds"] != now["correctAnswerIds"]:
            moved += 1

    print(f"\n{'FAIL' if bad else 'PASS'}: {bad} questions changed which option text "
          f"is correct ({moved} reordered safely)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
