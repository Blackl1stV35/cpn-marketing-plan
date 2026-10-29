import json, sys
sys.stdout.reconfigure(encoding="utf-8")
rs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if '"type":"result"' in l]
r = rs[3]["result"]
print("cluster:", r.get("cluster"), "changes:", len(r["changes"]))
for c in r["changes"]:
    print(" -", c["slide"], c["field"], "|", (c.get("after") or "")[:260].replace("\n", " "))
for u in r["unresolved"]:
    print(" UNRESOLVED:", u[:700])
