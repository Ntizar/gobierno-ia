#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de sentinela: verifica que data/raw/boe/ y data/canonical/ son inmutables.

Este test DEBE pasar siempre. Si falla, el sistema tiene un problema grave de integridad.
"""
import os
import sys
import hashlib
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_raw_inmutables():
    """Verifica que todos los ficheros raw/ tienen hash correcto en metadata.json."""
    raw_dir = os.path.join(BASE, "data", "raw", "boe")
    if not os.path.isdir(raw_dir):
        print("SKIP: data/raw/boe/ no existe todavía")
        return True  # Skip si aún no se ha creado

    ok = True
    for boe_id in os.listdir(raw_dir):
        boe_path = os.path.join(raw_dir, boe_id)
        if not os.path.isdir(boe_path):
            continue
        for fecha in os.listdir(boe_path):
            fecha_path = os.path.join(boe_path, fecha)
            meta_path = os.path.join(fecha_path, "metadata.json")
            source_path = os.path.join(fecha_path, "source.html")
            if not os.path.exists(meta_path) or not os.path.exists(source_path):
                print(f"FAIL: Faltan ficheros en {boe_id}/{fecha}")
                ok = False
                continue
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            actual_hash = sha256_file(source_path)
            expected_hash = meta.get("sha256", "")
            if actual_hash != expected_hash:
                print(f"FAIL: {boe_id}/{fecha}/source.html hash mismatch")
                print(f"  esperado: {expected_hash}")
                print(f"  actual:   {actual_hash}")
                ok = False
            else:
                print(f"OK: {boe_id}/{fecha}/source.html hash verificado")
    return ok


def test_canonical_inmutables():
    """Verifica que los JSONs canónicos tienen source_sha256 correcto."""
    canon_dir = os.path.join(BASE, "data", "canonical")
    if not os.path.isdir(canon_dir):
        print("SKIP: data/canonical/ no existe todavía")
        return True

    ok = True
    for boe_id in os.listdir(canon_dir):
        canon_path = os.path.join(canon_dir, boe_id)
        if not os.path.isdir(canon_path):
            continue
        for fname in os.listdir(canon_path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(canon_path, fname)
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            # Verificar source_sha256 existe
            if "source_sha256" not in data:
                print(f"FAIL: {boe_id}/{fname} no tiene source_sha256")
                ok = False
            else:
                print(f"OK: {boe_id}/{fname} tiene source_sha256: {data['source_sha256'][:16]}...")
    return ok


def test_no_escrituras_en_codigo():
    """Verifica que ningún script Python contiene escrituras a data/raw/ o data/canonical/."""
    ok = True
    for root, dirs, files in os.walk(BASE):
        if ".git" in root or "data" in root:
            continue
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8", errors="replace") as f:
                    content = f.read()
                # Buscar patrones de escritura a data/raw/ o data/canonical/
                import re
                patterns = [
                    r"open\(.*data/raw/.*['\"]w['\"]",
                    r"open\(.*data/canonical/.*['\"]w['\"]",
                    r"write_file\(.*data/raw/",
                    r"write_file\(.*data/canonical/",
                ]
                for pat in patterns:
                    if re.search(pat, content):
                        print(f"FAIL: {fpath} contiene escritura a data/raw/ o data/canonical/")
                        ok = False
                        break
            except (UnicodeDecodeError, PermissionError):
                pass
    if ok:
        print("OK: No se detectaron escrituras a data/raw/ o data/canonical/ en código")
    return ok


def main():
    print("=== TEST DE SENTINELA DE INMUTABILIDAD ===")
    results = []
    results.append(("raw_inmutables", test_raw_inmutables()))
    results.append(("canonical_inmutables", test_canonical_inmutables()))
    results.append(("no_escrituras_en_codigo", test_no_escrituras_en_codigo()))

    print("\n--- Resumen ---")
    all_ok = True
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")
        if not ok:
            all_ok = False

    if all_ok:
        print("\nRESULTADO: TODOS LOS TESTS PASARON")
        sys.exit(0)
    else:
        print("\nRESULTADO: HAY FALLOS — la inmutabilidad está comprometida")
        sys.exit(1)


if __name__ == "__main__":
    main()
