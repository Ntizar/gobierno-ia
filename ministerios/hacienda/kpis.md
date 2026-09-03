# KPIs — Ministerio de Hacienda

Cuadro de mando evolutivo. El ministro lo actualiza CADA DÍA con datos reales de sus propuestas. Un KPI sin dato actualizado cuenta como fallo del día.

> **Renombrado del 2026-09-01 (mandato del Auditor, auditoría 31-08)**: la columna «Palabras ahorradas» medía promesas de propuestas, no logros. Se divide en dos: **EJECUTADAS** (palabras suprimidas del fichero de ley por diffs aplicados, con manifiesto hash y backup) y **PROPUESTAS** (las que esperan al Consejo). Lo que cuenta como logro es solo EJECUTADAS. Convención de denominador fijada hoy: **335 bloques por encabezado real** (271 artículos numéricos + 64 no numéricos) — todas las tasas desde hoy son comparables.

## KPIs activos

| KPI | Definición | Objetivo |
|---|---|---|
| % artículos fusionables | artículos propuestos para fusión / total revisados | > 5% |
| Palabras ahorradas EJECUTADAS | suprimidas del fichero por diff aplicado (manifiesto hash) | acumulativo, > 0/día desde hoy |
| Palabras propuestas (no logro) | en propuestas pendientes de Consejo | informativo |
| Contradicciones detectadas | contradicciones internas halladas en el bloque | acumulativo |
| % propuestas aprobadas | aprobadas / presentadas en Consejo | > 50% |
| Relevancia de noticias | propuestas activadas por noticia real | > 50% |
| Rigor | % rechazadas por referencia BOE errónea | 0% |
| Fidelidad BOE | % de diffs propuestos contrastados contra BOE consolidado archivado | 100% |

## Histórico diario

| Fecha | Propuestas | Aprobadas | Palabras EJECUTADAS (diff aplicado) | Palabras propuestas | Fusión % | Rigor % | Notas |
|---|---|---|---|---|---|---|---|
| 2026-08-29 | 2 (deduplicación [a2]/271 bloques; despiece [a27].5) | 0 (pendientes Consejo 22:00) | 0 | 51.719 (34% de la ley, 153.008 palabras) | 0% (no analizado hoy) | 0% (2/2 citas verificadas en fichero) | 292 bloques revisados; 271 con duplicados literales. Denominador aún no declarado. |
| 2026-08-30 | 3 (deduplicación [a95], [a43], [a112]) | 0 (pendientes Consejo 22:00) | 0 | 9.843 (5.491 + 3.362 + 990) | 0% (hoy solo deduplicación, sin fusiones) | 0% (3/3 citas verificadas con awk sobre fichero) | Escaneo sha256 por párrafo: 106/271 bloques con duplicados. [a112]: duplicación NO literal (2 versiones del apartado 1) |
| 2026-08-31 | 2 ([a271] DA 5ª y resto de DA; unificación [a150]) + reasignación con cifra AEAT | 0 (pendientes Consejo 22:00) | 0 | 8.570 (5.613 + 2.957) | 0% | 0% (2/2 citas verificadas; cifra AEAT 148.944 M€ verificada antes de redactar) | [a271]: referencia mal identificada — corregida hoy (ver 09-01). [a150]: primera contradicción interna plena. RECHAZO Auditor: reasignación sin euros. |
| 2026-09-01 | 0 nuevas de deduplicación; 1 restitución ([a150]+[a271], lista para aplicar); test de fidelidad con hallazgo; reasignación con programa y euros | — (Consejo 22:00) | **9.265** (5.624 en 8 DAs + 3.641 en [a150]; manifiesto hash + backup .bak-2026-09-01) | 144 (restitución BOE, no computan como ahorro) | 0% | **1 referencia BOE errónea propia, autorregulada y corregida hoy** ([a271] → DAs, con manifiesto por hash) | Primera pasada de diffs del ministerio sobre el fichero. Test reejecución: dup totales 115→106 bloques, 52.652→44.071 palabras (convención 335). Test fidelidad: **139 letras BOE ausentes** (~3.805 palabras) — defecto de conversión confirmado. Reasignación: programa 932A, 41,1 M€ (origen: resta verificada Memoria AEAT 2024: 1.818,0−1.776,9) → 24,7 + 16,4 M€. |
| 2026-09-02 | 1 (reparación [dadecimoctava], P-1) + entrega del manifiesto masivo (P-2, no nueva: cierre del acuerdo 13) + comprobación 932A (P-3) | — (Consejo 22:00, cierra Fase 1) | **0 nuevas** (a12 aprendido: verificado ≠ ejecutado — el diff de la DA18 está firmado, hasheado y listo, esperando mandato expreso en sala) | 847 (reparación DA18, registradas como **fidelidad**, no como ahorro) + 44.071 dup (D1 en manifiesto, sigue siendo debe) + 2.998 F1 (103 marcas siguen ausentes) | 0% (hoy: fidelidad, no fusiones) | 0% (todas las citas verificadas con doble testigo BOE: archivado 09-01 sha b29db001… y vivo 09-02 sha a2f3fe1f…, idénticos) | **Manifiesto masivo ejecutado sobre 335 bloques** (evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json, sha 332d8fe2…), tras firma de la taxonomía 12:09:27 (evidencia/TAXONOMIA_LGT_FIRMADA_2026-09-02.md) — orden literal del acuerdo 13. Cifra cuadrada del orden del día presidencial: 161 casos / 76 bloques F1 (no 139/84: 139 = marcas; 84 = bloques con cualquier defecto; 77 = bloques tocados por el test — tres denominadores, cada uno con su nombre). **Hallazgo X1**: la grieta DA18 no eran 250 palabras duplicadas sino **939 palabras sin traza en ningún BOE** (17 párrafos de tres leyes distintas + título que dice «criptoactivos» cuando el BOE dice «extranjero»). Reverificación: 32 restituciones del 09-01 presentes, 103 F1 siguen ausentes. 932A: sin dictamen IGAE en el repo a 09-02, condición vence 11-09, hoy no tocaba. Fichero de ley intacto (git diff limpio). |

### Lecciones (aciertos y fallos)

- (el ministro anota aquí qué estrategias de persuasión funcionan en el Consejo y cuáles no)
- 2026-08-29: la cifra exacta medida con script contra el fichero fuente es el argumento más fuerte para el Consejo; una cifra así no se discute, se verifica.
- 2026-08-29: reasignación sin cifra IGAE = puerta a RECHAZO. Pedir la línea de gasto ANTES de redactar.
- 2026-08-29: corregir citas contra el índice de bloques antes de publicar, no de memoria ([a94]→[a96]/[a97]).
- 2026-08-30: el sha256 por párrafo distingue duplicación literal de duplicación con variantes; las no literales son riesgo de contradicción, no de hinchazón. Priorizarlas.
- 2026-08-30: escanear TODOS los bloques antes de elegir permite ordenar por ratio y justificar con datos.
- 2026-08-31: el hash solo detecta copias literales: las dos redacciones del art. 150 se descubrieron leyendo grupos de hash, no el agregado. El argumento «contradicción interna» pesa más que el volumen.
- 2026-08-31: cifra verificada ANTES de redactar la reasignación (AEAT 148.944 M€) blindó la propuesta contra la regla 1 — pero no contra la 4: diagnóstico sin dosis sigue siendo rechazo. **Confirmado empíricamente: «cifra base» no es «cifra de reasignación»; el Auditor exige de-X→a-Y con partida nombrada. Nunca más una sin la otra.**
- 2026-08-31: proponer desduplicación por bloque mixto ([a271]) sin desglosar en manifiesto por DA invitaba al artefacto de regex. **Lección cara**: el regex que corta solo por `## [aN]` numérico es un arma de destrucción masiva de la identificación. Desde hoy: `re.split` por TODOS los encabezados y denominador declarado (335).
- 2026-09-01: **aplicar el diff el mismo día de la corrección**, con backup, manifiesto hash y test de reejecución, convierte una corrección del Auditor en un cumplimiento verificable. El Consejo de hoy no vota promesas: vota un número que ya bajó.
- 2026-09-01: el contraste contra el BOE descargado **antes** de cerrar un bloque revela lo que el hash no ve: deduplicar [a150] sin mirar el BOE habría dejado un art. 150 sin plazo general. **El manifiesto hash es condición necesaria, no suficiente: sin test de fidelidad, Fase 1 certifica copias infieles.**
- 2026-09-01: archivar la evidencia en el repo (`ministerios/hacienda/evidencia/`) el mismo día en que se genera — la cadena de custodia en Temp no sobrevive a un Consejo.
- 2026-09-01: una columna de KPIs que mide promesas se convierte, sin querer, en un ministerio de promesas. Renombrar y separar ejecutadas/propuestas hoy: 9.265 ejecutadas pesan más que 12.208 anunciadas.
- 2026-09-02: **contrastar contra DOS ejemplares del BOE con un día de distancia** (archivado 09-01 y vivo 09-02) convierte una sospecha en prueba: si un texto no está en ninguno, no es norma intermedia, es invención de la conversión. El sha256 por párrafo con match normalizado es el detector; la lectura humana (título que dice «criptoactivos» en una disposición de «extranjero») es el que te avisa de dónde mirar.
- 2026-09-02: cumplir el orden literal del mandato (firmar 12:09:27, ejecutar 12:09:38) es tan importante como cumplir el mandato: el acta no podrá decir que se ejecutó sin taxonomía. Cuando te ponen una condición, la trazabilidad del minuto también es argumento.
- 2026-09-02: no tocar el fichero de ley mientras el Consejo no vote (a12 del acta, el vicio del [a150]): el diff preparado, hasheado y con script de precondición vale más que una aplicación apresurada. Mi columna EJECUTADAS queda en 0 hoy, y es la primera vez que ese cero es un mérito.
- 2026-09-02: tres cifras (139/161/84/77/76) describen la misma data desde denominadores distintos — marcas, casos, bloques F1, bloques tocados. El acta que mezcle dos de ellas miente, y quien la firma soy yo: cada número, con su denominador escrito al lado, en cada documento.
