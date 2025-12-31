# MAD NEWS - Satirischer Nachrichten-Generator

Generiert satirische, positive Nachrichten aus BILD-Headlines mit Ollama und einem erweiterten Zahlen-Filter.

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

## 📜 Lizenz

Anti-Capitalist Software License v1.4

---

**Made with 🎭 by error-wtf**