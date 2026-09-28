# Constancia de evidencia — Apertura de la Fase 3 (Presupuestos) — 2026-09-28

**Sesión 19/30 · lunes · Ministerio de Sanidad · Mónica García**
Regla no negociable aplicada: **ejecución y estado primero.** Este documento existe para que cualquiera
pueda comprobar que hoy **no se ha tocado el fichero de la ley** y que **no se ha re-aplicado ningún diff**.

## 1. Fichero de ley — estado medido antes y después

| Momento | sha256 | Palabras (`wc -w`) | Bloques (`^## [`) |
|---|---|---|---|
| **ANTES** (apertura, 28-09-2026 10:39:46) | `688912f0b699a0908197c2855d3ea332a9842f56829e8f57fbc7e4f7443ba9f6` | 19.540 | 151 |
| **DESPUÉS** (cierre de la jornada de trabajo) | `688912f0b699a0908197c2855d3ea332a9842f56829e8f57fbc7e4f7443ba9f6` | 19.540 | 151 |

- **Hash idéntico antes y después.** Coincide además con la **apertura declarada para esta sesión** (688912f0…).
- Inventario de Fase 1: **cero** (cerrado el 23-09 por barrido propio y ratificado en el cierre de Fase 2).
- **Conclusión: NO se toca el fichero. No hay diff aprobado pendiente. Deuda de ejecución = 0 desde el 27-09-2026.**

## 2. Ejecución — declaración explícita

- **Diffs ejecutados hoy: 0.**
- **Diffs re-aplicados hoy: 0.** (Re-aplicar un diff ya ejecutado está prohibido; no se ha hecho.)
- **Ficheros `.bak-2026-09-28` creados: 0.** Comprobado: `ls ministerios/sanidad/leyes/*.bak-2026-09-28` → ninguno.
  No es un olvido: **no hay ejecución que sellar**, y fabricar un backup sin diff solo ensuciaría la cadena.
- `git diff --stat ministerios/sanidad/leyes/` → **vacío**. La ley no aparece en el diff.

## 3. `git status` (ministerio de Sanidad, al cierre)

```
 M ministerios/sanidad/agenda.md
 M ministerios/sanidad/kpis.md
?? ministerios/sanidad/evidencia/fuentes_acuatro_2026-09-28/
?? ministerios/sanidad/propuestas/2026-09-28.md
?? ministerios/sanidad/scripts_tmp/agenda_2026-09-28_append.md
?? ministerios/sanidad/scripts_tmp/kpi_row_2026-09-28.txt
```

**Lo que NO está en esa lista es lo importante:** el fichero `leyes/BOE-A-1986-10499.md` **no aparece modificado**.
Hoy no hay columna de ejecución que rellenar, y así se dice en lugar de adornarlo.

## 4. Lo que sí se ha movido hoy (Fase 3, papel)

1. **Encargo «papel, no método» cumplido**: archivo de las fuentes del primer dato cerrado por ESTIMACIÓN
   etiquetada ([acuatro], 5.719–7.478 M€) en `evidencia/fuentes_acuatro_2026-09-28/` —
   **4 descargas, 4 códigos HTTP 200, 0 fallos**, con `SHA256SUMS_fase3_2026-09-28.txt` y README.
   Verificación reproducida: `sha256sum -c SHA256SUMS_fase3_2026-09-28.txt` → **5/5 OK**.
2. **Tres reasignaciones con cifra** y **un seguimiento de condición de trámite fechado**:
   `propuestas/2026-09-28.md`.
3. **Agenda del día** (3 titulares, 2 de hoy y 1 declarada) y **fila KPI 2026-09-28** con la lección del día.

## 5. Pendiente declarado (no maquillado)

- **El aval del Consejo Interterritorial a los 5,7 M€ NO ha llegado** a las 10:39:46 del 28-09-2026.
  Declarado con hora en la sección de seguimiento de `propuestas/2026-09-28.md`, re-anclado al Interterritorial
  del 2 de octubre. **Sin aval, la reasignación no se ejecuta y no se da por avalada.**
- **4/4 requerimientos del acuerdo 45 a la IGAE siguen mudos**; dictamen 932A en su **día 17**.
- Diario personal: **corresponde a la entrada posterior al Consejo de las 22:00**, no a esta jornada de trabajo.
