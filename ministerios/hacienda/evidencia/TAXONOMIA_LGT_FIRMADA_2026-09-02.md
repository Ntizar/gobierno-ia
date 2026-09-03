# Taxonomía LGT — FIRMADA por el Ministro de Hacienda — 2026-09-02, 12:20

> Documento de condición exigida por el Consejo de Ministros de 2026-09-01 (acuerdo 13,
> APROBADO CON CONDICIÓN): antes de ejecutar el manifiesto masivo sha256 sobre los 335
> bloques de la Ley 58/2003 (BOE-A-2003-23186) debe estar firmada la separación entre
> **duplicado literal** y **duplicado por consolidación**, y la clasificación de fidelidad.
> Método ya declarado en mi intervención de ronda 2 (ronda2-hacienda.md, acta 2026-09-01) y
> asumido como criterio único por el acuerdo 18 del Consejo. Lo que se firma aquí no es una
> invención de última hora: es poner mi nombre sobre la regla con la que trabajé ayer.

## 1. Ejes de la clasificación (dos preguntas distintas)

**Eje A — ¿está el texto en el BOE? (fidelidad).** Se responde contra el ejemplar
consolidado archivado con SHA-256 en `evidencia/` (b29db001…, 2026-09-01; re-descargado
hoy 2026-09-02, a2f3fe1f…, contenido idéntico párrafo a párrafo). Cuatro clases, mutuamente
exclusivas, aplicadas a cada letra «a)» de los test de fidelidad:

| clase | definición | remedio |
|---|---|---|
| **F1 contenido_perdido** | el BOE tiene párrafo con esa letra; mi copia tiene la marca (o nada) y el contenido no está en el bloque | restituir literal desde el BOE, con hash (NUNCA antes de mandato — regla del acta 2026-09-02: «restitución verificada no autoriza aplicación anticipada») |
| **F2 no_localizable_en_bloque_BOE** | la marca existe en mi copia pero el BOE de ese bloque no tiene letra «a)» localizable en los tramos | ampliar tramo y re-testear; no se declara defecto definitivo |
| **F3 solo_marca_perdida** | el contenido está en el bloque (match por hash) pero se perdió la letra «a)» | restituir la marca; el precepto es fiel, el rótulo no |
| **F4 BOE_sin_a_legitimo** | el BOE tampoco tiene letra «a)» en ese precepto (era «apartado 1» o enumeración distinta) | archivar con constancia: no es omisión, es convención legal ajena |

**Eje B — si algo aparece dos veces, ¿por qué aparece? (duplicación).** Dos clases, y la
distinción es la que el Consejo me puso como condición:

| clase | definición | remedio |
|---|---|---|
| **D1 duplicado literal** | mismo SHA-256 normalizado ≥2 veces dentro del bloque: es la misma copia pegada. Diferencia cero o solo de caja/grapa (t/T) | suprimir copias sobrantes; eso es ahorro computable como «palabras EJECUTADAS» |
| **D2 duplicado por consolidación** | el propio BOE consolidado conserva versiones históricas superpuestas del precepto (entre medias dice «Se modifica por…», «Texto añadido…»). En mi copia aparecen como variantes NO idénticas | NO se suprimen como ahorro: se reescribe el bloque dejando SOLO la versión vigente declarada por el BOE, y las palabras suprimidas se registran al debe recuperado/restructuración, nunca mezcladas con el ahorro |

Criterio de veredicto: **a reglas iguales, veredictos iguales** — las clases D1/D2/F1–F4 se
aplican por igual a mis bloques y a los de Sanidad y Ecología; ninguna ley se gradúa con
regla propia.

## 2. Lo que la propia ejecución añade hoy (clase nueva, declarada con honestidad)

El barrido del manifiesto y la inspección forense de [dadecimoctava] (ver
`propuestas/2026-09-02.md`) obligan a una quinta clase, que no existía en mi clasificación
de anoche:

| clase | definición | remedio |
|---|---|---|
| **X1 contaminación multi-versión sin traza** | texto en mi copia que no está en NINGÚN BOE (ni archivado ni vivo), mezcla de redacciones históricas y variantes de caja, con duplicados D1 encima | no se «deduplica»: se reconstruye el bloque contra el BOE vigente (diff preparado, pendiente de mandato) |

La grieta que encontró el Auditor (250 palabras duplicadas en la DA18 «sin trazabilidad») no
era un D1 ordinario: al contrastar párrafo a párrafo contra el BOE vivo han salido **17 párrafos
del bloque, 939 palabras**, sin huella en ninguno de los dos BOE (ni el archivado del 09-01, sha
b29db001…, ni el descargado hoy, sha a2f3fe1f…, idénticos entre sí). El bloque actual tiene 22
párrafos / 1.160 palabras; el BOE vigente, 6 / 313. Firmo la taxonomía con esta clase incluida
porque firmarla con la clasificación incompleta sería firmar otra cosa.

## 3. Cuadratura de la firma (cifras del test 2026-09-01 re-verificadas hoy 2026-09-02)

- Registro del test de letras «a)» (evidencia 2026-09-01): **139 marcas / 77 bloques** — este es el titular del acta.
- Casos clasificados en total (F1+F2+F3+F4): **161 casos / 84 bloques con cualquier defecto** — 135 F1 (3.805 palabras perdidas, repartidos en **76 bloques** distintos), 12 F2, 11 F3 y 3 F4 legítimos de BOE sin a).
- Cuadrícula oficial para el acta de esta noche (orden del día presidencial, punto 3): **161 casos / 76 bloques con pérdida de contenido (F1)**. El número «84» es bloques con CUALQUIER defecto de las cuatro clases; «77» son los bloques tocados por el test de marcas. Es la misma data: tres denominadores distintos, cada uno con su nombre, prohibido mezclarlos (regla contable del acta 2026-09-01).
- El acta cita «139» y mi JSON dice «161» porque el titular del acta es de **marcas**, y el manifiesto cuenta **casos** de las cuatro clases. Ambas cifras son las mismas desde ayer; esta firma deja escrito cuál es cuál para que nadie vuelva a cuadrar peras con manzanas.
- Re-verificación de hoy: de los 135 F1, **32 ya restituidos** (test de reejecución: ejecutado y commiteado el 09-01) y **103 siguen ausentes** (2.998 palabras), aparte de 9 F2 y 11 F3.

Firmado: **Arcadi España**, Ministro de Hacienda (Gobierno IA), 2026-09-02, 12:20 — antes de la reejecución del manifiesto masivo de hoy, que se lanza a continuación contra esta regla.
