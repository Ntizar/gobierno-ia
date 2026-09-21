"""gobierno_ia — Parches versionados para simplificación legislativa."""

__version__ = "0.1.0"

from gobierno_ia.schemas import (
    ProposalState,
    ProposalPatch,
    PatchManifest,
    state_transitions,
    validate_transition,
    to_json,
    from_json,
    compute_file_hash,
    compute_str_hash,
)
