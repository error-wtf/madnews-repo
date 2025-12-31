#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Test-Script
# ═══════════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prüfe ob venv existiert
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "/opt/mad-news/venv" ]; then
    source /opt/mad-news/venv/bin/activate
fi

echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  MAD NEWS - Test Suite${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"

PASSED=0
FAILED=0

# ─────────────────────────────────────────────────────────────────────────────
# Test 1: Python-Abhängigkeiten
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[1/5] Python-Abhängigkeiten...${NC}"
if python3 -c "import requests, feedparser, bs4" 2>/dev/null; then
    echo -e "${GREEN}  ✓ requests, feedparser OK${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ Fehlende Module! pip install -r requirements.txt${NC}"
    ((FAILED++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 2: Config laden
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[2/5] Config laden...${NC}"
if python3 -c "from config import OLLAMA_BASE_URL, FTP_HOST; print(f'  Ollama: {OLLAMA_BASE_URL}'); print(f'  FTP: {FTP_HOST}')" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Config OK${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ Config-Fehler!${NC}"
    ((FAILED++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 3: RSS-Feeds
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[3/5] RSS-Feeds abrufen...${NC}"
if python3 -c "from fetch_rss import fetch_news_headlines; h = fetch_news_headlines(max_items=3); print(f'  {len(h)} Headlines'); exit(0 if h else 1)" 2>/dev/null; then
    echo -e "${GREEN}  ✓ RSS OK${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ RSS-Fehler!${NC}"
    ((FAILED++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 4: FTP-Verbindung
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[4/5] FTP-Verbindung...${NC}"
if python3 -c "from ftp_uploader import test_ftp_connection; exit(0 if test_ftp_connection() else 1)" 2>/dev/null; then
    echo -e "${GREEN}  ✓ FTP OK${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ FTP-Fehler!${NC}"
    ((FAILED++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 5: Ollama-Verbindung
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}[5/5] Ollama-Verbindung...${NC}"
OLLAMA_URL=$(python3 -c "from config import OLLAMA_BASE_URL; print(OLLAMA_BASE_URL.replace('/api/generate',''))" 2>/dev/null)
if curl -s --connect-timeout 5 "${OLLAMA_URL}/api/tags" >/dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Ollama OK (${OLLAMA_URL})${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ Ollama nicht erreichbar (${OLLAMA_URL})${NC}"
    ((FAILED++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Zusammenfassung
# ─────────────────────────────────────────────────────────────────────────────
echo -e "\n${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
TOTAL=$((PASSED + FAILED))
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}  Ergebnis: ${PASSED}/${TOTAL} Tests bestanden${NC}"
    echo -e "${GREEN}  Bereit für Produktion!${NC}"
else
    echo -e "${RED}  Ergebnis: ${PASSED}/${TOTAL} Tests bestanden (${FAILED} fehlgeschlagen)${NC}"
fi
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"

exit $FAILED
