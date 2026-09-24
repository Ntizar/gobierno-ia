#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ejecucion ronda 3 - Consejo sesion 16/30 (2026-09-24). Presidencia.
Aplica sobre los ficheros de ley los acuerdos APROBADOS:
  LGT 61fc9fc9: [dfquinta] [dfsexta] [dfoctava]  (restauracion canon BOE)
  LGS 9e9b0921: [adieciseis].4 (organo fantasma) [atreintayseis].3 (plazo 5 anos)
  L7  932e9391: [df-11] [da-7]
Uso: python aplicar_s16_2026-09-24.py [--apply]
"""
import hashlib, json, os, re, shutil, sys, datetime

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"
FECHA = "2026-09-24"
APPLY = "--apply" in sys.argv

def sha(b):
    return hashlib.sha256(b).hexdigest()

# ---- definicion de los trabajos -------------------------------------------------
TRABAJOS = [
    # (ministerio, ley, id_bloque, tipo, payload)
    ("hacienda", "ministerios/hacienda/leyes/BOE-A-2003-23186.md", "dfquinta", "bloque",
     "ministerios/hacienda/evidencia/bloque_propuesto_dfquinta_2026-09-24.txt"),
    ("hacienda", "ministerios/hacienda/leyes/BOE-A-2003-23186.md", "dfsexta", "bloque",
     "ministerios/hacienda/evidencia/bloque_propuesto_dfsexta_2026-09-24.txt"),
    ("hacienda", "ministerios/hacienda/leyes/BOE-A-2003-23186.md", "dfoctava", "bloque",
     "ministerios/hacienda/evidencia/bloque_propuesto_dfoctava_2026-09-24.txt"),
    ("sanidad", "ministerios/sanidad/leyes/BOE-A-1986-10499.md", "adieciseis", "cadena",
     ("Dirección General de Cartilla SNS",
      "Dirección General de Cartera Común de Servicios del SNS y Farmacia")),
    ("sanidad", "ministerios/sanidad/leyes/BOE-A-1986-10499.md", "atreintayseis", "cadena",
     ("3. Las cuantías señaladas anteriormente deberán ser revisadas y actualizadas periódicamente "
      "por el Gobierno, por Real Decreto, teniendo en cuenta la variación de los índices de precios "
      "para el consumo.",
      "3. El Gobierno revisará y actualizará las cuantías señaladas en el apartado anterior, por Real "
      "Decreto y con una periodicidad máxima de cinco años, en función de la variación del índice de "
      "precios de consumo. El primer plazo vencerá a los cinco años de la entrada en vigor de esta "
      "redacción.")),
    ("ecologia", "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md", "df-11", "bloque",
     "ministerios/transicion-ecologica/evidencia/bloque_propuesto_df-11_2026-09-24.txt"),
    ("ecologia", "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md", "da-7", "bloque",
     "ministerios/transicion-ecologica/evidencia/bloque_propuesto_da-7_2026-09-24.txt"),
]

def leer(p):
    return open(os.path.join(REPO, p), "rb").read().decode("utf-8")

def rangos(lineas):
    idx = [(i, l) for i, l in enumerate(lineas) if l.startswith("## [")]
    out = {}
    for n, (i, l) in enumerate(idx):
        rid = re.match(r"## \[([^\]]+)\]", l).group(1)
        out[rid] = (i, idx[n + 1][0] if n + 1 < len(idx) else len(lineas))
    return out

manifiestos = {}
leyes = sorted({t[1] for t in TRABAJOS})
for ley in leyes:
    raw = open(os.path.join(REPO, ley), "rb").read()
    h0 = sha(raw)
    txt = raw.decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"
    lineas = txt.split(nl)
    n_bloques_antes = sum(1 for l in lineas if l.startswith("## ["))
    print("\n=== %s  sha256 ANTES=%s  lineas=%d  bloques=%d" % (ley, h0, len(lineas), n_bloques_antes))
    if APPLY:
        shutil.copy2(os.path.join(REPO, ley), os.path.join(REPO, ley + ".bak-" + FECHA))
    detalle = []
    # aplicar en orden descendente de linea para no descolocar indices
    trabajos_ley = [t for t in TRABAJOS if t[1] == ley]
    plan = []
    for minis, _ley, rid, tipo, payload in trabajos_ley:
        r = rangos(lineas)
        if rid not in r:
            raise SystemExit("ERROR: bloque %s no encontrado en %s" % (rid, ley))
        a, b = r[rid]
        vivo = "\n".join(lineas[a:b]).rstrip("\n")
        if tipo == "bloque":
            prop_txt = leer(payload).replace("\r\n", "\n").strip("\n")
            if "## [" in prop_txt.split("\n", 1)[1]:
                raise SystemExit("ERROR: el texto propuesto de %s contiene otro rotulo ## [" % rid)
            nuevas = prop_txt.split("\n")
            plan.append((a, b, rid, minis, tipo, vivo, "\n".join(nuevas), payload))
        else:
            viejo_t, nuevo_t = payload
            if vivo.count(viejo_t) != 1 or vivo.count(nuevo_t) != 0:
                raise SystemExit("ERROR %s: coincidencias viejo=%d nuevo=%d"
                                 % (rid, vivo.count(viejo_t), vivo.count(nuevo_t)))
            nuevo_bloque = vivo.replace(viejo_t, nuevo_t)
            plan.append((a, b, rid, minis, tipo, vivo, nuevo_bloque, "cadena literal"))
    plan.sort(key=lambda x: -x[0])
    for a, b, rid, minis, tipo, vivo, nuevo, ref in plan:
        print("  [%s] %s  l.%d-%d  %d -> %d palabras  sha vivo=%s  sha nuevo=%s  (%s)"
              % (minis, rid, a + 1, b, len(vivo.split()), len(nuevo.split()),
                 sha(vivo.encode())[:12], sha(nuevo.rstrip("\n").encode())[:12], ref))
        detalle.append({"bloque": rid, "ministerio": minis, "tipo": tipo, "referencia": ref,
                        "lineas_antes": [a + 1, b], "palabras_antes": len(vivo.split()),
                        "palabras_despues": len(nuevo.split()),
                        "sha256_bloque_antes": sha(vivo.encode()),
                        "sha256_bloque_despues": sha(nuevo.rstrip("\n").encode()),
                        "copias_rotulo_antes": sum(1 for l in lineas if l.startswith("## [%s]" % rid)),
                        })
        if APPLY:
            lineas[a:b] = nuevo.split("\n")
    if APPLY:
        out = nl.join(lineas)
        with open(os.path.join(REPO, ley), "w", newline="", encoding="utf-8") as f:
            f.write(out)
        raw2 = open(os.path.join(REPO, ley), "rb").read()
        h1 = sha(raw2)
        lineas2 = raw2.decode("utf-8").split(nl)
        n_bloques_desp = sum(1 for l in lineas2 if l.startswith("## ["))
        # verificacion: una sola copia de cada rotulo aplicado
        for d in detalle:
            d["copias_rotulo_despues"] = sum(1 for l in lineas2 if l.startswith("## [%s]" % d["bloque"]))
            assert d["copias_rotulo_despues"] == 1, "rotulo duplicado " + d["bloque"]
        print("  --> sha256 DESPUES=%s  lineas=%d  bloques=%d" % (h1, len(lineas2), n_bloques_desp))
        manifiestos.setdefault(minis, {})
        manifiestos[minis].setdefault(ley, {})["sha256_antes"] = h0
        manifiestos[minis][ley]["sha256_despues"] = h1
        manifiestos[minis][ley]["lineas_antes"] = len(lineas)
        manifiestos[minis][ley]["lineas_despues"] = len(lineas2)
        manifiestos[minis][ley]["bloques_antes"] = n_bloques_antes
        manifiestos[minis][ley]["bloques_despues"] = n_bloques_desp
        manifiestos[minis][ley]["detalle"] = detalle
        assert n_bloques_antes == n_bloques_desp, "cambio el numero de bloques"

if APPLY:
    for minis, data in manifiestos.items():
        p = os.path.join(REPO, "ministerios", minis, "evidencia",
                         "manifiesto_consejo_s16_%s.json" % FECHA)
        payload = {"sesion": "16/30", "fecha": FECHA, "ejecutor": "Presidencia",
                   "backup": ".bak-" + FECHA, "leyes": data}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print("manifiesto ->", p)
    print("\nAPLICADO. Manifiestos escritos.")
else:
    print("\nDRY-RUN (sin --apply). Nada modificado.")
