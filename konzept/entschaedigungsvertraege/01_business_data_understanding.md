# Entschädigungsverträge beim Leitungsbau — CRISP-ML(Q)

**Phase 1 von 6: Business & Data Understanding**
Klassifikation: INTERN · Stand 2026-06 · Teil des ConnectLAW-Projekts

> Vorgehensmodell: **CRISP-ML(Q)** — Cross-Industry Standard Process for
> Machine Learning with Quality assurance. Die sechs Phasen:
> (1) Business & Data Understanding → (2) Data Engineering →
> (3) Modellierung / Prompt-Engineering → (4) Evaluation →
> (5) Deployment → (6) Monitoring & Maintenance.
> Dieses Dokument deckt **Phase 1** ab. Die Folgephasen werden separat
> aufgesetzt (weitere Aufgaben folgen).

---

## 0. Problemstellung (Ausgangslage)

> «Beim Erstellen von Verträgen für Entschädigungen, die beim Bau einer
> Leitung entstehen. Weil darin Personendaten (Besitzer), Parzellennr.
> etc. enthalten sind und der Ablauf jedes Mal anders ist.»

Heute werden Entschädigungs-/Gestattungsverträge (Dienstbarkeitsverträge)
für den Werkleitungsbau **manuell und wiederholt von Hand** erstellt. Drei
Schmerzpunkte:

| # | Schmerzpunkt | Folge |
|---|---|---|
| A | Variable **Personendaten** (Grundeigentümer:in) und **Parzellendaten** je Vertrag | Fehleranfällige Copy-Paste-Arbeit, Datenschutzrisiko (DSG) |
| B | **Ablauf jedes Mal anders** (keine standardisierte Struktur) | Kein wiederverwendbarer Prozess, Qualität schwankt |
| C | Juristische Korrektheit (CH-Recht, Dienstbarkeit, Grundbuch) muss gewahrt bleiben | Risiko fehlerhafter/unverbindlicher Verträge |

---

## 1. Business Understanding

### 1.1 Geschäftsziel
Wiederkehrende Entschädigungsverträge für den Leitungsbau **schneller,
einheitlicher und rechtssicher** erstellen — bei gleichbleibender oder
besserer juristischer Qualität und **DSG-konformem** Umgang mit
Personendaten.

### 1.2 Anwendungsfall (Scope)
Im Mandat von ConnectLAW (Netzbau · Werkleitungen · Gestattungen · Tiefbau):
Entwurf von **Entschädigungs- und Dienstbarkeitsverträgen**, mit denen ein
Grundeigentümer dem Werkeigentümer die Erstellung/den Betrieb einer Leitung
auf seiner Parzelle gestattet, gegen eine Entschädigung.

**In Scope**
- Strukturierte Erfassung der variablen Vertragsfelder (Parteien, Parzelle,
  Leitung, Entschädigung, Dienstbarkeit).
- Generierung eines **Vertragsentwurfs** aus einer geprüften Vorlage.
- Kennzeichnung offener/zu verifizierender Punkte (kein Halluzinieren von
  SR-/Artikelnummern, Gebühren, Grundbuchdaten — vgl. System-Prompt Ziff. 3).

**Out of Scope (vorerst)**
- Notarielle Beurkundung / Grundbuchanmeldung (rechtsverbindlicher Akt).
- Verbindliche Rechtsberatung; der Entwurf bleibt KI-gestützte
  Erstorientierung und ist durch den Rechtsdienst zu prüfen.
- Automatisierte Entschädigungs-**Berechnung** nach kantonalen Tarifen
  (Gebühren/Ansätze nur per [WEB]/Reglement, nie aus Modellwissen).

### 1.3 Stakeholder
| Rolle | Interesse |
|---|---|
| Projektleitung Netzbau | Schnelle, standardisierte Verträge |
| Claims / Sachbearbeitung | Korrekte Felder, weniger Nacharbeit |
| Rechtsdienst | Rechtssicherheit, Eskalation bei Risiko |
| Datenschutz (DSG) | Schutz der Personendaten der Grundeigentümer |
| Grundeigentümer (extern) | Korrekte, faire Vertragsausgestaltung |

### 1.4 Erfolgskriterien (messbar, Quality-Gates «Q»)
| ID | Kriterium | Zielwert |
|---|---|---|
| KPI-1 | Zeit pro Vertragsentwurf | −50 % ggü. manuell |
| KPI-2 | Vollständigkeit der Pflichtfelder im Entwurf | 100 % (keine leeren Pflichtplatzhalter) |
| KPI-3 | Erfundene Norm-/Grundbuch-/Gebührenangaben | 0 (hartes Halluzinationsverbot) |
| KPI-4 | Korrekt erkannte Eskalationsfälle (z. B. Streitwert ≥ CHF 100k) | 100 % markiert |
| KPI-5 | Personendaten im Repository / in Logs | 0 echte Datensätze |

### 1.5 Risiken & Annahmen
- **Datenschutz (DSG):** Personendaten dürfen **nicht** ins Git-Repository,
  in Trainings-/Cachedaten oder Logs gelangen. → nur Platzhalter/Beispiel-
  daten versioniert; echte Daten bleiben lokal/zur Laufzeit.
- **Halluzination:** Grundbuch-, Parzellen- und Gebührendaten sind faktisch
  und dürfen nie erfunden werden (System-Prompt Ziff. 3 gilt vollumfänglich).
- **Rechtsverbindlichkeit:** Ergebnis ist ein **Entwurf**, kein
  beurkundeter Vertrag. Disclaimer bleibt Pflicht.
- **Mehrsprachigkeit:** Kanton GR/BE/FR/VS — Originalsprache beachten.
- Annahme: Nutzer liefert die Sachdaten; das System erfindet sie nicht.

---

## 2. Data Understanding

### 2.1 Datenobjekte des Vertrags (Feld-Inventar)

Die «jedes Mal anderen» Inhalte lassen sich in ein **stabiles Feldschema**
fassen. Damit wird der bisher uneinheitliche Ablauf (Schmerzpunkt B)
standardisierbar.

#### a) Parteien
| Feld | Typ | Pflicht | Datenschutz | Bemerkung |
|---|---|---|---|---|
| `werkeigentuemer` | Text | ✓ | gering | meist eigene Organisation |
| `grundeigentuemer.name` | Text | ✓ | **hoch (Personendaten)** | natürl./jurist. Person |
| `grundeigentuemer.adresse` | Text | ✓ | **hoch** | |
| `grundeigentuemer.rechtsform` | Enum | ✓ | gering | natürlich / juristisch / Erbengemeinschaft / Miteigentum |
| `vertreter` | Text | – | hoch | Vollmacht/Beistand |

#### b) Grundstück / Parzelle
| Feld | Typ | Pflicht | Datenschutz | Bemerkung |
|---|---|---|---|---|
| `parzellennummer` | Text | ✓ | mittel | Liegenschaft |
| `grundbuch` | Text | ✓ | mittel | Grundbuchkreis |
| `gemeinde` | Text | ✓ | gering | bestimmt anwendbares kant./komm. Recht |
| `kanton` | Enum | ✓ | gering | 1 von 26; steuert Sprache & Recht |
| `egrid` | Text | – | mittel | eidg. Grundstücksidentifikator |
| `flaeche_beanspruchung_m2` | Zahl | ✓ | gering | dauernd/temporär |

#### c) Leitung / Werk
| Feld | Typ | Pflicht | Bemerkung |
|---|---|---|---|
| `leitungstyp` | Enum | ✓ | Strom / Gas / Wasser / Telekom / Fernwärme / Abwasser |
| `spannung_dimension` | Text | – | z. B. Nennweite / kV |
| `verlauf_beschrieb` | Text | ✓ | Trassee, Tiefe, Schutzstreifen |
| `dauerhaft_temporaer` | Enum | ✓ | Dienstbarkeit vs. Baustelleninstallation |

#### d) Dienstbarkeit & Entschädigung
| Feld | Typ | Pflicht | Datenschutz | Bemerkung |
|---|---|---|---|---|
| `dienstbarkeitsart` | Enum | ✓ | gering | Grunddienstbarkeit / Personaldienstbarkeit (Baurecht/Leitungsrecht) |
| `entschaedigung_betrag_chf` | Zahl | ✓ | mittel | Einmal/wiederkehrend; **Berechnung nicht erfinden** |
| `entschaedigung_grundlage` | Text | ✓ | – | Tarif/Reglement/Verhandlung — Quelle nennen |
| `zahlungsmodalitaet` | Text | ✓ | – | «ohne Anerkennung einer Rechtspflicht» prüfen |
| `eintrag_grundbuch` | Bool | ✓ | – | mit/ohne Grundbucheintrag |

### 2.2 Datenquellen
- **Nutzer-Eingabe (zur Laufzeit):** Parteien, Parzelle, Betrag → nie
  versioniert, nie in Logs.
- **[DOK]-Vorlagen:** Mustervertrag mit Platzhaltern (versioniert, ohne
  echte Personendaten).
- **[WEB] (CH-Domains):** kant./komm. Gebühren, Tarife, Reglemente — nur
  belegt, nie aus Modellwissen.

### 2.3 Datenqualität & -schutz (Quality «Q»)
- **Validierung:** Pflichtfelder vollständig? Kanton ↔ Sprache konsistent?
  Betrag plausibel/numerisch? Eskalationsschwelle (≥ CHF 100k) geprüft?
- **Minimierung:** nur die für den Vertrag nötigen Personendaten erheben (DSG).
- **Trennung:** Schema/Vorlagen (versioniert) **vs.** Realdaten (flüchtig).
- **Beispieldaten:** im Repo nur **anonymisierte, klar als fiktiv
  gekennzeichnete** Beispiele zulässig (siehe Phase 2).

### 2.4 Beispiel-Datensatz (fiktiv, anonymisiert)

```yaml
# BEISPIEL — frei erfunden, dient nur der Veranschaulichung des Schemas.
werkeigentuemer: "Energienetz Musterstadt AG"
grundeigentuemer:
  name: "Muster, Hans (fiktiv)"
  adresse: "Beispielweg 1, 7000 Musterhausen"
  rechtsform: "natuerlich"
grundstueck:
  parzellennummer: "1234"
  grundbuch: "Musterhausen"
  gemeinde: "Musterhausen"
  kanton: "GR"
  flaeche_beanspruchung_m2: 45
leitung:
  leitungstyp: "Strom"
  spannung_dimension: "16 kV"
  verlauf_beschrieb: "Erdkabel, Trassee Ost-West, Tiefe ca. 1.2 m"
  dauerhaft_temporaer: "dauerhaft"
dienstbarkeit:
  dienstbarkeitsart: "Grunddienstbarkeit (Leitungsrecht)"
  entschaedigung_betrag_chf: 2500
  entschaedigung_grundlage: "Verhandlung; Tarif zu verifizieren [WEB]"
  zahlungsmodalitaet: "einmalig, ohne Anerkennung einer Rechtspflicht"
  eintrag_grundbuch: true
```

---

## 3. Ergebnis Phase 1 & Übergang Phase 2

**Erkenntnis:** Der «jedes Mal andere Ablauf» (Schmerzpunkt B) ist in
Wahrheit ein **stabiles Feldschema mit variablen Werten**. Damit wird das
Problem von einem Freitext- zu einem **Template-Befüllungs-Problem** —
gut standardisierbar und testbar.

**Empfohlener nächster Schritt (Phase 2 — Data Engineering):**
1. Feldschema formalisieren (`schema/entschaedigungsvertrag.yaml` o. ä.).
2. Mustervertrag-Vorlage mit Platzhaltern als [DOK] anlegen.
3. Validierungsregeln (Pflichtfelder, Plausibilität, Eskalation) definieren.
4. Anonymisierte Beispieldatensätze für die spätere Evaluation (Phase 4).

> Offene Entscheidungen für Folgeaufgaben: Lösungsform (geführter
> `/vertrag`-Modus vs. reine Vorlage vs. Formular), Ausgabeformat
> (Markdown/DOCX/PDF), und ob die Generierung in CLI **und** Web-Backend
> verfügbar sein soll.
