# Diff fino de los pares "casi literales" de la DA18 (p8/p16, p10/p17, p12/p18, p1/p14)
import re, io, sys, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
pars = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", m.group(1)) if re.sub(r"\s+", " ", p).strip()]
def norm_ci(s): return s.casefold().replace("1. ", "").strip()
for a, b in [(1, 14), (8, 16), (10, 17), (12, 18)]:
    print(f"=== par {a} vs {b} (len {len(pars[a])} / {len(pars[b])}) ===")
    sm = difflib.SequenceMatcher(None, pars[a], pars[b])
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print(" ", tag, "|A:", repr(pars[a][i1:i2])[:120], "|B:", repr(pars[b][j1:j2])[:120])
# tambien contra el parrafo 21 (intro sin numero, que SI esta en BOE)
print("=== par14 vs par21 ===")
sm = difflib.SequenceMatcher(None, pars[14], pars[21])
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        print(" ", tag, "|A:", repr(pars[14][i1:i2])[:140], "|B:", repr(pars[21][j1:j2])[:140])
