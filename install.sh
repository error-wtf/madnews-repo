#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Debian/Ubuntu Installation Script
# ═══════════════════════════════════════════════════════════════════════════
set -e

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Konfiguration
INSTALL_DIR="/opt/mad-news"
SERVICE_USER="madnews"
PYTHON_VERSION="python3"

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  MAD NEWS - Installation${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

# Root-Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Bitte als root ausführen (sudo ./install.sh)${NC}"
    exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
# 1. System-Abhängigkeiten
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[1/6] Installiere System-Abhängigkeiten...${NC}"
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv curl

# ─────────────────────────────────────────────────────────────────────────────
# 2. Service-User erstellen
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[2/6] Erstelle Service-User...${NC}"
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
    echo -e "${GREEN}✓ User '$SERVICE_USER' erstellt${NC}"
else
    echo -e "${GREEN}✓ User '$SERVICE_USER' existiert bereits${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# 3. Installationsverzeichnis
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[3/6] Erstelle Installationsverzeichnis...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/docs"
mkdir -p "$INSTALL_DIR/logs"

# Kopiere Dateien
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/config.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/fetch_rss.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/twist_with_model.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/ftp_uploader.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/mad_news.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/satire_prompt.txt" "$INSTALL_DIR/"

chmod +x "$INSTALL_DIR/mad_news.py"
echo -e "${GREEN}✓ Dateien kopiert nach $INSTALL_DIR${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# 4. Python Virtual Environment
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[4/6] Erstelle Python Virtual Environment...${NC}"
$PYTHON_VERSION -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

pip install --upgrade pip -q
pip install requests feedparser beautifulsoup4 -q

deactivate
echo -e "${GREEN}✓ Virtual Environment erstellt${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# 5. Berechtigungen
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[5/6] Setze Berechtigungen...${NC}"
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
chmod 755 "$INSTALL_DIR"
chmod 644 "$INSTALL_DIR"/*.py
chmod 644 "$INSTALL_DIR/satire_prompt.txt"
chmod 755 "$INSTALL_DIR/mad_news.py"
echo -e "${GREEN}✓ Berechtigungen gesetzt${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# 6. Systemd Service + Timer
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[6/6] Installiere Systemd Service...${NC}"

# Service-Datei
cat > /etc/systemd/system/mad-news.service << EOF
[Unit]
Description=MAD NEWS Satire Generator
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/mad_news.py
StandardOutput=append:$INSTALL_DIR/logs/mad-news.log
StandardError=append:$INSTALL_DIR/logs/mad-news.log

# Sicherheit
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$INSTALL_DIR/docs $INSTALL_DIR/logs
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
EOF

# Timer-Datei (stündlich)
cat > /etc/systemd/system/mad-news.timer << EOF
[Unit]
Description=MAD NEWS stündlicher Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
RandomizedDelaySec=5min
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Systemd neu laden und aktivieren
systemctl daemon-reload
systemctl enable mad-news.timer
systemctl start mad-news.timer

echo -e "${GREEN}✓ Systemd Service + Timer installiert${NC}"

# ═══════════════════════════════════════════════════════════════════════════
# Fertig
# ═══════════════════════════════════════════════════════════════════════════
echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Installation abgeschlossen!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}Installationspfad:${NC} $INSTALL_DIR"
echo -e "  ${YELLOW}Ausgabe HTML:${NC}      $INSTALL_DIR/docs/index.html"
echo -e "  ${YELLOW}Logs:${NC}              $INSTALL_DIR/logs/mad-news.log"
echo ""
echo -e "  ${YELLOW}Befehle:${NC}"
echo -e "    systemctl status mad-news.timer   # Timer-Status"
echo -e "    systemctl start mad-news.service  # Manuell ausführen"
echo -e "    journalctl -u mad-news.service    # Logs anzeigen"
echo ""
echo -e "  ${YELLOW}Test:${NC}"
echo -e "    sudo -u $SERVICE_USER $INSTALL_DIR/venv/bin/python $INSTALL_DIR/mad_news.py --dry-run"
echo ""
