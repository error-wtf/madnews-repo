#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Manueller Start (Linux)
# ═══════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prüfe ob venv existiert
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "/opt/mad-news/venv" ]; then
    source /opt/mad-news/venv/bin/activate
fi

echo "═══════════════════════════════════════════════════════════════"
echo "  MAD NEWS - Manueller Start"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════════════"

python3 mad_news.py "$@"

echo ""
echo "Fertig: $(date '+%Y-%m-%d %H:%M:%S')"
