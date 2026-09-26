"""Read-only batch checker for one Q1 task (lesson + its questions).

Usage: python scripts/q1_batch_check.py 3-1      (SAA lesson-3-1)
       python scripts/q1_batch_check.py tf-g1    (Terraform lesson-tf-g1)

Prints PASS/WARN/FAIL lines; exits 1 if any FAIL. Writes nothing.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TELLS = re.compile(
    r"\b(since|even though|which does not|despite|requiring|must|without changing|so that)\b", re.I
)
LETTER = re.compile(r"\b(choice|option|answer)\s+\(?[a-e]\)?(?=[\s,.;:)]|$)|\([a-e]\)", re.I)
RETIRED = re.compile(r"\b(Copilot|Snowball|Snowcone|Snowmobile|FSx File Gateway|CodeCommit|Cloud9|CodeStar|QLDB)\b")
SINGLE_AST = re.compile(r"(?<!\*)\*(?!\*)")

results = []


def report(level, msg):
    results.append(level)
    print(f"{level}: {msg}")


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def objective_texts():
    texts = {}
    for f in (CONTENT / "objectives").glob("*.json"):
        data = load(f)
        items = data if isinstance(data, list) else data.get("objectives", [])
        for o in items:
            if isinstance(o, dict) and o.get("id"):
                texts[o["id"]] = str(o.get("text") or o.get("title") or "")
    return texts


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    task = sys.argv[1]
    lesson_path = CONTENT / "lessons" / f"lesson-{task}.json"
    lesson = load(lesson_path)
    objs = set(lesson["objectiveIds"])
    questions = []
    for f in sorted((CONTENT / "questions").glob("*.json")):
        q = load(f)
        if objs & set(q.get("objectiveIds", [])):
            questions.append(q)
    ids = [q["id"] for q in questions]
    cites = {p.stem for p in (CONTENT / "citations").glob("*.json")}
    otexts = objective_texts()
    print(f"task {task}: {len(questions)} questions")

    # Lesson checks
    body = lesson.get("bodyMarkdown", "")
    stripped = re.sub(r"\*\*[^*]+\*\*", "", body)
    n_ast = len(SINGLE_AST.findall(stripped))
    report("PASS" if n_ast == 0 else "FAIL", f"lesson single-asterisk spans: {n_ast}")
    bad_md = [l for l in body.splitlines() if l.lstrip().startswith("|") or re.match(r"\s*\d+\.\s", l)]
    report("PASS" if not bad_md else "FAIL", f"lesson tables/numbered lines: {len(bad_md)}")
    if re.search(r"\[[^\]]+\]\([^)]+\)", body):
        report("FAIL", "lesson contains a markdown link")
    missing_c = [c for c in lesson.get("citationIds", []) if c not in cites]
    report("PASS" if not missing_c else "FAIL", f"lesson citations unresolved: {missing_c}")
    drill = lesson.get("drillIds", [])
    report("PASS" if sorted(drill) == sorted(ids) else "FAIL",
           f"drillIds match questions (missing {sorted(set(ids) - set(drill))}, extra {sorted(set(drill) - set(ids))})")
    report("PASS" if body.count("**Exam tip:**") >= len(objs) else "WARN",
           f"exam tips {body.count('**Exam tip:**')} for {len(objs)} objectives")
    for m in RETIRED.finditer(body):
        ctx = body[max(0, m.start() - 80): m.end() + 80].replace("\n", " ")
        report("WARN", f"lesson names retired/closed service '{m.group(0)}': ...{ctx}...")

    # Question checks
    openings = collections.Counter()
    mc = long_key = 0
    mc_pos, mr_pos = collections.Counter(), collections.Counter()
    for q in questions:
        qid = q["id"]
        openings[" ".join(q["stem"].lower().split()[:6])] += 1
        ch = {c["id"]: c["text"] for c in q["choices"]}
        keys = q["correctAnswerIds"]
        if q["type"] == "mc":
            mc += 1
            mc_pos[keys[0]] += 1
            if len(ch[keys[0]]) == max(len(t) for t in ch.values()):
                long_key += 1
            if len(ch) != 4:
                report("FAIL", f"{qid}: MC has {len(ch)} choices")
        else:
            for k in keys:
                mr_pos[k] += 1
            if len(ch) != 5:
                report("FAIL", f"{qid}: MR has {len(ch)} choices")
            if "(Select" not in q["stem"]:
                report("FAIL", f"{qid}: MR stem lacks '(Select N.)'")
        if q.get("selectCount", 1) != len(keys):
            report("FAIL", f"{qid}: selectCount {q.get('selectCount')} != {len(keys)} keys")
        if LETTER.search(q.get("rationale", "")):
            report("FAIL", f"{qid}: letter reference in rationale")
        for cid, t in ch.items():
            m = TELLS.search(t)
            if m:
                report("WARN", f"{qid} choice {cid}{' (KEY)' if cid in keys else ''}: tell word '{m.group(0)}': {t[:90]}")
            r = RETIRED.search(t)
            if r:
                report("WARN", f"{qid} choice {cid}{' (KEY)' if cid in keys else ''}: retired/closed '{r.group(0)}'")
            for oid in q.get("objectiveIds", []):
                ot = otexts.get(oid, "")
                if ot and len(ot) > 25 and ot.lower() in t.lower():
                    report("FAIL", f"{qid} choice {cid}: pastes objective text")
        for oid in q.get("objectiveIds", []):
            ot = otexts.get(oid, "")
            if ot and len(ot) > 25 and ot.lower() in q["stem"].lower():
                report("FAIL", f"{qid}: stem pastes objective text")
        qc = q.get("citationIds", [])
        if not qc:
            report("FAIL", f"{qid}: no citationIds")
        for c in qc:
            if c not in cites:
                report("FAIL", f"{qid}: citation {c} unresolved")
        if q.get("mcpStatus") != "verified" or q.get("reviewedOn") != "2026-09-26":
            report("FAIL", f"{qid}: mcpStatus/reviewedOn not verified/2026-09-26")
        if "Which action is the right fit for this requirement" in q["stem"]:
            report("FAIL", f"{qid}: still a placeholder stem")
    dups = [o for o, n in openings.items() if n > 1]
    report("PASS" if not dups else "FAIL", f"duplicate 6-word openings: {dups}")
    if mc:
        rate = long_key / mc
        report("PASS" if rate <= 0.35 else "FAIL", f"longest-is-key {long_key}/{mc} = {rate:.0%}")
        spread = max(mc_pos.values()) - min(mc_pos.get(k, 0) for k in "abcd")
        report("PASS" if spread <= max(2, mc // 4) else "WARN", f"MC key positions {dict(sorted(mc_pos.items()))}")
    if mr_pos:
        report("PASS" if len(mr_pos) >= 4 else "WARN", f"MR key slots {dict(sorted(mr_pos.items()))}")
    print("RESULT:", "FAIL" if "FAIL" in results else ("WARN" if "WARN" in results else "PASS"))
    return 1 if "FAIL" in results else 0


if __name__ == "__main__":
    sys.exit(main())
