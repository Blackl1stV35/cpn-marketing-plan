import json, sys
t = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(t[t.find("{"):])
r = d["result"]
print("logs:", d["logs"])
print("verified:", json.dumps(r["verified"], ensure_ascii=False)[:1500])
print("n issues:", len(r["issues"]) if isinstance(r["issues"], list) else r["issues"])
print("fixed:", json.dumps(r["fixed"], ensure_ascii=False)[:3000])
print("FINAL:", json.dumps(r["final"], ensure_ascii=False, indent=1)[:9000])
