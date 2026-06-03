# Lösung im Rahmen von CRISP-ML(Q)

**Phasen 2–6 + Reflexion**
Klassifikation: INTERN · Stand 2026-06 · baut auf Phase 1 auf
(`01_business_data_understanding.md`).

> **Kern der Lösung:** Der «jedes Mal andere Ablauf» wird in ein **stabiles
> Feldschema + eine geprüfte Vorlage** überführt. Das Befüllen übernimmt ein
> **Agent** (geführte Erfassung → Validierung → Entwurf). Visualisiert wird
> das Ganze in einer **interaktiven Browser-Demo**.

---

## 1. Lösung formulieren (CRISP-ML(Q) Phasen 2–6)

### Phase 2 — Data Engineering ✅
Aus dem «jedes Mal anderen» Freitext wird strukturierte Datenhaltung:

| Artefakt | Datei | Zweck |
|---|---|---|
| Feldschema | `schema/entschaedigungsvertrag.yaml` | 16 Pflichtfelder in 4 Gruppen, Typen, Datenschutz-Stufe, Eskalationsschwelle |
| Mustervorlage | `vorlagen/entschaedigungsvertrag_muster.md` | geprüfter Vertragstext mit `{{platzhalter}}` |
| Beispieldaten | in Phase 1 + Demo (fiktiv, anonymisiert) | Test & Veranschaulichung |

Konsistenz technisch gesichert: **alle 16 Platzhalter der Vorlage entsprechen
exakt einem Schema-Key** (automatisch geprüft).

### Phase 3 — Modellierung / Prompt-Engineering ✅
Statt eines klassischen ML-Modells ist das «Modell» hier ein **LLM-Agent mit
Workflow-Prompt** (`prompts/vertrag_prompt.md`), der den Fach-Prompt v4.0
erweitert:

1. **Erfassung** der Felder gruppenweise (a→d), keine Doppelfragen.
2. **Kein Erfinden** von Personen-/Parzellen-/Tarif-/Normdaten.
3. **Validierung** (Quality-Gates): Pflichtfelder vollständig? Betrag ≥
   CHF 100'000 → Eskalation? Mehrsprachiger Kanton?
4. **Generierung** des befüllten Entwurfs; offene Pflichtfelder bleiben
   sichtbar.
5. **Abschluss** mit Disclaimer.

Integration: CLI-Befehl **`/vertrag`** (`connectlaw/cli.py`) startet den
geführten Ablauf über den bestehenden `LegalAgent`.

### Phase 4 — Evaluation
Geprüft wird gegen die Erfolgskriterien aus Phase 1:

| KPI | Messung | Ergebnis dieser Lösung |
|---|---|---|
| KPI-2 Vollständigkeit | offene `{{…}}` zählen | Validierungsschritt erzwingt 100 % vor «fertig» |
| KPI-3 Halluzination | Norm-/Grundbuch-/Tarifangaben | Prompt verbietet Erfindung; Vorlage markiert «zu verifizieren» |
| KPI-4 Eskalation | Betrag ≥ 100k erkannt | Agent **und** Demo zeigen Warnung |
| KPI-1 Zeit | Erfassung statt Freitext | Sammelfragen + Vorlage → deutlich schneller |
| KPI-5 Datenschutz | Realdaten im Repo/Logs | nur Platzhalter/Beispiele versioniert; Demo rein client-seitig |

Konsistenz Schema↔Vorlage↔Demo ist automatisiert verifiziert (Platzhalter-
Abgleich, JS-Syntax-Check).

### Phase 5 — Deployment ✅
- **CLI:** `/vertrag` sofort nutzbar (siehe `cli.py`).
- **Web (Bonus):** `docs/vertrag-demo.html` — interaktiver Generator, von der
  Startseite verlinkt, läuft ohne Backend/API-Key vollständig im Browser.
- **Backend-Option:** dieselbe Vorlage als `[DOK]` in `knowledge/` ablegen,
  dann nutzt auch der Chat-Endpoint sie (vorlage ist bewusst nicht in
  `knowledge/`, da dieser Ordner vertraulich/gitignored ist).

### Phase 6 — Monitoring & Maintenance
- Vorlage & Schema versioniert → Änderungen nachvollziehbar (Git).
- Eskalations- und Disclaimer-Regeln zentral im Prompt → einmal pflegen.
- Erweiterbar: weitere Vertragstypen = neues Schema + neue Vorlage, gleicher
  Mechanismus.

---

## 2. Lösung mittels Agent — wo sinnvoll? (Punkt 3)

**Sinnvoll (Agent):** Die *Erfassung im Dialog* und das *kontextsensible
Befüllen* (Rückfragen, Sprache des Nutzers, Eskalationslogik, Umgang mit
Sonderfällen wie Erbengemeinschaft) — das ist genau die Stärke eines LLM-
Agenten und löst Schmerzpunkt B («Ablauf jedes Mal anders»).

**Bewusst NICHT dem Agenten überlassen (deterministisch):**
- Platzhalter-Ersetzung in der Demo (reine String-Substitution → kein LLM,
  kein Halluzinationsrisiko, datenschutzfreundlich offline).
- Pflichtfeld-/Eskalations-Prüfung als feste Regel (≥ CHF 100'000).
- Tarife/Normnummern/Grundbuchdaten → niemals generieren, nur erfragen/[WEB].

Das ist die **Hybrid-Architektur**: Agent für Dialog/Urteil, deterministische
Logik für Fakten und Vorlagentreue. Sie passt zur strengen Anti-Halluzinations-
Linie des Projekts.

### Ist es genug detailliert? Macht es Sinn?
- **Detailtiefe:** Für einen lauffähigen Prototyp ja — Schema (16 Felder),
  Vorlage, Agenten-Workflow und Demo greifen konsistent ineinander.
- **Offene Punkte (ehrlich):** der Vertragstext ist ein **Muster**, das vom
  Rechtsdienst juristisch finalisiert werden muss (ZGB-Artikel,
  kantonale Tarife, Beurkundung/Grundbuch sind bewusst als «zu verifizieren»
  markiert, nicht erfunden). Ein DOCX/PDF-Export und Mehrsprachigkeit (FR/IT)
  wären sinnvolle nächste Ausbaustufen.
- **Sinnhaftigkeit:** Ja — die Lösung trifft alle drei Schmerzpunkte
  (A Personendaten/Parzelle → strukturierte Felder; B Ablauf → standardisiert;
  C Recht → geprüfte Vorlage + Eskalation + Disclaimer).

---

## 3. Verstehe ich, was gemeint ist? (Punkt 4)

**Problem (in eigenen Worten):** Beim Werkleitungsbau müssen wiederholt
Entschädigungs-/Dienstbarkeitsverträge mit Grundeigentümern erstellt werden.
Jeder Vertrag enthält andere **Personendaten** (Eigentümer) und
**Parzellendaten**, und es gibt **keinen einheitlichen Ablauf** — das kostet
Zeit, ist fehleranfällig und datenschutzkritisch.

**Was gewünscht ist:** das Problem **im Rahmen von CRISP-ML(Q)** lösen, die
Lösung **interaktiv visualisieren** (Bonus) und **wo sinnvoll einen Agenten**
einsetzen — mit der Selbstprüfung, ob es detailliert genug ist und Sinn ergibt.

**Bestätigung des Verständnisses → umgesetzt:**

| Anforderung | Umsetzung |
|---|---|
| 1 · Lösung im Rahmen CRISP-ML | Phasen 1–6 dokumentiert + Artefakte (Schema, Vorlage, Prompt, CLI) |
| 2 · Interaktiv visualisieren (Bonus) | `docs/vertrag-demo.html` (Browser-Demo, live Vorschau, Fortschritt, Eskalations-Warnung) |
| 3 · Mittels Agent lösen, wo sinnvoll | `/vertrag`-Modus + Hybrid-Architektur, mit Begründung was *nicht* an den Agenten geht |
| 4 · Verständnis prüfen | dieser Abschnitt (Problem-Restatement + Mapping) |

Falls eine Annahme nicht passt (z. B. anderer Vertragstyp, anderes
Ausgabeformat, Backend statt Browser), bitte kurz Bescheid — das Schema-/
Vorlage-/Agenten-Muster ist generisch wiederverwendbar.
