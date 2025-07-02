#!/bin/bash
# Portrait Master FLUX - Installazione Mac/Linux

echo " Portrait Master FLUX - Installazione Locale"
echo "=============================================="
echo

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo " Python 3 non trovato! Installa Python 3.8+"
    exit 1
fi

echo " Python rilevato: $(python3 --version)"
echo

# Verifica Git
if ! command -v git &> /dev/null; then
    echo " Git non trovato! Installa Git"
    exit 1
fi

echo " Git rilevato"
echo

echo " Avvio installazione automatica..."
python3 install.py

echo
echo " Installazione completata!"
echo " Per avviare: python3 launcher.py"
echo " Interfaccia: http://localhost:8188"
