#!/usr/bin/env python3
"""cli.py — CLI principal de gobierno_ia.

Comandos:
    ingest-boe       Lee HTML BOE y genera JSON canónico
    validate-proposal Valida un parche contra el canonical
    apply-patch      Aplica un parche en un run directory
    audit-run        Audita un run: hashes, estado de parches, pendientes
    build-report     Genera informe Markdown del run

Todos los comandos siguen la convención:
    exit 0  → éxito
    exit 1  → error de validación / datos
    exit 2  → error interno / excepción
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Paths del proyecto ──────────────────────────────────────────
_PROYECTO = Path(__file__).resolve().parent.parent
_DATA_RAW = _PROYECTO / "data" / "raw" / "boe"
_DATA_CANONICAL = _PROYECTO / "data" / "canonical"
_RUNS_DIR = _PROYECTO / "runs"


# ══════════════════════════════════════════════════════════════════
#  Utilidades compartidas
# ══════════════════════════════════════════════════════════════════

def _sha256_file(path: Path) -> str:
    """Calcula SHA-256 del contenido de un archivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_str(s: str) -> str:
    """Calcula SHA-256 de una cadena UTF-8."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> Any:
    """Carga un archivo JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    """Escribe un archivo JSON con indentación."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_iso() -> str:
    """Devuelve la marca de tiempo actual en ISO 8601."""
    return datetime.now(timezone.utc).isoformat()


# ══════════════════════════════════════════════════════════════════
#  1. ingest-boe
# ══════════════════════════════════════════════════════════════════

def _extract_title(html_path: Path) -> str:
    """Extrae el título de la ley del tag <title> del HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"<title>(.*?)</title>", line)
            if m:
                raw = m.group(1).strip()
                raw = re.sub(r"^BOE-A-\d{4}-\d+\s*", "", raw)
                return raw
    return "Desconocido"


class _BOEHTMLParser:
    """Parser HTML ligero (stdlib) que extrae div.bloque → h5.articulo + p.parrafo."""

    def __init__(self) -> None:
        from html.parser import HTMLParser

        class _Parser(HTMLParser):
            def __init__(self_p) -> None:
                super().__init__()
                self_p.articles: list[dict] = []
                self_p._in_block = False
                self_p._block_id = None
                self_p._block_depth = 0
                self_p._in_h5 = False
                self_p._in_p = False
                self_p._in_a = False
                self_p._current_title = ""
                self_p._current_text_parts: list[str] = []
                self_p._current_links: list[dict] = []
                self_p._current_link_href = ""
                self_p._current_link_text = ""
                self_p._para_texts: list[str] = []
                self_p._para_links: list[dict] = []

            def handle_starttag(self_p, tag: str, attrs: list) -> None:
                attrs_dict = dict(attrs)
                cls = attrs_dict.get("class", "")

                if tag == "div" and "bloque" in cls.split():
                    self_p._in_block = True
                    self_p._block_id = attrs_dict.get("id", "")
                    self_p._block_depth = 1
                    self_p._current_title = ""
                    self_p._para_texts = []
                    self_p._para_links = []
                    return

                if self_p._in_block:
                    if tag == "div":
                        self_p._block_depth += 1
                    if tag == "h5" and "articulo" in cls.split():
                        self_p._in_h5 = True
                        self_p._current_title = ""
                        return
                    if tag == "p" and "parrafo" in cls.split():
                        self_p._in_p = True
                        self_p._current_text_parts = []
                        self_p._current_links = []
                        return
                    if tag == "a" and self_p._in_p:
                        self_p._in_a = True
                        self_p._current_link_href = attrs_dict.get("href", "")
                        self_p._current_link_text = ""
                        return

            def handle_endtag(self_p, tag: str) -> None:
                if not self_p._in_block:
                    return
                if tag == "h5" and self_p._in_h5:
                    self_p._in_h5 = False
                    return
                if tag == "p" and self_p._in_p:
                    self_p._in_p = False
                    text = " ".join("".join(self_p._current_text_parts).split())
                    if text:
                        self_p._para_texts.append(text)
                        self_p._para_links.extend(self_p._current_links)
                    self_p._current_links = []
                    return
                if tag == "a" and self_p._in_a:
                    self_p._in_a = False
                    if self_p._current_link_href:
                        self_p._current_links.append({
                            "href": self_p._current_link_href,
                            "text": self_p._current_link_text.strip(),
                        })
                    return
                if tag == "div":
                    self_p._block_depth -= 1
                    if self_p._block_depth <= 0:
                        self_p._in_block = False
                        title = self_p._current_title.strip()
                        if title.startswith("Artículo"):
                            self_p.articles.append({
                                "id": self_p._block_id,
                                "titulo": title,
                                "parrafos": self_p._para_texts,
                                "remisiones_raw": self_p._para_links,
                            })
                        self_p._block_id = None

            def handle_data(self_p, data: str) -> None:
                if not self_p._in_block:
                    return
                if self_p._in_h5:
                    self_p._current_title += data
                elif self_p._in_p:
                    self_p._current_text_parts.append(data)
                elif self_p._in_a:
                    self_p._current_link_text += data

        self._parser_cls = _Parser

    def parse(self, html_content: str) -> list[dict]:
        p = self._parser_cls()
        p.feed(html_content)
        return p.articles


def _extract_remisiones(links: list[dict]) -> list[dict]:
    """Extrae remisiones (ref. cruzadas a otros BOEs) de los enlaces."""
    remisiones = []
    for link in links:
        href = link.get("href", "")
        m = re.search(r"id=(BOE-[A-Z]-\d{4}-\d+)", href)
        if m:
            remisiones.append({"boe_ref": m.group(1), "texto": link.get("text", "")})
    return remisiones


def _extract_enumeraciones(texto: str) -> list[str]:
    """Extrae enumeraciones numeradas del texto."""
    enums: list[str] = []
    current_enum: list[str] = []
    for line in texto.split("\n"):
        stripped = line.strip()
        if re.match(r"^\d+\.\s", stripped):
            if current_enum:
                enums.append(" ".join(current_enum))
            current_enum = [stripped]
        elif current_enum and stripped:
            current_enum.append(stripped)
    if current_enum:
        enums.append(" ".join(current_enum))
    return enums


def cmd_ingest_boe(args: argparse.Namespace) -> int:
    """Lee un HTML BOE y genera un JSON canónico.

    Reutiliza la lógica de scripts/parse_boe_canonical.py.
    """
    html_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()

    if not html_path.exists():
        print(f"✗ Error: no existe el archivo HTML: {html_path}", file=sys.stderr)
        return 1

    if output_path.exists():
        print(
            f"✗ Error: ya existe un archivo canónico en {output_path}. "
            "Use una fecha diferente en el nombre para evitar sobrescribir.",
            file=sys.stderr,
        )
        return 1

    # Extraer BOE ID del nombre del directorio padre o del path
    boe_id = "desconocido"
    # Intentar extraer del path: .../boe/<boe-id>/...
    m = re.search(r"boe[/\\](BOE-[A-Z]-\d{4}-\d+)", str(html_path))
    if m:
        boe_id = m.group(1)

    print(f"Procesando: {html_path}")
    print(f"  BOE ID detectado: {boe_id}")

    # SHA-256 del fuente
    sha = _sha256_file(html_path)
    titulo = _extract_title(html_path)

    # Parsear HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = _BOEHTMLParser()
    raw_articles = parser.parse(html_content)

    articulos = []
    total_palabras = 0

    for art in raw_articles:
        texto_plano = " ".join(art["parrafos"])
        texto_plano = re.sub(r"\s+", " ", texto_plano).strip()

        enumeraciones = _extract_enumeraciones(texto_plano)
        remisiones = _extract_remisiones(art["remisiones_raw"])
        palabras = len(texto_plano.split())
        total_palabras += palabras

        articulos.append({
            "id": art["id"],
            "titulo": art["titulo"],
            "texto": texto_plano,
            "enumeraciones": enumeraciones,
            "remisiones": remisiones,
            "palabras": palabras,
        })

    canonical = {
        "schema_version": "1.0",
        "boe_id": boe_id,
        "titulo_ley": titulo,
        "fecha_consulta": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source_sha256": sha,
        "articulos": articulos,
        "total_articulos": len(articulos),
        "total_palabras": total_palabras,
    }

    _write_json(output_path, canonical)

    print(f"  ✓ {len(articulos)} artículos, {total_palabras} palabras")
    print(f"  ✓ Escrito en: {output_path}")
    return 0


# ══════════════════════════════════════════════════════════════════
#  2. validate-proposal
# ══════════════════════════════════════════════════════════════════

def cmd_validate_proposal(args: argparse.Namespace) -> int:
    """Valida un parche contra el canonical.

    Verifica:
    - Estructura del patch (campos obligatorios)
    - Que el boe_id del patch coincide con el canonical
    - Que el base_sha256 del patch coincide con el canonical
    - Que el article_id existe en el canonical
    - Transiciones de estado válidas
    """
    patch_path = Path(args.patch).resolve()
    canonical_path = Path(args.canonical).resolve()

    if not patch_path.exists():
        print(f"✗ Error: no existe el archivo de parche: {patch_path}", file=sys.stderr)
        return 1

    if not canonical_path.exists():
        print(
            f"✗ Error: no existe el archivo canónico: {canonical_path}",
            file=sys.stderr,
        )
        return 1

    # Cargar datos
    patch_data = _load_json(patch_path)
    canonical = _load_json(canonical_path)

    errores: list[str] = []

    # ── Validar campos obligatorios del patch ──
    campos_requeridos = [
        "proposal_id", "run_id", "boe_id", "base_snapshot", "base_sha256",
        "article_id", "operation", "content_before", "content_proposed",
        "author", "justification",
    ]
    for campo in campos_requeridos:
        if campo not in patch_data:
            errores.append(f"Campo obligatorio ausente: '{campo}'")

    if errores:
        for e in errores:
            print(f"  ✗ {e}", file=sys.stderr)
        print(f"\n✗ Parche inválido: {len(errores)} error(es) de estructura", file=sys.stderr)
        return 1

    # ── Validar coherencia con canonical ──

    # boe_id debe coincidir
    if patch_data["boe_id"] != canonical.get("boe_id"):
        errores.append(
            f"boe_id del parche ('{patch_data['boe_id']}') no coincide "
            f"con el canonical ('{canonical.get('boe_id')}')"
        )

    # base_sha256 debe coincidir con source_sha256 del canonical
    if patch_data["base_sha256"] != canonical.get("source_sha256"):
        errores.append(
            f"base_sha256 del parche ('{patch_data['base_sha256']}') no coincide "
            f"con source_sha256 del canonical ('{canonical.get('source_sha256')}')"
        )

    # article_id debe existir en canonical
    article_ids = {a["id"] for a in canonical.get("articulos", [])}
    if patch_data["article_id"] not in article_ids:
        errores.append(
            f"article_id '{patch_data['article_id']}' no existe en el canonical. "
            f"IDs disponibles: {sorted(article_ids)}"
        )

    # ── Validar operación ──
    operaciones_validas = {"sustituir", "insertar", "eliminar", "reformular"}
    if patch_data["operation"] not in operaciones_validas:
        errores.append(
            f"Operación '{patch_data['operation']}' no es válida. "
            f"Debe ser una de: {sorted(operaciones_validas)}"
        )

    # ── Validar content_before si es sustituir ──
    if patch_data["operation"] == "sustituir":
        if not patch_data.get("content_before"):
            errores.append(
                "Para operación 'sustituir', 'content_before' no puede estar vacío"
            )

    # ── Validar content_proposed no vacío ──
    if not patch_data.get("content_proposed", "").strip():
        errores.append("'content_proposed' no puede estar vacío")

    # ── Resultado ──
    if errores:
        for e in errores:
            print(f"  ✗ {e}", file=sys.stderr)
        print(f"\n✗ Parche inválido: {len(errores)} error(es)", file=sys.stderr)
        return 1

    print(f"✓ Parche válido: {patch_data['proposal_id']}")
    print(f"  Artículo: {patch_data['article_id']}")
    print(f"  Operación: {patch_data['operation']}")
    print(f"  Run: {patch_data['run_id']}")
    return 0


# ══════════════════════════════════════════════════════════════════
#  3. apply-patch
# ══════════════════════════════════════════════════════════════════

def cmd_apply_patch(args: argparse.Namespace) -> int:
    """Aplica un parche en un run directory.

    NO toca data/raw/ ni data/canonical/.
    Genera manifest de auditoría.
    """
    patch_path = Path(args.patch).resolve()
    output_dir = Path(args.output_dir).resolve()
    run_id = args.run_id

    if not patch_path.exists():
        print(f"✗ Error: no existe el archivo de parche: {patch_path}", file=sys.stderr)
        return 1

    patch_data = _load_json(patch_path)

    # Validaciones mínimas
    campos_requeridos = ["proposal_id", "boe_id", "article_id", "operation", "content_proposed"]
    for campo in campos_requeridos:
        if campo not in patch_data:
            print(f"✗ Campo obligatorio ausente en el parche: '{campo}'", file=sys.stderr)
            return 1

    # Determinar directorio del run
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Directorio de aplicación (donde se escriben los parches)
    applied_dir = run_dir / "applied"
    applied_dir.mkdir(exist_ok=True)

    # Copiar el parche al directorio del run
    patch_id = patch_data.get("proposal_id", f"patch-{run_id}")
    patch_copy = applied_dir / f"{patch_id}.json"
    _write_json(patch_copy, patch_data)

    # Buscar canonical para calcular hashes
    canonical_path = _DATA_CANONICAL / patch_data["boe_id"]
    if canonical_path.is_dir():
        # Buscar el JSON más reciente
        json_files = sorted(canonical_path.glob("*.json"), reverse=True)
        if json_files:
            canonical_data = _load_json(json_files[0])
            base_hash_before = canonical_data.get("source_sha256", "no-disponible")

            # Calcular hash del texto del artículo
            article_id = patch_data["article_id"]
            texto_before = ""
            for art in canonical_data.get("articulos", []):
                if art["id"] == article_id:
                    texto_before = art.get("texto", "")
                    break

            words_before = len(texto_before.split())
            words_after = len(patch_data["content_proposed"].split())
            base_hash_after = _sha256_str(patch_data["content_proposed"])
        else:
            base_hash_before = "no-disponible"
            base_hash_after = "no-disponible"
            words_before = 0
            words_after = len(patch_data["content_proposed"].split())
    else:
        base_hash_before = "no-disponible"
        base_hash_after = "no-disponible"
        words_before = 0
        words_after = len(patch_data["content_proposed"].split())

    # Generar manifest
    manifest = {
        "patch_id": patch_id,
        "proposal_id": patch_data.get("proposal_id", ""),
        "run_id": run_id,
        "applied_at": _now_iso(),
        "base_hash_before": base_hash_before,
        "base_hash_after": base_hash_after,
        "article_id": patch_data["article_id"],
        "words_before": words_before,
        "words_after": words_after,
        "operation": patch_data["operation"],
        "reversible": patch_data["operation"] != "eliminar",
        "patch_file": str(patch_copy.relative_to(run_dir)),
    }

    manifest_path = run_dir / "manifest.json"
    _write_json(manifest_path, manifest)

    print(f"✓ Parche aplicado en run '{run_id}'")
    print(f"  Parche: {patch_copy}")
    print(f"  Manifest: {manifest_path}")
    print(f"  Artículo: {patch_data['article_id']}")
    print(f"  Operación: {patch_data['operation']}")
    return 0


# ══════════════════════════════════════════════════════════════════
#  4. audit-run
# ══════════════════════════════════════════════════════════════════

def cmd_audit_run(args: argparse.Namespace) -> int:
    """Audita un run: verifica hashes, estado de parches, pendientes."""
    runs_dir = Path(args.runs_dir).resolve()
    run_id = args.run_id
    run_dir = runs_dir / run_id

    if not run_dir.exists():
        print(f"✗ Error: no existe el directorio del run: {run_dir}", file=sys.stderr)
        return 1

    problemas: list[str] = []

    # ── Verificar manifest ──
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        problemas.append("No se encontró manifest.json en el directorio del run")
    else:
        manifest = _load_json(manifest_path)

        # Verificar run_id coincide
        if manifest.get("run_id") != run_id:
            problemas.append(
                f"run_id en manifest ('{manifest.get('run_id')}') no coincide "
                f"con el directorio ('{run_id}')"
            )

        # Verificar que el parche referenciado existe
        patch_file = run_dir / manifest.get("patch_file", "applied/missing.json")
        if not patch_file.exists():
            problemas.append(
                f"Archivo de parche referenciado no existe: {manifest.get('patch_file')}"
            )
        else:
            # Verificar hashes del parche
            patch_data = _load_json(patch_file)
            if patch_data.get("proposal_id") != manifest.get("proposal_id"):
                problemas.append(
                    f"proposal_id en patch ('{patch_data.get('proposal_id')}') no coincide "
                    f"con manifest ('{manifest.get('proposal_id')}')"
                )

            # Verificar canonical sigue existiendo
            boe_id = patch_data.get("boe_id", "")
            canonical_dir = _DATA_CANONICAL / boe_id
            if not canonical_dir.exists():
                problemas.append(
                    f"Directorio canonical no existe: {canonical_dir}"
                )

        print(f"  Manifest: {manifest_path}")
        print(f"    run_id: {manifest.get('run_id')}")
        print(f"    applied_at: {manifest.get('applied_at')}")
        print(f"    operation: {manifest.get('operation')}")
        print(f"    reversible: {manifest.get('reversible')}")
        print(f"    words_before → words_after: {manifest.get('words_before')} → {manifest.get('words_after')}")

    # ── Verificar parches en applied/ ──
    applied_dir = run_dir / "applied"
    if applied_dir.exists():
        patches = sorted(applied_dir.glob("*.json"))
        print(f"\n  Parches encontrados: {len(patches)}")
        for p in patches:
            try:
                pdata = _load_json(p)
                estado = pdata.get("state", "desconocido")
                print(f"    - {p.name}: {pdata.get('proposal_id', '?')} "
                      f"[{pdata.get('operation', '?')}] estado={estado}")
            except Exception as e:
                problemas.append(f"Error leyendo parche {p}: {e}")
    else:
        problemas.append("Directorio 'applied/' no existe o está vacío")

    # ── Verificar archivos de evidencia ──
    evidencia_dir = run_dir / "evidencia"
    if evidencia_dir.exists():
        evidencias = sorted(evidencia_dir.glob("*"))
        print(f"\n  Evidencias: {len(evidencias)}")
    else:
        print(f"\n  Evidencias: ninguna (directorio no existe)")

    # ── Resultado ──
    print()
    if problemas:
        for p in problemas:
            print(f"  ✗ {p}", file=sys.stderr)
        print(f"\n✗ Auditoría con {len(problemas)} problema(s)", file=sys.stderr)
        return 1

    print("✓ Auditoría completada: todo OK")
    return 0


# ══════════════════════════════════════════════════════════════════
#  5. build-report
# ══════════════════════════════════════════════════════════════════

def cmd_build_report(args: argparse.Namespace) -> int:
    """Genera un informe Markdown del run con métricas."""
    runs_dir = Path(args.runs_dir).resolve()
    run_id = args.run_id
    run_dir = runs_dir / run_id

    if not run_dir.exists():
        print(f"✗ Error: no existe el directorio del run: {run_dir}", file=sys.stderr)
        return 1

    # Cargar manifest
    manifest_path = run_dir / "manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = _load_json(manifest_path)

    # Cargar parches
    applied_dir = run_dir / "applied"
    patches: list[dict] = []
    if applied_dir.exists():
        for p in sorted(applied_dir.glob("*.json")):
            try:
                patches.append(_load_json(p))
            except Exception:
                pass

    # ── Construir informe ──
    lines: list[str] = []
    lines.append(f"# Informe de Run: `{run_id}`")
    lines.append("")
    lines.append(f"**Generado:** {_now_iso()}")
    lines.append("")

    # Resumen
    lines.append("## Resumen")
    lines.append("")
    lines.append(f"- **Run ID:** `{run_id}`")
    if manifest:
        lines.append(f"- **Operación:** `{manifest.get('operation', 'N/A')}`")
        lines.append(f"- **Reversible:** {'Sí' if manifest.get('reversible') else 'No'}")
        lines.append(f"- **Applied at:** {manifest.get('applied_at', 'N/A')}")
    lines.append(f"- **Parches aplicados:** {len(patches)}")
    lines.append("")

    # Métricas
    total_words_before = manifest.get("words_before", 0)
    total_words_after = manifest.get("words_after", 0)
    delta = total_words_after - total_words_before
    pct = ((delta / total_words_before) * 100) if total_words_before else 0

    lines.append("## Métricas")
    lines.append("")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---------|-------|")
    lines.append(f"| Palabras antes | {total_words_before} |")
    lines.append(f"| Palabras después | {total_words_after} |")
    lines.append(f"| Δ palabras | {delta:+d} ({pct:+.1f}%) |")
    lines.append(f"| Reversible | {'Sí' if manifest.get('reversible') else 'No'} |")
    lines.append("")

    # Detalle de parches
    if patches:
        lines.append("## Parches Aplicados")
        lines.append("")
        lines.append("| # | Proposal ID | Artículo | Operación | Estado |")
        lines.append("|---|-------------|----------|-----------|--------|")
        for i, p in enumerate(patches, 1):
            lines.append(
                f"| {i} | `{p.get('proposal_id', '?')}` "
                f"| {p.get('article_id', '?')} "
                f"| {p.get('operation', '?')} "
                f"| {p.get('state', 'desconocido')} |"
            )
        lines.append("")
    else:
        lines.append("## Parches Aplicados")
        lines.append("")
        lines.append("No hay parches registrados.")
        lines.append("")

    # Verificación de integridad
    lines.append("## Verificación de Integridad")
    lines.append("")
    if manifest:
        lines.append(f"- **Hash base (antes):** `{manifest.get('base_hash_before', 'N/A')[:16]}…`")
        lines.append(f"- **Hash base (después):** `{manifest.get('base_hash_after', 'N/A')[:16]}…`")
    else:
        lines.append("- No hay manifest disponible.")
    lines.append("")

    # Guardar informe
    report_path = run_dir / f"informe-{run_id}.md"
    report_text = "\n".join(lines)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"✓ Informe generado: {report_path}")
    print(f"  {len(patches)} parche(s), {total_words_before} → {total_words_after} palabras")
    return 0


# ══════════════════════════════════════════════════════════════════
#  CLI Principal
# ══════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Construye el parser argparse con todos los subcomandos."""
    parser = argparse.ArgumentParser(
        prog="gobierno_ia",
        description=(
            "CLI de gobierno_ia — Parches versionados para simplificación legislativa.\n\n"
            "Comandos disponibles:\n"
            "  ingest-boe        Lee HTML BOE y genera JSON canónico\n"
            "  validate-proposal Valida un parche contra el canonical\n"
            "  apply-patch       Aplica un parche en un run directory\n"
            "  audit-run         Audita un run\n"
            "  build-report      Genera informe Markdown del run"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # ── ingest-boe ──
    p_ingest = sub.add_parser(
        "ingest-boe",
        help="Lee HTML BOE y genera JSON canónico",
        description=(
            "Parsea un archivo HTML del BOE y genera un JSON canónico.\n"
            "Reutiliza la lógica de scripts/parse_boe_canonical.py.\n"
            "No sobrescribe archivos existentes."
        ),
    )
    p_ingest.add_argument(
        "--source",
        required=True,
        help="Ruta al archivo HTML del BOE",
    )
    p_ingest.add_argument(
        "--output",
        required=True,
        help="Ruta de salida del JSON canónico (p.ej. data/canonical/BOE-A-XXXX/YYYY-MM-DD.json)",
    )
    p_ingest.set_defaults(func=cmd_ingest_boe)

    # ── validate-proposal ──
    p_validate = sub.add_parser(
        "validate-proposal",
        help="Valida un parche contra el canonical",
        description=(
            "Valida la estructura y coherencia de un parche contra el canonical.\n"
            "Exit 0 si es válido, exit 1 si no."
        ),
    )
    p_validate.add_argument(
        "--patch",
        required=True,
        help="Ruta al archivo JSON del parche",
    )
    p_validate.add_argument(
        "--canonical",
        required=True,
        help="Ruta al archivo JSON canónico",
    )
    p_validate.set_defaults(func=cmd_validate_proposal)

    # ── apply-patch ──
    p_apply = sub.add_parser(
        "apply-patch",
        help="Aplica un parche en un run directory",
        description=(
            "Aplica un parche en un directorio de run.\n"
            "NO toca data/raw/ ni data/canonical/.\n"
            "Genera manifest de auditoría."
        ),
    )
    p_apply.add_argument(
        "--patch",
        required=True,
        help="Ruta al archivo JSON del parche",
    )
    p_apply.add_argument(
        "--run-id",
        required=True,
        help="Identificador del run (p.ej. run-2026-09-21-hacienda)",
    )
    p_apply.add_argument(
        "--output-dir",
        default=str(_RUNS_DIR),
        help=f"Directorio donde se crean los runs (default: {_RUNS_DIR})",
    )
    p_apply.set_defaults(func=cmd_apply_patch)

    # ── audit-run ──
    p_audit = sub.add_parser(
        "audit-run",
        help="Audita un run: verifica hashes, estado de parches, pendientes",
        description=(
            "Audita un run verificando hashes, estado de parches,\n"
            "y detectando problemas. Exit 0 si todo OK, exit 1 si hay problemas."
        ),
    )
    p_audit.add_argument(
        "--run-id",
        required=True,
        help="Identificador del run a auditar",
    )
    p_audit.add_argument(
        "--runs-dir",
        default=str(_RUNS_DIR),
        help=f"Directorio base de runs (default: {_RUNS_DIR})",
    )
    p_audit.set_defaults(func=cmd_audit_run)

    # ── build-report ──
    p_report = sub.add_parser(
        "build-report",
        help="Genera un informe Markdown del run con métricas",
        description=(
            "Genera un informe Markdown con métricas del run:\n"
            "- Resumen de operación\n"
            "- Métricas de cambio\n"
            "- Detalle de parches aplicados\n"
            "- Verificación de integridad"
        ),
    )
    p_report.add_argument(
        "--run-id",
        required=True,
        help="Identificador del run",
    )
    p_report.add_argument(
        "--runs-dir",
        default=str(_RUNS_DIR),
        help=f"Directorio base de runs (default: {_RUNS_DIR})",
    )
    p_report.set_defaults(func=cmd_build_report)

    return parser


def main() -> None:
    """Punto de entrada principal del CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        exit_code = args.func(args)
    except Exception as e:
        print(f"✗ Error interno: {e}", file=sys.stderr)
        exit_code = 2

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
