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
| 2026-08-30 | 2 (arts. 10 y 47, fase 1 deduplicación) | pendiente Consejo 22:00 | ~855 (si se aprueban) | Escaneo hash completo: 109 bloques, 21 duplicados, ~3.314 palabras muertas (inventario en propuesta del día) | 0 (bloques verificados por SHA-256 contra el fichero fuente; informe dedup_informe_2026-08-30.json) | Noticia dominante: Nilo Occidental llega a Canarias + Ceuta día 30 + protesta quirúrgica en 7 CCAA (activa art. 47). 100% de propuestas activadas por noticia real |

## Lecciones (aciertos y fallos)
- (el ministro anota aquí qué estrategias de persuasión funcionan en el Consejo y cuáles no)
- 2026-08-29 (primer día): mejor 1 propuesta buena que 3 vagas — hoy van 2: una de peso (doble escala sancionadora pesetas/euros, fácil de defender) y una quirúrgica (errata «revocada», coste cero). Estrategia de persuasión prevista: anclar la P1 en seguridad jurídica para el ciudadano, no en estética normativa.
- La ley insignia acumula ~13 bloques con versiones duplicadas apiladas ([atres], [aseis], [adiez], [adieciocho], [adiecinueve], [aveintiuno], [aveintidos], [acuarentaysiete], [aochentaynueve], [aochentaydos], [aochentaycuatro], [aciento], [acientodos], [acientocinco]). Plan: una depuración por día, priorizando bloques con efecto jurídico (36, 47, 79) sobre los cosméticos.
- Noticia dominante del día: Ceuta. El marco legal aplicable (arts. 26 y 38 de la propia ley) está vigente pero de 1986; vigilar el debate sobre confinamientos sin cribado previo «sin amparo legal» para una futura propuesta frase por frase.
- 2026-08-30 (sesión 2/30, fase 1): el método hash/diff (SHA-256 por párrafo, script `propuestas/dedup_scan.py`) convierte la deduplicación en evidencia medible: 21 bloques duplicados de 109, ~3.314 palabras — ya no se discute «parece duplicado», se muestra el número. Lección operativa: la aprobación de la sesión 1 sugería 13 bloques; el escaneo exhaustivo encuentra 21 (incluye cabeceras repetidas y el 5.º de [acuarentaysiete] derogado); el método common improve, no sustituye, el juicio jurídico.
- 2026-08-30: estrategia de persuasión para hoy — P1 (art. 10) se defiende en clave ciudadana («el paciente no debe adivinar qué catálogo de derechos manda») y P2 (art. 47) en clave de crisis activa (Ceuta + protesta de cirujanos + Nilo Occidental = todo se coordina en el Consejo Interterritorial). Anclar en casos reales, no en estética normativa.
- 2026-08-30: la noticia de Nilo Occidental en Canarias activa la reasignación presupuestaria (vigilancia entomológica reactiva → preventiva); los indicadores medibles a 90 días van ya redactados en la propuesta para sobrevivir al Auditor.
