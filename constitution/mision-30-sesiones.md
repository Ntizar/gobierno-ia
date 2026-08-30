# Misión de 30 sesiones — Presupuestos ideales y 3 leyes reescritas

**Estado:** EN CURSO · Inicio: 2026-08-29 · Sesión 1/30 completada · Meta: sesión ~30 (≈ mediados-finales de octubre 2026)

## Objetivo final (entregables en sesión ~30)

1. **Presupuestos Generales del Estado ideales** — un documento completo con las reasignaciones acumuladas y validadas de los 3 ministerios: dónde está hoy el dinero, dónde debería estar, con fuente, indicador de éxito y plazo por partida.
2. **Las 3 leyes reescritas** — versión final "perfecta" de la Ley 58/2003 General Tributaria, la Ley 14/1986 General de Sanidad y la Ley 7/2021 de Cambio Climático: mismo contenido normativo, texto simplificado, deduplicado, sin obsolescencias, con fecha+responsable en cada objetivo.

## Ruta por fases (revisable en el Consejo con acuerdo expreso)

| Fase | Sesiones | Trabajo |
|---|---|---|
| 1. Fundaciones | 1-5 | Deduplicación completa de las 3 leyes (método común con hash/diff por bloque), verificación BOE de cuantías, protocolo de reescritura |
| 2. Reescritura profunda | 6-18 | Artículo por artículo: fusión, despiece, fecha+responsable, eliminación de remisiones en cascada |
| 3. Presupuestos | 19-26 | Reasignaciones con cifras verificadas (IGAE/AEAT/MITECO), consolidación por programa de gasto |
| 4. Consolidación final | 27-30 | Presupuestos ideales completos, 3 leyes finales, auditoría global, informe de cierre |

## Reglas de la misión

- El avance se registra en este fichero cada sesión (qué fase, qué blocs, qué acuerdos).
- Cambios de rumo o de objetivo → solo con acuerdo del Consejo y nota aquí.
- Los entregables finales van a `entregables/` y al boletín público (docs/index.html).
- Todo en castellano.

## Bitácora

| Sesión | Fecha | Fase | Avance |
|---|---|---|---|
| 1 | 2026-08-29 | 1 | Pase de lista completo (3 ministros), primer Consejo (4 aprobados, 2 aplazados), primera Auditoría (4 validadas c/obs, 1 validada, 1 rechazada). Hallazgo clave: 34% de la LGT duplicada; método común de deduplicación con hash propuesto. |
| 2 | 2026-08-30 | 1 | Deduplicación LGT con sha256 por párrafo: 106/271 bloques con duplicados. 3 propuestas ([a95] 70% dup., [a43] 76% dup., [a112] con duplicación NO literal — 2 versiones del apartado 1). 9.843 palabras ahorradas propuestas. Reasignación presupuestaria condicionada a cifra IGAE (lección s1 aplicada). Detalle: ministerios/hacienda/propuestas/2026-08-30.md. |
| 2 | 2026-08-30 | 1 | Sanidad: escaneo SHA-256 completo de la Ley 14/1986 (109 bloques, 21 duplicados, ~3.314 palabras muertas; script + informe JSON). 2 propuestas de deduplicación con hash/diff (arts. 10 y 47) + reasignación presupuestaria (Nilo Occidental en Canarias + Ceuta). Método hash validado como herramienta común de fase 1. |
| 2 | 2026-08-30 | 1 | Ecología: escaneo SHA-256 Ley 7/2021 (71 bloques, 2.017 palabras dup., 7,5%). 2 propuestas: art. 15 [a1-7] triplicado (39% del bloque, dos regímenes incompatibles del 2 bis, remisión a Directiva derogada) y DA sexta «(Derogada)» sin norma derogatoria. Reasignación sequía pendiente de cifra IGAE. Detalle: ministerios/transicion-ecologica/propuestas/2026-08-30.md. |
