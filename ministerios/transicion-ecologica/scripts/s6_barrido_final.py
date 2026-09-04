# S6 — barrido final de duplicacion hash SHA-256 por bloque sobre la ley ya ejecutada (ac.30)
# Denominador historico: 71 bloques por cabecera '## [' (contado sesion 5).
import hashlib, json, re, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "ministerios/transicion-ecologica"
raw = open(f"{BASE}/leyes/BOE-A-2021-8447.md", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
# trocear por cabecera '## ['
idxs = [i for i, l in enumerate(lines) if l.startswith("## [")]
bloques = []
for n, i in enumerate(idxs):
    j = idxs[n+1] if n + 1 < len(idxs) else len(lines)
    name = lines[i].strip()
    body = [l.strip() for l in lines[i+1:j] if l.strip()]
    bloques.append((name, body))
tot_palabras = len(re.findall(r"\S+", raw))
dup_exactos = []
difusos = 0
def h(p): return hashlib.sha256(p.encode()).hexdigest()
for name, body in bloques:
    seen = {}
    for p in body:
        hh = h(p)
        if hh in seen:
            dup_exactos.append((name, len(p.split()), p[:60]))
        seen.setdefault(hh, p)
    # difuso: parrafos que empiezan igual >=250 chars
    for a in range(len(body)):
        for b in range(a+1, len(body)):
            if body[a][:250] == body[b][:250] and body[a] != body[b] and len(body[a]) > 300:
                difusos += 1
# duplicados ENTRE bloques (mismo parrafo en dos bloques distintos)
allp = {}
for name, body in bloques:
    for p in set(body):
        allp.setdefault(h(p), []).append(name)
entre = {k2: v for k2, v in allp.items() if len(v) > 1 and len(set(v)) > 1}
pal_dup = sum(w for _, w, _ in dup_exactos)
print(json.dumps({"bloques": len(bloques), "palabras": tot_palabras,
  "dup_exactos_dentro_bloque": len(dup_exactos), "palabras_dup": pal_dup,
  "dup_difusos": difusos, "dup_entre_bloques": len(entre),
  "tasa_pct": round(100.0*pal_dup/tot_palabras, 2),
  "detalle_dup": [d[1:] for d in dup_exactos],
  "ejemplos_entre": [v for v in list(entre.values())[:5]]}, ensure_ascii=False, indent=1))
