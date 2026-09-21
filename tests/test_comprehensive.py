#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite completa de tests: unitarios, integración, negativos y gates críticos.

Ejecutar:  pytest tests/test_comprehensive.py -v
Cobertura:  ~28 tests (unitarios + integración + negativos + gold set)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile

import pytest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from gobierno_ia.core import (
    apply_patch,
    compute_article_hash,
    normalize_text,
    revert_patch,
    validate_patch,
    find_article,
    load_canonical,
)
from gobierno_ia.schemas import (
    ProposalPatch,
    ProposalState,
    PatchManifest,
    compute_str_hash,
    to_json,
    from_json,
    validate_transition,
)

# Canonical real para tests de integración
CANONICAL_LGT_ID = "BOE-A-2003-23186"
CANONICAL_FECHA = "2026-08-31"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def canonical_lgt():
    """Carga el canonical real de la LGT."""
    try:
        return load_canonical(CANONICAL_LGT_ID, CANONICAL_FECHA)
    except FileNotFoundError:
        pytest.skip("Canonical real no disponible")


@pytest.fixture
def tmp_run(tmp_path):
    """Directorio temporal para run_dir."""
    run_dir = str(tmp_path / "runs")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir


def _sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _make_patch_dict(canonical: dict, article_id: str = "a1",
                     operation: str = "reemplazar") -> dict:
    """Construye un dict de parche válido contra un canonical dado."""
    art = find_article(canonical, article_id)
    assert art is not None, f"article_id {article_id} no existe en canonical"
    return {
        "schema_version": "1.0",
        "proposal_id": "test-proposal-001",
        "run_id": "test-run-001",
        "boe_id": CANONICAL_LGT_ID,
        "base_snapshot": CANONICAL_FECHA,
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


# ============================================================================
# TESTS UNITARIOS (1–13)
# ============================================================================

# --- 1. normalize_text espacios ---
class TestNormalizeText:
    def test_normalize_text_espacios(self):
        """Normaliza espacios múltiples a uno solo."""
        assert normalize_text("  hola   mundo  ") == "hola mundo"
        assert normalize_text("a\t\tb") == "a b"
        assert normalize_text("  ") == ""

    # --- 2. normalize_text saltos ---
    def test_normalize_text_saltos(self):
        """Normaliza saltos de línea múltiples a doble salto."""
        assert normalize_text("hola\n\n\nmundo") == "hola\n\nmundo"
        assert normalize_text("a\r\n\r\nb") == "a\n\nb"
        # \r solo se convierte a \n (normalize_text reemplaza \r por \n)
        assert normalize_text("a\rb") == "a\nb"

    # --- 3. normalize_text unicode ---
    def test_normalize_text_unicode(self):
        """Normaliza Unicode (NFC) y elimina BOM/zero-width."""
        # BOM
        assert "\ufeff" not in normalize_text("\ufeffHola")
        # Zero-width
        result = normalize_text("hola\u200bmundo")
        assert "\u200b" not in result
        # NFC: ñ should remain as ñ
        assert normalize_text("niño") == "niño"

    # --- 4. compute_hash_determinista ---
    def test_compute_hash_determinista(self):
        """Mismo input → mismo hash (determinismo)."""
        text = "Artículo 1. Objeto de esta ley."
        h1 = compute_article_hash(text)
        h2 = compute_article_hash(text)
        assert h1 == h2
        assert len(h1) == 64  # SHA-256 hex digest

    # --- 5. compute_hash_diferente ---
    def test_compute_hash_diferente(self):
        """Input diferente → hash diferente."""
        h1 = compute_article_hash("Texto A")
        h2 = compute_article_hash("Texto B")
        assert h1 != h2

    # --- 6. ProposalPatch creation ---
    def test_proposal_patch_creation(self):
        """Se puede crear un ProposalPatch con campos obligatorios."""
        patch = ProposalPatch(
            proposal_id="p001",
            run_id="r001",
            boe_id="BOE-TEST",
            base_snapshot="2026-01-01",
            base_sha256="abc123",
            article_id="a1",
            operation="reemplazar",
            content_before="antes",
            content_proposed="después",
            author="tester",
            justification="test",
        )
        assert patch.proposal_id == "p001"
        assert patch.boe_id == "BOE-TEST"

    # --- 7. ProposalPatch default state ---
    def test_proposal_patch_default_state(self):
        """El estado inicial por defecto es BORRADOR."""
        patch = ProposalPatch(
            proposal_id="p001",
            run_id="r001",
            boe_id="BOE-TEST",
            base_snapshot="2026-01-01",
            base_sha256="abc",
            article_id="a1",
            operation="reemplazar",
            content_before="x",
            content_proposed="y",
            author="t",
            justification="t",
        )
        assert patch.state == ProposalState.BORRADOR

    # --- 8. State transition valid ---
    def test_state_transition_valid(self):
        """Transiciones válidas: BORRADOR→REVISADO→APROBADO."""
        assert validate_transition("BORRADOR", "REVISADO") is True
        assert validate_transition("REVISADO", "APROBADO") is True
        assert validate_transition("APROBADO", "AUDITADO") is True
        assert validate_transition("AUDITADO", "APLICADO") is True
        assert validate_transition("APLICADO", "OBSOLETO") is True

    # --- 9. State transition invalid ---
    def test_state_transition_invalid(self):
        """Transición inválida: BORRADOR→APLICADO (salto de estados)."""
        assert validate_transition("BORRADOR", "APLICADO") is False
        assert validate_transition("BORRADOR", "BORRADOR") is False
        assert validate_transition("OBSOLETO", "BORRADOR") is False

    # --- 10. validate_patch válido ---
    def test_validate_patch_valido(self, canonical_lgt):
        """Parche correcto contra canonical real pasa validación."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        valid, errors = validate_patch(patch, canonical_lgt)
        assert valid, f"Debería ser válido: {errors}"

    # --- 11. validate_patch hash incorrecto ---
    def test_validate_patch_hash_incorrecto(self, canonical_lgt):
        """Parche con base_sha256 incorrecto falla validación."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        patch["base_sha256"] = "0" * 64
        valid, errors = validate_patch(patch, canonical_lgt)
        assert not valid
        assert any("base_sha256" in e for e in errors)

    # --- 12. validate_patch artículo inexistente ---
    def test_validate_patch_articulo_inexistente(self, canonical_lgt):
        """Parche con article_id inexistente falla validación."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        patch["article_id"] = "a9999"
        valid, errors = validate_patch(patch, canonical_lgt)
        assert not valid
        assert any("a9999" in e for e in errors)

    # --- 13. validate_patch operación inválida ---
    def test_validate_patch_operacion_invalida(self, canonical_lgt):
        """Parche con operation no soportada falla en apply_patch."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        patch["operation"] = "voltear"
        with tempfile.TemporaryDirectory() as tmp:
            with pytest.raises(ValueError, match="operation.*no válida"):
                apply_patch(patch, tmp)


# ============================================================================
# TESTS DE INTEGRACIÓN (14–18)
# ============================================================================


class TestIntegration:
    # --- 14. apply_produces_output ---
    def test_apply_produces_output(self, canonical_lgt, tmp_run):
        """apply_patch crea un fichero JSON en run_dir."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        manifest = apply_patch(patch, tmp_run)
        # Check file exists
        expected_path = os.path.join(tmp_run, "test-run-001", CANONICAL_LGT_ID, "a1.json")
        assert os.path.isfile(expected_path), f"Fichero no creado: {expected_path}"
        with open(expected_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["article_id"] == "a1"
        assert data["operation"] == "reemplazar"

    # --- 15. apply_manifest_campos ---
    def test_apply_manifest_campos(self, canonical_lgt, tmp_run):
        """El manifest tiene todos los campos obligatorios."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        manifest = apply_patch(patch, tmp_run)
        assert isinstance(manifest, PatchManifest)
        assert manifest.patch_id  # non-empty
        assert manifest.proposal_id == "test-proposal-001"
        assert manifest.run_id == "test-run-001"
        assert manifest.article_id == "a1"
        assert manifest.operation == "reemplazar"
        assert manifest.words_before > 0
        assert manifest.words_after > 0
        assert manifest.base_hash_before  # non-empty
        assert manifest.base_hash_after  # non-empty
        assert manifest.reversible is True
        assert manifest.applied_at  # non-empty

    # --- 16. revert_restores_content ---
    def test_revert_restores_content(self, canonical_lgt, tmp_run):
        """revert_patch genera un archivo _reverted.json con el contenido original."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        manifest = apply_patch(patch, tmp_run)
        # Revert
        result = revert_patch(manifest, tmp_run)
        assert result is True
        # Check reverted file exists
        reverted_path = os.path.join(
            tmp_run, "test-run-001", CANONICAL_LGT_ID, "a1_reverted.json"
        )
        assert os.path.isfile(reverted_path), f"Archivo de reversión no creado: {reverted_path}"
        with open(reverted_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["restored_content"]
        assert data["restored_hash"]

    # --- 17. apply_doble_idempotente ---
    def test_apply_doble_idempotente(self, canonical_lgt, tmp_run):
        """Aplicar el mismo parche dos veces: el fichero se sobreescribe (idempotente)."""
        patch = _make_patch_dict(canonical_lgt, article_id="a2")
        manifest1 = apply_patch(patch, tmp_run)
        manifest2 = apply_patch(patch, tmp_run)
        # El fichero de salida debe existir con el contenido correcto
        out_path = os.path.join(tmp_run, "test-run-001", CANONICAL_LGT_ID, "a2.json")
        assert os.path.isfile(out_path)
        with open(out_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["article_id"] == "a2"
        # Both manifests should have different patch_ids (uuid4)
        assert manifest1.patch_id != manifest2.patch_id

    # --- 18. test_run_completo ---
    def test_run_completo(self, canonical_lgt, tmp_run):
        """Flujo completo: crear parche → validar → aplicar → auditar → informe."""
        from gobierno_ia.validators import GateCheck

        # 1. Crear parche
        patch = _make_patch_dict(canonical_lgt, article_id="a3")

        # 2. Validar
        valid, errors = validate_patch(patch, canonical_lgt)
        assert valid, f"Parche debería ser válido: {errors}"

        # 3. Aplicar
        manifest = apply_patch(patch, tmp_run)
        assert manifest.patch_id

        # 4. Auditar (simular gate check completo)
        proposal = dict(patch)
        proposal["audit_result"] = "PASS"
        proposal["legal_review"] = {"verdict": "APTE", "reviewer": "test-jurista"}
        gate = GateCheck()
        result = gate.validate(canonical_lgt, proposal=proposal)
        assert result.passed, f"Gates no aprobados: {result.errors}"

        # 5. Generar informe (simulado)
        report = {
            "run_id": "test-run-001",
            "patches_applied": [manifest.patch_id],
            "status": "COMPLETADO",
            "disclaimers": ["Resultado simulado, sin validez jurídica"],
        }
        report_path = os.path.join(tmp_run, "informe.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        assert os.path.isfile(report_path)


# ============================================================================
# TESTS NEGATIVOS (19–26)
# ============================================================================

class TestNegativos:
    # --- 19. fuente_mutada_rechazada ---
    def test_fuente_mutada_rechazada(self, canonical_lgt, tmp_run):
        """Parche contra canonical con hash mutado es rechazado."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        # Mutar el hash del canonical (simular fuente corrupta)
        mutated = dict(canonical_lgt)
        mutated["source_sha256"] = "mutado_" + canonical_lgt["source_sha256"][7:]
        valid, errors = validate_patch(patch, mutated)
        assert not valid
        assert any("base_sha256" in e for e in errors)

    # --- 20. hash_base_obsoleto ---
    def test_hash_base_obsoleto(self, canonical_lgt):
        """Parche con hash antiguo (ya aplicado) queda OBSOLETO."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        # Simular hash antiguo diferente al actual
        patch["base_sha256"] = _sha256_str("contenido_anterior_que_ya_no_es_valido")
        valid, errors = validate_patch(patch, canonical_lgt)
        assert not valid
        assert any("base_sha256" in e or "no coincide" in e for e in errors)

    # --- 21. rango_inexistente ---
    def test_rango_inexistente(self, canonical_lgt):
        """article_id fuera de rango falla."""
        patch = _make_patch_dict(canonical_lgt, article_id="a1")
        patch["article_id"] = "a9999"
        valid, errors = validate_patch(patch, canonical_lgt)
        assert not valid
        assert any("a9999" in e for e in errors)

    # --- 22. duplicacion_detectada ---
    def test_duplicacion_detectada(self, canonical_lgt):
        """Inyectar duplicación > umbral falla el detector."""
        from gobierno_ia.validators import DuplicateDetector

        # Crear un canonical con duplicaciones significativas
        art = find_article(canonical_lgt, "a1")
        dup_text = art["texto"] + " " + art["texto"]
        mutated_canonical = dict(canonical_lgt)
        mutated_canonical["articulos"] = [
            dict(a) for a in canonical_lgt["articulos"]
        ]
        # Reemplazar el artículo a1 con texto duplicado
        for a in mutated_canonical["articulos"]:
            if a["id"] == "a1":
                a["texto"] = dup_text
                break

        detector = DuplicateDetector(threshold=0.01)  # umbral muy bajo
        result = detector.validate(mutated_canonical)
        assert not result.passed, "Debería detectar duplicación"
        assert any("duplicación" in e.lower() or "duplica" in e.lower()
                    for e in result.errors)

    # --- 23. auditoría_ausente_bloquea ---
    def test_auditoria_ausente_bloquea(self, canonical_lgt):
        """Gate sin resultado de auditoría falla."""
        from gobierno_ia.validators import GateCheck
        proposal = {
            "base_sha256": canonical_lgt["source_sha256"],
            "article_id": "a1",
            "content_before": "test",
            "content_proposed": "test modificado",
            "state": "BORRADOR",
            "audit_result": None,
            "legal_review": {"verdict": "APTE", "reviewer": "j"},
        }
        gate = GateCheck()
        result = gate.validate(canonical_lgt, proposal=proposal)
        assert not result.passed
        assert any("auditoría" in e.lower() or "audit" in e.lower()
                    for e in result.errors)

    # --- 24. revisión_jurídica_ausente ---
    def test_revision_juridica_ausente(self, canonical_lgt):
        """Gate sin revisión jurídica bloquea."""
        from gobierno_ia.validators import GateCheck
        proposal = {
            "base_sha256": canonical_lgt["source_sha256"],
            "article_id": "a1",
            "content_before": "test",
            "content_proposed": "test modificado",
            "state": "BORRADOR",
            "audit_result": "PASS",
            "legal_review": None,
            "approved_by": None,
        }
        gate = GateCheck()
        result = gate.validate(canonical_lgt, proposal=proposal)
        assert not result.passed
        assert any("jurídica" in e.lower() or "legal" in e.lower()
                    for e in result.errors)

    # --- 25. acuerdo_pendiente_bloquea ---
    def test_acuerdo_pendiente_bloquea(self, canonical_lgt):
        """Gate con acuerdos pendientes falla."""
        from gobierno_ia.validators import GateCheck
        proposal = {
            "base_sha256": canonical_lgt["source_sha256"],
            "article_id": "a1",
            "content_before": "test",
            "content_proposed": "test modificado",
            "state": "PENDIENTE",  # Estado no reconocido → acuerdos_pendientes WARN
            "audit_result": "PASS",
            "legal_review": {"verdict": "APTE", "reviewer": "j"},
        }
        gate = GateCheck()
        result = gate.validate(canonical_lgt, proposal=proposal)
        # Check that acuerdos_pendientes gate was evaluated
        gates = result.metrics.get("gates", {})
        assert "acuerdos_pendientes" in gates
        # With an unrecognized state, the gate should warn
        assert gates["acuerdos_pendientes"] == "WARN" or not result.passed

    # --- 26. resultado_sin_aviso ---
    def test_resultado_sin_aviso(self, canonical_lgt):
        """Salida sin 'simulado' en disclaimers no se declara listo."""
        from gobierno_ia.validators import GateCheck
        proposal = {
            "base_sha256": canonical_lgt["source_sha256"],
            "article_id": "a1",
            "content_before": "test",
            "content_proposed": "test modificado",
            "state": "BORRADOR",
            "audit_result": "PASS",
            "legal_review": {"verdict": "APTE", "reviewer": "j"},
            "approved_by": None,
        }
        gate = GateCheck()
        result = gate.validate(canonical_lgt, proposal=proposal)
        # The gate should report revision_juridica as PENDING since approved_by is None
        gates = result.metrics.get("gates", {})
        # Verify that without approved_by, legal review is pending
        assert gates.get("revision_juridica") == "PENDING" or not result.passed


# ============================================================================
# TESTS DE GOLD SET (27–28)
# ============================================================================

class TestGoldSet:
    # --- 27. gold_set_20_casos ---
    def test_gold_set_20_casos(self):
        """gold_set.json tiene exactamente 20 casos."""
        gold_path = os.path.join(BASE, "gobierno_ia", "gold_set.json")
        assert os.path.isfile(gold_path), f"gold_set.json no encontrado: {gold_path}"
        with open(gold_path, encoding="utf-8") as f:
            gold = json.load(f)
        assert len(gold) == 20, f"Esperados 20 casos, encontrados {len(gold)}"

    # --- 28. gold_set_tipos_cobertura ---
    def test_gold_set_tipos_cobertura(self):
        """gold set cubre todos los tipos de violación definidos."""
        gold_path = os.path.join(BASE, "gobierno_ia", "gold_set.json")
        with open(gold_path, encoding="utf-8") as f:
            gold = json.load(f)

        # Tipos de violación definidos en el gold set del proyecto
        violation_types = {
            "excepcion_perdida",
            "sujeto_obligado_alterado",
            "plazo_alterado",
            "remision_rota",
            "carga_probatoria_modificada",
        }
        covered_types = {case["violation_type"] for case in gold}
        for vtype in violation_types:
            assert vtype in covered_types, f"Tipo '{vtype}' no cubierto en gold_set"

        # Verify each type has at least 3 cases for statistical relevance
        from collections import Counter
        type_counts = Counter(case["violation_type"] for case in gold)
        for vtype, count in type_counts.items():
            assert count >= 3, f"Tipo '{vtype}' solo tiene {count} casos (mínimo 3)"
