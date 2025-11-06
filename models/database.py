import sqlite3
from typing import List, Dict, Optional
import json

class DatabaseManager:
    """Gestionnaire de base de données pour l'assistant pharmacien"""
    
    def __init__(self, db_path: str = 'pharmacy_assistant.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtient une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialise les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table des produits cosmétiques
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                marque TEXT,
                type_produit TEXT,
                problemes_cibles TEXT,
                prix_min REAL,
                prix_max REAL,
                description TEXT,
                ingredients_actifs TEXT,
                disponible BOOLEAN DEFAULT 1,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des pharmacies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pharmacies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                adresse TEXT,
                latitude REAL,
                longitude REAL,
                telephone TEXT,
                horaires TEXT,
                ouvert_24h BOOLEAN DEFAULT 0,
                ville TEXT,
                actif BOOLEAN DEFAULT 1,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des consultations (historique)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                probleme_decrit TEXT,
                type_peau TEXT,
                age INTEGER,
                produits_recommandes TEXT,
                conseils_donnes TEXT,
                date_consultation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def rechercher_produits(self, probleme: str, type_peau: str = None, 
                           prix_max: float = None) -> List[Dict]:
        """Recherche des produits selon les critères"""
        conn = self.get_connection()
        
        query = '''
            SELECT * FROM produits 
            WHERE disponible = 1 AND problemes_cibles LIKE ?
        '''
        params = [f'%{probleme.lower()}%']
        
        if prix_max:
            query += ' AND prix_min <= ?'
            params.append(prix_max)
        
        query += ' ORDER BY prix_min ASC'
        
        produits = conn.execute(query, params).fetchall()
        conn.close()
        
        return [dict(produit) for produit in produits]
    
    def obtenir_pharmacies_proches(self, latitude: float, longitude: float,
                                  h24_seulement: bool = False) -> List[Dict]:
        """Obtient toutes les pharmacies (le calcul de distance se fait côté application)"""
        conn = self.get_connection()
        
        query = 'SELECT * FROM pharmacies WHERE actif = 1'
        if h24_seulement:
            query += ' AND ouvert_24h = 1'
        
        pharmacies = conn.execute(query).fetchall()
        conn.close()
        
        return [dict(pharmacie) for pharmacie in pharmacies]
    
    def ajouter_produit(self, produit_data: Dict) -> int:
        """Ajoute un nouveau produit"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO produits (nom, marque, type_produit, problemes_cibles,
                                prix_min, prix_max, description, ingredients_actifs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            produit_data['nom'], produit_data.get('marque'),
            produit_data.get('type_produit'), produit_data.get('problemes_cibles'),
            produit_data.get('prix_min'), produit_data.get('prix_max'),
            produit_data.get('description'), produit_data.get('ingredients_actifs')
        ))
        
        produit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return produit_id
    
    def ajouter_pharmacie(self, pharmacie_data: Dict) -> int:
        """Ajoute une nouvelle pharmacie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pharmacies (nom, adresse, latitude, longitude,
                                  telephone, horaires, ouvert_24h, ville)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pharmacie_data['nom'], pharmacie_data.get('adresse'),
            pharmacie_data.get('latitude'), pharmacie_data.get('longitude'),
            pharmacie_data.get('telephone'), pharmacie_data.get('horaires'),
            pharmacie_data.get('ouvert_24h', False), pharmacie_data.get('ville')
        ))
        
        pharmacie_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return pharmacie_id
    
    def enregistrer_consultation(self, consultation_data: Dict) -> int:
        """Enregistre une consultation dans l'historique"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO consultations (probleme_decrit, type_peau, age,
                                     produits_recommandes, conseils_donnes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            consultation_data['probleme'],
            consultation_data.get('type_peau'),
            consultation_data.get('age'),
            json.dumps(consultation_data.get('produits_recommandes', [])),
            json.dumps(consultation_data.get('conseils', []))
        ))
        
        consultation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return consultation_id
    
    def obtenir_statistiques(self) -> Dict:
        """Obtient des statistiques sur l'utilisation"""
        conn = self.get_connection()
        
        stats = {}
        
        # Nombre total de produits
        stats['total_produits'] = conn.execute(
            'SELECT COUNT(*) FROM produits WHERE disponible = 1'
        ).fetchone()[0]
        
        # Nombre total de pharmacies
        stats['total_pharmacies'] = conn.execute(
            'SELECT COUNT(*) FROM pharmacies WHERE actif = 1'
        ).fetchone()[0]
        
        # Pharmacies 24h
        stats['pharmacies_24h'] = conn.execute(
            'SELECT COUNT(*) FROM pharmacies WHERE ouvert_24h = 1 AND actif = 1'
        ).fetchone()[0]
        
        # Consultations du jour
        stats['consultations_aujourd_hui'] = conn.execute(
            'SELECT COUNT(*) FROM consultations WHERE DATE(date_consultation) = DATE("now")'
        ).fetchone()[0]
        
        # Problèmes les plus fréquents
        problemes_freq = conn.execute('''
            SELECT probleme_decrit, COUNT(*) as freq 
            FROM consultations 
            WHERE date_consultation >= datetime('now', '-30 days')
            GROUP BY LOWER(probleme_decrit)
            ORDER BY freq DESC 
            LIMIT 5
        ''').fetchall()
        
        stats['problemes_frequents'] = [dict(p) for p in problemes_freq]
        
        conn.close()
        return stats