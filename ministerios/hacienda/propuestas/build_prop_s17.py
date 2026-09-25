# Construcción de bloques propuestos (dedupe conservando ÚLTIMA copia = vigente) + validación canon ⊆ propuesto (s17)
import json, re, hashlib

ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}

def norm(s):
    s = s.replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

def bloque_raw(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0).rstrip("\n")

EV = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

def sha_bloque(texto):
    # convención única del Auditor: sha256 del bloque completo con cabecera, LF, sin saltos finales
    return hashlib.sha256(texto.replace("\r\n", "\n").encode("utf-8")).hexdigest()

def canon_frases(txt):
    txt = re.sub(r"\s+", " ", txt.replace("\u00a0", " ")).strip()
    partes = re.split(r"(?<=[.;:])\s+(?=[A-ZÁÉÍÓÚÑ«(a-zà-ö])", txt)
    return [p.strip() for p in partes if len(p.split()) >= 8]

for tag in ("a229", "a203", "a188"):
    b = bloque_raw(tag)
    lines = b.split("\n")
    header = lines[0]                      # "## [tag] Artículo NNN"
    # separamos cuerpo normativo de notas al pie (linas >) y título
    body = [l for l in lines[1:] if l.strip() and not l.strip().startswith(">")]
    pies = [l for l in lines[1:] if l.strip().startswith(">")]
    # dedupe conservando ÚLTIMA aparición: para ello invertimos, dedup, revertimos
    rev, out, seen = body[::-1], [], set()
    for l in rev:
        k = norm(l)
        if k in seen and l.strip():
            continue
        seen.add(k)
        out.append(l)
    ded = out[::-1]
    # título: eliminar líneas "Artículo NNN." duplicadas/obsoletas → dejar solo el del canon
    titulo_ok = arts[tag]["titulo"].strip()
    ded = [l for l in ded if not re.match(r"^Artículo \d+\.", l.strip())]
    prop = header + "\n\n" + titulo_ok + "\n\n" + "\n".join(ded).strip() + "\n\n" + "\n".join(pies)
    prop = prop.rstrip("\n")

    vivo_w, prop_w = len(b.split()), len(prop.split())
    nf = set(norm(x) for x in re.split(r"\n+", prop))
    faltan = [f[:90] for f in canon_frases(arts[tag]["texto"]) if norm(f) not in nf and not any(norm(f) in x for x in nf)]
    print("=" * 70)
    print(f"[{tag}] vivo {vivo_w} pal → propuesto {prop_w} pal | AHORRO {vivo_w - prop_w} | pies: {len(pies)}")
    print(f"   canon frases no cubiertas por propuesto: {len(faltan)}")
    for f in faltan[:4]:
        print("     ·", f)
    with open(EV + f"/bloque_propuesto_{tag}_2026-09-25.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(prop)
    with open(EV + f"/bloque_vivo_{tag}_2026-09-25.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(b)
    print(f"   sha vivo     : {sha_bloque(b)[:8]}")
    print(f"   sha propuesto: {sha_bloque(prop)[:8]}")
