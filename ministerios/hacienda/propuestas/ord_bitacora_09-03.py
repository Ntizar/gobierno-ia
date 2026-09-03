# Corregir orden cronologico de la bitacora: la fila 5 (09-03) debe ir tras la 5 (frustrada, 09-02)
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
p = "../../../constitution/mision-30-sesiones.md"
lines = open(p, encoding="utf-8").read().split("\n")
i5 = next(i for i, l in enumerate(lines) if l.startswith("| 5 | 2026-09-03"))
row5 = lines.pop(i5)
ifr = next(i for i, l in enumerate(lines) if l.startswith("| 5 (frustrada)"))
lines.insert(ifr + 1, row5)
open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("orden corregido; fila 09-03 en posicion", ifr + 1)
