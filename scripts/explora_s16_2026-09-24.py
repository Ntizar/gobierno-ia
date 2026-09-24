#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exploracion Presidencia sesion 16 - 2026-09-24: rangos de bloque y estado de los diffs."""
import hashlib, json, os, re, sys

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"

LEYES = {
    "hacienda":  ("ministerios/hacienda/leyes/BOE-A-2003-23186.md",
                  ["dfquinta", "dfsexta", "dfoctava"]),
    "sanidad":   ("ministerios/sanidad/leyes/BOE-A-1986-10499.md",
                  ["adieciseis", "atreintayseis"]),
    "ecologia":  ("ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
                  ["df-11", "da-7"]),
}

EVID = {
    "hacienda": "ministerios/hacienda/evidencia",
    "sanidad": "ministerios/sanidad/evidencia",
    "ecologia": "ministerios/transicion-ecologica/evidencia",
}

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def bloques(lineas):
    """Devuelve dict rid -> (inicio, fin_exclusivo) 1-indexado."""
    idx = [(i, l) for i, l in enumerate(lineas) if l.startswith("## [")]
    out = {}
    for n, (i, l) in enumerate(idx):
        rid = re.match(r"## \[([^\]]+)\]", l).group(1)
        fin = idx[n + 1][0] if n + 1 < len(idx) else len(lineas)
        out[rid] = (i + 1, fin)
    return out

res = {}
for minis, (rel, ids) in LEYES.items():
    p = os.path.join(REPO, rel)
    raw = open(p, "rb").read()
    txt = raw.decode("utf-8")
    crlf = txt.count("\r\n")
    lineas = txt.replace("\r\n", "\n").split("\n")
    bl = bloques(lineas)
    res[minis] = {"fichero": rel, "sha256_fichero": sha_bytes(raw),
                  "lineas": len(lineas), "crlf": crlf, "n_bloques": len(bl), "detalle": {}}
    for rid in ids:
        if rid not in bl:
            res[minis]["detalle"][rid] = {"ERROR": "bloque no encontrado"}
            continue
        a, b = bl[rid]
        print("### %s / %s -> lineas %d-%d" % (minis, rid, a, b))
        vivo = "\n".join(lineas[a - 1:b])
        vivo_z = vivo.rstrip("\n")
        d = {"lineas": [a, b], "n_lineas": b - a + 1,
             "palabras": len(vivo_z.split()),
             "sha256_bloque": sha_bytes(vivo_z.encode("utf-8"))}
        # comparar con evidencia vivo declarada
        ev = os.path.join(REPO, EVID[minis], "bloque_vivo_%s_2026-09-24.txt" % rid)
        if os.path.exists(ev):
            evb = open(ev, "rb").read().decode("utf-8")
            d["ev_vivo_sha"] = sha_bytes(evb.encode("utf-8"))
            d["ev_vivo_coincide"] = (evb.rstrip("\n") == vivo_z)
        evp = os.path.join(REPO, EVID[minis], "bloque_propuesto_%s_2026-09-24.txt" % rid)
        if os.path.exists(evp):
            pvb = open(evp, "rb").read().decode("utf-8")
            d["ev_prop_sha"] = sha_bytes(pvb.rstrip("\n").encode("utf-8"))
            d["ev_prop_palabras"] = len(pvb.rstrip("\n").split())
            d["prop_cabecera"] = pvb.split("\n")[0][:60]
            d["prop_ultima"] = pvb.rstrip("\n").split("\n")[-1][:60]
        else:
            d["ev_prop"] = "NO EXISTE"
        res[minis]["detalle"][rid] = d
        print(json.dumps(d, ensure_ascii=False, indent=1))
        print("--- cola del bloque vivo:")
        print("\n".join(lineas[max(a - 1, b - 6):b]))

with open(os.path.join(REPO, "consejo/evidencia/exploracion_s16_2026-09-24.json"), "w",
          encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("\nRESUMEN:", json.dumps({k: {"sha256": v["sha256_fichero"][:12], "bloques": v["n_bloques"],
      "lineas": v["lineas"], "crlf": v["crlf"]} for k, v in res.items()}, ensure_ascii=False))
