# -*- coding: utf-8 -*-
"""Localiza por literal exacto el numero de linea de cada cita que va a firmar el ministro.
Nada de citar de memoria: el numero sale de este script, no de mi cabeza."""
import io, json, re

P = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/lgp_texto_limpio_2026-09-30.txt"
lines = {}
for l in io.open(P, encoding="utf-8"):
    l = l.rstrip("\n")
    if "\t" in l:
        n, t = l.split("\t", 1)
        lines[int(n)] = t
print("lineas cargadas:", len(lines), "| max:", max(lines))

agujas = [
    "Artículo 42. Especialidad de los créditos.",
    "Artículo 43. Especificación de los presupuestos del Estado.",
    "Artículo 46. Limitación de los compromisos de gasto.",
    "Artículo 49. Temporalidad de los créditos.",
    "Los créditos para gastos que en el último día del ejercicio presupuestario no estén afectados",
    "Artículo 50. Fondo de Contingencia de ejecución presupuestaria.",
    "por importe del dos por ciento del total de gastos para operaciones no financieras",
    "Artículo 52. Transferencias de crédito.",
    "b) No podrán realizarse entre créditos de distintas secciones presupuestarias",
    "2. Las anteriores restricciones no afectarán a las transferencias de crédito",
    "las que se deriven de convenios o acuerdos de colaboración entre distintos departamentos",
    "3. En ningún caso las transferencias podrán crear créditos destinados a subvenciones nominativas",
    "Artículo 55. Créditos extraordinarios y suplementos de crédito del Estado.",
    "Artículo 58. Incorporaciones de crédito.",
    "No obstante lo dispuesto en el artículo 49, se podrán incorporar",
    "a) Cuando así lo disponga una norma de rango legal.",
    "d) Los que resulten de créditos extraordinarios y suplementos de crédito que hayan sido concedidos",
    "Las incorporaciones de crédito que afecten al presupuesto del Estado se financiarán mediante baja en el Fondo de Contingencia",
    "Artículo 62. Competencias del Ministro de Hacienda.",
    "c) Las incorporaciones de remanentes reguladas en el artículo 58.",
    "a) Las transferencias no reservadas a la competencia del Consejo de Ministros",
    "Artículo 63. Competencias de los ministros.",
    "1. Los titulares de los distintos ministerios podrán autorizar, previo informe favorable de la Intervención Delegada",
    "a) Transferencias entre créditos de un mismo programa o entre programas de un mismo servicio",
    "no afecten a los de personal o no incrementen los créditos que enumera el apartado 2 del articulo 43",
]
res = {}
for a in agujas:
    hits = [n for n, t in lines.items() if a in t]
    res[a] = hits
    print("%-6s %s" % (hits[:3] if hits else "NO ENCONTRADO", a[:78]))

io.open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/citas_lgp_s21_2026-09-30.json",
        "w", encoding="utf-8", newline="\n").write(
    json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True))
print("\n-> evidencia/citas_lgp_s21_2026-09-30.json")
