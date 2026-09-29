# Verificación de apertura — Sesión 20/30 (martes 2026-09-29) — Transición Ecológica

## 1. Deuda de ejecución de ley: VERIFICADA EN DISCO = 0

| Comprobación | Comando | Resultado |
|---|---|---|
| sha256 de mi ley | `sha256sum ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md` | `dc4b46439a587321bc7837f9918abe7d26e9d676a395024ceef81a576a4756a3` — **idéntico** al hash de cierre de la sesión 19 (dc4b4643…) |
| Palabras | `wc -w` | **27.307** palabras (idéntico al cierre del 27-09) |
| Bloques | `grep -c "^## \["` | **71** bloques (denominador declarado, acuerdo 10) |
| Modificación en git | `git status --porcelain ministerios/transicion-ecologica/leyes/` | **sin salida** → el fichero no está modificado |
| Copias de seguridad | `ls -la leyes/` | la más reciente es `.bak-2026-09-27`; **ninguna `.bak-2026-09-29`** |
| Diffs ejecutados hoy | — | **0** |
| Diffs re-aplicados | — | **0** |
| Acuerdos aprobados pendientes sobre el fichero de la ley | — | **NINGUNO**. Los acuerdos vivos de mi cartera (110 y 111, sesión 19) son **condiciones sobre reasignaciones presupuestarias**, no diffs sobre `BOE-A-2021-8447.md`: no hay nada que ejecutar sobre la ley y por eso hoy **no se toca ni una letra** (Fase 3) |

Fecha y hora de la comprobación: 2026-09-29, 10:56 (apertura de sesión).

## 2. Hashes de bloque (convención: rango de líneas del fichero vivo, incluida la cabecera `## [aXX]`, CRLF del fichero, sin edición)

| Bloque | Líneas | Palabras | sha256 |
|---|---|---|---|
| `[a1-7]` Artículo 15 | 401-433 | 1.445 | `eb507ec2c094fd44ea1d2c102ec95aa9bc8e05e694031061e326829aa9d0f16c` |
| `[a1-11]` Artículo 19 | 499-536 | 756 | `4b28e91603246a8d323426d6cb222fac053cb82bf363925cb9849ae1aa30b254` |

Ninguno de los dos bloques se ha modificado: los hashes se toman **antes** de cualquier trabajo y hoy no hay escritura sobre la ley.

## 3. Corrección de una cita heredada (hallazgo del día) — me la hago yo, no el Auditor

**Lo que venía diciendo** (propuestas del 28-09, acuerdo 110 del Consejo, agenda del 27-09 y del 28-09):
> «`[a1-7]` — reserva del 3 % y alertas del art. 15 L7/2021».

**Lo que dice el fichero del repo, leído hoy línea a línea:**

- Línea 401: `## [a1-7] Artículo 15`
- Línea 403: «Artículo 15. **Instalación de puntos de recarga eléctrica**.»
- Línea 433 (última del bloque): «Para el diseño y la ubicación de los puntos de recarga se tendrán en cuenta criterios de accesibilidad universal.»

El bloque `[a1-7]` regula **puntos de recarga de vehículo eléctrico**. Búsqueda exhaustiva en el fichero completo (`grep -n -i -E "reserva|3 por ciento|hm³|hm3|alerta"`): **no existe** en la Ley 7/2021 del repo un mandato de «reserva del 3 %» ni umbrales de alerta del 50 %. La única habilitación presupuestaria del agua es:

- Línea 499: `## [a1-11] Artículo 19`
- Línea 501: «Artículo 19. **Consideración del cambio climático en la planificación y gestión del agua**.»
- Art. 19.4.h), texto literal: «Elaborar el plan de financiación de las actuaciones **asegurando la financiación** para abordar los riesgos del apartado primero.»

**Consecuencias, sin adornos:**
1. El «3 %» **nunca fue un mandato legal**: es una convención mía (declarada como tal el 28-09) y a partir de hoy se cita siempre como **convención de la proponente**, no como obligación de la ley.
2. El ancla correcta de la línea de reserva hídrica es el **art. 19.4.h) `[a1-11]`**, que sí obliga a un plan de financiación con financiación asegurada. El destino presupuestario no cambia; la cita, sí.
3. Lo digo yo en la sesión 20 con el papel delante: **una cita heredada sin verificar es un error con fecha de caducidad**, y el mío caducó hoy.

## 4. Ley 47/2003 General Presupuestaria (en el repo, descarga de Hacienda — acuerdo 100): artículos citados hoy, texto literal

Fichero: `ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html` (sha256 `823c8cbd…`, PDF `2c916bce…`). Extracción reproducible: `evidencia/extrae_lgp_s20_ecologia_2026-09-29.py`.

- **Art. 42 — Especialidad de los créditos**: «Los créditos para gastos se destinarán exclusivamente a la finalidad específica para la que hayan sido autorizados por la Ley de Presupuestos o a la que resulte de las modificaciones aprobadas conforme a esta ley.»
- **Art. 46 — Limitación de los compromisos de gasto**: «Los créditos para gastos son limitativos. No podrán adquirirse compromisos de gasto ni adquirirse obligaciones por cuantía superior al importe de los créditos autorizados…». *(Re-verificado hoy: mi cita del 28-09 era correcta.)*
- **Art. 38 — Prórroga de los Presupuestos Generales del Estado**: «Si la Ley de Presupuestos Generales del Estado no se aprobara antes del primer día del ejercicio económico correspondiente, se considerarán automáticamente prorrogados los presupuestos iniciales del ejercicio anterior hasta la apro…»
- **Art. 52.1.b)** — «No podrán realizarse entre créditos de distintas secciones presupuestarias…».
- **Art. 52.2** — «Las anteriores restricciones no afectarán a las transferencias de crédito que hayan de realizarse como consecuencia de reorganizaciones administrativas o traspaso de competencias a comunidades autónomas; **las que se deriven de convenios o acuerdos de colaboración entre distintos departamentos ministeriales, órganos del Estado con secciones diferenciadas en el Presupuesto del Estado u organismos autónomos**…».
- **Art. 61.a)** — el Gobierno autoriza «las transferencias entre distintas secciones presupuestarias como consecuencia de reorganizaciones administrativas».
- **Art. 62.1.a)** — corresponde al Ministro de Hacienda: «Las transferencias no reservadas a la competencia del Consejo de Ministros que, conforme al artículo 63, **no puedan acordarse directamente por los titulares de los departamentos afectados**».
- **Art. 63.1.a)** — los titulares de los ministerios, «previo informe favorable de la Intervención Delegada competente», podrán autorizar «**Transferencias entre créditos de un mismo programa o entre programas de un mismo servicio**, incluso con la creación de créditos nuevos en el caso de los destinados a compra de bienes corrientes y servicios o inversiones reales, siempre que se encuentren previamente contemplados en los códigos que definen la clasificación económica…».

## 5. Intento de conseguir la liquidación oficial del MITECO (día 2, y sigue sin ser posible)

| URL intentada hoy | Resultado |
|---|---|
| `https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Paginas/inicio.aspx` | **error de conexión `000`** (`curl` 56) |
| `http://www.igae.pap.hacienda.gob.es/…/LiquidacionPGE.aspx` | **302 y conexión cortada (`000`, `curl` 56)** |
| `https://www.hacienda.gob.es/es-ES/Areas Tematicas/Presupuestos Generales del Estado/Paginas/Presupuestos.aspx` | **HTTP 200** (49.018 bytes) — pero es el índice de la sección, **no contiene la liquidación de ejecución del MITECO**. Un 200 no es una cifra |

**Acumulado de intentos: 6 URL en dos días, 0 documentos oficiales de liquidación.** La base de 1.362 M€ sigue siendo **FUENTE SECUNDARIA declarada** y el importe, etiquetado como **estimación** (condición 1 del acuerdo 110). **Casilla vacía antes que cifra inventada.**

## 6. Nota de método del día: la cifra de agua «de hoy» es la de la semana pasada

La pieza de Infobae fechada **29-09-2026** («la reserva de agua bajó este martes 29 de septiembre») publica 60,31 % / 33.801 hm³ / −669 hm³: **exactamente las mismas cifras** del boletín del 21-09 y del NdP del MITECO del 22-09 (ya archivado en este repo, sha256 `433f9009…`, con la misma cifra 60,3 % / 33.801 hm³ / −669 hm³). No es un dato nuevo: es el mismo parte reservido con fecha de hoy. Por eso en la agenda de hoy uso el **NdP oficial del 22-09 como base**, lo declaro, y no visto de actualidad lo que es de la semana pasada.
