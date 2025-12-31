"""
config.py - Zentrale Konfiguration für MAD NEWS
Credentials werden aus .env Datei geladen
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Ollama Konfiguration
# ─────────────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "300"))
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_MAX_TOKENS", "32768"))
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))

# ─────────────────────────────────────────────────────────────
# News Quellen (Google News Scraping)
# ─────────────────────────────────────────────────────────────
NEWS_SCRAPE_URL = os.getenv("NEWS_SCRAPE_URL", "")
USE_NEWS_SCRAPER = os.getenv("USE_NEWS_SCRAPER", "True").lower() == "true"

# ─────────────────────────────────────────────────────────────
# Ausgabe
# ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"
PROMPT_FILE = BASE_DIR / "satire_prompt.txt"

# ─────────────────────────────────────────────────────────────
# FTP Upload
# ─────────────────────────────────────────────────────────────
FTP_ENABLED = os.getenv("FTP_ENABLED", "True").lower() == "true"
FTP_HOST = os.getenv("FTP_HOST", "")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASS = os.getenv("FTP_PASS", "")
FTP_REMOTE_DIR = os.getenv("FTP_REMOTE_DIR", "madnews")
FTP_REMOTE_FILE = os.getenv("FTP_REMOTE_FILE", "index.html")
FTP_TIMEOUT = int(os.getenv("FTP_TIMEOUT", "30"))

# ─────────────────────────────────────────────────────────────
# Limits
# ─────────────────────────────────────────────────────────────
MAX_HEADLINES = int(os.getenv("MAX_HEADLINES", "30"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
