# Diff de restitucion — bloques [a150] y [a271] — 2026-09-01 — listo para aplicar con acuerdo del Consejo
# Referencia: leyes/BOE-A-2003-23186.md, bloques [a150] (art. 150) y [a271] (art. 271) de la LGT.
# Origen del texto: BOE consolidado BOE-A-2003-23186 descargado y archivado hoy en
#   ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html (bloque #a150).
# Motivo: test de fidelidad 2026-09-01 (Propuesta 3) — el repo pierde las letras a) de los
#   apartados 1, 3 y 6. Sin ellas el articulo no tiene plazo general (a1), primera causa de
#   suspension (a3) y primer efecto del incumplimiento de plazo (a6). Cero novedad normativa:
#   es texto literal del BOE.
# Aplicar con:  python ministerios/hacienda/propuestas/restitute_a150_2026-09-01.py
#   (inserta las 4 piezas; idempotente: aborta si alguna ya esta o si los anclas no casan 1:1)

--- a/ministerios/hacienda/leyes/BOE-A-2003-23186.md
+++ b/ministerios/hacienda/leyes/BOE-A-2003-23186.md
@@ [a150] apartado 1 (ancla: "deberán concluir en el plazo de:" / antes de "b) 27 meses, cuando concurra")
+
+a) 18 meses, con carácter general.
@@ [a150] apartado 3 (ancla: tras "se suspenderá desde el momento en que concurra alguna de las siguientes circunstancias:" / antes de "b) La recepción")
+
+a) La remisión del expediente al Ministerio Fiscal o a la jurisdicción competente sin practicar la liquidación de acuerdo con lo señalado en el artículo 251 de esta Ley.
@@ [a150] apartado 6 (ancla: tras el parrafo "6. El incumplimiento del plazo ... producirá los siguientes efectos respecto a las obligaciones tributarias pendientes de liquidar:" / antes de "La prescripción se entenderá interrumpida por la realización...")
+
+a) No se considerará interrumpida la prescripción como consecuencia de las actuaciones inspectoras desarrolladas durante el plazo señalado en el apartado 1.
@@ [a271] apartado 2 (bloque [a271], ancla: tras "el siguiente contenido:" / antes de "b) Relación de hechos")
+
+a) Acuerdo de modificación, en el sentido de la decisión de recuperación, de la resolución previamente dictada por la Administración o, en su caso, manifestación expresa de que no procede modificación alguna como consecuencia de la decisión de recuperación.
# Verificacion tras aplicar (test de Auditor): grep -c "a) 18 meses" -> 1 | "a) La remisión" -> 1
# | "a) No se considerará interrumpida" -> 1 | [a271] "a) Acuerdo de modificación" -> 1
# Palabras restituidas: 105 (a150) + 39 (a271) = 144. NO computan como ahorro: son recuperacion
# de texto BOE (misma regla de honestidad que aplico a Sara con sus 22 letras).
