#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Aritmetica de la sesion 20/30 (2026-09-29). Todo con fuente declarada."""
from decimal import Decimal as D

print("### A) Tipo de interes de demora (art. 26.6 LGT: interes legal + 25 %) ###")
legal = D("3.25")
tipo = legal * D("1.25")
print("  3,25 %% x 1,25 = %s %%  == 4,0625 %% ?  %s" % (tipo, tipo == D("4.0625")))

print()
print("### B) Programa 932A (AEAT), Cuentas Anuales 2024, E.I gastos ###")
c3 = D("1817977437.08"); c5 = D("1776913651.22")
print("  credito definitivo      : %s EUR  = %.2f M EUR" % (f"{c3:,.2f}", c3 / 10**6))
print("  obligaciones reconocidas: %s EUR  = %.2f M EUR" % (f"{c5:,.2f}", c5 / 10**6))
print("  remanente (resta)       : %s EUR  = %.2f M EUR" % (f"{c3-c5:,.2f}", (c3 - c5) / 10**6))
print("  == fila TOTAL 41.063.785,86 ?  %s" % ((c3 - c5) == D("41063785.86")))

print()
print("### C) Mutualistas: coste del silencio (ESTIMACION, metodo declarado) ###")
abonado = D("3500") * 10**6      # EUR abonados en tres ejercicios (ABC 19-05-2026)
exped = D("2.5") * 10**6         # expedientes analizados (ABC 19-05-2026)
medio = abonado / exped
print("  media por expediente = 3.500.000.000 EUR / 2.500.000 exp = %s EUR/expediente" % f"{medio:,.0f}")
principal = D("90717") * medio
print("  90.717 expedientes x %s EUR = %s EUR = %.1f M EUR" % (f"{medio:,.0f}", f"{principal:,.0f}", principal / 10**6))
interes = principal * D("0.040625")
print("  al 4,0625 %% anual = %s EUR/ano = %.2f M EUR/ano" % (f"{interes:,.0f}", interes / 10**6))
print("  proporcionado a 6 meses = %.2f M EUR" % (interes / 2 / 10**6))
print("  lote 41,06 M EUR del 932A / coste anual del silencio = %.2f anos de intereses" % ((c3 - c5) / interes))

print()
print("### D) Escudo: litros implicados por la subvencion de 20 c/L ###")
bolsa = D("65000000"); tipo_l = D("0.20")
litros = bolsa / tipo_l
print("  65.000.000 EUR / 0,20 EUR/L = %s litros = %.0f M litros/trimestre" % (f"{litros:,.0f}", litros / 10**6))
print("  DERIVADA. Limites: supone que toda la bolsa va a 20 c/L y a ese tipo todo el trimestre.")

print()
print("### E) Contrastes de cabecera ###")
print("  41,1 M EUR (expediente) vs 41,06 M EUR (documento) -> dif %.0f EUR" % (D("41100000") - (c3 - c5)))
print("  1.818,0 M EUR (expediente) vs 1.817,98 M EUR (documento) -> dif %.0f EUR" % (D("1818000000") - c3))
