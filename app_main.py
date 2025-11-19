#!/usr/bin/env python3
"""
Assistant Pharmacien Sénégal - Version Flask Complète
Interface publique moderne avec chat flottant
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import re
import math
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)

class PharmacyAssistant:
    """Assistant Pharmacien avec toutes les fonctionnalités"""
    
    def __init__(self):
        self.db_path = 'pharmacy_assistant.db'
    
    def get_db_connection(self):
        """Connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def search_products(self, query, type_peau=None, budget_max=None, limit=50):
        """Recherche de produits"""
        conn = self.get_db_connection()
        
        sql = "SELECT * FROM produits WHERE 1=1"
        params = []
        
        if query:
            sql += " AND (LOWER(nom) LIKE ? OR LOWER(problemes_cibles) LIKE ? OR LOWER(description) LIKE ?)"
            search_term = f'%{query.lower()}%'
            params.extend([search_term, search_term, search_term])
        
        if type_peau:
            sql += " AND LOWER(problemes_cibles) LIKE ?"
            params.append(f'%{type_peau.lower()}%')
        
        if budget_max:
            sql += " AND prix_min <= ?"
            params.append(budget_max)
        
        sql += f" ORDER BY prix_min ASC LIMIT {limit}"
        
        produits = conn.execute(sql, params).fetchall()
        conn.close()
        
        return [dict(p) for p in produits]
    
    def get_all_products(self, page=1, per_page=20):
        """Récupère tous les produits avec pagination"""
        conn = self.get_db_connection()
        offset = (page - 1) * per_page
        
        produits = conn.execute(
            'SELECT * FROM produits ORDER BY nom LIMIT ? OFFSET ?',
            (per_page, offset)
        ).fetchall()
        
        total = conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0]
        conn.close()
        
        return {
            'produits': [dict(p) for p in produits],
            'total': total,
            'pages': math.ceil(total / per_page),
            'current_page': page
        }
    
    def get_pharmacies(self, ville=None, h24_only=False, page=1, per_page=20):
        """Récupère les pharmacies avec pagination"""
        conn = self.get_db_connection()
        offset = (page - 1) * per_page
        
        sql = "SELECT * FROM pharmacies WHERE 1=1"
        params = []
        
        if ville:
            sql += " AND ville = ?"
            params.append(ville)
        
        if h24_only:
            sql += " AND ouvert_24h = 1"
        
        sql += " ORDER BY ville, nom LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        pharmacies = conn.execute(sql, params).fetchall()
        
        # Count total
        count_sql = "SELECT COUNT(*) FROM pharmacies WHERE 1=1"
        count_params = []
        if ville:
            count_sql += " AND ville = ?"
            count_params.append(ville)
        if h24_only:
            count_sql += " AND ouvert_24h = 1"
        
        total = conn.execute(count_sql, count_params).fetchone()[0]
        conn.close()
        
        return {
            'pharmacies': [dict(p) for p in pharmacies],
            'total': total,
            'pages': math.ceil(total / per_page),
            'current_page': page
        }
    
    def get_nearby_pharmacies(self, user_lat, user_lon, h24_only=False, limit=10):
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
        
        # Trier par distance
        pharmacies_with_distance.sort(key=lambda x: x['distance'])
        return pharmacies_with_distance[:limit]
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calcule la distance entre deux points GPS"""
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c
    
    def extract_skin_problems(self, text):
        """Extrait les problèmes de peau du texte"""
        problems = []
        text_lower = text.lower()
        
        problem_keywords = {
            'acné': ['acné', 'acne', 'bouton', 'boutons', 'point noir', 'comédons'],
            'sèche': ['sèche', 'seche', 'déshydrat', 'tiraille', 'rugueuse'],
            'grasse': ['grasse', 'gras', 'brillant', 'sébum', 'luisant'],
            'taches': ['tache', 'taches', 'hyperpigmentation', 'melasma', 'marque'],
            'sensible': ['sensible', 'irrité', 'rouge', 'rougeur', 'réactif'],
            'rides': ['ride', 'rides', 'ridule', 'vieillissement', 'anti-âge']
        }
        
        for problem, keywords in problem_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                problems.append(problem)
        
        return problems
    
    def save_conversation_to_csv(self, conversation_data):
        """Sauvegarde la conversation dans un fichier CSV"""
        csv_file = 'conversations_historique.csv'
        file_exists = os.path.isfile(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'timestamp', 'age', 'type_peau', 'probleme_initial', 
                    'produits_recommandes', 'nombre_produits', 'session_id'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(conversation_data)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

# Instance globale
assistant = PharmacyAssistant()

# Routes
@app.route('/')
def index():
    """Page d'accueil - Produits cosmétiques"""
    return render_template('index_main.html')

@app.route('/produits')
def produits():
    """Page des produits"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    if search:
        products = assistant.search_products(search, limit=20)
        result = {
            'produits': products,
            'total': len(products),
            'pages': 1,
            'current_page': 1
        }
    else:
        result = assistant.get_all_products(page=page, per_page=20)
    
    return render_template('produits.html', **result, search=search)

@app.route('/pharmacies')
def pharmacies():
    """Page des pharmacies"""
    page = request.args.get('page', 1, type=int)
    ville = request.args.get('ville', '')
    h24 = request.args.get('h24', 'false') == 'true'
    
    result = assistant.get_pharmacies(
        ville=ville if ville else None,
        h24_only=h24,
        page=page,
        per_page=20
    )
    
    return render_template('pharmacies.html', **result, ville=ville, h24=h24)

@app.route('/historique')
def historique():
    """Page de l'historique des conversations"""
    return render_template('historique.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API pour le chat"""
    data = request.json
    message = data.get('message', '')
    user_profile = data.get('profile', {})
    
    # Extraire les problèmes
    problems = assistant.extract_skin_problems(message)
    
    # Rechercher des produits
    produits = assistant.search_products(
        message,
        type_peau=user_profile.get('type_peau'),
        budget_max=user_profile.get('budget_max'),
        limit=5
    )
    
    # Créer la réponse
    response = {
        'message': f"J'ai trouvé {len(produits)} produits adaptés à votre problème.",
        'produits': produits,
        'problems': problems
    }
    
    # Sauvegarder la conversation
    csv_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'age': user_profile.get('age', ''),
        'type_peau': user_profile.get('type_peau', ''),
        'probleme_initial': message,
        'produits_recommandes': ', '.join([p['nom'] for p in produits[:5]]),
        'nombre_produits': len(produits),
        'session_id': data.get('session_id', '')
    }
    assistant.save_conversation_to_csv(csv_data)
    
    return jsonify(response)

@app.route('/api/pharmacies/nearby', methods=['POST'])
def nearby_pharmacies():
    """API pour trouver les pharmacies proches"""
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    h24_only = data.get('h24_only', False)
    
    if not lat or not lon:
        return jsonify({'error': 'Coordonnées manquantes'}), 400
    
    pharmacies = assistant.get_nearby_pharmacies(lat, lon, h24_only=h24_only, limit=10)
    
    return jsonify({'pharmacies': pharmacies})

@app.route('/api/stats')
def stats():
    """API pour les statistiques"""
    conn = assistant.get_db_connection()
    
    stats_data = {
        'total_produits': conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0],
        'total_pharmacies': conn.execute('SELECT COUNT(*) FROM pharmacies').fetchone()[0],
        'pharmacies_24h': conn.execute('SELECT COUNT(*) FROM pharmacies WHERE ouvert_24h = 1').fetchone()[0],
    }
    
    conn.close()
    return jsonify(stats_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
