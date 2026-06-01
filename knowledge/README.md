# Wissensquellen ([DOK])

In diesem Ordner abgelegte Textdateien (`.md`, `.txt`) werden beim Start
als **[DOK]** in den gecachten System-Kontext geladen und haben gemäss
System-Prompt Vorrang vor Live-Recherche `[WEB]` und Modellwissen `[MOD]`.

## Hinweise

- Eingelesen werden **Text** (`.md`, `.txt`, `.markdown`, `.rst`) und
  **PDF** (`.pdf`). `README.md` wird ignoriert.
- **PDF** benötigt `pypdf` (in `requirements-server.txt` enthalten). Fehlt
  es, werden PDFs übersprungen. Reine **Scan-PDFs ohne Textebene** liefern
  keinen Text – vorab per OCR in durchsuchbares PDF/Text umwandeln.
- Inhalte sind **vertraulich** und werden **nicht** ins Git-Repository
  übernommen (siehe `.gitignore`). Ablage erfolgt lokal beim Backend.
- Nach dem Ablegen/Ändern von Dateien das Backend neu starten **oder**
  `curl -X POST http://localhost:8000/reload` aufrufen.

## Webseite als [DOK] einlesen

Eine öffentliche CH-Rechtsquelle einmalig abrufen und hier ablegen:

```bash
python ingest_url.py "https://www.fedlex.admin.ch/eli/cc/..." --title "OR ..."
curl -X POST http://localhost:8000/reload     # Backend übernimmt die Quelle
```

Speichert Text als `.md` (mit Quell-URL + Abrufdatum im Kopf) bzw. PDFs als
`.pdf`. Lädt nur die eine angegebene URL (kein Crawling). Benötigt
`beautifulsoup4` (in `requirements-server.txt`).

## Beispiel

```
knowledge/
  gestattungsvertrag-musterklauseln.md
  interne-claims-richtlinie.txt
```
