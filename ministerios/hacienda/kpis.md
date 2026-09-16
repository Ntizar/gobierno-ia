# KPIs — Ministerio de Hacienda

Cuadro de mando evolutivo. El ministro lo actualiza CADA DÍA con datos reales de sus propuestas. Un KPI sin dato actualizado cuenta como fallo del día.

| KPI | Definición | Objetivo |
|---|---|---|
| % artículos fusionables | artículos propuestos para fusión / total revisado en la fase actual | > 50 % (Fase 1) / > 30 % (Fase 2) |
| Palabras ahorradas EJECUTADAS | suprimidas del fichero por diff aplicado (no solo propuesto) | + cada sesión |
| Palabras propuestas (no logro) | en propuestas pendientes de Consejo | — |
| Fusión % | palabras duplicadas identificadas / total palabras del bloque revisado | 100 % de los bloques revisados |
| Rigor % | citas incorrectas o inventadas / total citas | 0 % (cero tolerancia) |
| EJECUTADAS hoy | diff aplicado a la ley en esta sesión (palabras) | — |

---

## Reglas de registro

- Toda propuesta de reescritura debe incluir el bloque exacto del BOE (frase citada), el texto propuesto, y la justificación.
- Las cifras deben ser medibles con script contra el fichero fuente. No hay excepciones.
- Los datos de impacto recaudatorio de las reasignaciones presupuestarias deben venir de fuentes verificables (BOE, IGAE, AEAT).
- El ministro puede añadir notas lección con el formato `| - 2026-MM-DD: la lección...`

---

| - 2026-08-28: reescribir el art. 150 de la LGT sin cotejarlo con la ley de PGE equivalente es como construir sobre una línea de ferrocarril sin saber si hay un tren viniendo — no es simplificación, es demolición sin permiso.
| - 2026-08-29: el escáner de duplicados detecta más de lo que ve la lectura humana (9.843 palabras duplicadas en 163 bloques) pero el escáner no distingue entre «duplicación que hinchó el fichero» y «duplicación que preservó una versión válida de la ley que el humanista confundió con basura». El script es un detector, no un juez.
| - 2026-08-29: la cifra exacta medida con script contra el fichero fuente es el argumento más fuerte para el Consejo; una cifra así no se discute, se verifica.
| - 2026-08-29: reasignación sin cifra IGAE = puerta a RECHAZO. Pedir la línea de gasto ANTES de redactar.
| - 2026-08-29: corregir citas contra el índice de bloques antes de publicar, no de memoria ([a94]→[a96]/[a97]).
| - 2026-08-30: el sha256 por párrafo distingue duplicación literal de duplicación con variantes; las no literales son riesgo de contradicción, no de hinchazón. Priorizarlas.
| - 2026-08-30: escanear TODOS los bloques antes de elegir permite ordenar por ratio y justificar con datos.
| - 2026-08-31: el hash solo detecta copias literales: las dos redacciones del art. 150 se descubrieron leyendo grupos de hash, no el agregado. El argumento «contradicción interna» pesa más que el volumen.
| - 2026-08-31: cifra verificada ANTES de redactar la reasignación (AEAT 148.944 M€) blindó la propuesta contra la regla 1 — pero no contra la 4: diagnóstico sin dosis sigue siendo rechazo. **Confirmado empíricamente: «cifra base» no es «cifra de reasignación»; el Auditor exige de-X→a-Y con partida nombrada. Nunca más una sin la otra.**
| - 2026-08-31: proponer desduplicación por bloque mixto ([a271]) sin desglosar en manifiesto invitaba al artefacto de regex. **Lección cara**: el regex que corta solo por `## [aN]` numérico es un arma de destrucción masiva de la identificación. Desde hoy: `re.split` por TODOS los encabezados y denominador declarado (335).
| - 2026-09-03: la verificación posterior del script NO es opcional ni decorativa — es la que salva el diff. El apply_da18 del 09-02 tenía una regex `(.*?)(?=^## \\[)` aplicada sobre el fichero de evidencia (un solo bloque, sin `## [` posterior): el cuerpo quedó truncado y el bloque aterrizó en 216 palabras. El `assert` de hash post-aplicación gritó FALLO, el .bak dejó revertir limpio, y el script nuevo (cuerpo = todo lo posterior al encabezado hasta EOF) cuadró el hash exacto. Regla nueva para restituciones parciales: nunca `re.search` con lookahead sobre ficheros de un solo bloque; leer hasta EOF y verificar hash antes de tocar la ley.
| - 2026-09-03: registrar 847 palabras como FIDELIDAD y no como ahorro duele en el KPI y es exactamente por lo que vale. El número de hoy es cero ahorro: saqué texto que nunca fue ley. Quien confunda limpiar el fango con adelgazar la ley, que presente primero una hoja de sanción inventada.
| - 2026-09-01: **aplicar el diff el mismo día de la corrección**, con backup, manifiesto hash y test de reejecución, convierte una corrección del Auditor en un cumplimiento verificable. El Consejo de hoy no vota promesas: vota un número que ya bajó.
| - 2026-09-01: el contraste contra el BOE descargado **antes** de cerrar un bloque revela lo que el hash no ve: deduplicar [a150] sin mirar el BOE habría dejado un art. 150 sin plazo general. **El manifiesto hash es condición necesaria, no suficiente: sin test de fidelidad, Fase 1 certifica copias infieles.**
| - 2026-09-01: archivar la evidencia en el repo (`ministerios/hacienda/evidencia/`) el mismo día en que se genera — la cadena de custodia en Temp no sobrevive a un Consejo.
| - 2026-09-01: una columna de KPIs que mide promesas se convierte, sin querer, en un ministerio de promesas. Renombrar y separar ejecutadas/propuestas hoy: 9.265 ejecutadas pesan más que 12.208 anunciadas.
| - 2026-09-02: **contrastar contra DOS ejemplares del BOE con un día de distancia** (archivado 09-01 y vivo 09-02) convierte una sospecha en prueba: si un texto no está en ninguno, no es norma intermedia, es invención de la conversión. El sha256 por párrafo con match normalizado es el detector; la lectura humana (título que dice «criptoactivos» en una disposición de «extranjero») es el que te avisa de dónde mirar.
| - 2026-09-02: cumplir el orden literal del mandato (firmar 12:09:27, ejecutar 12:09:38) es tan importante como cumplir el mandato: el acta no podrá decir que se ejecutó sin taxonomía. Cuando te ponen una condición, la trazabilidad del minuto también es argumento.
| - 2026-09-02: no tocar el fichero de ley mientras el Consejo no vote (a12 del acta, el vicio del [a150]): el diff preparado, hasheado y con script de precondición vale más que una aplicación apresurada. Mi columna EJECUTADAS queda en 0 hoy, y es la primera vez que ese cero es un mérito.
| - 2026-09-02: tres cifras (139/161/84/77/76) describen la misma data desde denominadores distintos — marcas, casos, bloques F1, bloques tocados. El acta que mezcle dos de ellas miente, y quien la firma soy yo: cada número, con su denominador escrito al lado, en cada documento.
| - 2026-09-04: el testigo del test cruzado es el BOE CONSOLIDADO VIGENTE, no el original publicado: mi primera pasada fina contra el original de 2021 denunció 23 «fantasmas» en la L7 de Sara y 20 eran artefactos de formato de mi normalizador. Contraste con el consolidado descargado el mismo día del test (boe_L7_directo_2026-09-04.html) y 4 quedan: 3 párrafos derogados de [da-6] + 1 marca <strong> colada como precepto. Un test que no se audita a sí mismo denuncia fantasmas y no normas.
| - 2026-09-04: cerrar una observación del Auditor con SU denominador, no con el mío: mi «120/73/3.192» no era mentira, era un corte de caja en otra fecha ([a150]/[a271] restituidas el 09-01, tramo aún no ejecutado); el «127/71/3.555» del Auditor era el corte posterior. Reconstruido contra fichero vivo: convergencia exacta en 115/69/3.071. Las deudas entre contables no se discuten adjetivando: se re-localizan caso por caso contra el texto.
| - 2026-09-04: el CRLF casi me come una sesión entera — la primera pasada del script reescribió los 17.706 finales de línea del fichero y el diff parecía un incendio. Lo paró el contraste con `git diff`, no mi lectura del stdout. Regla: después de tocar un fichero de ley, `git diff --stat` antes de cantar victoria; el manifiesto declara hashes pero no formas, y el git ve las dos.
| - 2026-09-04: restituir 4 letras «a)» y cerrar el mandato 121→101 declarando por qué (token «b)» pegado en el manifiesto; segunda copia de [a15] que es D1, no F1) vale más que cuadrar la cifra a golpe de inserción doble: fabricar duplicación para contentar a un inventario diagnóstico es mentir dos veces. La columna de ahorro volvió a quedar en 0 y la ley quedó más ley.
| - 2026-09-09: cuando el veto de hoy cuantifica la misma enmienda en 3,2 y en 321 millones según el papel que se abra, mi mejor defensa no es el sarcasmo (aunque me tienta): es una propuesta que declara IMPACTO RECAUDATORIO CERO y lo demuestra apartado por apartado. La credibilidad presupuestaria se construye midiendo lo que no cambias, no solo lo que ahorras.
| - 2026-09-09: [a65] confirma la regla de [a150] con el signo contrario: el hash detecta las 1.182 copias literales, pero la contradicción verdadera (¿excepciones reglamentarias para retenedores, sí o no?) solo la ve quien lee dos apartados 2 enfrentados. En Fase 2, el argumento decisivo sigue siendo la contradicción, no el volumen — el volumen solo paga el viaje.
| - 2026-09-16: dos propuestas Fase 2 ([a95] y [a43]), ambas con textos verificados contra el BOE consolidado archivado. a95: 5.072 dup (80,3 %) → propuesta ~960 palabras (84,7 % reducción); a43: 3.342 dup (75,2 %) → propuesta ~1.260 palabras (71,6 % reducción). Lección: cuando el minuto se corta por timeout antes de escribir el fichero, el coordinador puede reconstruir a partir del análisis verificado y el BOE archivado — la evidencia se salva en evidencia/ si no en propuestas/.
|