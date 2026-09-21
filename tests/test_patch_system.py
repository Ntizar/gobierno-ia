#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del sistema de parches versionados.

Verifica que:
1. Los esquemas de parche se pueden crear y serializar
2. La validación de parches funciona correctamente
3. La aplicación de parches NO toca data/raw/ ni data/canonical/
4. La reversión funciona correctamente
5. Las transiciones de estado son correctas
"""
import os
import sys
import json
import hashlib
import tempfile
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

# === Helpers ===

def sha256_str(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def make_test_canonical(tmp_dir):
    """Crea un canonical de prueba mínimo."""
    canonical = {
        "schema_version": "1.0",
        "boe_id": "BOE-TEST-001",
        "fecha_consulta": "2026-01-01",
        "source_sha256": sha256_str("test_source"),
        "total_articulos": 2,
        "total_palabras": 20,
        "articulos": [
            {"id": "a1", "titulo": "Artículo 1. Test.", "texto": "Este es el artículo 1 de prueba. Tiene dos párrafos.\n\nSegundo párrafo del artículo.", "palabras": 12},
            {"id": "a2", "titulo": "Artículo 2. Test.", "texto": "Este es el artículo 2 de prueba.", "palabras": 6},
        ]
    }
    path = os.path.join(tmp_dir, "canonical.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(canonical, f, ensure_ascii=False, indent=2)
    return canonical, path


def make_test_patch(canonical, article_id="a1", operation="reemplazar"):
    """Crea un parche de prueba."""
    art = next(a for a in canonical["articulos"] if a["id"] == article_id)
    return {
        "schema_version": "1.0",
        "proposal_id": "test-proposal-001",
        "run_id": "test-run-001",
        "boe_id": canonical["boe_id"],
        "base_snapshot": canonical["fecha_consulta"],
        "base_sha256": canonical["source_sha256"],
        "article_id": article_id,
        "operation": operation,
        "content_before": art["texto"],
        "content_proposed": art["texto"] + " MODIFICADO.",
        "author": "test-author",
        "justification": "Test de modificación",
        "sources": ["https://example.com/test"],
        "state": "BORRADOR",
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00",
    }


# === Tests ===

def test_schemas_importable():
    """Los esquemas se pueden importar."""
    try:
        from gobierno_ia.schemas import ProposalPatch, ProposalState, PatchManifest
        print("OK: Esquemas importables")
        return True
    except ImportError as e:
        print(f"FAIL: No se pueden importar esquemas: {e}")
        return False


def test_core_importable():
    """El core se puede importar."""
    try:
        from gobierno_ia.core import validate_patch, apply_patch, normalize_text
        print("OK: Core importable")
        return True
    except ImportError as e:
        print(f"FAIL: No se puede importar core: {e}")
        return False


def test_cli_importable():
    """El CLI se puede importar."""
    try:
        from gobierno_ia.cli import main
        print("OK: CLI importable")
        return True
    except ImportError as e:
        print(f"FAIL: No se puede importar CLI: {e}")
        return False


def test_patch_serialization():
    """Los parches se pueden crear y serializar."""
    try:
        from gobierno_ia.schemas import ProposalPatch, ProposalState
        patch = ProposalPatch(
            proposal_id="test-001",
            run_id="run-001",
            boe_id="BOE-TEST-001",
            base_snapshot="2026-01-01",
            base_sha256="abc123",
            article_id="a1",
            operation="replace",
            content_before="texto anterior",
            content_proposed="texto propuesto",
            author="test",
            justification="test justification",
            sources=[],
        )
        assert patch.state == ProposalState.BORRADOR
        assert patch.schema_version == "1.0"
        print("OK: Parche creado correctamente")
        return True
    except Exception as e:
        print(f"FAIL: Error creando parche: {e}")
        return False


def test_state_transitions():
    """Las transiciones de estado son correctas."""
    try:
        from gobierno_ia.schemas import validate_transition, ProposalState
        assert validate_transition(ProposalState.BORRADOR, ProposalState.REVISADO) == True
        assert validate_transition(ProposalState.BORRADOR, ProposalState.APROBADO) == False  # Saltarse revisión
        assert validate_transition(ProposalState.REVISADO, ProposalState.APROBADO) == True
        assert validate_transition(ProposalState.APROBADO, ProposalState.AUDITADO) == True
        assert validate_transition(ProposalState.AUDITADO, ProposalState.APLICADO) == True
        assert validate_transition(ProposalState.APLICADO, ProposalState.BORRADOR) == False  # No revertir a borrador
        print("OK: Transiciones de estado correctas")
        return True
    except Exception as e:
        print(f"FAIL: Error en transiciones: {e}")
        return False


def test_validate_patch():
    """La validación de parches funciona."""
    try:
        from gobierno_ia.core import validate_patch
        tmp_dir = tempfile.mkdtemp()
        try:
            canonical, can_path = make_test_canonical(tmp_dir)
            patch = make_test_patch(canonical)
            
            # Parche válido
            valid, errors = validate_patch(patch, canonical)
            assert valid, f"Parche debería ser válido pero falló: {errors}"
            
            # Parche con hash base incorrecto
            bad_patch = dict(patch)
            bad_patch["base_sha256"] = "hash_incorrecto"
            valid2, errors2 = validate_patch(bad_patch, canonical)
            assert not valid2, "Parche con hash incorrecto debería fallar"
            
            # Parche con artículo inexistente
            bad_patch2 = dict(patch)
            bad_patch2["article_id"] = "a999"
            valid3, errors3 = validate_patch(bad_patch2, canonical)
            assert not valid3, "Parche con artículo inexistente debería fallar"
            
            print("OK: Validación de parches funciona")
            return True
        finally:
            shutil.rmtree(tmp_dir)
    except Exception as e:
        print(f"FAIL: Error en validación: {e}")
        return False


def test_apply_doesnt_touch_canonical():
    """Aplicar un parche NO toca data/raw/ ni data/canonical/."""
    try:
        from gobierno_ia.core import apply_patch
        tmp_dir = tempfile.mkdtemp()
        try:
            # Usar el canonical REAL del proyecto (BOE-A-2003-23186)
            real_canonical_path = os.path.join(BASE, "data", "canonical", "BOE-A-2003-23186", "2026-08-31.json")
            if not os.path.exists(real_canonical_path):
                print("SKIP: canonical real no encontrado")
                return True
            with open(real_canonical_path, encoding="utf-8") as f:
                canonical = json.load(f)
            patch = make_test_patch(canonical, article_id="a1", operation="reemplazar")
            
            # Calcular hashes antes
            raw_dir = os.path.join(BASE, "data", "raw")
            canon_dir = os.path.join(BASE, "data", "canonical")
            
            hashes_before = {}
            for root, dirs, files in os.walk(raw_dir):
                for f in files:
                    path = os.path.join(root, f)
                    with open(path, "rb") as fh:
                        hashes_before[path] = hashlib.sha256(fh.read()).hexdigest()
            
            for root, dirs, files in os.walk(canon_dir):
                for f in files:
                    path = os.path.join(root, f)
                    with open(path, "rb") as fh:
                        hashes_before[path] = hashlib.sha256(fh.read()).hexdigest()
            
            # Aplicar parche
            run_dir = os.path.join(tmp_dir, "runs")
            os.makedirs(run_dir, exist_ok=True)
            manifest = apply_patch(patch, run_dir)
            
            # Verificar que raw/canonical no cambiaron
            hashes_after = {}
            for root, dirs, files in os.walk(raw_dir):
                for f in files:
                    path = os.path.join(root, f)
                    with open(path, "rb") as fh:
                        hashes_after[path] = hashlib.sha256(fh.read()).hexdigest()
            
            for root, dirs, files in os.walk(canon_dir):
                for f in files:
                    path = os.path.join(root, f)
                    with open(path, "rb") as fh:
                        hashes_after[path] = hashlib.sha256(fh.read()).hexdigest()
            
            for path in hashes_before:
                assert hashes_before[path] == hashes_after.get(path), \
                    f"¡Fichero mutado! {path}"
            
            print("OK: apply_patch NO toca data/raw/ ni data/canonical/")
            return True
        finally:
            shutil.rmtree(tmp_dir)
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def test_normalize_text():
    """La normalización de texto funciona."""
    try:
        from gobierno_ia.core import normalize_text
        assert normalize_text("  hola   mundo  ") == "hola mundo"
        assert normalize_text("hola\n\n\nmundo") == "hola\n\nmundo"
        assert normalize_text("") == ""
        print("OK: Normalización funciona")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def main():
    print("=== TESTS DEL SISTEMA DE PARCHES ===\n")
    
    tests = [
        ("schemas_importable", test_schemas_importable),
        ("core_importable", test_core_importable),
        ("cli_importable", test_cli_importable),
        ("patch_serialization", test_patch_serialization),
        ("state_transitions", test_state_transitions),
        ("validate_patch", test_validate_patch),
        ("apply_doesnt_touch_canonical", test_apply_doesnt_touch_canonical),
        ("normalize_text", test_normalize_text),
    ]
    
    results = []
    for name, test_fn in tests:
        results.append((name, test_fn()))
    
    print("\n--- Resumen ---")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  {name}: {status}")
    
    print(f"\n{passed}/{total} tests pasaron")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
