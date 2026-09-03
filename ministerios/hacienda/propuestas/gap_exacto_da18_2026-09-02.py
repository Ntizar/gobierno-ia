# Diff exacto DA18: parrafos del repo vs los 11 del BOE vivo (match por sha256 normalizado)
import re, io, sys, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def shaci(p): return hashlib.sha256(norm(p).encode()).hexdigest()

boe = json.load(open("../evidencia/da18_boe_full_2026-09-02.json", encoding="utf-8"))
boe_by_h = {}
for p in boe:
    if p["class"] in ("parrafo", "parrafo_2", "nota_pie", "p", "pie_unico"):
        boe_by_h[shaci(p["text"])] = p

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
body = m.group(1)
pars = [p for p in re.split(r"\n\s*\n", body) if norm(p)]
print("repo:", len(pars), "| BOE:", len(boe_by_h))
repo_hashes = set()
for i, p in enumerate(pars, 1):
    h = shaci(p)
    repo_hashes.add(h)
    tag = "EN_BOE" if h in boe_by_h else "SOBRA "
    print(i, tag, "|", norm(p)[:72])
print("\n--- parrafos BOE que NO estan en el repo ---")
for h, p in boe_by_h.items():
    if h not in repo_hashes:
        print("FALTA", p["class"], "|", norm(p["text"])[:90])
