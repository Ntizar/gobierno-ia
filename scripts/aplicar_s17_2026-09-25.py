#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Consejo de Ministros - sesion 17/30 (2026-09-25). Ejecucion de la ronda 3 por Presidencia.

Aplica sobre los ficheros de ley los acuerdos APROBADOS por el Consejo:
  LGT  [a203] -1250 pal | [a188] -293 pal | [a82] +297 pal (fidelidad)
  L7   [a7]   +73   pal | [da-9] +101 pal | [a1-12] +126 pal
  LGS  [acuarentaysiete].4 (0 pal, organo inexistente) | [adieciocho].15 +46 pal

Reglas: .bak-2026-09-25, sha256 antes/despues, cotejo previo bloque_vivo == bloque real,
1 sola copia del rotulo por bloque, manifiesto por bloque. NO re-aplica: si el cotejo
del bloque vivo falla, el bloque se salta y se declara (jamas se aplica a ciegas).
Uso: python aplicar_s17_2026-09-25.py [--apply]
"""
import hashlib
import json
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "2026-09-25"

LGT = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
L7 = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
LGS = "ministerios/sanidad/leyes/BOE-A-1986-10499.md"

BLOQUES = [
    (LGT, "a203", "ministerios/hacienda/evidencia/bloque_propuesto_a203_2026-09-25.txt"),
    (LGT, "a188", "ministerios/hacienda/evidencia/bloque_propuesto_a188_2026-09-25.txt"),
    (LGT, "a82", "ministerios/hacienda/evidencia/bloque_propuesto_a82_2026-09-25.txt"),
    (L7, "a7", "ministerios/transicion-ecologica/evidencia/bloque_propuesto_a7_2026-09-25.txt"),
    (L7, "da-9", "ministerios/transicion-ecologica/evidencia/bloque_propuesto_da-9_2026-09-25.txt"),
    (L7, "a1-12", "ministerios/transicion-ecologica/evidencia/bloque_propuesto_a1-12_2026-09-25.txt"),
]

# sustituciones literales (LGS)
LITERALES = [
    (LGS, "acuarentaysiete.4",
     "4. Será Presidente del Consejo Interterritorial del Sistema Nacional de Salud el Ministro de Sanidad y Consumo.",
     "4. Será Presidente del Consejo Interterritorial del Sistema Nacional de Salud el titular del Ministerio de Sanidad."),
    (LGS, "adieciocho.15",
     "15. El fomento de la investigación científica en el campo específico de los problemas de salud, atendiendo a las diferencias entre mujeres y hombres.",
     "15. El fomento de la investigación científica en el campo específico de los problemas de salud, atendiendo a las diferencias entre mujeres y hombres, mediante un plan estratégico cuya renovación se producirá con una periodicidad máxima de cinco años, con primer vencimiento a los cinco años de la entrada en vigor de esta redacción, bajo responsabilidad del Ministerio de Sanidad y con evaluación publicada en el portal de transparencia del Departamento."),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def leer_norm(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8").replace("\r\n", "\n")


def bloques_de(texto):
    """Devuelve lista de (rotulo, inicio, fin) por encabezado '## [rotulo]'."""
    pos = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## \[([^\]]+)\]", texto)]
    out = []
    for i, (ini, rot) in enumerate(pos):
        fin = pos[i + 1][0] if i + 1 < len(pos) else len(texto)
        out.append((rot, ini, fin))
    return out


def main():
    aplicar = "--apply" in sys.argv
    manifiesto = {
        "fecha": FECHA, "sesion": "17/30", "autor": "Presidencia (ronda 3)",
        "ejecucion_en_ley": False, "ficheros": {}, "bloques": [], "literales": [],
    }
    textos = {}
    for rel in (LGT, L7, LGS):
        textos[rel] = leer_norm(os.path.join(REPO, rel))
        manifiesto["ficheros"][rel] = {
            "sha256_antes": sha(os.path.join(REPO, rel)),
            "palabras_antes": len(textos[rel].split()),
            "bloques_antes": len(bloques_de(textos[rel])),
        }

    cambios_por_fichero = {}

    # --- bloques completos ---
    for rel, rot, prop_rel in BLOQUES:
        ev_vivo = os.path.join(REPO, "ministerios", rel.split("/")[1], "evidencia",
                               "bloque_vivo_%s_%s.txt" % (rot, FECHA))
        if not os.path.exists(ev_vivo):
            manifiesto["bloques"].append({"bloque": rot, "ley": rel, "estado": "SALTADO",
                                          "motivo": "sin fichero de bloque vivo de referencia"})
            continue
        prop = leer_norm(os.path.join(REPO, prop_rel)).rstrip("\n")
        vivo_ev = leer_norm(ev_vivo).rstrip("\n")
        texto = cambios_por_fichero.get(rel, textos[rel])
        lista = bloques_de(texto)
        cand = [b for b in lista if b[0] == rot]
        if len(cand) != 1:
            manifiesto["bloques"].append({"bloque": rot, "ley": rel, "estado": "SALTADO",
                                          "motivo": "rotulo aparece %d veces" % len(cand)})
            continue
        _, ini, fin = cand[0]
        real = texto[ini:fin].rstrip("\n")
        if real != vivo_ev:
            manifiesto["bloques"].append({
                "bloque": rot, "ley": rel, "estado": "SALTADO",
                "motivo": "el bloque real NO coincide con bloque_vivo de evidencia (posible aplicacion previa)",
                "sha_real": hashlib.sha256(real.encode()).hexdigest()[:16],
                "sha_evidencia": hashlib.sha256(vivo_ev.encode()).hexdigest()[:16]})
            continue
        cola = re.search(r"\n+$", texto[ini:fin])
        cola = cola.group(0) if cola else "\n"
        nuevo = prop + cola
        cambios_por_fichero[rel] = texto[:ini] + nuevo + texto[fin:]
        manifiesto["bloques"].append({
            "bloque": rot, "ley": rel, "estado": "APLICADO",
            "palabras_antes": len(real.split()), "palabras_despues": len(prop.split()),
            "delta": len(prop.split()) - len(real.split()),
            "copias_rotulo_antes": len(cand), "sha_bloque_vivo_evidencia": hashlib.sha256(vivo_ev.encode()).hexdigest()[:16],
            "fichero_propuesto": prop_rel})

    # --- sustituciones literales ---
    for rel, etiqueta, viejo, nuevo in LITERALES:
        texto = cambios_por_fichero.get(rel, textos[rel])
        n = texto.count(viejo)
        if n != 1:
            manifiesto["literales"].append({"rotulo": etiqueta, "ley": rel, "estado": "SALTADO",
                                            "motivo": "ocurrencias = %d" % n})
            continue
        a = len(texto.split())
        texto = texto.replace(viejo, nuevo)
        cambios_por_fichero[rel] = texto
        manifiesto["literales"].append({"rotulo": etiqueta, "ley": rel, "estado": "APLICADO",
                                        "ocurrencias": 1, "palabras_fichero_antes": a,
                                        "palabras_fichero_despues": len(texto.split()),
                                        "delta_fichero": len(texto.split()) - a})

    # --- verificacion y escritura ---
    for rel, texto in cambios_por_fichero.items():
        ruta = os.path.join(REPO, rel)
        orig = textos[rel]
        if texto == orig:
            manifiesto["ficheros"][rel]["cambiado"] = False
            continue
        # 1 rotulo por bloque, intacto el numero de bloques
        lb_a, lb_d = len(bloques_de(orig)), len(bloques_de(texto))
        ok_rotulos = lb_a == lb_d
        manifiesto["ficheros"][rel].update({
            "cambiado": True, "bloques_despues": lb_d, "rotulos_estables": ok_rotulos,
            "palabras_despues": len(texto.split()),
            "delta_palabras": len(texto.split()) - len(orig.split()),
            "sha256_despues": hashlib.sha256(texto.replace("\n", "\r\n").encode("utf-8")).hexdigest(),
        })
        if aplicar:
            bak = ruta + ".bak-" + FECHA
            if not os.path.exists(bak):
                shutil.copy2(ruta, bak)
            with open(ruta, "wb") as fh:
                fh.write(texto.replace("\n", "\r\n").encode("utf-8"))
            manifiesto["ficheros"][rel]["bak"] = os.path.basename(bak)
            manifiesto["ficheros"][rel]["sha256_en_disco"] = sha(ruta)
            manifests_ok = manifiesto["ficheros"][rel]["sha256_en_disco"] == manifiesto["ficheros"][rel]["sha256_despues"]
            manifiesto["ficheros"][rel]["sha256_coincide"] = manifests_ok

    manifiesto["ejecucion_en_ley"] = bool(cambios_por_fichero)
    destino = os.path.join(REPO, "consejo", "evidencia",
                           "manifiesto_consejo_s17_%s.json" % FECHA)
    if aplicar:
        with open(destino, "w", encoding="utf-8") as fh:
            json.dump(manifiesto, fh, ensure_ascii=False, indent=2)
    print(json.dumps(manifiesto, ensure_ascii=False, indent=2))
    print("\nMODO:", "APLICADO" if aplicar else "DRY-RUN (usa --apply)")


if __name__ == "__main__":
    main()
