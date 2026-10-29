import fitz, sys
doc = fitz.open(sys.argv[1])
print("fitz", fitz.__doc__[:60] if fitz.__doc__ else "", getattr(fitz, "VersionBind", ""))
ls = doc[0].get_links()
print(len(ls), ls[:2])
names = doc.resolve_names()
print(len(names), list(names.items())[:2])
print(doc[3].get_links()[:2])
print(doc.get_toc()[:3])
