# Resultado Final — Rescate `Ntizar/gobierno-ia`

**Fecha:** 2026-09-21
**Rama:** `rescate/fase0-inventario` (5 commits desde `4412d4d`)

---

## Tabla de fases y estados

| Fase | Descripción | Estado | Commit |
|---|---|---|---|
| 0 | Inventario, rama de rescate y baseline | ✅ COMPLETA | `9259639` |
| 1 | Congelar BOE y separar derecho/propuesta/experimento | ✅ COMPLETA | `eb965f4` |
| 2 | Mover toda propuesta a parches versionados | ✅ COMPLETA | `58381a5` |
| 3 | Validación que falle de verdad y puerta jurídica humana | ✅ COMPLETA | `5b5c6dd` |
| 4 | Reproducibilidad e instalación limpia | ✅ COMPLETA | `5b5c6dd` |
| 5 | Suite de tests real con runner y umbrales | ✅ COMPLETA | `5b5c6dd` |
| 6 | Acotar producto a piloto PMUS/Movilidad Madrid15 | ✅ COMPLETA | `5b5c6dd` |
| 7 | Limpiar y contabilizar corrupción existente | ✅ COMPLETA | `5b5c6dd` |

## Arquitectura final

```
gobierno-ia/
├── gobierno_ia/                    ← Paquete Python
│   ├── __init__.py                (versión 0.1.0)
│   ├── __main__.py                (python -m gobierno_ia)
│   ├── schemas.py                 (ProposalPatch, ProposalState, PatchManifest)
│   ├── core.py                    (validate_patch, apply_patch, revert_patch)
│   ├── validators.py              (DuplicateDetector, NumeralParser, GateCheck)
│   ├── legal_review.py            (LegalReviewArtifact, verify_legal_review)
│   ├── cli.py                     (ingest-boe, validate-proposal, apply-patch, audit-run, build-report)
│   └── gold_set.json              (20 fragmentos con violaciones tipificadas)
├── data/
│   ├── raw/boe/                   ← FUENTE INMUTABLE
│   │   ├── BOE-A-2003-23186/2026-08-31/ (source.html + metadata.json)
│   │   ├── BOE-A-1986-10499/2026-08-31/ (source.html + metadata.json)
│   │   └── BOE-A-2021-8447/2026-08-31/  (source.html + metadata.json)
│   └── canonical/                 ← CANÓNICO INMUTABLE
│       ├── BOE-A-2003-23186/2026-08-31.json (292 artículos)
│       ├── BOE-A-1986-10499/2026-08-31.json (117 artículos)
│       └── BOE-A-2021-8447/2026-08-31.json  (41 artículos)
├── runs/                          ← PROPUESTAS Y RESULTADOS
├── tests/                         ← 45 tests en verde
├── scripts/                       ← Verificadores
├── .github/workflows/ci.yml       ← CI automatizado
├── pyproject.toml                 ← Paquete instalable
├── .gitignore                     ← Excluye temporales
├── reports/rescate/               ← Informes de fase
└── archivo/evidencia-2026-09/     ← Evidencia histórica preservada
```

## Flujo de datos

```
BOE API → data/raw/boe/ (inmutable)
       → data/canonical/ (inmutable, parseado)
       → gobierno_ia/validate_patch() → runs/<run-id>/ (propuesta como parche)
       → gobierno_ia/apply_patch() → runs/<run-id>/output/ (resultado simulado)
       → gobierno_ia/audit-run() → verificación de gates
       → gobierno_ia/build-report() → informe Markdown
```

**REGLA CLAVE:** `data/raw/` y `data/canonical/` NUNCA se modifican. Los parches solo escriben en `runs/`.

## Garantías automatizadas

| Garantía | Verificación | Evidencia |
|---|---|---|
| BOE no se muta | `verify_immutability.py` → PASSED | SHA-256 de 6 ficheros raw + 3 canonical verificados |
| Código no escribe en raw/canonical | `verify_no_writes_to_raw.py` → LIMPIO | 0 violaciones detectadas |
| Etiquetas honestas | `test_label_integrity.py` → PASS | Ningún MD dice "texto oficial" |
| Parches validados | `test_validate_patch` → PASS | Hash base, artículo, operación verificados |
| apply no toca fuente | `test_apply_doesnt_touch_canonical` → PASS | Hashes raw/canonical sin cambios |
| Máquina de estados | `test_state_transitions` → PASS | Transiciones válidas e inválidas |
| Gold set completo | `test_gold_set_20_casos` → PASS | 20 casos con 6 tipos de violación |
| Suite completa | `pytest tests/` → 45/45 PASS | Unitarios, integración, negativos, gold set |
| CI automatizado | `.github/workflows/ci.yml` | install → verificadores → pytest |

## Puertas humanas pendientes o satisfechas

| Puerta | Estado | Evidencia |
|---|---|---|
| Revisión jurídica del gold set | ⏳ PENDIENTE_REVISION_HUMANA | `gobierno_ia/gold_set.json` — 20 fragmentos esperando veredicto de jurista |
| Validación del piloto PMUS | ⏳ PENDIENTE_REVISION_HUMANA | 5 usuarios + 1 técnico movilidad + 1 jurista |
| Aprobación para merge a master | ⏳ PENDIENTE_APROBACION | Rama `rescate/fase0-inventario` con 5 commits |

## Resultado de CI y suite en entorno limpio

```
pytest tests/ -v
45 passed, 17 warnings in 0.79s

scripts/verify_immutability.py → PASSED
scripts/verify_no_writes_to_raw.py → LIMPIO
python -m gobierno_ia --help → 5 comandos disponibles
```

## Inventario de fuentes y hashes

| Fichero | SHA-256 (16 hex) | Bytes | Artículos |
|---|---|---|---|
| LGT .md (mutado) | `14aeb1ca76b631cd` | 897.275 | 335 bloques |
| LGS .md (mutado) | `14719f07dccf8eaa` | 154.431 | 151 bloques |
| L7 .md (mutado) | `3326932f492e2928` | 176.999 | 71 bloques |
| LGT .html (raw) | `b29db001d1a71f01` | 1.493.013 | 292 artículos |
| LGS .html (raw) | `2e42587547cc59b2` | 807.821 | 117 artículos |
| L7 .html (raw) | `ba5008021417c6ac` | 305.236 | 41 artículos |

## Ledger resumido de corrupción

| Ley | Duplicación | Omisión | Cambio editorial | Formato |
|---|---|---|---|---|
| LGT | 19 art. (10.482 pal.) | 1 art. (50 pal.) | 141 art. (17.200 pal.) | 131 |
| LGS | 11 art. (2.817 pal.) | 0 | 49 art. (1.955 pal.) | 57 |
| L7 | 1 art. (68 pal.) | 0 | 18 art. (179 pal.) | 21 |
| **TOTAL** | **13.367 palabras** | **50 palabras** | **19.334 palabras** | **209** |

⚠️ **Ninguna de estas cifras es "ahorro normativo".** Son cambios introducidos por el pipeline experimental sobre el corpus original.

## Métricas del piloto PMUS/Madrid15

| Entregable | Estado |
|---|---|
| Pregunta de producto | ✅ Definida |
| 3 medidas concretas | ✅ Definidas |
| Protocolo de prueba | ✅ Definido |
| Datos integrados | ⏳ Pendiente ejecución |
| Prueba con 5 usuarios | ⏳ PENDIENTE_REVISION_HUMANA |

## Deuda restante priorizada

1. **CRÍTICO:** Revisión jurídica del gold set por un jurista humano
2. **CRÍTICO:** Validación del piloto con 5 usuarios reales
3. **IMPORTANTE:** Re-descargar BOE fresh desde la API para verificar integridad
4. **IMPORTANTE:** Eliminar `scripts/audit_crons.py` y `scripts/parche_crons_ejecucion.py` (dependen de $LOCALAPPDATA)
5. **MEDIA:** Convertir los viejos scripts de ministerios en wrappers que usen la CLI
6. **MEDIA:** Añadir tests de cobertura de ramas para gates críticos (100%)
7. **BAJA:** Limpiar warnings de pytest (return en tests)

## Instrucciones exactas

### Instalar desde clon limpio
```bash
git clone https://github.com/Ntizar/gobierno-ia.git
cd gobierno-ia
pip install -e ".[dev]"
```

### Ejecutar demo
```bash
python -m gobierno_ia validate-proposal \
  --patch ejemplo.json \
  --canonical data/canonical/BOE-A-2003-23186/2026-08-31.json
```

### Ejecutar tests
```bash
pytest tests/ -v
```

### Auditar un run
```bash
python -m gobierno_ia audit-run --run-id <run-id> --runs-dir runs/
```

### Generar boletín
```bash
python -m gobierno_ia build-report --run-id <run-id> --runs-dir runs/
```

### Verificar inmutabilidad
```bash
python scripts/verify_immutability.py
python scripts/verify_no_writes_to_raw.py
```

### Ejecutar ledger de corrupción
```bash
python scripts/corruption_ledger.py
```

---

**RESULTADO: LISTO PARA PILOTO HUMANO, NO PARA USO JURÍDICO**

El sistema satisface las garantías técnicas automatizadas: BOE congelado e inmutable, parches versionados con máquina de estados, validadores que fallan ante anomalías, gold set de 20 fragmentos para revisión jurídica, CI automatizado y 45 tests en verde. Las puertas humanas pendientes (revisión jurídica del gold set y validación con 5 usuarios del piloto PMUS) impiden declarar el sistema listo para uso jurídico o producción.

---

*Hecho con ❤️ por David Antizar*
