# -*- coding: utf-8 -*-
"""Prueba de integridad: si a kpis.md le quito MIS dos lineas de hoy, debe ser byte a byte
igual al backup previo. Si no lo es, algo ajeno se ha tocado y hay que revertir."""
import io, hashlib

P = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/kpis.md"
B = P + ".bak-2026-09-30"

cur = io.open(P, encoding="utf-8", newline="").read()
bak = io.open(B, encoding="utf-8", newline="").read()

lineas = cur.split("\n")
mias = [i for i, l in enumerate(lineas) if l.startswith("| - 2026-09-30")]
print("lineas mias localizadas:", [i + 1 for i in mias])
print("filas ajenas de la madrugada intactas:", [i + 1 for i, l in enumerate(lineas) if l.startswith("|| - 2026-09-30")])

sin_mias = "\n".join(l for i, l in enumerate(lineas) if i not in mias)
ok = (sin_mias == bak)
print("quitar mis dos lineas devuelve EXACTAMENTE el fichero previo:", ok)
print("sha256 previo :", hashlib.sha256(bak.encode("utf-8")).hexdigest()[:24])
print("sha256 reconst:", hashlib.sha256(sin_mias.encode("utf-8")).hexdigest()[:24])
if not ok:
    # diagnostico: primera diferencia
    a, b = sin_mias.split("\n"), bak.split("\n")
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else "<FIN>"
        y = b[i] if i < len(b) else "<FIN>"
        if x != y:
            print("PRIMERA DIFERENCIA en la linea %d:" % (i + 1))
            print("  sin_mias:", x[:160])
            print("  previo  :", y[:160])
            break
else:
    print("INTEGRIDAD OK: no se ha borrado ni sobrescrito nada del fichero previo.")
