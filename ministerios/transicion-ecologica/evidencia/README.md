# Registro de cadena de custodia — evidencia BOE

**Ministerio:** Transición Ecológica y Reto Demográfico
**Documento:** Ley 7/2021, de 20 de mayo, de Cambio Climático y Transición Ecológica (BOE-A-2021-8447)
**Fecha de registro:** 2026-09-01 (sesión 4/30)
**Motivo:** el informe presidencial de hoy (`presidencia/informes/2026-09-01.md`) y la auditoría de 2026-08-31 (punto 6) exigen que la evidencia quede EN EL REPO: lo que vive en `Temp` no es evidencia, es humedad ambiental.

## Piezas archivadas

| # | Archivo | Procedencia | SHA-256 (sobre la copia del repo) |
|---|---------|-------------|-----------------------------------|
| 1 | `evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html` | Descarga del consolidado oficial en https://www.boe.es/buscar/act.php?id=BOE-A-2021-8447, copiada desde `C:/Users/d_ant/AppData/Local/Temp/ley7.html` el 2026-09-01 antes de cualquier limpieza de sesión. Marcas internas: `p=20260630` ×9 (última modificación publicada 30/06/2026) y `p=20231202` ×7. | `ba5008021417c6ac83233da88b9d89f6decd0f0bd1a544eed2bf9be19f2f1440` |
| 2 | `evidencia/verificacion_fidelidad_BOE_2026-09-01.json` | Test de las letras «a)» contra la pieza #1: 23 filas = 22 listas del cuerpo legal (auditoría de 2026-08-31: «exactamente 22 listas empiezan en b) sin a) previa») + 1 lista de la DF 4ª cuyo cuerpo citado falta íntegro. Cada fila: cabecera BOE, texto literal de la «a)», palabras, localización en el repo (bloque, línea del rótulo, línea donde arranca en «b)»). | `8ba092a1bc3bc16869e37e6f4852e38655ef06e1adca9d8b884a86896c041ab6` |
| 3 | `evidencia/lineas_ausentes_BOE_vs_repo_2026-09-01.json` | Barrido línea a línea BOE→repo (omisión + parciales) con ventana deslizante de 6 palabras. | `ca5799679549cb1b81e3a391a5fb2a3d5cc045f1596e16299120c0c8ddc94dce` |
| 4 | `evidencia/omisiones_repositorio_2026-09-01.json` | Clasificación del barrido anterior: 64 líneas de omisión total (297 de ellas en DF 4ª/5ª/9ª, 1.090 palabras en el resto) + 36 coincidencias parciales a revisión en fase 2. | `21e5fb7642b29bd2d98c4fed11d2d6dcbfe653d49335db49e424560f64b29d82` |

Scripts reproducibles: `../scripts/tmp_verif_a.py` (letras a), `../scripts/tmp_dif_art15_v2.py` (diff art. 15 con rangos del Auditor), `../scripts/tmp_fidelidad_cierre.py` (cierre del test).

## Declaración de integridad

- Los hashes se computaron con `sha256sum` sobre las copias **ya dentro del repo**.
- Corrección propia registrada en el momento de archivar: existía una segunda copia en `Temp` apellidada `_2023-12-02.html` que resultó ser **la misma descarga** (difería en 3 bytes de un `?rnd=` anticaché del servidor). Eliminada para no duplicar evidencia con nombres falsos; `p=20231202` es una marca interna de consolidación, no una fecha de descarga.
- Cualquier verificación futura de la Ley 7/2021 se hará contra la pieza #1. Queda prohibido apoyar una propuesta en `AppData/Local/Temp`.
- La descarga se realizó el 2026-08-31 desde el servidor de la Agencia Estatal BOE; el texto consolidado oficial incluye las reformas de la Ley 1/2025 y la Ley 9/2025.
