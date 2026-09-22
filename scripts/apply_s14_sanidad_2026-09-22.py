#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Presidencia — ejecución ronda 3 del Consejo 2026-09-22 (sesión 14/30).
SANIDAD — aplica [aveintiuno] (art. 21 LGS) y [acientodos] (art. 102 LGS).
Textos extraídos LITERALMENTE del fichero de propuestas del ministerio (bloques ```markdown).
Única normalización: se quita el prefijo '### ' del encabezado del primer renglón, porque el
rótulo del bloque ya es '## [aclave] Artículo N' y el título debe vivir en el cuerpo (convención
de rótulo aprobada en la sesión 13). No se cambia ni una palabra.
"""
import hashlib, json, os, shutil, re

FECHA = "2026-09-22"
LAW = "ministerios/sanidad/leyes/BOE-A-1986-10499.md"
PROP = "ministerios/sanidad/propuestas/2026-09-22.md"
EVID = "ministerios/sanidad/evidencia"

def sha(b):
    return hashlib.sha256(b).hexdigest()

prop_txt = open(PROP, "rb").read().decode("utf-8").replace("\r\n", "\n")
bloques_codigo = re.findall(r"```markdown\n(.*?)```", prop_txt, re.S)
print("bloques ```markdown encontrados:", len(bloques_codigo))
if len(bloques_codigo) != 2:
    raise SystemExit("se esperaban 2 bloques de código en la propuesta de Sanidad")

def limpia(t):
    ls = t.rstrip("\n").split("\n")
    if ls[0].startswith("### "):
        ls[0] = ls[0][4:]
    return "\n".join(ls)

BLOQUES = [
    dict(clave="aveintiuno", a=303, b=347, nuevo=limpia(bloques_codigo[0]),
         declarado="2 pasadas completas -> 1 (-289 palabras medidas por dedup_scan.py)",
         ancla="Artículo veintiuno. Salud laboral."),
    dict(clave="acientodos", a=1376, b=1398, nuevo=limpia(bloques_codigo[1]),
         declarado="4 capas del ap. 1 -> 1 (-122 palabras)",
         ancla="Artículo ciento dos. Información y promoción de medicamentos y productos"),
]
# NOTA de rango: se sustituye SOLO el cuerpo (el rótulo '## [aclave] Artículo N' de cada bloque
# NO se toca ni se duplica — convención de rótulo de la sesión 13). En [aveintiuno] se conserva
# además el marcador ' (Derogado)' huérfano (líneas 349-350): está denunciado como errata y su
# borrado queda pendiente de cita BOE, así que no se toca esta noche.

# Descendente: al insertar líneas arriba se desplazan los rangos posteriores.
BLOQUES = sorted(BLOQUES, key=lambda b: b["a"], reverse=True)

raw = open(LAW, "rb").read()
assert b"\r\n" in raw
antes = sha(raw)
shutil.copy2(LAW, LAW + ".bak-" + FECHA)
texto = raw.decode("utf-8")
lineas = texto.split("\r\n")
lf = texto.replace("\r\n", "\n")

detalle = []
for blq in BLOQUES:
    viejo = "\n".join(lineas[blq["a"] - 1:blq["b"]])
    nuevo = blq["nuevo"]
    if nuevo.strip() in lf:
        raise SystemExit("YA APLICADO (no se re-aplica): " + blq["clave"])
    if blq["ancla"] not in nuevo:
        raise SystemExit("el texto propuesto no contiene el ancla esperada: " + blq["clave"])
    if ("## [" + blq["clave"] + "]") not in lf:
        raise SystemExit("rótulo ausente: " + blq["clave"])
    lineas[blq["a"] - 1:blq["b"]] = nuevo.split("\n")
    detalle.append(dict(clave=blq["clave"], lineas=f'{blq["a"]}-{blq["b"]}',
                        palabras_antes=len(viejo.split()), palabras_despues=len(nuevo.split()),
                        sha256_bloque_antes=sha(viejo.encode()), sha256_bloque_despues=sha(nuevo.encode()),
                        declarado_por_el_ministerio=blq["declarado"]))

salida = "\r\n".join(lineas)
open(LAW, "wb").write(salida.encode("utf-8"))
despues = sha(open(LAW, "rb").read())
lf2 = salida.replace("\r\n", "\n")
for blq in BLOQUES:
    copias = lf2.count(blq["nuevo"].strip())
    rotulos = lf2.count("## [" + blq["clave"] + "]")
    if copias != 1 or rotulos != 1:
        raise SystemExit(f"VERIFICACION FALLIDA {blq['clave']}: copias={copias} rotulos={rotulos}")

man = dict(fecha=FECHA, sesion="14/30", ejecutor="Presidencia (ronda 3 del Consejo)", ley=LAW,
           sha256_fichero_antes=antes, sha256_fichero_despues=despues, backup=LAW + ".bak-" + FECHA,
           bloques=detalle, verificacion="1 copia por bloque, 1 rótulo por bloque",
           nota="texto del ministerio extraído literal del bloque ```markdown de la propuesta; sólo se retiró el prefijo '### ' del encabezado")
open(f"{EVID}/manifiesto_consejo_s14_{FECHA}.json", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=2))
with open(f"{EVID}/SHA256SUMS_{FECHA}.txt", "w", encoding="utf-8") as fh:
    fh.write(f"{antes}  {LAW} (antes)\n{despues}  {LAW} (después)\n")

print("LGS", antes[:16], "->", despues[:16])
for d in detalle:
    print(f"  [{d['clave']}] {d['palabras_antes']} -> {d['palabras_despues']} pal. · neto {d['palabras_despues']-d['palabras_antes']:+d} ({d['declarado_por_el_ministerio']}) OK 1 copia / 1 rótulo")
print("manifiesto:", f"{EVID}/manifiesto_consejo_s14_{FECHA}.json")
