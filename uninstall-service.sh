#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Service Deinstallation (nur Systemd)
# ═══════════════════════════════════════════════════════════════════════════
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${RED}  MAD NEWS - Service Deinstallation${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Bitte als root ausführen (sudo ./uninstall-service.sh)${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Stoppe Timer und Service...${NC}"
systemctl stop mad-news.timer 2>/dev/null || true
systemctl stop mad-news.service 2>/dev/null || true
systemctl disable mad-news.timer 2>/dev/null || true

echo -e "\n${YELLOW}Entferne Systemd-Dateien...${NC}"
rm -f /etc/systemd/system/mad-news.service
rm -f /etc/systemd/system/mad-news.timer
systemctl daemon-reload

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Service entfernt!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}Hinweis:${NC} Dateien unter /opt/mad-news/ bleiben erhalten."
echo -e "  Zum vollständigen Entfernen: sudo ./uninstall.sh"
echo ""
