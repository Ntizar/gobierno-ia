#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sesion 21/30 (2026-09-30) - Fase 3, jornada 3. Hacienda.
Verifica con script (no con cabeza) TODAS las cifras que hoy firma el ministro.
Salida: consola + evidencia/aritmetica_s21_2026-09-30.json
"""
import json, hashlib, os, re

W = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda"
out = {}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ---------- 1. Ley insignia intacta ----------
ley = W + "/leyes/BOE-A-2003-23186.md"
raw = open(ley, "rb").read()
txt = raw.decode("utf-8")
h = hashlib.sha256(raw).hexdigest()
out["ley"] = {
    "sha256": h,
    "palabras": len(txt.split()),
    "bloques": len(re.findall(r"(?m)^## \[", txt)),
    "encabezados_a": len(re.findall(r"(?m)^## \[a", txt)),
    "hash_esperado_coincide": h.startswith("d0b7ef22"),
}
print("LEY  sha256=%s  palabras=%d  bloques=%d  [a..]=%d  -> %s" % (
    h[:16], out["ley"]["palabras"], out["ley"]["bloques"], out["ley"]["encabezados_a"],
    "OK (d0b7ef22…)" if out["ley"]["hash_esperado_coincide"] else "FALLO"))

# ---------- 2. Arbol de las cifras del MAPA (documento oficial 29-09-2026) ----------
agricola_previo, agricola_nuevo = 107.0, 52.0
pesquero_previo, pesquero_nuevo = 35.0, 15.0
tot_agr = agricola_previo + agricola_nuevo
tot_pes = pesquero_previo + pesquero_nuevo
prorroga = agricola_nuevo + pesquero_nuevo
acumulado = tot_agr + tot_pes
out["mapa_q4_2026"] = {
    "agricola_M_eur": tot_agr, "pesquero_M_eur": tot_pes,
    "amortiguacion_total_M_eur": acumulado, "prorroga_4T_M_eur": prorroga,
    "comprueba_159": tot_agr == 159.0, "comprueba_50": tot_pes == 50.0,
    "comprueba_209": acumulado == 209.0, "comprueba_67": prorroga == 67.0,
}
print("MAPA  agrario %g = 107+52 %s | pesquero %g = 35+15 %s | amortiguacion %g %s | prorroga 4T %g %s" % (
    tot_agr, "OK" if tot_agr == 159 else "NO CUADRA",
    tot_pes, "OK" if tot_pes == 50 else "NO CUADRA",
    acumulado, "OK" if acumulado == 209 else "NO CUADRA",
    prorroga, "OK" if prorroga == 67 else "NO CUADRA"))

# ---------- 3. Remanente 932A: la cifra de ayer, re-verificada hoy ----------
cred, oblig = 1817977437.08, 1776913651.22
remanente = round(cred - oblig, 2)
out["932A_2024"] = {"creditos_definitivos": cred, "obligaciones_reconocidas": oblig,
                    "remanente": remanente,
                    "coincide_con_ayer": remanente == 41063785.86}
print("932A  %.2f - %.2f = %.2f EUR (ayer 41.063.785,86) -> %s" % (
    cred, oblig, remanente, "OK" if remanente == 41063785.86 else "NO CUADRA"))

# ---------- 4. Coste del silencio mutualistas (ESTIMACION, metodo declarado) ----------
total_devuelto, expedientes_analizados = 3500.0, 2_500_000
media_exp = total_devuelto * 1_000_000 / expedientes_analizados
pendientes = 90_717
principal_pendiente = pendientes * media_exp
interes_legal, recargo_demora = 3.25, 1.25
tipo_demora = round(interes_legal * recargo_demora, 4)
intereses_anuales = round(principal_pendiente * (1 + tipo_demora / 100) - principal_pendiente, 2)
out["mutualistas_estimacion"] = {
    "media_expediente_eur": round(media_exp, 2),
    "principal_pendiente_eur": round(principal_pendiente, 2),
    "tipo_demora_pct": tipo_demora,
    "intereses_anio_eur": intereses_anuales,
    "anios_de_remanente_que_los_paga": round(41063785.86 / intereses_anuales, 2) if intereses_anuales else None,
    "etiqueta": "ESTIMACION con metodo escrito; TECHO, no prevision",
}
print("MUT   media=%.2f EUR/exp | principal pendiente=%.0f EUR | tipo=%.4f%% | intereses/ano=%.0f EUR" % (
    media_exp, principal_pendiente, tipo_demora, intereses_anuales))
print("      el remanente del 932A paga %.2f anos de esos intereses" % out["mutualistas_estimacion"]["anios_de_remanente_que_los_paga"])

# ---------- 5. Hashes de la evidencia de hoy ----------
ev = W + "/evidencia"
hashes = {}
for f in ["mapa_cm_2026-09-29_ampliacion_medidas_iran.pdf",
          "mapa_cm_2026-09-29_texto_2026-09-30.txt",
          "ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html",
          "lgp_texto_limpio_2026-09-30.txt",
          "AEAT-cuentas-anuales-2024.pdf"]:
    p = os.path.join(ev, f)
    hashes[f] = sha256(p) if os.path.exists(p) else "AUSENTE"
out["hashes_evidencia"] = hashes
for k, v in hashes.items():
    print("EV    %s  %s" % (v[:16] + "…", k))

json.dump(out, open(ev + "/aritmetica_s21_2026-09-30.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1, sort_keys=True)
print("\n-> evidencia/aritmetica_s21_2026-09-30.json")
