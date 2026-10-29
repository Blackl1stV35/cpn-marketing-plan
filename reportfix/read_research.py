import json, sys
sys.stdout.reconfigure(encoding="utf-8")
for line in open(sys.argv[1], encoding="utf-8"):
    o = json.loads(line)
    if o.get("type") == "result":
        r = o["result"]
        print("--", o.get("agentId"), "verified:", r.get("verified"))
        for k in ("author", "date", "title", "url", "page_or_section", "quote", "notes"):
            print("  %s: %s" % (k, str(r.get(k))[:400]))
