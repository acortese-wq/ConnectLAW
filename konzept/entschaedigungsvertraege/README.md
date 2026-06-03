# Konzept: Entschädigungsverträge beim Leitungsbau (CRISP-ML(Q))

Strukturierte Aufbereitung des Anwendungsfalls „Entschädigungsverträge für
den Werkleitungsbau generieren" nach dem Vorgehensmodell **CRISP-ML(Q)**.

Ziel: wiederkehrende Verträge mit variablen Personen-/Parzellendaten
**schneller, einheitlicher und rechtssicher** erstellen — DSG-konform und
ohne erfundene Fakten (vgl. `prompts/system_prompt.md`, Ziff. 3).

## Phasen-Fahrplan

| Phase | Inhalt | Status |
|---|---|---|
| 1 · Business & Data Understanding | Ziele, Stakeholder, Erfolgskriterien, Feldschema, Datenschutz | ✅ `01_business_data_understanding.md` |
| 2 · Data Engineering | Feldschema formalisieren, Mustervorlage + Platzhalter, Validierung, Beispieldaten | ⏳ offen |
| 3 · Modellierung / Prompt-Engineering | Vertrags-Workflow im System-Prompt / `/vertrag`-Modus | ⏳ offen |
| 4 · Evaluation | Tests gegen Beispieldatensätze, Qualitäts-Gates (KPI-1…5) | ⏳ offen |
| 5 · Deployment | Integration in CLI und/oder Web-Backend, Ausgabeformat | ⏳ offen |
| 6 · Monitoring & Maintenance | Qualität/Eskalationen überwachen, Vorlagen pflegen | ⏳ offen |

> Weitere Aufgaben (Phase 2 ff.) folgen schrittweise.
