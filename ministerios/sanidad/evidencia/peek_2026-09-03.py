# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"

d = json.load(open(BASE + "/evidencia/a_restituir_completas_2026-09-01.json", encoding="utf-8"))
print("TIPO:", type(d).__name__)
s = json.dumps(d, ensure_ascii=False)
print(s[:2000])
