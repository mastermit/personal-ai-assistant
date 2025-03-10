# Configuratiehandleiding

Dit document beschrijft hoe je de verschillende onderdelen van je AI-assistent kunt configureren.

## API-configuratie

### Together.ai API

Het project gebruikt standaard de Together.ai API, die een gratis tier aanbiedt met toegang tot verschillende open-source modellen.

1. Bewerk het `.env` bestand in de backend map:

```
TOGETHER_API_KEY=jouw_api_sleutel_hier
PORT=5000
```

2. Je kunt de poort veranderen als poort 5000 al in gebruik is.

### Veranderen van standaard model

In `backend/server.py` kun je het standaardmodel wijzigen door de waarde van `model` in de payload aan te passen:

```python
payload = {
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Verander dit naar een ander model
    "messages": messages,
    "temperature": 0.7,
    "max_tokens": 1000
}
```

### Aanpassen van model parameters

Je kunt ook de parameters voor het model aanpassen:

- `temperature`: Hogere waarden (bijvoorbeeld 0.8) maken de output meer creatief/random, lagere waarden (bijvoorbeeld 0.2) maken de output meer deterministisch/gefocust.
- `max_tokens`: Het maximale aantal tokens dat de API in respons produceert.

## Frontend-configuratie

### Backend API URL aanpassen

Als je de backend draait op een andere server of poort, pas dan de `API_BASE_URL` aan in `frontend/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Systeemboodschap aanpassen

Om de persoonlijkheid of het gedrag van je assistent te veranderen, pas de systeemboodschap aan in `frontend/app.js`:

```javascript
let messageHistory = [
    {
        "role": "system",
        "content": "Je bent een behulpzame, vriendelijke en betrouwbare AI-assistent."
    },
    // ...
];
```

Je kunt de systeemboodschap aanpassen om specifieke instructies te geven over hoe de assistent moet reageren, welke toon te gebruiken, of om domeinspecifieke kennis te verstrekken.

### UI aanpassen

Om het uiterlijk van de UI aan te passen:

1. **Kleuren**: Pas de kleurschema's aan in `frontend/styles.css`
2. **Lettertypen**: Verander de `font-family` eigenschappen in het CSS bestand
3. **Lay-out**: Pas de structuur aan in `frontend/index.html`

## Uitbreidingsmogelijkheden

### Toevoegen van meer modellen

Om meer modellen toe te voegen, pas de `/api/models` functie aan in `backend/server.py`:

```python
@app.route('/api/models', methods=['GET'])
def get_models():
    models = [
        {"id": "mistralai/Mixtral-8x7B-Instruct-v0.1", "name": "Mixtral 8x7B", "provider": "Together.ai", "free": True},
        {"id": "meta-llama/Llama-2-7b-chat-hf", "name": "Llama 2 7B", "provider": "Together.ai", "free": True},
        {"id": "NousResearch/Nous-Hermes-2-Yi-34B", "name": "Nous Hermes 2 Yi 34B", "provider": "Together.ai", "free": True},
        # Voeg hier meer modellen toe
    ]
    
    return jsonify(models)
```

### Toevoegen van andere API providers

Om ondersteuning toe te voegen voor andere AI providers, zoals OpenAI of Anthropic (wat niet gratis is, maar als voorbeeld):

1. Pas de backend aan met een nieuwe route of logica voor de nieuwe provider
2. Voeg de juiste configuratieparameters toe in `.env`
3. Pas de frontend aan om ondersteuning te bieden voor de nieuwe provider

Bijvoorbeeld, om OpenAI toe te voegen:

```python
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Nieuwe route voor OpenAI
@app.route('/api/chat/openai', methods=['POST'])
def chat_openai():
    # Implementeer de logica hier
    pass
```
