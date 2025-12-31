#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Deinstallation Script
# ═══════════════════════════════════════════════════════════════════════════
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

INSTALL_DIR="/opt/mad-news"
SERVICE_USER="madnews"

echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${RED}  MAD NEWS - Deinstallation${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Bitte als root ausführen (sudo ./uninstall.sh)${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Stoppe und entferne Systemd Services...${NC}"
systemctl stop mad-news.timer 2>/dev/null || true
systemctl disable mad-news.timer 2>/dev/null || true
rm -f /etc/systemd/system/mad-news.service
rm -f /etc/systemd/system/mad-news.timer
systemctl daemon-reload
echo -e "${GREEN}✓ Services entfernt${NC}"

echo -e "\n${YELLOW}Lösche Installationsverzeichnis...${NC}"
rm -rf "$INSTALL_DIR"
echo -e "${GREEN}✓ $INSTALL_DIR gelöscht${NC}"

echo -e "\n${YELLOW}Entferne Service-User...${NC}"
if id "$SERVICE_USER" &>/dev/null; then
    userdel "$SERVICE_USER" 2>/dev/null || true
    echo -e "${GREEN}✓ User '$SERVICE_USER' entfernt${NC}"
fi

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Deinstallation abgeschlossen!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
