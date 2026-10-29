import json, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(t[t.find("{"):])
r = d["result"]
print({s["reviewer"]: s["n"] for s in r["summaries"]})
iss = r["issues"]
sev = {}
for x in iss: sev[x["severity"]] = sev.get(x["severity"], 0) + 1
print(sev)
json.dump(iss, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for i, x in enumerate(iss):
    if x["severity"] in ("critical", "major"):
        print("\n[%d] %s %s p%s %s/%s" % (i, x["severity"].upper(), x["reviewer"], x["page"], x["slide"], x["where"]))
        print("  PROBLEM:", x["problem"][:600])
        print("  FIX:", x["fix"][:500])
