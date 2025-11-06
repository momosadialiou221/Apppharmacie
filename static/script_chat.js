// JavaScript pour chat fluide Assistant Pharmacien

class ChatAssistant {
    constructor() {
        this.userLocation = null;
        this.conversationHistory = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.scrollToBottom();
        this.loadUserProfile();
    }
    
    loadUserProfile() {
        const profile = localStorage.getItem('pharmacyProfile');
        if (profile) {
            const data = JSON.parse(profile);
            document.getElementById('typePeau').value = data.typePeau || '';
            document.getElementById('age').value = data.age || '';
        }
    }
    
    saveUserProfile() {
        const profile = {
            typePeau: document.getElementById('typePeau').value,
            age: document.getElementById('age').value
        };
        localStorage.setItem('pharmacyProfile', JSON.stringify(profile));
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Sauvegarder le profil
        this.saveUserProfile();
        
        // Afficher le message utilisateur
        this.addUserMessage(message);
        input.value = '';
        
        // Désactiver le bouton d'envoi
        this.toggleSendButton(false);
        
        // Afficher l'indicateur de frappe
        this.showTypingIndicator();
        
        try {
            // Analyser le message pour extraire la durée des symptômes
            const symptomDuration = this.extractSymptomDuration(message);
            
            // Préparer les données
            const requestData = {
                probleme: message,
                type_peau: document.getElementById('typePeau').value,
                age: parseInt(document.getElementById('age').value) || 0,
                duree_symptomes: symptomDuration,
                localisation: this.userLocation
            };
            
            // Envoyer à l'API avec délai réaliste
            await this.delay(1000 + Math.random() * 1000); // 1-2 secondes
            
            const response = await fetch('/diagnostic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            // Masquer l'indicateur de frappe
            this.hideTypingIndicator();
            
            // Afficher la réponse
            this.addBotResponse(data, requestData);
            
            // Si localisation demandée, chercher pharmacies
            if (this.isLocationRequest(message) && this.userLocation) {
                await this.delay(500);
                this.showTypingIndicator();
                await this.delay(1000);
                this.hideTypingIndicator();
                await this.searchNearbyPharmacies();
            }
            
        } catch (error) {
            console.error('Erreur:', error);
            this.hideTypingIndicator();
            this.addBotMessage("Désolé, j'ai rencontré une erreur. Pouvez-vous reformuler votre question ?");
        } finally {
            this.toggleSendButton(true);
        }
    }
    
    extractSymptomDuration(message) {
        const message_lower = message.toLowerCase();
        
        // Patterns pour détecter la durée - LOGIQUE CORRIGÉE
        const patterns = [
            // Patterns avec nombres - ordre important (plus spécifique d'abord)
            { regex: /depuis\s+(\d+)\s+ans?/i, multiplier: 365 },
            { regex: /depuis\s+(\d+)\s+années?/i, multiplier: 365 },
            { regex: /il\s+y\s+a\s+(\d+)\s+ans?/i, multiplier: 365 },
            { regex: /(\d+)\s+ans?\s+que/i, multiplier: 365 },
            { regex: /depuis\s+(\d+)\s+mois/i, multiplier: 30 },
            { regex: /il\s+y\s+a\s+(\d+)\s+mois/i, multiplier: 30 },
            { regex: /(\d+)\s+mois\s+que/i, multiplier: 30 },
            { regex: /depuis\s+(\d+)\s+semaines?/i, multiplier: 7 },
            { regex: /il\s+y\s+a\s+(\d+)\s+semaines?/i, multiplier: 7 },
            { regex: /(\d+)\s+semaines?\s+que/i, multiplier: 7 },
            { regex: /depuis\s+(\d+)\s+jours?/i, multiplier: 1 },
            { regex: /il\s+y\s+a\s+(\d+)\s+jours?/i, multiplier: 1 },
            
            // Patterns textuels - estimations réalistes
            { regex: /depuis\s+toujours/i, days: 3650 }, // 10 ans
            { regex: /depuis\s+très\s+longtemps/i, days: 1095 }, // 3 ans
            { regex: /depuis\s+longtemps/i, days: 730 }, // 2 ans
            { regex: /depuis\s+l['']enfance/i, days: 5475 }, // 15 ans
            { regex: /depuis\s+l['']adolescence/i, days: 3650 }, // 10 ans
            { regex: /depuis\s+des\s+années/i, days: 1095 }, // 3 ans
            { regex: /depuis\s+des\s+mois/i, days: 180 }, // 6 mois
            { regex: /depuis\s+quelques\s+années/i, days: 730 }, // 2 ans
            { regex: /depuis\s+quelques\s+mois/i, days: 90 }, // 3 mois
            { regex: /depuis\s+quelques\s+semaines/i, days: 21 }, // 3 semaines
            { regex: /depuis\s+quelques\s+jours/i, days: 5 }, // 5 jours
            
            // Patterns saisonniers spécifiques au Sénégal
            { regex: /depuis\s+l['']harmattan/i, days: 60 }, // 2 mois
            { regex: /depuis\s+la\s+saison\s+sèche/i, days: 150 }, // 5 mois
            { regex: /depuis\s+l['']hivernage/i, days: 120 }, // 4 mois
            { regex: /depuis\s+la\s+saison\s+des\s+pluies/i, days: 120 }, // 4 mois
            { regex: /depuis\s+l['']hiver/i, days: 90 }, // 3 mois
            { regex: /depuis\s+l['']été/i, days: 90 }, // 3 mois
            
            // Patterns d'intensité temporelle
            { regex: /récemment/i, days: 10 },
            { regex: /dernièrement/i, days: 14 },
            { regex: /depuis\s+peu/i, days: 14 },
            { regex: /depuis\s+pas\s+longtemps/i, days: 21 },
            { regex: /ça\s+fait\s+un\s+moment/i, days: 60 },
            { regex: /ça\s+fait\s+longtemps/i, days: 180 },
            { regex: /chronique/i, days: 365 },
            { regex: /persistant/i, days: 90 }
        ];
        
        for (const pattern of patterns) {
            const match = message_lower.match(pattern.regex);
            if (match) {
                if (pattern.days) {
                    // Pattern textuel
                    return { 
                        jours: pattern.days, 
                        texte: match[0],
                        type: 'textuel',
                        estimation: true
                    };
                } else {
                    // Pattern numérique
                    const number = parseInt(match[1]);
                    const days = number * pattern.multiplier;
                    const unit = pattern.multiplier === 1 ? 'jours' : 
                                pattern.multiplier === 7 ? 'semaines' :
                                pattern.multiplier === 30 ? 'mois' : 'années';
                    return { 
                        jours: days, 
                        texte: match[0],
                        type: 'numerique',
                        valeur_originale: number,
                        unite: unit
                    };
                }
            }
        }
        
        return null;
    }
    
    isLocationRequest(message) {
        const locationKeywords = ['pharmacie', 'où', 'proche', 'près', 'trouver', 'acheter', 'adresse'];
        return locationKeywords.some(keyword => message.toLowerCase().includes(keyword));
    }
    
    addUserMessage(message) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                ${this.escapeHtml(message)}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addBotResponse(data, requestData) {
        let response = this.generateIntelligentResponse(data, requestData);
        
        // Ajouter les conseils
        if (data.conseils && data.conseils.length > 0) {
            response += '<br><br><strong>💡 Mes conseils personnalisés :</strong><ul>';
            data.conseils.forEach(conseil => {
                response += `<li>${conseil}</li>`;
            });
            response += '</ul>';
        }
        
        this.addBotMessage(response);
        
        // Ajouter les produits recommandés
        if (data.produits_recommandes && data.produits_recommandes.length > 0) {
            this.addProductRecommendations(data.produits_recommandes);
        }
    }
    
    generateIntelligentResponse(data, requestData) {
        let response = "";
        
        // Accusé de réception personnalisé avec durée corrigée
        if (requestData.duree_symptomes) {
            const duration = requestData.duree_symptomes;
            const jours = duration.jours || 0;
            const texte = duration.texte || '';
            
            if (jours <= 14) {
                response += `🕐 Je vois que c'est un problème récent (${texte}). `;
                response += "Commençons par des soins doux pour ne pas aggraver la situation. ";
            } else if (jours <= 90) {
                response += `📅 Ce problème persiste ${texte}, il mérite une attention particulière. `;
                response += "Une routine ciblée devrait vous aider. ";
            } else if (jours <= 365) {
                response += `⏰ Problème installé ${texte} - une approche méthodique sera nécessaire. `;
                response += "La patience et la constance seront vos alliées. ";
            } else {
                response += `🏥 Problème chronique ${texte} - je recommande vivement de consulter un dermatologue. `;
                response += "Les problèmes anciens nécessitent souvent un suivi professionnel. ";
            }
        }
        
        // Analyse du problème avec conseils contextuels
        const probleme = requestData.probleme.toLowerCase();
        const age = requestData.age || 25;
        
        if (probleme.includes('acné') || probleme.includes('bouton')) {
            if (age < 20) {
                response += "L'acné juvénile est très courante et se traite bien avec patience. ";
            } else if (age >= 25) {
                response += "L'acné adulte est souvent liée au stress et aux hormones. ";
            } else {
                response += "L'acné peut avoir plusieurs causes selon votre profil. ";
            }
        } else if (probleme.includes('sèche') || probleme.includes('tiraille') || probleme.includes('déshydrat')) {
            response += "La peau sèche nécessite une hydratation adaptée et régulière. ";
            if (probleme.includes('hiver') || probleme.includes('harmattan')) {
                response += "La saison sèche aggrave particulièrement ce problème au Sénégal. ";
            }
        } else if (probleme.includes('tache') || probleme.includes('pigment') || probleme.includes('melasma')) {
            response += "Les taches pigmentaires demandent patience et protection solaire rigoureuse. ";
            if (age > 40) {
                response += "À votre âge, des soins professionnels peuvent être envisagés. ";
            }
        } else if (probleme.includes('sensible') || probleme.includes('irrité') || probleme.includes('rouge')) {
            response += "La peau sensible nécessite des soins très doux et une approche progressive. ";
        } else if (probleme.includes('ride') || probleme.includes('anti-âge')) {
            if (age < 30) {
                response += "La prévention anti-âge commence par une bonne protection solaire. ";
            } else {
                response += "Les soins anti-âge sont plus efficaces quand ils sont adaptés à votre âge. ";
            }
        }
        
        // Recommandations selon le type de peau - améliorées
        if (requestData.type_peau) {
            response += `Avec votre peau ${requestData.type_peau}, `;
            switch (requestData.type_peau) {
                case 'grasse':
                    response += "privilégiez des textures légères (gels, sérums) et évitez les huiles lourdes. ";
                    break;
                case 'seche':
                    response += "optez pour des soins riches (crèmes, baumes) et hydratez matin et soir. ";
                    break;
                case 'sensible':
                    response += "choisissez des produits hypoallergéniques et testez toujours sur une petite zone. ";
                    break;
                case 'mixte':
                    response += "adaptez vos soins : zone T (textures légères) et joues (plus nourrissantes). ";
                    break;
                case 'normale':
                    response += "maintenez l'équilibre avec des soins adaptés aux saisons. ";
                    break;
            }
        }
        
        // Conseils selon l'âge
        if (age < 20) {
            response += "À votre âge, une routine simple et régulière est la clé. ";
        } else if (age >= 40) {
            response += "Votre peau mature mérite des soins ciblés et de qualité. ";
        }
        
        response += "Voici mes recommandations personnalisées :";
        
        return response;
    }
    
    addBotMessage(message) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="message-content">
                ${message}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addProductRecommendations(produits) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        let content = '<strong>💊 Produits que je vous recommande :</strong><br><br>';
        
        produits.slice(0, 4).forEach(produit => {
            const prix = produit.prix_min && produit.prix_max ? 
                `${produit.prix_min} - ${produit.prix_max} FCFA` : 
                'Prix à vérifier';
                
            content += `
                <div class="product-card">
                    <strong>${produit.nom}</strong><br>
                    <small class="text-muted">${produit.marque || 'Marque non spécifiée'}</small><br>
                    <span class="text-success fw-bold">${prix}</span><br>
                    ${produit.description ? `<small>${produit.description}</small>` : ''}
                </div>
            `;
        });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="message-content">
                ${content}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    async searchNearbyPharmacies() {
        if (!this.userLocation) return;
        
        try {
            const response = await fetch('/pharmacies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    latitude: this.userLocation.latitude,
                    longitude: this.userLocation.longitude,
                    rayon: 10,
                    h24_seulement: false
                })
            });
            
            const data = await response.json();
            
            if (data.pharmacies && data.pharmacies.length > 0) {
                // Limiter aux 5 plus proches
                const pharmaciesProches = data.pharmacies.slice(0, 5);
                this.addPharmacyRecommendations(pharmaciesProches);
            } else {
                this.addBotMessage("Je n'ai pas trouvé de pharmacies dans votre zone. Essayez d'élargir la recherche ou vérifiez votre position.");
            }
            
        } catch (error) {
            console.error('Erreur recherche pharmacies:', error);
        }
    }
    
    addPharmacyRecommendations(pharmacies) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        let content = `<strong>🏥 Les 5 pharmacies les plus proches de vous :</strong><br><br>`;
        
        pharmacies.forEach((pharmacie, index) => {
            const h24Badge = pharmacie.ouvert_24h ? ' <span class="badge bg-success">24h/24</span>' : '';
            const distance = pharmacie.distance ? ` (${pharmacie.distance} km)` : '';
            
            content += `
                <div class="pharmacy-card ${pharmacie.ouvert_24h ? 'h24' : ''}">
                    <strong>${index + 1}. ${pharmacie.nom}</strong>${h24Badge}<br>
                    <small class="text-muted">📍 ${pharmacie.adresse}${distance}</small><br>
                    ${pharmacie.telephone ? `<small>📞 ${pharmacie.telephone}</small><br>` : ''}
                    ${pharmacie.horaires ? `<small>🕒 ${pharmacie.horaires}</small>` : ''}
                </div>
            `;
        });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="message-content">
                ${content}
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        document.getElementById('typingIndicator').style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        document.getElementById('typingIndicator').style.display = 'none';
    }
    
    toggleSendButton(enabled) {
        const btn = document.getElementById('sendBtn');
        btn.disabled = !enabled;
    }
    
    async obtenirLocalisation() {
        const statusDiv = document.getElementById('locationStatus');
        
        if (!navigator.geolocation) {
            statusDiv.innerHTML = '<i class="fas fa-times text-danger"></i> Géolocalisation non supportée';
            return;
        }
        
        statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Localisation en cours...';
        
        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 300000
                });
            });
            
            this.userLocation = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            
            statusDiv.innerHTML = '<i class="fas fa-check text-success"></i> Position obtenue';
            
            // Message automatique
            setTimeout(() => {
                this.addBotMessage("📍 J'ai obtenu votre position ! Je peux maintenant vous indiquer les pharmacies les plus proches quand vous en aurez besoin.");
            }, 500);
            
        } catch (error) {
            console.error('Erreur géolocalisation:', error);
            statusDiv.innerHTML = '<i class="fas fa-times text-danger"></i> Erreur de localisation';
        }
    }
    
    sendQuickMessage(message) {
        document.getElementById('chatInput').value = message;
        this.sendMessage();
    }
    
    clearChat() {
        if (confirm('Effacer toute la conversation ?')) {
            const messagesContainer = document.getElementById('chatMessages');
            // Garder seulement le message de bienvenue
            const welcomeMessage = messagesContainer.querySelector('.bot-message');
            messagesContainer.innerHTML = '';
            if (welcomeMessage) {
                messagesContainer.appendChild(welcomeMessage);
            }
            this.conversationHistory = [];
        }
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Fonctions globales
let chatAssistant;

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        chatAssistant.sendMessage();
    }
}

function sendMessage() {
    chatAssistant.sendMessage();
}

function sendQuickMessage(message) {
    chatAssistant.sendQuickMessage(message);
}

function obtenirLocalisation() {
    chatAssistant.obtenirLocalisation();
}

function clearChat() {
    chatAssistant.clearChat();
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    chatAssistant = new ChatAssistant();
});