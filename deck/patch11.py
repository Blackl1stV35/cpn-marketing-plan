import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
old = '''    wanted = [s["headline"]] + ["Sources: " + x for x in []] + strings(s["body"]) + list(s["sources"])'''
new = '''    wanted = ([] if s["layout"] == "title" else [s["headline"]]) + strings(s["body"]) + list(s["sources"])'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
print("ok")
