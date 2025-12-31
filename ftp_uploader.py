"""
ftp_uploader.py - FTP Upload für MAD NEWS
"""
import logging
from ftplib import FTP, error_perm
from pathlib import Path

from config import (
    FTP_ENABLED,
    FTP_HOST,
    FTP_USER,
    FTP_PASS,
    FTP_REMOTE_DIR,
    FTP_REMOTE_FILE,
    FTP_TIMEOUT,
    OUTPUT_FILE,
)

logger = logging.getLogger(__name__)


def upload_to_ftp(local_file: Path = OUTPUT_FILE) -> bool:
    """
    Lädt die generierte HTML-Datei auf den FTP-Server hoch.
    
    Args:
        local_file: Pfad zur lokalen Datei
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    if not FTP_ENABLED:
        logger.info("FTP Upload deaktiviert (FTP_ENABLED=False)")
        return True
    
    if not local_file.exists():
        logger.error(f"Datei nicht gefunden: {local_file}")
        return False
    
    try:
        logger.info(f"FTP: Verbinde mit {FTP_HOST}...")
        
        with FTP(FTP_HOST, timeout=FTP_TIMEOUT) as ftp:
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            logger.info("FTP: Login erfolgreich")
            
            # In Zielverzeichnis wechseln
            try:
                ftp.cwd(FTP_REMOTE_DIR)
            except error_perm:
                # Verzeichnis existiert nicht, erstellen
                logger.info(f"FTP: Erstelle Verzeichnis {FTP_REMOTE_DIR}")
                ftp.mkd(FTP_REMOTE_DIR)
                ftp.cwd(FTP_REMOTE_DIR)
            
            # Datei hochladen
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {FTP_REMOTE_FILE}", f)
            
            logger.info(f"FTP: Upload OK -> /{FTP_REMOTE_DIR}/{FTP_REMOTE_FILE}")
            return True
            
    except Exception as e:
        logger.error(f"FTP: Fehler - {e}")
        return False


def test_ftp_connection() -> bool:
    """Testet die FTP-Verbindung ohne Upload."""
    try:
        with FTP(FTP_HOST, timeout=FTP_TIMEOUT) as ftp:
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            dirs = ftp.nlst()
            logger.info(f"FTP: Verbindung OK, {len(dirs)} Eintraege im Root")
            return True
    except Exception as e:
        logger.error(f"FTP: Verbindungstest fehlgeschlagen - {e}")
        return False
