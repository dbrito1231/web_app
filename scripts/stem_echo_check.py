"""Find questions whose key can be picked by matching wording with the stem.

RULES.md (from task 4.4) requires a stem to state its requirement in the
scenario's own operational language rather than the lesson's distinctive
keywords, and forbids the key from echoing the stem. The failure it targets:
a reader spots the one option sharing a distinctive term with the stem and
picks it without understanding the material. Students scored 100% on tasks
3.5 through 4.3 and reported 9 of 22 stems on 4.3 as answerable this way.

A token counts as a GIVEAWAY when it appears in the stem and in exactly one
choice, and that choice is a key. Tokens in several choices are not giveaways,
because they do not single anything out -- which is also why this reports
stem/key echo rather than raw word overlap.

An ECHO is the same idea measured in bulk: the key shares strictly more
distinctive stem tokens than any distractor does. A question can echo without
having a giveaway when the overlap is spread across common terms.

Detecting the candidates is the easy half; classifying them is not, and no
script does it. RULES.md exempts a term that "simply names an object,
resource, or job the stem itself introduced into the scenario" -- a
structural scenario reference rather than a defect. So each flagged question
is classified by a reviewer and recorded in WAIVERS with a reason. An
unwaived giveaway fails the task; a waived one is listed and does not.

Filtering by how common a token is was tried and removed. It does nothing:
on task 4.4 every false positive ("billing", "daily", "audit", "dedicated",
"cloudfront") appeared in exactly one stem, because a coincidental rare word
and a genuine tell are both rare. No frequency threshold separates them, and
one set high enough to drop "availability" also dropped "gateway", "private"
and "hybrid", which are the terms most likely to carry a real tell.

Waivers are reviewer judgement, not a mute button. Add one only when a role
has said in a report that the reference is structural, and cite that report.

The gate applies from **task tf-g1 onward**, the same way the stem-paraphrase
rule applied from 4.4 onward. Tasks 1.1-4.4 closed before it existed and have
no waiver entries, so running it on them reports failures that were never
assessed against this standard.

Still blind to a paraphrase that is a one-to-one mapping ("semi-structured
documents" -> "JSON"), so the Student packet's two counts remain the real
measure.

Read-only. Usage: stem_echo_check.py <task>    e.g. 4-4, tf-g1
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Words that carry no discriminating signal in an exam stem.
STOP = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "for", "from",
    "has", "have", "in", "into", "is", "it", "its", "of", "on", "or", "that",
    "the", "their", "them", "then", "this", "to", "use", "uses", "using", "want",
    "wants", "with", "without", "while", "when", "which", "would", "should",
    "needs", "need", "needed", "new", "one", "two", "all", "each", "every",
    "must", "also", "only", "same", "other", "than", "per", "over", "under",
    "select", "team", "company", "platform", "workload", "workloads", "aws",
    "amazon", "account", "accounts", "service", "services", "cost", "costs",
    "keep", "keeps", "keeping", "across", "between", "during", "after", "before",
    "run", "runs", "running", "make", "makes", "set", "sets", "give", "gives",
    "traffic", "data", "instead", "still", "more", "most", "less", "least",
}

MIN_LEN = 5  # shorter words are rarely distinctive
WAIVERS_PATH = ROOT / "reports/fix-loop-r2/q1/stem-echo-waivers.json"


def tokens(text: str) -> set:
    words = re.findall(r"[a-z][a-z0-9-]+", text.lower())
    return {w for w in words if len(w) >= MIN_LEN and w not in STOP}


def load_waivers(task: str) -> dict:
    if not WAIVERS_PATH.exists():
        return {}
    return json.loads(WAIVERS_PATH.read_text(encoding="utf-8")).get(task, {})


def main(task: str) -> int:
    files = sorted((ROOT / "content/questions").glob(f"q-*-{task}-*.json"))
    lesson_path = ROOT / f"content/lessons/lesson-{task}.json"
    if lesson_path.exists():
        # Objective-group tasks (e.g. tf-g1) don't have a filename token that
        # matches the task id directly, so select by the lesson's own
        # objectiveIds instead -- the same approach q1_batch_check.py uses.
        objs = set(json.loads(lesson_path.read_text(encoding="utf-8"))["objectiveIds"])
        files = sorted(
            f for f in (ROOT / "content/questions").glob("q-*.json")
            if objs & set(json.loads(f.read_text(encoding="utf-8")).get("objectiveIds", []))
        )
    if not files:
        print(f"no question files for task {task}")
        return 1

    docs = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    waivers = load_waivers(task)

    giveaway, echo, waived = [], [], []
    for d in docs:
        keys = set(d["correctAnswerIds"])
        stem = tokens(d["stem"])
        per_choice = {c["id"]: tokens(c["text"]) & stem for c in d["choices"]}

        # A stem token is a giveaway when exactly one choice carries it and
        # that choice is a key.
        hits = []
        for tok in stem:
            holders = [cid for cid, toks in per_choice.items() if tok in toks]
            if len(holders) == 1 and holders[0] in keys:
                hits.append((tok, holders[0]))

        key_max = max((len(per_choice[k]) for k in keys), default=0)
        dis_max = max(
            (len(t) for cid, t in per_choice.items() if cid not in keys), default=0
        )
        short = d["id"].replace(f"q-saa-{task}-", "").replace(f"q-tf-004-{task}-", "")
        if hits and short in waivers:
            waived.append((short, sorted(hits), waivers[short]))
        elif hits:
            giveaway.append((short, sorted(hits)))
        elif key_max > dis_max and key_max > 0:
            echo.append((short, key_max, dis_max))

    print(f"task {task}: {len(files)} questions, "
          f"{len(waivers)} waiver(s) on file\n")
    if giveaway:
        print(f"GIVEAWAY -- a stem token appears in the key and no distractor ({len(giveaway)}):")
        for qid, hits in giveaway:
            pairs = ", ".join(f"{t} -> {c}" for t, c in hits)
            print(f"  {qid:10} {pairs}")
    if echo:
        print(f"\nECHO -- key shares more stem wording than any distractor ({len(echo)}):")
        for qid, km, dm in echo:
            print(f"  {qid:10} key={km} tokens, best distractor={dm}")
    if waived:
        print(f"\nWAIVED -- reviewer recorded these as structural ({len(waived)}):")
        for qid, hits, why in waived:
            pairs = ", ".join(f"{t} -> {c}" for t, c in hits)
            print(f"  {qid:10} {pairs}")
            print(f"{'':13}{why}")
    if not giveaway and not echo and not waived:
        print("no stem/key echo found")

    print(f"\n{len(giveaway)} unwaived giveaway, {len(waived)} waived, "
          f"{len(echo)} bulk echo, of {len(files)} questions")
    if echo:
        print("Bulk echo is advisory: read those, do not assume a defect.")
    print(f"RESULT: {'FAIL' if giveaway else 'PASS'}")
    return 1 if giveaway else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
