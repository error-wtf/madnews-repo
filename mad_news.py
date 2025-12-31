#!/usr/bin/env python3
"""
mad_news.py - MAD NEWS Satire Generator
========================================
Holt Headlines aus RSS-Feeds und generiert satirische Artikel mit Ollama Cloud.

Usage:
    python mad_news.py [--max N] [--dry-run] [--no-upload]
"""
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR, OUTPUT_FILE, MAX_HEADLINES, FTP_ENABLED
from fetch_rss import fetch_bild_headlines
from twist_with_model import generate_satire
from ftp_uploader import upload_to_ftp, test_ftp_connection

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def generate_full_html(html_blocks: list[str], timestamp: datetime) -> str:
    """Generiert vollstaendiges HTML aus Satire-HTML-Bloecken."""
    items = []
    for block in html_blocks:
        items.append(f"<article>\n{block}\n</article>")
    
    body = "\n<hr/>\n".join(items)
    
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MAD NEWS - Satirische Nachrichten</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        h1 {{
            color: #c00;
            border-bottom: 3px solid #c00;
            padding-bottom: 10px;
        }}
        article {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        article b {{
            color: #333;
            font-size: 1.2em;
            display: block;
            margin-bottom: 10px;
        }}
        hr {{
            border: none;
            height: 1px;
            background: #ddd;
            margin: 30px 0;
        }}
        footer {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <h1>MAD NEWS</h1>
    <p><em>Satirische Nachrichten aus einer besseren Welt</em></p>
    
    {body}
    
    <footer>
        <hr/>
        <p>Stand: {timestamp:%d.%m.%Y %H:%M:%S}</p>
        <p>Generiert mit KI</p>
    </footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="MAD NEWS Satire Generator")
    parser.add_argument("--max", type=int, default=MAX_HEADLINES, help="Max Headlines")
    parser.add_argument("--dry-run", action="store_true", help="Nur Headlines anzeigen")
    parser.add_argument("--no-upload", action="store_true", help="FTP-Upload deaktivieren")
    parser.add_argument("--test-ftp", action="store_true", help="Nur FTP-Verbindung testen")
    args = parser.parse_args()
    
    # FTP-Test Modus
    if args.test_ftp:
        logger.info("Teste FTP-Verbindung...")
        if test_ftp_connection():
            logger.info("FTP-Verbindung OK")
            sys.exit(0)
        else:
            logger.error("FTP-Verbindung fehlgeschlagen")
            sys.exit(1)
    
    logger.info("MAD NEWS Generator startet...")
    
    # Headlines holen
    headlines = fetch_bild_headlines(max_items=args.max)
    if not headlines:
        logger.error("Keine Headlines gefunden!")
        sys.exit(1)
    
    logger.info(f"-> {len(headlines)} Headlines gefunden")
    
    if args.dry_run:
        for i, h in enumerate(headlines, 1):
            print(f"{i}. {h}")
        sys.exit(0)
    
    # Satire generieren
    satire_html_blocks: list[str] = []
    
    logger.info("Generiere Satire mit Ollama...")
    for idx, headline in enumerate(headlines, 1):
        short = headline[:50] + "..." if len(headline) > 50 else headline
        logger.info(f"  [{idx}/{len(headlines)}] {short}")
        
        try:
            html_block = generate_satire(headline)
            if html_block:
                satire_html_blocks.append(html_block)
                logger.info(f"    OK")
            else:
                logger.warning(f"    Keine Antwort")
                
        except Exception as e:
            logger.warning(f"    Fehler: {e}")
    
    if not satire_html_blocks:
        logger.error("Kein einziger Satire-Block erzeugt!")
        sys.exit(1)
    
    # HTML schreiben
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html = generate_full_html(satire_html_blocks, datetime.now())
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    
    logger.info(f"{len(satire_html_blocks)} Artikel gespeichert: {OUTPUT_FILE}")
    
    # FTP Upload
    if FTP_ENABLED and not args.no_upload:
        logger.info("Starte FTP-Upload...")
        if upload_to_ftp(OUTPUT_FILE):
            logger.info("FTP-Upload erfolgreich")
        else:
            logger.error("FTP-Upload fehlgeschlagen")
            sys.exit(1)
    elif args.no_upload:
        logger.info("FTP-Upload uebersprungen (--no-upload)")
    
    logger.info("Fertig!")


if __name__ == "__main__":
    main()
