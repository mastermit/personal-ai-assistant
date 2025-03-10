from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
from dotenv import load_dotenv

# Laad omgevingsvariabelen
load_dotenv()

app = Flask(__name__)
CORS(app)  # Sta cross-origin requests toe

# API endpoints
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# API-sleutels
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Standaard API provider
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openrouter")

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint voor de chatfunctionaliteit.
    Verwacht een JSON met 'messages' array in het formaat dat de API verwacht.
    """
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', "")
        provider = data.get('provider', DEFAULT_PROVIDER)
        
        if provider == "together" and TOGETHER_API_KEY:
            return chat_together(messages, model)
        elif provider == "openrouter" and OPENROUTER_API_KEY:
            return chat_openrouter(messages, model)
        else:
            # Fallback naar beschikbare provider
            if OPENROUTER_API_KEY:
                return chat_openrouter(messages, model)
            elif TOGETHER_API_KEY:
                return chat_together(messages, model)
            else:
                return jsonify({"error": "Geen API-sleutels geconfigureerd"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def chat_together(messages, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    """
    Verstuur een verzoek naar de Together.ai API
    """
    # Basis configuratie voor het model
    payload = {
        "model": model or "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Standaard model
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOGETHER_API_KEY}"
    }
    
    # Maak het verzoek naar de Together API
    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({"error": f"Together API fout: {response.status_code}", "details": response.text}), 500

def chat_openrouter(messages, model="openai/gpt-3.5-turbo"):
    """
    Verstuur een verzoek naar de OpenRouter API
    """
    # Basis configuratie voor het model
    payload = {
        "model": model or "openai/gpt-3.5-turbo",  # Standaard model als geen is opgegeven
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",  # Verplicht voor OpenRouter
        "X-Title": "Persoonlijke AI-assistent"  # Optionele titel voor je app
    }
    
    # Maak het verzoek naar de OpenRouter API
    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({"error": f"OpenRouter API fout: {response.status_code}", "details": response.text}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Geeft een lijst terug van beschikbare modellen.
    """
    provider = request.args.get('provider', DEFAULT_PROVIDER)
    
    if provider == "together":
        models = [
            {"id": "mistralai/Mixtral-8x7B-Instruct-v0.1", "name": "Mixtral 8x7B", "provider": "Together.ai", "free": True},
            {"id": "meta-llama/Llama-2-7b-chat-hf", "name": "Llama 2 7B", "provider": "Together.ai", "free": True},
            {"id": "NousResearch/Nous-Hermes-2-Yi-34B", "name": "Nous Hermes 2 Yi 34B", "provider": "Together.ai", "free": True}
        ]
    else:  # openrouter als standaard
        models = [
            {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenRouter", "free": True},
            {"id": "google/gemma-7b-it", "name": "Gemma 7B", "provider": "OpenRouter", "free": True},
            {"id": "anthropic/claude-instant-v1", "name": "Claude Instant", "provider": "OpenRouter", "free": True},
            {"id": "mistralai/mistral-7b-instruct", "name": "Mistral 7B", "provider": "OpenRouter", "free": True}
        ]
    
    return jsonify(models)

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """
    Geeft een lijst terug van beschikbare providers.
    """
    providers = []
    
    if OPENROUTER_API_KEY:
        providers.append({"id": "openrouter", "name": "OpenRouter", "available": True})
    else:
        providers.append({"id": "openrouter", "name": "OpenRouter", "available": False})
    
    if TOGETHER_API_KEY:
        providers.append({"id": "together", "name": "Together.ai", "available": True})
    else:
        providers.append({"id": "together", "name": "Together.ai", "available": False})
    
    return jsonify(providers)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Eenvoudige health check om te controleren of de server draait.
    """
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
