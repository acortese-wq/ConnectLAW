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
| 2 · Data Engineering | `schema/entschaedigungsvertrag.yaml` + `vorlagen/…_muster.md` | ✅ siehe `02_loesung_crisp_ml.md` |
| 3 · Modellierung / Prompt-Engineering | `prompts/vertrag_prompt.md` + CLI-Befehl `/vertrag` | ✅ |
| 4 · Evaluation | Quality-Gates (KPI-1…5), Konsistenz Schema↔Vorlage↔Demo | ✅ |
| 5 · Deployment | CLI `/vertrag` + interaktive Web-Demo `docs/vertrag-demo.html` | ✅ |
| 6 · Monitoring & Maintenance | versionierte Vorlage/Schema, zentrale Eskalations-/Disclaimer-Regeln | ✅ Grundlage gelegt |

## Lösung & Artefakte

| Artefakt | Datei |
|---|---|
| Lösung CRISP-ML(Q) Phasen 2–6 + Reflexion | `02_loesung_crisp_ml.md` |
| Feldschema (16 Felder, 4 Gruppen) | `../../schema/entschaedigungsvertrag.yaml` |
| Mustervertrag mit Platzhaltern | `../../vorlagen/entschaedigungsvertrag_muster.md` |
| Agenten-Workflow (Vertrags-Modus) | `../../prompts/vertrag_prompt.md` |
| CLI-Befehl `/vertrag` | `../../connectlaw/cli.py` |
| **Interaktive Visualisierung (Bonus)** | `../../docs/vertrag-demo.html` |
