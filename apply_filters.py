#!/usr/bin/env python3
import re

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacement 1: Changer 3 colonnes en 4
content = content.replace(
    '        col1, col2, col3 = st.columns(3)\n        \n        with col1:\n            search_term = st.text_input("🔍 Rechercher un produit")',
    '        col1, col2, col3, col4 = st.columns(4)\n        \n        with col1:\n            probleme_filter = st.selectbox(\n                "Problème",\n                ["Tous", "Acné", "Peau sèche", "Taches", "Rides", "Peau grasse", "Sensible"]\n            )\n        \n        with col2:\n            search_term = st.text_input("🔍 Rechercher")'
)

# Remplacement 2: col3 -> col4
content = content.replace(
    '        with col3:\n            prix_max_filter = st.selectbox(\n                "Prix maximum",',
    '        with col4:\n            prix_max_filter = st.selectbox(\n                "Prix max",'
)

# Remplacement 3: format_func
content = content.replace(
    'format_func=lambda x: "Tous prix" if x is None else f"≤ {x:,} FCFA"',
    'format_func=lambda x: "Tous" if x is None else f"≤{x//1000}k FCFA"'
)

# Remplacement 4: Ajouter logique filtrage
old_logic = '''            query = "SELECT * FROM produits WHERE 1=1"
            params = []
            
            if search_term:'''

new_logic = '''            query = "SELECT * FROM produits WHERE 1=1"
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

content = content.replace(old_logic, new_logic)

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Modifications appliquées!")
