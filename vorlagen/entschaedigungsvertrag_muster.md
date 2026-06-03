# Mustervertrag — Entschädigung / Dienstbarkeit Leitungsbau

> **VORLAGE / ENTWURF · INTERN.** KI-gestützte Erstorientierung, **keine**
> verbindliche Rechtsberatung. Normverweise, Tarife und Grundbuchangaben
> sind durch den **Rechtsdienst zu verifizieren**. Beurkundung/
> Grundbuchanmeldung erfolgen separat. Schweizer Hochdeutsch («ss»).
>
> Platzhalter `{{…}}` werden aus dem Feldschema
> (`schema/entschaedigungsvertrag.yaml`) befüllt. Offene Pflichtfelder
> bleiben als `{{…}}` sichtbar und sind vor Unterzeichnung zu ergänzen.

---

## Dienstbarkeits- und Entschädigungsvertrag

**zwischen**

**{{werkeigentuemer.name}}**
— nachfolgend «Werkeigentümerin» —

**und**

**{{grundeigentuemer.name}}**, {{grundeigentuemer.adresse}}
Rechtsform: {{grundeigentuemer.rechtsform}}
— nachfolgend «Grundeigentümer:in» —

---

### 1. Vertragsgegenstand

Die Grundeigentümer:in räumt der Werkeigentümerin auf dem nachstehenden
Grundstück das Recht ein, eine **{{leitung.typ}}-Leitung** zu erstellen,
zu betreiben, zu unterhalten und zu erneuern.

| | |
|---|---|
| Grundstück (Parzelle) | {{grundstueck.parzellennummer}} |
| Grundbuchkreis | {{grundstueck.grundbuch}} |
| Politische Gemeinde / Kanton | {{grundstueck.gemeinde}} / {{grundstueck.kanton}} |
| Beanspruchte Fläche | {{grundstueck.flaeche_beanspruchung_m2}} m² |
| Verlauf / Trassee | {{leitung.verlauf_beschrieb}} |
| Art der Beanspruchung | {{leitung.dauerhaft_temporaer}} |

### 2. Dienstbarkeit

Als Rechtsgrundlage wird eine **{{dienstbarkeit.art}}** vereinbart.
Grundbucheintrag der Dienstbarkeit: **{{entschaedigung.eintrag_grundbuch}}**.

*[Rechtsnatur und einschlägige Bestimmungen des ZGB über Dienstbarkeiten
durch den Rechtsdienst zu verifizieren — keine Artikelnummer aus
Modellwissen einsetzen.]*

### 3. Entschädigung

Die Werkeigentümerin entrichtet der Grundeigentümer:in eine Entschädigung
von **CHF {{entschaedigung.betrag_chf}}**.

- Grundlage: {{entschaedigung.grundlage}}
- Zahlungsmodalität: {{entschaedigung.zahlungsmodalitaet}}

Die Zahlung erfolgt **ohne Anerkennung einer Rechtspflicht**, soweit nicht
ausdrücklich anders vereinbart.

### 4. Rechte und Pflichten der Werkeigentümerin

Die Werkeigentümerin führt die Arbeiten fachgerecht aus, stellt den
ursprünglichen Zustand nach Bauabschluss wieder her und haftet für
Schäden aus dem Bau und Betrieb der Leitung nach den anwendbaren
Bestimmungen *[durch Rechtsdienst zu konkretisieren]*.

### 5. Pflichten der Grundeigentümer:in

Im Bereich des Schutzstreifens unterlässt die Grundeigentümer:in
Handlungen, die die Leitung gefährden (insb. Tiefbau, Anpflanzungen,
Überbauung), und gewährt der Werkeigentümerin Zutritt für Unterhalt und
Reparatur.

### 6. Dauer

Die Dienstbarkeit wird **{{leitung.dauerhaft_temporaer}}** eingeräumt.
Bei temporärer Beanspruchung endet das Recht mit Abschluss der Bauarbeiten
und Wiederherstellung des Zustands.

### 7. Schlussbestimmungen

Änderungen bedürfen der Schriftform. Gerichtsstand und anwendbares Recht
richten sich nach den am Ort des Grundstücks geltenden Bestimmungen
({{grundstueck.kanton}}). Bei mehrsprachigen Kantonen gilt die
rechtsverbindliche Originalsprache.

---

**Ort / Datum:** ____________________

| Werkeigentümerin | Grundeigentümer:in |
|---|---|
| {{werkeigentuemer.name}} | {{grundeigentuemer.name}} |
| ____________________ | ____________________ |

---

> ⚠ **Risikohinweis prüfen:** Bei Streitwert/Entschädigung ≥ CHF 100'000,
> drohender Verjährung/Verfügung, Personenschäden oder strittiger
> Vertragslage **Rechtsdienst beiziehen** (System-Prompt Ziff. 7).
>
> *KI-gestützte Erstorientierung, ersetzt keine verbindliche
> Rechtsberatung. [MOD]-Aussagen sind zu verifizieren.*
