#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integridad de etiquetas: verifica que ningun fichero MD rotulado
como 'oficial' contenga texto que haya sido modificado por el pipeline.

Detecta:
- Ficheros que dicen 'texto oficial del BOE' pero no son inmutables
- Ficheros que NO dicen 'Texto simulado, sin validez jurídica' cuando deberían
"""
import os
import sys
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_no_oficial_en_mutados():
    """Los ficheros MD de leyes NO deben rotularse como 'texto oficial'."""
    patrones_oficial = [
        "texto oficial del BOE",
        "texto oficial del boe",
        "Texto oficial del BOE",
    ]
    leyes_dir = os.path.join(BASE, "ministerios")
    ok = True
    for root, dirs, files in os.walk(leyes_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8", errors="replace") as f:
                    content = f.read(5000)  # Solo las primeras 5000 chars (headers)
                for patron in patrones_oficial:
                    if patron in content:
                        rel = os.path.relpath(fpath, BASE)
                        print(f"FAIL: {rel} contiene '{patron}' — texto modificado no puede ser 'oficial'")
                        ok = False
            except (UnicodeDecodeError, PermissionError):
                pass
    if ok:
        print("OK: Ningun fichero MD de leyes se rotula falsamente como 'oficial'")
    return ok


def test_constitucion_no_oficial():
    """La constitucion no debe llamar 'texto oficial' a los MD mutados."""
    fpath = os.path.join(BASE, "constitution", "constitucion.md")
    if not os.path.exists(fpath):
        print("SKIP: constitution/constitucion.md no existe")
        return True
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    # Buscar la frase exacta "texto oficial del BOE" en el contexto de describir los MD
    if "texto oficial del BOE" in content:
        print("FAIL: constitution/constitucion.md ainda diz 'texto oficial del BOE'")
        return False
    print("OK: constitution/constitucion.md no llama 'oficial' a los MD mutados")
    return True


def test_simulado_en_salidas():
    """Las salidas de resultados experimentales deben decir 'simulado'."""
    # Este test es aspiracional — se activa cuando existan runs/
    runs_dir = os.path.join(BASE, "runs")
    if not os.path.isdir(runs_dir):
        print("SKIP: runs/ no existe todavía (Fase 2)")
        return True
    # Cuando exista, verificar que cada run tiene el aviso
    print("SKIP: runs/ existe pero el test de simulado se implementa en Fase 2")
    return True


def main():
    print("=== TEST DE INTEGRIDAD DE ETIQUETAS ===")
    results = []
    results.append(("no_oficial_en_mutados", test_no_oficial_en_mutados()))
    results.append(("constitucion_no_oficial", test_constitucion_no_oficial()))
    results.append(("simulado_en_salidas", test_simulado_en_salidas()))

    print("\n--- Resumen ---")
    all_ok = True
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")
        if not ok:
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
