#!/usr/bin/env python3
"""
Assistant Pharmacien Sénégal - Version Streamlit
Déploiement web avec interface moderne et interactive
"""

import streamlit as st
import sqlite3
import pandas as pd
import json
import re
import math
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Assistant Pharmacien Sénégal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            return "🕐 Très récent", "Observez d'abord l'évolution naturelle"
        elif jours <= 21:
            return "📅 Récent", "Routine douce et progressive"
        elif jours <= 90:
            return "⏰ Persistant", "Routine plus ciblée nécessaire"
        elif jours <= 365:
            return "📋 Installé", "Approche méthodique requise"
        elif jours <= 1095:
            return "🏥 Chronique", "Consultation dermatologique recommandée"
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
            'acné': ['acné', 'acne', 'bouton', 'boutons', 'pustule', 'comédon'],
            'sèche': ['sèche', 'seche', 'sécheresse', 'tiraille', 'déshydrat'],
            'taches': ['tache', 'taches', 'pigment', 'melasma', 'hyperpigmentation'],
            'sensible': ['sensible', 'irrité', 'rouge', 'rougeur', 'démangeaison'],
            'rides': ['ride', 'rides', 'ridule', 'vieillissement', 'anti-âge'],
            'grasse': ['grasse', 'brillant', 'sébum', 'huileux', 'pores']
        }
        
        text_lower = text.lower()
        for problem, terms in synonyms.items():
            if any(term in text_lower for term in terms):
                problems.append(problem)
        
        return problems
    
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
                    "🧴 Routine simple : Nettoyant doux + hydratant léger",
                    "🚫 Évitez de toucher votre visage",
                    "🧼 Changez vos taies d'oreiller régulièrement"
                ])
            else:
                conseils.extend([
                    "💊 Acné adulte souvent liée au stress et hormones",
                    "🧴 Produits avec acide salicylique le soir",
                    "☀️ Protection solaire obligatoire"
                ])
        
        if 'sèche' in problems:
            conseils.extend([
                "💧 Hydratez sur peau encore humide après la douche",
                "🚿 Douches tièdes et courtes (5-10 min)",
                "💦 Buvez 1,5-2L d'eau par jour"
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
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat Assistant", "💊 Produits", "🏥 Pharmacies", "📊 Analytics"])
    
    with tab1:
        st.header("💬 Chat avec l'Assistant")
        
        # Zone de saisie
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_message = st.text_area(
                "Décrivez votre problème de peau :",
                placeholder="Ex: J'ai des boutons sur le visage depuis 2 semaines...",
                height=100
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Analyser", type="primary", use_container_width=True):
                if user_message.strip():
                    # Traitement du message
                    with st.spinner("🤖 Analyse en cours..."):
                        # Extraction de la durée
                        duration = assistant.extract_symptom_duration(user_message)
                        
                        # Recherche de produits
                        produits = assistant.search_products(
                            user_message,
                            st.session_state.user_profile.get('type_peau'),
                            st.session_state.user_profile.get('budget_max')
                        )
                        
                        # Génération de conseils
                        conseils = assistant.generate_personalized_advice(
                            user_message,
                            st.session_state.user_profile.get('type_peau'),
                            st.session_state.user_profile.get('age'),
                            duration
                        )
                        
                        # Ajouter à l'historique
                        st.session_state.conversation_history.append({
                            'user': user_message,
                            'duration': duration,
                            'produits': produits,
                            'conseils': conseils,
                            'timestamp': datetime.now()
                        })
        
        # Suggestions rapides
        st.markdown("**💡 Suggestions rapides :**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔴 Problème d'acné"):
                st.session_state.quick_message = "J'ai de l'acné depuis 1 mois"
        
        with col2:
            if st.button("💧 Peau sèche"):
                st.session_state.quick_message = "Ma peau est très sèche depuis l'harmattan"
        
        with col3:
            if st.button("🟤 Taches brunes"):
                st.session_state.quick_message = "J'ai des taches brunes depuis 6 mois"
        
        # Affichage de l'historique de conversation
        if st.session_state.conversation_history:
            st.markdown("---")
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
                        
                        african_badge = "🌍 **Produit Africain**" if is_african else ""
                        
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
                    st.plotly_chart(fig_prix, use_container_width=True)
            
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
                    st.plotly_chart(fig_ville, use_container_width=True)
            
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
                st.dataframe(df_marques, use_container_width=True)
            
            conn.close()
            
        except Exception as e:
            st.error(f"Erreur lors du chargement des statistiques: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🏥 Assistant Pharmacien Sénégal - Conseils cosmétiques avec produits africains authentiques<br>
        Développé avec ❤️ pour les pharmaciens et patients sénégalais
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()