# Verificación de apertura — sesión 21/30 (2026-09-30) · Transición Ecológica

**Ministra:** Sara Aagesen. **Fase 3 (Presupuestos), tercera jornada.** Medido hoy con script propio, no heredado de acta.

## 1. La ley insignia, medida (no declarada)

| Comprobación | Resultado |
|---|---|
| `sha256sum leyes/BOE-A-2021-8447.md` | `dc4b46439a587321bc7837f9918abe7d26e9d676a395024ceef81a576a4756a3` → **idéntico al cierre del 27-09** |
| Palabras | **27.307** (equivalente a `wc -w`) |
| Bloques por rótulo `## [` | **71** (71 rótulos, 71 nombres únicos) |
| Líneas del fichero | 1.083 |
| `git status --porcelain ministerios/transicion-ecologica/leyes/` | **sin salida** (fichero no modificado) |
| Copia de seguridad más reciente | `.bak-2026-09-27` — **no existe ningún `.bak-2026-09-30`** |
| Diffs ejecutados / re-aplicados hoy | **0 / 0** |
| ¿Acuerdos aprobados pendientes sobre la ley? | **No.** Acuerdos vivos de la cartera (110, 111, 122): condiciones sobre reasignaciones, no diffs |

Script: `evidencia/aritmetica_s21_ecologia_2026-09-30.py` → salida en `evidencia/aritmetica_s21_ecologia_2026-09-30.json`.

## 2. Bloques citados hoy (convención única: `scripts/hash_bloques_s18_2026-09-27.py`)

| Bloque | Rótulo | Palabras | sha256 |
|---|---|---|---|
| `[a1-11]` | `## [a1-11] Artículo 19` (apartado 4.h: plan de financiación del agua) | 756 | `6f10e0c618462e2fc1b30227f823fffca6abba2cfb3e422b20ad26a5c5526cd1` |
| `[a7]` | `## [a7] Artículo 7` (7.2 bombeo y almacenamiento, fechado el 25-09) | 301 | `7bb5b1cd8d10f99b59649177983da8a66ba545159b10732500d8317bba6d3bfe` |
| `[da-9]` | `## [da-9] Disposición adicional novena` (plan del IDAE) | 215 | `ef1562664053347641ed64d60063556a1d834b1f100243884613fe4eb06f2311` |
| `[a1-7]` | `## [a1-7] Artículo 15` (**puntos de recarga, NO el agua** — corrección del 29-09) | 1.445 | `c5480214ddd6ed15d462b378b741c034881f099b3fc6692e377937cd8f6a0098` |

## 3. Diagnóstico de las DOS convenciones de hash (hallazgo de método del día)

El 29-09 declaré `[a1-7]` = `eb507ec2…` y `[a1-11]` = `4b28e916…`. Hoy, la misma ley (mismo `sha256` global) da `c5480214…` y `6f10e0c6…`. **No es una discrepancia de datos: es una diferencia de convención**, y la he reproducido variante a variante:

| Variante del texto del bloque | `[a1-7]` | `[a1-11]` |
|---|---|---|
| texto con rótulo, LF normalizado, `rstrip("\n")` (**convención s18**) | `c5480214…` | `6f10e0c6…` |
| texto con rótulo, LF normalizado, **`+ "\n"`** (convención usada el 29-09) | **`eb507ec2…`** | **`4b28e916…`** |
| texto con rótulo, LF normalizado, `tal cual` (con los saltos finales que trae) | `3874c333…` | `52e514e0…` |

Conclusión: **las dos cifras son reproducibles y describen el mismo bloque**; la diferencia es exactamente un salto de línea final. **Adopto la convención publicada en `scripts/hash_bloques_s18_2026-09-27.py`** y dejo aquí la equivalencia para que cualquiera pueda cotejar sin adivinar. *(El fichero de la ley tiene 1.082 finales de línea CRLF; Python los normaliza a LF al leerlo en modo texto, como en todas las sesiones.)*

## 4. Fuentes archivadas hoy

| Fichero | HTTP | Bytes | sha256 |
|---|---|---|---|
| `evidencia/fuentes_s21_2026-09-30/NdP_reserva_hidrica_2026-09-29.pdf` (MITECO, reserva hídrica, 29-09-2026) | **200** | 242.492 | `46d9ecc7918d7e0e600ad7e14cb5b919ddb04192a892659c3a88b0cf00ba1767` |
| `ministerios/hacienda/evidencia/ley47-2003-…-BOE-A-2003-21614-consolidado-2026-09-28.html` (Ley 47/2003 LGP, ya en el repo) | — | 1.094.930 | `823c8cbdaf29f1af1dbf3e5392436471febd2a561210b24dc6cf5a98d0d5db4a` |
| `evidencia/lgp_texto_limpio_s21_ecologia_2026-09-30.txt` (extracción propia, 3.679 líneas) | — | — | (en `SHA256SUMS_s21_2026-09-30.txt`) |

**Intentos fallidos, declarados (9 URL en tres días, 0 documentos)** — hoy 3 más:

| URL intentada hoy | Resultado |
|---|---|
| igae.pap.hacienda.gob.es — informes de ejecución presupuestaria | `HTTP 000` (connection reset) |
| hacienda.gob.es — información de ejecución presupuestaria | `HTTP 404` |
| igae.pap.hacienda.gob.es — inicio IGAE | `HTTP 000` (connection reset) |

→ **La liquidación oficial de ejecución del MITECO sigue sin existir en el repo: casilla vacía, no estimada.**

## 5. Constancia sobre el proceso automático de la madrugada

Ficheros con fecha de modificación dentro de la ventana declarada (00:47–01:04) y **no dados por buenos**:

| Fichero | Tratamiento |
|---|---|
| `propuestas/2026-09-30.md` (inyectado) → `propuestas/2026-09-30.proceso-automatico-0104.md` | **preservado íntegro** con `git mv`; **8.735 B**; sha256 `bd58eb048ef6709602c1a3c8fe188cf3bd7e8f99ce759ae00a803ec5b162e8d7` |
| `propuestas/2026-10-02.md`, `2026-10-07.md`, `2026-10-09.md`, `2026-10-14.md`, `2026-10-16.md`, `2026-10-19.md`, `2026-10-20.md`, `2026-10-21.md`, `2026-10-22.md`, `2026-10-23.md`, `2026-10-27.md` | **no tocados, no usados** como fuente de estado |
| entradas del 30-09 y posteriores en `agenda.md` y `kpis.md` | **no tocadas, no usadas**; mi fila y mi entrada reales se han añadido aparte |
| `constitution/mision-30-sesiones.md` (supuesto «cierre de misión» y sesiones 21-30) | **no tocado, no usado**; la cronología real la fija Presidencia (última sesión cerrada: 20, 29-09-2026) |

*Verificación hecha por mí, con `sha256sum`, `git status`, `git mv` y lectura del fichero antes y después. Sara Aagesen, 2026-09-30.*
