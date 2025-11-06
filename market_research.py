#!/usr/bin/env python3
"""
Module d'étude de marché pour l'Assistant Pharmacien Sénégal
Analyse des besoins via sondages et feedback pharmaciens
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List

class MarketResearch:
    """Gestionnaire d'étude de marché et feedback pharmaciens"""
    
    def __init__(self, db_path: str = 'pharmacy_assistant.db'):
        self.db_path = db_path
        self.init_research_tables()
    
    def init_research_tables(self):
        """Initialise les tables pour l'étude de marché"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des sondages pharmaciens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sondages_pharmaciens (
                id INTEGER PRIMARY KEY,
                nom_pharmacie TEXT,
                ville TEXT,
                experience_annees INTEGER,
                problemes_frequents TEXT,
                marques_preferees TEXT,
                besoins_formation TEXT,
                satisfaction_actuelle INTEGER,
                suggestions TEXT,
                date_sondage TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des besoins identifiés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS besoins_marche (
                id INTEGER PRIMARY KEY,
                categorie TEXT,
                besoin_description TEXT,
                priorite INTEGER,
                frequence_mention INTEGER DEFAULT 1,
                statut TEXT DEFAULT 'identifie',
                date_identification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des produits demandés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits_demandes (
                id INTEGER PRIMARY KEY,
                nom_produit TEXT,
                marque_souhaitee TEXT,
                probleme_cible TEXT,
                prix_souhaite_min REAL,
                prix_souhaite_max REAL,
                nb_demandes INTEGER DEFAULT 1,
                disponible BOOLEAN DEFAULT 0,
                date_premiere_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def ajouter_sondage_pharmacien(self, sondage_data: Dict):
        """Ajoute un sondage de pharmacien"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sondages_pharmaciens (
                nom_pharmacie, ville, experience_annees, problemes_frequents,
                marques_preferees, besoins_formation, satisfaction_actuelle, suggestions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sondage_data.get('nom_pharmacie'),
            sondage_data.get('ville'),
            sondage_data.get('experience_annees'),
            json.dumps(sondage_data.get('problemes_frequents', [])),
            json.dumps(sondage_data.get('marques_preferees', [])),
            sondage_data.get('besoins_formation'),
            sondage_data.get('satisfaction_actuelle'),
            sondage_data.get('suggestions')
        ))
        
        conn.commit()
        conn.close()
    
    def analyser_besoins_marche(self) -> Dict:
        """Analyse les besoins du marché basés sur les sondages"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Problèmes les plus fréquents
        sondages = conn.execute('SELECT problemes_frequents FROM sondages_pharmaciens').fetchall()
        
        problemes_count = {}
        for sondage in sondages:
            if sondage['problemes_frequents']:
                problemes = json.loads(sondage['problemes_frequents'])
                for probleme in problemes:
                    problemes_count[probleme] = problemes_count.get(probleme, 0) + 1
        
        # Marques les plus demandées
        marques = conn.execute('SELECT marques_preferees FROM sondages_pharmaciens').fetchall()
        marques_count = {}
        for marque_data in marques:
            if marque_data['marques_preferees']:
                marques_list = json.loads(marque_data['marques_preferees'])
                for marque in marques_list:
                    marques_count[marque] = marques_count.get(marque, 0) + 1
        
        # Satisfaction moyenne
        satisfaction = conn.execute(
            'SELECT AVG(satisfaction_actuelle) as moyenne FROM sondages_pharmaciens'
        ).fetchone()
        
        conn.close()
        
        return {
            'problemes_frequents': sorted(problemes_count.items(), key=lambda x: x[1], reverse=True),
            'marques_demandees': sorted(marques_count.items(), key=lambda x: x[1], reverse=True),
            'satisfaction_moyenne': satisfaction['moyenne'] if satisfaction['moyenne'] else 0,
            'total_sondages': len(sondages)
        }
    
    def generer_sondages_exemple(self):
        """Génère des sondages d'exemple basés sur 20 pharmaciens fictifs"""
        sondages_exemple = [
            {
                'nom_pharmacie': 'Pharmacie Plateau Central',
                'ville': 'Dakar',
                'experience_annees': 15,
                'problemes_frequents': ['acné', 'peau sèche', 'taches brunes'],
                'marques_preferees': ['La Roche-Posay', 'Vichy', 'Eucerin'],
                'besoins_formation': 'Nouveaux ingrédients actifs, conseils anti-âge',
                'satisfaction_actuelle': 7,
                'suggestions': 'Plus de produits pour peaux noires, formation continue'
            },
            {
                'nom_pharmacie': 'Pharmacie Liberté',
                'ville': 'Dakar',
                'experience_annees': 8,
                'problemes_frequents': ['acné adolescente', 'hyperpigmentation', 'peau sensible'],
                'marques_preferees': ['Fair & White', 'Caro White', 'Avène'],
                'besoins_formation': 'Conseil personnalisé, dermatologie',
                'satisfaction_actuelle': 6,
                'suggestions': 'Outils de diagnostic, base de données élargie'
            },
            {
                'nom_pharmacie': 'Pharmacie Thiès Centre',
                'ville': 'Thiès',
                'experience_annees': 12,
                'problemes_frequents': ['peau sèche', 'eczéma', 'protection solaire'],
                'marques_preferees': ['Eucerin', 'Sebamed', 'Nivea'],
                'besoins_formation': 'Soins pédiatriques, allergies cutanées',
                'satisfaction_actuelle': 8,
                'suggestions': 'Plus de produits naturels, prix accessibles'
            },
            # Ajouter 17 autres sondages...
        ]
        
        # Compléter avec des variations
        villes = ['Dakar', 'Thiès', 'Saint-Louis', 'Kaolack', 'Ziguinchor']
        problemes_pool = [
            ['acné', 'peau grasse', 'points noirs'],
            ['peau sèche', 'eczéma', 'dermatite'],
            ['taches brunes', 'melasma', 'hyperpigmentation'],
            ['rides', 'anti-âge', 'fermeté'],
            ['peau sensible', 'irritation', 'rougeurs']
        ]
        marques_pool = [
            ['La Roche-Posay', 'Vichy', 'Avène'],
            ['Fair & White', 'Caro White', 'Makari'],
            ['Eucerin', 'Sebamed', 'CeraVe'],
            ['Nivea', 'Palmer\'s', 'L\'Occitane']
        ]
        
        for i in range(4, 21):  # Compléter jusqu'à 20
            sondages_exemple.append({
                'nom_pharmacie': f'Pharmacie {villes[i % len(villes)]} {i}',
                'ville': villes[i % len(villes)],
                'experience_annees': 5 + (i % 15),
                'problemes_frequents': problemes_pool[i % len(problemes_pool)],
                'marques_preferees': marques_pool[i % len(marques_pool)],
                'besoins_formation': 'Formation continue, nouveaux produits',
                'satisfaction_actuelle': 5 + (i % 5),
                'suggestions': 'Améliorer l\'offre produits, formation pratique'
            })
        
        # Insérer tous les sondages
        for sondage in sondages_exemple:
            self.ajouter_sondage_pharmacien(sondage)
        
        print(f"✅ {len(sondages_exemple)} sondages pharmaciens ajoutés")

def main():
    """Test du module d'étude de marché"""
    research = MarketResearch()
    
    print("📊 Génération des sondages d'exemple...")
    research.generer_sondages_exemple()
    
    print("\n📈 Analyse des besoins du marché...")
    analyse = research.analyser_besoins_marche()
    
    print(f"\n🎯 Résultats de l'étude de marché ({analyse['total_sondages']} pharmaciens) :")
    print(f"📊 Satisfaction moyenne : {analyse['satisfaction_moyenne']:.1f}/10")
    
    print(f"\n🔥 Top 5 problèmes les plus fréquents :")
    for probleme, count in analyse['problemes_frequents'][:5]:
        print(f"   • {probleme} : {count} mentions")
    
    print(f"\n🏷️  Top 5 marques les plus demandées :")
    for marque, count in analyse['marques_demandees'][:5]:
        print(f"   • {marque} : {count} mentions")

if __name__ == '__main__':
    main()