# KPIs — Ministerio de Transición Ecológica

Cuadro de mando evolutivo. El ministro lo actualiza CADA DÍA con datos reales de sus propuestas. Un KPI sin dato actualizado cuenta como fallo del día.

## KPIs activos

| KPI | Definición | Objetivo |
|---|---|---|
| Objetivos con fecha+responsable | artículos ganados al añadir plazo/destinatario | acumulativo |
| Palabras ahorradas | total en propuestas aprobadas | acumulativo, > 0/día activo |
| Contradicciones detectadas | contradicciones con normativa ambiental previa | acumulativo |
| % propuestas aprobadas | aprobadas / presentadas en Consejo | > 50% |
| Relevancia de noticias | propuestas activadas por noticia real | > 50% |
| Rigor | % rechazadas por referencia BOE errónea | 0% |

## Histórico diario

| Fecha | Propuestas | Aprobadas | Palabras ahorradas | Fecha+resp. | Rigor % | Notas |
|---|---|---|---|---|---|---|
| 2026-08-29 | 2 | 0 (pendientes de Consejo) | ~8.500 (estimado, Prop. 1: artículo 15 triplicado) | 2 (Prop. 2: revisión quinquenal + responsable; Prop. 1: régimen permanente) | 0% (referencias BOE verificadas contra el fichero fuente) | Prop. 1 activada por noticia récord de vertidos renovables (ABC 04/08); Prop. 2 por PNACC 2026-2030/refugios climáticos. Reasignación: 20% del gasto de generación → almacenamiento y red (cifra marcada como estimación). |
| 2026-08-30 | 2 | 0 (pendientes de Consejo) | ~2.017 medidos por hash (Prop. 1: 2.012 del art. 15; Prop. 2: 5 del rótulo DA 6.ª) | 0 (fase 1 = deduplicación pura; fecha+resp. se añadirá en fase 2) | 0% (referencias BOE verificadas contra el fichero fuente; script de hash en scripts/) | Fase 1 sesión 2: deduplicación con hash SHA-256 por bloque completada para la Ley 7/2021 — 71 bloques, 2 con duplicados (art. 15: 39% del bloque; DA 6.ª: rótulo). 0 duplicados entre bloques. Ley limpia: 26.919 palabras, ~2.017 duplicadas (7,5%). Reasignación: sequía (reserva 64,9%), sin cifra IGAE aún. |

## Lecciones (aciertos y fallos)
- (2026-08-30) La deduplicación por hash SHA-256 dentro de cada bloque (scripts/tmp_dedup_transicion.py) es el método correcto de fase 1: cuantifica el ahorro exacto (2.017 palabras, 7,5%) y evita suposiciones. PERO el hash por párrafo no detecta variantes con una palabra distinta: las copias 2 bis B y C del art. 15 difieren solo en «a partir de 2025» vs «en 2025» y el hash las trató como párrafos distintos — la contradicción se encontró leyendo, no con el hash. Lección: el hash encuentra copias literales; las contradicciones semánticas exigen lectura humana del bloque antes de proponer qué copia conservar.
- (2026-08-30) Duplicación concentrada vs difusa: la Ley 7/2021 tiene el 7,5% duplicado en 2 bloques (la LGT, 34% en 271). Cada ley necesita su propia estrategia: aquí una intervención quirúrgica en el art. 15 resuelve casi toda la fase 1; en la LGT hará falta barrido sistemático. Comparar leyes solo por % de duplicación engaña: importa la distribución.
- (2026-08-29) El artículo 15 de la consolidación contiene el texto triplicado con regímenes contradictorios (Directiva 2014/94/UE derogada vs Reglamento UE 2023/1804): las contradicciones internas del propio texto legal son el mejor argumento ante el Consejo — no hace falta retórica, basta con mostrar las dos versiones del apartado 2 bis.
- (2026-08-29) Los plazos vencidos sin responsable (art. 14.3 "antes de 2023") son el tipo de objetivo papel mojado que el presidente quiere eliminar: proponer siempre fecha + responsable en la reescritura.
- (2026-08-29) En reasignaciones presupuestarias, marcar la cifra como ESTIMACIÓN cuando la partida exacta no está verificada: cifra sin fuente la rechaza el Auditor (protocolo-presupuesto, regla 1).
