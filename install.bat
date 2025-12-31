@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM MAD NEWS - Windows Installation
REM ═══════════════════════════════════════════════════════════════════════════
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ═══════════════════════════════════════════════════════════════
echo   MAD NEWS - Windows Installation
echo ═══════════════════════════════════════════════════════════════

REM ─────────────────────────────────────────────────────────────────────────────
REM 1. Python prüfen
REM ─────────────────────────────────────────────────────────────────────────────
echo.
echo [1/4] Pruefe Python...
python --version >NUL 2>&1
if errorlevel 1 (
    echo   FEHLER: Python nicht gefunden!
    echo   Bitte Python 3.10+ installieren: https://python.org
    pause
    exit /b 1
)
python --version
echo   OK

REM ─────────────────────────────────────────────────────────────────────────────
REM 2. Virtual Environment erstellen
REM ─────────────────────────────────────────────────────────────────────────────
echo.
echo [2/4] Erstelle Virtual Environment...
if not exist "venv" (
    python -m venv venv
    echo   venv erstellt
) else (
    echo   venv existiert bereits
)

REM ─────────────────────────────────────────────────────────────────────────────
REM 3. Dependencies installieren
REM ─────────────────────────────────────────────────────────────────────────────
echo.
echo [3/4] Installiere Dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo   OK

REM ─────────────────────────────────────────────────────────────────────────────
REM 4. Verzeichnisse erstellen
REM ─────────────────────────────────────────────────────────────────────────────
echo.
echo [4/4] Erstelle Verzeichnisse...
if not exist "docs" mkdir docs
if not exist "logs" mkdir logs
echo   OK

REM ═══════════════════════════════════════════════════════════════════════════
REM Fertig
REM ═══════════════════════════════════════════════════════════════════════════
echo.
echo ═══════════════════════════════════════════════════════════════
echo   Installation abgeschlossen!
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Naechste Schritte:
echo.
echo   1. Test ausfuehren:
echo      test.bat
echo.
echo   2. Dry-Run (ohne Ollama):
echo      run.bat --dry-run
echo.
echo   3. Vollstaendiger Lauf:
echo      run.bat
echo.
echo   4. Loop-Modus (stuendlich):
echo      run_loop.bat
echo.
pause
