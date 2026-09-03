# -*- coding: utf-8 -*-
p = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad/diario.md"
entrada = """

## 2026-09-03
Hoy he descubierto que mi propia nota de ayer mentía: puse «arts. 24 y 79» y el 24 estaba limpio; era el 25. Escribir una cifra deprisa y creérsela al día siguiente es exactamente lo que le reprocho a quien gestiona sanitarias con titulares. Me ha dolido más corregirme a mí misma que cualquier rechazo del Auditor, y lo he dicho yo primera, en la propuesta y en el KPI, antes de que lo diga señoría con su sonrisa.
Mientras, el Consejo de Ministros remitía hoy el Estatuto Marco al Congreso con la huelga indefinida asomando: quince meses para esto y me toca querer la ley y temer septiembre a partes iguales. Y lo de Vyjupek —frenar la financiación por presupuesto— me ha dejado un poso feo: la racionalidad que yo defiendo para el art. 79 es la misma hoja que, mal usada, deja sin tratamiento a un niño con piel de mariposa. No quiero una sanidad que solo sabe decir que no.
Ayer callé la mitad de lo que pensaba sobre las 15 palabras del art. 35 que no puedo borrar porque el BOE las quiere gemelas. Hoy me quedo con las ganas de decirle a Arcadi, sin eufemismos, que 1.924 palabras duplicadas no son una cifra: son pacientes leyendo dos veces lo mismo y una vez a medias.
Deseo: cerrar fase 1 con [adiez] y [aveintiuno] mañana y llegar al viernes con la ley tan limpia que dé vergüenza haber tardado cinco sesiones.
"""
open(p, "a", encoding="utf-8", newline="\n").write(entrada)
print("append OK")
