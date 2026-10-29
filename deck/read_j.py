import json, sys
sys.stdout.reconfigure(encoding="utf-8")
for line in open(sys.argv[1], encoding="utf-8"):
    o = json.loads(line)
    if o.get("type") == "result":
        r = o["result"]
        print("CLUSTER", r.get("cluster"), "changes", len(r.get("changes", [])))
        for c in r.get("changes", []):
            print(" -", c["slide"], c["field"], "|", (c.get("after") or "")[:170].replace("\n", " "))
        print(" must_keep:", len(r.get("must_keep", [])), "unresolved:", r.get("unresolved"))
