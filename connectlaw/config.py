"""Konfiguration für ConnectLAW.

Werte werden aus Umgebungsvariablen gelesen (optional via .env-Datei).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv ist optional, aber empfohlen
    pass


# Projektpfade
ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.md"

# Zulässige Schweizer Quell-Domains (vgl. System-Prompt Ziff. 4).
# Begrenzt die Live-Websuche technisch auf CH-Quellen und verhindert
# die Verwendung deutscher/österreichischer/EU-Quellen als Primärquelle.
SWISS_SEARCH_DOMAINS: list[str] = [
    # Bund
    "admin.ch",
    "fedlex.admin.ch",
    "bger.ch",
    "bakom.admin.ch",
    # Kantonale Rechtssammlungen
    "lexfind.ch",
    "gr.lexfind.ch",
    "zhlex.zh.ch",
    # Fachorganisationen
    "sia.ch",
    "kbob.admin.ch",
    "vss.ch",
    "asut.ch",
    "suissedigital.ch",
    # Datenbanken
    "swisslex.ch",
    "weblaw.ch",
]


def _get_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "ja", "on")


@dataclass
class Config:
    """Laufzeitkonfiguration des Chatbots."""

    api_key: str | None = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY"))
    model: str = field(default_factory=lambda: os.environ.get("CONNECTLAW_MODEL", "claude-opus-4-8"))
    effort: str = field(default_factory=lambda: os.environ.get("CONNECTLAW_EFFORT", "high"))
    max_tokens: int = field(default_factory=lambda: int(os.environ.get("CONNECTLAW_MAX_TOKENS", "16000")))
    web_search: bool = field(default_factory=lambda: _get_bool("CONNECTLAW_WEB_SEARCH", True))
    verbose: bool = field(default_factory=lambda: _get_bool("CONNECTLAW_VERBOSE", False))

    # Maximale Anzahl Websuchen pro Antwort (Kostenschutz)
    web_search_max_uses: int = 6

    def validate(self) -> None:
        if not self.api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY ist nicht gesetzt. Bitte .env anlegen "
                "(siehe .env.example) oder die Umgebungsvariable setzen."
            )
        if self.effort not in ("low", "medium", "high", "max"):
            raise RuntimeError(
                f"Ungültige Aufwandsstufe '{self.effort}'. Erlaubt: low | medium | high | max."
            )
