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
| 3 | 2026-08-31 | 1 | Hacienda: [a271] (DA 5ª y bloque, copias de DA 6ª/11ª/18ª/20ª/22ª/23ª/24ª, 5.613 palabras dup.) y [a150] (primera contradicción interna plena: redacción antigua 12+12 meses vs nueva 12/27 conviviendo, nueva ×3). Reasignación con cifra AEAT verificada (148.944 M€ 1S-2026). Detalle: ministerios/hacienda/propuestas/2026-08-31.md. |
| 3 | 2026-08-31 | 1 | Sanidad: 2 propuestas, arts. 18 (817 palabras dup., corazón operativo: 18.5/18.14/18.12) y 35 (292; diferencia real en el 5.ª, Registro Estatal). Hallazgo gratis: numeración incompleta del art. 35 (candidata fase 2). Reejecución del scan como test de aplicación de diffs. Reasignación horas extra → contratos FSE 2027 (ESTIMACIÓN, sin IGAE). Detalle: ministerios/sanidad/propuestas/2026-08-31.md. |
| 3 | 2026-08-31 | 1 | Ecología: barrido hash completo confirma que fuera del art. 15 la Ley 7/2021 está limpia (0 dup. literal/difusa/entre bloques; 71 bloques). 2 propuestas: (1) art. 15 — conservar solo la v3 (la vigente, por remisiones internas), ahorro 2.529 palabras, 9,3% de la ley, elimina la contradicción de plazos 12 vs 21 meses del 2 bis; (2) restitución de 22 letras «a)» omitidas en la conversión al repo, verificadas 22/22 contra el BOE consolidado (incl. principio art. 2 y objetivo −23% del art. 3). Reasignación: sequía Segura/Júcar/Ebro (<57%), cuantía pendiente IGAE. Detalle: ministerios/transicion-ecologica/propuestas/2026-08-31.md. |
| 3 | 2026-08-31 | 1 | Consejo de Ministros 22:00 (acta: consejo/actas/2026-08-31.md): 6 APROBADOS (LGT [a271] y [a150]; LGS arts. 18 c/condición y 35; L7/2021 art. 15 y 22 letras a)), 1 APROBADO CON CONDICIÓN (reasignación Hacienda: concretar programa IGAE antes de Fase 3), 2 APLAZADOS (reasignaciones Sanidad y Ecología sin cifra IGAE). Método común de Fase 1 validado por el Consejo: sha256 por párrafo + BOE consolidado + desglose literal/consolidación. Presidente encarga a Hacienda localizar programas de gasto IGAE para las reasignaciones aplazadas. |
