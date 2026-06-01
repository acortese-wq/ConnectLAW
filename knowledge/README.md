# Wissensquellen ([DOK])

In diesem Ordner abgelegte Textdateien (`.md`, `.txt`) werden beim Start
als **[DOK]** in den gecachten System-Kontext geladen und haben gemäss
System-Prompt Vorrang vor Live-Recherche `[WEB]` und Modellwissen `[MOD]`.

## Hinweise

- Nur **textbasierte** Dateien werden automatisch eingelesen
  (`.md`, `.txt`, `.markdown`, `.rst`). `README.md` wird ignoriert.
- Inhalte sind **vertraulich** und werden **nicht** ins Git-Repository
  übernommen (siehe `.gitignore`). Ablage erfolgt lokal.
- Für PDF-Dokumente: Text extrahieren und als `.txt`/`.md` ablegen, oder
  die App um die Files API erweitern (siehe README → Erweiterungen).

## Beispiel

```
knowledge/
  gestattungsvertrag-musterklauseln.md
  interne-claims-richtlinie.txt
```
