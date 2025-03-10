# Installatiehandleiding

Volg deze stappen om je persoonlijke AI-assistent op te zetten.

## Vereisten

- Python 3.8 of hoger
- Internetverbinding
- Web browser
- Gratis account bij OpenRouter of Together.ai (voor API-toegang)

## Stap 1: Repository klonen

Kloon de repository naar je computer:

```bash
git clone https://github.com/mastermit/personal-ai-assistant.git
cd personal-ai-assistant
```

Of download en pak het ZIP-bestand uit als je Git niet hebt geïnstalleerd.

## Stap 2: Python omgeving instellen

Het is aan te raden om een virtuele omgeving te gebruiken. In je terminal:

```bash
# Virtuele omgeving aanmaken
python -m venv venv

# Activeren op macOS/Linux
source venv/bin/activate

# Activeren op Windows
venv\Scripts\activate
```

## Stap 3: Dependencies installeren

Installeer de benodigde packages:

```bash
pip install -r requirements.txt
```

## Stap 4: API-sleutel instellen

### Optie 1: OpenRouter (Aanbevolen)

1. Maak een gratis account aan op [OpenRouter](https://openrouter.ai)
2. Ga naar je account instellingen om een API-sleutel te verkrijgen
3. In de `backend` map, maak een bestand aan genaamd `.env` en voeg het volgende toe:

```
OPENROUTER_API_KEY=jouw_openrouter_api_sleutel_hier
DEFAULT_PROVIDER=openrouter
PORT=5000
```

### Optie 2: Together.ai (Alternatief)

1. Maak een gratis account aan op [Together.ai](https://www.together.ai)
2. Ga naar je account instellingen om een API-sleutel te verkrijgen
3. In de `backend` map, maak een bestand aan genaamd `.env` en voeg het volgende toe:

```
TOGETHER_API_KEY=jouw_together_api_sleutel_hier
DEFAULT_PROVIDER=together
PORT=5000
```

Je kunt het `.env.example` bestand kopiëren en hernoemen als uitgangspunt.

## Stap 5: Backend starten

Vanuit de hoofdmap van het project:

```bash
cd backend
python server.py
```

Je zou een bericht moeten zien dat de server draait op `http://0.0.0.0:5000`.

## Stap 6: Frontend openen

Open het bestand `frontend/index.html` in je webbrowser. Je kunt dit doen door:

1. Te dubbelklikken op het bestand in je bestandsbrowser
2. Of te openen via een lokale webserver zoals de Live Server extensie in VSCode

## Stap 7: Testen

1. Kies een provider in het dropdown menu (OpenRouter of Together.ai)
2. Kies een model in het tweede dropdown menu
3. Typ een bericht in het chatvenster en klik op 'Verstuur' om te controleren of alles werkt

## Probleemoplossing

Als je problemen ondervindt:

1. **Backend fout**: Controleer of je terminal waar je `server.py` hebt gestart geen foutmeldingen weergeeft
2. **API-sleutel fout**: Controleer of je API-sleutel correct is ingesteld in je `.env` bestand
3. **Frontend verbindingsfout**: Controleer of je backend draait en toegankelijk is op poort 5000
4. **OpenRouter of Together.ai**:
   - Bij OpenRouter: Controleer of je HTTP-Referer header correct is ingesteld
   - Bij Together.ai: Controleer of je het juiste model ID gebruikt

## Volgende stappen

Na de installatie kun je de volgende aanpassingen doen:

- Pas de systeemboodschap aan in `frontend/app.js` om de persoonlijkheid van je assistent te wijzigen
- Experimenteer met verschillende providers en modellen in het dropdown menu
- Pas de UI aan door het wijzigen van `frontend/styles.css`
