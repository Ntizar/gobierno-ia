#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reparacion de fidelidad LGS descubierta por el test cruzado ciego (21-09-2026).

Hallazgo 1 — [adieciseis] art. 16: el bloque arranca en «2.» porque falta el
apartado 1 vigente del BOE (atención primaria / asignación de equipos y libre
elección). Numeración huérfana = firma del corte.
Hallazgo 2 — [aseis] art. 6: el BOE consolidado numera la introducción como
apartado «1.» (renumeración de la LO 3/2007); el repo la tenía sin prefijo.

Ambas son RESTITUCIONES DE FIDELIDAD (texto del BOE que faltaba), no ahorro.
Idempotente: si ya están aplicadas, no escribe.
"""
import io, re, json, hashlib, os, datetime

P = "ministerios/sanidad/leyes/BOE-A-1986-10499.md"
BAK = P + ".bak-2026-09-21b-reparacion"

FALTA_16 = ("1. Por lo que se refiere a la atención primaria, se les aplicarán las mismas "
            "normas sobre asignación de equipos y libre elección que al resto de los usuarios.")
ANCLA_16 = "2. El ingreso en centros hospitalarios se efectuará a través de la unidad de admisión del hospital"
PREFIJO_6 = "1. Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:"


def main():
    with io.open(P, encoding="utf-8", newline="") as f:
        txt = f.read()
    nl = "\r\n" if "\r\n" in txt else "\n"
    antes = txt
    cambios = []

    # --- Hallazgo 1: restituir apartado 1 del art. 16 ---
    if "atención primaria, se les aplicarán las mismas normas" not in txt:
        idx = txt.find(ANCLA_16)
        if idx == -1:
            raise SystemExit("no encuentro el ancla del art. 16")
        txt = txt[:idx] + FALTA_16 + nl + nl + txt[idx:]
        cambios.append({"hallazgo": "art. 16 LGS: restituido el apartado 1 vigente (atención primaria / libre elección)",
                        "tipo": "restauracion_fidelidad", "palabras_anadidas": len(FALTA_16.split())})
    else:
        cambios.append({"hallazgo": "art. 16 LGS: el apartado 1 ya estaba presente", "tipo": "sin_cambios"})

    # --- Hallazgo 2: prefijo «1.» en la introducción del art. 6 ---
    m = re.search(r"^## \[aseis\][^\r\n]*\r?\n", txt, re.M)
    ini = m.end()
    sig = re.search(r"^## \[", txt[ini:], re.M)
    fin = ini + sig.start()
    bloque = txt[ini:fin]
    if "1. Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:" in bloque:
        cambios.append({"hallazgo": "art. 6 LGS: la introducción ya lleva el prefijo «1.»", "tipo": "sin_cambios"})
    else:
        nuevo_bloque = bloque.replace(
            "Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:",
            PREFIJO_6, 1)
        if nuevo_bloque == bloque:
            raise SystemExit("no encuentro la introduccion del art. 6")
        txt = txt[:ini] + nuevo_bloque + txt[fin:]
        cambios.append({"hallazgo": "art. 6 LGS: restituido el prefijo «1.» de la introducción (renumeración LO 3/2007)",
                        "tipo": "restauracion_fidelidad", "palabras_anadidas": 1})

    if txt == antes:
        print("SIN CAMBIOS: nada que reparar")
        return

    with io.open(BAK, "w", encoding="utf-8", newline="") as f:
        f.write(antes)
    with io.open(P, "w", encoding="utf-8", newline="") as f:
        f.write(txt)

    man = {
        "acto": "reparacion de fidelidad LGS por hallazgo del test cruzado ciego",
        "fecha": datetime.date.today().isoformat(),
        "sesion": "13/30",
        "disparador": "consejo/evidencia/test_cruzado_LGS_2026-09-21.md (veredicto RECHAZADA en [adieciseis])",
        "responsable": "Presidencia (Mastermind) — pendiente de ratificacion por el Consejo",
        "sha256_antes": hashlib.sha256(antes.encode("utf-8")).hexdigest(),
        "sha256_despues": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
        "palabras_antes": len(antes.split()),
        "palabras_despues": len(txt.split()),
        "tipo_contable": "RESTITUCION DE FIDELIDAD — NO es ahorro",
        "cambios": cambios,
    }
    with io.open("ministerios/sanidad/evidencia/manifiesto_reparacion_fidelidad_2026-09-21.json",
                 "w", encoding="utf-8", newline="\n") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    for c in cambios:
        print(c)
    print("palabras:", man["palabras_antes"], "->", man["palabras_despues"])
    print("sha antes:", man["sha256_antes"][:32], "| despues:", man["sha256_despues"][:32])


if __name__ == "__main__":
    main()
