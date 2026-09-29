# Evidencia Fase 3 — Sanidad — 2026-09-29 (sesión 20/30)

Fuentes descargadas HOY 29-09-2026 y archivadas en el repo **antes** de escribir las propuestas del día.
Regla propia (heredada de la R2 del 28-09 y del correctivo del 29-09): **la base de una cifra se cita del documento, nunca del titular.**

| Fichero | URL | Fecha de la fuente | HTTP | sha256 |
|---|---|---|---|---|
| `sanidad.gob.es-nota-6904-salud-mental-56.830.000eur-2026-05-12.html` | https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=6904 | 12-05-2026 (nota oficial) | 200 | `d4b10c14693ebc5a5d4764ae59ab25b23172cfd0a0ca7db2c2e8bf2f74350ea8` |
| `sanidad.gob.es-nota-6904-gl-salud-mental-2026-05-12.html` | https://www.sanidad.gob.es/gl/gabinete/notasPrensa.do?id=6904 | 12-05-2026 (copia GL, control cruzado) | 200 | `e67cb8bb228ec94d0a3c0df4cce8923e620e2cb983ee90d3cd3b0d60bb28f3ec` |
| `opinandosinanestesia-interterritorial-2oct-50.268.707,0746eur-2026-09.html` | https://opinandosinanestesia.es/2026/09/sanidad-intensifica-su-ofensiva-con-las-listas-de-espera-y-convoca-un-interterritorial-para-el-2-de-octubre/ | septiembre 2026 (**fuente secundaria**) | 200 | `2cf6d09bdafd1cbca1123ba611af46bd066afbea5b5d84a0e3e162c3d3d37a28` |
| `gacetamedica-claves-interterritorial-2oct-2026-09.html` | https://gacetamedica.com/politica/claves-proximo-interterritorial-listas-espera-sivain-reparto-fondos-autonomicos/ | septiembre 2026 (**fuente secundaria**) | 200 | `8b04d42442846ca0020491b91752b24271290db5708d0251e4ccc7ce08850ea2` |
| `immedicohospitalario-235.449.950eur-2026-07-13.html` | https://www.immedicohospitalario.es/noticia/57319/sanidad-moviliza-235-millones-para-reforzar-los-servicios-publicos-de.html | 13-07-2026 (**fuente secundaria**) | 200 | `7a44a084e3823b1c56908b3df480303457b3d020da0d6fdba878197d2a522810` |

## Qué sostiene cada una (lo que se citó en `propuestas/2026-09-29.md`)

- **F1/F2 (oficiales)** — línea madre de salud mental y prevención del suicidio **2026 = 56.830.000 €** (39.000.000 € + 17.830.000 €). **Corrige el «57 M€» redondeado** con el que el 28-09 firmé «5,7 M€»: el 10,000 % exacto son **5.683.000 €**.
- **F3** — orden del día del Interterritorial del 2 de octubre: reparto de **50.268.707,0746 €** (cohesión sanitaria, formación de médicos/odontólogos/farmacéuticos/enfermeros y educación sanitaria).
- **F4** — los dos bloques del 2-O (RD del Sistema de Información de Listas de Espera + acuerdos de distribución de créditos) y el **plazo de alegaciones de las CCAA hasta el miércoles 30-09**.
- **F5** — **235.449.950 €** aprobados por el Pleno del Interterritorial del 13-07-2026: 172.425.000 € (Atención Primaria y Comunitaria) + 60.058.000 € (salud bucodental) + 2.006.950 € (sistemas de información del SNS) + 960.000 € (enfermería).

## Comprobaciones aritméticas propias (no copiadas de ninguna fuente)

- 39.000.000 + 17.830.000 = **56.830.000 €** → 10,000 % = **5.683.000 €**; línea madre restante **51.147.000 €**.
- 172.425.000 + 60.058.000 + 2.006.950 + 960.000 = **235.449.950 €** (cuadra al euro con F5).
- 235.449.950 + 50.268.707,0746 = **285.718.657,0746 €** repartidos en un año → sistemas de información = **0,70 %** (2.006.950 ÷ 285.718.657,0746).
- 5,0 % de 60.058.000 = **3.002.900 €** → línea de sistemas de información: 2.006.950 → **5.009.850 €**; bucodental restante **57.055.100 €**.
- Diferencial de coste por alta: 8.758,7 − 6.699,0 = **2.059,7 €** → 10.000 altas = **20.597.000 €**; 50.000 = **102.985.000 €**; 100.000 = **205.970.000 €**.
- Control del rango de **[acuatro]** archivado ayer: 853.740 × 6.699,0 = **5.719,204 M€** y × 8.758,7 = **7.477,653 M€** → reproduce el rango declarado **5.719–7.478 M€** (coincidencia al dígito con la ejecución del 27-09).

## Descargas fallidas

**Ninguna: 5/5 HTTP 200.** Si alguna hubiera fallado, aquí figuraría la URL intentada y el error devuelto. No hay error que declarar.

## Límites declarados (no se cruzan)

- F3, F4 y F5 son **prensa especializada**, no boletines oficiales: se usan para fechas, orden del día e importes de acuerdos ya aprobados, y van etiquetadas como secundarias en la propuesta.
- La liquidación oficial de los acuerdos de distribución y el **importe de la línea de conciertos** siguen **NO VERIFICADOS**: no se estiman, se piden con fecha (31-10-2026).
