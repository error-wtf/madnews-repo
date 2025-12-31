# 🗞️ MAD NEWS - Satirischer Nachrichten-Generator

Generiert satirische, positive Nachrichten aus News-Headlines mit Ollama und einem erweiterten Zahlen-Filter.

> **🌐 Live Demo:** [https://error.wtf/mad-news/](https://error.wtf/mad-news/)

> **Inspiration:** Dieses Projekt wurde inspiriert von [Mad News (1994)](https://archive.org/details/msdos_Mad_News_1994), einem DOS-Spiel, das satirische Nachrichten generierte. Wir haben die Idee ins KI-Zeitalter übertragen.

## Features

- BILD Scraping via Google News
- Satire-Generierung mit Ollama (`gpt-oss:120b-cloud` oder lokal)
- Intelligenter Zahlen-Filter - verhindert problematische Zahlen (18, 81, 88)
- Bevorzugte sichere Zahlen (13, 17, 19, 23, 37, 42, 52, 73, 93, 103)
- Statische HTML-Ausgabe mit Matrix-Design
- Optionaler FTP-Upload
- Sichere Credential-Verwaltung via `.env`
- Interaktiver Setup-Wizard

## Schnellstart

### 1. Repository klonen

```bash
git clone https://github.com/error-wtf/madnews-repo.git
cd madnews-repo
```

### 2. Setup-Wizard ausführen

```bash
python setup.py
```

Der Setup-Wizard führt dich durch die Konfiguration:
- Ollama API URL (Standard: `http://localhost:11434/api/generate`)
- Ollama Modell (Standard: `gpt-oss:120b-cloud`)
- FTP-Credentials (optional für automatischen Upload)
- Weitere Einstellungen

Die Konfiguration wird in einer `.env` Datei gespeichert.

### 3. Ollama starten

```bash
# Ollama Server starten
ollama serve

# Modell laden (in neuem Terminal)
ollama pull gpt-oss:120b-cloud
```

### 4. MAD NEWS ausführen

```bash
# Test-Lauf (nur Headlines anzeigen, keine Satire generieren)
python run.py --dry-run

# Vollständiger Lauf (Satire generieren)
python run.py
```

Die generierte Satire-Seite findest du unter: `docs/index.html`

## Installation auf Debian/Ubuntu Server

```bash
# Als root ausführen
sudo ./install.sh
```

### Was passiert bei der Installation:

1. System-Abhängigkeiten werden installiert (python3, python3-venv)
2. Service-User `madnews` wird erstellt
3. Dateien werden nach `/opt/mad-news/` kopiert
4. Python Virtual Environment wird erstellt
5. Systemd Service + Timer werden installiert

### Nach der Installation:

```bash
# Timer-Status prüfen
systemctl status mad-news.timer

# Manuell ausführen
sudo systemctl start mad-news.service

# Logs anzeigen
journalctl -u mad-news.service -f

# HTML-Ausgabe
cat /opt/mad-news/docs/index.html
```

## Deinstallation

```bash
sudo ./uninstall.sh
```

## ⚙️ Manuelle Konfiguration

Falls du `setup.py` nicht verwendest, erstelle eine `.env` Datei:

```bash
cp .env.example .env
```

Bearbeite die `.env` Datei:

```env
# OLLAMA CONFIGURATION
OLLAMA_BASE_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gpt-oss:120b-cloud
OLLAMA_TIMEOUT=300
OLLAMA_MAX_TOKENS=32768
OLLAMA_TEMPERATURE=0.7

# FTP UPLOAD (Optional)
FTP_ENABLED=True
FTP_HOST=ftp.your-server.com
FTP_USER=your_username
FTP_PASS=your_password
FTP_REMOTE_DIR=madnews
FTP_REMOTE_FILE=index.html

# NEWS SOURCE
BILD_SCRAPE_URL=https://news.google.com/search?q=site:bild.de&hl=de&gl=DE&ceid=DE%3Ade
USE_BILD_SCRAPER=True

# OUTPUT
MAX_HEADLINES=30
REQUEST_TIMEOUT=15
```

**Wichtig:** Die `.env` Datei enthält sensible Daten und wird **nicht** in Git committed!

## 📁 Dateistruktur

```
madnews-repo/
├── setup.py                 # 🆕 Interaktiver Setup-Wizard
├── run.py                   # Hauptskript
├── config.py                # Konfiguration (lädt .env)
├── twist_with_model.py      # Ollama API Client
├── bild_scraper.py          # BILD Headline Scraper
├── ftp_uploader.py          # FTP Upload Handler
├── satire_prompt.txt        # 🔢 LLM Prompt + Zahlen-Filter
├── requirements.txt         # Python Dependencies
├── .env.example             # 🆕 Beispiel-Konfiguration
├── .gitignore               # 🆕 Git Ignore (inkl. .env)
├── install.sh               # Linux Installation
├── uninstall.sh             # Deinstallation
├── docs/
│   └── index.html           # Generierte Ausgabe
└── README.md
```

**Neue Dateien:**
- `setup.py` - Interaktiver Wizard für einfache Konfiguration
- `.env.example` - Template für deine Credentials
- `.gitignore` - Verhindert versehentliches Committen von Secrets

## Timer anpassen

Der Timer läuft standardmäßig stündlich. Zum Ändern:

```bash
sudo systemctl edit mad-news.timer
```

```ini
[Timer]
OnBootSec=5min
OnUnitActiveSec=2h  # Alle 2 Stunden
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart mad-news.timer
```

## 🤝 Contributing

Contributions sind willkommen! Bitte:
1. Forke das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Erstelle einen Pull Request

---

## ⚠️ Hinweis / Disclaimer

### 1. Satire-Charakter
Alle Beiträge auf dieser Seite sind frei erfundene Satire und dienen ausschließlich der Unterhaltung. Sie basieren auf Schlagzeilen, die wir automatisiert auslesen und mittels KI humoristisch neu interpretieren.

### 2. Keine Diffamierung
Es besteht kein Anspruch, reale Personen oder Institutionen zu verunglimpfen. Vielmehr möchten wir eine alternative, oft überzeichnete Perspektive auf die teils hetzerischen Originalmeldungen bieten.

### 3. Automatisierte Erstellung & Gewähr
Sämtliche Texte werden vollautomatisch von einer Sprach-KI generiert. Für sachliche Richtigkeit, Vollständigkeit oder etwaige unbeabsichtigte Verstöße kann keine Haftung übernommen werden.

### 4. Urheberrecht
Wir verwenden ausschließlich eigene, von der KI erstellte Formulierungen. Ursprüngliche Wortlaute aus Pressequellen werden so weit umgeschrieben, dass keine urheberrechtlich geschützten Passagen erkennbar bleiben.

### 5. Filter & Qualitätskontrolle
Wir entwickeln unsere Filter fortlaufend weiter, um problematische Inhalte frühzeitig auszusortieren. Sollten dennoch unpassende oder beleidigende Passagen erscheinen, freuen wir uns über konstruktives Feedback.

### 6. Künstlerischer Ansatz
Dieses Projekt ist als künstlerisches Experiment zu verstehen: Wir versuchen, den oft beängstigenden und hetzerischen Charakter mancher Schlagzeilen in absurde, unterhaltsame Texte zu verwandeln – ohne neuen Hass zu schüren.

---

## 📜 Lizenz

**Anti-Capitalist Software License v1.4**  
Copyright (c) 2025 Lino Casu

**⚠️ KOMMERZIELLE NUTZUNG STRENG VERBOTEN**

Dieses Projekt steht unter der Anti-Capitalist Software License v1.4. 

### Erlaubte Nutzung:
- ✅ Persönliche, nicht-kommerzielle Nutzung
- ✅ Bildungszwecke
- ✅ Forschung und Entwicklung
- ✅ Gemeinnützige Zwecke

### **VERBOTEN:**
- ❌ **Jegliche kommerzielle Nutzung**
- ❌ **Verkauf der Software oder abgeleiteter Werke**
- ❌ **Nutzung in gewinnorientierten Unternehmen**
- ❌ **Monetarisierung durch Werbung**
- ❌ **Bezahlte Dienste basierend auf dieser Software**

**Vollständiger Lizenztext:** [Anti-Capitalist Software License v1.4](https://anticapitalist.software/)

Bei Fragen zur Lizenzierung kontaktieren Sie: Lino Casu

---

## ⚖️ Umfassende rechtliche Hinweise & Warnungen

### 🚨 RSS Feed Quellen - WICHTIGE WARNUNG

**ACHTUNG:** Nutzen Sie ausschließlich RSS Feeds von Quellen, die keine aggressive Abmahnpraxis betreiben!

- ⚠️ **NICHT EMPFOHLEN:** Springer-Verlag Publikationen (BILD, WELT, etc.) - bekannt für Abmahnungen
- ⚠️ Prüfen Sie die Nutzungsbedingungen Ihrer gewählten Quelle
- ⚠️ Dieses Tool ist für **legale Satire** gedacht, nicht für Urheberrechtsverletzungen

**Empfohlene sichere Quellen:**
- Öffentlich-rechtliche Medien (Tagesschau, ZDF)
- Creative-Commons-lizenzierte Nachrichtenquellen
- Eigene/selbst gehostete News-Feeds

**Sie tragen die volle Verantwortung für die Wahl Ihrer News-Quelle!**

---

### 🛡️ Satire-Prompt & Sicherheitsfilter

Unser Satire-Prompt wurde nach **bestem Wissen und Gewissen** entwickelt und enthält:

#### Implementierte Filter:
1. **Zahlen-Filter:** Blockiert problematische Zahlensymbolik (18, 81, 88, etc.)
2. **Marken-Filter:** Ersetzt echte Markennamen durch satirische Alternativen
3. **Namens-Filter:** Vermeidet vollständige Nennung realer Personen
4. **Blacklist:** 700+ verbotene Begriffe (Gewalt, Hass, Diskriminierung)
5. **Positiv-Zwang:** KI muss positive, gewaltfreie Geschichten erzählen

**Trotz aller Filter:**
- KI-generierte Inhalte sind nicht 100% vorhersagbar
- Unerwünschte Outputs können auftreten
- Kontinuierliche Verbesserung nötig

**Wir bitten um konstruktives Feedback bei problematischen Outputs!**

---

### ⚠️ RECHTLICHE WARNUNG & HAFTUNGSAUSSCHLUSS

#### 1. Reine Satire
Alle generierten Inhalte sind **fiktive Satire** und dienen ausschließlich der Unterhaltung. Es besteht keinerlei Anspruch auf Wahrheit oder Faktentreue.

#### 2. Keine Verantwortung für Missbrauch
**WICHTIG:** Die Entwickler und Rechteinhaber übernehmen **KEINE VERANTWORTUNG** für:
- Missbräuchliche Nutzung dieser Software
- Rechtsverstöße durch Dritte
- Urheberrechtsverletzungen bei unsachgemäßer Quellennutzung
- Schäden jeglicher Art durch Nutzung dieser Software
- Von der KI generierte Inhalte, die gegen Gesetze verstoßen

#### 3. Gegen Hetze & Gewalt
Dieses Projekt steht explizit **GEGEN:**
- Hetze und Hassrede
- Gewalt und Gewaltverherrlichung
- Diskriminierung jeglicher Art
- Fehlinformationen und Desinformation

Wir entwickeln Satire als **antifaschistisches Werkzeug**, um hetzerische Medien zu entlarven.

#### 4. Nutzung auf eigene Gefahr
Die Nutzung erfolgt **auf eigenes Risiko**. Sie sind verantwortlich für:
- Die Wahl Ihrer News-Quelle
- Die Prüfung generierter Inhalte vor Veröffentlichung
- Die Einhaltung aller anwendbaren Gesetze
- Die Respektierung von Urheberrechten Dritter

#### 5. Keine Rechtsberatung
Diese Software und Dokumentation stellen keine Rechtsberatung dar. Konsultieren Sie bei rechtlichen Fragen einen Anwalt.

#### 6. Technische Grenzen
- KI ist nicht perfekt - Filter können versagen
- Keine Garantie für fehlerfreien Betrieb
- Keine Haftung für technische Probleme oder Datenverlust

#### 7. Disclosure & Transparenz
**WIR ÜBERNEHMEN KEINE VERANTWORTUNG FÜR:**
- Verleumdung oder Rufschädigung durch generierte Inhalte
- Urheberrechtsverletzungen bei Missachtung der RSS-Warnung
- Rechtliche Konsequenzen jeglicher Art
- Missbräuchliche oder kriminelle Nutzung
- Schäden an Dritten durch von dieser Software generierte Inhalte

**Nutzen Sie dieses Tool verantwortungsvoll und rechtmäßig!**

---

**Made with 🎭 by error-wtf | Gegen Hetze, für Humor**