# -*- coding: utf-8 -*-
"""Sesión 21/30 · 2026-09-30.

Marca la cabecera del artefacto del 30-09 que dejó el proceso automático de la
madrugada en `agenda.md`, SIN borrarlo ni alterar su contenido: solo se añade
una etiqueta a su cabecera para que el boletín no lea dos entradas de hoy como
si fueran las dos mías.

Verifica, además, que el cuerpo del artefacto queda byte a byte igual.
"""
import hashlib
import pathlib

P = pathlib.Path(__file__).resolve().parents[1] / "agenda.md"
antes = P.read_bytes()

CAB = "# Agenda — 2026-09-30 — Sanidad"
CUERPO = "\r\n\r\n- **Titular**: «Las CCAA piden"
OLD = (CAB + CUERPO).encode("utf-8")
MARCA = (
    CAB
    + " (ARTEFACTO no verificado — proceso automático de la madrugada; "
    + "**conservado íntegro, no es mi trabajo de hoy** — mi entrada verificada "
    + "va al principio del fichero)"
    + CUERPO
).encode("utf-8")

n = antes.count(OLD)
if n != 1:
    raise SystemExit(f"ABORTADO: cabecera del artefacto encontrada {n} veces (se esperaba 1)")

despues = antes.replace(OLD, NEW := MARCA)

# Integridad: quitando la cabecera (marcada o no), el resto debe ser idéntico.
cuerpo_antes = antes.replace(OLD, b"")
cuerpo_despues = despues.replace(NEW, b"")
if cuerpo_antes != cuerpo_despues:
    raise SystemExit("ABORTADO: el cuerpo del fichero cambiaría; no se escribe nada")

P.write_bytes(despues)

cabeceras_hoy = despues.decode("utf-8").count(CAB)
print("sha256 ANTES  :", hashlib.sha256(antes).hexdigest())
print("sha256 DESPUES:", hashlib.sha256(despues).hexdigest())
print("bytes nuevos  :", len(despues) - len(antes))
print("cabeceras '", CAB, "' en el fichero:", cabeceras_hoy)
print("cuerpo del artefacto intacto (byte a byte):", cuerpo_antes == cuerpo_despues)
