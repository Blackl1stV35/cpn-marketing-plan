import json, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(t[t.find("{"):])
v = d["result"]["verdicts"]
for x in v:
    print(x["id"], "PASS" if x.get("pass") else "FAIL", "spoken", x.get("spoken"), "edited", x.get("edited"))
    for i in x.get("issues", [])[:3]:
        print("    ", i[:300])
