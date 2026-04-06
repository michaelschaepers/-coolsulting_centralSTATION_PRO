@echo off
:: ################################################################################
:: APP-NAME:      °coolWIRE
:: AUTOR:         Michael Schäpers_°coolsulting
:: DATUM:         03.04.2026
:: ZWECK:         Sicherer Start auf Port 8580 (relativer Pfad)
################################################################################

title °coolWIRE Starter
:: Wechselt automatisch in das Verzeichnis, in dem diese BAT liegt
cd /d "%~dp0"

echo Port 8580 wird geprueft und ggf. befreit...
:: Versucht einen eventuell haengenden Port zu schließen
powershell -Command "Stop-Process -Id (Get-NetTCPConnection -LocalPort 8580).OwningProcess -Force" 2>nul

echo Starte °coolWIRE Umgebung...
if not exist "venv\Scripts\activate.bat" (
    echo [FEHLER] Virtuelle Umgebung 'venv' wurde nicht gefunden!
    echo Bitte stelle sicher, dass der Ordner 'venv' hier existiert: %~dp0
    pause
    exit
)

call venv\Scripts\activate.bat

echo App wird geladen...
streamlit run coolWIRE_main.py --server.port 8580

pause