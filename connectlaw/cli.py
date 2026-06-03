"""Interaktive CLI für ConnectLAW."""

from __future__ import annotations

import sys

from . import __version__
from .agent import LegalAgent
from .config import (
    Config,
    KNOWLEDGE_DIR,
    SWISS_SEARCH_DOMAINS,
    SYSTEM_PROMPT_PATH,
    VERTRAG_PROMPT_PATH,
    VORLAGE_PATH,
)
from .knowledge import load_knowledge, load_system_prompt

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║   ConnectLAW · Juristischer Fach-Chatbot v{version:<8}             ║
║   Netzbau · Werkleitungen · Gestattungen · Tiefbau · Claims    ║
║   INTERN – KI-gestützte Erstorientierung, keine Rechtsberatung ║
╚══════════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
Befehle:
  /help     diese Hilfe anzeigen
  /vertrag  geführter Entwurf eines Entschädigungs-/Dienstbarkeitsvertrags
  /reset    Gesprächsverlauf löschen (System-Prompt & [DOK] bleiben)
  /exit     beenden  (auch: /quit, Strg+D)

Eingabe einer Frage = juristische Analyse. Mehrzeilig: einfach tippen
und mit Enter senden. Antwortsprache folgt der Frage (DE/FR/IT/EN/RM).
"""


def _build_vertrag_kickoff() -> str | None:
    """Lädt Vertrags-Workflow-Prompt + Mustervorlage als Kickoff-Nachricht.

    Gibt None zurück, wenn eine der Dateien fehlt. Die Nachricht startet im
    Agenten den geführten Erfassungs-/Generierungs-Ablauf (CRISP-ML(Q)-Lösung).
    """
    if not VERTRAG_PROMPT_PATH.is_file() or not VORLAGE_PATH.is_file():
        return None
    workflow = VERTRAG_PROMPT_PATH.read_text(encoding="utf-8").strip()
    vorlage = VORLAGE_PATH.read_text(encoding="utf-8").strip()
    return (
        f"{workflow}\n\n{vorlage}\n\n"
        "══════════════════════════════════════\n"
        "Starte jetzt mit Schritt 1 (Erfassung), Gruppe (a) Parteien. "
        "Stelle nur die kompakte Sammelfrage für diese Gruppe."
    )


def _print_text(text: str) -> None:
    print(text, end="", flush=True)


def _print_usage(message) -> None:
    u = getattr(message, "usage", None)
    if not u:
        return
    print(
        "  [usage] input={inp} cache_read={cr} cache_creation={cc} output={out}".format(
            inp=getattr(u, "input_tokens", "?"),
            cr=getattr(u, "cache_read_input_tokens", "?"),
            cc=getattr(u, "cache_creation_input_tokens", "?"),
            out=getattr(u, "output_tokens", "?"),
        )
    )


def run() -> int:
    config = Config()
    try:
        config.validate()
    except RuntimeError as exc:
        print(f"Konfigurationsfehler: {exc}", file=sys.stderr)
        return 2

    system_prompt = load_system_prompt(SYSTEM_PROMPT_PATH)
    knowledge_text, knowledge_files = load_knowledge(KNOWLEDGE_DIR)

    agent = LegalAgent(config, system_prompt, knowledge_text)

    print(BANNER.format(version=__version__))
    print(f"Modell: {config.model}   Aufwand: {config.effort}")
    if config.web_search:
        print(f"Live-Websuche: aktiv (nur CH-Domains, {len(SWISS_SEARCH_DOMAINS)} zugelassen)")
    else:
        print("Live-Websuche: deaktiviert ([WEB]-Recherche nicht verfügbar)")
    if knowledge_files:
        print(f"Wissensquellen [DOK]: {', '.join(knowledge_files)}")
    else:
        print("Wissensquellen [DOK]: keine (Dokumente in knowledge/ ablegen)")
    print(HELP_TEXT)

    while True:
        try:
            user_input = input("\n\033[1mFrage›\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAuf Wiedersehen.")
            return 0

        if not user_input:
            continue

        command = user_input.lower()
        if command in ("/exit", "/quit"):
            print("Auf Wiedersehen.")
            return 0
        if command == "/help":
            print(HELP_TEXT)
            continue
        if command == "/reset":
            agent.reset()
            print("Verlauf gelöscht.")
            continue
        if command == "/vertrag":
            kickoff = _build_vertrag_kickoff()
            if kickoff is None:
                print(
                    "Vertrags-Modus nicht verfügbar: prompts/vertrag_prompt.md "
                    "oder vorlagen/entschaedigungsvertrag_muster.md fehlt.",
                    file=sys.stderr,
                )
                continue
            agent.reset()
            print(
                "Vertrags-Modus gestartet (Entschädigung/Dienstbarkeit). "
                "Antworte auf die Rückfragen; /reset beendet den Modus.\n"
            )
            print("\033[1mConnectLAW›\033[0m ", end="", flush=True)
            try:
                agent.ask(kickoff, on_text=_print_text)
                print()
            except Exception as exc:  # robuste CLI
                print(f"\n[Fehler im Vertrags-Modus: {exc}]", file=sys.stderr)
            continue

        print("\n\033[1mConnectLAW›\033[0m ", end="", flush=True)
        try:
            message = agent.ask(user_input, on_text=_print_text)
        except KeyboardInterrupt:
            print("\n[abgebrochen]")
            continue
        except Exception as exc:  # robuste CLI – Fehler nicht fatal
            print(f"\n[Fehler bei der Anfrage: {exc}]", file=sys.stderr)
            continue

        print()  # Zeilenumbruch nach gestreamter Antwort
        if config.verbose:
            _print_usage(message)


if __name__ == "__main__":
    raise SystemExit(run())
