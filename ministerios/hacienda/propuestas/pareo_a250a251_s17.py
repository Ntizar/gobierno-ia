# Canon de arts. 250 y 251 LGT + comparación contra bloque vivo (sesión 17, 25-09)
import json, re, hashlib

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + tag + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0).rstrip("\n") if m else None

for aid in ("a250", "a251"):
    a = arts.get(aid)
    b = bloque(aid)
    cp = len((a["texto"] or "").split()) if a else -1
    bp = len(b.split()) if b else -1
    print("=====", aid, "| canon titulo:", (a or {}).get("titulo", "?")[:80])
    print("canon palabras:", cp, "| bloque vivo palabras:", bp)
    # ¿está el texto del canon contenido (normalizado) en el bloque vivo?
    def norm(s):
        return re.sub(r"\s+", " ", s).strip().lower()
    if a and b:
        cn = norm(a["texto"])
        bn = norm(b)
        print("canon en vivo:", cn in bn, "| vivo en canon:", bn.replace("## [" + aid + "] " + (a.get("titulo") or ""), "").strip() [:0] or "n/a")
        # faltantes: párrafos del canon que no están en el vivo
        falt = []
        for par in a["texto"].split("\n"):
            par = par.strip()
            if par and norm(par) not in bn:
                falt.append((len(par.split()), par[:110]))
        print("PÁRRAFOS DEL CANON AUSENTES EN EL BLOQUE VIVO:", len(falt), "palabras:", sum(f[0] for f in falt))
        for f in falt:
            print("  -", f[0], "pal |", f[1])
    if b:
        h = hashlib.sha256(b.replace("\r\n", "\n").encode("utf-8")).hexdigest()
        print("hash vivo (conv. Auditor):", h)
json_out = {}
for aid in ("a250", "a251"):
    a = arts.get(aid)
    if a:
        json_out[aid] = {"titulo": a.get("titulo"), "texto": a.get("texto")}
open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/canon_a250_a251_2026-09-25.json", "w", encoding="utf-8").write(json.dumps(json_out, ensure_ascii=False, indent=1))
print("guardado evidencia/canon_a250_a251_2026-09-25.json")
