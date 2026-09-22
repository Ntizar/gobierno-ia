# Reextrae canon DA 11 y 20 filtrando el aparato web del BOE y mide palabras
# current (fichero de ley) vs canon (evidencia) por bloque.
import re, hashlib

SRC = "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html"
LAW = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"

raw = open(SRC, encoding="utf-8", errors="replace").read()
txt = re.sub(r"<[^>]+>", "\n", raw)
import html as H
txt = H.unescape(txt)
txt = re.sub(r"[ \t]+", " ", txt)
BAD = ("Ref. BOE", "Seleccionar redacci", "Última actualizaci", "Texto original, publicado",
       "Subir", "[Bloque", "Se deroga", "Se añade", "Añadido", "Redacción anterior")
lines = [l.strip() for l in txt.splitlines() if l.strip()]
joined = [l for l in lines if not any(l.startswith(b) for b in BAD)]
J = "\n".join(joined)

def grab(inicio, fin):
    i = J.find(inicio)
    j = J.find(fin, i + len(inicio))
    return J[i:j].strip()

canon = {
    "da11": grab("Disposición adicional undécima.", "Disposición adicional duodécima."),
    "da20": grab("Disposición adicional vigésima.", "Disposición adicional vigésimo primera"),
}
res = []
for k, v in canon.items():
    h = hashlib.sha256(v.encode("utf-8")).hexdigest()
    res.append(f"### {k}: {len(v.split())} palabras, sha256 {h}")
    res.append(v)
    res.append("")
open("ministerios/hacienda/evidencia/boe_canonico_da11_da20_2026-09-22.txt", "w", encoding="utf-8").write("\n".join(res))

law = open(LAW, encoding="utf-8").read()
for tag, ini, fin in (("[daundecima]", "## [daundecima]", "## [daduodecima]"),
                      ("[davigesima]", "## [davigesima]", "## [davigesimoprimera]")):
    i = law.find(ini); j = law.find(fin, i + 1)
    body = law[i:j]
    w = len(body.split())
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    print(tag, "ACTUAL:", w, "palabras, sha256", h[:16])
for k, v in canon.items():
    print("CANON", k, len(v.split()), "palabras")
