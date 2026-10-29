import json, sys
t = open(sys.argv[1], encoding="utf-8").read()
i = t.find("{")
try:
    d = json.loads(t[i:])
except Exception as e:
    # output file may wrap; try last JSON object
    j = t.rfind('\n{')
    d = json.loads(t[j:])
print("keys", list(d.keys()))
for k, v in d.items():
    if isinstance(v, list):
        print(k, "list", len(v))
    elif isinstance(v, dict):
        print(k, "dict", list(v.keys())[:12])
    else:
        print(k, str(v)[:300])
sw = d.get("sweep") or d.get("final") or d.get("final_sweep")
if sw:
    print(json.dumps(sw, ensure_ascii=False, indent=1)[:6000])
