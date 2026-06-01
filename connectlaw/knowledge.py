"""Laden von System-Prompt und [DOK]-Wissensquellen.

Textbasierte Wissensdokumente (.md/.txt) werden in den (gecachten)
System-Kontext eingebettet und erhalten damit gemäss System-Prompt
Ziff. 2 Vorrang ([DOK] vor [WEB] vor [MOD]).
"""

from __future__ import annotations

from pathlib import Path

# Als Wissensquelle eingelesene Dateiendungen.
TEXT_EXTENSIONS = {".md", ".txt", ".markdown", ".rst"}


def load_system_prompt(path: Path) -> str:
    """Liest den System-Prompt aus der Datei."""
    if not path.is_file():
        raise FileNotFoundError(
            f"System-Prompt nicht gefunden: {path}. "
            "Erwartet wird prompts/system_prompt.md."
        )
    return path.read_text(encoding="utf-8").strip()


def load_knowledge(knowledge_dir: Path) -> tuple[str, list[str]]:
    """Lädt alle textbasierten Wissensdokumente aus dem Verzeichnis.

    Rückgabe: (zusammengesetzter Kontext-Text, Liste der Dateinamen).
    Gibt ("", []) zurück, wenn keine Dokumente vorhanden sind.
    """
    if not knowledge_dir.is_dir():
        return "", []

    files = sorted(
        p
        for p in knowledge_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() in TEXT_EXTENSIONS
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
        try:
            content = f.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            # Nicht-UTF-8-Dateien überspringen statt zu raten.
            continue
        if not content:
            continue
        sections.append(f"\n----- [DOK] BEGINN: {f.name} -----\n")
        sections.append(content)
        sections.append(f"\n----- [DOK] ENDE: {f.name} -----\n")
        loaded.append(f.name)

    if not loaded:
        return "", []

    return "\n".join(sections), loaded
