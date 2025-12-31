"""
ollama_client.py - Ollama Client (HTTP API)
"""
import requests
import json
import re
import logging
from typing import Optional

from config import OLLAMA_TIMEOUT, PROMPT_FILE

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"

# Steuerzeichen entfernen
_CTRL = re.compile(r"[\x00-\x1F\x7F-\x9F]")


def _load_prompt() -> str:
    """Laedt satire_prompt.txt"""
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8").strip()
    return "Du bist ein satirischer Nachrichtenschreiber. Schreibe auf Deutsch."


def generate_satire(headline: str) -> Optional[str]:
    """
    Generiert Satire mit Ollama HTTP API.
    
    Args:
        headline: Original-Headline
        
    Returns:
        Generierter Satire-Text oder None
    """
    base_prompt = _load_prompt()
    full_prompt = f"{base_prompt}\n\nOriginalheadline: {headline}\n"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
    }
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        result = data.get("response", "").strip()
        return _CTRL.sub("", result) if result else None
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout nach {OLLAMA_TIMEOUT}s")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API-Fehler: {e}")
    except Exception as e:
        logger.error(f"Fehler: {e}")
    
    return None


def clean_response(raw: str) -> tuple[str, str]:
    """
    Bereinigt die LLM-Antwort und extrahiert Headline + Artikel.
    """
    # Entferne <think>-Bloecke
    txt = raw
    while True:
        start = txt.lower().find('<think')
        if start == -1:
            break
        end = txt.lower().find('</think>', start)
        if end != -1:
            txt = txt[:start] + txt[end + 8:]
        else:
            txt = txt[:start]
    
    txt = txt.strip()
    
    # Split nach doppeltem Zeilenumbruch
    parts = [p.strip() for p in txt.split("\n\n") if p.strip()]
    
    if len(parts) < 2:
        # Versuche einfachen Split
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        if len(lines) >= 2:
            return lines[0], "\n".join(lines[1:])
        raise ValueError(f"Unpassendes Format: {repr(txt[:200])}")
    
    headline = parts[0]
    artikel = "\n\n".join(parts[1:])
    
    # Entferne Labels
    for label in ["Headline:", "Satire:", "Article:", "Artikel:", "**", "Ueberschrift:"]:
        headline = headline.replace(label, "").strip(' ":')
    
    return headline.strip(), artikel.strip()
