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
# A rationale must name options by content, never by letter. The old pattern
# only caught "choice c" / "option b" / "(c)": it passed all 10 tf-g4
# rationales written as "c is wrong because ...", and it flagged the English
# "so they answer a different question". A bare letter only counts when a
# predicate verb follows it, and "a" only before verbs the article never takes.
_VERBS = (r"(?:is|isn't|was|misstates|reverses|overreaches|names|claims|confuses|describes|"
          r"fails|gets|swaps|invents|would|directly|also|only|and|or|correctly|wrongly|"
          r"contradicts|assumes|mixes|picks|offers|uses|adds|ignores|repeats)")
LETTER = re.compile(
    r"\b(?:choice|option)\s+\(?[a-eA-E]\)?(?=[\s,.;:)]|$)"
    r"|\([a-eA-E]\)"
    r"|(?<![\w`'\".\-/])[b-e]\s+" + _VERBS + r"\b"
    r"|(?<![\w`'\".\-/])a\s+(?:is|isn't|was|misstates|reverses|overreaches|claims|confuses|"
    r"fails|swaps|invents|contradicts)\b"
    r"|(?:^|[.;:]\s+|--\s+|,\s+)[A-E]\s+" + _VERBS + r"\b"
)
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
    # Code spans render literally, so a wildcard like `/api/*` is not italics.
    stripped = re.sub(r"`[^`]*`", "", re.sub(r"\*\*[^*]+\*\*", "", body))
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
    mc = long_key = short_key = 0
    mc_pos, mr_pos = collections.Counter(), collections.Counter()
    mr_sets = collections.Counter()
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
            # The mirror tell. Capping only "longest is key" pushes a writer
            # to make keys conspicuously short instead: tf-g4's first draft
            # was flagged at 38% longest, and the fix landed at 0% longest
            # and 38% shortest, which is the same giveaway inverted.
            if len(ch[keys[0]]) == min(len(t) for t in ch.values()):
                short_key += 1
            if len(ch) != 4:
                report("FAIL", f"{qid}: MC has {len(ch)} choices")
        else:
            mr_sets[",".join(sorted(keys))] += 1
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
        srate = short_key / mc
        report("PASS" if srate <= 0.35 else "FAIL",
               f"shortest-is-key {short_key}/{mc} = {srate:.0%}")
        spread = max(mc_pos.values()) - min(mc_pos.get(k, 0) for k in "abcd")
        report("PASS" if spread <= max(2, mc // 4) else "WARN", f"MC key positions {dict(sorted(mc_pos.items()))}")
    if mr_pos:
        report("PASS" if len(mr_pos) >= 4 else "WARN", f"MR key slots {dict(sorted(mr_pos.items()))}")
        # Distinct slots alone hide the real tell: the same key combination
        # repeated. "Always answer a,b" must not score well without reading.
        n_mr = sum(mr_sets.values())
        combo, hits = mr_sets.most_common(1)[0]
        report(
            "PASS" if n_mr < 4 or hits / n_mr <= 0.4 else "FAIL",
            f"MR key sets: most common '{combo}' in {hits}/{n_mr} "
            f"({hits / n_mr:.0%}); all {dict(mr_sets.most_common())}",
        )
    print("RESULT:", "FAIL" if "FAIL" in results else ("WARN" if "WARN" in results else "PASS"))
    return 1 if "FAIL" in results else 0


if __name__ == "__main__":
    sys.exit(main())
