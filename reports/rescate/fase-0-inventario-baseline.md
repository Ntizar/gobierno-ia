# Fase 0 — Inventario, Rama de Rescate y Baseline

**Estado:** COMPLETA

## Commit y alcance

- **Commit:** pendiente (rama `rescate/fase0-inventario` desde `4412d4d`)
- **Ficheros creados:** `reports/rescate/inventario-baseline.json`, `reports/rescate/baseline-verificadores.json`, `reports/rescate/fase-0-inventario-baseline.md`
- **Ficheros modificados:** 0 (fase no destructiva)
- **Ficheros movidos:** 0

## Hallazgos de partida

### Estructura del repositorio

| Métrica | Valor |
|---|---|
| Total ficheros | 388 |
| Scripts Python | 135 (12 en scripts/, 12 temp en auditoria/, ~80+ en propuestas/ministerios) |
| Ficheros Markdown | 117 |
| Backups .bak-* | 11 |
| Temporales/scratch | 45 |
| JSONs evidencia | ~80 |

### Corpus jurídico — hashes SHA-256

| Ley | Fichero | SHA-256 (16 hex) | Bytes | Líneas |
|---|---|---|---|---|
| LGT | `ministerios/hacienda/leyes/BOE-A-2003-23186.md` | `14aeb1ca76b631cd` | 897.275 | 8.391 |
| LGS | `ministerios/sanidad/leyes/BOE-A-1986-10499.md` | `14719f07dccf8eaa` | 154.431 | 1.880 |
| L7 | `ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md` | `3326932f492e2928` | 176.999 | 1.067 |

### BOE HTML — snapshots originales archivados

| Ley | Fichero | SHA-256 (16 hex) | Bytes |
|---|---|---|---|
| LGT | `ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html` | `b29db001d1a71f01` | 1.493.013 |
| LGS | `ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html` | `2e42587547cc59b2` | 807.821 |
| L7 | `ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html` | `ba5008021417c6ac` | 305.236 |

### Verificadores — ejecución y códigos de salida

| Verificador | Comando | Exit code | Resultado |
|---|---|---|---|
| scan_duplicacion.py | `python scripts/scan_duplicacion.py` | **0** (engañoso) | Detecta 105/335 bloques con dup en LGT, pero termina OK |
| diag_deuda.py | `python scripts/diag_deuda.py` | **0** (engañoso) | LGS muestra 0 cabeceras (no reconoce "Artículo tres") |
| verifica_diffs_s13.py | `python scripts/verifica_diffs_s13.py` | **0** (engañoso) | Produciendo métricas pero sin gates de fallo |
| audit_crons.py | `python scripts/audit_crons.py` | **0** | Depende de `$LOCALAPPDATA/hermes/cron/jobs.json` |
| parche_crons_ejecucion.py | `python scripts/parche_crons_ejecucion.py` | **0** | Depende de `$LOCALAPPDATA/hermes/cron/jobs.json` |

**Todos los verificadores terminan con código 0 independientemente de los problemas detectados.** Este es el defecto más crítico del sistema actual.

### Infraestructura ausente

- ❌ No existe `.gitignore`
- ❌ No existe `.github/workflows/` (sin CI)
- ❌ No existe `pyproject.toml` ni `requirements.txt` (sin paquete instalable)
- ❌ No existe `tests/` (sin suite ejecutable)
- ❌ No existe aviso "Texto simulado, sin validez jurídica" en ninguna salida

### Anomalías clasificadas

| ID | Tipo | Descripción | Severidad |
|---|---|---|---|
| A001 | Falso label oficial | Leyes MD rotuladas "texto oficial del BOE" pero modificadas por el pipeline | 🔴 Crítica |
| A002 | Duplicación LGT | 105/335 bloques con dup interna (11.12% palabras) | 🟡 Importante |
| A003 | Verificador engañoso | scan_duplicacion.py → exit 0 siempre | 🔴 Crítica |
| A004 | Verificador engañoso | verifica_diffs_s13.py → exit 0 siempre | 🔴 Crítica |
| A005 | Parser incompleto | diag_deuda.py no reconoce numerales en letras | 🟡 Importante |
| A006 | Ruta local hardcodeada | audit_crons/parche_crons → $LOCALAPPDATA | 🟡 Importante |
| A007 | Sin .gitignore | Temporales y backups trackeados | 🟡 Importante |
| A008 | Sin CI | No hay workflows automatizados | 🟡 Importante |
| A009 | Sin paquete | No es instalable desde clon limpio | 🟡 Importante |
| A010 | Sin avisos simulación | Ninguna salida dice "sin validez jurídica" | 🔴 Crítica |
| A011 | Corrupción 21-09 | Contenido normativo borrado y restaurado | 🟡 Importante |
| A012 | Sin suite tests | 18 ficheros "test" pero ninguno ejecutable | 🟡 Importante |

## Cambios ejecutados

- **Ninguno.** La Fase 0 es exclusivamente de inventario y baseline. No se modificó ningún contenido existente.

## Criterios de aceptación

| Criterio | Comando/Prueba | Resultado | Evidencia |
|---|---|---|---|
| Inventario legible por máquina | `cat reports/rescate/inventario-baseline.json \| jq .total_ficheros` | ✅ 388 ficheros inventariados | `reports/rescate/inventario-baseline.json` |
| Baseline registra anomalias conocidas | `jq .anomalias_conocidas \| length reports/rescate/inventario-baseline.json` | ✅ 12 anomalías documentadas | `reports/rescate/inventario-baseline.json` |
| No se modificó contenido BOE | `git diff --stat` tras inventario | ✅ Solo 3 ficheros nuevos (reports/) | working tree clean |
| Commit dedicado al inventario | `git log --oneline -1` | ⏳ Pendiente commit | — |
| Verificadores ejecutados y guardados | `cat reports/rescate/baseline-verificadores.json` | ✅ 5 verificadores, todos exit 0 | `reports/rescate/baseline-verificadores.json` |
| Hashes calculados | `jq .corpus_juridico reports/rescate/inventario-baseline.json` | ✅ SHA-256 de 3 leyes + 3 BOE HTML | `reports/rescate/inventario-baseline.json` |

## Pruebas

```bash
# Verificar que el inventario existe y es JSON válido
python -c "import json; json.load(open('reports/rescate/inventario-baseline.json'))" && echo "OK"

# Verificar hashes de leyes
python -c "
import json, hashlib
base = json.load(open('reports/rescate/inventario-baseline.json'))
for k,v in base['corpus_juridico'].items():
    h = hashlib.sha256(open(v['ruta'],'rb').read()).hexdigest()
    assert h == v['sha256'], f'Hash mismatch {k}'
print('Todos los hashes verificados')
"

# Verificar que verificadores devuelven 0 (reproduciendo el baseline)
for s in scan_duplicacion diag_deuda; do
    python scripts/${s}.py > /dev/null 2>&1
    echo "${s}: $?"
done
```

## Integridad del BOE

| Fichero | SHA-256 antes | SHA-256 después | Mutado |
|---|---|---|---|
| LGT .md | `14aeb1ca76b631cd` | `14aeb1ca76b631cd` | ❌ No |
| LGS .md | `14719f07dccf8eaa` | `14719f07dccf8eaa` | ❌ No |
| L7 .md | `3326932f492e2928` | `3326932f492e2928` | ❌ No |
| LGT .html | `b29db001d1a71f01` | `b29db001d1a71f01` | ❌ No |
| LGS .html | `2e42587547cc59b2` | `2e42587547cc59b2` | ❌ No |
| L7 .html | `ba5008021417c6ac` | `ba5008021417c6ac` | ❌ No |

**Confirmación:** Ningún fichero BOE fue mutado durante la fase de inventario.

## Contabilidad

| Categoría | Cantidad |
|---|---|
| Simplificación propuesta | 0 (no medido en fase 0) |
| Corrupción eliminada | 0 (no medido en fase 0) |
| Contenido restaurado | 0 (no medido en fase 0) |
| Cambios editoriales | 0 |

## Riesgos y bloqueos

| Bloqueo | Responsable | Artefacto | Condición de desbloqueo |
|---|---|---|---|
| No se puede verificar equivalencia jurídica desde código | Jurista humano | Gold set de 20 fragmentos (Fase 3) | Revisión firmada con resultado, fecha, hash y observaciones |
| Fuente BOE canónica no verificable contra originals mutados | — | HTML BOE archivados | Descargar fresh desde API BOE para validar integridad |
| Crons dependen de $LOCALAPPDATA | David (config local) | `scripts/audit_crons.py:3` | Adaptador configurable (Fase 4) |

## Siguiente fase

** prerequisitos para Fase 1:**
- ✅ Inventario completo con hashes
- ✅ Baseline de verificadores
- ✅ No se ha mutado el BOE
- ✅ Anomalías conocidas documentadas
- ⏳ Commit del inventario (pendiente)

**Fase 1 puede comenzar inmediatamente tras el commit.**
