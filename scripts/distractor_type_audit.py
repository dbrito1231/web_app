import json, glob, collections

TERMS = ["Outpost", "Local Zone", "Wavelength", "Savings Plan", "Reserved Instance",
         "Spot", "Auto Scaling", "Lambda", "Fargate", "Graviton", "Compute Optimizer",
         "hibernat", "Global Accelerator", "Classic Load Balancer"]

files = sorted(glob.glob("content/questions/q-saa-4-2-*.json"))
cnt = collections.Counter()
where = collections.defaultdict(list)

for f in files:
    d = json.load(open(f, encoding="utf-8"))
    keys = set(d["correctAnswerIds"])
    seen = set()
    for ch in d["choices"]:
        if ch["id"] in keys:
            continue
        for t in TERMS:
            if t.lower() in ch["text"].lower():
                seen.add(t)
    for t in seen:
        cnt[t] += 1
        where[t].append(d["id"].replace("q-saa-4-2-", ""))

print(f"{len(files)} questions; cap at 15% = 3 questions\n")
for t, c in cnt.most_common():
    flag = "   <-- OVER CAP" if c > 3 else ""
    print(f"{t:22}{c:3d}{c / len(files) * 100:5.0f}%  {','.join(where[t])}{flag}")
