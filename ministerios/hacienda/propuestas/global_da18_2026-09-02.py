# Buscar los parrafos "sobrantes" de la DA18 en TODO el BOE archivado (otra disposicion?) y en el vivo
import re, io, sys, hashlib, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def shaci(s): return hashlib.sha256(norm(s).casefold().encode()).hexdigest()

for f in ("boe_consolidado_BOE-A-2003-23186.html", "boe_vivo_LGT_2026-09-02.html"):
    raw = open("../evidencia/" + f, encoding="utf-8", errors="replace").read()
    idx = {}
    for m in re.finditer(r'<(p|blockquote|h5)[^>]*>(.*?)</\1>', raw, re.S):
        t = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()).strip()
        if t:
            idx.setdefault(shaci(t), 0)
            idx[shaci(t)] += 1
    print(f, "-> parrafos unicos:", len(idx), "| total:", sum(idx.values()))
    if f.startswith("boe_consolidado"):
        g01 = idx
    else:
        g02 = idx

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
pars = [p for p in re.split(r"\n\s*\n", m.group(1)) if norm(p)]
print("=== parrafos de la DA18 del repo: localizacion global en cada BOE (casefold) ===")
for k, p in enumerate(pars):
    h = shaci(p)
    print(k, "| en_archivado:", g01.get(h, 0), "| en_vivo:", g02.get(h, 0), "|", norm(p)[:75])
