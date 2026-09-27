#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sesión 18/30 — cascada del nombre fósil «Ministerio de Sanidad y Consumo» (acuerdo 76).
Autora: Mónica García, Ministra de Sanidad.
Aplica 5 sustituciones literales (1 sola copia cada una, comprobada) sobre las
apariciones restantes del fósil, una vez matada [acuarentaysiete].4 en la sesión 17.
Regla anti-reaplicación: exige 5 ocurrencias exactas y la de [acuarentaysiete] a CERO.
Dry-run por defecto; --apply escribe.
"""
import hashlib
import json
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FECHA = "2026-09-27"
LGS = "ministerios/sanidad/leyes/BOE-A-1986-10499.md"

# (bloque, texto_antes_literal, texto_despues_literal)
SUSTITUCIONES = [
    ("aquince.2",
     "2. El Ministerio de Sanidad y Consumo acreditará servicios de referencia,",
     "2. El Ministerio de Sanidad acreditará servicios de referencia,"),
    ("atreintayocho.3",
     "3. El Ministerio de Sanidad y Consumo colaborará con otros Departamentos",
     "3. El Ministerio de Sanidad colaborará con otros Departamentos"),
    ("aochentaydos",
     "las comunidades autónomas remitirán puntualmente al Ministerio de Sanidad y Consumo sus Presupuestos,",
     "las comunidades autónomas remitirán puntualmente al Ministerio de Sanidad sus Presupuestos,"),
    ("aciento",
     "serán elaborados por el Ministerio de Sanidad y Consumo.",
     "serán elaborados por el Ministerio de Sanidad."),
    ("novena-2",
     "adscritos al Ministerio de Sanidad y Consumo y, entre ellos,",
     "adscritos al Ministerio de Sanidad y, entre ellos,"),
]

def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def main():
    aplicar = "--apply" in sys.argv
    path = os.path.join(REPO, LGS)
    raw = open(path, "rb").read()
    sha_antes = hashlib.sha256(raw).hexdigest()
    txt = raw.decode("utf-8")
    nwc_antes = len(txt.split())

    manifiesto = {
        "fecha": FECHA, "sesion": "18/30", "autor": "Mónica García (Sanidad) — ejecución propia",
        "acuerdo_al_al_rojo": "76 (cascada declarada en sesión 17)",
        "leyenda": "Cascada del nombre fósil 'Ministerio de Sanidad y Consumo': 5 apariciones restantes -> 0",
        "fichero": LGS, "sha256_antes": sha_antes, "palabras_antes": nwc_antes,
        "ejecucion_en_ley": bool(aplicar), "bloques": [],
    }
    ok = True
    nuevo = txt
    for bloque, antes, despues in SUSTITUCIONES:
        copias = txt.count(antes)
        reg = {"bloque": bloque, "antes_literal": antes, "despues_literal": despues,
               "ocurrencias_antes_del_diff": copias}
        if copias != 1:
            reg["estado"] = "RECHAZADO_por_ocurrencias"
            ok = False
        else:
            reg["estado"] = "unicidad_verificada"
            nuevo = nuevo.replace(antes, despues, 1)
        manifiesto["bloques"].append(reg)

    # anti-reaplicación: la aparición de [acuarentaysiete] ya muerta en la 17 debe seguir muerta
    fosil_restante_antes = txt.count("Ministerio de Sanidad y Consumo")
    fosil_restante_despues = nuevo.count("Ministerio de Sanidad y Consumo")
    manifiesto["fosil_check"] = {
        "ocurrencias_fossil_antes": fosil_restante_antes,
        "ocurrencias_fossil_despues": fosil_restante_despues,
        "esperado_antes": 5, "esperado_despues": 0,
    }
    if fosil_restante_antes != 5 or fosil_restante_despues != 0:
        ok = False
        manifiesto["fosil_check"]["estado"] = "FALLO"
    else:
        manifiesto["fosil_check"]["estado"] = "OK"

    if not ok:
        print(json.dumps({"resultado": "ABORT — no se escribe nada", "manifiesto": manifiesto},
                         ensure_ascii=False, indent=2))
        sys.exit(1)

    nwc_despues = len(nuevo.split())
    manifiesto["palabras_despues"] = nwc_despues
    manifiesto["delta_palabras"] = nwc_despues - nwc_antes
    for reg in manifiesto["bloques"]:
        reg["aplicado"] = bool(aplicar)

    if aplicar:
        bak = path + ".bak-2026-09-27"
        shutil.copy2(path, bak)
        with open(path, "wb") as fh:
            fh.write(nuevo.encode("utf-8"))
        manifiesto["bak"] = os.path.relpath(bak, REPO)
        manifiesto["sha256_bak"] = sha(bak)
        manifiesto["sha256_despues"] = sha(path)
        manifiesto["bloques_identicos_a_propuesto"] = True
        # verificación post: releer y comprobar 0 fósiles y cada 'despues' presente 1 vez
        chk = open(path, "rb").read().decode("utf-8")
        manifiesto["verificacion_post"] = {
            "fosil_cero": chk.count("Ministerio de Sanidad y Consumo") == 0,
            "despues_presente": all(chk.count(d) == 1 for _, _, d in SUSTITUCIONES),
            "sha256_reido": sha(path),
        }
        out = os.path.join(REPO, "ministerios", "sanidad", "evidencia",
                           "manifiesto_cascada_fosil_s18_2026-09-27.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(manifiesto, fh, ensure_ascii=False, indent=2)
        print("ESCRITO:", out)
        print("sha256 ANTES:", manifiesto["sha256_antes"])
        print("sha256 DESPUES:", manifiesto["sha256_despues"])
        print("palabras:", nwc_antes, "->", nwc_despues, "delta:", nwc_despues - nwc_antes)
        print("verificacion_post:", manifiesto["verificacion_post"])
    else:
        print(json.dumps({"resultado": "DRY-RUN (sin escribir)", "manifiesto": manifiesto},
                         ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
