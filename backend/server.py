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

# Standaard API endpoint en key
DEFAULT_API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = os.getenv("TOGETHER_API_KEY", "")

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint voor de chatfunctionaliteit.
    Verwacht een JSON met 'messages' array in het formaat dat de Together API verwacht.
    """
    try:
        data = request.json
        messages = data.get('messages', [])
        
        # Basis configuratie voor het model
        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Standaard model (gratis tier)
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Maak het verzoek naar de Together API
        response = requests.post(DEFAULT_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({"error": f"API fout: {response.status_code}", "details": response.text}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Geeft een lijst terug van beschikbare modellen.
    Voor nu een hardcoded lijst van gratis/goedkope modellen.
    """
    models = [
        {"id": "mistralai/Mixtral-8x7B-Instruct-v0.1", "name": "Mixtral 8x7B", "provider": "Together.ai", "free": True},
        {"id": "meta-llama/Llama-2-7b-chat-hf", "name": "Llama 2 7B", "provider": "Together.ai", "free": True},
        {"id": "NousResearch/Nous-Hermes-2-Yi-34B", "name": "Nous Hermes 2 Yi 34B", "provider": "Together.ai", "free": True}
    ]
    
    return jsonify(models)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Eenvoudige health check om te controleren of de server draait.
    """
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
