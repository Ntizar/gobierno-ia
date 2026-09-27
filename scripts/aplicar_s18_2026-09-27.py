#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ejecución material de la ronda 3 del Consejo de la sesión 18/30 (2026-09-27).

Aplica los acuerdos APROBADOS esta noche, con dry-run por defecto y --apply para escribir:
  LGT  [a65]  art. 65  : 1.764 -> 516 palabras (dedupe 5 capas + letra a) restituida)
  LGT  [a112] art. 112 : 2.560 -> 451 palabras (4 capas -> 1; cae la capa «sede electronica» sin traza BOE)
  LGS  [acuatro] art. 4: 63 -> 117 palabras (nuevo apartado 3, redaccion del 17-09 + ESTIMACION etiquetada)
  LGS  [aciento].3     : 29 -> 28 palabras («Comunidad Economica Europea» -> «Union Europea»)

Todo el trabajo es en BYTES: los ficheros de ley usan CRLF y las evidencias de los ministerios LF;
la conversion LF->CRLF se hace SOLO dentro del bloque que se inserta, para no tocar el resto del fichero.
Convencion de hash de bloque declarada: sha256 de los bytes del rango [linea del rotulo .. linea anterior
al siguiente '## ['] unidos por CRLF, sin salto final. Reglas: .bak previo, sha256 antes/despues,
precondicion del bloque vivo (dos direcciones), 1 rotulo por bloque y prohibicion de re-aplicacion.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOY = "2026-09-27"
LGT = ROOT / "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
LGS = ROOT / "ministerios/sanidad/leyes/BOE-A-1986-10499.md"
EV_H = ROOT / "ministerios/hacienda/evidencia"
MANIF = ROOT / "consejo/evidencia/manifiesto_consejo_s18_2026-09-27.json"
SUMS = ROOT / "consejo/evidencia/SHA256SUMS_2026-09-27.txt"

APARTADO3 = ("3. El derecho a la asistencia sanitaria universal incluye, como mínimo, la garantía de una fecha real "
             "de intervención no superior a 90 días desde la derivación de Atención Primaria para las intervenciones "
             "prioritarias, y no superior a 180 días para las intervenciones ordinarias, con independencia del "
             "resultado de cualquier planificación o criterio administrativo.")
CEE = "de la Comunidad Económica Europea."
UE = "de la Unión Europea."


def sha(b):
    return hashlib.sha256(b).hexdigest()


def wc(b):
    # convencion del proyecto = `wc -w` en locale UTF-8 = str.split() de Python (U+00A0 tambien separa)
    return len(b.decode("utf-8").split())


def split_crlf(b):
    return b.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")


def join_crlf(lines, original):
    sep = "\r\n" if original.count(b"\r\n") else "\n"
    return sep.encode("utf-8").join(l.encode("utf-8") for l in lines)


def region_bytes(lines, i, j, sep=b"\r\n"):
    return sep.join(l.encode("utf-8") for l in lines[i:j])


def find_block(lines, name):
    idx = [i for i, l in enumerate(lines) if l.startswith("## [")]
    for k, i in enumerate(idx):
        if lines[i].startswith("## [" + name + "]"):
            return i, (idx[k + 1] if k + 1 < len(idx) else len(lines))


def main(apply_it):
    manifiesto = {
        "sesion": "18/30", "fecha": HOY, "ejecutor": "Presidencia (ronda 3)", "dry_run": not apply_it,
        "convencion_hash_bloque": "sha256 de los bytes del rango [linea del rotulo .. linea anterior al siguiente '## ['] unidos por CRLF, sin salto final",
        "ficheros": {}, "bloques": [],
    }
    planes = []

    lgt_b = LGT.read_bytes()
    lgt_lines = split_crlf(lgt_b)
    for name, evf, declarado in (("a65", "bloque_propuesto_a65_2026-09-27.txt", 516),
                                 ("a112", "bloque_propuesto_a112_2026-09-27.txt", 451)):
        i, j = find_block(lgt_lines, name)
        vivo = (EV_H / ("bloque_vivo_" + name + "_2026-09-27.txt")).read_bytes().decode("utf-8")
        prop = (EV_H / evf).read_bytes().decode("utf-8")
        actual = region_bytes(lgt_lines, i, j).decode("utf-8")
        planes.append(dict(f="LGT", bloque=name, i=i, j=j, nuevo=prop.replace("\n", "\r\n"),
                           ya_aplicado=(actual.strip() == prop.strip()),
                           pre_ok=(actual == vivo.replace("\n", "\r\n")),
                           pal_antes=wc(actual.encode("utf-8")), pal_desp=wc(prop.encode("utf-8")),
                           declarado=declarado, evidencia_vivo="evidencia/bloque_vivo_%s_2026-09-27.txt" % name))

    lgs_b = LGS.read_bytes()
    lgs_lines = split_crlf(lgs_b)
    propuesta_s = (ROOT / "ministerios/sanidad/propuestas/2026-09-27.md").read_text(encoding="utf-8")
    assert APARTADO3 in propuesta_s, "el apartado 3 no coincide con el texto de la propuesta de Sanidad"
    i4, j4 = find_block(lgs_lines, "acuatro")
    actual4 = region_bytes(lgs_lines, i4, j4).decode("utf-8")
    nuevo4 = actual4.rstrip("\r\n") + "\r\n\r\n" + APARTADO3
    planes.append(dict(f="LGS", bloque="acuatro", i=i4, j=j4, nuevo=nuevo4,
                       ya_aplicado=(APARTADO3 in actual4), pre_ok=True,
                       pal_antes=wc(actual4.encode("utf-8")), pal_desp=wc(nuevo4.encode("utf-8")),
                       declarado=117, evidencia_vivo=None))

    i5, j5 = find_block(lgs_lines, "aciento")
    actual5 = region_bytes(lgs_lines, i5, j5).decode("utf-8")
    assert actual5.count(CEE) == 1, "la CEE no aparece exactamente 1 vez en [aciento]"
    nuevo5 = actual5.replace(CEE, UE)
    planes.append(dict(f="LGS", bloque="aciento.3", i=i5, j=j5, nuevo=nuevo5,
                       ya_aplicado=(CEE not in actual5 and UE in actual5), pre_ok=True,
                       pal_antes=wc(actual5.encode("utf-8")), pal_desp=wc(nuevo5.encode("utf-8")),
                       declarado=28, evidencia_vivo=None))

    print("PLAN (dry-run):")
    for p in planes:
        print("  %-4s %-10s lineas %d-%d | pal %d -> %d | ya_aplicado=%s | pre_ok=%s | sha_bloque_antes=%s"
              % (p["f"], p["bloque"], p["i"] + 1, p["j"], p["pal_antes"], p["pal_desp"], p["ya_aplicado"],
                 p["pre_ok"], sha(region_bytes(lgt_lines if p["f"] == "LGT" else lgs_lines, p["i"], p["j"]))[:12]))

    for target, planes_f in ((LGT, [p for p in planes if p["f"] == "LGT"]),
                             (LGS, [p for p in planes if p["f"] == "LGS"])):
        raw = target.read_bytes()
        antes_sha, antes_pal = sha(raw), wc(raw)
        lines = split_crlf(raw)
        antes_bloques = len([l for l in lines if l.startswith("## [")])
        nuevo_lines = list(lines)
        activos = [p for p in planes_f if not p["ya_aplicado"]]
        for p in sorted(activos, key=lambda x: -x["i"]):
            if not p["pre_ok"]:
                raise SystemExit("PRECONDICION FALLIDA en %s %s: el bloque vivo no coincide con la evidencia"
                                 % (p["f"], p["bloque"]))
            nuevo_lines = nuevo_lines[:p["i"]] + p["nuevo"].split("\r\n") + nuevo_lines[p["j"]:]
        nuevo_raw = join_crlf(nuevo_lines, raw)
        info = {"sha256_antes": antes_sha, "palabras_antes": antes_pal, "bloques_antes": antes_bloques,
                "sha256_despues": sha(nuevo_raw), "palabras_despues": wc(nuevo_raw),
                "bloques_despues": len([l for l in split_crlf(nuevo_raw) if l.startswith("## [")]),
                "crlf": raw.count(b"\r\n") > 0, "verificaciones": []}
        for p in planes_f:
            nl = split_crlf(nuevo_raw)
            ii, jj = find_block(nl, p["bloque"].split(".")[0])
            reg = region_bytes(nl, ii, jj)
            v = {"bloque": p["bloque"], "rotulos": sum(1 for l in nl if l.startswith("## [" + p["bloque"] + "]")
                                                       or l.startswith("## [" + p["bloque"].split(".")[0] + "]")),
                 "sha_bloque_despues": sha(reg), "palabras_bloque_despues": wc(reg)}
            if p["bloque"] in ("a65", "a112"):
                v["resultante_igual_propuesto"] = reg.decode("utf-8").replace("\r\n", "\n") == \
                    p["nuevo"].replace("\r\n", "\n")
            elif p["bloque"] == "acuatro":
                v["apartado3_una_sola_vez"] = reg.decode("utf-8").count(APARTADO3) == 1
                v["cadena_90dias_una_sola_vez"] = nuevo_raw.decode("utf-8").count("no superior a 90 días") == 1
            else:
                v["cee_restante"] = nuevo_raw.decode("utf-8").count(CEE)
                linea_antes = [l for l in actual5.split("\r\n") if CEE in l][0]
                linea_desp = [l for l in nuevo_raw.decode("utf-8").split("\r\n") if "Unión Europea" in l][0]
                v["parrafo_3_palabras"] = "%d -> %d" % (len(linea_antes.split()), len(linea_desp.split()))
                v["linea_3_identica_a_propuesta"] = linea_desp in propuesta_s
            info["verificaciones"].append(v)
        ruta = str(target.relative_to(ROOT)).replace("\\", "/")
        info["ruta"] = ruta
        if apply_it and activos:
            suf = "-consejo" if target == LGS else ""
            bak = Path(str(target) + ".bak-" + HOY + suf)
            if not bak.exists():
                shutil.copy2(target, bak)
            info["bak"] = str(bak.relative_to(ROOT)).replace("\\", "/")
            info["bak_sha256"] = sha(bak.read_bytes())
            target.write_bytes(nuevo_raw)
            assert sha(target.read_bytes()) == info["sha256_despues"]
        manifiesto["ficheros"][ruta] = info

    for p in planes:
        manifiesto["bloques"].append({
            "fichero": p["f"], "bloque": p["bloque"], "lineas_antes": [p["i"] + 1, p["j"]],
            "palabras_antes": p["pal_antes"], "palabras_despues": p["pal_desp"],
            "declarado_por_el_ministro": p["declarado"], "ya_aplicado": p["ya_aplicado"],
            "precondicion_bloque_vivo": p["pre_ok"], "evidencia_vivo": p["evidencia_vivo"],
        })
    manifiesto["resumen"] = {r: {"palabras": "%s -> %s" % (i["palabras_antes"], i["palabras_despues"]),
                                "sha256": "%s -> %s" % (i["sha256_antes"], i["sha256_despues"])}
                             for r, i in manifiesto["ficheros"].items()}
    if apply_it:
        MANIF.parent.mkdir(parents=True, exist_ok=True)
        MANIF.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
        SUMS.write_text("".join("%s  %s\n" % (i["sha256_despues"], r)
                                for r, i in sorted(manifiesto["ficheros"].items())), encoding="utf-8")
    print(json.dumps(manifiesto["resumen"], ensure_ascii=False, indent=2))
    print(json.dumps([i["verificaciones"] for i in manifiesto["ficheros"].values()], ensure_ascii=False, indent=2))
    print("MODO:", "APLICADO" if apply_it else "DRY-RUN")


if __name__ == "__main__":
    main("--apply" in sys.argv)
