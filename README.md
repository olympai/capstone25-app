# VC Pitch Deck Analyzer

## 🚀 Schnellstart

```bash
./run.sh
```

Eine KI-gestützte Streamlit-Anwendung zur Analyse von Startup Pitch Decks mit Claude AI. Die Anwendung führt umfassende Bewertungen durch, kombiniert Pitch Deck Analyse mit Web-Recherche, Wettbewerber-Screening und Markt-Trends-Analyse, um fundierte Investment-Entscheidungen zu treffen.

## ✨ Features

### Kern-Funktionalität
- **PDF-Upload**: Lade Startup Pitch Decks im PDF-Format hoch
- **KI-gestützte Analyse**: Nutzt Claude AI zur Bewertung über mehrere Dimensionen:
  - Unternehmen & Geschäftsmodell
  - Wettbewerb & Marktposition
  - Finanzen & Metriken
  - Marktgröße & Dynamik
  - Produkt & Technologie
  - Team & Expertise

### Erweiterte Analyse-Features
- **Kriterien-Gewichtung**: Passe die Wichtigkeit einzelner Bewertungskriterien an (niedrig/mittel/hoch)
- **Eigene Kriterien**: Füge spezifische Bewertungskriterien für deine Investment-These hinzu
- **Red Flags**: Definiere K.O.-Kriterien, die automatisch zu einer roten Ampel führen
- **Wettbewerber-Screening**: Automatische Identifikation und Analyse von Wettbewerbern
- **Markt-Trends-Analyse**: Recherche aktueller Marktentwicklungen und Branchentrends
- **Web-Recherche**: Automatische Suche nach fehlenden Informationen mit konfigurierbaren Quellen

### Ausgabe & Kommunikation
- **Ampel-Bewertung**: Visueller grün/gelb/rot-Indikator für schnelle Einschätzung
- **Executive Summary**: Exportiere professionelle PDF-Zusammenfassungen
- **E-Mail-Generierung**: Automatische Erstellung personalisierter Einladungs- oder Absage-E-Mails
- **Interaktiver Chat**: Stelle Fragen zu den Analyse-Ergebnissen mit Web-Suche-Integration
- **Detaillierte Reports**: Umfassende Begründungen für alle Analyse-Schritte mit Quellenangaben

## 📋 Voraussetzungen

- Python 3.9+
- Azure OpenAI Account mit Claude-Zugriff (via Anthropic Foundry)
- Internetverbindung für Web-Recherche-Funktionalität

## ⚙️ Installation & Konfiguration

### 1. Repository klonen
```bash
git clone <repository-url>
cd capstone25-app
```

### 2. Virtual Environment erstellen
```bash
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### 3. Azure API-Konfiguration (WICHTIG!)
Bevor du die Anwendung starten kannst, musst du deine Azure OpenAI API-Zugangsdaten konfigurieren:

1. Öffne die Datei `.env` im Projekt-Root
2. Trage deine Azure-Zugangsdaten ein:

```env
API_KEY=DEIN_AZURE_API_KEY
API_ENDPOINT=https://DEINE_RESOURCE.openai.azure.com/anthropic
```

**So erhältst du die Zugangsdaten:**
- Logge dich in dein [Azure Portal](https://portal.azure.com) ein
- Navigiere zu deiner Azure OpenAI Ressource
- Kopiere den **API Key** unter "Keys and Endpoint"
- Kopiere den **Endpoint** (sollte mit `https://` beginnen und auf `/anthropic` enden)

### 4. Anwendung starten
Nutze das mitgelieferte Start-Script:
```bash
./run.sh
```

Das Script führt automatisch folgende Schritte aus:
- Aktiviert die Virtual Environment
- Installiert alle Dependencies aus `requirements.txt`
- Prüft ob die `.env` Datei vorhanden ist
- Lädt die Umgebungsvariablen
- Startet die Streamlit-Anwendung

Die App öffnet sich automatisch in deinem Browser unter `http://localhost:8501`

## 🎯 Nutzung

### 1. Konfiguration

#### Pitch Deck hochladen
- Lade eine PDF-Datei deines Startup Pitch Decks hoch

#### Kriterien-Gewichtung anpassen
- Passe die Wichtigkeit der Standard-Kriterien an:
  - **Niedrig**: Geringere Gewichtung in der Gesamtbewertung
  - **Mittel**: Standard-Gewichtung (Default)
  - **Hoch**: Höchste Priorität - kritisch für Investment-Entscheidung

#### Eigene Kriterien hinzufügen (Optional)
- Klicke auf "➕ Neues Kriterium hinzufügen"
- Wähle die Gewichtung (niedrig/mittel/hoch)
- Beschreibe das Kriterium (z.B. "Nachhaltigkeit der Lösung", "Social Impact")

#### Red Flags definieren (Optional)
- Definiere K.O.-Kriterien, die automatisch zu einer roten Ampel führen
- Ein Red Flag pro Zeile (z.B. "Keine zahlenden Kunden", "Regulatorische Probleme")

#### Web-Suchquellen konfigurieren (Optional)
- Gib bevorzugte Webseiten für die Recherche an (eine pro Zeile)
- Beispiele: `crunchbase.com`, `techcrunch.com`, `pitchbook.com`, `linkedin.com`

### 2. Analyse durchführen

Klicke auf **"🚀 Analyse starten"**. Die App führt folgende Schritte automatisch aus:

1. **📊 Pitch Deck Analyse**: Detaillierte Bewertung des PDFs anhand gewichteter Kriterien
2. **🔍 Wettbewerber-Screening**: Identifikation und Analyse von Wettbewerbern
3. **🌐 Web-Recherche & Markt-Trends**: Suche nach fehlenden Informationen und aktuellen Markttrends
4. **🚨 Red Flag Check**: Überprüfung der K.O.-Kriterien
5. **📝 Zusammenfassung**: Generierung einer Executive Summary

### 3. Ergebnisse auswerten

#### Ampel-Bewertung
- **🟢 Grün**: Beide Analysen prognostizieren Erfolg
- **🟡 Gelb**: Gemischte Prognosen - weitere Untersuchung empfohlen
- **🔴 Rot**: Negative Prognosen oder Red Flags getroffen

#### Detaillierte Analysen
Erweitere die Accordions für detaillierte Einblicke:
- Pitch Deck Analyse mit Begründung
- K.O.-Kriterien Check (falls Red Flags definiert)
- Wettbewerber-Screening mit Quellen
- Web-Recherche & Markt-Trends mit Quellen

#### PDF-Export
- Klicke auf **"📄 Executive Summary als PDF exportieren"**
- Erhalte eine professionelle PDF-Zusammenfassung mit allen wichtigen Ergebnissen

### 4. E-Mail generieren

- Klicke auf **"📝 E-Mail generieren"**
- Die App erstellt automatisch eine personalisierte E-Mail:
  - **Einladung** bei positiver Bewertung (grün)
  - **Absage** bei negativer/gemischter Bewertung (gelb/rot)
- Öffne die E-Mail direkt in deinem E-Mail-Programm mit einem Klick

### 5. Interaktiver Chat

- Stelle Fragen zu den Analyse-Ergebnissen
- Der Chat hat Zugriff auf:
  - Das ursprüngliche PDF
  - Alle Analyse-Ergebnisse
  - Web-Suche für zusätzliche Recherchen
- Beispiel-Fragen:
  - "Was sind die größten Risiken für dieses Startup?"
  - "Wie sieht die Wettbewerbslandschaft aus?"
  - "Welche Markt-Trends sprechen für/gegen dieses Investment?"


## 📁 Projektstruktur

```
capstone25-app/
├── app.py                      # Hauptanwendung (Streamlit UI)
├── run.sh                      # Start-Script für die Anwendung
├── .env                        # Umgebungsvariablen (API-Konfiguration)
├── requirements.txt            # Python-Dependencies
├── ai_config/
│   ├── config.py              # API-Konfiguration & Bewertungskriterien
│   ├── functions.py           # KI-Funktionen (Analyse, Web-Suche, E-Mails)
│   ├── pdf_export.py          # PDF-Export-Funktionalität
│   └── workflow.py            # Workflow-Orchestrierung
├── tmp/                        # Temporäres Verzeichnis für hochgeladene PDFs
└── README.md                   # Diese Datei
```

## 🔧 Funktionsweise

### 1. Pitch Deck Analyse
Die Anwendung nutzt Claude AI mit einem strukturierten Bewertungsrahmen:
- **Gewichtete Kriterien**: Nutzer-definierte Gewichtung der Standard-Kriterien
- **Eigene Kriterien**: Zusätzliche Investment-spezifische Bewertungsdimensionen
- **Strukturierte Bewertung**: Analyse von Unternehmen, Wettbewerb, Finanzen, Markt, Produkt und Team
- **Identifikation von Lücken**: Erkennung fehlender Informationen für Web-Recherche

### 2. Wettbewerber-Screening
Automatische Wettbewerbsanalyse:
- Identifikation direkter und indirekter Wettbewerber
- Analyse von Marktpositionierung und Differenzierung
- Bewertung der Wettbewerbslandschaft
- Quellenangaben für weitere Recherchen

### 3. Web-Recherche & Markt-Trends
Intelligente Informationsbeschaffung:
- Gezielte Suche nach fehlenden Informationen
- Analyse aktueller Markttrends und Branchenentwicklungen
- Fokus auf konfigurierbare Quellen (Crunchbase, TechCrunch, etc.)
- Sammlung zusätzlicher Kontextinformationen über Markt und Team

### 4. Red Flag Check
Automatische Überprüfung von K.O.-Kriterien:
- Analyse aller Ergebnisse gegen definierte Red Flags
- Automatische Bewertungsanpassung bei getroffenen Red Flags
- Detaillierte Begründung für jedes getriggerte Kriterium

### 5. Zusammenfassung & Bewertung
Intelligente Ergebnis-Aggregation:
- Kombination aller Analyse-Ergebnisse
- Executive Summary mit Gesamtbewertung
- Ampel-System (grün/gelb/rot) basierend auf allen Faktoren
- Detaillierte Begründungen aus allen Quellen

### 6. E-Mail-Generierung
Automatisierte Kommunikation:
- **Einladungs-E-Mails** bei positiver Bewertung (grün)
- **Absage-E-Mails** bei negativer/gemischter Bewertung (gelb/rot)
- Personalisierung basierend auf Analyse-Ergebnissen
- Professioneller Ton mit konstruktivem Feedback

### 7. Interaktive Nachbearbeitung
Chat-Interface mit erweiterten Funktionen:
- Zugriff auf das ursprüngliche PDF
- Zugriff auf alle Analyse-Ergebnisse
- Integrierte Web-Suche für zusätzliche Recherchen
- Kontextbewusste Antworten basierend auf allen verfügbaren Daten

## ⚙️ Konfigurationsoptionen

### Bewertungskriterien
Das Standard-Framework umfasst:
- **Unternehmen** (COMPANY): Standort, Entwicklungsstand, Geschäftsmodell
- **Wettbewerb** (COMPETITION): Marktpositionierung, Differenzierung, Proof Points
- **Finanzen** (FINANCIALS): KPIs, Traction, Bewertung, Cap Table, Investoren
- **Markt** (MARKET): TAM/SAM/SOM, Wachstumsdynamik, Markteintrittsbarrieren
- **Produkt** (PRODUCT): Roadmap, Product-Market-Fit, UX, Profitabilität
- **Team** (TEAM): Bildung, Erfahrung, Skills, Netzwerk, Gründerhistorie

Alle Kriterien können in drei Gewichtungen konfiguriert werden:
- **Niedrig**: Geringere Bedeutung in der Gesamtbewertung
- **Mittel**: Standard-Gewichtung (Default)
- **Hoch**: Kritisch für Investment-Entscheidung

### Eigene Kriterien
Zusätzliche Bewertungsdimensionen können frei definiert werden:
- **Gewichtung**: niedrig/mittel/hoch
- **Beschreibung**: Freitext zur Definition des Kriteriums
- Beispiele: "Nachhaltigkeit", "Social Impact", "Regulatorisches Risiko"

### Red Flags (K.O.-Kriterien)
Definiere Ausschlusskriterien, die automatisch zu einer roten Ampel führen:
- Ein Kriterium pro Zeile
- Beispiele:
  - "Keine zahlenden Kunden trotz 2+ Jahren Marktpräsenz"
  - "Founder hat bereits das Unternehmen verlassen"
  - "Schwerwiegende regulatorische Probleme"
  - "Unrealistische Bewertung (>10x branchenüblich)"

### Web-Suchquellen
Konfigurierbare Quellen für Web-Recherche:
- **Standard-Quellen**: crunchbase.com, techcrunch.com, pitchbook.com, linkedin.com
- **Anpassbar**: Beliebige Domains können hinzugefügt werden
- Eine Quelle pro Zeile

## 🚦 Ampel-Bewertungssystem

Die finale Bewertung basiert auf mehreren Faktoren:

### 🟢 Grün (Empfehlung: Einladen)
- Pitch Deck Analyse prognostiziert Erfolg
- Web-Recherche bestätigt positives Bild
- Keine Red Flags getroffen
- Starke Markt-Trends unterstützen das Geschäftsmodell

### 🟡 Gelb (Empfehlung: Weitere Untersuchung)
- Gemischte Prognosen zwischen Analysen
- Einige Bedenken, aber keine K.O.-Kriterien
- Weitere Due Diligence empfohlen

### 🔴 Rot (Empfehlung: Absagen)
- Beide Analysen prognostizieren Misserfolg ODER
- Mindestens ein Red Flag wurde getroffen
- Signifikante Risiken oder fehlende Grundvoraussetzungen

**Wichtig**: Ein einzelner getroffener Red Flag setzt die Bewertung automatisch auf ROT, unabhängig von anderen Faktoren.

## 🐛 Troubleshooting

### "Error analyzing pitch deck"
**Mögliche Ursachen:**
- Azure API Key ist ungültig oder abgelaufen
- PDF ist beschädigt oder nicht lesbar
- API Endpoint ist falsch konfiguriert

**Lösungen:**
1. Überprüfe `.env` Datei auf korrekte Zugangsdaten
2. Teste PDF mit anderem PDF-Reader
3. Verifiziere Endpoint-Format: `https://RESOURCE.openai.azure.com/anthropic`

### ".env file not found"
**Problem**: Das run.sh Script findet keine `.env` Datei

**Lösung:**
1. Erstelle `.env` Datei im Projekt-Root
2. Füge API_KEY und API_ENDPOINT hinzu (siehe Installation Schritt 3)

### "Error during web research"
**Mögliche Ursachen:**
- Keine Internetverbindung
- Web-Suche ist für deinen API-Key nicht aktiviert
- Quellen sind nicht erreichbar

**Lösungen:**
1. Prüfe Internetverbindung
2. Kontaktiere Azure Support zur Aktivierung der Web-Suche
3. Versuche es zunächst ohne eigene Quellen (leer lassen)

### "Streamlit won't start"
**Mögliche Ursachen:**
- Dependencies nicht installiert
- Falsche Python-Version
- Port 8501 bereits belegt

**Lösungen:**
```bash
# Dependencies neu installieren
pip install -r requirements.txt

# Python-Version prüfen (sollte 3.9+ sein)
python --version

# Streamlit-Cache löschen
streamlit cache clear

# Anderen Port verwenden
streamlit run app.py --server.port 8502
```

### "Red Flags werden nicht erkannt"
**Problem**: Red Flag Check findet keine getroffenen Kriterien

**Mögliche Ursachen:**
- Red Flags zu spezifisch formuliert
- Informationen im Pitch Deck nicht ausreichend

**Lösung:**
1. Formuliere Red Flags allgemeiner (z.B. "Keine Kunden" statt "Weniger als 100 zahlende Kunden")
2. Prüfe ob relevante Informationen im Pitch Deck vorhanden sind

## 📞 Support & Feedback

Bei Problemen oder Verbesserungsvorschlägen:
- Erstelle ein Issue im GitHub Repository
- Kontaktiere das Entwicklungsteam
- Prüfe die Dokumentation auf Updates
