import json, sys
sys.stdout.reconfigure(encoding="utf-8")
iss = json.load(open(sys.argv[1] + "/deck/qa_issues2.json", encoding="utf-8"))
print(iss[0]["fix"])
