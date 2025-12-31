from ftplib import FTP
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FTP-Zugangsdaten aus Umgebungsvariablen
FTP_HOST = os.getenv("FTP_HOST", "")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASS = os.getenv("FTP_PASS", "")

# Lokaler Pfad zur HTML-Datei
local_file = "D:\\mad-news-ollama\\docs\\index.html"

# Ziel auf dem Server
remote_dir = "madnews"
remote_file = "index.html"

def upload_file():
    try:
        print("🔌 Verbinde mit FTP-Server...")
        with FTP(FTP_HOST) as ftp:
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            print("✅ Erfolgreich verbunden.")

            # In Zielverzeichnis wechseln
            ftp.cwd(remote_dir)

            # Datei hochladen
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {remote_file}", f)
                print(f"📤 Hochgeladen: {remote_file} → /{remote_dir}/")

    except Exception as e:
        print(f"❌ Fehler beim Hochladen: {e}")

if __name__ == "__main__":
    upload_file()
