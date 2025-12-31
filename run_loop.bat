@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM MAD NEWS - Loop-Modus (Windows)
REM ═══════════════════════════════════════════════════════════════════════════
cd /d "%~dp0"

REM Aktiviere venv falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo ═══════════════════════════════════════════════════════════════
echo   MAD NEWS - Loop-Modus (stuendlich)
echo   Strg+C zum Beenden
echo ═══════════════════════════════════════════════════════════════

:START
    echo.
    echo [%DATE% %TIME%] Starte MAD NEWS...
    echo ---------------------------------------------------------------
    python mad_news.py
    echo ---------------------------------------------------------------
    echo [%DATE% %TIME%] Warte 3600 Sekunden...
    timeout /t 3600 /nobreak >NUL
goto START

