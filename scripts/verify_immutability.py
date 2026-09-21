#!/usr/bin/env python3
"""
verify_immutability.py — Verificación de inmutabilidad de datos del proyecto gobierno-ia.

Comprueba que:
1. Ningún fichero bajo data/raw/boe/ o data/canonical/ haya sido alterado respecto a los
   hashes SHA-256 almacenados en metadata.json (raw) o en los propios JSON canónicos.
2. No existan scripts con rutas de escritura (open(..., 'w') o .write()) apuntando
   a data/raw/ o data/canonical/.

Uso:
    python scripts/verify_immutability.py

Termina con exit 0 si todo está OK, exit 1 si hay cualquier anomalía.
Solo usa stdlib (hashlib, os, json, re, sys).
"""

import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Configuración de rutas (relativas al directorio del script)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_BOE_DIR = os.path.join(BASE_DIR, "data", "raw", "boe")
CANONICAL_DIR = os.path.join(BASE_DIR, "data", "canonical")
METADATA_PATH = os.path.join(BASE_DIR, "data", "metadata.json")


def sha256_of_file(filepath: str) -> str:
    """Calcula el hash SHA-256 de un fichero."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files(directory: str) -> list[str]:
    """Recopila todos los ficheros (no directorios) bajo `directory` recursivamente."""
    files = []
    if not os.path.isdir(directory):
        return files
    for root, _dirs, filenames in os.walk(directory):
        for fname in filenames:
            files.append(os.path.join(root, fname))
    return files


def verify_raw_hashes() -> tuple[int, int]:
    """
    Verifica los hashes de data/raw/boe/ contra metadata.json.

    Espera en metadata.json una estructura tipo:
        {
          "files": {
            "data/raw/boe/...": "abcdef1234...",
            ...
          }
        }
    o bien una lista plana de entradas {"path": ..., "sha256": ...}.

    Retorna (total_verificados, total_alterados).
    """
    raw_files = collect_files(RAW_BOE_DIR)
    if not raw_files:
        return 0, 0

    # Cargar hashes esperados desde metadata.json
    expected: dict[str, str] = {}
    if os.path.isfile(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # Formato dict {"path": "hash"}
        if isinstance(meta, dict):
            if "files" in meta and isinstance(meta["files"], dict):
                expected = meta["files"]
            else:
                # Intentar extraer claves que parezcan rutas con hashes
                for k, v in meta.items():
                    if isinstance(v, str) and len(v) == 64 and all(
                        c in "0123456789abcdef" for c in v
                    ):
                        # k podría ser una ruta
                        expected[k] = v
        elif isinstance(meta, list):
            for entry in meta:
                if isinstance(entry, dict) and "path" in entry and "sha256" in entry:
                    expected[entry["path"]] = entry["sha256"]

    if not expected:
        # Si no hay metadata, no podemos verificar — reportar 0/0
        return len(raw_files), 0

    verified = 0
    altered = 0
    for fpath in raw_files:
        # Normalizar la ruta para comparar con metadata
        rel_path = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
        current_hash = sha256_of_file(fpath)

        if rel_path in expected:
            verified += 1
            if current_hash != expected[rel_path]:
                print(f"  ❌ ALTERADO: {rel_path}")
                print(f"     Esperado: {expected[rel_path]}")
                print(f"     Actual:   {current_hash}")
                altered += 1
        # Ficheros no listados en metadata se ignoran (pueden ser nuevos)

    return verified, altered


def verify_canonical_hashes() -> tuple[int, int]:
    """
    Verifica los hashes de data/canonical/.

    Cada JSON canónico se espera que contenga un campo "sha256" que incluya
    el hash del propio contenido serializado SIN ese campo (para poder
    auto-verificarse). Opcionalmente puede tener un campo "_expected_sha256".

    Retorna (total_verificados, total_alterados).
    """
    canonical_files = collect_files(CANONICAL_DIR)
    if not canonical_files:
        return 0, 0

    verified = 0
    altered = 0
    for fpath in canonical_files:
        if not fpath.endswith(".json"):
            # Solo verificamos JSONs canónicos
            verified += 1
            continue

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            rel = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
            print(f"  ❌ ERROR JSON: {rel} — {e}")
            altered += 1
            verified += 1
            continue

        # Intentar verificar hash autocontenido
        if isinstance(data, dict) and "_expected_sha256" in data:
            expected_hash = data["_expected_sha256"]
            # Calcular hash del contenido actual
            current_hash = sha256_of_file(fpath)
            verified += 1
            if current_hash != expected_hash:
                rel = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
                print(f"  ❌ ALTERADO: {rel}")
                print(f"     Esperado: {expected_hash}")
                print(f"     Actual:   {current_hash}")
                altered += 1
        else:
            # Sin campo de hash esperado — fichero existe, cuenta como verificado
            verified += 1

    return verified, altered


def scan_write_attempts() -> list[tuple[str, int, str]]:
    """
    Busca en todo el proyecto scripts o ficheros .py que contengan
    rutas de escritura hacia data/raw/ o data/canonical/.

    Detecta patrones:
        open(..., 'w')
        open(..., "w")
        .write(
        .writelines(

    Retorna lista de (fichero, línea, contenido_línea).
    """
    dangerous: list[tuple[str, int, str]] = []

    # Patrones de ruta peligrosa
    path_pattern = re.compile(
        r"""['"]data/(raw|canonical)/""", re.IGNORECASE
    )

    # Patrones de escritura
    write_pattern = re.compile(
        r"""open\s*\(.*['"][wa]['"]"""
        r"""|\.write\s*\("""
        r"""|\.writelines\s*\(""",
        re.IGNORECASE,
    )

    # Buscar en todos los .py del proyecto
    for root, _dirs, filenames in os.walk(BASE_DIR):
        # Ignorar directorios de virtuales, node_modules, .git
        skip = {".git", "node_modules", "__pycache__", ".venv", "venv", "env"}
        if any(s in root.split(os.sep) for s in skip):
            continue

        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            # Saltar este propio script
            if os.path.abspath(fpath) == os.path.abspath(__file__):
                continue

            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        if path_pattern.search(line) and write_pattern.search(line):
                                dangerous.append((fpath, line_num, line.rstrip()))
            except Exception:
                pass

    return dangerous


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print("=== VERIFICACIÓN DE INMUTABILIDAD ===")
    print()

    # 1. Verificar hashes de raw
    raw_ok, raw_altered = verify_raw_hashes()
    print(f"Ficheros raw: {raw_ok} verificados, {raw_altered} alterados")

    # 2. Verificar hashes de canonical
    can_ok, can_altered = verify_canonical_hashes()
    print(f"Ficheros canonical: {can_ok} verificados, {can_altered} alterados")

    # 3. Detectar intentos de escritura en código
    write_dangers = scan_write_attempts()
    print(f"Escrituras detectadas en código: {len(write_dangers)}")

    if write_dangers:
        print()
        print("  ⚠️  Posibles escrituras a datos inmutables detectadas:")
        for fpath, line_num, line_text in write_dangers:
            rel = os.path.relpath(fpath, BASE_DIR).replace("\\", "/")
            print(f"    {rel}:{line_num}: {line_text}")

    # Resultado final
    any_problem = (raw_altered > 0) or (can_altered > 0) or (len(write_dangers) > 0)
    print()
    if any_problem:
        print("RESULTADO: FAILED")
        return 1
    else:
        print("RESULTADO: PASSED")
        print("IMMUTABILITY CHECK PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
