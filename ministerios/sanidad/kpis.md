# KPIs — Ministerio de Sanidad

Cuadro de mando evolutivo. El ministro lo actualiza CADA DÍA con datos reales de sus propuestas. Un KPI sin dato actualizado cuenta como fallo del día.

## KPIs activos

| KPI | Definición | Objetivo |
|---|---|---|
| Palabras ahorradas | total en propuestas aprobadas | acumulativo, > 0/día activo |
| Índice de obsolescencia | artículos desactualizados detectados / total revisados | tracking |
| % propuestas aprobadas | aprobadas / presentadas en Consejo | > 50% |
| Solapes detectados | solapes con otras normas sanitarias | acumulativo |
| Relevancia de noticias | propuestas activadas por noticia real | > 50% |
| Rigor | % rechazadas por referencia BOE errónea | 0% |

## Histórico diario

| Fecha | Propuestas | Aprobadas | Palabras ahorradas | Obsolescencia | Rigor % | Notas |
|---|---|---|---|---|---|---|
| 2026-08-29 | 2 (arts. 36 y 96.2) | pendiente Consejo 22:00 | ~60 (si se aprueban) | 13 bloques duplicados + 3 erratas detectados en ley insignia | 0 (todas las citas verificadas contra el fichero fuente) | Activadas por noticias reales: crisis Ceuta (art. 26/38 como marco), IPC sanitario +1,9% (art. 36), gasto farmacéutico (reasignación) |
| 2026-08-30 | 2 (arts. 10 y 47, fase 1 deduplicación) | pendiente Consejo 22:00 | ~855 (si se aprueban) | Escaneo hash completo: 109 bloques, 21 duplicados, ~3.314 palabras muertas (inventario en propuesta del día) | 0 (bloques verificados por SHA-256 contra el fichero fuente; informe dedup_informe_2026-08-30.json) | Noticia dominante: Nilo Occidental en Canarias + Ceuta día 30 + protesta quirúrgica en 7 CCAA (activa art. 47). 100% de propuestas activadas por noticia real |
| 2026-08-31 | 2 ([adieciocho] y [atreintaycinco], fase 1 deduplicación) | pendiente Consejo 22:00 | ~1.109 (si se aprueban; acumulado propuesto 3 sesiones: ~2.015) | Reejecución dedup_scan.py: invariante 21/109 bloques, 3.314 palabras (propuestas aún no aplicadas al fichero). Hoy atacados los 2 mayores: art. 18 (817 dup.) y art. 35 (292 dup.) | 0 (ambos bloques re-leídos íntegros y verificados contra el fichero fuente antes de citar texto) | Noticias activadoras: Reglamento UE 2026/1818 (microchip perros/gatos, en vigor 30-08), oferta 12.850 plazas FSE 2027 (Ministerio 10-08), decreto de guardias MIR 17 h (20minutos), Ceuta día 31 con refuerzo a 3 meses, intrusismo profesional (activa el 5.ª reformado del art. 35). 100% activadas por noticia real |

## Lecciones (aciertos y fallos)
- (el ministro anota aquí qué estrategias de persuasión funcionan en el Consejo y cuáles no)
- 2026-08-29 (primer día): mejor 1 propuesta buena que 3 vagas — hoy van 2: una de peso (doble escala sancionadora pesetas/euros, fácil de defender) y una quirúrgica (errata «revocada», coste cero). Estrategia de persuasión prevista: anclar la P1 en seguridad jurídica para el ciudadano, no en estética normativa.
- La ley insignia acumula ~13 bloques con versiones duplicadas apiladas ([atres], [aseis], [adiez], [adieciocho], [adiecinueve], [aveintiuno], [aveintidos], [acuarentaysiete], [aochentaynueve], [aochentaydos], [aochentaycuatro], [aciento], [acientodos], [acientocinco]). Plan: una depuración por día, priorizando bloques con efecto jurídico (36, 47, 79) sobre los cosméticos.
- Noticia dominante del día: Ceuta. El marco legal aplicable (arts. 26 y 38 de la propia ley) está vigente pero de 1986; vigilar el debate sobre confinamientos sin cribado previo «sin amparo legal» para una futura propuesta frase por frase.
- 2026-08-30 (sesión 2/30, fase 1): el método hash/diff (SHA-256 por párrafo, script `propuestas/dedup_scan.py`) convierte la deduplicación en evidencia medible: 21 bloques duplicados de 109, ~3.314 palabras — ya no se discute «parece duplicado», se muestra el número. Lección operativa: la aprobación de la sesión 1 sugería 13 bloques; el escaneo exhaustivo encuentra 21 (incluye cabeceras repetidas y el 5.º de [acuarentaysiete] derogado); el método common improve, no sustituye, el juicio jurídico.
- 2026-08-30: estrategia de persuasión para hoy — P1 (art. 10) se defiende en clave ciudadana («el paciente no debe adivinar qué catálogo de derechos manda») y P2 (art. 47) en clave de crisis activa (Ceuta + protesta de cirujanos + Nilo Occidental = todo se coordina en el Consejo Interterritorial). Anclar en casos reales, no en estética normativa.
- 2026-08-30: la noticia de Nilo Occidental en Canarias activa la reasignación presupuestaria (vigilancia entomológica reactiva → preventiva); los indicadores medibles a 90 días van ya redactados en la propuesta para sobrevivir al Auditor.
- 2026-08-31 (sesión 3/30, fase 1): lección de ponderación — atacar SIEMPRE primero el bloque mayor duplicado ([adieciocho], 817 palabras) rinde más que repartir esfuerzo: hoy van 1.109 palabras propuestas en un solo día, 57% del total acumulado. Estrategia de persuasión prevista: P1 anclada en el corazón operativo de la ley (los arts. 18.5, 18.14 y 18.12 son la base de las reasignaciones y noticias del propio Consejo — «el catálogo que justifica el gasto debe ser uno y el vigente»); P2 anclada en seguridad jurídica sancionadora (5.ª del art. 35: diferencia REAL, no cosmética — delimita quién puede requerir colaboración, y el intrusismo profesional está en agenda desde marzo).
- 2026-08-31: descubrimiento de la sesión — el art. 35 tiene numeración sin 1.ª y sin encabezados de sección («Leves/Graves/Muy graves») en el BOE consolidado. Anotado en la propuesta como candidata a la fase 2 (no se toca hoy: fase 1 solo deduplica). Este tipo de hallazgo «gratis» al re-leer bloques íntegros es valor adicional del método hash.
- 2026-08-31: lección de rigor — reejecutar dedup_scan.py cada sesión antes de proponer: hoy confirma invariante (21/109, 3.314) que valida que las propuestas anteriores no se han aplicado aún; si el Consejo las aprueba, la reejecución mañana debe BAJAR — es el test automático de que los diffs se aplican.
