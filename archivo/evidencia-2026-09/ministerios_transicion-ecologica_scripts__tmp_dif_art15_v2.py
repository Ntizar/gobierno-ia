"""Sesion 4 (2026-09-01) - Recuento AUTORITATIVO del dif corregido del articulo 15.

Correccion exigida por el Auditor (auditoria/2026-08-31.md, punto 5): la v3 del
art. 15 son las lineas 445-473, no el bloque entero (385-473).

Convencion de conteo DECLARADA (para que la cifra sea comparable y reproducible):
  - palabra = token separado por espacios en blanco del fichero markdown del repo;
  - se EXCLUYEN las lineas de encabezado de bloque '^## [';
  - se INCLUYEN los rotulos 'Articulo 15. ...' (son texto eliminable);
  - rango medido por numero de linea 1-indexado del fichero tal como esta en git.
"""
import re
import sys

PATH = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"


def lines():
    return open(PATH, encoding="utf-8").read().replace("\r", "").split("\n")


def words(rng):
    """Palabras segun la convencion declarada, sobre un rango 1-indexado inclusivo."""
    L = lines()
    tot = 0
    for i in range(rng[0], rng[1] + 1):
        ln = L[i - 1]
        if ln.startswith("## ["):
            continue
        tot += len([w for w in re.split(r"\s+", ln) if w])
    return tot


def main():
    L = lines()
    # anclas: comprobamos que el rango sigue siendo el que creemos
    def show(n):
        return L[n - 1][:70]

    assert L[378].startswith("## [a1-7]"), L[378]
    assert L[380].startswith("Artículo 15."), show(381)
    assert L[382].startswith("Artículo 15."), show(383)
    assert L[384].startswith("Artículo 15."), show(385)
    assert L[444].startswith("1. El Gobierno"), show(445)
    assert L[472].startswith("Para el diseño"), show(473)
    assert L[474].startswith("## [a1-12]"), show(475)

    print("ANCHAS OK | L475 =", show(475))
    print()
    print("DIF CORREGIDO: eliminar lineas 382-444, conservar 379-381 + 445-473")
    print("  eliminar 382-444 (63 lineas) :", words((382, 444)), "palabras")
    print("    - rotulos duplicados 383 y 385 (2 x 7 palabras):", words((383, 383)) + words((385, 385)))
    print("    - cuerpo v1 387-413         :", words((387, 413)))
    print("    - cuerpo v2 415-443         :", words((415, 443)))
    print("    - lineas 382/384/414/444 (vacias o de transicion):",
          words((382, 382)) + words((384, 384)) + words((414, 414)))
    print("  conservar v3 445-473          :", words((445, 473)))
    print("  conserve bloque completo (379-381+445-473):", words((379, 381)) + words((445, 473)))
    print()
    print("RECONCILIACION DE CIFRAS ANTERIORES")
    print("  sesion 3 (2026-08-31) alegaba 2.529 = v1 1.152 + v2 1.361 + rotulos 16")
    print("  Auditor midio v1 1.152 + v2 1.380 -> 2.532")
    print("  recuento autoritativo del dif 382-444 ->", words((382, 444)))
    print("  v2 real (415-443) =", words((415, 443)), "-> la sesion 3 midio v2 corta en 19 palabras")
    print()
    print("DA 6a (rotulo derogado sin norma derogatoria, sesion 2):")
    m = [i + 1 for i, x in enumerate(L) if x.startswith("## [da-6]")]
    if m:
        s = m[0]
        e = next((j + 1 for j in range(s, len(L)) if L[j].startswith("## [")), len(L))
        print("  bloque [da-6] lineas", s, "-", e - 1, "| palabras:", words((s, e - 1)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
