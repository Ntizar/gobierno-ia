# -*- coding: utf-8 -*-
"""
Aritmética verificable — Ministerio de Sanidad, sesión 21/30 (2026-09-30).

Toda cifra de propuestas/2026-09-30.md se reproduce ejecutando este script.
No hay ni un número escrito "de cabeza": si algo no cuadra, se ve aquí.
"""
import hashlib
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
LEY = REPO / "ministerios/sanidad/leyes/BOE-A-1986-10499.md"


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- 1. Estado de la ley insignia (medido, no declarado) -------------------
ley_bytes = LEY.read_bytes()
ley_txt = ley_bytes.decode("utf-8")
palabras = len(ley_txt.split())
bloques = sum(1 for ln in ley_txt.splitlines() if ln.startswith("## ["))

# --- 2. Reparto territorial de créditos: foto verificada -------------------
# F5 (IM Médico, 13-07-2026, archivada el 29-09) — importes al euro.
lin_ap = 172_425_000      # Atención Primaria y Comunitaria
lin_buco = 60_058_000     # cartera bucodental
lin_sis = 2_006_950       # sistemas de información del SNS
lin_enf = 960_000         # cuidados de enfermería
total_13jul = lin_ap + lin_buco + lin_sis + lin_enf

# F3 (orden del día del Interterritorial, archivada el 29-09) — bloque mayor.
bloque_2o = 50_268_707.0746
reparto_anual = total_13jul + bloque_2o

# --- 3. La reasignación propuesta (método declarado: 5,0 % exacto) ---------
pct_trasvase = 5.0
reasignacion = round(lin_buco * pct_trasvase / 100, 2)   # 3.002.900,00 €
sis_despues = lin_sis + reasignacion                     # 5.009.850,00 €
buco_despues = lin_buco - reasignacion                   # 57.055.100,00 €
factor_sis = round(sis_despues / lin_sis, 4)

pct_sis_antes = round(lin_sis / reparto_anual * 100, 4)
pct_sis_despues = round(sis_despues / reparto_anual * 100, 4)

# --- 4. Contexto del acuerdo 107 (diferencial de coste por alta) -----------
coste_medio_25proc = 6_699.0
coste_medio_quir = 8_758.7
diferencial_alta = round(coste_medio_quir - coste_medio_25proc, 1)   # 2.059,7

# --- 5. Partidas del orden del día (9-O) según prensa del 29-09 -----------
# NATURALEZA: fuente secundaria (Gaceta Médica / La Razón, 29-09-2026).
# No es norma ni documento oficial: se etiqueta como tal y no sustituye al acta.
partidas_9o = {
    "cohesion_sanitaria_formacion_y_trasplantes": 50_270_000,
    "enfermedades_raras_y_neurodegenerativas_ELA": 2_810_000,
    "autosuficiencia_plasma_humano": 2_000_000,
    "prevencion_y_cribados_tabaquismo": 3_000_000,
    "sistemas_de_vigilancia": 7_000_000,
    "sivain_y_unidades_de_plasma": 5_000_000,
}
suma_9o_prensa = sum(partidas_9o.values())

# --- 6. Comprobaciones (se imprimen en claro; si alguna falla, se ve) -------
comprobaciones = {
    "ley_palabras_19540": palabras == 19540,
    "ley_bloques_151": bloques == 151,
    "235_449_950_cuadra": total_13jul == 235_449_950,
    "285_718_657_0746_cuadra": round(reparto_anual, 4) == 285_718_657.0746,
    "reasignacion_5pct_exacto": reasignacion == 3_002_900.0,
    "sis_despues_cuadra": sis_despues == 5_009_850.0,
    "buco_despues_cuadra": buco_despues == 57_055_100.0,
    "diferencial_2059_7": diferencial_alta == 2059.7,
}

salida = {
    "ley": {
        "fichero": "ministerios/sanidad/leyes/BOE-A-1986-10499.md",
        "sha256": sha256(LEY),
        "palabras": palabras,
        "bloques": bloques,
    },
    "reparto": {
        "13_jul_2026_total_eur": total_13jul,
        "orden_del_dia_total_eur": bloque_2o,
        "reparto_anual_eur": round(reparto_anual, 4),
        "linea_ap_eur": lin_ap,
        "linea_bucodental_eur": lin_buco,
        "linea_sis_antes_eur": lin_sis,
        "linea_enfermeria_eur": lin_enf,
    },
    "reasignacion": {
        "metodo": "5,0 % exacto de la linea bucodental 2026",
        "importe_eur": reasignacion,
        "linea_sis_despues_eur": sis_despues,
        "linea_bucodental_despues_eur": buco_despues,
        "factor_crecimiento_sis": factor_sis,
        "pct_sis_sobre_reparto_antes": pct_sis_antes,
        "pct_sis_sobre_reparto_despues": pct_sis_despues,
        "coste_fiscal_neto_eur": 0,
    },
    "acuerdo_107_contexto": {
        "coste_medio_25_procesos_eur": coste_medio_25proc,
        "coste_medio_quirurgico_eur": coste_medio_quir,
        "diferencial_por_alta_eur": diferencial_alta,
    },
    "partidas_9o_prensa": partidas_9o,
    "suma_partidas_9o_prensa_eur": suma_9o_prensa,
    "comprobaciones": comprobaciones,
    "todo_cuadra": all(comprobaciones.values()),
}

salidajson = pathlib.Path(__file__).with_suffix(".json")
salidajson.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")

print(json.dumps(salida, indent=1, ensure_ascii=False))
print("\nTODO CUADRA:", salida["todo_cuadra"])
