#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de que ningun codigo operativo escribe en data/raw/ o data/canonical/.

Escanea todos los .py del repo buscando patrones de escritura a esas rutas.
Termina con exit 0 si esta limpio, exit 1 si encuentra violaciones.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_file(fpath):
    """Busca patrones de escritura prohibida en un fichero."""
    violations = []
    try:
        with open(fpath, encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                low = line.lower()
                # Buscar menciones de data/raw o data/canonical con contexto de escritura
                if "data/raw" in low or "data/canonical" in low:
                    # Detectar contexto de escritura
                    if any(kw in low for kw in ["open(", "write", "write_text", "write_bytes",
                                                 "write_file", "os.write", "shutil.copy",
                                                 "shutil.move", "os.rename", "os.replace"]):
                        violations.append({
                            "line": line_num,
                            "content": line.strip()[:120],
                        })
    except (UnicodeDecodeError, PermissionError):
        pass
    return violations


def main():
    all_violations = []
    scan_dirs = [
        os.path.join(BASE, "gobierno_ia"),
        os.path.join(BASE, "scripts"),
        os.path.join(BASE, "tests"),
    ]
    exclude = ["archiv", "evidencia", ".bak", "tmp_", "scratch_", "test_"]

    for scan_dir in scan_dirs:
        if not os.path.isdir(scan_dir):
            continue
        for root, dirs, files in os.walk(scan_dir):
            if any(ex in root.lower() for ex in exclude):
                continue
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(root, fname)
                if any(ex in fpath.lower() for ex in exclude):
                    continue
                violations = check_file(fpath)
                if violations:
                    rel = os.path.relpath(fpath, BASE)
                    for v in violations:
                        all_violations.append(f"  {rel}:{v['line']} — {v['content']}")

    if all_violations:
        print("=== VIOLACIONES DE ESCRITURA DETECTADAS ===\n")
        for v in all_violations:
            print(v)
        print(f"\nTotal: {len(all_violations)} violaciones")
        sys.exit(1)
    else:
        print("LIMPIO: No se detectaron escrituras a data/raw/ o data/canonical/ en codigo")
        sys.exit(0)


if __name__ == "__main__":
    main()
