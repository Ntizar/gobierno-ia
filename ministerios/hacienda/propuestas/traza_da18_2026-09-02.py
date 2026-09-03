# Traza de los 18 parrafos "sobrantes" de la DA18 contra el BOE ARCHIVADO del 09-01
# (decidir si es texto legal con fuente o invencion de la conversion)
import re, io, sys, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def sha(s, ci=False):
    t = norm(s)
    if ci: t = t.casefold()
    return hashlib.sha256(t.encode()).hexdigest()

raw01 = open("../evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
i = raw01.find('id="dadecimoctava"')
j = raw01.find('id="dadecimonovena"', i + 10)
sec01 = raw01[i:j]
import html as H
boe01 = {}
for m in re.finditer(r'<(p|blockquote|h5)[^>]*>(.*?)</\1>', sec01, re.S):
    t = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()).strip()
    if t:
        boe01[sha(t)] = t
        boe01[sha(t, True)] = t
print("parrafos BOE archivado 09-01 (DA18):", len(set(boe01.values())))

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
repo_pars = [p for p in re.split(r"\n\s*\n", m.group(1)) if norm(p)]
for k, p in enumerate(repo_pars):
    exact = sha(p) in boe01
    ci = sha(p, True) in boe01
    tag = "EXACTO" if exact else ("IGNORANDO_MAYUSCULAS" if ci else "NO_ESTA_EN_BOE")
    print(k, "|", tag, "|", len(p.split()), "pal |", norm(p)[:70])
