"""Laden von System-Prompt und [DOK]-Wissensquellen.

Textbasierte Wissensdokumente (.md/.txt) sowie PDFs werden in den
(gecachten) System-Kontext eingebettet und erhalten damit gemäss
System-Prompt Ziff. 2 Vorrang ([DOK] vor [WEB] vor [MOD]).

PDF-Text wird über pypdf extrahiert. Ist pypdf nicht installiert,
werden PDFs übersprungen (statt das Laden abzubrechen).
"""

from __future__ import annotations

from pathlib import Path

# Direkt einlesbare Textendungen.
TEXT_EXTENSIONS = {".md", ".txt", ".markdown", ".rst"}
# Über Extraktion einlesbare Endungen.
PDF_EXTENSIONS = {".pdf"}
SUPPORTED_EXTENSIONS = TEXT_EXTENSIONS | PDF_EXTENSIONS


def load_system_prompt(path: Path) -> str:
    """Liest den System-Prompt aus der Datei."""
    if not path.is_file():
        raise FileNotFoundError(
            f"System-Prompt nicht gefunden: {path}. "
            "Erwartet wird prompts/system_prompt.md."
        )
    return path.read_text(encoding="utf-8").strip()


def _extract_pdf_text(path: Path) -> str:
    """Extrahiert den Text eines PDF. Leere Zeichenkette bei Fehlern/fehlendem pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        # pypdf nicht installiert – PDF wird übersprungen.
        return ""
    try:
        reader = PdfReader(str(path))
        parts = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(parts).strip()
    except Exception:
        # Beschädigte/verschlüsselte PDFs nicht fatal behandeln.
        return ""


def _read_document(path: Path) -> str:
    """Liest ein einzelnes Wissensdokument als Text (je nach Endung)."""
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        try:
            return path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            return ""
    if suffix in PDF_EXTENSIONS:
        return _extract_pdf_text(path)
    return ""


def load_knowledge(knowledge_dir: Path) -> tuple[str, list[str]]:
    """Lädt alle Wissensdokumente (Text + PDF) aus dem Verzeichnis.

    Rückgabe: (zusammengesetzter Kontext-Text, Liste der Dateinamen).
    Gibt ("", []) zurück, wenn keine verwertbaren Dokumente vorhanden sind.
    """
    if not knowledge_dir.is_dir():
        return "", []

    files = sorted(
        p
        for p in knowledge_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_EXTENSIONS
        and p.name.lower() != "readme.md"
    )
    if not files:
        return "", []

    sections: list[str] = [
        "══════════════════════════════════════",
        "WISSENSQUELLEN [DOK] – VORRANG VOR [WEB] UND [MOD]",
        "Nachfolgend hochgeladene/konfigurierte Dokumente. Nur diese",
        "Inhalte gelten als [DOK]. Nicht enthaltene Angaben dürfen NICHT",
        "aus Modellwissen ergänzt werden (vgl. System-Prompt Ziff. 3/4).",
        "══════════════════════════════════════",
    ]
    loaded: list[str] = []
    for f in files:
        content = _read_document(f)
        if not content:
            # Leere/nicht extrahierbare Datei (z.B. Scan-PDF ohne Textebene)
            # überspringen, statt Platzhalter zu erfinden.
            continue
        sections.append(f"\n----- [DOK] BEGINN: {f.name} -----\n")
        sections.append(content)
        sections.append(f"\n----- [DOK] ENDE: {f.name} -----\n")
        loaded.append(f.name)

    if not loaded:
        return "", []

    return "\n".join(sections), loaded
