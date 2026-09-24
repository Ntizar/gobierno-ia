# Escaneo s16: TODOS los bloques df* del vivo vs canon BOE archivado (DF 1ª-12ª si existen).
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
raw = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
h = open(BASE + r"/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()

txt = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S | re.I)
import html as H
txt = H.unescape(re.sub(r"<[^>]+>", "\n", txt)).replace("\xa0", " ")
flat = "\n".join(l.strip() for l in txt.split("\n") if l.strip())

allhits = [(m.start(), m.group(1).lower()) for m in re.finditer(r"Disposición final (\w+)\b", flat)]
ordenes = ["primera","segunda","tercera","cuarta","quinta","sexta","séptima","septima","octava","novena","décima","decima","undécima","undecima","duodécima","duodecima"]
canon = {}
for o in set(ordenes):
    hits = [p for p, w in allhits if w == o]
    if not hits:
        continue
    start = hits[1] if len(hits) > 1 else hits[0]
    after = [p for p, _ in allhits if p > start]
    canon[o] = flat[start:(after[0] if after else len(flat))].strip()

# bloques df* del vivo
parts = re.split(r"(?m)^(?=## \[)", raw)
WS = re.compile(r"\S+")
lineo = {"primera":"dfprimera","segunda":"dfsegunda","tercera":"dftercera","cuarta":"dfcuarta",
         "quinta":"dfquinta","sexta":"dfsexta","séptima":"dfseptima","octava":"dfoctava",
         "novena":"dfnovena","décima":"dfdecima","undécima":"dfundecima","duodécima":"dfduodecima"}
print("slug | vivos pal | canon pal | ¿cuerpo ausente?")
for p in parts:
    m = re.match(r"## \[(df[a-z]+)\]", p)
    if not m:
        continue
    slug = m.group(1)
    live_words = len(WS.findall(p))
    # encontrar orden
    o = None
    for ordn, s2 in lineo.items():
        if s2 == slug:
            o = ordn
    c = canon.get(o) or canon.get(o.replace("é","i") if o else "", "")
    cw = len(WS.findall(c)) if c else None
    print(slug, "|", live_words, "|", cw, "|", "SI" if (c and cw > live_words + 5) else "no")
