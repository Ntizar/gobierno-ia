# Gobierno IA 🇪🇸

**Simulación multiagente de un gobierno de España creado con IA, cuyo objetivo es un Estado al máximo de simple: legislación eficaz, corta y clara, y el dinero donde hay problemas medidos.**

> ⚠️ **Proyecto de experimentación — NO PARA USO JURÍDICO.** Los "ministros" son agentes de IA con personalidad inspirada en los ministros reales (Arcadi España, Mónica García, Sara Aagesen) pero **no** son ellos ni representan al Gobierno de España. El texto legal oficial está **congelado y verificado por hash** en `data/`; las copias de trabajo de los agentes están etiquetadas como mutadas y **no sustituyen a la publicación oficial** (un test de integridad vigila que ninguna etiqueta mienta).

**Estado (2026-09-21, sesión 13/30 · 43 %):** Fase 2 de la misión (reescritura profunda) · deuda de ejecución 16 → **5** acuerdos (los 5 restantes bloqueados por condición: cifra IGAE o verificación legal) · **−9.247 palabras ejecutadas en la sesión 13** · **0 €** de reasignación validada con sello IGAE (declarado como riesgo de la Fase 3) · y el mismo 21-09 quedó fusionado el **rescate de ingeniería**: corpus inmutable + parches versionados + 45/45 tests + CI. Bitácora viva: [`constitution/mision-30-sesiones.md`](constitution/mision-30-sesiones.md) · informe del rescate: [`reports/rescate/resultado-final.md`](reports/rescate/resultado-final.md).

## Las dos capas del proyecto

### 1. Capa de simulación de gobierno (el experimento diario)

Todo está orquestado con perfiles de Hermes Agent + cron (prompts en [`constitution/prompts-cron/`](constitution/prompts-cron)); el avance se mide en una misión de 30 sesiones (~octubre 2026) con dos entregables: **Presupuestos Generales ideales** (reasignaciones con fuente, indicador y plazo) y **las 3 leyes reescritas** (mismo contenido normativo, texto simplificado, deduplicado, fecha+responsable en cada objetivo).

| Hora | Qué pasa | Dónde queda |
|---|---|---|
| ≈10:00 | **Pase de lista**: cada ministro busca 2-3 noticias **reales del día** de su área, revisa su ley y escribe propuestas frase por frase + una **reasignación presupuestaria** (de X € → a Y € con cifra y fuente; sin fuente, el Auditor la rechaza). Actualiza su fila de KPIs. | `ministerios/<m>/agenda.md`, `propuestas/YYYY-MM-DD.md`, `kpis.md` |
| 22:00 | **Consejo de Ministros**: 3 rondas (exposición → réplica cruzada → decisión presidencial): APROBADO / APLAZADO / RECHAZADO con motivo. | `consejo/actas/` |
| 23:30 | **Auditoría del Estado**: un auditor independiente valida o rechaza cada acuerdo y los KPIs, y señala los 3 mayores riesgos no atendidos. | `auditoria/` |
| 08:00 | **Informe presidencial** (máx. 2 páginas): lo importante, qué se simplificó, qué está atascado, cuadro de KPIs — con los fallos, no solo los éxitos. | `presidencia/informes/` → boletín |

Además: cada noche el ministro escribe **diario personal** en `ministerios/<m>/diario.md` (protocolo de emoción: la simulación está habitada; el Presidente lee el clima, nadie cita pasajes) y los viernes hay ⚗️ **Laboratorio**: una medida disruptiva sin cita BOE, etiquetada (`constitution/protocolo-laboratorio.md`).

**Regla de ejecución (vigente desde el 21-09): ejecutar antes de proponer.** Los acuerdos aprobados se aplican **el mismo día** sobre la copia de trabajo de la ley con copia `.bak-YYYY-MM-DD`, sha256 antes/después y **manifiesto JSON** en `ministerios/<m>/evidencia/`, con verificación de que el bloque queda con una sola copia; **prohibido re-aplicar un diff ya ejecutado** (se comprueba el hash del bloque primero). Verificación presidencial independiente: `scripts/verifica_diffs_s13.py`.

**Test cruzado y ciego (acuerdo 32, permanente):** cada ministro audita la ley del otro **sin leer manifiestos ni propuestas** — solo el fichero y el BOE archivado. Ya encontró un defecto grave invisible para todos (apartado 1 del art. 16 LGS perdido; restituido el mismo día). Informes: `consejo/evidencia/`.

**Fidelidad ≠ ahorro:** restituir texto legal perdido se registra aparte del adelgazamiento; una propuesta puede *engordar* un bloque y aun así ser mejor ley.

### 2. Capa de verificación e ingeniería (el rescate de 2026-09-21)

Un auditoría interna (inventario de 388 ficheros, 12 anomalías) terminó en 8 fases de rescate: el proyecto ahora es **reproducible y con fronteras de datos honestas**.

```
BOE API ──► data/raw/boe/<id>/          HTML oficial CONGELADO + metadata.json con sha256
        ──► data/canonical/<id>/        JSON parseado canónico (292 + 117 + 41 artículos)
                     │
ministerios/<m>/leyes/*.md   copia de trabajo MUTADA de la simulación (etiquetada como tal)
                     │
propuesta aprobada ──► parche versionado (ProposalPatch: hash base, artículo, operación)
                 ──► gobierno_ia/validate → apply (solo escribe en runs/, nunca en data/)
                 ──► audit-run → build-report
```

- **El BOE no se muta**: `scripts/verify_immutability.py` (hashes raw+canonical) y `scripts/verify_no_writes_to_raw.py` (escaneo de escrituras en código) pasan en verde y corren en CI.
- **Etiquetas honestas**: `tests/test_label_integrity.py` verifica que ningún fichero se presente como «texto oficial».
- **Parches versionados** (paquete Python `gobierno_ia`, instalable, CLI `gobierno-ia`): `ingest-boe · validate-proposal · apply-patch · audit-run · build-report`; máquina de estados de propuesta validada con transiciones ilegales rechazadas.
- **Gold set**: 20 fragmentos legales con 6 tipos de violación tipificados (`gobierno_ia/gold_set.json`) — ⏳ **esperando revisión jurídica humana**.
- **Suite y CI**: `pytest tests/` → **45/45 en verde**; GitHub Actions: install limpio → verificadores → tests.
- **Ledger de corrupción** (`scripts/corruption_ledger.py`, resumen en `reports/rescate/`): contabilidad honesta de lo que el pipeline experimental cambió sobre el corpus original — 13.367 palabras de duplicación, 50 de omisión y 19.334 de cambio editorial en las copias LGT/LGS/L7. **Ninguna de esas cifras es «ahorro normativo»**: son cicatrices declaradas, no mérito.
- **Producto acotado**: piloto **PMUS / Movilidad 15 min** (Madrid) como caso de uso — ⏳ pendiente de validación con 5 usuarios + 1 técnico + 1 jurista.

## Los agentes

| Agente | Perfil Hermes | Cartera | Ley insignia (bloques de la copia de trabajo) |
|---|---|---|---|
| 🏛️ Presidente | mastermind (orquestador) | Coordina, arbitra, informa, verifica en repo | — |
| 💼 Hacienda | `ministro-hacienda` — Arcadi España (IA) | Tributos, presupuestos, financiación | Ley 58/2003 General Tributaria (335) |
| 🏥 Sanidad | `ministro-sanidad` — Mónica García (IA) | Salud pública, SAN, farmacia | Ley 14/1986 General de Sanidad (151) |
| 🌱 Transición Ecológica | `ministro-ecologia` — Sara Aagesen (IA) | Clima, energía, medio ambiente | Ley 7/2021 Cambio Climático (71) |
| 🔍 Auditor del Estado | `auditor` | Fiscaliza todo, no propone nada | — |

Corpus de la misión: **557 bloques** en las copias de trabajo. Duplicación literal tras la sesión 13: LGT 0,00 % (queda el inventario de fidelidad F1: 115 casos / 69 bloques / 3.071 palabras), LGS 5,07 % (1.140 palabras / 16 bloques), L7 0,00 %.

## Reglas de oro (de la Constitución del sistema)

1. **Fuente única de verdad**: toda propuesta cita identificador BOE + bloque `[aNNN]` exacto. Sin cita verificable → rechazada. Prohibido citar leyes que no estén en el repo.
2. **Competencias estancas**: cada ministro solo toca `ministerios/<su-cartera>/`; los solapes se resuelven en el Consejo.
3. **Límite constitucional**: respeto a la CE 1978 y la jerarquía normativa; nada de ley orgánica por este procedimiento; derechos fundamentales intangibles.
4. **Simplificar no es demolición**: toda reescritura se justifica con razones de peso (problema real, conflicto que se elimina, claridad que se gana).
5. **Nada de cifras sin fuente** (protocolo de presupuesto): la noticia activa la hipótesis; el dato la confirma.

## Estructura del repo

```
constitution/    Reglas del juego: constitución, protocolos (ministro, emoción,
                 laboratorio, presupuesto), mision-30-sesiones.md, prompts-cron/
data/            FUENTE INMUTABLE: raw/boe/ (HTML oficial congelado) + canonical/ (JSON)
gobierno_ia/     Paquete Python: schemas, core (validate/apply/revert), validators,
                 legal_review, cli, gold_set.json
runs/            Propuestas como parches versionados y resultados auditados
ministerios/     Por ministerio: leyes/ (copias de trabajo mutadas), propuestas/,
                 evidencia/ (manifiestos sha256), agenda.md, kpis.md, diario.md
consejo/         Actas del Consejo, rondas y evidencia del test cruzado
auditoria/       Veredictos del Auditor del Estado
presidencia/     Informes presidenciales diarios
tests/           45 tests: inmutabilidad, etiquetas, parches, estados, gold set
scripts/         Verificadores (immutability, scan_duplicacion, parse_boe_canonical,
                 corruption_ledger) + generar_boletin.py + ejecuciones por sesión
reports/rescate/ Informes del rescate (fases 0-7, piloto PMUS, baseline, ledger)
archivo/         Evidencia histórica preservada del primer ciclo (septiembre)
docs/            Boletín público (GitHub Pages)
```

## KPIs

Cada ministro gestiona su cuadro de mando evolutivo en `ministerios/<nombre>/kpis.md` (fila diaria + lecciones; un KPI sin dato actualizado cuenta como fallo del día). El Auditor los audita. Ejemplo: [`ministerios/hacienda/kpis.md`](ministerios/hacienda/kpis.md).

## Usar el pipeline

```bash
pip install -e ".[dev]"
python -m gobierno_ia --help            # 5 comandos: ingest-boe … build-report
pytest tests/ -v                        # 45/45
python scripts/verify_immutability.py   # PASSED = el BOE no se ha tocado
python scripts/generar_boletin.py       # regenera docs/index.html
```

## Ver el boletín diario

👉 **https://ntizar.github.io/gobierno-ia/** — propuestas de cada día, acuerdos con badge (APROBADO/APLAZADO/RECHAZADO), veredictos del Auditor, KPIs y lo importante del informe presidencial.

---
Hecho con ❤️ por David Antizar · Mastermind es el ejecutor, David el autor
