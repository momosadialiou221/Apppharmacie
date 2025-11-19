#!/usr/bin/env python3
"""Script pour ajouter le filtre par problème de peau"""

# Lire le fichier
with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacement 1: Changer col3 en col4 pour prix_max
content = content.replace(
    '        with col3:\n            prix_max_filter = st.selectbox(\n                "Prix maximum",',
    '        with col4:\n            prix_max_filter = st.selectbox(\n                "Prix max",'
)

# Remplacement 2: Changer le format_func
content = content.replace(
    'format_func=lambda x: "Tous prix" if x is None else f"≤ {x:,} FCFA"',
    'format_func=lambda x: "Tous" if x is None else f"≤{x//1000}k FCFA"'
)

# Remplacement 3: Ajouter la logique de filtrage par problème
old_query_logic = '''            query = "SELECT * FROM produits WHERE 1=1"
            params = []
            
            if search_term:'''

new_query_logic = '''            query = "SELECT * FROM produits WHERE 1=1"
            params = []
            
            # Filtre par problème de peau
            if probleme_filter != "Tous":
                probleme_map = {
                    "Acné": "acné",
                    "Peau sèche": "sèche",
                    "Taches": "taches",
                    "Rides": "rides",
                    "Peau grasse": "grasse",
                    "Sensible": "sensible"
                }
                probleme_key = probleme_map.get(probleme_filter, "")
                if probleme_key:
                    query += " AND LOWER(problemes_cibles) LIKE ?"
                    params.append(f'%{probleme_key}%')
            
            if search_term:'''

content = content.replace(old_query_logic, new_query_logic)

# Écrire le fichier
with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Modifications appliquées avec succès!")
