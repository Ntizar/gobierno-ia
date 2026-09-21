# Test cruzado y ciego — LGS (Ley 14/1986, General de Sanidad)

- **Fecha:** 2026-09-21
- **Objeto:** `ministerios/sanidad/leyes/BOE-A-1986-10499.md` (estado actual del fichero)
- **Evidencia de contraste:** `ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html` (anclas por artículo) y `ministerios/sanidad/evidencia/boe_texto_plano.txt`
- **Verificador:** subagente independiente y ciego (acuerdo 32: test cruzado y ciego)
- **Regla de ceguera cumplida:** NO se abrieron `manifiesto_*.json`, ni `ministerios/sanidad/propuestas/2026-09-08.md|2026-09-16.md|2026-09-17.md`, ni actas del Consejo, ni scripts de aplicación de diffs.
- **Hashes (traza de lo auditado):**
  - ley MD: `sha256 b60a808323a3c01264bd86edcd9e30574edde432696e170bd5f869ff99b55fde`
  - BOE HTML: `sha256 2e42587547cc59b2dda56a5dd2312bc42ead99aa5973f6839f848e42cf701ab7`
  - BOE plano: `sha256 92c3445cea6fa43b15cbae9625a293887c98c054959de12436620eea03b08007`

---

## 1. Coherencia del fichero

| Comprobación | Resultado |
|---|---|
| Bloques `## [` | **151** (sin cambios) |
| Etiquetas duplicadas | ninguna |
| Etiquetas del MD sin ancla en el BOE | ninguna |
| Anclas del BOE sin bloque en el MD | 32, todas **estructurales** (preámbulo, títulos `ti`–`tvii`, capítulos `ci`–`cvi…`, `firma`): 183 − 32 = **151** |

**Conclusión:** no ha aparecido ningún bloque nuevo ni ha desaparecido ninguno; los cuatro bloques objetivo conservan su ancla y su etiqueta.

---

## 2. Veredictos

### [atres] Artículo 3 —líneas 27-38— → **VALIDADA**
- Copias del cuerpo: **1**. Frases ≥8 palabras repetidas dentro del bloque: **0**.
- Los 4 apartados (incluido el 4, añadido por la LO 3/2007) son **literalmente idénticos** al BOE consolidado; 0 frases sin traza.
- Diferencia única (menor): se omite la nota de pie editorial del BOE *«Se añade el apartado 4 por la disposición adicional 8.1 de la Ley Orgánica 3/2007, de 22 de marzo.»*. La omisión de notas de pie es **sistemática en todo el fichero** y no afecta al texto articulado.

### [aseis] Artículo 6 —líneas 55-72— → **VALIDADA CON OBSERVACIONES**
- Copias del cuerpo: **1**. Frases ≥8 palabras repetidas: **0**.
- Contenido completo y fiel: introducción + apartados 1-5 + apartado 2 añadido por la LO 3/2007, todos literales frente al BOE. 0 frases sin traza.
- Observaciones de forma: (a) el BOE consolidado numera la introducción como *«1. Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:»* (renumeración de 2007: «Se numera como apartado 1 y se añade el apartado 2…») y el repo la reproduce **sin el prefijo «1.»**; (b) se omite la nota de pie (patrón sistemático). Ninguna afecta al contenido normativo.

### [adieciseis] Artículo 16 —líneas 175-200— → **RECHAZADA**
- Copias del cuerpo: **1**. Frases ≥8 palabras repetidas dentro del bloque: **2** (ambas en el texto nuevo, repetición productiva, no duplicación de copias):
  - `el sistema de información de las listas de espera` → líneas 185 y 187
  - `de los datos de las listas de espera` → líneas 195 y 199

**(1) Contenido del BOE ausente del repo — pérdida de contenido vigente:**
- Apartado 1 íntegro: *«Por lo que se refiere a la atención primaria, se les aplicarán las mismas normas sobre asignación de equipos y libre elección que al resto de los usuarios.»*
  - Ocurrencias: **1** en el HTML del BOE, **1** en el texto plano, **0** en el MD.
  - Rastro del corte: el bloque **arranca en «2.»**, numeración huérfana.

**(2) Texto sin traza (no existe en ningún punto del BOE archivado):** 8 frases ≥6 palabras, líneas 185-199
| Línea | Apartado nuevo | Palabras nuevas detectadas |
|---|---|---|
| 185 | 4. Ministerio de Sanidad / «Dirección General de **Cartilla** SNS» fijará criterios técnicos y sistema de información de listas de espera del SNS | `cartilla` |
| 187 | 5. Garantías mínimas del sistema de información de listas de espera | `garantizara` |
| 189 | 5.a) Trazabilidad completa del paciente, de la derivación de Primaria al alta | `trazabilidad`, `derivacion`, `diagnosticas`, `quirofano` |
| 191 | 5.b) Verificación independiente por autoridad técnica con acceso a historias clínicas electrónicas | `verificacion`, `independiente`, `historias`, `clinicas`, `electronicas` |
| 193 | 5.c) Publicación desglosada (CCAA, provincia, hospital) y % operados en plazo clínico | `desglosados`, `operados`, `porcentaje`, `recomendados` |
| 195 | 5.d) Protección legal del personal que denuncie, sin represalia | `denuncie`, `manipulacion`, `falseamiento`, `disciplinaria` |
| 197 | 5.e) Auditoría aleatoria trimestral del 5% de expedientes prioritarios | `auditoria`, `aleatoria`, `expedientes`, `prioritarios`, `trimestral` |
| 199 | 6. Régimen sancionador: falta muy grave para gestores y directivos | `considerara`, `gestores`, `directivos`, `implicados` |

- Contraste de vocabulario sobre la evidencia archivada: `trazabilidad` = 0, `auditoría` = 0, `Cartilla` = 0, `denuncie` = 0; `lista(s) de espera` = **1** (solo la expresión *«lista de espera única»* del apartado 2 del propio BOE).
- Duración de la comprobación específica del art. 16 (punto 5 del encargo): la LGS vigente regula el uso de los servicios sanitarios **sin** mecanismos de verificación de listas de espera. Los contenidos de listas de espera (4), trazabilidad y verificación independiente (5.a, 5.b), auditoría aleatoria (5.e) y **protección del denunciante** (5.d) son adiciones sin traza. **Se registran como «texto sin traza»; pueden corresponder a una decisión aprobada: se reporta, no se corrige.**

**Motivo forense:** doble hallazgo — supresión de un apartado vigente del BOE (con numeración huérfana como firma del corte) y adición de 8 frases normativas sin traza alguna. El bloque no es reproducción fiel del BOE consolidado.
**Contradicciones internas:** no hay dos versiones del mismo apartado; sí un corte de contenido evidente (salto de «1.» a «2.»).

### [aveinte] Artículo 20 —líneas 283-298— → **VALIDADA CON OBSERVACIONES**
- Copias del cuerpo: **1**. Frases ≥8 palabras repetidas: **0**. Frases sin traza: **0**.
- Apartados 1-4 **literales** frente al BOE; el apartado 1 y el párrafo de psiquiatría infantil/psicogeriatría están completos (sin truncamientos).
- Observaciones:
  - (a) El primer párrafo (L287) **no** es texto sin traza: coincide literalmente con el **texto definitivo que el propio BOE archiva en su blockquote** del mismo bloque (1 ocurrencia en HTML, 1 en plano). Sustituye al párrafo **corrupto/truncado** del cuerpo principal del BOE (*«…a las demás personas que recursos asistenciales a nivel ambulatorio…»*, 0 ocurrencias en el MD). Es una **sustitución documentada**, no una invención.
  - (b) Se omite la nota del BOE *«Se advierte que el texto definitivo aprobado por el Congreso de los Diputados… para el primer párrafo de este artículo era el siguiente:»*, de modo que la elección queda **sin justificación visible** en el fichero.
- Contradicciones internas: ninguna (no hay dos versiones conviviendo; el párrafo corrupto no se reproduce).

---

## 3. Contenido del BOE ausente (resumen)

| Bloque | Frases ≥6 palabras del BOE ausentes del repo | Naturaleza |
|---|---|---|
| [atres] | 1 (nota de pie «Se añade el apartado 4…») | aparato editorial del BOE, omitido sistemáticamente |
| [aseis] | 1 (nota de pie «Se numera como apartado 1…») + prefijo «1.» de la introducción | editorial + diferencia de numeración |
| [adieciseis] | 1 (**apartado 1 vigente**, atención primaria / asignación de equipos y libre elección) | **pérdida de contenido articulado** |
| [aveinte] | 2 (párrafo corrupto del cuerpo principal + nota «Se advierte…») | cobertura documentada: el texto del repo sí tiene traza en el blockquote del BOE |

## 4. Texto sin traza (resumen)

- [atres]: 0 · [aseis]: 0 · [aveinte]: 0
- **[adieciseis]: 8 frases** (apartados 4, 5.a-5.e y 6: listas de espera, trazabilidad, verificación independiente, auditoría y protección del denunciante), líneas 185-199.

## 5. Recuento de copias y repeticiones

| Bloque | Artículo | Líneas | Copias del cuerpo | Frases ≥8 palabras repetidas | Frases sin traza | Veredicto |
|---|---|---|---|---|---|---|
| [atres] | 3 | 27-38 | 1 | 0 | 0 | VALIDADA |
| [aseis] | 6 | 55-72 | 1 | 0 | 0 | VALIDADA CON OBSERVACIONES |
| [adieciseis] | 16 | 175-200 | 1 | 2 | 8 | RECHAZADA |
| [aveinte] | 20 | 283-298 | 1 | 0 | 0 | VALIDADA CON OBSERVACIONES |

**Bloques del fichero:** 151. **Ficheros escritos:** `consejo/evidencia/test_cruzado_LGS_2026-09-21.md` y `consejo/evidencia/test_cruzado_LGS_2026-09-21.json`. Ningún fichero de ley modificado; sin commits.
