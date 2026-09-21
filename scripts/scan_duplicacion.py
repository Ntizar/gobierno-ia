#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Barrido de duplicacion literal de las 3 leyes (medicion propia de Presidencia).

Para cada ley: total de palabras, frases (>=8 palabras) repetidas dentro del mismo
bloque y repetidas entre bloques distintos, palabras implicadas y tasa.

Uso: python scripts/scan_duplicacion.py [--fuente head|worktree]
"""
import re, os, sys, io, json, subprocess, hashlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEYES = {
    "hacienda (LGT)": "ministerios/hacienda/leyes/BOE-A-2003-23186.md",
    "sanidad (LGS)": "ministerios/sanidad/leyes/BOE-A-1986-10499.md",
    "ecologia (L7)": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
}


def leer(rel, fuente):
    if fuente == "head":
        return subprocess.run(["git", "show", "HEAD:" + rel], cwd=RAIZ,
                              capture_output=True).stdout.decode("utf-8", "replace")
    with io.open(os.path.join(RAIZ, rel), encoding="utf-8", errors="replace") as f:
        return f.read()


def bloques(texto):
    """Devuelve [(etiqueta, cuerpo)]."""
    out = []
    for m in re.finditer(r"^## \[([^\]]+)\][^\n]*\n", texto, re.M):
        ini = m.end()
        sig = re.search(r"^## \[", texto[ini:], re.M)
        fin = ini + sig.start() if sig else len(texto)
        out.append((m.group(1), texto[ini:fin]))
    return out


def claves(cuerpo):
    """Frases normalizadas de >=8 palabras."""
    frases = [f.strip() for f in re.split(r"(?<=[.;])\s+|\n\s*\n", cuerpo) if len(f.split()) >= 8]
    return [re.sub(r"\W+", " ", f.lower()) for f in frases]


def main():
    fuente = "worktree"
    if "--fuente" in sys.argv:
        fuente = sys.argv[sys.argv.index("--fuente") + 1]
    res = {"fuente": fuente, "leyes": {}}
    for nombre, rel in LEYES.items():
        txt = leer(rel, fuente)
        bl = bloques(txt)
        total_pal = len(txt.split())
        vistas_global = {}
        dup_intra_pal = 0
        dup_entre_pal = 0
        bloques_con_dup = set()
        for etq, cuerpo in bl:
            pal_bloque = len(cuerpo.split())
            ks = claves(cuerpo)
            # intra-bloque
            vistos = {}
            dup_aqui = 0
            for k in ks:
                if k in vistos:
                    dup_aqui += 1
                vistos[k] = 1
            if dup_aqui:
                bloques_con_dup.add(etq)
                dup_intra_pal += min(pal_bloque, dup_aqui * 12)
            # entre bloques
            for k in set(ks):
                if k in vistas_global and vistas_global[k] != etq:
                    dup_entre_pal += min(12, len(k.split()))
                vistas_global.setdefault(k, etq)
        res["leyes"][nombre] = {
            "fichero": rel,
            "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16],
            "bloques": len(bl),
            "palabras": total_pal,
            "bloques_con_dup_interna": len(bloques_con_dup),
            "etiquetas_afectadas": sorted(bloques_con_dup),
            "palabras_dup_interna_est": dup_intra_pal,
            "tasa_dup_interna_pct": round(100.0 * dup_intra_pal / max(1, total_pal), 2),
            "palabras_dup_entre_bloques_est": dup_entre_pal,
            "tasa_dup_entre_bloques_pct": round(100.0 * dup_entre_pal / max(1, total_pal), 2),
        }
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
