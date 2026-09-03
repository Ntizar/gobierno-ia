# -*- coding: utf-8 -*-
# quita la linea en blanco que rompe la tabla entre la fila 09-01 y la 09-03
p = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad/kpis.md"
t = open(p, encoding="utf-8", newline="").read()
t = t.replace("fecha de efectos |\r\n\r\n| 2026-09-03", "fecha de efectos |\r\n| 2026-09-03")
t = t.replace("fecha de efectos |\n\n| 2026-09-03", "fecha de efectos |\n| 2026-09-03")
open(p, "w", encoding="utf-8", newline="").write(t)
print("OK, filas consecutivas:", "fecha de efectos |\n| 2026-09-03" in t.replace("\r\n","\n"))
