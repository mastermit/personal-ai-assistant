#!/bin/bash

# Installatiescript voor de persoonlijke AI-assistent op macOS
# Dit script zal alle benodigde componenten configureren

echo "=========================================="
echo "Persoonlijke AI-assistent Setup"
echo "=========================================="
echo ""

# Controleer of Python is geïnstalleerd
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is niet geïnstalleerd. Installeer Python 3 eerst."
    echo "Je kunt het downloaden van https://www.python.org/downloads/"
    exit 1
fi

echo "Python 3 gevonden: $(python3 --version)"

# Controleer Python versie
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "Python 3.8 of hoger is vereist. Je hebt versie $python_version"
    exit 1
fi

echo "Virtuele omgeving aanmaken..."
python3 -m venv venv

# Activeer de virtuele omgeving
echo "Virtuele omgeving activeren..."
source venv/bin/activate

# Installeer benodigde packages
echo "Packages installeren..."
pip install -r requirements.txt

# Maak .env bestand
echo "Configureer de API-sleutel..."
read -p "Voer je Together.ai API-sleutel in (laat leeg om over te slaan): " api_key

if [ -n "$api_key" ]; then
    echo "TOGETHER_API_KEY=$api_key" > backend/.env
    echo "PORT=5000" >> backend/.env
    echo "API-sleutel geconfigureerd."
else
    echo "API-sleutel configuratie overgeslagen. Je moet handmatig backend/.env aanmaken."
    echo "Kopieer backend/.env.example naar backend/.env en bewerk het bestand."
fi

echo ""
echo "=========================================="
echo "Installatie voltooid! 🎉"
echo ""
echo "Om de applicatie te starten:"
echo "1. Activeer de virtuele omgeving: source venv/bin/activate"
echo "2. Start de backend: cd backend && python server.py"
echo "3. Open frontend/index.html in je browser"
echo ""
echo "Als je de virtuele omgeving wilt verlaten, typ: deactivate"
echo "=========================================="
