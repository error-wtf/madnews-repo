#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Service Installation (nur Systemd)
# ═══════════════════════════════════════════════════════════════════════════
# Voraussetzung: Dateien bereits unter /opt/mad-news/ oder im aktuellen Verzeichnis
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Konfiguration
SERVICE_USER="madnews"
INSTALL_DIR="/opt/mad-news"

echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  MAD NEWS - Service Installation${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

# Root-Check
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Bitte als root ausführen (sudo ./install-service.sh)${NC}"
    exit 1
fi

# Prüfe ob Installationsverzeichnis existiert
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}Fehler: $INSTALL_DIR existiert nicht!${NC}"
    echo -e "${YELLOW}Bitte zuerst ./install.sh ausführen oder Dateien manuell kopieren.${NC}"
    exit 1
fi

# ─────────────────────────────────────────────────────────────────────────────
# 1. Service-User erstellen (falls nicht vorhanden)
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[1/4] Prüfe Service-User...${NC}"
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
    echo -e "${GREEN}✓ User '$SERVICE_USER' erstellt${NC}"
else
    echo -e "${GREEN}✓ User '$SERVICE_USER' existiert bereits${NC}"
fi

# Berechtigungen setzen
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

# ─────────────────────────────────────────────────────────────────────────────
# 2. Systemd Service erstellen
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[2/4] Erstelle Systemd Service...${NC}"

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

echo -e "${GREEN}✓ /etc/systemd/system/mad-news.service erstellt${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# 3. Systemd Timer erstellen (stündlich)
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[3/4] Erstelle Systemd Timer...${NC}"

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

echo -e "${GREEN}✓ /etc/systemd/system/mad-news.timer erstellt${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# 4. Service aktivieren und starten
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[4/4] Aktiviere und starte Timer...${NC}"

systemctl daemon-reload
systemctl enable mad-news.timer
systemctl start mad-news.timer

echo -e "${GREEN}✓ Timer aktiviert und gestartet${NC}"

# ═══════════════════════════════════════════════════════════════════════════
# Zusammenfassung
# ═══════════════════════════════════════════════════════════════════════════
echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Service-Installation abgeschlossen!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}Status prüfen:${NC}"
echo -e "    systemctl status mad-news.timer"
echo -e "    systemctl list-timers | grep mad-news"
echo ""
echo -e "  ${YELLOW}Manuell ausführen:${NC}"
echo -e "    sudo systemctl start mad-news.service"
echo ""
echo -e "  ${YELLOW}Logs anzeigen:${NC}"
echo -e "    journalctl -u mad-news.service -f"
echo -e "    tail -f $INSTALL_DIR/logs/mad-news.log"
echo ""
echo -e "  ${YELLOW}Service stoppen:${NC}"
echo -e "    sudo systemctl stop mad-news.timer"
echo -e "    sudo systemctl disable mad-news.timer"
echo ""
