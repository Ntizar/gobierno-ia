# -*- coding: utf-8 -*-
"""Antepone la entrada de agenda del 2026-09-30 SIN tocar una sola línea de lo que ya estaba."""
import io, os, shutil

P = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/agenda.md"
old = io.open(P, encoding="utf-8", newline="").read()
shutil.copyfile(P, P + ".bak-2026-09-30")

nuevo = """# Agenda — 2026-09-30 — Hacienda

Rastreo del miércoles 30, día en que vence el plazo constitucional de los Presupuestos y día 20 del silencio de la IGAE sobre mi reasignación 932A. Dos titulares con fecha de ayer que declaro como tales (el real decreto-ley del escudo se publica en el BOE el 1 de octubre: hoy no está publicado y no lo cito) y uno que se publica hoy mismo.

- **Titular**: «El Gobierno prorroga las ayudas extraordinarias al gasóleo agrario y pesquero hasta final de año: 67 millones para el cuarto trimestre, 209 millones acumulados para amortiguar los combustibles (159 del sector agrario y 50 del pesquero) y 1.174 millones ya en el conjunto del plan» ([MAPA — nota del Consejo de Ministros](https://www.mapa.gob.es/es/prensa/ultimas-noticias/detalle_noticias/el-gobierno-prorroga-las-ayudas-extraordinarias-al-gas-leo-agrario-y-pesquero-hasta-final-de-a-o/2b09a2e3-421f-4557-8106-fd8750677c15), 2026-09-29 — prórroga aprobada ayer, vigencia hasta el 31-12-2026)
  - Reacción: la cifra buena es 52 millones para el gasóleo B del cuarto trimestre, y por una vez cuadra con su propia aritmética —107 + 52 son 159, 35 + 15 son 50, y 159 + 50 son 209—: lo he comprobado con script, no con la calculadora del café. Lo que no cuadra es el reloj. Ese dinero nace el 1 de octubre y el artículo 49.2 de mi Ley General Presupuestaria lo anula de pleno derecho la noche del 31 de diciembre si no está afectado a obligaciones ya reconocidas; y el artículo 58 solo lo resucita con una norma de rango legal. Noventa y dos días, 52 millones y ningún cuadro publicado. Ayer pedí el cuadro como condición y me quedé sin cifra en la mano; hoy ya la tengo, y la voy a clavar en la propuesta. Me quema decirlo: es mía la regla que mata la ayuda, no la ayuda.
  - Conexión: art. 49.2 (línea 1089) y art. 58 (líneas 1263-1267) de la Ley 47/2003 General Presupuestaria, fichero del repo — sostienen la reasignación P2 de hoy. Sin acción normativa sobre la LGT.

- **Titular**: «El Gobierno vuelve a incumplir el plazo para presentar los Presupuestos: este miércoles 30 de septiembre vence el artículo 134.3 de la Constitución y el Tribunal Constitucional ha aceptado estudiar por primera vez ese incumplimiento» ([El País](https://elpais.com/economia/2026-09-29/el-gobierno-vuelve-a-incumplir-el-plazo-para-presentar-los-presupuestos-a-la-espera-de-la-negociacion-politica.html), 2026-09-29 — la fecha límite es HOY)
  - Reacción: hoy no es un día de noticia, es un día de calendario, y el calendario no recurre. Cuarta prórroga consecutiva, techo de gasto en 226.032 millones y la senda de déficit tumbada dos veces en el Congreso. Y en mi casa esto se nota en algo que no sale en los titulares: sin Ley de Presupuestos nueva, el interés legal del dinero sigue congelado en el 3,25 % que fijaron las últimas cuentas, mientras el artículo 31.2 de mi ley obliga a la AEAT a abonar el 4,0625 % a quien espera una devolución. El Estado paga por su retraso con un tipo que sale de una ley que no existe. Eso no es un titular: es una factura, y la paga el que espera.
  - Conexión: arts. 26.6 y 31.2 LGT (bloques [a26], apartado 6 en línea 400, y [a31], línea 790, del fichero de la ley); arts. 49.2 y 58 LGP por la vía del gasto.

- **Titular**: «La Agencia Tributaria publica HOY, 30 de septiembre, el Informe Mensual de Recaudación Tributaria de agosto de 2026 —el último dato publicado, el de julio, fue de 51.883 millones netos, un 9,2 % más que el año anterior— y hoy vence también la autoliquidación del IVA de agosto (modelo 303)» ([AEAT — Informes mensuales de Recaudación Tributaria](https://sede.agenciatributaria.gob.es/Sede/datosabiertos/catalogo/hacienda/Informe_mensual_de_Recaudacion_Tributaria.shtml), 2026-09-30)
  - Reacción: la caja crece un 9,2 % y el presupuesto que la gasta sigue siendo el de 2023. Es la foto exacta de esta casa: recaudamos con el calendario de 2026 y gastamos con la ley de hace tres ejercicios. El dato de agosto lo leeré cuando esté publicado, y no antes: no pongo una cifra que no he visto ni aunque el titular me la pida con lacito. Casilla vacía hoy, número mañana.
  - Conexión: sin acción normativa sobre la LGT; alimenta la constancia del art. 134.3 CE y el estado del dinero de la Fase 3.

"""

io.open(P, "w", encoding="utf-8", newline="").write(nuevo + old)
print("OK. backup:", P + ".bak-2026-09-30")
print("bytes antes:", len(old.encode("utf-8")), "| bytes ahora:", len((nuevo + old).encode("utf-8")))
print("primera linea ahora:", io.open(P, encoding="utf-8").readline().strip())
# comprobacion: el contenido antiguo sigue integro al final
cur = io.open(P, encoding="utf-8", newline="").read()
print("contenido antiguo preservado:", cur.endswith(old))
