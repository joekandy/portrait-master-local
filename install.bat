@echo off
echo  Portrait Master FLUX - Installazione Windows
echo ===============================================
echo.
echo Rilevamento sistema in corso...
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python non trovato! Installa Python 3.8+ da python.org
    pause
    exit /b 1
)

echo  Python rilevato
echo.
echo  Avvio installazione automatica...
python install.py

echo.
echo  Installazione completata!
echo  Trovi l'icona "Portrait Master" sul desktop
pause
