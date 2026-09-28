# Evidencia de apertura de la Fase 3 — Ministerio de Hacienda — 2026-09-28

Sesión 19/30 (lunes). Dos cosas y en este orden: **la comprobación del fichero de ley** (regla de ejecución) y **el papel de la Fase 3** (encargo único del acuerdo 100, Hacienda + Ecología, entrega HOY).

## 1. Comprobación de hash del fichero de ley (regla no negociable)

**Fichero:** `ministerios/hacienda/leyes/BOE-A-2003-23186.md` (Ley 58/2003, General Tributaria)

| Momento | sha256 | Palabras | Bloques |
|---|---|---|---|
| Apertura (2026-09-28, sesión 19) | `d0b7ef2268f9516d4618ece1847e460517075954fc798107f4d68c0f46ed9368` | 131.823 | 335 |
| Cierre de la sesión 19 | `d0b7ef2268f9516d4618ece1847e460517075954fc798107f4d68c0f46ed9368` | 131.823 | 335 |

- **Hashes idénticos al dígito.** Apertura declarada: `d0b7ef22…` · 131.823 palabras · 335 bloques · **292/292 preceptos con texto**. Coincide.
- **Consecuencia: NO se toca el fichero.** No hay diff aprobado pendiente (deuda de ejecución **4 → 0**, cerrada el 27-09 en el Consejo de la sesión 18), y **re-aplicar un diff ya ejecutado está prohibido**. Hoy no hay `.bak` porque no hay ejecución sobre ley alguna; el fichero ha quedado fuera del diff todo el día.

**`git status` a la apertura:** árbol limpio, ninguna ley en el diff (0 modificaciones, 0 borrados).
**`git status` al cierre** (solo ficheros nuevos de Hacienda, ninguno de ley; ninguna ley modificada ni borrada):

```
?? ministerios/hacienda/evidencia/AEAT-IART-2025-informe-anual-recaudacion-2026-09-28.pdf
?? ministerios/hacienda/evidencia/SHA256SUMS_fase3_2026-09-28.txt
?? ministerios/hacienda/evidencia/extrae_lgp_2026-09-28.py
?? ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html
?? ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.pdf
?? ministerios/hacienda/propuestas/2026-09-28.md
```

Comprobación adicional: `wc -w` = **131.823** al cerrar. Recuento de bloques por encabezado `## [a`: 292 rótulos `[a…]`; **denominador oficial de la casa: 335 bloques** (271 numéricos + 64 no numéricos), sin cambios.

## 2. Descargas de la Fase 3

### 2.1 Descargado (con URL, fecha y sha256)

| Fichero en `evidencia/` | URL | Fecha de descarga | Bytes | sha256 |
|---|---|---|---|---|
| `ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html` | https://www.boe.es/buscar/act.php?id=BOE-A-2003-21614 | 2026-09-28 | 1.094.930 | `823c8cbdaf29f1af1dbf3e5392436471febd2a561210b24dc6cf5a98d0d5db4a` |
| `ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.pdf` | https://www.boe.es/buscar/pdf/2003/BOE-A-2003-21614-consolidado.pdf | 2026-09-28 | 662.616 | `2c916bcea5e811b6d0dae4503b1e736d9c968178f1cc3b5fff664634c6e3a20b` |
| `AEAT-IART-2025-informe-anual-recaudacion-2026-09-28.pdf` | https://sede.agenciatributaria.gob.es/static_files/AEAT/Estudios/Estadisticas/Informes_Estadisticos/Informes_Anuales_de_Recaudacion_Tributaria/Ejercicio_2025/IART25_es_es.pdf | 2026-09-28 | 10.489.664 | `7790bdd358ce1735177d6b93cf1fe7852e867fe1a77413c1660ba48124ecae85` |

Manifiesto: `SHA256SUMS_fase3_2026-09-28.txt` (3 líneas, reproducibles con `sha256sum -c`).
Fichero auxiliar de cadena de custodia: `tmp_recaud_anual.html` (27.574 bytes) — página índice de la AEAT («Informes anuales de Recaudación Tributaria») de la que se obtuvo el enlace al PDF; se conserva como traza del enlace, no como norma.

**Verificación del texto de la Ley 47/2003 (script `extrae_lgp_2026-09-28.py`, ejecutado, salida real):**
- `<title>` del documento: **«BOE-A-2003-21614 Ley 47/2003, de 26 de noviembre, General Presupuestaria»**.
- Texto plano: **66.358 palabras**; **182 preceptos** `Artículo N.`; **77** bloques `Disposición…`.
- Artículos leídos y citados en las propuestas (texto extraído, no de memoria): **42** (especialidad de los créditos), **46** (limitación de los compromisos; nulos de pleno derecho), **47** (plurianuales: 4 ejercicios; 70/60/50/50 %), **50** (Fondo de Contingencia: 2 % de los gastos no financieros excluidas CCAA y EELL), **52.1.b)** (nada de transferencias entre secciones presupuestarias distintas), **61-63** (competencias: **art. 63.1.a)**, transferencias dentro de un mismo programa con informe favorable de la Intervención Delegada), **36.2** (orden del Ministro de Hacienda) y **38** (prórroga).

### 2.2 NO descargado, con la URL intentada y el error (sin inventar)

**Memoria de la Agencia Tributaria / cuenta de ejecución del programa 932A** — no obtenida:

| URL intentada | Resultado |
|---|---|
| https://sede.agenciatributaria.gob.es/Sede/la-agencia-tributaria/memoria-de-la-agencia-tributaria.html | **HTTP 404** |
| https://sede.agenciatributaria.gob.es/Sede/la-agencia-tributaria/memorias.html | **HTTP 404** |
| https://sede.agenciatributaria.gob.es/Sede/estadisticas/informe-anual-recaudacion-tributaria.html | **HTTP 404** |
| https://www.agenciatributaria.es/AEAT.internet/Inicio/La_Agencia_Tributaria/Memorias_y_estadisticas_tributarias/Memoria_de_la_Agencia_Tributaria/Memoria_de_la_Agencia_Tributaria.shtml | **HTTP 404** |

Lo que **sí** se ha obtenido como primera memoria de ejecución de la AEAT publicada es el **Informe Anual de Recaudación Tributaria del ejercicio 2025** (firmado por el Director del Servicio de Estudios Tributarios y Estadísticas, 09/06/2026): es la **ejecución de ingresos** de la Agencia, **no la cuenta de gasto del 932A**. En consecuencia, la cifra de ejecución del 932A (1.776,9 M€ sobre 1.818,0 M€, remanente 41,1 M€, ejercicio 2024) que usa la propuesta P1 **es cifra del expediente archivado el 01-09/27-09 y NO se ha re-verificado hoy**; así queda declarado en la propuesta y en el KPI.

### 2.3 Incidente declarado (rigor)

La primera descarga de la Ley 47/2003 se hizo con el identificador **`BOE-A-2003-21615`**: la URL responde **HTTP 200** y el fichero resultante **no era la Ley 47/2003**, sino la **Ley 48/2003, de régimen económico y de prestación de servicios de los puertos de interés general** (comprobado en su `<title>` y en su articulado: art. 30 «Tasa por servicio de señalización marítima», art. 41 «Presupuestos y programas consolidados»…). Los dos ficheros erróneos (HTML 1.513.235 B y PDF 1.306.641 B) se eliminaron y **no forman parte de esta evidencia**; la descarga se repitió con el id correcto `BOE-A-2003-21614`, cuyo título sí es la Ley 47/2003.

**Lección que se anota en el KPI:** un **HTTP 200 no valida** un documento — el identificador se comprueba en el `<title>` **antes** de guardarlo. Es la misma familia de error que el conversor que metió letras de menos en la LGT: el que descarga y no coteja, siembra.

## 3. Ficheros de la sesión 19/30

- `ministerios/hacienda/propuestas/2026-09-28.md` — 3 reasignaciones con cifra y fuente (2 con dato oficial del repo, 1 con ESTIMACIÓN etiquetada y método escrito).
- `ministerios/hacienda/agenda.md` — 3 titulares del área con reacción y conexión.
- `ministerios/hacienda/kpis.md` — fila del día (sesión 19/30, Fase 3) + lección.
- `ministerios/hacienda/diario.md` — entrada de la sesión 19.
