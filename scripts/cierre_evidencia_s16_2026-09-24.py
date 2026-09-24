#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cierra la evidencia de la sesion 16: manifiesto de Ecologia (el script principal
uso la clave 'ecologia' y la carpeta real es 'transicion-ecologica') + SHA256SUMS.
Mide de nuevo sobre disco, no copia cifras de memoria."""
import hashlib, json, os, re

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"
FECHA = "2026-09-24"
BLOQUES = {"transicion-ecologica": ("ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
                                    ["df-11", "da-7"])}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def rangos(ls):
    idx = [i for i, l in enumerate(ls) if l.startswith("## [")]
    out = {}
    for n, i in enumerate(idx):
        r = re.match(r"## \[([^\]]+)\]", ls[i]).group(1)
        out[r] = (i, idx[n + 1] if n + 1 < len(idx) else len(ls))
    return out

for minis, (ley, ids) in BLOQUES.items():
    hoy = open(os.path.join(REPO, ley), "rb").read()
    bak = open(os.path.join(REPO, ley + ".bak-" + FECHA), "rb").read()
    t_hoy = hoy.decode("utf-8").replace("\r\n", "\n").split("\n")
    t_bak = bak.decode("utf-8").replace("\r\n", "\n").split("\n")
    r_hoy, r_bak = rangos(t_hoy), rangos(t_bak)
    detalle = []
    for rid in ids:
        a, b = r_hoy[rid]
        a0, b0 = r_bak[rid]
        nuevo = "\n".join(t_hoy[a:b]).rstrip("\n")
        viejo = "\n".join(t_bak[a0:b0]).rstrip("\n")
        detalle.append({
            "bloque": rid, "ministerio": minis, "tipo": "bloque (restauracion canon)",
            "referencia": "ministerios/transicion-ecologica/evidencia/bloque_propuesto_%s_2026-09-24.txt" % rid,
            "lineas_antes": [a0 + 1, b0], "lineas_despues": [a + 1, b],
            "palabras_antes": len(viejo.split()), "palabras_despues": len(nuevo.split()),
            "sha256_bloque_antes": sha(viejo.encode()),
            "sha256_bloque_despues": sha(nuevo.encode()),
            "copias_rotulo_antes": sum(1 for l in t_bak if l.startswith("## [%s]" % rid)),
            "copias_rotulo_despues": sum(1 for l in t_hoy if l.startswith("## [%s]" % rid))})
        print(rid, detalle[-1]["palabras_antes"], "->", detalle[-1]["palabras_despues"],
              "copias:", detalle[-1]["copias_rotulo_despues"])
    payload = {"sesion": "16/30", "fecha": FECHA, "ejecutor": "Presidencia",
               "backup": ".bak-" + FECHA, "nota": ("manifiesto regenerado por Presidencia: el script "
                        "aplicar_s16 uso la clave 'ecologia' y la carpeta real es 'transicion-ecologica'"),
               "leyes": {ley: {"sha256_antes": sha(bak), "sha256_despues": sha(hoy),
                               "lineas_antes": len(t_bak), "lineas_despues": len(t_hoy),
                               "bloques_antes": sum(1 for l in t_bak if l.startswith("## [")),
                               "bloques_despues": sum(1 for l in t_hoy if l.startswith("## [")),
                               "detalle": detalle}}}
    p = os.path.join(REPO, "ministerios", minis, "evidencia", "manifiesto_consejo_s16_%s.json" % FECHA)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print("manifiesto ->", p)

# SHA256SUMS por ministerio con los ficheros de ley + manifiestos del dia
for minis in ("hacienda", "sanidad", "transicion-ecologica"):
    base = os.path.join(REPO, "ministerios", minis)
    ley = [os.path.join("leyes", f) for f in os.listdir(os.path.join(base, "leyes"))
           if f.endswith(".md")]
    ev = [os.path.join("evidencia", f) for f in os.listdir(os.path.join(base, "evidencia"))
          if FECHA in f]
    out = []
    for rel in sorted(ley + ev):
        out.append("%s  %s" % (sha(open(os.path.join(base, rel), "rb").read()), rel))
    p = os.path.join(base, "evidencia", "SHA256SUMS_%s.txt" % FECHA)
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("SHA256SUMS ->", p, "(%d entradas)" % len(out))
