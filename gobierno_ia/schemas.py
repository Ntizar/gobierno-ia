"""Esquemas de parches versionados para propuestas legislativas.

Tipos de datos puros (stdlib) — sin dependencias externas.
"""

from __future__ import annotations

import enum
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enum de estados
# ---------------------------------------------------------------------------

class ProposalState(enum.Enum):
    """Estados posibles de una propuesta de parche legislativo."""
    BORRADOR = "BORRADOR"
    REVISADO = "REVISADO"
    APROBADO = "APROBADO"
    AUDITADO = "AUDITADO"
    APLICADO = "APLICADO"
    OBSOLETO = "OBSOLETO"
    RECHAZADO = "RECHAZADO"


# ---------------------------------------------------------------------------
# Transiciones de estado
# ---------------------------------------------------------------------------

state_transitions: dict[str, list[str]] = {
    "BORRADOR":   ["REVISADO", "RECHAZADO"],
    "REVISADO":   ["APROBADO", "RECHAZADO"],
    "APROBADO":   ["AUDITADO", "RECHAZADO"],
    "AUDITADO":   ["APLICADO", "RECHAZADO"],
    "APLICADO":   ["OBSOLETO"],
    "OBSOLETO":   [],
    "RECHAZADO":  [],
}


def validate_transition(from_state: str | ProposalState, to_state: str | ProposalState) -> bool:
    """Devuelve True si la transición from→to es permitida."""
    if isinstance(from_state, ProposalState):
        from_state = from_state.value
    if isinstance(to_state, ProposalState):
        to_state = to_state.value
    allowed = state_transitions.get(from_state, [])
    return to_state in allowed


# ---------------------------------------------------------------------------
# Dataclasses de parches
# ---------------------------------------------------------------------------

@dataclass
class ProposalPatch:
    """Parche propuesto para un artículo de ley.

    Representa una propuesta concreta de modificación sobre el corpus
    canónico oficial.
    """
    proposal_id: str
    run_id: str
    boe_id: str
    base_snapshot: str
    base_sha256: str
    article_id: str
    operation: str
    content_before: str
    content_proposed: str
    author: str
    justification: str
    sources: list[str] = field(default_factory=list)
    state: ProposalState = ProposalState.BORRADOR
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    schema_version: str = "1.0"
    approved_by: Optional[str] = None
    audit_result: Optional[str] = None
    legal_review: Optional[str] = None


@dataclass
class PatchManifest:
    """Registro de auditoría de un parche aplicado.

    Incluye hashes antes/después y métricas de cambio para trazabilidad.
    """
    patch_id: str
    proposal_id: str
    run_id: str
    applied_at: str
    base_hash_before: str
    base_hash_after: str
    article_id: str
    words_before: int
    words_after: int
    operation: str
    reversible: bool


# ---------------------------------------------------------------------------
# Serialización / deserialización
# ---------------------------------------------------------------------------

def _serialize(obj: Any) -> Any:
    """Serializa enumeraciones anidadas para JSON."""
    if isinstance(obj, ProposalState):
        return obj.value
    raise TypeError(f"Objeto no serializable: {type(obj)}")


def to_json(data: Any) -> str:
    """Serializa un dataclass a JSON pretty-printed."""
    return json.dumps(asdict(data), indent=2, ensure_ascii=False, default=_serialize)


def from_json(cls: type, json_str: str) -> Any:
    """Deserializa un JSON a la dataclass especificada.

    Para ProposalPatch convierte el campo state de string a ProposalState.
    """
    raw = json.loads(json_str)
    if cls is ProposalPatch and isinstance(raw.get("state"), str):
        raw["state"] = ProposalState(raw["state"])
    return cls(**raw)


# ---------------------------------------------------------------------------
# Hashes SHA-256
# ---------------------------------------------------------------------------

def compute_file_hash(path: str | Path) -> str:
    """Calcula SHA-256 del contenido de un archivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_str_hash(s: str) -> str:
    """Calcula SHA-256 de una cadena UTF-8."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
