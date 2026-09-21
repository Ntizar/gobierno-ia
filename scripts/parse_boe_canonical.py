#!/usr/bin/env python3
"""
parse_boe_canonical.py — Parser canónico de BOE HTML → JSON canónico.

Lee HTML de data/raw/boe/<boe-id>/<fecha>/source.html
Genera data/canonical/<boe-id>/<fecha>.json

Uso:
  python scripts/parse_boe_canonical.py                    # parsea las 3 leyes
  python scripts/parse_boe_canonical.py BOE-A-2003-23186  # solo una
"""

import json
import hashlib
import re
import sys
import os
from pathlib import Path
from html.parser import HTMLParser

# ── Configuración ──────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent  # raíz del proyecto
RAW_DIR = BASE / "data" / "raw" / "boe"
CANON_DIR = BASE / "data" / "canonical"

BOES = [
    "BOE-A-2003-23186",
    "BOE-A-1986-10499",
    "BOE-A-2021-8447",
]

FECHA_CONSULTA = "2026-08-31"


# ── Parser HTML ligero (sin dependencias externas) ─────────────
class SimpleHTMLTag:
    """Representa una etiqueta HTML parseada."""
    def __init__(self, tag, attrs, text="", children=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.text = text
        self.children = children or []

    def get(self, key, default=None):
        return self.attrs.get(key, default)


class BOEHTMLParser(HTMLParser):
    """Parser HTML que extrae div.bloque con h5.articulo y p.parrafo."""

    def __init__(self):
        super().__init__()
        self.articles = []
        self._in_block = False
        self._block_id = None
        self._block_depth = 0
        self._in_h5 = False
        self._in_p = False
        self._in_a = False
        self._current_title = ""
        self._current_text_parts = []
        self._current_links = []
        self._current_link_href = ""
        self._current_link_text = ""
        self._para_texts = []
        self._para_links = []
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")

        # Detectar inicio de bloque de artículo
        if tag == "div" and "bloque" in cls.split():
            self._in_block = True
            self._block_id = attrs_dict.get("id", "")
            self._block_depth = 1
            self._current_title = ""
            self._para_texts = []
            self._para_links = []
            return

        if self._in_block:
            if tag == "div":
                self._block_depth += 1

            # Detectar h5.articulo
            if tag == "h5" and "articulo" in cls.split():
                self._in_h5 = True
                self._current_title = ""
                return

            # Detectar p.parrafo
            if tag == "p" and "parrafo" in cls.split():
                self._in_p = True
                self._current_text_parts = []
                self._current_links = []
                return

            # Detectar enlaces dentro de parrafo
            if tag == "a" and self._in_p:
                self._in_a = True
                self._current_link_href = attrs_dict.get("href", "")
                self._current_link_text = ""
                return

    def handle_endtag(self, tag):
        if self._in_block:
            if tag == "h5" and self._in_h5:
                self._in_h5 = False
                return

            if tag == "p" and self._in_p:
                self._in_p = False
                text = " ".join("".join(self._current_text_parts).split())
                if text:
                    self._para_texts.append(text)
                    self._para_links.extend(self._current_links)
                self._current_links = []
                return

            if tag == "a" and self._in_a:
                self._in_a = False
                if self._current_link_href:
                    self._current_links.append({
                        "href": self._current_link_href,
                        "text": self._current_link_text.strip()
                    })
                return

            if tag == "div":
                self._block_depth -= 1
                if self._block_depth <= 0:
                    self._in_block = False
                    # Guardar artículo si tiene título de tipo Artículo
                    title = self._current_title.strip()
                    if title.startswith("Artículo"):
                        self.articles.append({
                            "id": self._block_id,
                            "titulo": title,
                            "parrafos": self._para_texts,
                            "remisiones_raw": self._para_links,
                        })
                    self._block_id = None

    def handle_data(self, data):
        if self._in_block:
            if self._in_h5:
                self._current_title += data
            elif self._in_p:
                self._current_text_parts.append(data)
            elif self._in_a:
                self._current_link_text += data


# ── Funciones auxiliares ──────────────────────────────────────

def sha256_file(path: Path) -> str:
    """Calcula SHA-256 de un fichero."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_title(html_path: Path) -> str:
    """Extrae el título de la ley del tag <title> del HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"<title>(.*?)</title>", line)
            if m:
                raw = m.group(1).strip()
                # Quitar el BOE ID del principio
                raw = re.sub(r"^BOE-A-\d{4}-\d+\s*", "", raw)
                return raw
    return "Desconocido"


def extract_enumeraciones(texto: str) -> list:
    """Extrae enumeraciones (items numerados) del texto de un artículo."""
    enums = []
    # Patrón: inicio de línea o después de punto con número + punto
    # "1. ", "2. ", "a) ", "b) ", etc.
    patron = re.compile(
        r"(?:^|\n)\s*(\d+\.\s+.+?)(?=(?:\n\s*\d+\.|\n\s*[a-z]\)|\Z))",
        re.DOTALL
    )
    # Más simple: buscar líneas que empiecen con N.
    lines = texto.split("\n")
    current_enum = []
    for line in lines:
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


def extract_remisiones(links: list) -> list:
    """Extrae remisiones (referencias cruzadas a otras leyes) de los enlaces."""
    remisiones = []
    for link in links:
        href = link.get("href", "")
        # Buscar referencias a otros BOEs
        m = re.search(r"id=(BOE-[A-Z]-\d{4}-\d+)", href)
        if m:
            remisiones.append({
                "boe_ref": m.group(1),
                "texto": link.get("text", "")
            })
    return remisiones


def count_words(texto: str) -> int:
    """Cuenta palabras en un texto."""
    return len(texto.split())


def parse_boe(boe_id: str):
    """Parsea un BOE y genera el JSON canónico."""
    raw_path = RAW_DIR / boe_id / FECHA_CONSULTA / "source.html"
    meta_path = RAW_DIR / boe_id / "metadata.json"
    out_dir = CANON_DIR / boe_id
    out_path = out_dir / f"{FECHA_CONSULTA}.json"

    if not raw_path.exists():
        print(f"  ✗ No existe: {raw_path}")
        return False

    # Leer metadata
    metadata = {}
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    sha = sha256_file(raw_path)
    titulo_ley = extract_title(raw_path)

    # Parsear HTML
    with open(raw_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = BOEHTMLParser()
    parser.feed(html_content)

    # Construir artículos canónicos
    articulos = []
    total_palabras = 0

    for art in parser.articles:
        # Unir todos los párrafos en texto plano
        texto_plano = " ".join(art["parrafos"])
        # Limpiar espacios múltiples
        texto_plano = re.sub(r"\s+", " ", texto_plano).strip()

        enumeraciones = extract_enumeraciones(texto_plano)
        remisiones = extract_remisiones(art["remisiones_raw"])
        palabras = count_words(texto_plano)
        total_palabras += palabras

        articulos.append({
            "id": art["id"],
            "titulo": art["titulo"],
            "texto": texto_plano,
            "enumeraciones": enumeraciones,
            "remisiones": remisiones,
            "palabras": palabras,
        })

    # Construir JSON canónico
    canonical = {
        "schema_version": "1.0",
        "boe_id": boe_id,
        "titulo_ley": titulo_ley,
        "fecha_consulta": FECHA_CONSULTA,
        "source_sha256": sha,
        "articulos": articulos,
        "total_articulos": len(articulos),
        "total_palabras": total_palabras,
    }

    # Guardar
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(canonical, f, ensure_ascii=False, indent=2)

    print(f"  ✓ {boe_id}: {len(articulos)} artículos, {total_palabras} palabras → {out_path}")
    return True


def main():
    boes_to_parse = BOES
    if len(sys.argv) > 1:
        boes_to_parse = [arg for arg in sys.argv[1:] if arg.startswith("BOE-")]

    print(f"Parseando {len(boes_to_parse)} leyes BOE...\n")
    for boe_id in boes_to_parse:
        parse_boe(boe_id)
    print("\nHecho.")


if __name__ == "__main__":
    main()
