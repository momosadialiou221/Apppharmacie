#!/usr/bin/env python3
"""
Assistant Pharmacien Sénégal - Version Chat Fluide avec Analyse Avancée
Interface conversationnelle comme ChatGPT avec diagnostic amélioré et IA
"""

import sqlite3
import json
import math
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

# Import des modules avancés
try:
    from advanced_analysis import AdvancedNeedsAnalyzer
    ADVANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ADVANCED_ANALYSIS_AVAILABLE = False
    print("⚠️  Module d'analyse avancée non disponible")

class ChatPharmacyHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialiser l'analyseur avancé si disponible
        if ADVANCED_ANALYSIS_AVAILABLE:
            self.advanced_analyzer = AdvancedNeedsAnalyzer()
        else:
            self.advanced_analyzer = None
        super().__init__(*args, **kwargs)
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Lire le template chat
            try:
                with open('templates/index_chat.html', 'r', encoding='utf-8') as f:
                    html = f.read()
                # Remplacer les URLs Flask par des chemins statiques
                html = html.replace("{{ url_for('static', filename='script_chat.js') }}", '/static/script_chat.js')
                self.wfile.write(html.encode('utf-8'))
            except FileNotFoundError:
                self.send_basic_interface()
                
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        elif self.path == '/diagnostic':
            self.handle_diagnostic()
        elif self.path == '/pharmacies':
            self.handle_pharmacies()
    
    def do_POST(self):
        if self.path == '/diagnostic':
            self.handle_diagnostic()
        elif self.path == '/pharmacies':
            self.handle_pharmacies()
    
    def serve_static_file(self):
        try:
            file_path = self.path[1:]  # Remove leading '/'
            if file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', f'{content_type}; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
    
    def send_basic_interface(self):
        """Interface de base si le template n'est pas trouvé"""
        html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Assistant Pharmacien Chat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chat { max-width: 800px; margin: 0 auto; }
        .message { margin: 10px 0; padding: 10px; border-radius: 10px; }
        .user { background: #007bff; color: white; text-align: right; }
        .bot { background: #f1f1f1; }
        #input { width: 70%; padding: 10px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <div class="chat">
        <h1>🏥 Assistant Pharmacien Sénégal</h1>
        <div id="messages">
            <div class="message bot">
                Bonjour ! Décrivez votre problème de peau et depuis combien de temps vous l'avez.
            </div>
        </div>
        <div>
            <input type="text" id="input" placeholder="Ex: J'ai de l'acné depuis 2 semaines">
            <button onclick="sendMessage()">Envoyer</button>
        </div>
    </div>
    <script>
        function sendMessage() {
            const input = document.getElementById('input');
            const message = input.value.trim();
            if (!message) return;
            
            // Afficher message utilisateur
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML += '<div class="message user">' + message + '</div>';
            input.value = '';
            
            // Envoyer à l'API
            fetch('/diagnostic', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({probleme: message})
            })
            .then(response => response.json())
            .then(data => {
                let response = 'Voici mes recommandations :<br>';
                if (data.produits_recommandes) {
                    data.produits_recommandes.forEach(p => {
                        response += '• ' + p.nom + ' (' + p.marque + ')<br>';
                    });
                }
                messagesDiv.innerHTML += '<div class="message bot">' + response + '</div>';
            });
        }
        
        document.getElementById('input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def handle_diagnostic(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        probleme = data.get('probleme', '')
        type_peau = data.get('type_peau', '')
        age = data.get('age', 0)
        duree_symptomes = data.get('duree_symptomes')
        localisation = data.get('localisation')
        
        # Utiliser l'analyse avancée si disponible
        if self.advanced_analyzer and ADVANCED_ANALYSIS_AVAILABLE:
            context = {
                'age': age,
                'type_peau': type_peau,
                'localisation': localisation
            }
            
            # Analyse avancée des besoins
            analysis = self.advanced_analyzer.analyze_user_needs(probleme, context)
            
            # Recommandations avancées
            produits_list = self.advanced_analyzer.get_advanced_recommendations(analysis, limit=8)
            
            # Conseils personnalisés avancés
            conseils = self.advanced_analyzer.generate_personalized_advice(analysis)
            
            response = {
                'produits_recommandes': produits_list,
                'conseils': conseils,
                'duree_detectee': duree_symptomes,
                'analysis_advanced': {
                    'primary_needs': analysis['primary_needs'],
                    'behavior_pattern': analysis['behavior_pattern'],
                    'confidence_score': analysis['confidence_score'],
                    'budget_indication': analysis['budget_indication'],
                    'experience_level': analysis['experience_level']
                },
                'response_type': 'advanced'
            }
        else:
            # Fallback vers analyse basique
            probleme_lower = probleme.lower()
            
            # Extraire la durée des symptômes du texte si pas fournie
            if not duree_symptomes:
                duree_symptomes = self.extract_symptom_duration(probleme_lower)
            
            # Recherche dans la base de données
            conn = sqlite3.connect('pharmacy_assistant.db')
            conn.row_factory = sqlite3.Row
            
            # Recherche intelligente avec plusieurs mots-clés
            search_terms = self.extract_skin_problems(probleme_lower)
            
            if search_terms:
                placeholders = ' OR '.join(['problemes_cibles LIKE ?' for _ in search_terms])
                query = f'SELECT * FROM produits WHERE {placeholders} ORDER BY prix_min ASC LIMIT 6'
                params = [f'%{term}%' for term in search_terms]
            else:
                query = 'SELECT * FROM produits WHERE problemes_cibles LIKE ? ORDER BY prix_min ASC LIMIT 6'
                params = [f'%{probleme_lower}%']
            
            produits = conn.execute(query, params).fetchall()
            conn.close()
            
            produits_list = [dict(p) for p in produits]
            conseils = self.generer_conseils_avances(probleme_lower, type_peau, age, duree_symptomes)
            
            response = {
                'produits_recommandes': produits_list,
                'conseils': conseils,
                'duree_detectee': duree_symptomes,
                'response_type': 'basic'
            }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def extract_skin_problems(self, text):
        """Extrait les problèmes de peau du texte"""
        problems = []
        
        # Dictionnaire des synonymes
        synonyms = {
            'acné': ['acné', 'acne', 'bouton', 'boutons', 'pustule', 'comédon', 'point noir'],
            'sèche': ['sèche', 'seche', 'sécheresse', 'tiraille', 'déshydrat', 'rugueuse'],
            'taches': ['tache', 'taches', 'pigment', 'melasma', 'hyperpigmentation', 'brun'],
            'sensible': ['sensible', 'irrité', 'rouge', 'rougeur', 'démangeaison', 'pique'],
            'rides': ['ride', 'rides', 'ridule', 'vieillissement', 'anti-âge', 'fermeté'],
            'grasse': ['grasse', 'brillant', 'sébum', 'huileux', 'pores']
        }
        
        for problem, terms in synonyms.items():
            if any(term in text for term in terms):
                problems.append(problem)
        
        return problems
    
    def extract_symptom_duration(self, text):
        """Extrait la durée des symptômes du texte avec logique améliorée"""
        patterns = [
            # Patterns avec nombres
            (r'depuis\s+(\d+)\s+ans?', lambda x: int(x) * 365),
            (r'depuis\s+(\d+)\s+années?', lambda x: int(x) * 365),
            (r'il\s+y\s+a\s+(\d+)\s+ans?', lambda x: int(x) * 365),
            (r'(\d+)\s+ans?\s+que', lambda x: int(x) * 365),
            (r'depuis\s+(\d+)\s+mois', lambda x: int(x) * 30),
            (r'il\s+y\s+a\s+(\d+)\s+mois', lambda x: int(x) * 30),
            (r'(\d+)\s+mois\s+que', lambda x: int(x) * 30),
            (r'depuis\s+(\d+)\s+semaines?', lambda x: int(x) * 7),
            (r'il\s+y\s+a\s+(\d+)\s+semaines?', lambda x: int(x) * 7),
            (r'(\d+)\s+semaines?\s+que', lambda x: int(x) * 7),
            (r'depuis\s+(\d+)\s+jours?', lambda x: int(x)),
            (r'il\s+y\s+a\s+(\d+)\s+jours?', lambda x: int(x)),
            (r'(\d+)\s+jours?\s+que', lambda x: int(x)),
            
            # Patterns textuels
            (r'depuis\s+toujours', lambda x: 365 * 10),  # 10 ans pour "toujours"
            (r'depuis\s+très\s+longtemps', lambda x: 365 * 3),  # 3 ans
            (r'depuis\s+longtemps', lambda x: 365 * 2),  # 2 ans
            (r'depuis\s+l\'enfance', lambda x: 365 * 15),  # 15 ans
            (r'depuis\s+l\'adolescence', lambda x: 365 * 10),  # 10 ans
            (r'depuis\s+des\s+années', lambda x: 365 * 3),  # 3 ans
            (r'depuis\s+des\s+mois', lambda x: 180),  # 6 mois
            (r'depuis\s+quelques\s+années', lambda x: 365 * 2),  # 2 ans
            (r'depuis\s+quelques\s+mois', lambda x: 90),  # 3 mois
            (r'depuis\s+quelques\s+semaines', lambda x: 21),  # 3 semaines
            (r'depuis\s+quelques\s+jours', lambda x: 5),  # 5 jours
            
            # Patterns saisonniers
            (r'depuis\s+l\'hiver', lambda x: 120),  # 4 mois
            (r'depuis\s+l\'été', lambda x: 90),  # 3 mois
            (r'depuis\s+l\'harmattan', lambda x: 60),  # 2 mois
            (r'depuis\s+la\s+saison\s+sèche', lambda x: 150),  # 5 mois
            (r'depuis\s+la\s+saison\s+des\s+pluies', lambda x: 120),  # 4 mois
            
            # Patterns d'intensité temporelle
            (r'récemment', lambda x: 10),  # 10 jours
            (r'dernièrement', lambda x: 14),  # 2 semaines
            (r'depuis\s+peu', lambda x: 14),  # 2 semaines
            (r'depuis\s+pas\s+longtemps', lambda x: 21),  # 3 semaines
            (r'ça\s+fait\s+un\s+moment', lambda x: 60),  # 2 mois
            (r'ça\s+fait\s+longtemps', lambda x: 180),  # 6 mois
            (r'chronique', lambda x: 365),  # 1 an
            (r'persistant', lambda x: 90),  # 3 mois
        ]
        
        for pattern, converter in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if match.groups():
                    # Pattern avec nombre
                    jours = converter(match.group(1))
                    return {
                        'jours': jours, 
                        'texte': match.group(0),
                        'type': 'numerique',
                        'valeur_originale': match.group(1)
                    }
                else:
                    # Pattern textuel
                    jours = converter(None)
                    return {
                        'jours': jours, 
                        'texte': match.group(0),
                        'type': 'textuel',
                        'estimation': True
                    }
        
        return None
    
    def generer_conseils_avances(self, probleme, type_peau, age, duree_symptomes):
        """Génère des conseils avancés et personnalisés selon le contexte"""
        conseils = []
        
        # Conseils selon la durée - LOGIQUE CORRIGÉE ET AMÉLIORÉE
        if duree_symptomes:
            jours = duree_symptomes.get('jours', 0)
            texte_duree = duree_symptomes.get('texte', '')
            
            # Catégorisation précise selon la durée
            if jours <= 7:  # Moins d'1 semaine
                conseils.append("🕐 Problème très récent : Observez d'abord l'évolution naturelle")
                conseils.append("⚠️ Évitez de multiplier les produits - laissez votre peau respirer")
                conseils.append("💧 Hydratation douce et protection solaire suffisent pour commencer")
            elif jours <= 21:  # 1 à 3 semaines
                conseils.append("📅 Problème récent : Commencez une routine douce et progressive")
                conseils.append("⏳ Patience - laissez 4-6 semaines pour voir les premiers résultats")
                conseils.append("🎯 Un seul produit actif à la fois pour identifier ce qui fonctionne")
            elif jours <= 90:  # 3 semaines à 3 mois
                conseils.append("⏰ Problème persistant : Il est temps d'adopter une routine plus ciblée")
                conseils.append("🔄 Évaluez ce que vous avez déjà essayé - qu'est-ce qui a marché ?")
                conseils.append("💪 Soyez régulier dans l'application - la constance est clé")
            elif jours <= 365:  # 3 mois à 1 an
                conseils.append("📋 Problème installé : Une approche méthodique s'impose")
                conseils.append("🔬 Peut-être temps de consulter pour identifier les causes profondes")
                conseils.append("📊 Tenez un journal de vos soins pour optimiser votre routine")
            elif jours <= 1095:  # 1 à 3 ans
                conseils.append("🏥 Problème chronique : Consultation dermatologique fortement recommandée")
                conseils.append("💡 Les causes peuvent être internes (hormones, alimentation, stress)")
                conseils.append("🎯 Approche globale nécessaire : soins + hygiène de vie")
            else:  # Plus de 3 ans
                conseils.append("🩺 Problème ancien : Suivi médical spécialisé indispensable")
                conseils.append("💪 Ne perdez pas espoir - même les problèmes anciens peuvent s'améliorer")
                conseils.append("🔄 Remise à plat complète de votre approche avec un professionnel")
                conseils.append("📚 Éducation thérapeutique pour comprendre votre peau")
        
        # Conseils selon le problème - AMÉLIORÉS ET PERSONNALISÉS
        if 'acné' in probleme or 'bouton' in probleme:
            if age and age < 20:
                conseils.extend([
                    "🧴 Routine simple : Nettoyant doux matin et soir + hydratant léger",
                    "🚫 Évitez de toucher votre visage - vos mains portent des bactéries",
                    "🧼 Changez vos taies d'oreiller 2 fois par semaine",
                    "⚠️ Si l'acné est sévère, consultez rapidement pour éviter les cicatrices"
                ])
            elif age and 20 <= age <= 30:
                conseils.extend([
                    "💊 Acné adulte : Souvent liée au stress et aux hormones",
                    "🧴 Utilisez des produits avec acide salicylique (BHA) le soir",
                    "☀️ Protection solaire obligatoire si vous utilisez des actifs",
                    "🍎 Surveillez votre alimentation - limitez les produits laitiers et sucrés"
                ])
            else:
                conseils.extend([
                    "🔬 Acné tardive : Consultez pour identifier les causes hormonales",
                    "💧 Hydratez même une peau acnéique - choisissez des textures légères",
                    "🎯 Traitements ciblés sur les boutons plutôt que sur tout le visage"
                ])
        
        if 'sèche' in probleme or 'tiraille' in probleme or 'déshydrat' in probleme:
            conseils.extend([
                "💧 Hydratation immédiate : Appliquez votre crème sur peau encore humide",
                "🚿 Douches tièdes (pas chaudes) et limitées à 5-10 minutes",
                "💦 Buvez 1,5-2L d'eau par jour - la peau se nourrit de l'intérieur",
                "🏠 Utilisez un humidificateur, surtout en saison sèche (Harmattan)"
            ])
            
            if 'hiver' in probleme or 'harmattan' in probleme:
                conseils.extend([
                    "❄️ Saison sèche : Renforcez votre routine avec des soins plus riches",
                    "🧴 Ajoutez une huile végétale (argan, jojoba) le soir",
                    "🧣 Protégez votre peau du vent avec une écharpe"
                ])
            
            if type_peau == 'sensible':
                conseils.append("🌿 Privilégiez les produits sans parfum et hypoallergéniques")
        
        if 'tache' in probleme or 'pigment' in probleme or 'melasma' in probleme:
            conseils.extend([
                "☀️ Protection solaire SPF 30+ TOUS LES JOURS - même en intérieur !",
                "🌙 Soins éclaircissants uniquement le soir (photosensibilisants)",
                "⏳ Patience requise : 3-6 mois minimum pour voir des résultats",
                "👒 Portez chapeau et lunettes de soleil en extérieur"
            ])
            
            if age and age > 40:
                conseils.extend([
                    "🔬 Taches de maturité : Considérez des soins professionnels (peeling)",
                    "💊 Vitamine C le matin + rétinol le soir (en alternance au début)"
                ])
            
            if 'melasma' in probleme:
                conseils.extend([
                    "🤰 Melasma souvent hormonal - consultez un dermatologue",
                    "💊 Évitez les contraceptifs hormonaux si possible",
                    "🧴 Produits avec hydroquinone, arbutine ou kojic acid"
                ])
        
        if 'sensible' in probleme or 'irrité' in probleme or 'rouge' in probleme:
            conseils.extend([
                "🧪 Test patch obligatoire : Testez tout nouveau produit sur l'avant-bras",
                "🌿 Ingrédients apaisants : Aloe vera, camomille, eau thermale",
                "🚫 Évitez : Parfums, alcool, huiles essentielles, gommages",
                "❄️ Compresses d'eau thermale froide pour calmer les irritations"
            ])
        
        if 'ride' in probleme or 'ridule' in probleme or 'anti-âge' in probleme:
            if age and age < 30:
                conseils.extend([
                    "🛡️ Prévention avant tout : Protection solaire et hydratation",
                    "💧 Acide hyaluronique pour maintenir l'hydratation",
                    "🍇 Antioxydants (vitamine C) pour protéger du vieillissement"
                ])
            elif age and 30 <= age <= 45:
                conseils.extend([
                    "🔄 Commencez les actifs anti-âge : Rétinol progressivement",
                    "💊 Routine complète : Vitamine C matin + Rétinol soir",
                    "💆 Massages du visage pour stimuler la circulation"
                ])
            else:
                conseils.extend([
                    "🎯 Soins intensifs : Sérums concentrés et crèmes riches",
                    "🏥 Considérez les soins professionnels (injections, lasers)",
                    "💪 Constance essentielle - les résultats prennent du temps"
                ])
        
        # Conseils selon l'âge - PLUS SPÉCIFIQUES
        if age:
            if age < 18:
                conseils.extend([
                    "👶 Peau jeune : Routine simple et produits doux",
                    "🚫 Évitez les actifs puissants (rétinol, acides forts)",
                    "📚 Apprenez les bons gestes dès maintenant"
                ])
            elif 18 <= age < 25:
                conseils.extend([
                    "🎓 Âge des premiers soins : Établissez une routine de base",
                    "💧 Hydratation + Protection solaire = Base essentielle",
                    "⚠️ Attention au stress des études qui peut aggraver l'acné"
                ])
            elif 25 <= age < 35:
                conseils.extend([
                    "💼 Vie active : Adaptez vos soins à votre rythme",
                    "🛡️ Commencez la prévention anti-âge",
                    "😴 Soins de nuit plus riches pour récupérer"
                ])
            elif 35 <= age < 50:
                conseils.extend([
                    "🔄 Changements hormonaux : Adaptez votre routine",
                    "💊 Intégrez des actifs anti-âge efficaces",
                    "🏥 Bilans dermatologiques annuels recommandés"
                ])
            else:
                conseils.extend([
                    "👑 Peau mature : Soins riches et nourrissants",
                    "🎯 Ciblez fermeté et confort avant tout",
                    "💆 Massages et soins professionnels bénéfiques"
                ])
        
        # Conseils selon le type de peau - DÉTAILLÉS
        if type_peau:
            if type_peau == 'grasse':
                conseils.extend([
                    "🧴 Textures légères : Gels, sérums, fluides",
                    "🚫 Évitez les huiles lourdes et crèmes trop riches",
                    "🧼 Nettoyage 2x/jour mais pas plus (effet rebond)",
                    "💧 Hydratation obligatoire même pour peau grasse"
                ])
            elif type_peau == 'sèche':
                conseils.extend([
                    "🧴 Textures riches : Crèmes, baumes, huiles",
                    "💧 Hydratation matin ET soir sans exception",
                    "🛁 Évitez les nettoyants moussants agressifs",
                    "🌙 Masque hydratant 1-2 fois par semaine"
                ])
            elif type_peau == 'mixte':
                conseils.extend([
                    "🎯 Soins ciblés : Zone T (gel) + Joues (crème)",
                    "⚖️ Équilibrez sans assécher ni surgraisser",
                    "🧴 Sérum hydratant sur tout le visage",
                    "🔄 Adaptez selon les saisons"
                ])
            elif type_peau == 'sensible':
                conseils.extend([
                    "🌿 Moins c'est mieux : Routine minimaliste",
                    "🧪 Un nouveau produit à la fois maximum",
                    "❄️ Eau thermale pour apaiser les irritations",
                    "📋 Tenez un journal pour identifier les déclencheurs"
                ])
        
        # Conseils saisonniers spécifiques au Sénégal
        from datetime import datetime
        mois_actuel = datetime.now().month
        
        if mois_actuel in [12, 1, 2]:  # Harmattan
            conseils.extend([
                "🌪️ Saison Harmattan : Renforcez l'hydratation x2",
                "💨 Protégez-vous de la poussière et du vent sec",
                "🧴 Ajoutez une huile végétale à votre routine"
            ])
        elif mois_actuel in [3, 4, 5]:  # Saison chaude
            conseils.extend([
                "🔥 Saison chaude : Textures légères et matifiantes",
                "☀️ Protection solaire renforcée (SPF 50+)",
                "💦 Brumisateur d'eau thermale pour rafraîchir"
            ])
        elif mois_actuel in [6, 7, 8, 9]:  # Hivernage
            conseils.extend([
                "🌧️ Saison des pluies : Attention à l'humidité et aux champignons",
                "🧼 Nettoyage plus fréquent si transpiration",
                "☀️ Protection solaire même par temps nuageux"
            ])
        
        # Conseils de routine générale
        conseils.extend([
            "📅 Constance = Clé du succès : Routine quotidienne obligatoire",
            "📸 Prenez des photos pour suivre l'évolution",
            "💰 Investissez dans la qualité plutôt que la quantité",
            "🏥 Consultez un dermatologue si aucune amélioration après 3 mois"
        ])
        
        return conseils
    
    def handle_pharmacies(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        h24_seulement = data.get('h24_seulement', False)
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')
        
        conn = sqlite3.connect('pharmacy_assistant.db')
        conn.row_factory = sqlite3.Row
        
        query = 'SELECT * FROM pharmacies'
        if h24_seulement:
            query += ' WHERE ouvert_24h = 1'
        
        pharmacies = conn.execute(query).fetchall()
        conn.close()
        
        # Calculer les distances si position fournie
        pharmacies_with_distance = []
        for pharmacie in pharmacies:
            pharmacie_dict = dict(pharmacie)
            
            if user_lat and user_lon and pharmacie['latitude'] and pharmacie['longitude']:
                # Calcul distance avec formule haversine simplifiée
                lat1, lon1 = math.radians(float(user_lat)), math.radians(float(user_lon))
                lat2, lon2 = math.radians(float(pharmacie['latitude'])), math.radians(float(pharmacie['longitude']))
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                distance = 6371 * c  # Rayon de la Terre en km
                
                pharmacie_dict['distance'] = round(distance, 1)
            else:
                pharmacie_dict['distance'] = None
            
            pharmacies_with_distance.append(pharmacie_dict)
        
        # Trier par distance et limiter aux 5 plus proches
        if user_lat and user_lon:
            pharmacies_with_distance = [p for p in pharmacies_with_distance if p['distance'] is not None]
            pharmacies_with_distance.sort(key=lambda x: x['distance'])
            pharmacies_with_distance = pharmacies_with_distance[:5]  # Limiter à 5
        
        response = {
            'pharmacies': pharmacies_with_distance,
            'message': f"Voici les {min(5, len(pharmacies_with_distance))} pharmacies les plus proches de vous"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

def main():
    print("🤖 Assistant Pharmacien Sénégal - Version Chat Fluide")
    print("=" * 55)
    print("💬 Interface conversationnelle comme ChatGPT")
    print("⏰ Diagnostic avec durée des symptômes")
    print("🏥 Top 5 pharmacies les plus proches")
    print("🚀 Serveur démarré sur http://localhost:8000")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    
    server = HTTPServer(('localhost', 8000), ChatPharmacyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")
        server.server_close()

if __name__ == '__main__':
    main()