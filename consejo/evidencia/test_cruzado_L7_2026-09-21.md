# Test cruzado ciego — Ley 7/2021 de Cambio Climático (BOE-A-2021-8447)

- **Fecha:** 2026-09-21 · **Tipo:** verificador independiente y ciego (acuerdo 32)
- **Fichero auditado:** `ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md`
- **Patrón de contraste:** `ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html`
- **Bloques auditados:** `[a1]` (art. 1), `[a2]` (art. 2), `[a1-7]` (art. 15)
- **Regla de ceguera respetada:** no se han leído manifiestos, propuestas, actas ni scripts de aplicación.
- **Modificaciones:** ninguna. Solo lectura; sin commit ni push.
- **Huella del fichero auditado:** `sha256 = 3326932f492e2928e3b37877db28f2fdff1d4c0d35ef5e9a93dbd6c11b3ba998` (176999 bytes, 1067 líneas, todas CRLF).

## Veredicto por bloque

| Bloque | Artículo | Veredicto | Fidelidad palabras (repo/BOE) | Frases BOE ausentes | Texto sin traza |
|---|---|---|---|---|---|
| `[a1]` | Art. 1 Objeto de la Ley | **VALIDADA CON OBSERVACIONES** | 145/145 — ratio 1.00000 (bloque) · 1.00000 (párrafos) | 0 | 0 |
| `[a2]` | Art. 2 Principios rectores | **VALIDADA CON OBSERVACIONES** | 324/315 — ratio 0.98592 (bloque) · 0.98574 (párrafos) | 0 | 9 |
| `[a1-7]` | Art. 15 Puntos de recarga | **VALIDADA CON OBSERVACIONES** | 1446/1444 — ratio 0.99931 (bloque) · 1.00000 (párrafos) | 0 | 2 |

### `[a1]` — Art. 1 Objeto de la Ley

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Cuerpo íntegro y fiel: ratio difflib 1.00000 (145/145 palabras, cero diferencias palabra a palabra con el bloque del BOE), 0 frases del BOE ausentes, 0 texto sin traza, 1 sola copia del artículo, sin frases repetidas y espaciado uniforme. Observación de formato: el rótulo fusiona el título («## [a1] Artículo 1. Objeto de la Ley») y el cuerpo ya no lo repite, desviándose de la convención del fichero (los 39 bloques de artículo llevan «Artículo N» en el rótulo y el título como primera línea del cuerpo) y de su propio estado previo (bak-2026-09-21). Falta además el encabezado estructural «TÍTULO PRELIMINAR / Disposiciones generales» (ausente en todo el fichero). No hay pérdida de contenido del BOE.

Evidencia:

- Rótulo: `Artículo 1. Objeto de la Ley`
- Título en el BOE: `Artículo 1. Objeto de la Ley.` · el rótulo incluye el título: **True**
- Líneas no vacías: 3 en el repo vs 3 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «esta ley tiene por objeto asegurar el cumplimiento por parte de espana…»).
- Fidelidad palabra a palabra (difflib): **ratio 1.00000** con el rótulo incluido (145 palabras repo / 145 BOE) · **1.00000** solo con los párrafos del artículo.
- Frases repetidas de ≥8 palabras dentro del bloque: **ninguna** (0 secuencias de 15 palabras con ≥2 apariciones).
- Espaciado de listas/líneas en blanco: secuencias de líneas en blanco = [1, 1] → uniforme: **True**
- Diff palabra a palabra contra el BOE (difflib): opcodes no iguales =

**Contenido del BOE ausente en el repo: NINGUNO** (cobertura completa a partir de 6 palabras).

**Texto del repo sin traza en el BOE: NINGUNO.**

### `[a2]` — Art. 2 Principios rectores

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Cuerpo íntegro: 0 frases del BOE ausentes, 1 sola copia, sin frases repetidas; las 15 listas a)–ñ) van separadas por exactamente una línea en blanco (uniforme) y sin líneas en blanco irregulares. El único delta palabra a palabra contra el BOE es una inserción de 9 palabras (ratio 0.98592 en el bloque, 0.98574 en los párrafos): el encabezado «TÍTULO I / Objetivos y planificación de la transición energética», que existe verbatim en el BOE pero como bloque propio (id="ti"); en el fichero viaja anexado al final del bloque a2, en la posición correcta (justo antes de [a3]). Observaciones: (i) el rótulo fusiona el título igual que [a1], desviándose de la convención del fichero; (ii) el encabezado TÍTULO I no constituye bloque propio, lo que rompe la granularidad por bloques; (iii) la uniformidad de espaciado es única en el fichero (los otros 19 bloques con listas tienen huecos irregulares de 0/1 línea en blanco): a2 es coherente internamente pero no con el resto.

Evidencia:

- Rótulo: `Artículo 2. Principios rectores`
- Título en el BOE: `Artículo 2. Principios rectores.` · el rótulo incluye el título: **True**
- Líneas no vacías: 19 en el repo vs 17 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «las actuaciones derivadas de esta ley y de su desarrollo se regiran po…»).
- Fidelidad palabra a palabra (difflib): **ratio 0.98592** con el rótulo incluido (324 palabras repo / 315 BOE) · **0.98574** solo con los párrafos del artículo.
- Frases repetidas de ≥8 palabras dentro del bloque: **ninguna** (0 secuencias de 15 palabras con ≥2 apariciones).
- Espaciado de listas/líneas en blanco: secuencias de líneas en blanco = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] → uniforme: **True**
- Diff palabra a palabra contra el BOE (difflib): opcodes no iguales =
  - `insert` BOE=`` → repo=`titulo i objetivos y planificacion de la transicion energetica`

**Contenido del BOE ausente en el repo: NINGUNO** (cobertura completa a partir de 6 palabras).

**Texto del repo sin traza en el BOE (9):**
- [14 palabras] de suministro de energia n cooperacion colaboracion y coordinacion entre las administraciones publicas titulo
- [14 palabras] suministro de energia n cooperacion colaboracion y coordinacion entre las administraciones publicas titulo i
- [14 palabras] de energia n cooperacion colaboracion y coordinacion entre las administraciones publicas titulo i objetivos
- [14 palabras] energia n cooperacion colaboracion y coordinacion entre las administraciones publicas titulo i objetivos y
- [14 palabras] n cooperacion colaboracion y coordinacion entre las administraciones publicas titulo i objetivos y planificacion
- [14 palabras] cooperacion colaboracion y coordinacion entre las administraciones publicas titulo i objetivos y planificacion de
- [14 palabras] colaboracion y coordinacion entre las administraciones publicas titulo i objetivos y planificacion de la
- [14 palabras] y coordinacion entre las administraciones publicas titulo i objetivos y planificacion de la transicion
- [14 palabras] coordinacion entre las administraciones publicas titulo i objetivos y planificacion de la transicion energetica

  *Interpretación forense:* las 9 secuencias son ventanas deslizantes sobre la MISMA juntura —el último principio («…Administraciones Públicas.») seguido del encabezado «TÍTULO I / Objetivos y planificación de la transición energética»—. Ambas partes existen verbatim en el BOE (bloques `a2` y `ti`), pero no son consecutivas en el BOE porque allí el encabezado es un bloque aparte. No es texto inventado ni pérdida.

### `[a1-7]` — Art. 15 Puntos de recarga

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Fidelidad total al BOE consolidado: los párrafos del artículo son idénticos palabra a palabra (ratio difflib 1.00000, 1444/1444 palabras, 0 frases del BOE ausentes), art. 15 en UNA sola versión y sin apartados duplicados (1, 2, 2 bis, 3–12). Las 80 secuencias internas distintas de 15 palabras con ≥2 apariciones son repeticiones legítimas del texto legal, con el MISMO número de apariciones que en el BOE (4/4, 5/5…), no duplicación de bloque. Contradicción de plazos: NO existe (0 «12/doce meses» y 2 «veintiún meses» en el bloque, idéntico al BOE). Observación de formato: el rótulo «## [a1-7] Artículo 15» no incluye el título y el cuerpo lo repite («Artículo 15. Instalación de puntos de recarga eléctrica.»), generando la secuencia «Artículo 15 Artículo 15» sin traza en el BOE (1446 palabras en el repo frente a 1444 en el BOE, ratio 0.99931 con el rótulo incluido); es la convención general del fichero, pero inconsistente con el nuevo formato de [a1] y [a2].

Evidencia:

- Rótulo: `Artículo 15`
- Título en el BOE: `Artículo 15. Instalación de puntos de recarga eléctrica.` · el rótulo incluye el título: **False**
- Líneas no vacías: 17 en el repo vs 16 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «el gobierno velara especialmente por el cumplimiento de lo establecido…»).
- Fidelidad palabra a palabra (difflib): **ratio 0.99931** con el rótulo incluido (1446 palabras repo / 1444 BOE) · **1.00000** solo con los párrafos del artículo.
- Frases repetidas de ≥8 palabras dentro del bloque: **80** secuencias distintas de 15 palabras con ≥2 apariciones — todas con el mismo nº de apariciones que en el BOE (repetición legítima del texto legal, no duplicación de bloque).
  - Muestra: «de suministro de combustibles y carburantes a…» repo=5 / BOE=5 · «suministro de combustibles y carburantes a ve…» repo=5 / BOE=5 · «de combustibles y carburantes a vehiculos cuy…» repo=5 / BOE=5 · «combustibles y carburantes a vehiculos cuyo v…» repo=5 / BOE=5
- Espaciado de listas/líneas en blanco: secuencias de líneas en blanco = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] → uniforme: **True**
- Apartados numerados detectados: 13 → 1, 2, 2bis, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (duplicados: ninguno)
- Diff palabra a palabra contra el BOE (difflib): opcodes no iguales =
  - `insert` BOE=`` → repo=`articulo 15`

**Contenido del BOE ausente en el repo: NINGUNO** (cobertura completa a partir de 6 palabras).

**Texto del repo sin traza en el BOE (2):**
- [14 palabras] articulo 15 articulo 15 instalacion de puntos de recarga electrica 1 el gobierno pondra
- [14 palabras] 15 articulo 15 instalacion de puntos de recarga electrica 1 el gobierno pondra a

  *Interpretación forense:* las 2 secuencias son ventanas deslizantes sobre la juntura rótulo+cuerpo («Artículo 15» del rótulo + «Artículo 15. Instalación de puntos de recarga eléctrica.» del cuerpo). Cada parte existe en el BOE; lo que no existe es la repetición consecutiva del nombre del artículo.

## Contradicción de plazos del art. 15 (puntos de recarga)

- «12 / doce meses» en el bloque `[a1-7]`: **0** · «21 / veintiún meses»: **2**
- Lo mismo en el BOE consolidado: «12 / doce meses»: **0** · «21 / veintiún meses»: **2**
- **Estado de la contradicción: RESUELTA / NO EXISTE en el estado actual.** Los apartados 2 y 2 bis dicen ambos «veintiún meses», igual que el BOE.
- Apartado 2 (final): `…potencia igual o superior a 150 kW en corriente continua, que deberá prestar servicio en un plazo de veintiún meses a partir de la entrada en vigor de esta ley.`
- Apartado 2 bis (final): `… casos, la infraestructura de recarga eléctrica deberá prestar servicio en el plazo de veintiún meses desde la publicación de las resoluciones a las que hace referencia el apartado 7 de este artículo.`
- Único «doce meses» del fichero (fuera del art. 15, y también en el BOE): línea 1014 — En el plazo de doce meses desde la entrada en vigor de esta ley, el Gobierno y la Comisión
- Versiones del artículo 15 en el fichero: **1** (bloque `[a1-7]`); el bloque `[a1-12]` es el art. 15 *bis*, artículo distinto, y no lo duplica.
- Ocurrencias de «Artículo 15» dentro del bloque `[a1-7]`: **2** (rótulo + primera línea del cuerpo).
- Traza histórica (backups del propio fichero): en `.bak-2026-09-03` el bloque tenía 48 líneas, 3 copias del título y del apartado 2, y sí contenía «en un plazo de 12 meses» (1 vez) junto a «veintiún meses» (5): ahí existía la duplicación y la contradicción. Desde `.bak-2026-09-04` en adelante: 17 líneas, 1 copia, 0 «12 meses», 2 «veintiún meses».

## Coherencia del fichero

- Nº de bloques `## [……]` : **71** (idéntico en los tres backups .bak-2026-09-03 / 09-04 / 09-21 → ni bloques nuevos ni desaparecidos).
- Bloques del md sin bloque homólogo en el BOE: **ninguno** (ninguno inventado).
- Bloques del BOE que en el md no son bloque propio: no, tp, ti, ti-2, ti-3, ti-4, tv, tv-2, tv-3, tv-4, ti-5 (11 encabezados estructurales de TÍTULO), el md los lleva como texto llano.
- Encabezados del BOE ausentes por completo en el fichero: **TÍTULO PRELIMINAR, Disposiciones generales** (contexto estructural de los arts. 1 y 2, que en el BOE abren el TÍTULO PRELIMINAR).
- Rótulos con el título fusionado en el rótulo: **`[a1]`, `[a2]`**; los otros 39 bloques de artículo usan «## [tag] Artículo N» y dejan el nombre del artículo/disposición como primera línea del cuerpo (67 de los 71 bloques siguen esa convención; solo no la siguen: `[pr]`, `[a1]`, `[a2]`, `[fi]`).
- Finales de línea: **1067 líneas CRLF / 1067 LF totales → 0 LF huérfanos** ⇒ conserva CRLF originales.

### Cambios respecto a los backups del propio fichero (evidencia temporal)

- `BOE-A-2021-8447.md.bak-2026-09-03` (n=71 bloques, sha256…95804d1950230d80): a1=difiere, a2=difiere, a1-7=difiere → métricas del bloque a1-7 en ese backup: 48 líneas, 3 copia(s) del título, 3 copia(s) del ap. 2, 1 «12 meses», 5 «veintiún meses»
- `BOE-A-2021-8447.md.bak-2026-09-04` (n=71 bloques, sha256…af2e435f814fa02f): a1=difiere, a2=difiere, a1-7=identico → métricas del bloque a1-7 en ese backup: 17 líneas, 1 copia(s) del título, 1 copia(s) del ap. 2, 0 «12 meses», 2 «veintiún meses»
- `BOE-A-2021-8447.md.bak-2026-09-21` (n=71 bloques, sha256…715fee2597145e23): a1=difiere, a2=difiere, a1-7=identico → métricas del bloque a1-7 en ese backup: 17 líneas, 1 copia(s) del título, 1 copia(s) del ap. 2, 0 «12 meses», 2 «veintiún meses»

## Dictamen global

Los tres bloques **conservan íntegro el texto del BOE consolidado** (0 frases de ≥6 palabras perdidas en los tres) y **no contienen texto sin traza**, salvo las rampas de rótulo+título/encabezado, que se explican arriba y que no son texto inventado. El artículo 15 está saneado: una sola versión, sin duplicación y sin la contradicción 12/21 meses (que sí existía en el backup del 03-09). Las únicas anomalías detectadas son **de formato/estructura, no de contenido**: (1) `[a1]` y `[a2]` fusionaron el título en el rótulo, apartándose de la convención de los otros 39 bloques de artículo y de su propio estado del 21-09; (2) el encabezado «TÍTULO I» viaja al final del bloque `[a2]` en lugar de ser bloque propio; (3) el encabezado «TÍTULO PRELIMINAR / Disposiciones generales» no existe en el fichero; (4) el espaciado de las listas de `[a2]` es uniforme dentro del bloque pero único en el fichero. Ninguna diferencia se ha corregido: se reporta tal cual, tal como exige la regla del test ciego.

---
*Generado por verificación independiente y ciega. Evidencia en `consejo/evidencia/test_cruzado_L7_2026-09-21.json`.*
