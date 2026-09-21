# Test cruzado ciego — Ley 7/2021 de Cambio Climático (BOE-A-2021-8447)

- **Fecha:** 2026-09-21 · **Tipo:** verificador independiente y ciego (acuerdo 32)
- **Fichero auditado:** `ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md`
- **Patrón de contraste:** `ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html`
- **Bloques auditados:** `[a1]` (art. 1), `[a2]` (art. 2), `[a1-7]` (art. 15)
- **Regla de ceguera respetada:** no se han leído manifiestos, propuestas, actas ni scripts de aplicación.
- **Modificaciones:** ninguna. Solo lectura; sin commit ni push.
- **Huella del fichero auditado:** `sha256 = 3326932f492e2928e3b37877db28f2fdff1d4c0d35ef5e9a93dbd6c11b3ba998` (176999 bytes, 1067 líneas, todas CRLF).

## Veredicto por bloque

| Bloque | Artículo | Veredicto | Fidelidad palabras | Frases BOE ausentes | Texto sin traza |
|---|---|---|---|---|---|
| `[a1]` | Art. 1 Objeto de la Ley | **VALIDADA CON OBSERVACIONES** | 145/145 (ratio 1.00000) | 0 | 0 |
| `[a2]` | Art. 2 Principios rectores | **VALIDADA CON OBSERVACIONES** | 324/315 (ratio 0.98592) | 0 | 9 |
| `[a1-7]` | Art. 15 Puntos de recarga | **VALIDADA CON OBSERVACIONES** | 1446/1444 (ratio 0.99931) | 0 | 2 |

### `[a1]` — Art. 1 Objeto de la Ley

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Cuerpo íntegro y fiel: 0 frases del BOE ausentes, 0 texto sin traza, 1 sola copia del artículo, sin frases repetidas y espaciado uniforme. Observación de formato: el rótulo fusiona el título («## [a1] Artículo 1. Objeto de la Ley») y el cuerpo ya no lo repite, desviándose de la convención del fichero (67 de 71 bloques llevan el título como primera línea del cuerpo) y de su propio estado previo (bak-2026-09-21). Falta además el encabezado estructural «TÍTULO PRELIMINAR / Disposiciones generales» (ausente en todo el fichero). Sin pérdida de contenido del BOE.

Evidencia:

- Rótulo: `Artículo 1. Objeto de la Ley`
- Título en el BOE: `Artículo 1. Objeto de la Ley.` · el rótulo incluye el título: **True**
- Líneas no vacías: 3 en el repo vs 3 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «esta ley tiene por objeto asegurar el cumplimiento por parte de espana…»).
- Frases repetidas de ≥8 palabras dentro del bloque: **0** (ninguna).
- Espaciado de listas/líneas en blanco: secuencias de líneas en blanco = [1, 1] → uniforme: **True**
- Diff palabra a palabra contra el BOE (difflib): opcodes no iguales =

**Contenido del BOE ausente en el repo: NINGUNO** (cobertura completa a partir de 6 palabras).

**Texto del repo sin traza en el BOE: NINGUNO.**

### `[a2]` — Art. 2 Principios rectores

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Cuerpo íntegro: 0 frases del BOE ausentes, 1 sola copia, sin frases repetidas; las 15 listas a)–ñ) van separadas por exactamente una línea en blanco (uniforme) y sin líneas en blanco irregulares. Observaciones: (i) el rótulo fusiona el título igual que [a1], desviándose de la convención del fichero; (ii) el encabezado «TÍTULO I / Objetivos y planificación de la transición energética» queda anexado al final del bloque (en el BOE es un bloque propio, id="ti"): posición correcta y texto verbatim, pero rompe la granularidad por bloques; (iii) esa uniformidad de espaciado es única en el fichero (otros 19 bloques con listas tienen huecos irregulares de 0/1 línea en blanco), por lo que a2 es coherente internamente pero no con el resto.

Evidencia:

- Rótulo: `Artículo 2. Principios rectores`
- Título en el BOE: `Artículo 2. Principios rectores.` · el rótulo incluye el título: **True**
- Líneas no vacías: 19 en el repo vs 17 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «las actuaciones derivadas de esta ley y de su desarrollo se regiran po…»).
- Frases repetidas de ≥8 palabras dentro del bloque: **0** (ninguna).
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

### `[a1-7]` — Art. 15 Puntos de recarga

**Veredicto: VALIDADA CON OBSERVACIONES**

Motivo forense: Fidelidad total al BOE consolidado: 1444 palabras idénticas, ratio difflib 1.00000, 0 frases del BOE ausentes, art. 15 en UNA sola versión y sin apartados duplicados (1, 2, 2 bis, 3–12). Las 87 frases internas de ≥8 palabras repetidas son repeticiones legítimas del texto legal (mismo nº de apariciones que en el BOE). Contradicción de plazos: NO existe (0 «12/doce meses» y 2 «veintiún meses» en el bloque, idéntico al BOE). Observación de formato: el rótulo «## [a1-7] Artículo 15» no incluye el título y el cuerpo lo repite («Artículo 15. Instalación de puntos de recarga eléctrica.»), generando la secuencia sin traza en el BOE «Artículo 15 Artículo 15»; es la convención general del fichero, pero inconsistente con el nuevo formato de [a1] y [a2].

Evidencia:

- Rótulo: `Artículo 15`
- Título en el BOE: `Artículo 15. Instalación de puntos de recarga eléctrica.` · el rótulo incluye el título: **False**
- Líneas no vacías: 17 en el repo vs 16 párrafos en el BOE.
- **Copias del cuerpo del artículo:** 1 (clave de detección: «el gobierno velara especialmente por el cumplimiento de lo establecido…»).
- Frases repetidas de ≥8 palabras dentro del bloque: **819** — todas con el mismo nº de apariciones que en el BOE (repetición legítima del texto legal).
  - Muestra: «quienes ostenten la titularidad de las instal…» repo=4 / BOE=4 · «ostenten la titularidad de las instalaciones …» repo=4 / BOE=4 · «la titularidad de las instalaciones de sumini…» repo=4 / BOE=4 · «titularidad de las instalaciones de suministr…» repo=4 / BOE=4
- Espaciado de listas/líneas en blanco: secuencias de líneas en blanco = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] → uniforme: **True**
- Apartados numerados detectados: 13 (duplicados: ['2'])
- Diff palabra a palabra contra el BOE (difflib): opcodes no iguales =
  - `insert` BOE=`` → repo=`articulo 15`

**Contenido del BOE ausente en el repo: NINGUNO** (cobertura completa a partir de 6 palabras).

**Texto del repo sin traza en el BOE (2):**
- [14 palabras] articulo 15 articulo 15 instalacion de puntos de recarga electrica 1 el gobierno pondra
- [14 palabras] 15 articulo 15 instalacion de puntos de recarga electrica 1 el gobierno pondra a

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
- Bloques del BOE que en el md no son bloque propio: ['no', 'tp', 'ti', 'ti-2', 'ti-3', 'ti-4', 'tv', 'tv-2', 'tv-3', 'tv-4', 'ti-5'] (11 encabezados estructurales: TÍTULOS/CAPÍTULOS), el md los lleva como texto llano.
- Encabezados del BOE ausentes por completo en el fichero: **TÍTULO PRELIMINAR, Disposiciones generales** (contexto estructural de los arts. 1 y 2).
- Rótulos con el título fusionado en el rótulo: **['a1', 'a2']** — el resto (39 bloques de artículo) usa «## [tag] Artículo N» y deja el título como primera línea del cuerpo (67 bloques).
- Finales de línea: **1067 líneas CRLF / 1067 LF totales → 0 LF huérfanos** ⇒ conserva CRLF originales.

### Cambios respecto a los backups del propio fichero (evidencia temporal)

- `BOE-A-2021-8447.md.bak-2026-09-03` (n=71 bloques, sha256…95804d1950230d80): a1=difiere, a2=difiere, a1-7=difiere → bak a1-7: 48 líneas, 3 copias de título, 3 copias de ap. 2, 1 «12 meses», 5 «veintiún meses»
- `BOE-A-2021-8447.md.bak-2026-09-04` (n=71 bloques, sha256…af2e435f814fa02f): a1=difiere, a2=difiere, a1-7=identico → bak a1-7: 17 líneas, 1 copias de título, 1 copias de ap. 2, 0 «12 meses», 2 «veintiún meses»
- `BOE-A-2021-8447.md.bak-2026-09-21` (n=71 bloques, sha256…715fee2597145e23): a1=difiere, a2=difiere, a1-7=identico → bak a1-7: 17 líneas, 1 copias de título, 1 copias de ap. 2, 0 «12 meses», 2 «veintiún meses»

## Dictamen global

Los tres bloques **conservan íntegro el texto del BOE consolidado** (0 frases de ≥6 palabras perdidas en los tres) y **no contienen texto sin traza**, salvo las dos secuencias de rótulo+título de `[a1-7]`. El artículo 15 está saneado: una sola versión, sin duplicación y sin la contradicción 12/21 meses. Las únicas anomalías detectadas son **de formato/estructura, no de contenido**: (1) `[a1]` y `[a2]` fusionaron el título en el rótulo, apartándose de la convención de los otros 67 bloques y de su propio estado del 21-09; (2) el encabezado «TÍTULO I» viaja al final del bloque `[a2]` en lugar de ser bloque propio; (3) el encabezado «TÍTULO PRELIMINAR / Disposiciones generales» no existe en el fichero; (4) el espaciado de las listas de `[a2]` es uniforme dentro del bloque pero único en el fichero. Ninguna diferencia se ha corregido: se reporta tal cual.

---
*Generado por verificación independiente y ciega. Evidencia en `consejo/evidencia/test_cruzado_L7_2026-09-21.json`.*
