# Test cruzado y ciego — LGT (Ley 58/2003, de 17 de diciembre, General Tributaria)

- **Fecha:** 2026-09-21
- **Objeto:** `ministerios/hacienda/leyes/BOE-A-2003-23186.md` (estado actual, commit `cca052e`)
- **Evidencia de contraste:** `ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html` (anclas `id="a12"`, `id="a43"`, `id="a62"`, `id="a95"`)
- **Verificador:** subagente independiente y ciego (acuerdo 32: test cruzado y ciego)
- **Regla de ceguera cumplida:** NO se abrieron manifiestos de aplicación (`manifiesto_*.json`), ni propuestas (`ministerios/hacienda/propuestas/2026-09-08.md`, `2026-09-16.md`), ni actas del Consejo, ni scripts de aplicación de diffs. La desviación de [a12] se descubrió por contraste directo con el BOE y con la copia de seguridad del propio fichero de ley.
- **Hashes (traza de lo auditado):**
  - ley MD: `sha256 14aeb1ca76b631cd23f7f3f8b90df1262705666f803e3e5e0f1df9820efb3d8d`
  - BOE HTML: `sha256 f11b4197d22360cd28d7e73183ddff16770d78768083ba0dfdefe4c14428d891`
  - bloques: [a12] `9ecfbf99…`, [a43] `37021747…`, [a62] `daf4421c…`, [a95] `0231f26f…`
- **Método:** extracción de los párrafos del `div.bloque` del BOE (clases `parrafo`, `parrafo_2`, `articulo`), descartando el aparato editorial del BOE (notas «Se modifica/Se añade/Se derogan…», «Última actualización», «Modificación publicada», «Véase», «Texto añadido», «Subir», «[Bloque n]»); normalización tipográfica (minúsculas, sin tildes ni puntuación) y comparación por subsecuencia contigua de palabras, frase a frase (≥6 palabras) y por n-gramas de 8 palabras.

---

## 1. Coherencia del fichero

| Comprobación | Resultado |
|---|---|
| Bloques `## [` | **335** |
| Etiquetas duplicadas | ninguna |
| Bloques nuevos / desaparecidos vs `.bak-2026-09-01` | **0 / 0** (el respaldo también tenía 335) |
| Anclas en el BOE archivado | 448; sin bloque en el MD = **113, todas estructurales** (preámbulo, títulos `t*`, capítulos `c*`, secciones `s*` y sus variantes de numeración `-2`…`-13`, `firma`): 448 − 113 = **335** |
| Etiquetas del MD sin ancla en el BOE | ninguna |

**Conclusión:** no ha aparecido ningún bloque nuevo ni ha desaparecido ninguno; los cuatro bloques objetivo conservan su ancla y su etiqueta. Coherencia estructural del fichero: correcta.

---

## 2. Veredictos

### [a12] Artículo 12 — líneas 225-237 — **RECHAZADA**
- Copias del cuerpo: **1** (el `.bak-2026-09-01` tenía **2** rótulos y **2** juegos completos de apartados 1-3). Frases ≥8 palabras repetidas dentro del bloque: **0**. Palabras: BOE **227** / repo **169** (−58).
- **(1) Contenido del BOE ausente del repo — el apartado 3 vigente íntegro (5 frases ≥6 palabras):**
  - «En el ámbito de las competencias del Estado, la facultad de dictar disposiciones interpretativas o aclaratorias de las leyes y demás normas en materia tributaria corresponde al Ministro de Hacienda y Administraciones Públicas y a los órganos de la Administración Tributaria a los que se refiere el artículo 88.5 de esta Ley.»
  - «Las disposiciones interpretativas o aclaratorias dictadas por el Ministro serán de obligado cumplimiento para todos los órganos de la Administración Tributaria.»
  - «Las disposiciones interpretativas o aclaratorias dictadas por los órganos de la Administración Tributaria a los que se refiere el artículo 88.5 de esta Ley tendrán efectos vinculantes para los órganos y entidades de la Administración Tributaria encargados de la aplicación de los tributos.»
  - «Las disposiciones interpretativas o aclaratorias previstas en este apartado se publicarán en el boletín oficial que corresponda.»
  - «Con carácter previo al dictado de las resoluciones a las que se refiere este apartado, y una vez elaborado su texto, cuando la naturaleza de las mismas lo aconseje, podrán ser sometidas a información pública.»
- **(2) Texto sin traza (no existe en ningún punto del BOE archivado) — 4 frases, líneas 233, 235 y 237:**

| Línea | Frase (inicio literal) | Palabras nuevas vs BOE |
|---|---|---|
| 233 | «En el ámbito de las competencias del Estado, corresponde al Ministro de Hacienda la facultad **exclusiva** de dictar disposiciones interpretativas de las leyes y demás normas en materia tributaria.» | `exclusiva` |
| 235 | «Las disposiciones interpretativas serán de obligado cumplimiento para todos los órganos de la Administración tributaria y se publicarán en el boletín oficial que corresponda.» | — (refrito: todo su vocabulario existe en el BOE, pero la frase no) |
| 237 | «Los órganos de la Administración Tributaria a los que se refiere el artículo 88.5 podrán dictar **criterios** de aplicación **interna** vinculantes para los órganos y entidades de su **dependencia**, que se publicarán en el boletín oficial **correspondiente**.» | `criterios`, `interna`, `dependencia`, `correspondiente` |
| 237 | «Con carácter previo a su dictado, y cuando la naturaleza de los **mismos** lo aconseje, podrán ser **sometidos** a información pública.» | `mismos`, `sometidos` |

- **Contradicciones:** en el estado actual **no** conviven dos versiones del mismo apartado (queda una sola redacción del apartado 3). Sí convivían **antes de este commit**: en el `.bak` la copia A del apartado 3 decía «…corresponde **de forma exclusiva** al Ministro de Hacienda» y la copia B reproducía **literalmente** el BOE consolidado (redacción posterior a la Ley 34/2015).
- **Motivo forense:** la desduplicación se ejecutó correctamente (2 copias → 1, 0 frases repetidas), **pero se eliminó la copia fiel al BOE y sobrevive una redacción que no está en el BOE**: se pierden las 5 frases del apartado 3 vigente y aparecen 4 frases sin traza, una de ellas un párrafo íntegramente nuevo («criterios de aplicación interna vinculantes… de su dependencia»). En el **mismo commit**, los otros tres bloques objetivos quedaron idénticos palabra por palabra al BOE, luego el criterio aplicado sí preserva la copia consolidada: **[a12] es la excepción**. El fichero no contiene ningún marcador editorial (0 ocurrencias de marcas de enmienda), de modo que la desviación queda sin justificación visible. **Si el Consejo aprobó re-redactar el art. 12.3, debe registrarse como enmienda deliberada y el veredicto pasaría a VALIDADA CON OBSERVACIONES; tal como está ahora, el bloque no es reproducción fiel.**

### [a43] Artículo 43 — líneas 1165-1209 — **VALIDADA**
- Copias del cuerpo: **1** (el `.bak` tenía **6** rótulos, con los apartados 1, 2 y 3 repetidos hasta 6 veces). Frases ≥8 palabras repetidas: **16**, todas cláusulas paralelas del propio texto legal (p. ej. «los administradores de hecho o de derecho de», líneas **1171, 1173 y 1197**) — esas mismas repeticiones existen en el BOE ⇒ repetición legítima del texto, no duplicación de copias.
- **1.079 palabras en el repo = 1.079 en el BOE**; secuencia de palabras **idéntica** al BOE consolidado (apartados 1 a)-h), 2, 3 y 4). 0 frases del BOE ausentes; 0 frases sin traza.
- Única diferencia: se omiten las notas de pie editoriales del BOE («Se añaden los párrafos g) y h)…», «Véase… Resolución 2/2004…», «Última actualización…», «Modificación publicada…»), omisión **sistemática en todo el fichero** (0 ocurrencias en el MD) y sin efecto sobre el texto articulado.

### [a62] Artículo 62 — líneas 1489-1531 — **VALIDADA**
- Copias del cuerpo: **1** (`.bak`: 2). Frases ≥8 palabras repetidas: **75**, todas procedentes de las cláusulas de plazo paralelas inherentes al artículo (`o si éste no fuera hábil hasta el inmediato hábil siguiente`, 7 veces, líneas **1497, 1499, 1501, 1509, 1511, 1515 y 1517**; `de cada mes, desde la fecha de recepción de la notificación`, 6 veces) — todas presentes en el BOE.
- **813 palabras en el repo = 813 en el BOE**; secuencia de palabras **idéntica** al BOE consolidado (apartados 1-9, incluidos el 6 de asistencia mutua y los 8-9 de suspensión del ingreso). 0 ausentes / 0 sin traza. Misma omisión sistemática de notas de pie.

### [a95] Artículo 95 — líneas 2613-2661 — **VALIDADA**
- Copias del cuerpo: **1** (el `.bak` tenía **8** rótulos y los apartados 1, 3 y 4 repetidos 8 veces). Frases ≥8 palabras repetidas: **4**, boilerplate de sigilo del propio artículo (`al más estricto y completo sigilo respecto de ellos`, líneas **2651 y 2659**; `los retenedores y obligados a realizar ingresos a cuenta`, líneas **2657 y 2659**) — todas presentes en el BOE.
- **994 palabras en el repo = 994 en el BOE**; secuencia de palabras **idéntica** al BOE consolidado (apartado 1 a)-n), 2, 3, 4, 5 y 6). 0 ausentes / 0 sin traza. Misma omisión sistemática de notas de pie.

---

## 3. Contenido del BOE ausente del repositorio (resumen)

| Bloque | Frases ≥6 palabras del BOE ausentes | Naturaleza |
|---|---|---|
| [a12] | **5** (apartado 3 vigente íntegro: competencia del Ministro y de los órganos del art. 88.5, obligatoriedad, efectos vinculantes, publicación e información pública) | **pérdida de contenido articulado vigente** |
| [a43] | 0 | — |
| [a62] | 0 | — |
| [a95] | 0 | — |

## 4. Texto sin traza en el BOE (resumen)

- **[a12]: 4 frases** (líneas 233, 235 y 237) — reordenación/refrito del apartado 3 más un párrafo nuevo («criterios de aplicación interna vinculantes»). Palabras nuevas detectadas: `exclusiva`, `criterios`, `interna`, `dependencia`, `correspondiente`, `mismos`, `sometidos`. Contraste de vocabulario sobre la evidencia archivada: `exclusiva` = 0, `aplicación interna` = 0, `criterios de aplicación` = 0, `de forma exclusiva` = 0 ocurrencias.
- [a43]: 0 · [a62]: 0 · [a95]: 0.

## 5. Recuento de copias, frases repetidas y veredictos

| Bloque | Artículo | Líneas | Copias del cuerpo (ahora / bak) | Frases ≥8 palabras repetidas | Palabras BOE / repo | Frases BOE ausentes | Frases sin traza | Veredicto |
|---|---|---|---|---|---|---|---|---|
| [a12] | 12 | 225-237 | 1 / **2** | 0 | 227 / 169 (−58) | **5** | **4** | **RECHAZADA** |
| [a43] | 43 | 1165-1209 | 1 / **6** | 16 (legítimas) | 1.079 / 1.079 (=) | 0 | 0 | **VALIDADA** |
| [a62] | 62 | 1489-1531 | 1 / 2 | 75 (legítimas) | 813 / 813 (=) | 0 | 0 | **VALIDADA** |
| [a95] | 95 | 2613-2661 | 1 / **8** | 4 (legítimas) | 994 / 994 (=) | 0 | 0 | **VALIDADA** |

**Duplicación:** los cuatro bloques arrancaban el commit con copias múltiples del cuerpo (2, 6, 2 y 8) y los cuatro tienen ahora **una sola copia**. La desduplicación es correcta en los cuatro; en [a12] el problema no es la duplicación sino **qué copia sobrevivió**.

## 6. Contexto, contraste externo y limitaciones

- **Fidelidad global del fichero (contexto):** de los 335 bloques con ancla en el BOE, **156 son idénticos palabra por palabra** al texto consolidado y **179 difieren** (coherente con la naturaleza de simulación del proyecto: el fichero reescribe la ley en muchos artículos; 3 de esas diferencias son solo notas editoriales del BOE de −15 palabras). Los bloques [a43], [a62] y [a95] están entre los 156 idénticos; **[a12] es el único de los cuatro con pérdida y adición de contenido normativo**.
- **Contraste externo secundario** (a título de contexto, fuera de la evidencia archivada): la redacción del art. 12.3 del BOE archivado es la **vigente** publicada (post Ley 34/2015), y la redacción anterior publicada era «…corresponde **de forma exclusiva** al Ministro de Hacienda». El texto que hoy figura en el repo no coincide literalmente con **ninguna** de las dos: reordena la primera frase, contrae la segunda y añade el párrafo de «criterios de aplicación interna», sin precedente en las versiones consultadas.
- **Lo que NO he podido determinar (por la regla de ceguera):** si la redacción actual de [a12] corresponde a un acuerdo del Consejo. Se reporta, **no se corrige**; no se ha modificado ningún fichero de ley y no se ha hecho commit ni push.
- **Nota de método:** las notas de pie del BOE (aparato editorial) se han excluido de la comparación porque el MD no las reproduce en ningún artículo (0 ocurrencias en 8.391 líneas); no se computan como contenido ausente salvo mención expresa.

**Bloques del fichero:** 335. **Ficheros escritos:** `consejo/evidencia/test_cruzado_LGT_2026-09-21.md` y `consejo/evidencia/test_cruzado_LGT_2026-09-21.json`.
