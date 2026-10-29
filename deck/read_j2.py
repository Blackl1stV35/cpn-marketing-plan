import json, sys
sys.stdout.reconfigure(encoding="utf-8")
for line in open(sys.argv[1], encoding="utf-8"):
    o = json.loads(line)
    if o.get("type") == "result":
        r = o["result"]
        if r.get("cluster") == "SITUATION":
            continue
        print("== CLUSTER", r.get("cluster"), "changes", len(r.get("changes", [])))
        for c in r.get("changes", [])[:40]:
            print(" -", c["slide"], c["field"], "|", (c.get("after") or "")[:130].replace("\n", " "))
        for u in r.get("unresolved", []):
            print(" UNRESOLVED:", u[:600])
