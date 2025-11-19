#!/usr/bin/env python3
"""
Assistant Pharmacien Sénégal - Version Streamlit
Déploiement web avec interface moderne et interactive
"""

import streamlit as st
import sqlite3
import pandas as pd
import json
import unicodedata
import re
import math
import csv
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Assistant Pharmacien Sénégal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cacher le menu et footer Streamlit pour une meilleure expérience
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #28a745, #20c997);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        background-color: #f8f9fa;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .product-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .pharmacy-card {
        border: 1px solid #c3e6c3;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8fff8;
    }
    
    .pharmacy-24h {
        border-left: 4px solid #28a745;
        background-color: #e8f5e8;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .african-product {
        border-left: 4px solid #ff6b35;
        background: linear-gradient(90deg, #fff5f0, #ffffff);
    }
</style>
""", unsafe_allow_html=True)

class StreamlitPharmacyAssistant:
    """Assistant Pharmacien pour Streamlit avec optimisations"""
    
    def __init__(self):
        self.db_path = 'pharmacy_assistant.db'
        self.init_session_state()
    
    def init_session_state(self):
        """Initialise l'état de session Streamlit"""
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {}
        if 'user_location' not in st.session_state:
            st.session_state.user_location = None
        if 'chat_state' not in st.session_state:
            st.session_state.chat_state = 'initial'
        if 'current_problem' not in st.session_state:
            st.session_state.current_problem = {}
        if 'pending_questions' not in st.session_state:
            st.session_state.pending_questions = []
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "👋 Bonjour ! Je suis votre assistant pharmacien.\n\n**Deux façons de commencer :**\n\n📸 **Option 1 :** Téléchargez une photo de votre peau pour une analyse automatique par IA\n\n💬 **Option 2 :** Décrivez-moi votre problème de peau dans le chat\n\nJe vous aiderai à trouver les meilleurs produits adaptés à vos besoins !"}
            ]
        if 'awaiting_response' not in st.session_state:
            st.session_state.awaiting_response = False
    
    def get_db_connection(self):
        """Connexion à la base de données thread-safe"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    @st.cache_data(ttl=3600)  # Cache pendant 1 heure
    def load_all_products(_self):
        """Charge tous les produits avec mise en cache"""
        conn = sqlite3.connect(_self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        produits = conn.execute('SELECT * FROM produits ORDER BY nom').fetchall()
        conn.close()
        return [dict(p) for p in produits]
    
    @st.cache_data(ttl=3600)  # Cache pendant 1 heure
    def load_all_pharmacies(_self):
        """Charge toutes les pharmacies avec mise en cache"""
        conn = sqlite3.connect(_self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        pharmacies = conn.execute('SELECT * FROM pharmacies ORDER BY ville, nom').fetchall()
        conn.close()
        return [dict(p) for p in pharmacies]
    
    def extract_symptom_duration(self, text):
        """Extrait la durée des symptômes avec logique corrigée"""
        patterns = [
            (r'depuis\s+(\d+)\s+ans?', lambda x: int(x) * 365),
            (r'depuis\s+(\d+)\s+mois', lambda x: int(x) * 30),
            (r'depuis\s+(\d+)\s+semaines?', lambda x: int(x) * 7),
            (r'depuis\s+(\d+)\s+jours?', lambda x: int(x)),
            (r'depuis\s+très\s+longtemps', lambda x: 1095),  # 3 ans
            (r'depuis\s+longtemps', lambda x: 730),  # 2 ans
            (r'récemment', lambda x: 10),
            (r'depuis\s+peu', lambda x: 14),
            (r'depuis\s+l\'harmattan', lambda x: 60),
            (r'depuis\s+l\'hiver', lambda x: 90),
        ]
        
        text_lower = text.lower()
        for pattern, converter in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                if match.groups():
                    return {'jours': converter(match.group(1)), 'texte': match.group(0)}
                else:
                    return {'jours': converter(None), 'texte': match.group(0)}
        return None
    
    def categorize_duration(self, jours):
        """Catégorise la durée des symptômes"""
        if jours <= 7:
            return " Très récent", "Observez d'abord l'évolution naturelle"
        elif jours <= 21:
            return " Récent", "Routine douce et progressive"
        elif jours <= 90:
            return " Persistant", "Routine plus ciblée nécessaire"
        elif jours <= 365:
            return " Installé", "Approche méthodique requise"
        elif jours <= 1095:
            return " Chronique", "Consultation dermatologique recommandée"
        else:
            return "🩺 Chronique ancien", "Suivi médical spécialisé indispensable"
    
    def search_products(self, probleme, type_peau=None, budget_max=None):
        """Recherche de produits avec filtres"""
        conn = self.get_db_connection()
        
        # Mots-clés de recherche
        search_terms = self.extract_skin_problems(probleme)
        
        conditions = []
        params = []
        
        if search_terms:
            term_conditions = []
            for term in search_terms:
                term_conditions.append('problemes_cibles LIKE ?')
                params.append(f'%{term}%')
            conditions.append(f"({' OR '.join(term_conditions)})")
        else:
            conditions.append('problemes_cibles LIKE ?')
            params.append(f'%{probleme}%')
        
        if budget_max:
            conditions.append('prix_max <= ?')
            params.append(budget_max)
        
        query = f'''
            SELECT * FROM produits 
            WHERE {' AND '.join(conditions)}
            ORDER BY prix_min ASC
            LIMIT 12
        '''
        
        produits = conn.execute(query, params).fetchall()
        conn.close()
        
        return [dict(p) for p in produits]
    
    def extract_skin_problems(self, text):
        """Extrait les problèmes de peau du texte"""
        problems = []
        synonyms = {
            'acné': [
                'acné', 'acne', 'bouton', 'boutons', 'pustule', 'pustules',
                'comédon', 'comedon', 'points noirs', 'points blancs',
                'imperfection', 'imperfections', 'eruption', 'éruption',
                'peau à tendance acnéique'
            ],

            'sèche': [
                'sèche', 'seche', 'peau sèche', 'sécheresse', 'dessechée',
                'déshydratée', 'tiraillement', 'tiraille', 'peau qui tire',
                'xerose', 'xérose' 
            ],

            'taches': [
                'tache', 'taches', 'tache brune', 'taches brunes',
                'hyperpigmentation', 'pigment', 'pigmentaire',
                'melasma', 'mélasma', 'masque de grossesse',
                'taches solaires', 'taches pigmentaires'
            ],

            'sensible': [
                'sensible', 'irrité', 'irritee', 'irritée',
                'rouge', 'rougeur', 'rougeurs', 'démangeaison', 'démangeaisons',
                'réactive', 'reactive', 'intolérante', 'peau fragile'
            ],

            'rides': [
                'ride', 'rides', 'ridule', 'ridules',
                'vieillissement', 'anti-âge', 'anti age',
                'perte de fermeté', 'relâchement', 'relachement',
                'peau mature'
            ],

            'grasse': [
                'grasse', 'peau grasse', 'brillant', 'brillance',
                'excès de sébum', 'sébum', 'sebum',
                'huileux', 'pores dilatés', 'peau huileuse',
                'acné hormonal'  #
            ],

            'depigmentation': [
                'depigmentation', 'depigmentee', 'depigmentées',
                'teint clair', 'eclaircissement', 'eclaircir',
                'blanchiment', 'produits eclaircissants',
                'carotone', 'makari', 'fair and white', 
                'claire', 'peau claire artificiellement'
            ],

        }

        
        text_lower = text.lower()
        for problem, terms in synonyms.items():
            if any(term in text_lower for term in terms):
                problems.append(problem)
        
        return problems
    
    
    def normalize_text(text: str) -> str:
        # Retirer les accents
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        
        # Minuscules
        text = text.lower()
        
        # Retirer les caractères inutiles
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Nettoyage des espaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text


    # -----------------------------------------------------
    # 3) Fonction : Détection automatique des mots-clés
    # -----------------------------------------------------

    def detect_keywords(text: str, synonyms_dict: dict):
        text_norm = normalize_text(text)
        detected = []

        for category, words in synonyms_dict.items():
            for w in words:
                w_norm = normalize_text(w)
                if w_norm in text_norm:
                    detected.append(category)
                    break

        return list(set(detected))
    
    def get_nearby_pharmacies(self, user_lat, user_lon, h24_only=False, limit=5):
        """Obtient les pharmacies proches"""
        conn = self.get_db_connection()
        
        query = 'SELECT * FROM pharmacies'
        if h24_only:
            query += ' WHERE ouvert_24h = 1'
        
        pharmacies = conn.execute(query).fetchall()
        conn.close()
        
        # Calcul des distances
        pharmacies_with_distance = []
        for pharmacie in pharmacies:
            if pharmacie['latitude'] and pharmacie['longitude']:
                distance = self.calculate_distance(
                    user_lat, user_lon,
                    pharmacie['latitude'], pharmacie['longitude']
                )
                
                pharmacie_dict = dict(pharmacie)
                pharmacie_dict['distance'] = round(distance, 1)
                pharmacies_with_distance.append(pharmacie_dict)
        
        # Trier par distance et limiter
        pharmacies_with_distance.sort(key=lambda x: x['distance'])
        return pharmacies_with_distance[:limit]
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calcule la distance entre deux points GPS"""
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c  # Rayon de la Terre en km
    
    def analyze_missing_info(self, message):
        """Analyse quelles informations manquent dans le message"""
        missing = []
        
        # Vérifier la durée
        duration = self.extract_symptom_duration(message)
        if not duration:
            missing.append('duration')
        
        # Vérifier la localisation sur le corps
        body_parts = ['visage', 'front', 'joues', 'nez', 'menton', 'cou', 'dos', 'bras', 'jambes', 'mains', 'pieds', 'corps']
        has_location = any(part in message.lower() for part in body_parts)
        if not has_location:
            missing.append('location')
        
        # Vérifier l'aspect/description
        aspects = ['rouge', 'gonflé', 'sec', 'gras', 'rugueux', 'lisse', 'douloureux', 'qui gratte', 'qui démange']
        has_aspect = any(aspect in message.lower() for aspect in aspects)
        if not has_aspect:
            missing.append('aspect')
        
        return missing
    
    def generate_follow_up_question(self, missing_info):
        """Génère une question de suivi selon l'information manquante"""
        questions = {
            'duration': " **Depuis combien de temps avez-vous ce problème ?**\n\nExemples : depuis 2 semaines, depuis 3 mois, depuis longtemps...",
            'location': " **Où exactement sur votre corps se trouve ce problème ?**\n\nExemples : sur le visage, sur les joues, sur le front, sur le dos...",
            'aspect': " **Comment décririez-vous l'aspect de votre peau ?**\n\nExemples : rouge et gonflé, sec et rugueux, avec des boutons, qui démange..."
        }
        return questions.get(missing_info, "")
    
    def save_conversation_to_csv(self, conversation_data):
        """Sauvegarde la conversation dans un fichier CSV"""
        csv_file = 'conversations_historique.csv'
        file_exists = os.path.isfile(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'timestamp', 'age', 'type_peau', 'probleme_initial', 
                    'duree', 'localisation', 'aspect', 'produits_recommandes', 
                    'nombre_produits', 'budget_max', 'session_id'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(conversation_data)
            return True
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde : {e}")
            return False
    
    def generate_personalized_advice(self, probleme, type_peau, age, duration):
        """Génère des conseils personnalisés"""
        conseils = []
        
        # Conseils selon la durée
        if duration:
            jours = duration['jours']
            category, advice = self.categorize_duration(jours)
            conseils.append(f"{category}: {advice}")
        
        # Conseils selon le problème
        problems = self.extract_skin_problems(probleme)
        
        if 'acné' in problems:
            if age and age < 25:
                conseils.extend([
                    " Routine simple : Nettoyant doux + hydratant léger",
                    " Évitez de toucher votre visage",
                    " Changez vos taies d'oreiller régulièrement"
                ])
            else:
                conseils.extend([
                    " Acné adulte souvent liée au stress et hormones",
                    " Produits avec acide salicylique le soir",
                    " Protection solaire obligatoire"
                ])
        
        if 'sèche' in problems:
            conseils.extend([
                " Hydratez sur peau encore humide après la douche",
                " Douches tièdes et courtes (5-10 min)",
                " Buvez 1,5-2L d'eau par jour"
            ])
            
            if 'harmattan' in probleme.lower():
                conseils.append("❄️ Saison sèche : Renforcez avec des soins plus riches")
        
        if 'taches' in problems:
            conseils.extend([
                "☀️ Protection solaire SPF 30+ TOUS LES JOURS",
                "🌙 Soins éclaircissants uniquement le soir",
                "⏳ Patience : 3-6 mois minimum pour voir des résultats"
            ])
        
        # Conseils selon le type de peau
        if type_peau:
            if type_peau == 'grasse':
                conseils.append("🧴 Privilégiez textures légères (gels, sérums)")
            elif type_peau == 'sèche':
                conseils.append("🧴 Optez pour textures riches (crèmes, baumes)")
            elif type_peau == 'sensible':
                conseils.append("🧪 Test patch obligatoire pour nouveaux produits")
        
        # Conseils généraux
        conseils.extend([
            "📅 Constance = Clé du succès : routine quotidienne",
            "📸 Prenez des photos pour suivre l'évolution",
            "🏥 Consultez un dermatologue si aucune amélioration après 3 mois"
        ])
        
        return conseils
    
    def analyze_skin_image(self, image):
        """Analyse une image de peau pour détecter des problèmes"""
        try:
            # Convertir en RGB si nécessaire
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Redimensionner pour analyse plus rapide
            image = image.resize((300, 300))
            
            # Convertir en array numpy pour analyse
            import numpy as np
            img_array = np.array(image)
            
            # Analyse des couleurs
            avg_red = np.mean(img_array[:, :, 0])
            avg_green = np.mean(img_array[:, :, 1])
            avg_blue = np.mean(img_array[:, :, 2])
            
            # Calcul de la variance (texture)
            variance = np.var(img_array)
            
            # Détection des problèmes basée sur l'analyse
            detected_problems = []
            confidence_scores = {}
            
            # Détection de rougeurs (acné, irritation)
            if avg_red > avg_green + 10 and avg_red > avg_blue + 10:
                detected_problems.append('acné')
                confidence_scores['acné'] = min(95, 60 + (avg_red - avg_green) / 2)
            
            # Détection de peau sèche (texture irrégulière)
            if variance > 1500:
                detected_problems.append('sèche')
                confidence_scores['sèche'] = min(90, 50 + variance / 50)
            
            # Détection de taches (variations de luminosité)
            brightness = (avg_red + avg_green + avg_blue) / 3
            if variance > 1000 and brightness < 150:
                detected_problems.append('taches')
                confidence_scores['taches'] = min(85, 55 + variance / 40)
            
            # Si aucun problème détecté
            if not detected_problems:
                detected_problems.append('normale')
                confidence_scores['normale'] = 70
            
            return {
                'problems': detected_problems,
                'confidence': confidence_scores,
                'analysis': {
                    'avg_red': avg_red,
                    'avg_green': avg_green,
                    'avg_blue': avg_blue,
                    'variance': variance,
                    'brightness': brightness
                }
            }
            
        except Exception as e:
            return {
                'problems': [],
                'confidence': {},
                'error': str(e)
            }

def main():
    """Fonction principale Streamlit"""
    assistant = StreamlitPharmacyAssistant()
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Assistant Pharmacien Sénégal</h1>
        <p>Conseils cosmétiques intelligents avec produits africains authentiques</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Profil utilisateur
    with st.sidebar:
        st.header("👤 Votre Profil")
        
        age = st.number_input("Âge", min_value=1, max_value=100, value=25)
        type_peau = st.selectbox(
            "Type de peau",
            ["", "Normale", "Sèche", "Grasse", "Mixte", "Sensible"]
        )
        budget_max = st.selectbox(
            "Budget maximum (FCFA)",
            [None, 3000, 5000, 10000, 15000, 25000],
            format_func=lambda x: "Pas de limite" if x is None else f"{x:,} FCFA"
        )
        
        # Sauvegarder le profil
        st.session_state.user_profile = {
            'age': age,
            'type_peau': type_peau.lower() if type_peau else '',
            'budget_max': budget_max
        }
        
        st.markdown("---")
        
        # Géolocalisation simulée (Dakar par défaut)
        st.header("📍 Localisation")
        ville = st.selectbox(
            "Votre ville",
            ["Dakar", "Thiès", "Saint-Louis", "Kaolack"]
        )
        
        # Coordonnées par défaut selon la ville
        coords = {
            "Dakar": (14.6937, -17.4441),
            "Thiès": (14.7886, -16.9317),
            "Saint-Louis": (16.0469, -16.4814),
            "Kaolack": (14.1333, -16.0667)
        }
        
        if ville in coords:
            st.session_state.user_location = coords[ville]
            st.success(f"📍 Position: {ville}")
        
        h24_only = st.checkbox("Pharmacies 24h/24 seulement")
        
        st.markdown("---")
        
        # Statistiques
        st.header("📊 Statistiques")
        try:
            conn = assistant.get_db_connection()
            total_produits = conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0]
            total_pharmacies = conn.execute('SELECT COUNT(*) FROM pharmacies').fetchone()[0]
            pharmacies_24h = conn.execute('SELECT COUNT(*) FROM pharmacies WHERE ouvert_24h = 1').fetchone()[0]
            conn.close()
            
            st.metric("Produits", total_produits)
            st.metric("Pharmacies", total_pharmacies)
            st.metric("Ouvertes 24h", pharmacies_24h)
        except:
            st.error("Base de données non disponible")
    
    # Interface principale
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat Assistant", "💊 Produits", "🏥 Pharmacies", "📊 Analytics", "📝 Historique"])
    
    with tab1:
        st.header("💬 Chat avec l'Assistant")
        
        # Section d'upload d'image
        st.markdown("### 📸 Analyse de Photo de Peau")
        
        with st.expander("ℹ️ Comment prendre une bonne photo ?"):
            st.markdown("""
            **Pour une analyse optimale :**
            - 📱 Utilisez un smartphone ou appareil photo de bonne qualité
            - ☀️ Prenez la photo en lumière naturelle (près d'une fenêtre)
            - 📏 Gardez une distance de 15-20 cm de la zone à photographier
            - 🎯 Assurez-vous que la zone est nette et bien visible
            - 🚫 Évitez le flash qui peut altérer les couleurs
            - 🧼 Nettoyez votre peau avant (pas de maquillage)
            
            **L'IA peut détecter :**
            - 🔴 Acné et rougeurs
            - 💧 Peau sèche et déshydratée
            - 🟤 Taches pigmentaires
            - ✨ État général de la peau
            """)
        
        uploaded_file = st.file_uploader(
            "Téléchargez une photo de votre problème de peau pour une analyse automatique",
            type=['jpg', 'jpeg', 'png'],
            help="Prenez une photo claire de la zone affectée en bonne lumière naturelle"
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Afficher l'image
                image = Image.open(uploaded_file)
                st.image(image, caption="Photo téléchargée", use_column_width=True)
            
            with col2:
                # Analyser l'image
                with st.spinner("🔍 Analyse de l'image en cours..."):
                    analysis_result = assistant.analyze_skin_image(image)
                
                if 'error' in analysis_result:
                    st.error(f"❌ Erreur lors de l'analyse : {analysis_result['error']}")
                else:
                    st.success("✅ Analyse terminée !")
                    
                    # Afficher les résultats
                    st.markdown("**🔬 Problèmes détectés :**")
                    for problem in analysis_result['problems']:
                        confidence = analysis_result['confidence'].get(problem, 0)
                        st.markdown(f"• **{problem.capitalize()}** (confiance: {confidence:.0f}%)")
                    
                    # Générer automatiquement une description
                    if analysis_result['problems'] and analysis_result['problems'][0] != 'normale':
                        auto_message = f"J'ai des problèmes de {', '.join(analysis_result['problems'])} détectés sur la photo"
                        
                        if st.button("🚀 Obtenir des recommandations basées sur cette analyse"):
                            # Ajouter le message automatique
                            st.session_state.messages.append({"role": "user", "content": f"📸 Photo analysée : {auto_message}"})
                            st.session_state.current_problem['initial_message'] = auto_message
                            st.session_state.current_problem['all_messages'] = [auto_message]
                            st.session_state.current_problem['from_image'] = True
                            st.session_state.chat_state = 'ready'
                            st.rerun()
                    else:
                        st.info("✨ Votre peau semble en bonne santé ! Si vous avez des préoccupations spécifiques, décrivez-les dans le chat ci-dessous.")
        
        st.markdown("---")
        
        # Container pour les messages avec hauteur fixe et scroll
        chat_container = st.container(height=400)
        
        with chat_container:
            # Afficher tous les messages de la conversation avec st.chat_message
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Suggestions rapides (seulement au début)
        if len(st.session_state.messages) == 1:
            st.markdown("**💡 Suggestions rapides :**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔴 Problème d'acné"):
                    st.session_state.quick_prompt = "J'ai de l'acné sur le visage"
                    st.rerun()
            
            with col2:
                if st.button("💧 Peau sèche"):
                    st.session_state.quick_prompt = "Ma peau est très sèche"
                    st.rerun()
            
            with col3:
                if st.button("🟤 Taches brunes"):
                    st.session_state.quick_prompt = "J'ai des taches brunes"
                    st.rerun()
        
        # Traiter les suggestions rapides
        if 'quick_prompt' in st.session_state and st.session_state.quick_prompt:
            user_input = st.session_state.quick_prompt
            st.session_state.quick_prompt = None  # Réinitialiser
            
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Traiter le message
            # Déterminer l'état de la conversation
            if st.session_state.chat_state == 'initial':
                # Premier message - analyser
                st.session_state.current_problem['initial_message'] = user_input
                st.session_state.current_problem['all_messages'] = [user_input]
                missing_info = assistant.analyze_missing_info(user_input)
                
                if missing_info:
                    # Poser la première question
                    question = assistant.generate_follow_up_question(missing_info[0])
                    st.session_state.messages.append({"role": "assistant", "content": question})
                    st.session_state.pending_questions = missing_info[1:]
                    st.session_state.chat_state = 'asking_questions'
                    st.session_state.awaiting_response = True
                else:
                    st.session_state.chat_state = 'ready'
            
            # Générer les recommandations si prêt
            if st.session_state.chat_state == 'ready':
                # Combiner tous les messages
                full_message = " ".join(st.session_state.current_problem.get('all_messages', [user_input]))
                
                # Extraction de la durée
                duration = assistant.extract_symptom_duration(full_message)
                
                # Recherche de produits
                produits = assistant.search_products(
                    full_message,
                    st.session_state.user_profile.get('type_peau'),
                    st.session_state.user_profile.get('budget_max')
                )
                
                # Génération de conseils
                conseils = assistant.generate_personalized_advice(
                    full_message,
                    st.session_state.user_profile.get('type_peau'),
                    st.session_state.user_profile.get('age'),
                    duration
                )
                
                # Créer la réponse complète
                response = "✅ **Analyse terminée !**\n\n"
                
                if duration:
                    jours = duration['jours']
                    category, _ = assistant.categorize_duration(jours)
                    response += f"📅 **Durée :** {category}\n\n"
                
                response += f"💊 **J'ai trouvé {len(produits)} produits adaptés à votre problème.**\n\n"
                
                if conseils:
                    response += "💡 **Mes conseils personnalisés :**\n"
                    for i, conseil in enumerate(conseils[:5], 1):
                        response += f"{i}. {conseil}\n"
                    response += "\n"
                
                if produits:
                    response += "🛍️ **Top 3 produits recommandés :**\n"
                    for i, produit in enumerate(produits[:3], 1):
                        prix = f"{produit['prix_min']}-{produit['prix_max']} FCFA" if produit['prix_min'] else "Prix variable"
                        response += f"\n**{i}. {produit['nom']}** ({produit['marque']})\n"
                        response += f"   💰 {prix}\n"
                        if produit['description']:
                            response += f"   📝 {produit['description'][:100]}...\n"
                
                response += "\n\n📋 Consultez l'onglet **Produits** pour voir tous les détails !"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Sauvegarder dans l'historique
                conversation_entry = {
                    'user': full_message,
                    'duration': duration,
                    'produits': produits,
                    'conseils': conseils,
                    'timestamp': datetime.now()
                }
                st.session_state.conversation_history.append(conversation_entry)
                
                # Sauvegarder dans CSV
                csv_data = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'age': st.session_state.user_profile.get('age', ''),
                    'type_peau': st.session_state.user_profile.get('type_peau', ''),
                    'probleme_initial': st.session_state.current_problem.get('initial_message', user_input),
                    'duree': duration['texte'] if duration else '',
                    'localisation': full_message,
                    'aspect': full_message,
                    'produits_recommandes': ', '.join([p['nom'] for p in produits[:5]]),
                    'nombre_produits': len(produits),
                    'budget_max': st.session_state.user_profile.get('budget_max', ''),
                    'session_id': st.session_state.get('session_id', id(st.session_state))
                }
                assistant.save_conversation_to_csv(csv_data)
                
                # Réinitialiser pour une nouvelle conversation
                st.session_state.chat_state = 'initial'
                st.session_state.current_problem = {}
                st.session_state.pending_questions = []
                st.session_state.awaiting_response = False
            
            st.rerun()
        
        # Zone de saisie en bas (toujours visible)
        user_input = st.chat_input("Tapez votre message ici...")
        
        if user_input:
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Traiter le message
            # Déterminer l'état de la conversation
            if st.session_state.chat_state == 'initial':
                # Premier message - analyser
                st.session_state.current_problem['initial_message'] = user_input
                st.session_state.current_problem['all_messages'] = [user_input]
                missing_info = assistant.analyze_missing_info(user_input)
                
                if missing_info:
                    # Poser la première question
                    question = assistant.generate_follow_up_question(missing_info[0])
                    st.session_state.messages.append({"role": "assistant", "content": question})
                    st.session_state.pending_questions = missing_info[1:]  # Garder les autres questions
                    st.session_state.chat_state = 'asking_questions'
                    st.session_state.awaiting_response = True
                else:
                    # Toutes les infos présentes, générer recommandations
                    st.session_state.chat_state = 'ready'
            
            elif st.session_state.chat_state == 'asking_questions':
                # Enregistrer la réponse
                st.session_state.current_problem['all_messages'].append(user_input)
                
                if st.session_state.pending_questions:
                    # Poser la question suivante
                    question = assistant.generate_follow_up_question(st.session_state.pending_questions[0])
                    st.session_state.messages.append({"role": "assistant", "content": question})
                    st.session_state.pending_questions.pop(0)
                else:
                    # Toutes les questions répondues
                    st.session_state.chat_state = 'ready'
            
            # Générer les recommandations si prêt
            if st.session_state.chat_state == 'ready':
                # Combiner tous les messages
                full_message = " ".join(st.session_state.current_problem.get('all_messages', [user_input]))
                
                # Extraction de la durée
                duration = assistant.extract_symptom_duration(full_message)
                
                # Recherche de produits
                produits = assistant.search_products(
                    full_message,
                    st.session_state.user_profile.get('type_peau'),
                    st.session_state.user_profile.get('budget_max')
                )
                
                # Génération de conseils
                conseils = assistant.generate_personalized_advice(
                    full_message,
                    st.session_state.user_profile.get('type_peau'),
                    st.session_state.user_profile.get('age'),
                    duration
                )
                
                # Créer la réponse complète
                response = "✅ **Analyse terminée !**\n\n"
                
                if duration:
                    jours = duration['jours']
                    category, _ = assistant.categorize_duration(jours)
                    response += f"📅 **Durée :** {category}\n\n"
                
                response += f"💊 **J'ai trouvé {len(produits)} produits adaptés à votre problème.**\n\n"
                
                if conseils:
                    response += "💡 **Mes conseils personnalisés :**\n"
                    for i, conseil in enumerate(conseils[:5], 1):
                        response += f"{i}. {conseil}\n"
                    response += "\n"
                
                if produits:
                    response += "🛍️ **Top 3 produits recommandés :**\n"
                    for i, produit in enumerate(produits[:3], 1):
                        prix = f"{produit['prix_min']}-{produit['prix_max']} FCFA" if produit['prix_min'] else "Prix variable"
                        response += f"\n**{i}. {produit['nom']}** ({produit['marque']})\n"
                        response += f"   💰 {prix}\n"
                        if produit['description']:
                            response += f"   📝 {produit['description'][:100]}...\n"
                
                response += "\n\n📋 Consultez l'onglet **Produits** pour voir tous les détails !"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Sauvegarder dans l'historique
                conversation_entry = {
                    'user': full_message,
                    'duration': duration,
                    'produits': produits,
                    'conseils': conseils,
                    'timestamp': datetime.now()
                }
                st.session_state.conversation_history.append(conversation_entry)
                
                # Sauvegarder dans CSV
                csv_data = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'age': st.session_state.user_profile.get('age', ''),
                    'type_peau': st.session_state.user_profile.get('type_peau', ''),
                    'probleme_initial': st.session_state.current_problem.get('initial_message', user_input),
                    'duree': duration['texte'] if duration else '',
                    'localisation': full_message,
                    'aspect': full_message,
                    'produits_recommandes': ', '.join([p['nom'] for p in produits[:5]]),
                    'nombre_produits': len(produits),
                    'budget_max': st.session_state.user_profile.get('budget_max', ''),
                    'session_id': st.session_state.get('session_id', id(st.session_state))
                }
                assistant.save_conversation_to_csv(csv_data)
                
                # Réinitialiser pour une nouvelle conversation
                st.session_state.chat_state = 'initial'
                st.session_state.current_problem = {}
                st.session_state.pending_questions = []
                st.session_state.awaiting_response = False
            
            # Recharger pour afficher les nouveaux messages
            st.rerun()
        
        # Bouton pour nouvelle conversation
        if len(st.session_state.messages) > 1:
            if st.button("🔄 Nouvelle conversation"):
                st.session_state.messages = [
                    {"role": "assistant", "content": "👋 Bonjour ! Je suis votre assistant pharmacien.\n\n**Deux façons de commencer :**\n\n📸 **Option 1 :** Téléchargez une photo de votre peau pour une analyse automatique par IA\n\n💬 **Option 2 :** Décrivez-moi votre problème de peau dans le chat\n\nJe vous aiderai à trouver les meilleurs produits adaptés à vos besoins !"}
                ]
                st.session_state.chat_state = 'initial'
                st.session_state.current_problem = {}
                st.session_state.pending_questions = []
                st.rerun()
            st.header("💬 Historique de Conversation")
            
            for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):
                # Message utilisateur
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Vous :</strong> {conv['user']}
                </div>
                """, unsafe_allow_html=True)
                
                # Réponse assistant
                response_text = "🤖 **Assistant :** "
                
                if conv['duration']:
                    jours = conv['duration']['jours']
                    category, _ = assistant.categorize_duration(jours)
                    response_text += f"{category} - "
                
                response_text += f"J'ai analysé votre problème et trouvé {len(conv['produits'])} produits adaptés."
                
                st.markdown(f"""
                <div class="chat-message">
                    {response_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Conseils
                if conv['conseils']:
                    st.markdown("**💡 Conseils personnalisés :**")
                    for conseil in conv['conseils'][:3]:
                        st.markdown(f"• {conseil}")
                
                # Produits (aperçu)
                if conv['produits']:
                    st.markdown("**💊 Produits recommandés :**")
                    for produit in conv['produits'][:2]:
                        prix = f"{produit['prix_min']}-{produit['prix_max']} FCFA" if produit['prix_min'] else "Prix non disponible"
                        st.markdown(f"• **{produit['nom']}** ({produit['marque']}) - {prix}")
                
                st.markdown("---")
    
    with tab2:
        st.header("💊 Catalogue de Produits")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Rechercher un produit")
        
        with col2:
            marque_filter = st.selectbox(
                "Marque",
                ["Toutes"] + ["La Roche-Posay", "Vichy", "Avène", "Eucerin", "Karité Authentique", "Aloe du Sénégal"]
            )
        
        with col3:
            prix_max_filter = st.selectbox(
                "Prix maximum",
                [None, 3000, 5000, 10000, 15000],
                format_func=lambda x: "Tous prix" if x is None else f"≤ {x:,} FCFA"
            )
        
        # Affichage des produits
        try:
            conn = assistant.get_db_connection()
            
            query = "SELECT * FROM produits WHERE 1=1"
            params = []
            
            if search_term:
                query += " AND (LOWER(nom) LIKE ? OR LOWER(description) LIKE ?)"
                params.extend([f'%{search_term.lower()}%', f'%{search_term.lower()}%'])
            
            if marque_filter != "Toutes":
                query += " AND marque = ?"
                params.append(marque_filter)
            
            if prix_max_filter:
                query += " AND prix_max <= ?"
                params.append(prix_max_filter)
            
            query += " ORDER BY prix_min ASC"
            
            produits = conn.execute(query, params).fetchall()
            conn.close()
            
            if produits:
                # Affichage en grille
                cols = st.columns(2)
                
                for i, produit in enumerate(produits):
                    with cols[i % 2]:
                        # Déterminer si c'est un produit africain
                        is_african = any(term in produit['nom'].lower() or term in (produit['ingredients_actifs'] or '').lower() 
                                       for term in ['karité', 'baobab', 'aloe', 'neem', 'moringa', 'bissap'])
                        
                        card_class = "product-card african-product" if is_african else "product-card"
                        
                        prix = f"{produit['prix_min']}-{produit['prix_max']} FCFA" if produit['prix_min'] else "Prix non disponible"
                        
                        african_badge = " **Produit Africain**" if is_african else ""
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            <h4>{produit['nom']}</h4>
                            <p><strong>Marque:</strong> {produit['marque'] or 'Non spécifiée'}</p>
                            <p><strong>Prix:</strong> {prix}</p>
                            <p>{produit['description'] or ''}</p>
                            {african_badge}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aucun produit trouvé avec ces critères.")
                
        except Exception as e:
            st.error(f"Erreur lors du chargement des produits: {e}")
    
    with tab3:
        st.header("🏥 Pharmacies du Sénégal")
        
        if st.session_state.user_location:
            lat, lon = st.session_state.user_location
            
            # Obtenir les pharmacies proches
            pharmacies = assistant.get_nearby_pharmacies(lat, lon, h24_only, limit=10)
            
            if pharmacies:
                st.success(f"📍 {len(pharmacies)} pharmacies trouvées près de {ville}")
                
                for i, pharmacie in enumerate(pharmacies, 1):
                    card_class = "pharmacy-card pharmacy-24h" if pharmacie['ouvert_24h'] else "pharmacy-card"
                    h24_badge = "🟢 **24h/24**" if pharmacie['ouvert_24h'] else ""
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h4>{i}. {pharmacie['nom']}</h4>
                        <p>📍 {pharmacie['adresse']}</p>
                        <p>📞 {pharmacie['telephone']}</p>
                        <p>🕒 {pharmacie['horaires']}</p>
                        <p>📏 Distance: {pharmacie['distance']} km</p>
                        {h24_badge}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Aucune pharmacie trouvée dans votre zone.")
        else:
            st.info("Sélectionnez votre ville dans la barre latérale pour voir les pharmacies proches.")
    
    with tab4:
        st.header("📊 Analytics & Statistiques")
        
        try:
            conn = assistant.get_db_connection()
            
            # Statistiques générales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_produits = conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0]
                st.metric("Total Produits", total_produits)
            
            with col2:
                total_pharmacies = conn.execute('SELECT COUNT(*) FROM pharmacies').fetchone()[0]
                st.metric("Total Pharmacies", total_pharmacies)
            
            with col3:
                pharmacies_24h = conn.execute('SELECT COUNT(*) FROM pharmacies WHERE ouvert_24h = 1').fetchone()[0]
                st.metric("Pharmacies 24h/24", pharmacies_24h)
            
            with col4:
                african_products = conn.execute('''
                    SELECT COUNT(*) FROM produits 
                    WHERE LOWER(nom) LIKE '%karité%' OR LOWER(nom) LIKE '%baobab%' OR 
                          LOWER(nom) LIKE '%aloe%' OR LOWER(nom) LIKE '%neem%'
                ''').fetchone()[0]
                st.metric("Produits Africains", african_products)
            
            # Graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution des prix
                prix_data = conn.execute('''
                    SELECT 
                        CASE 
                            WHEN prix_max <= 3000 THEN 'Très accessible (≤3000)'
                            WHEN prix_max <= 5000 THEN 'Accessible (3000-5000)'
                            WHEN prix_max <= 10000 THEN 'Moyen (5000-10000)'
                            WHEN prix_max <= 20000 THEN 'Premium (10000-20000)'
                            ELSE 'Très premium (>20000)'
                        END as gamme_prix,
                        COUNT(*) as count
                    FROM produits 
                    WHERE prix_max IS NOT NULL
                    GROUP BY gamme_prix
                ''').fetchall()
                
                if prix_data:
                    df_prix = pd.DataFrame(prix_data, columns=['Gamme de Prix', 'Nombre'])
                    fig_prix = px.pie(df_prix, values='Nombre', names='Gamme de Prix', 
                                     title='Distribution des Prix (FCFA)')
                    st.plotly_chart(fig_prix, use_column_width=True)
            
            with col2:
                # Pharmacies par ville
                ville_data = conn.execute('''
                    SELECT ville, COUNT(*) as count 
                    FROM pharmacies 
                    GROUP BY ville 
                    ORDER BY count DESC
                ''').fetchall()
                
                if ville_data:
                    df_ville = pd.DataFrame(ville_data, columns=['Ville', 'Nombre'])
                    fig_ville = px.bar(df_ville, x='Ville', y='Nombre', 
                                      title='Pharmacies par Ville')
                    st.plotly_chart(fig_ville, use_column_width=True)
            
            # Top marques
            st.subheader("🏷️ Top Marques")
            marques_data = conn.execute('''
                SELECT marque, COUNT(*) as count 
                FROM produits 
                WHERE marque IS NOT NULL
                GROUP BY marque 
                ORDER BY count DESC 
                LIMIT 10
            ''').fetchall()
            
            if marques_data:
                df_marques = pd.DataFrame(marques_data, columns=['Marque', 'Produits'])
                st.dataframe(df_marques, use_column_width=True)
            
            conn.close()
            
        except Exception as e:
            st.error(f"Erreur lors du chargement des statistiques: {e}")
    
    with tab5:
        st.header("📝 Historique des Conversations")
        
        csv_file = 'conversations_historique.csv'
        
        if os.path.isfile(csv_file):
            try:
                df_conversations = pd.read_csv(csv_file)
                
                st.subheader(f"📊 {len(df_conversations)} conversations enregistrées")
                
                # Statistiques rapides
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Conversations", len(df_conversations))
                
                with col2:
                    if 'type_peau' in df_conversations.columns:
                        type_peau_counts = df_conversations['type_peau'].value_counts()
                        if len(type_peau_counts) > 0:
                            st.metric("Type de peau le plus fréquent", type_peau_counts.index[0])
                
                with col3:
                    if 'nombre_produits' in df_conversations.columns:
                        avg_produits = df_conversations['nombre_produits'].mean()
                        st.metric("Moyenne produits recommandés", f"{avg_produits:.1f}")
                
                st.markdown("---")
                
                # Filtres
                col1, col2 = st.columns(2)
                
                with col1:
                    date_filter = st.date_input("Filtrer par date", value=None)
                
                with col2:
                    if 'type_peau' in df_conversations.columns:
                        type_peau_filter = st.selectbox(
                            "Filtrer par type de peau",
                            ["Tous"] + list(df_conversations['type_peau'].dropna().unique())
                        )
                
                # Appliquer les filtres
                df_filtered = df_conversations.copy()
                
                if date_filter:
                    df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])
                    df_filtered = df_filtered[df_filtered['timestamp'].dt.date == date_filter]
                
                if 'type_peau_filter' in locals() and type_peau_filter != "Tous":
                    df_filtered = df_filtered[df_filtered['type_peau'] == type_peau_filter]
                
                # Affichage du tableau
                st.subheader("📋 Détails des Conversations")
                
                # Colonnes à afficher
                display_columns = ['timestamp', 'age', 'type_peau', 'probleme_initial', 'duree', 'nombre_produits']
                available_columns = [col for col in display_columns if col in df_filtered.columns]
                
                if available_columns:
                    st.dataframe(
                        df_filtered[available_columns].sort_values('timestamp', ascending=False),
                        use_column_width=True,
                        height=400
                    )
                
                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger l'historique complet (CSV)",
                    data=df_conversations.to_csv(index=False).encode('utf-8'),
                    file_name=f'historique_conversations_{datetime.now().strftime("%Y%m%d")}.csv',
                    mime='text/csv'
                )
                
                # Graphiques
                st.markdown("---")
                st.subheader("📈 Analyses")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'type_peau' in df_conversations.columns:
                        st.markdown("**Distribution par type de peau**")
                        type_peau_counts = df_conversations['type_peau'].value_counts()
                        fig = px.pie(
                            values=type_peau_counts.values,
                            names=type_peau_counts.index,
                            title="Types de peau des utilisateurs"
                        )
                        st.plotly_chart(fig, use_column_width=True)
                
                with col2:
                    if 'age' in df_conversations.columns:
                        st.markdown("**Distribution par âge**")
                        fig = px.histogram(
                            df_conversations,
                            x='age',
                            nbins=20,
                            title="Répartition des âges"
                        )
                        st.plotly_chart(fig, use_column_width=True)
                
            except Exception as e:
                st.error(f"Erreur lors du chargement de l'historique : {e}")
        else:
            st.info("📭 Aucune conversation enregistrée pour le moment. Commencez à utiliser le chat pour créer un historique !")
            st.markdown("""
            **L'historique enregistrera automatiquement :**
            - 📅 Date et heure de la conversation
            - 👤 Profil utilisateur (âge, type de peau)
            - 💬 Problème décrit
            - ⏱️ Durée des symptômes
            - 💊 Produits recommandés
            - 📊 Statistiques d'utilisation
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Assistant Pharmacien Sénégal - Conseils cosmétiques avec produits africains authentiques<br>
        Développé pour les pharmaciens et patients sénégalais
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


