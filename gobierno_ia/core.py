"""
gobierno_ia/core.py — Lógica central de validación, aplicación y reversión de parches.

Principios:
  - NUNCA escribe en data/raw/ ni data/canonical/
  - Opera exclusivamente sobre run_dir/<run_id>/<boe_id>/<article_id>.json
  - Solo stdlib (json, hashlib, os, datetime, uuid, re)
  - Usa las clases de schemas.py cuando están disponibles;
    fallback inline cuando schemas.py aún no existe.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Importar schemas con fallback
# ---------------------------------------------------------------------------
try:
    from gobierno_ia.schemas import (
        ProposalPatch,
        ProposalState,
        PatchManifest,
        state_transitions,
        validate_transition,
        to_json as schema_to_json,
        from_json as schema_from_json,
        compute_file_hash as schema_compute_file_hash,
        compute_str_hash as schema_compute_str_hash,
    )
    _HAS_SCHEMAS = True
except ImportError:
    _HAS_SCHEMAS = False
    ProposalState = None
    ProposalPatch = None
    PatchManifest = None
    state_transitions = {}
    schema_to_json = None
    schema_from_json = None
    schema_compute_file_hash = None
    schema_compute_str_hash = None


# ===========================================================================
# Fallback PatchManifest cuando schemas.py no existe
# ===========================================================================

if PatchManifest is None:
    @dataclass
    class PatchManifest:
        """Registro de auditoría de un parche aplicado."""
        patch_id: str
        proposal_id: str
        run_id: str
        applied_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        base_hash_before: str = ""
        base_hash_after: str = ""
        article_id: str = ""
        words_before: int = 0
        words_after: int = 0
        operation: str = ""
        reversible: bool = True


# ===========================================================================
# 0. Normalización — centralizada aquí
# ===========================================================================

def normalize_text(text: str) -> str:
    """Normaliza un texto legislativo para comparación fiable.

    Pasos:
      1. Reemplaza BOM y zero-width chars
      2. Normaliza Unicode a NFC
      3. Unifica saltos de línea a \\n
      4. Colapsa espacios múltiples (excepto saltos de línea)
      5. Colapsa líneas vacías múltiples
      6. Recorta cabecera y cola
    """
    if not isinstance(text, str):
        return ""
    t = text
    # BOM
    t = t.replace("\ufeff", "")
    # Zero-width characters (ZWSP, ZWNJ, ZWJ, etc.)
    t = re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]", "", t)
    # Unicode NFC
    t = unicodedata.normalize("NFC", t)
    # Unificar saltos de línea
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    # Colapsar espacios múltiples preservando newlines
    t = re.sub(r"[^\S\n]+", " ", t)
    # Colapsar líneas vacías múltiples
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def compute_article_hash(article_text: str) -> str:
    """SHA-256 del texto normalizado de un artículo."""
    normalized = normalize_text(article_text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _word_count(text: str) -> int:
    """Cuenta palabras en un texto normalizado."""
    return len(normalize_text(text).split())


# ===========================================================================
# 1. load_canonical
# ===========================================================================

def load_canonical(boe_id: str, fecha: str) -> dict:
    """Lee data/canonical/<boe_id>/<fecha>.json y retorna el dict completo.

    Raises:
        FileNotFoundError: si el archivo no existe.
        json.JSONDecodeError: si el JSON es inválido.
    """
    path = os.path.join("data", "canonical", boe_id, f"{fecha}.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Canonical no encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# 2. find_article
# ===========================================================================

def find_article(canonical: dict, article_id: str) -> Optional[dict]:
    """Busca un artículo por su 'id' dentro de canonical['articulos'].

    Retorna el dict del artículo o None si no existe.
    """
    for art in canonical.get("articulos", []):
        if art.get("id") == article_id:
            return art
    return None


# ===========================================================================
# 3. validate_patch
# ===========================================================================

_VALID_STATES = {"BORRADOR", "REVISADO"}
_VALID_OPERATIONS = {"reemplazar", "insertar", "eliminar", "fusionar"}
_EXPECTED_SCHEMA_VERSION = "1.0"


def validate_patch(patch_dict: dict, canonical: dict) -> tuple[bool, list[str]]:
    """Valida un parche contra el canonical.

    Checks:
      - schema_version es "1.0"
      - state es BORRADOR o REVISADO
      - base_sha256 coincide con canonical['source_sha256']
      - article_id existe en canonical
      - content_before coincide con el texto actual del artículo (normalizado)

    Retorna (es_valido, lista_de_errores).
    """
    errors: list[str] = []

    # --- schema_version ---
    sv = patch_dict.get("schema_version", "")
    if sv != _EXPECTED_SCHEMA_VERSION:
        errors.append(
            f"schema_version inválida: esperado '{_EXPECTED_SCHEMA_VERSION}', "
            f"recibido '{sv}'"
        )

    # --- state ---
    state = patch_dict.get("state", "")
    # Aceptar tanto string como ProposalState enum
    if hasattr(state, "value"):
        state_str = state.value
    else:
        state_str = str(state)
    if state_str not in _VALID_STATES:
        errors.append(
            f"state inválido: '{state_str}'. Valores permitidos: {_VALID_STATES}"
        )

    # --- base_sha256 vs canonical ---
    base_sha = patch_dict.get("base_sha256", "")
    canonical_sha = canonical.get("source_sha256", "")
    if base_sha != canonical_sha:
        errors.append(
            f"base_sha256 no coincide con canonical: "
            f"patch='{base_sha[:16]}...' canonical='{canonical_sha[:16]}...'"
        )

    # --- article_id existe ---
    article_id = patch_dict.get("article_id", "")
    article = find_article(canonical, article_id)
    if article is None:
        errors.append(
            f"article_id '{article_id}' no encontrado en canonical"
        )
    else:
        # --- content_before coincide ---
        content_before = patch_dict.get("content_before", "")
        article_text = article.get("texto", "")
        norm_before = normalize_text(content_before)
        norm_article = normalize_text(article_text)
        if norm_before != norm_article:
            if not content_before:
                errors.append("content_before está vacío")
            elif not article_text:
                errors.append("artículo canonical tiene texto vacío")
            else:
                # Diagnóstico: primera diferencia
                min_len = min(len(norm_before), len(norm_article))
                first_diff = -1
                for i in range(min_len):
                    if norm_before[i] != norm_article[i]:
                        first_diff = i
                        break
                if first_diff == -1 and len(norm_before) != len(norm_article):
                    first_diff = min_len
                preview_b = norm_before[max(0, first_diff - 20):first_diff + 20]
                preview_a = norm_article[max(0, first_diff - 20):first_diff + 20]
                errors.append(
                    f"content_before no coincide con texto del artículo "
                    f"(primera diferencia en char {first_diff}). "
                    f"patch='…{preview_b}…' canonical='…{preview_a}…'"
                )

    return (len(errors) == 0, errors)


# ===========================================================================
# 4. apply_patch
# ===========================================================================

def apply_patch(patch_dict: dict, run_dir: str) -> PatchManifest:
    """Aplica un parche y genera el manifest resultante.

    REGLAS ABSOLUTAS:
      - NO escribe en data/raw/ ni data/canonical/
      - Solo escribe en run_dir/<run_id>/<boe_id>/<article_id>.json

    Flujo:
      1. Extraer run_id, boe_id, article_id del parche
      2. Leer el canonical para obtener el texto actual
      3. Aplicar la operación (reemplazar, insertar, eliminar, fusionar)
      4. Guardar el resultado en run_dir
      5. Generar el PatchManifest con hashes antes/después

    Raises:
        ValueError: si la operación no es válida o la validación falla.
    """
    # --- Extraer campos del parche ---
    run_id = patch_dict.get("run_id", "")
    boe_id = patch_dict.get("boe_id", "")
    article_id = patch_dict.get("article_id", "")
    operation = patch_dict.get("operation", "")
    content_proposed = patch_dict.get("content_proposed", "")
    proposal_id = patch_dict.get("proposal_id", "")

    if not run_id:
        raise ValueError("patch_dict debe tener 'run_id'")
    if not boe_id:
        raise ValueError("patch_dict debe tener 'boe_id'")
    if not article_id:
        raise ValueError("patch_dict debe tener 'article_id'")
    if operation not in _VALID_OPERATIONS:
        raise ValueError(
            f"operation '{operation}' no válida. "
            f"Permitidas: {_VALID_OPERATIONS}"
        )

    # --- Leer canonical (solo lectura, nunca escritura) ---
    canonical_dir = os.path.join("data", "canonical", boe_id)
    if not os.path.isdir(canonical_dir):
        raise FileNotFoundError(
            f"Directorio canonical no encontrado: {canonical_dir}"
        )
    fecha_files = sorted(
        f for f in os.listdir(canonical_dir)
        if f.endswith(".json")
    )
    if not fecha_files:
        raise FileNotFoundError(
            f"No hay JSONs canónicos para {boe_id}"
        )
    canonical_path = os.path.join(canonical_dir, fecha_files[-1])
    with open(canonical_path, "r", encoding="utf-8") as f:
        canonical = json.load(f)

    article = find_article(canonical, article_id)
    if article is None:
        raise ValueError(
            f"article_id '{article_id}' no encontrado en {boe_id}"
        )

    original_text = article.get("texto", "")
    original_text_norm = normalize_text(original_text)
    before_hash = compute_article_hash(original_text)
    words_before = _word_count(original_text)

    # --- Aplicar operación ---
    if operation == "reemplazar":
        new_text = content_proposed
    elif operation == "insertar":
        new_text = original_text + "\n\n" + content_proposed
    elif operation == "eliminar":
        new_text = ""
    elif operation == "fusionar":
        new_text = original_text + "\n\n" + content_proposed
    else:
        raise ValueError(f"Operación no implementada: {operation}")

    new_text_norm = normalize_text(new_text)
    after_hash = compute_article_hash(new_text)
    words_after = _word_count(new_text)

    # --- Guardar resultado en run_dir ---
    patch_id = str(uuid.uuid4())
    out_dir = os.path.join(run_dir, run_id, boe_id)
    os.makedirs(out_dir, exist_ok=True)

    result = {
        "patch_id": patch_id,
        "proposal_id": proposal_id,
        "run_id": run_id,
        "boe_id": boe_id,
        "article_id": article_id,
        "operation": operation,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "content_before": original_text_norm,
        "content_after": new_text_norm,
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "patch": patch_dict,
    }

    def _json_default(obj):
        """Serializa ProposalState y otros tipos no nativos."""
        if hasattr(obj, "value") and hasattr(obj, "name"):
            # ProposalState o similar enum
            return obj.value
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        raise TypeError(f"Objeto no serializable: {type(obj)}")

    out_path = os.path.join(out_dir, f"{article_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=_json_default)

    # --- Generar manifest ---
    now_str = datetime.now(timezone.utc).isoformat()
    manifest = PatchManifest(
        patch_id=patch_id,
        proposal_id=proposal_id,
        run_id=run_id,
        applied_at=now_str,
        base_hash_before=before_hash,
        base_hash_after=after_hash,
        article_id=article_id,
        words_before=words_before,
        words_after=words_after,
        operation=operation,
        reversible=True,
    )

    return manifest


# ===========================================================================
# 5. revert_patch
# ===========================================================================

def revert_patch(patch_manifest, run_dir: str) -> bool:
    """Invierte un parche aplicado.

    Lee el archivo resultado del patch en run_dir y restaura el contenido
    anterior (content_before). Retorna True si tuvo éxito.

    Genera un archivo de reversión en
    run_dir/<run_id>/<boe_id>/<article_id>_reverted.json para trazabilidad.

    NOTA: Esto NO modifica data/canonical.
    """
    # Aceptar dict o PatchManifest con atributos
    if isinstance(patch_manifest, dict):
        run_id = patch_manifest.get("run_id", "")
        boe_id = patch_manifest.get("boe_id", "")
        article_id = patch_manifest.get("article_id", "")
        proposal_id = patch_manifest.get("proposal_id", "")
    else:
        run_id = getattr(patch_manifest, "run_id", "")
        article_id = getattr(patch_manifest, "article_id", "")
        proposal_id = getattr(patch_manifest, "proposal_id", "")
        # PatchManifest de schemas.py no tiene boe_id — extraer del path
        boe_id = ""

    if not run_id or not article_id:
        return False

    # --- Localizar el archivo de patch ---
    # Si no tenemos boe_id del manifest, buscarlo en run_dir
    if not boe_id:
        run_path = os.path.join(run_dir, run_id)
        if not os.path.isdir(run_path):
            return False
        boe_dirs = [
            d for d in os.listdir(run_path)
            if os.path.isdir(os.path.join(run_path, d))
        ]
        if not boe_dirs:
            return False
        boe_id = boe_dirs[0]

    original_path = os.path.join(
        run_dir, run_id, boe_id, f"{article_id}.json"
    )

    if not os.path.isfile(original_path):
        return False

    # --- Leer el archivo de patch ---
    with open(original_path, "r", encoding="utf-8") as f:
        patch_data = json.load(f)

    content_before = patch_data.get("content_before", "")
    if not content_before:
        return False

    # --- Crear archivo de reversión ---
    reverted_path = os.path.join(
        run_dir, run_id, boe_id, f"{article_id}_reverted.json"
    )

    reverted = {
        "reverted_from": patch_data.get("patch_id", ""),
        "proposal_id": proposal_id,
        "run_id": run_id,
        "boe_id": boe_id,
        "article_id": article_id,
        "restored_content": content_before,
        "restored_hash": compute_article_hash(content_before),
        "reverted_at": datetime.now(timezone.utc).isoformat(),
    }

    os.makedirs(os.path.dirname(reverted_path), exist_ok=True)
    with open(reverted_path, "w", encoding="utf-8") as f:
        json.dump(reverted, f, indent=2, ensure_ascii=False)

    return True


# ===========================================================================
# 6. segment_articles
# ===========================================================================

def segment_articles(canonical: dict) -> dict[str, str]:
    """Extrae todos los artículos normalizados como {article_id: texto}.

    Retorna un dict con article_id como clave y el texto normalizado como valor.
    """
    result: dict[str, str] = {}
    for art in canonical.get("articulos", []):
        aid = art.get("id", "")
        texto = art.get("texto", "")
        if aid:
            result[aid] = normalize_text(texto)
    return result


# ===========================================================================
# Utilities de conveniencia
# ===========================================================================

def compute_file_hash(filepath: str) -> str:
    """SHA-256 de un archivo completo."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_str_hash(text: str) -> str:
    """SHA-256 de una cadena de texto UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def to_json(obj: Any, indent: int = 2) -> str:
    """Serializa un objeto a JSON string con ensure_ascii=False.

    Si schemas.py está disponible, delega a su serializer para dataclasses.
    """
    if _HAS_SCHEMAS and schema_to_json is not None and hasattr(obj, "__dataclass_fields__"):
        return schema_to_json(obj)
    if hasattr(obj, "to_dict"):
        return json.dumps(obj.to_dict(), indent=indent, ensure_ascii=False)
    if hasattr(obj, "__dict__"):
        return json.dumps(
            obj.__dict__, indent=indent, ensure_ascii=False, default=str
        )
    return json.dumps(obj, indent=indent, ensure_ascii=False, default=str)


def from_json(text: str, cls: type = None) -> Any:
    """Deserializa JSON string.

    Si cls es ProposalPatch y schemas.py está disponible, usa su deserializer.
    """
    if _HAS_SCHEMAS and schema_from_json is not None and cls is not None:
        return schema_from_json(cls, text)
    return json.loads(text)


# ===========================================================================
# Helpers de consulta de estado de parches
# ===========================================================================

def list_applied_patches(run_dir: str, run_id: str = None) -> list[dict]:
    """Lista todos los parches aplicados en un run_dir.

    Si run_id se especifica, solo lista los de ese run.
    Retorna una lista de dicts con la información de cada patch.
    """
    results: list[dict] = []
    if not os.path.isdir(run_dir):
        return results

    run_ids = [run_id] if run_id else [
        d for d in os.listdir(run_dir)
        if os.path.isdir(os.path.join(run_dir, d))
    ]

    for rid in run_ids:
        run_path = os.path.join(run_dir, rid)
        if not os.path.isdir(run_path):
            continue
        for boe_dir in os.listdir(run_path):
            boe_path = os.path.join(run_path, boe_dir)
            if not os.path.isdir(boe_path):
                continue
            for fname in os.listdir(boe_path):
                if fname.endswith(".json") and not fname.endswith("_reverted.json"):
                    fpath = os.path.join(boe_path, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        data["_file"] = fpath
                        results.append(data)
                    except (json.JSONDecodeError, OSError):
                        continue

    return results


def get_patch_state(patch_dict: dict) -> str:
    """Retorna el estado de un parche (BORRADOR, REVISADO, etc.)."""
    state = patch_dict.get("state", "DESCONOCIDO")
    if hasattr(state, "value"):
        return state.value
    return str(state)


def is_reversible(patch_manifest) -> bool:
    """Verifica si un parche puede ser revertido."""
    if isinstance(patch_manifest, dict):
        return patch_manifest.get("reversible", False)
    return getattr(patch_manifest, "reversible", False)
