import json, sys
sys.stdout.reconfigure(encoding="utf-8")
iss = json.load(open(sys.argv[1] + "/deck/qa_issues2.json", encoding="utf-8"))
for i, x in enumerate(iss):
    if x["severity"] == "minor":
        print("[%d] %s p%s %s/%s: %s" % (i, x["reviewer"][:4], x["page"], x["slide"], x["where"], x["problem"][:150].replace("\n", " ")))
