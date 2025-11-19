// Chat Widget
const chatButton = document.getElementById('chatButton');
const chatWidget = document.getElementById('chatWidget');
const chatClose = document.getElementById('chatClose');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');
const chatMessages = document.getElementById('chatMessages');
const chatBadge = document.querySelector('.chat-badge');

let sessionId = Date.now().toString();

// Toggle chat
chatButton.addEventListener('click', () => {
    chatWidget.classList.add('active');
    chatButton.style.display = 'none';
    chatInput.focus();
    // Cacher le badge
    if (chatBadge) chatBadge.style.display = 'none';
});

chatClose.addEventListener('click', () => {
    chatWidget.classList.remove('active');
    chatButton.style.display = 'flex';
});

// Envoyer message
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Afficher message utilisateur
    addMessage(message, 'user');
    chatInput.value = '';
    
    // Afficher "typing..."
    const typingDiv = addMessage('🤖 Réflexion en cours...', 'bot', 'typing');
    
    // Envoyer au serveur
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            profile: getUserProfile(),
            session_id: sessionId
        })
    })
    .then(response => response.json())
    .then(data => {
        // Retirer "typing..."
        typingDiv.remove();
        
        // Afficher réponse
        let response = data.message;
        
        if (data.produits && data.produits.length > 0) {
            response += '\n\n💊 Produits recommandés:\n';
            data.produits.slice(0, 3).forEach((p, i) => {
                const prix = p.prix_min ? `${p.prix_min}-${p.prix_max} FCFA` : 'Prix variable';
                response += `\n${i + 1}. ${p.nom} (${p.marque})\n   💰 ${prix}`;
            });
            response += '\n\n📋 Consultez la page Produits pour plus de détails!';
        }
        
        addMessage(response, 'bot');
    })
    .catch(error => {
        typingDiv.remove();
        addMessage('❌ Désolé, une erreur est survenue. Veuillez réessayer.', 'bot');
        console.error('Error:', error);
    });
}

chatSend.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function addMessage(text, sender, id = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    if (id) messageDiv.id = id;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

function getUserProfile() {
    // Récupérer le profil depuis localStorage ou valeurs par défaut
    return {
        age: localStorage.getItem('user_age') || 25,
        type_peau: localStorage.getItem('user_type_peau') || '',
        budget_max: localStorage.getItem('user_budget_max') || null
    };
}

// Charger les statistiques
fetch('/api/stats')
    .then(response => response.json())
    .then(data => {
        document.getElementById('total-produits').textContent = data.total_produits + '+';
        document.getElementById('total-pharmacies').textContent = data.total_pharmacies + '+';
        document.getElementById('pharmacies-24h').textContent = data.pharmacies_24h + '+';
    })
    .catch(error => console.error('Error loading stats:', error));

// Charger les produits populaires
fetch('/produits?page=1')
    .then(response => response.text())
    .then(html => {
        // Parser le HTML pour extraire les produits
        // Pour simplifier, on va faire une requête API dédiée
    })
    .catch(error => console.error('Error loading products:', error));
