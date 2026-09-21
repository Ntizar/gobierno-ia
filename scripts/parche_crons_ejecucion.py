#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica la REGLA DE EJECUCION a los crons vivos del Gobierno IA y sincroniza
las copias de prompts del repo. Idempotente: no duplica el bloque si ya existe.

Uso: python scripts/parche_crons_ejecucion.py [--dry-run]
"""
import json, io, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS = os.path.expandvars(r"$LOCALAPPDATA/hermes/cron/jobs.json")
MARCA = "REGLA DE EJECUCIÓN (no negociable, añadida 2026-09-21)"

BLOQUE_EJECUCION = """
REGLA DE EJECUCIÓN (no negociable, añadida 2026-09-21): el sistema acumuló 16 acuerdos aprobados sin aplicar sobre los ficheros de ley (los ficheros no se tocaban desde el 04-09). Eso no puede repetirse. Antes de proponer artículos nuevos, cada ministro EJECUTA sobre el fichero de su ley los acuerdos APROBADOS pendientes que le toquen (mira la sección «Deuda de ejecución» de constitution/mision-30-sesiones.md): copia .bak-<fecha> del fichero, sha256 ANTES y DESPUÉS, manifiesto en ministerios/<carpeta>/evidencia/manifiesto_*.json con el detalle por bloque, y verificación de que el bloque objetivo queda con UNA sola copia del texto. PROHIBIDO re-aplicar un diff ya ejecutado: comprueba primero el hash del bloque y, si ya está aplicado, dilo y no lo toques. Un acuerdo aprobado que siga sin ejecutarse al día siguiente es DEUDA y debe aparecer como tal en la primera línea del informe. Solo después de ejecutar y verificar propone artículos NUEVOS, y nunca propone un artículo que ya tenga un acuerdo aprobado pendiente de ejecución.
"""

BLOQUE_PRESIDENTE = """
REGLA DE EJECUCIÓN (no negociable, añadida 2026-09-21): en el acta y en la respuesta, el Presidente debe incluir SIEMPRE la línea de ejecución: «Ejecutados hoy: N acuerdos (con hash del fichero) · Pendientes de ejecución: M acuerdos». Si M no baja respecto a la sesión anterior, dilo explícitamente como fallo del Gobierno, no lo maquilles. Los acuerdos APROBADOS CON CONDICIÓN no cuentan como ejecutados hasta que la condición se cumple por escrito.
"""

OBJETIVO = {
    "7f86939758e2": ("pase-lista.txt", BLOQUE_EJECUCION),
    "d8c606f0f8da": ("consejo.txt", BLOQUE_EJECUCION + BLOQUE_PRESIDENTE),
}


def main():
    dry = "--dry-run" in sys.argv
    with io.open(JOBS, encoding="utf-8") as f:
        data = json.load(f)
    jobs = data if isinstance(data, list) else data.get("jobs", data)

    cambios = []
    for j in jobs:
        jid = j.get("job_id") or j.get("id")
        if jid not in OBJETIVO:
            continue
        fichero_repo, bloque = OBJETIVO[jid]
        pr = j.get("prompt") or ""
        if MARCA in pr:
            cambios.append((jid, "YA TIENE LA REGLA (sin cambios)"))
            continue
        nuevo = pr.rstrip() + "\n" + bloque
        if not dry:
            r = subprocess.run(["hermes", "cron", "edit", jid, "--prompt", nuevo],
                               capture_output=True, cwd=REPO)
            if r.returncode != 0:
                cambios.append((jid, "ERROR: " + r.stderr.decode("utf-8", "replace")[:300]))
                continue
            with io.open(os.path.join(REPO, "constitution", "prompts-cron", fichero_repo),
                         "w", encoding="utf-8", newline="\n") as f:
                f.write(nuevo)
        cambios.append((jid, "ACTUALIZADO (%d -> %d chars)" % (len(pr), len(nuevo))))
    for jid, estado in cambios:
        print(jid, "|", estado)


if __name__ == "__main__":
    main()
