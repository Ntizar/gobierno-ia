# v2: dedupe conservando PRIMERA copia; validar canon ⊆ propuesto en los tres bloques (s17)
import json, re, hashlib

ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
EV = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ").replace("\u202f", " ")).strip().lower()

def bloque_raw(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0).rstrip("\n")

resumen = {}
for tag in ("a229", "a203", "a188"):
    b = bloque_raw(tag)
    lines = b.split("\n")
    header, body = lines[0], [l for l in lines[1:] if l.strip()]
    out, seen = [], set()
    for l in body:                       # PRIMERA copia
        k = norm(l)
        if k in seen:
            continue
        seen.add(k)
        out.append(l)
    titulo = arts[tag]["titulo"].strip()
    out = [l for l in out if not re.match(r"^Artículo \d+\.", l.strip())]
    prop = (header + "\n\n" + titulo + "\n\n" + "\n".join(out)).rstrip()

    np_ = norm(prop)
    ct = norm(arts[tag]["texto"])
    cubierto = ct in np_
    w_v, w_p = len(b.split()), len(prop.split())
    resumen[tag] = dict(vivo=w_v, propuesto=w_p, ahorro=w_v - w_p,
                        sha_vivo=hashlib.sha256(b.replace("\r\n","\n").encode()).hexdigest(),
                        sha_prop=hashlib.sha256(prop.replace("\r\n","\n").encode()).hexdigest(),
                        canon_cubierto=cubierto)
    with open(EV + f"/bloque_propuesto_{tag}_2026-09-25.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(prop)
    print(f"[{tag}] vivo {w_v} → prop {w_p} | ahorro {w_v-w_p} | canon cubierto: {cubierto}")

json.dump(resumen, open(EV + "/dedupe_a229_a203_a188_s17.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("guardado evidencia/dedupe_a229_a203_a188_s17.json")
