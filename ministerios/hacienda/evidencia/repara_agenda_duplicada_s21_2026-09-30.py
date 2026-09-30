# -*- coding: utf-8 -*-
"""REPARACION declarada: re-ejecute por error mi propio script de prepend y la entrada del
30-09 quedo DUPLICADA al principio de agenda.md (cabecera en las lineas 1 y 17).
Aqui: (1) quito la copia sobrante, (2) reconstruyo el respaldo con el contenido ORIGINAL
(sin mi entrada), (3) compruebo byte a byte que el fichero = mi entrada + el original intacto.
El incidente queda escrito en la leccion del KPI: no se esconde."""
import io, hashlib, shutil

P = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/agenda.md"
marker = "# Agenda — 2026-09-30 — Hacienda\n"

cur = io.open(P, encoding="utf-8", newline="").read()
primera = cur.find(marker)
segunda = cur.find(marker, primera + 1)
print("cabecera encontrada en los offsets:", primera, segunda)
assert primera == 0 and segunda > 0, "estado inesperado: no hay duplicado que reparar"

# (1) el fichero correcto empieza en la SEGUNDA aparicion = una sola entrada + original
fixed = cur[segunda:]
io.open(P + ".duplicado-2026-09-30", "w", encoding="utf-8", newline="").write(cur)  # guardo el estado malo
io.open(P, "w", encoding="utf-8", newline="").write(fixed)
print("escrito. cabeceras de hoy ahora:", fixed.count(marker))

# (2) contenido ORIGINAL = todo lo que va despues de mi entrada en el fichero corregido
mi_entrada = fixed[:fixed.find("|# Agenda")] if "|# Agenda" in fixed else None
if mi_entrada is None:
    # el original puede no empezar por '|#'; lo busco por la primera cabecera de otro dia
    idx = [fixed.find("\n# Agenda", 1), fixed.find("\n|# Agenda", 1)]
    idx = [i for i in idx if i > 0]
    corte = min(idx)
    mi_entrada, original = fixed[:corte + 1], fixed[corte + 1:]
else:
    original = fixed[fixed.find("|# Agenda"):]
print("longitud de mi entrada:", len(mi_entrada.encode("utf-8")), "B")
print("longitud del original reconstruido:", len(original.encode("utf-8")), "B (declarado antes: 27429 B)")
io.open(P + ".bak-2026-09-30", "w", encoding="utf-8", newline="").write(original)
print("respaldo regenerado con el original limpio.")

# (3) verificacion final
final = io.open(P, encoding="utf-8", newline="").read()
ok = (final == mi_entrada + original) and final.count(marker) == 1
print("VERIFICACION: fichero == mi entrada + original, y una sola cabecera de hoy ->", ok)
print("sha256 final agenda.md:", hashlib.sha256(final.encode("utf-8")).hexdigest()[:24])
print("sha256 original limpio:", hashlib.sha256(original.encode("utf-8")).hexdigest()[:24])
print("lineas:", len(final.split("\n")), "| cabeceras totales:", final.count("\n# Agenda") + final.count("|# Agenda"))
