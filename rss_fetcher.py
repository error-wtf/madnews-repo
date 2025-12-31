"""
rss_fetcher.py - BILD Headlines Scraper (via Google News)
"""
import logging
import requests
from bs4 import BeautifulSoup
from typing import List

from config import BILD_SCRAPE_URL, REQUEST_TIMEOUT, MAX_HEADLINES

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Fallback Headlines falls Scraping fehlschlägt
FALLBACK_HEADLINES = [
    "Mann isst 42 Currywuerste - Weltrekord oder Wahnsinn?",
    "Katzen uebernehmen Bundestag",
    "Olaf Scholz erklaert Montag fuer abgeschafft",
    "Neue Partei fordert: Gratis Pommes fuer alle",
    "Wissenschaftler entdecken, dass Kaffee denken kann",
    "Habeck warnt vor Heizkatastrophe",
    "Putin startet TikTok-Channel",
    "Scholz vergisst eigenen Namen",
    "Kanzleramt in Currywurst umbenannt",
    "Lindner gruendet Spar-Partei"
]


def fetch_headlines(max_items: int = MAX_HEADLINES) -> List[str]:
    """
    Scraped BILD-Headlines von Google News.
    
    Args:
        max_items: Maximale Anzahl Headlines
        
    Returns:
        Liste von Headlines
    """
    try:
        logger.info(f"Scrape BILD-Headlines von Google News...")
        response = requests.get(
            BILD_SCRAPE_URL,
            headers=_HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = []
        
        # Google News article headlines
        for h in soup.select("article h3, article h4"):
            text = h.get_text(strip=True)
            if text and len(text) > 10:
                headlines.append(text)
        
        if headlines:
            headlines = headlines[:max_items]
            logger.info(f"OK: {len(headlines)} BILD-Headlines gefunden")
            return headlines
        
        logger.warning("Keine Headlines gefunden, nutze Fallback")
        return FALLBACK_HEADLINES[:max_items]
        
    except Exception as e:
        logger.error(f"Scraping fehlgeschlagen: {e}")
        logger.info("Nutze Fallback-Headlines")
        return FALLBACK_HEADLINES[:max_items]
