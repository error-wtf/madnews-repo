#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# MAD NEWS - Loop-Modus (stündlich)
# ═══════════════════════════════════════════════════════════════════════════
# Hinweis: Für Produktion besser systemd Timer verwenden!

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Prüfe ob venv existiert
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "/opt/mad-news/venv" ]; then
    source /opt/mad-news/venv/bin/activate
fi

INTERVAL=3600  # 1 Stunde in Sekunden

echo "═══════════════════════════════════════════════════════════════"
echo "  MAD NEWS - Loop-Modus (alle ${INTERVAL}s)"
echo "  Strg+C zum Beenden"
echo "═══════════════════════════════════════════════════════════════"

while true; do
    echo ""
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starte MAD NEWS..."
    echo "───────────────────────────────────────────────────────────────"
    
    python3 mad_news.py
    
    echo "───────────────────────────────────────────────────────────────"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Warte ${INTERVAL} Sekunden..."
    sleep $INTERVAL
done
