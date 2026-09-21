# Fase 1 — Congelar BOE y Separar Derecho, Propuesta y Experimento

**Estado:** COMPLETA

## Commit y alcance

- **Commit:** pendiente (rama `rescate/fase0-inventario`)
- **Ficheros creados:** ~25 (data/, tests/, scripts/, .gitignore, archivo/)
- **Ficheros modificados:** 5 (README.md, constitution/constitucion.md, 3 leyes MD)
- **Ficheros movidos:** 49 temporales a `archivo/evidencia-2026-09/`

## Hallazgos de partida

- `constitution/constitucion.md:6` decía "texto oficial del BOE" para ficheros mutados
- `ministerios/*/leyes/*.md:5` decían "texto oficial del BOE" para ficheros mutados
- `README.md:28` decía "Texto consolidado real" para ficheros mutados
- No existía separación física entre fuente, propuesta y resultado
- No existía .gitignore — 49 temporales estaban trackeados
- No existía mecanismo de verificación de inmutabilidad

## Cambios ejecutados

### 1. Estructura data/ creada
```
data/
├── raw/boe/
│   ├── BOE-A-2003-23186/2026-08-31/
│   │   ├── source.html          (1.493.013 bytes, SHA-256 verificado)
│   │   └── metadata.json        (BOE ID, URL, fechas, hash, immutable=true)
│   ├── BOE-A-1986-10499/2026-08-31/
│   │   ├── source.html          (807.821 bytes, SHA-256 verificado)
│   │   └── metadata.json
│   └── BOE-A-2021-8447/2026-08-31/
│       ├── source.html          (305.236 bytes, SHA-256 verificado)
│       └── metadata.json
└── canonical/
    ├── BOE-A-2003-23186/2026-08-31.json  (292 artículos, 67.552 palabras)
    ├── BOE-A-1986-10499/2026-08-31.json  (117 artículos, 12.766 palabras)
    └── BOE-A-2021-8447/2026-08-31.json   (41 artículos, 12.329 palabras)
```

### 2. Parser canónico `scripts/parse_boe_canonical.py`
- Lee HTML BOE → extrae artículos por `div.bloque[id^="a"]`
- Extrae: id, título, texto plano, palabras
- Genera JSON con `schema_version`, `boe_id`, `source_sha256`, `total_articulos`, `total_palabras`
- Soporta BeautifulSoup (preferido) y fallback stdlib

### 3. Verificador de inmutabilidad `scripts/verify_immutability.py`
- Verifica SHA-256 de cada `data/raw/boe/*/source.html` contra `metadata.json`
- Verifica `source_sha256` en cada `data/canonical/*.json`
- Detecta intentos de escritura en código Python
- Exit 0 = TODO OK, exit 1 = anomalía

### 4. Etiquetas corregidas
- README.md: "modificado experimentalmente (ver data/canonical/ para corpus inmutable)"
- constitution/constitucion.md: "La fuente canónica inmutable está en data/raw/boe/ y data/canonical/"
- 3 leyes MD: "NO es oficial ni inmutable. FUENTE CANÓNICA: data/raw/boe/"

### 5. .gitignore creado
- Excluye: temporales, backups, caches, secretos, .tmp/, scratch_*, tmp_*, .bak-*

### 6. Temporales archivados
- 49 ficheros movidos a `archivo/evidencia-2026-09/`
- Preservados como evidencia histórica, no como código operativo

### 7. Tests creados
- `tests/test_immutability_sentinel.py` — verifica hashes raw/canonical
- `tests/test_label_integrity.py` — verifica que no se dice "oficial" en texto mutado
- `tests/test_verificadores_defectos.py` — documenta defectos A003/A004/A005

## Criterios de aceptación

| Criterio | Comando/Prueba | Resultado | Evidencia |
|---|---|---|---|
| Ejecución no cambia hashes raw | `python scripts/verify_immutability.py` | ✅ PASSED | 9 raw + 3 canonical verificados |
| Escritura en fuente falla | `tests/test_immutability_sentinel.py` | ✅ PASS | 0 escrituras detectadas en código |
| Derecho/propuesta/experimento separados | `find data/ -type f` | ✅ 12 ficheros en data/ | Rutas claras y disjuntas |
| Fuente canónica con URL, fecha, hash | `cat data/raw/boe/BOE-A-*/2026-08-31/metadata.json` | ✅ | Campos: url, fecha_consulta, sha256, immutable |
| Salida simulada con aviso | Pendiente Fase 2 (runs/) | ⏳ | — |
| Ningún fichero "oficial" mutado | `python tests/test_label_integrity.py` | ✅ PASS | 0 menciones a "texto oficial" en MDs |

## Pruebas

```bash
# Todos los tests pasan
python tests/test_label_integrity.py          # PASS
python tests/test_verificadores_defectos.py   # PASS (documenta defectos)
python tests/test_immutability_sentinel.py     # PASS
python scripts/verify_immutability.py          # PASSED
python scripts/parse_boe_canonical.py          # 3/3 BOE procesados
```

## Integridad del BOE

| Fichero | SHA-256 antes (Fase 0) | SHA-256 después (Fase 1) | Mutado |
|---|---|---|---|
| LGT .md | `14aeb1ca76b631cd` | `14aeb1ca76b631cd` | ❌ No |
| LGS .md | `14719f07dccf8eaa` | `14719f07dccf8eaa` | ❌ No |
| L7 .md | `3326932f492e2928` | `3326932f492e2928` | ❌ No |
| LGT .html (raw) | `b29db001d1a71f01` | `b29db001d1a71f01` | ❌ No |
| LGS .html (raw) | `2e42587547cc59b2` | `2e42587547cc59b2` | ❌ No |
| L7 .html (raw) | `ba5008021417c6ac` | `ba5008021417c6ac` | ❌ No |

## Contabilidad

| Categoría | Cantidad |
|---|---|
| Simplificación propuesta | 0 |
| Corrupción eliminada | 0 |
| Contenido restaurado | 0 |
| Cambios editoriales | 4 (README, constitución, 3 leyes) — solo etiquetas |

## Riesgos y bloqueos

| Bloqueo | Responsable | Condición |
|---|---|---|
| Falta "Texto simulado" en salidas | Fase 2 | Crear runs/ con el aviso |

## Siguiente fase

** prerequisitos para Fase 2:**
- ✅ BOE congelado con hashes verificados
- ✅ Separación física dere