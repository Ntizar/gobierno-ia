"""Revisión jurídica de parches legislativos — stub mínimo para fase 0.

Proporciona:
- LegalReviewArtifact: resultado de una revisión jurídica
- verify_legal_review: verifica la presencia y validez de la revisión
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LegalReviewArtifact:
    """Artifacto resultante de una revisión jurídica de un parche.

    Attributes:
        reviewer: identificador del revisor jurídico
        verdict: APTE / NO_APTE / CONDICIONAL
        comments: comentarios del revisor
        reviewed_at: timestamp de la revisión
        patch_id: ID del parche revisado
        risk_level: BAJO / MEDIO / ALTO
    """
    reviewer: str
    verdict: str  # "APTE", "NO_APTE", "CONDICIONAL"
    comments: str = ""
    reviewed_at: str = ""
    patch_id: str = ""
    risk_level: str = "BAJO"


def verify_legal_review(patch_dict: dict) -> tuple[bool, list[str]]:
    """Verifica que un parche tenga revisión jurídica válida.

    Checks:
    - campo 'legal_review' o 'revision_juridica' presente
    - Si es LegalReviewArtifact, verdict debe ser APTE o CONDICIONAL
    - Si es dict, debe tener al menos 'verdict' y 'reviewer'

    Retorna (es_valido, lista_errores).
    """
    errors: list[str] = []

    review = patch_dict.get("legal_review") or patch_dict.get("revision_juridica")
    if not review:
        errors.append("Revisión jurídica ausente — campo 'legal_review' requerido")
        return False, errors

    # Si es un LegalReviewArtifact
    if isinstance(review, LegalReviewArtifact):
        if review.verdict not in ("APTE", "CONDICIONAL"):
            errors.append(
                f"Verdicto jurídico no apto: '{review.verdict}'"
            )
            return False, errors
        if not review.reviewer:
            errors.append("Revisor jurídico no identificado")
            return False, errors
        return True, []

    # Si es un dict
    if isinstance(review, dict):
        verdict = review.get("verdict", "")
        if verdict not in ("APTE", "CONDICIONAL"):
            errors.append(
                f"Verdicto jurídico no apto: '{verdict}'"
            )
            return False, errors
        if not review.get("reviewer"):
            errors.append("Revisor jurídico no identificado")
            return False, errors
        return True, []

    errors.append(f"Tipo de revisión jurídica no reconocido: {type(review)}")
    return False, errors
