# -*- coding: utf-8 -*-
# Metodo EXACTO de build_prop3_s17.py (aprobado y ejecutado el 25-09 en a203/a188):
# dedupe conservando la ULTIMA copia de cada linea + titulo canon + canon ⊆ propuesto.
# Candidatos de hoy: a81, a68, a65, a112.
import json, re, hashlib
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
EV = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ").replace("\u202f", " ")).strip().lower()

def bloque_raw(tag):
    return re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M).group(0).rstrip("\n")

def sha(t):
    return hashlib.sha256(t.replace("\r\n", "\n").encode("utf-8")).hexdigest()

resumen = {}
for tag in ("a81", "a68", "a65", "a112"):
    b = bloque_raw(tag)
    lines = b.split("\n")
    header, body = lines[0], [l for l in lines[1:] if l.strip()]
    rev, out = body[::-1], []
    seen = set()
    for l in rev:
        k = norm(l)
        if k not in seen:
            seen.add(k)
            out.append(l)
    out = out[::-1]
    titulo = arts[tag]["titulo"].strip()
    out = [l for l in out if not re.match(r"^Artículo \d+\.", l.strip())]
    prop = (header + "\n\n" + titulo + "\n\n" + "\n".join(out)).rstrip()
    np_ = norm(prop)
    ct = norm(arts[tag]["texto"])
    ok = ct in np_
    w_v, w_p = len(b.split()), len(prop.split())
    open(EV + f"/bloque_propuesto_{tag}_2026-09-27.txt", "w", encoding="utf-8", newline="\n").write(prop)
    open(EV + f"/bloque_vivo_{tag}_2026-09-27.txt", "w", encoding="utf-8", newline="\n").write(b)
    resumen[tag] = dict(vivo_pal=w_v, propuesto_pal=w_p, ahorro_pal=w_v - w_p,
                        canon_integro_en_propuesto=ok,
                        sha256_bloque_vivo=sha(b), sha256_bloque_propuesto=sha(prop))
    print(f"[{tag}] {w_v} -> {w_p} | ahorro {w_v - w_p} | canon ⊆ propuesto: {ok}")
json.dump(resumen, open(EV + "/dedupe_a81_a68_a65_a112_s18_2026-09-27.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK evidencia/dedupe_a81_a68_a65_a112_s18_2026-09-27.json")
