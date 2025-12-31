"""
fetch_rss.py
============
Holt deutsche News-Schlagzeilen aus RSS-Feeds (Spiegel, Sueddeutsche, etc.)

Strategie
---------
1. XML-RSS-Feeds kombinieren bis max_items erreicht
2. Duplikate werden gefiltert

Alle Requests laufen mit
- echtem Browser-User-Agent
- Zeitlimit 8s pro Feed
"""

from __future__ import annotations
import json
import ssl
import sys
from typing import List

import feedparser
import urllib.request
from urllib.error import HTTPError, URLError


# --------------------------------------------------------------------------- #
# 1) FEED-Kandidaten                                                          #
# --------------------------------------------------------------------------- #
JSON_FEEDS: list[tuple[str, str]] = [
    # Keine JSON-Feeds verfuegbar
]

XML_FEEDS: list[str] = [
    # Good News Network (positive Nachrichten)
    "https://www.goodnewsnetwork.org/category/news/feed/",
]

# --------------------------------------------------------------------------- #
# 2) Werkzeug: “echter” HTTPS-Opener ohne Zert-Prüfung                        #
# --------------------------------------------------------------------------- #
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}

_OPENER = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=_CTX)
)
_OPENER.addheaders = list(_HEADERS.items())


def _fetch(url: str, timeout: int = 8) -> bytes | None:
    """Lädt URL → Bytes, gibt None bei Fehler zurück & loggt ins Terminal."""
    try:
        with _OPENER.open(url, timeout=timeout) as resp:
            if resp.status != 200:
                print(f" WARN: {url} -> HTTP {resp.status}", file=sys.stderr)
                return None
            return resp.read()
    except (HTTPError, URLError, ssl.SSLError) as exc:
        print(f" WARN: {url} -> {exc}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- #
# 3) Parser-Helfer für JSON-Feeds                                             #
# --------------------------------------------------------------------------- #
def _parse_bild_json(data: bytes, title_key: str, max_items: int) -> List[str]:
    try:
        items = json.loads(data)
        # Feed liefert Liste von Dicts unter Root
        titles = [item.get(title_key, "").strip() for item in items[:max_items]]
        return [t for t in titles if t]
    except Exception as exc:  # noqa: BLE001
        print(f" WARN: JSON-Parse-Fail ({exc})", file=sys.stderr)
        return []


# --------------------------------------------------------------------------- #
# 4) Öffentliche Funktion                                                     #
# --------------------------------------------------------------------------- #
def fetch_news_headlines(max_items: int = 30) -> List[str]:
    """
    Holt max. `max_items` frische Schlagzeilen aus mehreren Feeds kombiniert.
    """
    all_titles: List[str] = []
    seen: set = set()

    # --- XML-RSS-Feeds kombinieren ---
    for url in XML_FEEDS:
        if len(all_titles) >= max_items:
            break
        raw = _fetch(url)
        if not raw:
            continue

        feed = feedparser.parse(raw)
        if feed.bozo:
            print(f" XML-Parse-Fail {url}", file=sys.stderr)
            continue
        
        for e in feed.entries:
            if len(all_titles) >= max_items:
                break
            if hasattr(e, "title"):
                title = e.title.strip()
                if title and title not in seen:
                    seen.add(title)
                    all_titles.append(title)
        
        if all_titles:
            print(f" OK: {url} (+{len([t for t in all_titles if t not in seen or True])})")

    if not all_titles:
        print(" Kein Feed lieferte verwertbare Headlines!", file=sys.stderr)
    
    return all_titles[:max_items]


# --------------------------------------------------------------------------- #
# 5) Aliase fuer Kompatibilitaet                                              #
# --------------------------------------------------------------------------- #
fetch_bild_headlines = fetch_news_headlines
fetch_bild_rss_headlines = fetch_news_headlines

