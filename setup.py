#!/usr/bin/env python3
"""
MAD NEWS - Interactive Setup Script
Erstellt die .env Datei mit deinen Credentials
"""

import os
import sys
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("  MAD NEWS - Setup Wizard")
    print("="*60 + "\n")

def print_section(title):
    print(f"\n{title}")
    print("-" * len(title))

def get_input(prompt, default=""):
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def get_yes_no(prompt, default=True):
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    if not response:
        return default
    return response in ['y', 'yes', 'ja', 'j']

def main():
    print_header()
    
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        print(f"⚠️  Die Datei {env_file} existiert bereits!")
        if not get_yes_no("Möchtest du sie überschreiben?", default=False):
            print("Setup abgebrochen.")
            sys.exit(0)
    
    config = {}
    
    # ====== OLLAMA CONFIGURATION ======
    print_section("📡 OLLAMA CONFIGURATION")
    print("Ollama ist die lokale LLM-API für die Satire-Generierung.")
    
    config['OLLAMA_BASE_URL'] = get_input(
        "Ollama API URL",
        "http://localhost:11434/api/generate"
    )
    
    config['OLLAMA_MODEL'] = get_input(
        "Ollama Modell",
        "gpt-oss:120b-cloud"
    )
    
    config['OLLAMA_TIMEOUT'] = get_input(
        "Ollama Timeout (Sekunden)",
        "300"
    )
    
    config['OLLAMA_MAX_TOKENS'] = get_input(
        "Max Tokens",
        "32768"
    )
    
    config['OLLAMA_TEMPERATURE'] = get_input(
        "Temperature (0.0-1.0)",
        "0.7"
    )
    
    # ====== FTP CONFIGURATION ======
    print_section("📤 FTP UPLOAD CONFIGURATION (Optional)")
    print("Aktiviere FTP-Upload um die generierten News automatisch hochzuladen.")
    
    ftp_enabled = get_yes_no("FTP-Upload aktivieren?", default=False)
    config['FTP_ENABLED'] = str(ftp_enabled)
    
    if ftp_enabled:
        config['FTP_HOST'] = get_input("FTP Server (z.B. ftp.example.com)")
        config['FTP_USER'] = get_input("FTP Benutzername")
        config['FTP_PASS'] = get_input("FTP Passwort")
        config['FTP_REMOTE_DIR'] = get_input("Remote Verzeichnis", "madnews")
        config['FTP_REMOTE_FILE'] = get_input("Remote Dateiname", "index.html")
        config['FTP_TIMEOUT'] = get_input("FTP Timeout (Sekunden)", "30")
    else:
        config['FTP_HOST'] = ""
        config['FTP_USER'] = ""
        config['FTP_PASS'] = ""
        config['FTP_REMOTE_DIR'] = "madnews"
        config['FTP_REMOTE_FILE'] = "index.html"
        config['FTP_TIMEOUT'] = "30"
    
    # ====== NEWS SOURCE ======
    print_section("📰 NEWS SOURCE")
    
    config['BILD_SCRAPE_URL'] = get_input(
        "BILD Scrape URL",
        "https://news.google.com/search?q=site:bild.de&hl=de&gl=DE&ceid=DE%3Ade"
    )
    
    config['USE_BILD_SCRAPER'] = str(get_yes_no("BILD Scraper nutzen?", default=True))
    
    # ====== OUTPUT CONFIGURATION ======
    print_section("⚙️  OUTPUT CONFIGURATION")
    
    config['MAX_HEADLINES'] = get_input("Max Anzahl Headlines", "30")
    config['REQUEST_TIMEOUT'] = get_input("Request Timeout (Sekunden)", "15")
    
    # ====== WRITE .ENV FILE ======
    print_section("💾 Speichere Konfiguration...")
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# MAD NEWS - Environment Configuration\n")
        f.write("# Automatisch generiert durch setup.py\n\n")
        
        f.write("# OLLAMA CONFIGURATION\n")
        f.write(f"OLLAMA_BASE_URL={config['OLLAMA_BASE_URL']}\n")
        f.write(f"OLLAMA_MODEL={config['OLLAMA_MODEL']}\n")
        f.write(f"OLLAMA_TIMEOUT={config['OLLAMA_TIMEOUT']}\n")
        f.write(f"OLLAMA_MAX_TOKENS={config['OLLAMA_MAX_TOKENS']}\n")
        f.write(f"OLLAMA_TEMPERATURE={config['OLLAMA_TEMPERATURE']}\n\n")
        
        f.write("# FTP UPLOAD CONFIGURATION\n")
        f.write(f"FTP_ENABLED={config['FTP_ENABLED']}\n")
        f.write(f"FTP_HOST={config['FTP_HOST']}\n")
        f.write(f"FTP_USER={config['FTP_USER']}\n")
        f.write(f"FTP_PASS={config['FTP_PASS']}\n")
        f.write(f"FTP_REMOTE_DIR={config['FTP_REMOTE_DIR']}\n")
        f.write(f"FTP_REMOTE_FILE={config['FTP_REMOTE_FILE']}\n")
        f.write(f"FTP_TIMEOUT={config['FTP_TIMEOUT']}\n\n")
        
        f.write("# NEWS SOURCE\n")
        f.write(f"BILD_SCRAPE_URL={config['BILD_SCRAPE_URL']}\n")
        f.write(f"USE_BILD_SCRAPER={config['USE_BILD_SCRAPER']}\n\n")
        
        f.write("# OUTPUT CONFIGURATION\n")
        f.write(f"MAX_HEADLINES={config['MAX_HEADLINES']}\n")
        f.write(f"REQUEST_TIMEOUT={config['REQUEST_TIMEOUT']}\n")
    
    print(f"✅ Konfiguration gespeichert: {env_file}")
    
    # ====== INSTALL DEPENDENCIES ======
    print_section("📦 Installation")
    
    if get_yes_no("Dependencies jetzt installieren? (pip install -r requirements.txt)", default=True):
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        print("✅ Dependencies installiert")
    
    # ====== DONE ======
    print_section("🎉 Setup abgeschlossen!")
    print("\nNächste Schritte:")
    print("1. Starte Ollama: ollama serve")
    print("2. Lade ein Modell: ollama pull gpt-oss:120b-cloud")
    print("3. Starte MAD NEWS: python run.py")
    print("\nViel Spaß mit MAD NEWS! 🎭\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup abgebrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fehler: {e}")
        sys.exit(1)
