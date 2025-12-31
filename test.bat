@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM MAD NEWS - Test-Script (Windows)
REM ═══════════════════════════════════════════════════════════════════════════
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Aktiviere venv falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo ===============================================================
echo   MAD NEWS - Test Suite
echo ===============================================================

set PASSED=0
set FAILED=0

echo.
echo [1/5] Python-Abhaengigkeiten...
python -c "import requests, feedparser; print('  OK')" 2>NUL
if errorlevel 1 (
    echo   FEHLER: pip install -r requirements.txt
    set /a FAILED+=1
) else (
    set /a PASSED+=1
)

echo.
echo [2/5] Config laden...
python -c "from config import OLLAMA_BASE_URL, FTP_HOST; print('  Ollama:', OLLAMA_BASE_URL); print('  FTP:', FTP_HOST)" 2>NUL
if errorlevel 1 (
    echo   FEHLER: Config nicht ladbar
    set /a FAILED+=1
) else (
    set /a PASSED+=1
)

echo.
echo [3/5] RSS-Feeds abrufen...
python -c "from fetch_rss import fetch_news_headlines; h=fetch_news_headlines(max_items=3); print('  Headlines:', len(h)); exit(0 if h else 1)" 2>NUL
if errorlevel 1 (
    echo   FEHLER: RSS nicht erreichbar
    set /a FAILED+=1
) else (
    set /a PASSED+=1
)

echo.
echo [4/5] FTP-Verbindung...
python -c "from ftp_uploader import test_ftp_connection; exit(0 if test_ftp_connection() else 1)" 2>NUL
if errorlevel 1 (
    echo   FEHLER: FTP nicht erreichbar
    set /a FAILED+=1
) else (
    echo   OK
    set /a PASSED+=1
)

echo.
echo [5/5] Ollama-Verbindung...
curl -s --connect-timeout 5 http://localhost:11434/api/tags >NUL 2>&1
if errorlevel 1 (
    echo   WARNUNG: Ollama nicht erreichbar (optional fuer --dry-run)
    set /a FAILED+=1
) else (
    echo   OK: Ollama laeuft
    set /a PASSED+=1
)

echo.
echo ===============================================================
set /a TOTAL=!PASSED!+!FAILED!
echo   Ergebnis: !PASSED!/!TOTAL! Tests bestanden
if !FAILED! EQU 0 (
    echo   Bereit fuer Produktion!
) else (
    echo   !FAILED! Test^(s^) fehlgeschlagen
)
echo ===============================================================
pause
