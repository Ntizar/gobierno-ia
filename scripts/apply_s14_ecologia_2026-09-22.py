#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Presidencia — ejecución ronda 3 del Consejo 2026-09-22 (sesión 14/30).
ECOLOGÍA — aplica [a1-4] (art. 12 L7, reescritura completa), [a1-11] (art. 19.2 L7) y
[a4] (art. 4.2 L7, condición RESUELTA por escrito por la ministra hoy: anclaje en el
Consejo Nacional del Clima, RD 415/2014, sin duplicar el informe del 4.2).
Textos extraídos literalmente de los blockquotes de la propuesta del ministerio.
NO se aplica [a14] (la ministra arrastra la corrección de objeto a la sesión 18) ni [da-2]
(espera la cifra de participaciones fósiles) ni [a1-7] (bloqueada sin cifra IGAE).
"""
import hashlib, json, os, shutil

FECHA = "2026-09-22"
LAW = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
PROP = "ministerios/transicion-ecologica/propuestas/2026-09-22.md"
EVID = "ministerios/transicion-ecologica/evidencia"

def sha(b):
    return hashlib.sha256(b).hexdigest()

pl = open(PROP, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")

def cita(prefijo):
    """devuelve el texto de un blockquote de una sola línea que empieza por el prefijo dado"""
    hits = [l[2:] for l in pl if l.startswith("> ") and l[2:].startswith(prefijo)]
    if len(hits) != 1:
        raise SystemExit(f"cita ambigua ({len(hits)}) para: {prefijo[:40]}")
    return hits[0]

def cita_bloque(marca):
    """devuelve el texto completo (párrafos) del blockquote que sigue a la marca dada"""
    i = pl.index(marca)
    j = i + 1
    out = []
    while j < len(pl) and (pl[j].startswith(">") or (pl[j] == "" and j + 1 < len(pl) and pl[j + 1].startswith(">"))):
        out.append(pl[j])
        j += 1
    while out and out[-1] == "":
        out.pop()
    txt = "\n".join(l[2:] if l.startswith("> ") else ("" if l == ">" else l) for l in out)
    return txt

art12 = cita_bloque("**Texto propuesto (282 palabras, medido)**:")
art19_2 = cita("2. La planificación y la gestión hidrológicas deberán adecuarse a las directrices y medidas que se desarrollen en la Estrategia del Agua para la Transición Ecológica, sin perjuicio de las competencias que correspondan a las Comunidades Autónomas. Dicha Estrategia,")
art4_2 = cita("2. Los informes de progreso sobre el Plan Nacional Integrado de Energía y Clima, elaborados por el Ministerio para la Transición Ecológica")

BLOQUES = [
    dict(clave="a1-4", rango=(336, 345), nuevo=art12,
         declarado="196 -> 282 palabras (+86): fecha 31/12/2026, responsable DG Energía, informe anual"),
    dict(clave="a4", rango=(242, 242), nuevo=art4_2,
         declarado="4.2: 47 -> 62 palabras (+15): periodicidad + Consejo Nacional del Clima + Cortes antes del 30/06 (condición resuelta)"),
    dict(clave="a1-11", rango=(500, 500), nuevo=art19_2,
         declarado="19.2: 72 -> 91 palabras (+19): revisión cuatrienal + Conferencia Sectorial + Cortes"),
]

# Descendente: al insertar líneas arriba se desplazan los rangos posteriores.
BLOQUES = sorted(BLOQUES, key=lambda b: b["rango"][0], reverse=True)

raw = open(LAW, "rb").read()
assert b"\r\n" in raw
antes = sha(raw)
shutil.copy2(LAW, LAW + ".bak-" + FECHA)
texto = raw.decode("utf-8")
lineas = texto.split("\r\n")
lf = texto.replace("\r\n", "\n")

detalle = []
for blq in BLOQUES:
    a, b = blq["rango"]
    viejo = "\n".join(lineas[a - 1:b])
    nuevo = blq["nuevo"].rstrip("\n")
    print(f"--- [{blq['clave']}] propuesto ({len(nuevo.split())} pal.): {nuevo[:110]}...")
    if nuevo.strip() in lf:
        raise SystemExit("YA APLICADO (no se re-aplica): " + blq["clave"])
    if ("## [" + blq["clave"] + "]") not in lf:
        raise SystemExit("rótulo ausente: " + blq["clave"])
    lineas[a - 1:b] = nuevo.split("\n")
    detalle.append(dict(clave=blq["clave"], lineas=f"{a}-{b}",
                        palabras_antes=len(viejo.split()), palabras_despues=len(nuevo.split()),
                        sha256_bloque_antes=sha(viejo.encode()), sha256_bloque_despues=sha(nuevo.encode()),
                        declarado_por_el_ministerio=blq["declarado"]))

salida = "\r\n".join(lineas)
# Normalización de formato (sin tocar palabra): el blockquote del art. 12 traía una línea vacía
# de más tras el rótulo; la convención del repo es rótulo + UNA línea en blanco + cuerpo.
salida = salida.replace("## [a1-4] Artículo 12\r\n\r\n\r\n", "## [a1-4] Artículo 12\r\n\r\n")
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
           no_ejecutados=["a14 (corrección de objeto -> sesión 18)", "da-2 (falta cifra de participaciones fósiles)",
                          "a1-7 (bloqueada: sin cifra IGAE del 3 % de reserva hídrica)"])
open(f"{EVID}/manifiesto_consejo_s14_{FECHA}.json", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=2))
with open(f"{EVID}/SHA256SUMS_{FECHA}.txt", "w", encoding="utf-8") as fh:
    fh.write(f"{antes}  {LAW} (antes)\n{despues}  {LAW} (después)\n")

print("L7", antes[:16], "->", despues[:16])
for d in detalle:
    print(f"  [{d['clave']}] {d['palabras_antes']} -> {d['palabras_despues']} pal. · neto {d['palabras_despues']-d['palabras_antes']:+d} ({d['declarado_por_el_ministerio']}) OK 1 copia / 1 rótulo")
print("manifiesto:", f"{EVID}/manifiesto_consejo_s14_{FECHA}.json")
