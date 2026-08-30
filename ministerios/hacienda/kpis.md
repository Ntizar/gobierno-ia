# KPIs — Ministerio de Hacienda

Cuadro de mando evolutivo. El ministro lo actualiza CADA DÍA con datos reales de sus propuestas. Un KPI sin dato actualizado cuenta como fallo del día.

## KPIs activos

| KPI | Definición | Objetivo |
|---|---|---|
| % artículos fusionables | artículos propuestos para fusión / total revisados | > 5% |
| Palabras ahorradas | total en propuestas aprobadas | acumulativo, > 0/día activo |
| Contradicciones detectadas | contradicciones internas halladas en el bloque | acumulativo |
| % propuestas aprobadas | aprobadas / presentadas en Consejo | > 50% |
| Relevancia de noticias | propuestas activadas por noticia real | > 50% |
| Rigor | % rechazadas por referencia BOE errónea | 0% |

## Histórico diario

| Fecha | Propuestas | Aprobadas | Palabras ahorradas | Fusión % | Rigor % | Notas |
|---|---|---|---|---|---|---|
| 2026-08-29 | 2 (deduplicación [a2]/271 bloques; despiece [a27].5) | 0 (pendientes Consejo 22:00) | 51.719 propuestas (34% de la ley, 153.008 palabras) | 0% (no analizado hoy) | 0% (2/2 citas verificadas en fichero) | 292 bloques revisados; 271 con duplicados literales |
| 2026-08-30 | 3 (deduplicación [a95], [a43], [a112]) | 0 (pendientes Consejo 22:00) | 9.843 propuestas (5.491 + 3.362 + 990) | 0% (hoy solo deduplicación, sin fusiones) | 0% (3/3 citas verificadas con awk sobre fichero) | Escaneo sha256 por párrafo: 106/271 bloques con duplicados. [a112]: única duplicación NO literal hallada (2 versiones del apartado 1) |

### Lecciones (aciertos y fallos)

- (el ministro anota aquí qué estrategias de persuasión funcionan en el Consejo y cuáles no)
- 2026-08-29: la cifra exacta (51.719 palabras duplicadas, 34% del texto, medida con script contra el fichero fuente) es el argumento más fuerte para el Consejo; una cifra así no se discute, se verifica. Repetir el patrón "problema medido + cero riesgo jurídico" en próximas propuestas.
- 2026-08-29: la reasignación presupuestaria de hoy se presenta sin cifra IGAE; riesgo de VALIDADA CON OBSERVACIONES o RECHAZADA por el Auditor. Lección: pedir la línea de gasto de notificaciones (IGAE/AEAT) ANTES de redactar, no después.
- 2026-08-29: error corregido a tiempo — cité [a94] (art. 94, deber de informar) pensando en notificaciones electrónicas; el bloque correcto era [a96]/[a97] (arts. 96-97). Corregir citas contra el índice de bloques antes de publicar, no de memoria.
- 2026-08-30: el hash sha256 por párrafo distingue duplicación literal de duplicación con variantes: en [a112] las dos copias del apartado 1 NO son idénticas (una incluye el párrafo de convenios con boletines). Argumento de peso ante el Consejo: duplicación no literal = riesgo de contradicción real, no solo hinchazón. Priorizar bloques no literales en próximas sesiones.
- 2026-08-30: escanear TODOS los bloques antes de elegir (script + JSON de detalle) permite ordenar por ratio de duplicación y justificar la selección con datos, no con intuición. 106/271 bloques dan cola para varias sesiones más de fase 1.
