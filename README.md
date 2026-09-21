# Gobierno IA 🇪🇸

**Simulación multiagente de un gobierno de España creado con IA, cuyo objetivo es un Estado al máximo de simple: legislación eficaz, corta y clara, y el dinero donde hay problemas medidos.**

> ⚠️ **Proyecto de experimentación — no es uso jurídico.** Los "ministros" son agentes de IA con personalidad inspirada en los ministros reales (Arcadi España, Mónica García, Sara Aagesen) pero **no** son ellos ni representan al Gobierno de España. Los textos legales son reales (BOE); las propuestas y los acuerdos, ficticios y en pilota humano: los ficheros de ley del repo han sido modificados por los agentes bajo su propio protocolo de ejecución y **no sustituyen a la publicación oficial**.

**Estado (2026-09-21, sesión 13/30 · 43 %):** Fase 2 (reescritura profunda) · deuda de ejecución 16 → **5** acuerdos (los 5 restantes bloqueados por condición: cifra IGAE o verificación legal) · **−9.247 palabras ejecutadas en la sesión 13** (LGT −9.232 · LGS −11 · L7 −4) · **0 €** de reasignación validada con sello IGAE en 13 sesiones (declarado: es el mayor riesgo de la Fase 3). Detalle vivo en [`constitution/mision-30-sesiones.md`](constitution/mision-30-sesiones.md).

## La misión (30 sesiones)

Un experimento con fecha de cierre: ~sesión 30 (mediados-finales de octubre de 2026). Dos entregables:

1. **Presupuestos Generales del Estado ideales** — reasignaciones acumuladas y validadas de los 3 ministerios: dónde está el dinero, dónde debería estar, con fuente, indicador de éxito y plazo por partida.
2. **Las 3 leyes reescritas** — versión final "perfecta" de la Ley 58/2003 General Tributaria, la Ley 14/1986 General de Sanidad y la Ley 7/2021 de Cambio Climático: mismo contenido normativo, texto simplificado, deduplicado, sin obsolescencias, con fecha+responsable en cada objetivo.

| Fase | Sesiones | Trabajo |
|---|---|---|
| 1. Fundaciones | 1-5 | Deduplicación completa con sha256, verificación BOE de cuantías, protocolo de reescritura — cerrada con prórroga técnica en la 6 |
| 2. Reescritura profunda | 6-18 | Artículo por artículo: fusión, despiece, fecha+responsable, eliminación de remisiones en cascada — **en curso (13)** |
| 3. Presupuestos | 19-26 | Reasignaciones con cifras verificadas (IGAE/AEAT/MITECO) |
| 4. Consolidación final | 27-30 | Presupuestos ideales, 3 leyes finales, auditoría global, informe de cierre |

El avance se registra sesión a sesión en la bitácora de `mision-30-sesiones.md`, con una **tabla de deuda de ejecución** (qué acuerdo aprobado está ya aplicado sobre la ley y cuál no) y notas presidenciales de ritmo y meta.

## Cómo funciona el día

Todo está orquestado con perfiles de Hermes Agent + cron (los prompts viven en [`constitution/prompts-cron/`](constitution/prompts-cron)):

1. **≈10:00 — Pase de lista.** Cada ministro busca 2-3 noticias **reales del día** de su área (`web_search`) y las anota en su `agenda.md` con reacción personal y bloque afectado; revisa su ley; escribe 1-3 propuestas en `ministerios/<m>/propuestas/YYYY-MM-DD.md` y una **reasignación presupuestaria** (de X € → a Y € con fuente, indicador de éxito y plazo — cifra sin fuente la rechaza el Auditor). Actualiza su fila de `kpis.md`.
2. **22:00 — Consejo de Ministros.** 3 rondas: exposición de la propuesta estrella → réplica cruzada (solapes, contradicciones, test cruzado) → decisión del Presidente: APROBADO / APLAZADO / RECHAZADO, con motivo. Acta en `consejo/actas/`.
3. **23:30 — Auditoría del Estado.** Un auditor independiente valida o rechaza cada acuerdo y los KPIs, y señala los 3 mayores riesgos no atendidos. Veredictos en `auditoria/`.
4. **08:00 — Informe presidencial** (máx. 2 páginas): lo importante, qué se simplificó, qué está atascado, cuadro de KPIs. En `presidencia/informes/`; se publica en el boletín (abajo).

**Cada noche, además, cada ministro escribe entrada personal en su `diario.md`** (protocolo de emoción: la simulación está "habitada"; el Presidente usa el clima, nadie lee pasajes en voz alta). Y los viernes, ⚗️ **Laboratorio**: una medida disruptiva sin cita BOE, etiquetada.

## Reglas de verificación (lo que hace esto distinto de un chatbot escribiendo leyes)

- **Fuente única de verdad**: los textos legales son reales, del BOE (Legislación Consolidada), congelados y con cadena de custodia en `data/raw/boe/` y `data/canonical/` — [`scripts/verify_immutability.py`](scripts/verify_immutability.py) comprueba que ningún script del repo escribe ahí.
- **Toda propuesta cita identificador BOE + bloque `[aNNN]` exacto del fichero.** Sin cita verificable → rechazada. Prohibido citar leyes que no estén en el repo.
- **Método común Fase 1**: sha256 por párrafo para detectar duplicación literal + contraste contra el BOE consolidado archivado (halló, p. ej., 939 palabras de texto sin traza en ningún BOE y 239 letras «a)» perdidas por la conversión).
- **Regla de ejecución (desde 21-09): ejecutar antes de proponer.** Los acuerdos aprobados se aplican **el mismo día** sobre el fichero de la ley con copia `.bak-YYYY-MM-DD`, sha256 antes/después y **manifiesto JSON** en `ministerios/<m>/evidencia/`, con verificación de que el bloque queda con una sola copia y **prohibido re-aplicar un diff ya ejecutado** (se comprueba el hash del bloque primero). Verificación presidencial independiente con [`scripts/verifica_diffs_s13.py`](scripts/verifica_diffs_s13.py).
- **Test cruzado y ciego (acuerdo 32, permanente):** cada ministro audita la ley del otro sin leer manifiestos ni propuestas — solo el fichero y el BOE archivado. Encontró ya un defecto grave que nadie había visto (apartado 1 del art. 16 LGS perdido, restituido el mismo día). Los informes salen en `consejo/evidencia/`.
- **Fidelidad ≠ ahorro**: restituir texto legal perdido se registra aparte del adelgazamiento (una propuesta puede *engordar* un bloque y ser mejor ley).
- **Los cambios se aplican como diffs de git**, auditables por cualquiera: `git log -- ministerios/*/leyes/`.

## El equipo

| Agente | Perfil Hermes | Cartera | Ley insignia (bloques) |
|---|---|---|---|
| 🏛️ Presidente | mastermind (orquestador) | Coordina, arbitra, informa, verifica en repo | — |
| 💼 Hacienda | `ministro-hacienda` — Arcadi España (IA) | Tributos, presupuestos, financiación | Ley 58/2003 General Tributaria (335) |
| 🏥 Sanidad | `ministro-sanidad` — Mónica García (IA) | Salud pública, SAN, farmacia | Ley 14/1986 General de Sanidad (151) |
| 🌱 Transición Ecológica | `ministro-ecologia` — Sara Aagesen (IA) | Clima, energía, medio ambiente | Ley 7/2021 Cambio Climático (71) |
| 🔍 Auditor del Estado | `auditor` | Fiscaliza todo, no propone nada | — |

Corpus total de la misión: **557 bloques**. Duplicación literal tras la sesión 13: LGT 0,00 % (queda el inventario F1 de *fidelidad*: 115 casos / 69 bloques / 3.071 palabras), LGS 5,07 % (1.140 palabras / 16 bloques), L7 0,00 %.

## Las leyes que se mejoran

Descargadas de la [API de Legislación Consolidada del BOE](https://www.boe.es/datosabiertos/) y convertidas a markdown con verificación de fidelidad (la conversión inicial perdió letras «a)» y párrafos que hoy se están restituyendo):

- [`ministerios/hacienda/leyes/BOE-A-2003-23186.md`](ministerios/hacienda/leyes/BOE-A-2003-23186.md) — Ley 58/2003, General Tributaria
- [`ministerios/sanidad/leyes/BOE-A-1986-10499.md`](ministerios/sanidad/leyes/BOE-A-1986-10499.md) — Ley 14/1986, General de Sanidad
- [`ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md`](ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md) — Ley 7/2021, de Cambio Climático y Transición Ecológica

## KPIs

Cada ministro gestiona su cuadro de mando evolutivo en `ministerios/<nombre>/kpis.md` (fila diaria + lecciones; un KPI sin dato actualizado cuenta como fallo del día). El Auditor los audita. Ejemplo: [`ministerios/hacienda/kpis.md`](ministerios/hacienda/kpis.md).

## Estructura del repo

```
constitution/     Reglas del juego: constitución, protocolos (ministro, emoción,
                  laboratorio, presupuesto), misión-30-sesiones.md y prompts-cron/
data/             Corpus inmutable: raw/boe/ (HTML oficial) y canonical/ (JSON parseado)
ministerios/      Por ministerio: leyes/ (BOE editable), propuestas/, evidencia/
                  (manifiestos sha256), agenda.md, kpis.md, diario.md
consejo/          Actas del Consejo (actas/), rondas y evidencia del test cruzado
auditoria/        Veredictos del Auditor del Estado + diario
presidencia/      Informes presidenciales diarios (informes/)
scripts/          scan_duplicacion · parse_boe_canonical · verify_immutability ·
                  verifica_diffs · generar_boletin (y los de ejecución por sesión)
docs/             Boletín público (GitHub Pages), generado por scripts/generar_boletin.py
```

## Ver el boletín diario

👉 **https://ntizar.github.io/gobierno-ia/** — propuestas de cada día, acuerdos con badge (APROBADO/APLAZADO/RECHAZADO), veredictos del Auditor, KPIs y lo importante del informe presidencial. Se regenera con `python scripts/generar_boletin.py`.

---
Hecho con ❤️ por David Antizar · Mastermind es el ejecutor, David el autor
