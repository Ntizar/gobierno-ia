#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correccion de Presidencia (21-09, sesion 13/30).

La propuesta aprobada del art. 2 L7 (sesion 9) se contradice a si misma:
su 'Texto propuesto' pega los principios sin linea en blanco, pero su
'Justificacion' dice «un principio por linea, separados por linea en blanco
simple». Se aplica la justificacion (que es el acuerdo: unificar el espaciado
irregular) y se deja UN salto de linea entre principios consecutivos.

Idempotente: si ya hay linea en blanco entre principios, no hace nada.
"""
import re, io, sys

P = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
PRINCIPIO = re.compile(r"^[a-zñ]\)\s")


def main():
    with io.open(P, encoding="utf-8", newline="") as f:
        txt = f.read()
    nl = "\r\n" if "\r\n" in txt else "\n"

    m = re.search(r"^## \[a2\][^\r\n]*\r?\n", txt, re.M)
    if not m:
        raise SystemExit("bloque [a2] no encontrado")
    ini = m.end()
    sig = re.search(r"^## \[", txt[ini:], re.M)
    fin = ini + sig.start() if sig else len(txt)
    bloque = txt[ini:fin]

    lineas = bloque.split(nl)
    salida = []
    insertados = 0
    for i, ln in enumerate(lineas):
        if PRINCIPIO.match(ln) and salida and salida[-1].strip() != "" and PRINCIPIO.match(salida[-1]):
            salida.append("")
            insertados += 1
        salida.append(ln)
    nuevo_bloque = nl.join(salida)

    if insertados == 0:
        print("SIN CAMBIOS: ya hay linea en blanco entre principios (o no hay lista)")
        return
    nuevo = txt[:ini] + nuevo_bloque + txt[fin:]
    with io.open(P, "w", encoding="utf-8", newline="") as f:
        f.write(nuevo)
    print("lineas en blanco insertadas:", insertados)
    print("palabras antes:", len(txt.split()), "despues:", len(nuevo.split()))


if __name__ == "__main__":
    main()
