# Los 18 parrafos sobrantes de DA18: existen en el BOE archivado 09-01? (trazabilidad)
import re, io, sys, json, html as H, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def shaci(p): return hashlib.sha256(norm(p).encode()).hexdigest()

def section(fname, start, end):
    raw = open(fname, encoding="utf-8", errors="replace").read()
    i = raw.find(start); j = raw.find(end, i + 10)
    sec = raw[i:j]
    out = {}
    for m in re.finditer(r'<(p|blockquote)[^>]*>(.*?)</\1>', sec, flags=re.S):
        t = re.sub(r"<[^>]+>", "", m.group(2))
        t = norm(H.unescape(t))
        if t:
            out[shaci(t)] = t
    return out

arch = section("../evidencia/boe_consolidado_BOE-A-2003-23186.html", 'id="dadecimoctava"', 'id="dadecimonovena"')
vivo = json.load(open("../evidencia/da18_boe_full_2026-09-02.json", encoding="utf-8"))
vivoset = set()
for p in vivo:
    vivoset.add(shaci(p["text"]))

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
pars = [p for p in re.split(r"\n\s*\n", m.group(1)) if norm(p)]
sobrantes = [p for p in pars if shaci(p) not in vivoset and not p.startswith("## [")]
# quitar el parrafo 1 que es el titulo repetido
sobrantes = [p for p in sobrantes if shaci(p) not in vivoset]
print("archivado 09-01: parrafos unicos:", len(arch), "| hoy vivo:", len(vivoset), "| sobrantes repo:", len(sobrantes))
en_arch = sum(1 for p in sobrantes if shaci(p) in arch)
print("sobrantes presentes en BOE ARCHIVADO 09-01:", en_arch)
print("sobrantes sin traza en NINGUN BOE:", len(sobrantes) - en_arch)
for p in sobrantes:
    h = shaci(p)
    tag = "TRAZA-ARCHIVADO" if h in arch else "SIN-TRAZA"
    print(tag, "|", len(p.split()), "w |", norm(p)[:60])
