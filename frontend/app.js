// Frontend JavaScript voor de AI-assistent

// API configuratie
const API_BASE_URL = 'http://localhost:5000/api';

// DOM elementen
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const modelSelect = document.getElementById('model-select');
const providerSelect = document.getElementById('provider-select');

// Geschiedenis van berichten voor de API 
let messageHistory = [
    {
        "role": "system",
        "content": "Je bent een behulpzame, vriendelijke en betrouwbare AI-assistent."
    },
    {
        "role": "assistant",
        "content": "Hallo! Ik ben je persoonlijke AI-assistent. Waar kan ik je mee helpen?"
    }
];

// Huidige provider
let currentProvider = 'openrouter';

// Event listeners
document.addEventListener('DOMContentLoaded', initialize);
sendButton.addEventListener('click', handleSendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
    }
});

// Wanneer de provider verandert, laad de beschikbare modellen
if (providerSelect) {
    providerSelect.addEventListener('change', (e) => {
        currentProvider = e.target.value;
        loadModels(currentProvider);
    });
}

// Initialisatie
async function initialize() {
    await loadProviders();
    await loadModels(currentProvider);
    userInput.focus();
}

// Laad beschikbare providers van de API
async function loadProviders() {
    try {
        if (!providerSelect) return; // Skip als er geen provider select element is
        
        const response = await fetch(`${API_BASE_URL}/providers`);
        const providers = await response.json();
        
        providerSelect.innerHTML = '';
        providers.forEach(provider => {
            if (provider.available) {
                const option = document.createElement('option');
                option.value = provider.id;
                option.textContent = provider.name;
                providerSelect.appendChild(option);
                
                // Sla de eerste beschikbare provider op als huidige
                if (!currentProvider && provider.available) {
                    currentProvider = provider.id;
                }
            }
        });
    } catch (error) {
        console.error('Fout bij het laden van providers:', error);
        // Fallback optie als de server niet bereikbaar is
        if (providerSelect) {
            providerSelect.innerHTML = '<option value="openrouter">OpenRouter</option>';
        }
    }
}

// Laad beschikbare modellen van de API
async function loadModels(provider = 'openrouter') {
    try {
        const response = await fetch(`${API_BASE_URL}/models?provider=${provider}`);
        const models = await response.json();
        
        modelSelect.innerHTML = '';
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.id;
            option.textContent = `${model.name}${model.free ? ' (gratis)' : ''}`;
            modelSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Fout bij het laden van modellen:', error);
        // Fallback optie als de server niet bereikbaar is
        if (provider === 'openrouter') {
            modelSelect.innerHTML = '<option value="openai/gpt-3.5-turbo">GPT-3.5 Turbo (gratis)</option>';
        } else {
            modelSelect.innerHTML = '<option value="mistralai/Mixtral-8x7B-Instruct-v0.1">Mixtral 8x7B (gratis)</option>';
        }
    }
}

// Verstuur een bericht naar de API
async function sendMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messageHistory,
                model: modelSelect.value,
                provider: currentProvider
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        const assistantMessage = data.choices[0].message.content;
        messageHistory.push({
            role: "assistant",
            content: assistantMessage
        });
        
        return assistantMessage;
    } catch (error) {
        console.error('Fout bij het versturen van bericht:', error);
        return `Er is een fout opgetreden bij het communiceren met de AI: ${error.message}`;
    }
}

// Handle het versturen van een bericht door de gebruiker
async function handleSendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Voeg het bericht toe aan de UI
    addMessageToUI('user', message);
    
    // Reset het invoerveld
    userInput.value = '';
    
    // Voeg het bericht toe aan de geschiedenis
    messageHistory.push({
        role: "user",
        content: message
    });
    
    // Toon een "bezig met typen" indicator
    const typingIndicator = addTypingIndicator();
    
    // Verstuur het bericht naar de API
    const response = await sendMessage(message);
    
    // Verwijder de typing indicator
    typingIndicator.remove();
    
    // Voeg het antwoord toe aan de UI
    addMessageToUI('assistant', response);
    
    // Scroll naar beneden
    scrollToBottom();
}

// Voeg een bericht toe aan de UI
function addMessageToUI(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Gebruik marked.js om Markdown te renderen
    messageContent.innerHTML = marked.parse(content);
    
    // Highlight code blocks met highlight.js
    messageContent.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

// Voeg een "bezig met typen" indicator toe
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant-message typing-indicator';
    typingDiv.innerHTML = '<div class="message-content">Aan het typen...</div>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv;
}

// Scroll naar de onderkant van het chatvenster
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Controleer connectie met de backend
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('Backend niet bereikbaar:', error);
        return false;
    }
}
