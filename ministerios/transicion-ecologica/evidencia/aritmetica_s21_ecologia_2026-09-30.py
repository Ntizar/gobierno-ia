# -*- coding: utf-8 -*-
"""Sesion 21/30 (2026-09-30) - Ministerio de Transicion Ecologica.
Aritmetica verificable del dia:
  1) verificacion de la ley (sha256, palabras, bloques) y de los bloques [a1-11] y [a7]
  2) reparto por cuenca del art. 19.4.h) recalculado con el NdP OFICIAL del MITECO (29-09-2026)
  3) aritmetica del mercado OMIE del 30-09-2026 (tabla horaria publicada)
Convencion de hash de bloque: la declarada en scripts/hash_bloques_s18_2026-09-27.py
(bloque desde su rotulo '## [' hasta la linea anterior al siguiente rotulo, rstrip, LF, UTF-8).
"""
import hashlib, io, json, os, re

LEY = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
Ndp = "ministerios/transicion-ecologica/evidencia/fuentes_s21_2026-09-30/NdP_reserva_hidrica_2026-09-29.pdf"

res = {}

# ---------- 1) la ley ----------
raw = io.open(LEY, encoding="utf-8").read()
res["ley"] = {
    "sha256": hashlib.sha256(io.open(LEY, "rb").read()).hexdigest(),
    "palabras": len(raw.split()),
    "lineas": len(raw.split("\n")),
}
lines = raw.split("\n")
marks = [i for i, l in enumerate(lines) if l.startswith("## [")]
blocks = {}
for k, i in enumerate(marks):
    j = marks[k + 1] if k + 1 < len(marks) else len(lines)
    name = lines[i].split("]")[0][4:]
    blocks[name] = "\n".join(lines[i:j]).rstrip("\n")
res["ley"]["bloques_rotulo_##["] = len(marks)
res["ley"]["bloques_unicos"] = len(blocks)
res["bloques"] = {}
for nm in ("a1-7", "a1-11", "a7", "da-9"):
    if nm in blocks:
        res["bloques"][nm] = {
            "sha256": hashlib.sha256(blocks[nm].encode("utf-8")).hexdigest(),
            "palabras": len(blocks[nm].split()),
            "primera_linea": blocks[nm].split("\n")[0],
        }

# NdP oficial del MITECO
res["ndp_pdf"] = {"sha256": hashlib.sha256(io.open(Ndp, "rb").read()).hexdigest(),
                  "bytes": os.path.getsize(Ndp)}

# ---------- 2) reparto por cuenca (metodo declarado, datos OFICIALES 29-09-2026) ----------
# datos del cuadro del NdP: capacidad total (hm3), reserva actual (hm3)
oficial = {
    "Cantábrico Oriental": (73, 44), "Cantábrico Occidental": (490, 287), "Miño-Sil": (3030, 1768),
    "Galicia Costa": (684, 354), "Cuencas internas del País Vasco": (21, 15), "Duero": (7602, 3907),
    "Tajo": (11056, 6068), "Guadiana": (9538, 6877), "Tinto, Odiel y Piedras": (229, 149),
    "Guadalete-Barbate": (1651, 1253), "Guadalquivir": (8030, 5590),
    "Cuenca Mediterránea Andaluza": (1174, 755), "Segura": (1140, 571), "Júcar": (2846, 1478),
    "Ebro": (7802, 3590), "Cuencas internas de Cataluña": (677, 498),
}
total_cap, total_act = 56043, 33204
nacional = 59.2   # porcentaje PUBLICADO en el NdP (titular: «al 59,2 %»)
# porcentajes PUBLICADOS por el NdP (los que se usan para el peso)
pct = {
    "Cantábrico Oriental": 60.3, "Cantábrico Occidental": 58.6, "Miño-Sil": 58.3,
    "Galicia Costa": 51.8, "Cuencas internas del País Vasco": 71.4, "Duero": 51.4,
    "Tajo": 54.9, "Guadiana": 72.1, "Tinto, Odiel y Piedras": 65.1,
    "Guadalete-Barbate": 75.9, "Guadalquivir": 69.6, "Cuenca Mediterránea Andaluza": 64.3,
    "Segura": 50.1, "Júcar": 51.9, "Ebro": 46.0, "Cuencas internas de Cataluña": 73.6,
}
nacional_control = round(100.0 * total_act / total_cap, 2)  # control aritmetico: 59,25
# universo declarado: cuencas peninsulares por debajo de la media nacional
deficit = {k: round(nacional - p, 1) for k, p in pct.items() if p < nacional}
D = round(sum(deficit.values()), 1)
TOTAL = 40.90
euro_por_punto = TOTAL / D
reparto = {k: round(v * euro_por_punto, 2) for k, v in sorted(deficit.items(), key=lambda x: -x[1])}
res["reparto"] = {
    "media_nacional_pct": nacional, "cuencas_bajo_media": len(deficit),
    "deficit_total_puntos": D, "euro_por_punto": round(euro_por_punto, 6),
    "total_M€": TOTAL, "suma_M€": round(sum(reparto.values()), 2),
    "detalle": {k: {"pct": pct[k], "deficit_puntos": deficit[k], "M€": reparto[k]}
                for k in reparto},
    "cuencas_excluidas_por_encima_media": {k: pct[k] for k, p in pct.items() if p >= nacional},
}

# comparacion con el reparto entregado el 29-09 (acuerdo 122) - las 5 cuencas de entonces
ayer = {"Ebro": 11.77, "Júcar": 8.64, "Segura": 8.16, "Galicia Costa": 6.26, "Duero": 6.07}
res["reparto"]["cotejo_con_29_09"] = {
    k: {"M€_29_09": ayer[k], "M€_30_09": reparto.get(k)} for k in ayer}

# ---------- 3) OMIE 30-09-2026 (tabla horaria publicada) ----------
horas = [133.35, 132.56, 133.35, 138.11, 136.68, 153.94, 169.13, 204.69, 205.32, 180.72, 159.64,
         125.57, 105.20, 89.07, 96.60, 114.18, 128.12, 168.38, 214.28, 242.07, 249.61, 231.22,
         230.37, 217.27]
media = round(sum(horas) / len(horas), 2)
res["omie_3009"] = {
    "horas": len(horas), "suma": round(sum(horas), 2), "media_calculada": media,
    "min": min(horas), "max": max(horas), "diferencial": round(max(horas) - min(horas), 2),
    "ratio_max_min": round(max(horas) / min(horas), 2),
    "horas_por_encima_200": sum(1 for h in horas if h > 200),
    "horas_por_debajo_100": sum(1 for h in horas if h < 100),
    "media_dia_anterior": 130.10,
    "variacion_pct": round(100 * (media / 130.10 - 1), 2),
}

# dias hasta el 31-10-2026 (condicion del acuerdo 111)
import datetime
res["plazos"] = {
    "dias_hasta_31_10_2026": (datetime.date(2026, 10, 31) - datetime.date(2026, 9, 30)).days,
    "dias_hasta_30_06_2027": (datetime.date(2027, 6, 30) - datetime.date(2026, 9, 30)).days,
    "dias_hasta_31_12_2026": (datetime.date(2026, 12, 31) - datetime.date(2026, 9, 30)).days,
}

out = "ministerios/transicion-ecologica/evidencia/aritmetica_s21_ecologia_2026-09-30.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=2))
print(json.dumps(res, ensure_ascii=False, indent=2))
print("\nJSON ->", out)
