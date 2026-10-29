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
        if lab == "check:nation-2026c":
            print("== nation-2026c: supported:", r.get("supported"))
            print("  figures:", r.get("figures_found")[:700])
            print("  notes:", r.get("notes")[:1500])
        if lab == "proofread":
            print("== proofread:", r.get("summary"))
            for it in r.get("issues", []):
                print("  ISSUE where:", it["where"][:140])
                print("        problem:", it["problem"][:400])
                print("        fix:", it["fix"][:300])
