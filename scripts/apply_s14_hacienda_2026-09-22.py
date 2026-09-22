#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Presidencia — ejecución ronda 3 del Consejo de Ministros 2026-09-22 (sesión 14/30).
HACIENDA — aplica [daundecima] y [davigesima] sobre la LGT con .bak, sha256 antes/después
y manifiesto por bloque. Los textos son BYTE A BYTE los ficheros preparados y hasheados
por el ministerio en evidencia/ (criterio: lo que se vota es lo que se aplica).
"""
import hashlib, json, os, shutil

FECHA = "2026-09-22"
LAW = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
EVID = "ministerios/hacienda/evidencia"

BLOQUES = [
    dict(clave="daundecima", a=7893, b=7921,
         prop=EVID + "/bloque_propuesto_da11_2026-09-22.txt",
         sha_lf="6a3ffce967bdb210bbc635f113192ccc30bf9f9be6254c76f9a71c0f368d84fb",
         declarado="328 -> 616 palabras (+288; fidelidad, ahorro 0)",
         ancla="Disposición adicional undécima. Reclamaciones económico-administrativas en otras materias."),
    dict(clave="davigesima", a=8013, b=8029,
         prop=EVID + "/bloque_propuesto_da20_2026-09-22.txt",
         sha_lf="91020a16118985077b08ca8a78476fe98f3ac8c1f2d85e65c362ccbc7f6bc08e",
         declarado="372 -> 647 palabras (+275; fidelidad, ahorro 0)",
         ancla="Disposición adicional vigésima."),
]

def sha(b):
    return hashlib.sha256(b).hexdigest()

# Se aplica de ABAJO hacia ARRIBA: al insertar líneas arriba cambian los offsets de los
# bloques posteriores; procesar en orden descendente evita desplazar rangos pendientes.
BLOQUES = sorted(BLOQUES, key=lambda b: b["a"], reverse=True)

raw = open(LAW, "rb").read()
assert b"\r\n" in raw, "se esperaba CRLF"
antes = sha(raw)
shutil.copy2(LAW, LAW + ".bak-" + FECHA)
texto = raw.decode("utf-8")
assert texto.count("\n") == texto.count("\r\n"), "saltos mixtos"
lineas = texto.split("\r\n")

detalle = []
for blq in BLOQUES:
    viejo = "\n".join(lineas[blq["a"] - 1:blq["b"]])
    nuevo = open(blq["prop"], "rb").read().decode("utf-8").replace("\r\n", "\n")
    if sha(nuevo.encode()) != blq["sha_lf"]:
        raise SystemExit("HASH DEL TEXTO PROPUESTO NO COINCIDE en " + blq["clave"])
    nuevo = nuevo.rstrip("\n")
    if nuevo in texto.replace("\r\n", "\n"):
        raise SystemExit("YA APLICADO (no se re-aplica): " + blq["clave"])
    if texto.count(blq["ancla"]) < 1:
        raise SystemExit("ANCLA AUSENTE: " + blq["clave"])
    lineas[blq["a"] - 1:blq["b"]] = nuevo.split("\n")
    detalle.append(dict(clave=blq["clave"], lineas=f'{blq["a"]}-{blq["b"]}',
                        palabras_antes=len(viejo.split()), palabras_despues=len(nuevo.split()),
                        sha256_bloque_antes=sha(viejo.encode()), sha256_bloque_despues=sha(nuevo.encode()),
                        declarado_por_el_ministerio=blq["declarado"]))

salida = "\r\n".join(lineas)
open(LAW, "wb").write(salida.encode("utf-8"))
despues = sha(open(LAW, "rb").read())

lf = salida.replace("\r\n", "\n")
for blq in BLOQUES:
    nuevo_txt = open(blq["prop"], "rb").read().decode("utf-8").replace("\r\n", "\n").rstrip("\n")
    copias = lf.count(nuevo_txt)
    rotulos = lf.count("## [" + blq["clave"] + "]")
    if copias != 1 or rotulos != 1:
        raise SystemExit(f"VERIFICACION FALLIDA {blq['clave']}: copias={copias} rotulos={rotulos}")

man = dict(fecha=FECHA, sesion="14/30", ejecutor="Presidencia (ronda 3 del Consejo)",
           ley=LAW, sha256_fichero_antes=antes, sha256_fichero_despues=despues,
           backup=LAW + ".bak-" + FECHA, bloques=detalle, verificacion="1 copia por bloque, 1 rótulo por bloque")
os.makedirs(EVID, exist_ok=True)
open(f"{EVID}/manifiesto_consejo_s14_{FECHA}.json", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=2))
with open(f"{EVID}/SHA256SUMS_{FECHA}.txt", "w", encoding="utf-8") as fh:
    fh.write(f"{antes}  {LAW} (antes)\n{despues}  {LAW} (después)\n")
    fh.write(f"{sha(open(LAW + '.bak-' + FECHA, 'rb').read())}  {LAW}.bak-{FECHA}\n")

print("LGT", antes[:16], "->", despues[:16])
for d in detalle:
    print(f"  [{d['clave']}] {d['palabras_antes']} -> {d['palabras_despues']} pal. ({d['declarado_por_el_ministerio']}) OK 1 copia / 1 rótulo")
print("manifiesto:", f"{EVID}/manifiesto_consejo_s14_{FECHA}.json")
