import sys, json
sys.stdout.reconfigure(encoding="utf-8")
want = int(sys.argv[2])
with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    for n, line in enumerate(f, 1):
        if n != want:
            continue
        o = json.loads(line)
        m = o.get("message", {})
        c = m.get("content")
        if isinstance(c, list):
            for part in c:
                if part.get("type") == "tool_result":
                    cc = part.get("content")
                    txt = cc if isinstance(cc, str) else " ".join(x.get("text", "") for x in cc if isinstance(x, dict))
                    print("[tool_result]", txt[:3800])
                elif part.get("type") == "tool_use":
                    print("[tool_use]", json.dumps(part.get("input"))[:600])
                elif part.get("type") == "text":
                    print("[text]", part["text"][:1500])
        break
