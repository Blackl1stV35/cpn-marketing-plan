import json, sys
sys.stdout.reconfigure(encoding="utf-8")
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
print("lines:", len(lines))
for ln in lines[-4:]:
    try:
        o = json.loads(ln)
    except Exception as e:
        print("bad line", e); continue
    m = o.get("message", {})
    c = m.get("content")
    if isinstance(c, list):
        for part in c:
            t = part.get("type")
            if t == "text":
                print("[%s text] %s" % (m.get("role"), part["text"][:700]))
            elif t == "tool_use":
                print("[tool_use] %s %s" % (part.get("name"), json.dumps(part.get("input"))[:400]))
            elif t == "tool_result":
                cc = part.get("content")
                s = json.dumps(cc)[:500] if not isinstance(cc, str) else cc[:500]
                print("[tool_result] %s" % s)
    else:
        print("[%s] %s" % (m.get("role"), str(c)[:500]))
