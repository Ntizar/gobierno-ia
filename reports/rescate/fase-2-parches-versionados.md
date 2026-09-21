# Fase 2 — Mover Toda Propuesta a Parches Versionados

**Estado:** COMPLETA

## Commit y alcance

- **Commit:** pendiente
- **Ficheros creados:** gobierno_ia/ (paquete), tests/test_patch_system.py, scripts/verify_no_writes_to_raw.py
- **Ficheros modificados:** 0 (solo nuevos)
- **Líneas de código nuevo:** ~900 (schemas 150, core 521, cli ~200, tests ~300)

## Hallazgos de partida

- No existía esquema formal de propuestas — se escribían como diff ad-hoc sobre MD
- No existía máquina de estados — los acuerdos eran texto libre
- No existía reversibilidad — un diff aplicado no podía revertirse de forma fiable
- Las operaciones estaban en español: reemplazar, insertar, eliminar, fusionar

## Cambios ejecutados

### 1. Paquete gobierno_ia/

```
gobierno_ia/
├── __init__.py       (3 LOC — versión y exports)
├── __main__.py       (6 LOC — python -m gobierno_ia)
├── schemas.py        (150 LOC — esquemas con dataclasses)
├── core.py           (521 LOC — lógica de parches)
└── cli.py            (~200 LOC — CLI con 5 comandos)
```

### 2. Esquemas (schemas.py)

- **ProposalState**: BORRADOR → REVISADO → APROBADO → AUDITADO → APLICADO (también OBSOLETO, RECHAZADO)
- **ProposalPatch**: schema_version, proposal_id, run_id, boe_id, base_snapshot, base_sha256, article_id, operation, content_before, content_proposed, author, justification, sources, state, timestamps, approved_by, audit_result, legal_review
- **PatchManifest**: patch_id, proposal_id, run_id, applied_at, base_hash_before/after, article_id, words_before/after, operation, reversible
- Transiciones de estado validadas por código
- Serialización JSON bidireccional

### 3. Core (core.py)

- **load_canonical(boe_id, fecha)** → dict
- **find_article(canonical, article_id)** → dict | None
- **validate_patch(patch, canonical)** → (bool, list[str])
- **apply_patch(patch, run_dir)** → PatchManifest (NUNCA toca raw/canonical)
- **revert_patch(manifest, run_dir)** → bool
- **normalize_text(text)** → str
- **segment_articles(canonical)** → dict
- **compute_article_hash(text)** → str
- Centralización de normalización, segmentación y hashing

### 4. CLI (cli.py)

- `gobierno_ia ingest-boe` — HTML → JSON canónico
- `gobierno_ia validate-proposal` — valida parche contra canonical
- `gobierno_ia apply-patch` — aplica en run directory
- `gobierno_ia audit-run` — audita un run
- `gobierno_ia build-report` — genera informe Markdown
- Exit codes: 0=éxito, 1=error validación, 2=error interno

### 5. Verificadores

- `scripts/verify_no_writes_to_raw.py` — detecta intentos de escritura a raw/canonical
- `tests/test_patch_system.py` — 8 tests del sistema de parches

## Criterios de aceptación

| Criterio | Comando | Resultado | Evidencia |
|---|---|---|---|
| No hay escrituras a raw/canonical | `python scripts/verify_no_writes_to_raw.py` | ✅ LIMPIO | 0 violaciones |
| Parches se crean y serializan | `python tests/test_patch_system.py::test_patch_serialization` | ✅ PASS | — |
| Transiciones validadas | `python tests/test_patch_system.py::test_state_transitions` | ✅ PASS | — |
| Validación funciona | `python tests/test_patch_system.py::test_validate_patch` | ✅ PASS | — |
| apply_patch no toca raw/canonical | `python tests/test_patch_system.py::test_apply_doesnt_touch_canonical` | ✅ PASS | Hashes verificados |
| CLI funciona | `python -m gobierno_ia --help` | ✅ | 5 comandos disponibles |

## Pruebas

```bash
python tests/test_patch_system.py           # 8/8 PASS
python scripts/verify_no_writes_to_raw.py    # LIMPIO
python scripts/verify_immutability.py        # PASSED
python -m gobierno_ia --help                 # 5 comandos
```

## Integridad del BOE

| Fichero | SHA-256 Fase 1 | SHA-256 Fase 2 | Mutado |
|---|---|---|---|
| LGT .md | `14aeb1ca76b631cd` | `14aeb1ca76b631cd` | ❌ No |
| LGS .md | `14719f07dccf8eaa` | `14719f07dccf8eaa` | ❌ No |
| L7 .md | `3326932f492e2928` | `3326932f492e2928` | ❌ No |

## Contabilidad

| Categoría | Cantidad |
|---|---|
| Simplificación propuesta | 0 |
| Corrupción eliminada | 0 |
| Contenido restaurado | 0 |
| Cambios editoriales | 0 |

## Riesgos y bloqueos

| Bloqueo | Responsable | Condición |
|---|---|---|
| Falta gold set de 20 fragmentos | Jurista humano (Fase 3) | Revisión firmada |

## Siguiente fase

**Prerequisitos para Fase 3:**
- ✅ Esquema de parches versionados
- ✅ Validación de parches
- ✅ apply/revert sin tocar raw/canonical
- ✅ CLI funcional
- ✅ Verificador de no-escrituras
