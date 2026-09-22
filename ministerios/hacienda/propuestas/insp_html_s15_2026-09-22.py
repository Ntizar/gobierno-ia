# -*- coding: utf-8 -*-
"""Inspección del HTML BOE alrededor de la DA undécima (idx 1355335) para ver
la estructura de párrafos y localizar la DA vigésima."""
import io, sys, re, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
raw = open("ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html",
           encoding="utf-8", errors="replace").read()

i = raw.find("Disposición adicional undécima. Reclamaciones")
print("idx:", i)
print(raw[i-400:i+2500].replace("\r", ""))
print("======== busca DA vigésima (deuda aduanera) ========")
j = raw.find("Tributos integrantes de la deuda aduanera")
print("idx20:", j)
print(raw[j-300:j+300].replace("\r", ""))
