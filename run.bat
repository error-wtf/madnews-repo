@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM MAD NEWS - Manueller Start (Windows)
REM ═══════════════════════════════════════════════════════════════════════════
cd /d "%~dp0"

REM Aktiviere venv falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo ═══════════════════════════════════════════════════════════════
echo   MAD NEWS - Manueller Start
echo   %DATE% %TIME%
echo ═══════════════════════════════════════════════════════════════

python mad_news.py %*

echo.
echo Fertig: %DATE% %TIME%
pause
