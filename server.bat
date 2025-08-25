@echo off
:: Prüfe, ob Python installiert ist
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nicht gefunden. Bitte installieren.
    pause
    exit /b
)

:: Starte lokalen Server auf Port 8000
start "" http://localhost:8000/raetsel.html
python -m http.server 8000
