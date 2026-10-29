import json, sys
sys.stdout.reconfigure(encoding="utf-8")
labels = {}
for line in open(sys.argv[1], encoding="utf-8"):
    o = json.loads(line)
    if o.get("type") == "started":
        labels[o["agentId"]] = o.get("label")
    if o.get("type") == "result":
        r = o["result"]
        lab = labels.get(o["agentId"])
        if len(sys.argv) > 2 and sys.argv[2] not in (lab or ""):
            continue
        print("\n##########", lab)
        print("SUMMARY:", r.get("summary", "")[:1500])
        for i, it in enumerate(r.get("issues", []), 1):
            print("\n[%d] %s | %s" % (i, it["severity"], it["where"][:200]))
            print("  PROBLEM:", it["problem"][:900])
            print("  QUOTE  :", it["quote"][:300])
            print("  FIX    :", it["fix"][:700])
