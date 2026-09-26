import sqlite3, hashlib, json, sys
p = sys.argv[1]
c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
h = hashlib.sha256("\n".join(c.iterdump()).encode()).hexdigest()
tables = [r[0] for r in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
counts = {t: c.execute(f'select count(*) from "{t}"').fetchone()[0] for t in tables}
print(json.dumps({"sha256_iterdump": h, "integrity": c.execute("pragma integrity_check").fetchone()[0], "workbook_counts": {k:v for k,v in counts.items() if k.startswith("workbook")}}, indent=1))
