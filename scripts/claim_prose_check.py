"""Flag claim-table rows the lesson prose does not back up, and over-long quotes.

Teach-before-test means a question may only rely on a fact the learner actually
read. A number that lives only in the writer's claim table is not taught. This
was the most common round-1 finding on task 4.2.

Read-only. Usage: claim_prose_check.py <task>   e.g. 4-3, tf-g1
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUOTE_WORD_CAP = 20  # RULES.md: "a verbatim quote of 20 words or fewer"

# Bare small integers and years are too noisy to be useful signal.
IGNORE = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "2026", "2025", "004"}


def numbers_in(text: str) -> set[str]:
    return {n for n in re.findall(r"\d[\d,.]*", text) if n not in IGNORE}


def main(task: str) -> int:
    lesson = json.loads((ROOT / f"content/lessons/lesson-{task}.json").read_text(encoding="utf-8"))
    body = lesson["bodyMarkdown"]
    body_nums = numbers_in(body)

    report = ROOT / f"reports/fix-loop-r2/q1/lesson-{task}-impl.md"
    missing = []
    long_quotes = []
    for line in report.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() in ("#", "---") or set(cells[0]) <= {"-"}:
            continue
        section, claim = cells[1], cells[2]
        for n in sorted(numbers_in(claim) - body_nums):
            missing.append((cells[0], section, n, claim[:90]))
        # RULES.md caps the supporting quote at 20 words. A long quote tends to
        # carry more than the claim beside it, which is how a quote ends up
        # verbatim but supporting a different statement.
        quote = cells[-1].strip().strip('"')
        words = len(quote.split())
        if words > QUOTE_WORD_CAP:
            long_quotes.append((cells[0], words, quote[:70]))

    if long_quotes:
        print(f"WARN: {len(long_quotes)} claim-table quotes over "
              f"{QUOTE_WORD_CAP} words")
        for row, words, quote in long_quotes:
            print(f"  row {row} {words}w  <- {quote}")

    print(f"task {task}: {len(body_nums)} distinct numbers in lesson prose")
    if missing:
        print(f"WARN: {len(missing)} claim-table numbers absent from lesson prose")
        for row, section, n, claim in missing:
            print(f"  row {row} [{section}] {n!r}  <- {claim}")
    else:
        print("PASS: every claim-table number appears in the lesson prose")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
