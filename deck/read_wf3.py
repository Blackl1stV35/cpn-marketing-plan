import json, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(t[t.find("{"):])
r = d["result"]
for i, f in enumerate(r["fixed"]):
    if i < 3:
        continue
    print("== fixer", i)
    for u in f.get("unresolved", []):
        print("  UNRESOLVED:", u[:600])
sev = {}
for it in r["issues"]:
    sev[it.get("severity")] = sev.get(it.get("severity"), 0) + 1
print("issue severities:", sev)
