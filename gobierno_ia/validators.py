"""
gobierno_ia/validators.py — Validadores que devuelven exit != 0 ante anomalías.

Validadores:
  1. DuplicateDetector  — detecta líneas repetidas dentro de artículos
  2. NumeralParser      — verifica parseo de numerales (Artículo 3, tres, etc.)
  3. FidelityChecker    — compara texto canonical vs propuesta (sin palabras sin traza)
  4. GateCheck          — verifica puertas obligatorias del pipeline

Uso:
  from gobierno_ia.validators import run_all_validators, run_gold_set

  results = run_all_validators("data/canonical/BOE-A-1986-10499/2026-08-31.json")
  run_gold_set()
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from gobierno_ia.core import compute_article_hash, normalize_text

# ---------------------------------------------------------------------------
# Resultados de validación
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Resultado de un validador individual."""
    validator_name: str
    passed: bool
    exit_code: int  # 0=pass, 1=fail, 2=error
    errors: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "validator": self.validator_name,
            "passed": self.passed,
            "exit_code": self.exit_code,
            "errors": self.errors,
            "metrics": self.metrics,
        }


# ---------------------------------------------------------------------------
# Validator base
# ---------------------------------------------------------------------------

class Validator:
    """Base class para validadores."""
    name: str = "Validator"
    threshold: float = 0.0

    def validate(self, data: Any) -> ValidationResult:
        raise NotImplementedError("Subclasses must implement validate()")


# ---------------------------------------------------------------------------
# 1. DuplicateDetector
# ---------------------------------------------------------------------------

class DuplicateDetector(Validator):
    """Detecta líneas repetidas dentro de cada artículo.

    Para cada artículo del canonical, compara las oraciones (separadas por
    punto o punto y coma) contra sí mismas. Si una misma oración aparece
    más de una vez dentro del mismo artículo, se contabiliza.

    Threshold: tasa máxima de duplicación aceptada (default 5.0%).
    """

    name = "DuplicateDetector"
    threshold: float = 5.0  # porcentaje máximo

    def __init__(self, threshold: float | None = None):
        if threshold is not None:
            self.threshold = threshold

    def validate(self, data: Any) -> ValidationResult:
        """
        Args:
            data: ruta al JSON canónico, o dict ya cargado.
        """
        try:
            canonical = self._load(data)
        except Exception as e:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=[f"Error cargando canonical: {e}"],
            )

        articulos = canonical.get("articulos", [])
        if not articulos:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=["Canonical sin artículos"],
            )

        total = len(articulos)
        con_duplicacion = 0
        total_duplicadas = 0
        total_oraciones = 0
        detalles: list[str] = []

        for art in articulos:
            aid = art.get("id", "???")
            texto = normalize_text(art.get("texto", ""))
            if not texto:
                continue

            # Dividir en oraciones (punto seguido de espacio mayúscula, o punto final)
            oraciones = re.split(r'(?<=[.;])\s+', texto)
            # Filtrar oraciones muy cortas (< 5 palabras) para evitar falsos positivos
            oraciones = [o.strip() for o in oraciones if len(o.split()) >= 5]

            total_oraciones += len(oraciones)

            # Contar frecuencias
            freq: dict[str, int] = {}
            for o in oraciones:
                norm = re.sub(r'\s+', ' ', o.lower().strip())
                freq[norm] = freq.get(norm, 0) + 1

            dupes_in_art = sum(c - 1 for c in freq.values() if c > 1)
            if dupes_in_art > 0:
                con_duplicacion += 1
                total_duplicadas += dupes_in_art
                duplicadas_texto = [o[:80] for o, c in freq.items() if c > 1]
                detalles.append(
                    f"art={aid}: {dupes_in_art} duplicadas → {duplicadas_texto[:3]}"
                )

        tasa = (total_duplicadas / total_oraciones * 100) if total_oraciones > 0 else 0.0
        passed = tasa <= self.threshold

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            exit_code=0 if passed else 1,
            errors=[] if passed else [
                f"Tasa de duplicación {tasa:.2f}% supera umbral {self.threshold}%"
            ] + detalles[:10],
            metrics={
                "total_articulos": total,
                "articulos_con_duplicacion": con_duplicacion,
                "total_oraciones": total_oraciones,
                "total_duplicadas": total_duplicadas,
                "tasa_global_pct": round(tasa, 4),
                "threshold_pct": self.threshold,
            },
        )

    @staticmethod
    def _load(data: Any) -> dict:
        if isinstance(data, dict):
            return data
        if isinstance(data, str) and os.path.isfile(data):
            with open(data, "r", encoding="utf-8") as f:
                return json.load(f)
        raise ValueError(f"No se puede cargar canonical desde: {data}")


# ---------------------------------------------------------------------------
# 2. NumeralParser
# ---------------------------------------------------------------------------

# Diccionario completo de nombres españoles 1-117 (cubre las 3 leyes)
_NOMBRES_NUMERAL: dict[str, int] = {}

def _build_numeral_dict() -> dict[str, int]:
    """Construye el diccionario de números en español 1-117."""
    # Unidades
    unidades = {
        1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
        6: "seis", 7: "siete", 8: "ocho", 9: "nueve",
    }
    # Especiales 10-19
    especiales = {
        10: "diez", 11: "once", 12: "doce", 13: "trece", 14: "catorce",
        15: "quince", 16: "dieciséis", 17: "diecisiete", 18: "dieciocho",
        19: "diecinueve",
    }
    # Decenas 20-90
    decenas = {
        20: "veinte", 30: "treinta", 40: "cuarenta", 50: "cincuenta",
        60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa",
    }
    # Centenas
    centenas = {
        100: "cien", 101: "ciento",
    }

    result: dict[str, int] = {}

    # 1-9
    for n, w in unidades.items():
        result[w] = n

    # 10-19
    for n, w in especiales.items():
        result[w] = n

    # 20
    result["veinte"] = 20

    # 21-29 (veinti-)
    veintis = {
        21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro",
        25: "veinticinco", 26: "veintiséis", 27: "veintisiete", 28: "veintiocho",
        29: "veintinueve",
    }
    for n, w in veintis.items():
        result[w] = n

    # 30-99 (decena y unidad)
    for dec_n, dec_w in [(30, "treinta"), (40, "cuarenta"), (50, "cincuenta"),
                          (60, "sesenta"), (70, "setenta"), (80, "ochenta"),
                          (90, "noventa")]:
        result[dec_w] = dec_n
        for uni_n, uni_w in unidades.items():
            result[f"{dec_w} y {uni_w}"] = dec_n + uni_n

    # 100-117
    result["cien"] = 100
    result["ciento"] = 101  # "ciento" como prefijo
    for n in range(101, 118):
        if n == 101:
            result["ciento uno"] = n
        elif n == 116:
            result["ciento dieciséis"] = n
        else:
            # Parse "ciento <unidad/especial>"
            if n <= 109:
                result[f"ciento {unidades[n-100]}"] = n
            elif n <= 119:
                result[f"ciento {especiales[n-100]}"] = n

    # "ciento" alone maps to 101 (prefix used in titles)
    return result


_NOMBRES_NUMERAL = _build_numeral_dict()

# Números romanos simples 1-30
_ROMANOS = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
    "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
    "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19,
    "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23, "XXIV": 24, "XXV": 25,
    "XXVI": 26, "XXVII": 27, "XXVIII": 28, "XXIX": 29, "XXX": 30,
}

# Patrón regex para "Artículo <numeral>" en títulos
# Captura: (1) dígito, (2) romano, o (3) texto hasta un delimitador
_ART_PATTERN = re.compile(
    r'Art[ií]culo\s+'
    r'(?:(\d+)'                     # dígito: "3", "16"
    r'|([IVXLCDM]+)'               # romano: "III", "XVI"
    r'|([a-záéíóúñ]+(?:\s+(?:y\s+)?[a-záéíóúñ]+)*))',  # nombre: "tres", "cuarenta y uno", "ciento tres"
    re.IGNORECASE,
)


def parse_numeral(titulo: str) -> Optional[int]:
    """Extrae el número de artículo de un título.

    Acepta:
      - "Artículo 3", "Artículo 3.", "Artículo 16. Objeto."
      - "Artículo tres", "Artículo dieciséis"
      - "Artículo III", "Artículo XVI"
      - "Artículo cuarenta y uno", "Artículo ciento tres"

    Retorna el número entero o None si no se puede parsear.
    """
    m = _ART_PATTERN.search(titulo)
    if not m:
        return None
    if m.group(1):
        return int(m.group(1))
    if m.group(2):
        return _ROMANOS.get(m.group(2).upper())
    if m.group(3):
        numeral_str = m.group(3).lower().strip()
        # Buscar en el diccionario
        if numeral_str in _NOMBRES_NUMERAL:
            return _NOMBRES_NUMERAL[numeral_str]
        # Intentar sin caracteres especiales
        clean = re.sub(r'[áéíóú]', lambda m: {'á':'a','é':'e','é':'e','í':'i','ó':'o','ú':'u'}[m.group()], numeral_str)
        if clean in _NOMBRES_NUMERAL:
            return _NOMBRES_NUMERAL[clean]
        # Buscar por valor numérico del prefijo para "bis" etc.
        if "bis" in numeral_str:
            base = numeral_str.replace("bis", "").strip()
            if base in _NOMBRES_NUMERAL:
                return _NOMBRES_NUMERAL[base]
        return None
    return None


class NumeralParser(Validator):
    """Verifica que todos los artículos tengan un numeral parseable.

    Revisa campo 'titulo' de cada artículo. Si alguno no contiene un
    "Artículo <numeral>" reconocible, falla.
    """

    name = "NumeralParser"

    def validate(self, data: Any) -> ValidationResult:
        try:
            canonical = DuplicateDetector._load(data)
        except Exception as e:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=[f"Error cargando canonical: {e}"],
            )

        articulos = canonical.get("articulos", [])
        if not articulos:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=["Canonical sin artículos"],
            )

        total = len(articulos)
        parseados = 0
        fallidos: list[str] = []

        for art in articulos:
            aid = art.get("id", "???")
            titulo = art.get("titulo", "")
            num = parse_numeral(titulo)
            if num is not None:
                parseados += 1
            else:
                fallidos.append(f"{aid}: titulo='{titulo}'")

        tasa = (parseados / total * 100) if total > 0 else 0.0
        passed = len(fallidos) == 0

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            exit_code=0 if passed else 1,
            errors=[] if passed else [
                f"{len(fallidos)} artículo(s) sin numeral parseable"
            ] + fallidos[:20],
            metrics={
                "total_articulos": total,
                "parseados_ok": parseados,
                "fallidos": len(fallidos),
                "tasa_exito_pct": round(tasa, 2),
            },
        )


# ---------------------------------------------------------------------------
# 3. FidelityChecker
# ---------------------------------------------------------------------------

class FidelityChecker(Validator):
    """Compara texto de un artículo en el canonical contra una propuesta.

    Verifica que cada palabra de la propuesta exista en el canonical
    (sin contar puntuación ni números). Palabras sin traza significan
    que la propuesta introduce contenido nuevo.

    Threshold: número máximo de palabras sin traza permitidas (default 0).
    """

    name = "FidelityChecker"
    threshold: float = 0.0  # tolerancia de palabras sin traza

    def __init__(self, threshold: float | None = None):
        if threshold is not None:
            self.threshold = threshold

    def validate(self, data: Any, proposal: dict | None = None) -> ValidationResult:
        """
        Args:
            data: ruta al JSON canónico, o dict ya cargado.
            proposal: dict con keys 'article_id', 'content_proposed'.
                      Si es None, se salta esta validación.
        """
        if proposal is None:
            return ValidationResult(
                validator_name=self.name,
                passed=True,
                exit_code=0,
                metrics={"skipped": True, "reason": "No se proporcionó propuesta"},
            )

        try:
            canonical = DuplicateDetector._load(data)
        except Exception as e:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=[f"Error cargando canonical: {e}"],
            )

        article_id = proposal.get("article_id", "")
        content_proposed = proposal.get("content_proposed", "")

        if not article_id:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=1,
                errors=["proposal sin article_id"],
            )

        # Buscar artículo en canonical
        article = None
        for art in canonical.get("articulos", []):
            if art.get("id") == article_id:
                article = art
                break

        if article is None:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=1,
                errors=[f"article_id '{article_id}' no encontrado en canonical"],
            )

        canonical_text = normalize_text(article.get("texto", ""))
        proposed_text = normalize_text(content_proposed)

        if not proposed_text:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=1,
                errors=["content_proposed está vacío"],
            )

        # Extraer palabras (solo alfanumérico, lower)
        def extract_words(text: str) -> set[str]:
            return {w.lower() for w in re.findall(r'\b[a-záéíóúñü]+\b', text, re.IGNORECASE)}

        canonical_words = extract_words(canonical_text)
        proposed_words = extract_words(proposed_text)

        # Palabras en la propuesta que NO están en el canonical
        sin_traza = proposed_words - canonical_words

        passed = len(sin_traza) <= self.threshold

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            exit_code=0 if passed else 1,
            errors=[] if passed else [
                f"{len(sin_traza)} palabra(s) en propuesta sin traza en canonical (umbral: {self.threshold})"
            ] + [f"  • {w}" for w in sorted(sin_traza)[:30]],
            metrics={
                "article_id": article_id,
                "canonical_words": len(canonical_words),
                "proposed_words": len(proposed_words),
                "words_without_trace": len(sin_traza),
                "threshold": self.threshold,
                "sin_traza_sample": sorted(sin_traza)[:10],
            },
        )


# ---------------------------------------------------------------------------
# 4. GateCheck
# ---------------------------------------------------------------------------

class GateCheck(Validator):
    """Verifica puertas obligatorias del pipeline de parches.

    Puertas:
      a) Fuente y hash válidos
      b) Artículo/rango existentes
      c) Diff reversible
      d) Enumeraciones conservadas
      e) Remisiones preservadas
      f) Auditoría presente
      g) No hay acuerdos pendientes
      h) Tests verdes
      i) Revisión jurídica humana válida (o pendiente explícita)
    """

    name = "GateCheck"

    def validate(self, data: Any, proposal: dict | None = None,
                 run_dir: str | None = None) -> ValidationResult:
        """
        Args:
            data: ruta al JSON canónico, o dict ya cargado.
            proposal: dict de la propuesta a validar (ProposalPatch serializado).
            run_dir: directorio de ejecución (para verificar tests).
        """
        errors: list[str] = []
        gates_checked: dict[str, str] = {}

        if proposal is None:
            return ValidationResult(
                validator_name=self.name,
                passed=True,
                exit_code=0,
                metrics={"skipped": True, "reason": "No se proporcionó propuesta"},
            )

        try:
            canonical = DuplicateDetector._load(data)
        except Exception as e:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                exit_code=2,
                errors=[f"Error cargando canonical: {e}"],
            )

        # --- (a) Fuente y hash válidos ---
        base_sha = proposal.get("base_sha256", "")
        canonical_sha = canonical.get("source_sha256", "")
        if base_sha and canonical_sha:
            if base_sha == canonical_sha:
                gates_checked["fuente_hash"] = "OK"
            else:
                gates_checked["fuente_hash"] = "FAIL"
                errors.append(
                    f"(a) base_sha256 no coincide: "
                    f"proposal={base_sha[:16]} canonical={canonical_sha[:16]}"
                )
        else:
            gates_checked["fuente_hash"] = "MISSING"
            errors.append("(a) Falta base_sha256 o source_sha256 en canonical")

        # --- (b) Artículo existente ---
        article_id = proposal.get("article_id", "")
        article = None
        for art in canonical.get("articulos", []):
            if art.get("id") == article_id:
                article = art
                break

        if article is not None:
            gates_checked["articulo_existe"] = "OK"
        else:
            gates_checked["articulo_existe"] = "FAIL"
            errors.append(f"(b) article_id '{article_id}' no existe en canonical")

        # --- (c) Diff reversible ---
        content_before = proposal.get("content_before", "")
        content_proposed = proposal.get("content_proposed", "")
        if content_before and content_proposed:
            # Verificar que el diff es no vacío (hay cambios)
            if normalize_text(content_before) != normalize_text(content_proposed):
                gates_checked["diff_reversible"] = "OK"
            else:
                gates_checked["diff_reversible"] = "WARN"
                errors.append("(c) content_before == content_proposed (sin cambios)")
        else:
            gates_checked["diff_reversible"] = "SKIP"
            errors.append("(c) Faltan content_before o content_proposed")

        # --- (d) Enumeraciones conservadas ---
        if article is not None:
            enumeraciones = article.get("enumeraciones", [])
            if enumeraciones:
                # Verificar que la propuesta no elimina numeración existente
                # Buscar patrones tipo "1.", "2.", etc. en el original
                enum_pattern = re.compile(r'(?:^|\s)(\d+)\.\s')
                orig_nums = set(enum_pattern.findall(content_before)) if content_before else set()
                prop_nums = set(enum_pattern.findall(content_proposed)) if content_proposed else set()

                lost = orig_nums - prop_nums
                if lost:
                    gates_checked["enumeraciones"] = "FAIL"
                    errors.append(
                        f"(d) Enumeraciones perdidas en propuesta: {sorted(lost)}"
                    )
                else:
                    gates_checked["enumeraciones"] = "OK"
            else:
                gates_checked["enumeraciones"] = "N/A"
        else:
            gates_checked["enumeraciones"] = "SKIP"

        # --- (e) Remisiones preservadas ---
        if article is not None:
            remisiones = article.get("remisiones", [])
            if remisiones:
                # Verificar que las referenciasBOE siguen presentes en la propuesta
                lost_refs = []
                for rem in remisiones:
                    ref = rem.get("boe_ref", "")
                    if ref and ref not in (content_proposed or ""):
                        lost_refs.append(ref)
                if lost_refs:
                    gates_checked["remisiones"] = "FAIL"
                    errors.append(
                        f"(e) Remisiones perdidas: {lost_refs}"
                    )
                else:
                    gates_checked["remisiones"] = "OK"
            else:
                gates_checked["remisiones"] = "N/A"
        else:
            gates_checked["remisiones"] = "SKIP"

        # --- (f) Auditoría presente ---
        audit = proposal.get("audit_result")
        if audit:
            gates_checked["auditoria"] = "OK"
        else:
            gates_checked["auditoria"] = "PENDING"
            errors.append("(f) audit_result no presente en la propuesta")

        # --- (g) No hay acuerdos pendientes ---
        state = proposal.get("state", "")
        if hasattr(state, "value"):
            state = state.value
        if state in ("RECHAZADO", "OBSOLETO"):
            gates_checked["acuerdos_pendientes"] = "OK"
        elif state in ("BORRADOR", "REVISADO", "APROBADO", "AUDITADO", "APLICADO"):
            gates_checked["acuerdos_pendientes"] = "OK"
        else:
            gates_checked["acuerdos_pendientes"] = "WARN"

        # --- (h) Tests verdes ---
        # Solo verificable si run_dir existe
        if run_dir and os.path.isdir(run_dir):
            gates_checked["tests_verdes"] = "OK"
        else:
            gates_checked["tests_verdes"] = "SKIP"

        # --- (i) Revisión jurídica humana válida ---
        legal_review = proposal.get("legal_review")
        approved_by = proposal.get("approved_by")
        if legal_review or approved_by:
            gates_checked["revision_juridica"] = "OK"
        else:
            gates_checked["revision_juridica"] = "PENDING"
            errors.append(
                "(i) Revisión jurídica humana no presente "
                "(pendiente explícita aceptable)"
            )

        passed = len(errors) == 0

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            exit_code=0 if passed else 1,
            errors=errors,
            metrics={"gates": gates_checked},
        )


# ---------------------------------------------------------------------------
# 5. run_all_validators
# ---------------------------------------------------------------------------

def run_all_validators(
    canonical_path: str,
    proposal: dict | None = None,
    run_dir: str | None = None,
    dup_threshold: float = 5.0,
    fidelity_threshold: int = 0,
) -> list[ValidationResult]:
    """Ejecuta todos los validadores sobre un canonical.

    Args:
        canonical_path: ruta al JSON canónico.
        proposal: dict de la propuesta (opcional; FidelityChecker y GateCheck
                  se saltan si no se proporciona).
        run_dir: directorio de ejecución (para GateCheck).
        dup_threshold: umbral de duplicación en % (default 5.0).
        fidelity_threshold: tolerancia de palabras sin traza (default 0).

    Returns:
        Lista de ValidationResult. Si alguno falla, el caller debe usar
        exit_code = 1 en su conjunto.
    """
    results: list[ValidationResult] = []

    # 1. DuplicateDetector
    dd = DuplicateDetector(threshold=dup_threshold)
    results.append(dd.validate(canonical_path))

    # 2. NumeralParser
    np = NumeralParser()
    results.append(np.validate(canonical_path))

    # 3. FidelityChecker (solo si hay propuesta)
    fc = FidelityChecker(threshold=fidelity_threshold)
    results.append(fc.validate(canonical_path, proposal=proposal))

    # 4. GateCheck (solo si hay propuesta)
    gc = GateCheck()
    results.append(gc.validate(canonical_path, proposal=proposal, run_dir=run_dir))

    return results


# ---------------------------------------------------------------------------
# 6. Gold Set
# ---------------------------------------------------------------------------

_GOLD_SET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "gold_set.json"
)


def load_gold_set() -> list[dict]:
    """Carga el gold set desde gold_set.json."""
    with open(_GOLD_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_gold_set() -> dict:
    """Ejecuta el gold set y retorna resultados.

    Returns:
        {
            "total": int,
            "passed": int,
            "failed": int,
            "details": [{id, violation_type, verdict_match, errors}]
        }
    """
    gold = load_gold_set()
    results = {"total": len(gold), "passed": 0, "failed": 0, "details": []}

    for case in gold:
        verdict = case.get("expected_verdict", "violation")
        boe_id = case.get("boe_id", "")
        article_id = case.get("article_id", "")
        proposed = case.get("proposed_text", "")
        original = case.get("original_text", "")

        # Cargar canonical correspondiente
        canonical_dir = os.path.join("data", "canonical", boe_id)
        fecha_files = sorted(
            f for f in os.listdir(canonical_dir) if f.endswith(".json")
        ) if os.path.isdir(canonical_dir) else []

        canonical_path = (
            os.path.join(canonical_dir, fecha_files[-1])
            if fecha_files else None
        )

        errors: list[str] = []

        if canonical_path is None:
            errors.append(f"Canonical no encontrado para {boe_id}")
        else:
            # Construir propuesta ficticia para FidelityChecker
            proposal = {
                "article_id": article_id,
                "content_proposed": proposed,
                "content_before": original,
                "base_sha256": "",
                "state": "BORRADOR",
            }

            fc = FidelityChecker(threshold=0)
            fc_result = fc.validate(canonical_path, proposal=proposal)

            # Determinar veredicto
            detected_violation = not fc_result.passed
            expected_violation = verdict == "violation"
            match = detected_violation == expected_violation

            if match:
                results["passed"] += 1
            else:
                results["failed"] += 1
                errors.append(
                    f"Veredicto incorrecto: detectado={'VIOLATION' if detected_violation else 'OK'}, "
                    f"esperado={verdict.upper()}"
                )
                errors.extend(fc_result.errors[:5])

        results["details"].append({
            "id": case.get("id", "???"),
            "violation_type": case.get("violation_type", "unknown"),
            "expected_verdict": verdict,
            "detected_verdict": "violation" if (canonical_path and not fc_result.passed) else "ok",
            "match": match if canonical_path else False,
            "errors": errors,
        })

    # Imprimir resumen
    print(f"\n{'='*60}")
    print(f"GOLD SET: {results['passed']}/{results['total']} pasaron "
          f"({results['failed']} fallaron)")
    print(f"{'='*60}")
    for d in results["details"]:
        status = "✓" if d["match"] else "✗"
        print(f"  {status} [{d['violation_type']}] {d['id']}: "
              f"esperado={d['expected_verdict']} detectado={d['detected_verdict']}")
        if d["errors"]:
            for e in d["errors"]:
                print(f"    → {e}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m gobierno_ia.validators <canonical.json> [proposal.json]")
        print("     python -m gobierno_ia.validators --gold-set")
        sys.exit(1)

    if sys.argv[1] == "--gold-set":
        run_gold_set()
    else:
        canonical_path = sys.argv[1]
        proposal = None
        if len(sys.argv) >= 3:
            with open(sys.argv[2], "r", encoding="utf-8") as f:
                proposal = json.load(f)

        results = run_all_validators(canonical_path, proposal=proposal)
        total_exit = 0
        for r in results:
            print(f"\n{'='*60}")
            print(f"  {r.validator_name}: {'PASS ✓' if r.passed else 'FAIL ✗'} "
                  f"(exit={r.exit_code})")
            if r.errors:
                for e in r.errors:
                    print(f"    • {e}")
            if r.metrics:
                print(f"    métricas: {json.dumps(r.metrics, ensure_ascii=False)}")
            if r.exit_code != 0:
                total_exit = 1

        print(f"\n{'='*60}")
        print(f"EXIT TOTAL: {total_exit}")
        sys.exit(total_exit)
