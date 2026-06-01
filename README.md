# ConnectLAW – Juristischer Fach-Chatbot v4.0

Interner juristischer Analyse-Assistent mit Schwerpunkt **Netzbau,
Werkleitungen, Gestattungen, Tiefbau und Schadenregulierung** (Schweizer
Recht). Lauffähige Python-CLI auf Basis des **Anthropic Python SDK**
(Messages API).

> ⚠️ KI-gestützte Erstorientierung. Ersetzt **keine** verbindliche
> Rechtsberatung. `[MOD]`-Aussagen sind zu verifizieren. Bei Risiko →
> Rechtsdienst.

## Funktionen

- **System-Prompt-Laden** – der Fach-Prompt v4.0 (Halluzinationsverbot,
  Eskalationsregeln, Mandatsgrenze, Selbstcheck) liegt in
  `prompts/system_prompt.md`.
- **Wissensquellen `[DOK]`** – Textdokumente in `knowledge/` werden in
  den gecachten Kontext geladen und haben Vorrang vor `[WEB]`/`[MOD]`.
- **Live-Websuche `[WEB]`** – server-seitiger `web_search`-Tool, technisch
  **auf Schweizer Domains beschränkt** (admin.ch, fedlex, bger.ch,
  lexfind.ch, swisslex.ch, SIA, KBOB, VSS …). Verhindert DE/AT/EU-Quellen.
- **Prompt-Caching** – System-Prompt + `[DOK]` als stabiles, gecachtes
  Präfix → günstige, schnelle Folgeanfragen.
- **Multi-Turn-CLI** – interaktiver Verlauf mit `/reset`, `/help`, `/exit`.
- **Adaptives Thinking** + Aufwandssteuerung (`effort`).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # dann ANTHROPIC_API_KEY eintragen
```

## Start

```bash
python main.py
```

Beispielsitzung:

```
Frage› Wir haben bei Tiefbauarbeiten eine fremde Werkleitung beschädigt.
       Wer trägt die Kosten?
ConnectLAW› [Analyse nach Schema Sachverhalt → Norm/Prinzip → ...]
```

## Konfiguration (Umgebungsvariablen / `.env`)

| Variable | Standard | Bedeutung |
|---|---|---|
| `ANTHROPIC_API_KEY` | – | **Pflicht.** API-Schlüssel. |
| `CONNECTLAW_MODEL` | `claude-opus-4-8` | Verwendetes Modell. |
| `CONNECTLAW_EFFORT` | `high` | Denk-/Aufwandsstufe: `low`/`medium`/`high`/`max`. |
| `CONNECTLAW_MAX_TOKENS` | `16000` | Maximale Antwortlänge. |
| `CONNECTLAW_WEB_SEARCH` | `true` | Live-Websuche aktivieren. |
| `CONNECTLAW_VERBOSE` | `false` | Diagnose (Cache-/Token-Nutzung) anzeigen. |

## Projektstruktur

```
ConnectLAW/
├── main.py                     # Einstiegspunkt
├── prompts/system_prompt.md    # Fach-Prompt v4.0
├── knowledge/                  # [DOK]-Wissensquellen (lokal, nicht versioniert)
└── connectlaw/
    ├── config.py               # Konfiguration + zugelassene CH-Domains
    ├── knowledge.py            # System-Prompt-/Wissens-Laden
    ├── agent.py                # Messages-API-Loop, Websuche, Caching
    └── cli.py                  # interaktive CLI
```

## Quellenregeln (technisch durchgesetzt)

Die Live-Recherche ist über `allowed_domains` auf Schweizer Quellen
begrenzt (siehe `connectlaw/config.py` → `SWISS_SEARCH_DOMAINS`). Das
unterstützt die Prompt-Regel, deutsche/österreichische/EU-Quellen nicht
als Primärquelle zu verwenden. Liste bei Bedarf erweitern.

## Erweiterungen

- **PDF-Wissensquellen** – per Files API hochladen und als
  `document`-Block mit `citations` einbinden (für belegte Zitate).
- **HTTP-Endpoint** – `LegalAgent` lässt sich hinter FastAPI als
  `/chat`-Endpoint betreiben.
- **Eskalations-Hooks** – `LegalAgent.ask()` liefert die finale Message
  zurück; Antworttext kann auf `⚠ Risikohinweis` geprüft und an ein
  Ticketsystem weitergereicht werden.

## Hinweise zur Verlässlichkeit

Der System-Prompt verbietet das Erfinden von SR-/Artikel-/BGE-Nummern,
URLs und Daten. Die App erzwingt CH-Quellen bei der Websuche, kann
jedoch inhaltliche Korrektheit nicht garantieren – kritische Aussagen
sind durch den Rechtsdienst zu verifizieren.
