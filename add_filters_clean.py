#!/usr/bin/env python3
"""Script pour ajouter proprement les filtres"""
import re

# Lire le fichier
with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver et remplacer la ligne avec col1, col2, col3
for i, line in enumerate(lines):
    # Ligne 1019 environ
    if 'col1, col2, col3 = st.columns(3)' in line and i > 1000:
        lines[i] = '        col1, col2, col3, col4 = st.columns(4)\n'
        print(f"✅ Ligne {i+1}: Changé en 4 colonnes")
        
        # Ajouter le filtre problème après
        # Trouver "with col1:"
        for j in range(i+1, min(i+10, len(lines))):
            if 'with col1:' in lines[j]:
                # Insérer le filtre problème
                indent = '            '
                new_lines = [
                    f'{indent}probleme_filter = st.selectbox(\n',
                    f'{indent}    "Problème de peau",\n',
                    f'{indent}    ["Tous", "Acné", "Peau sèche", "Taches", "Rides", "Peau grasse", "Sensible"]\n',
                    f'{indent})\n',
                    '\n',
                    '        with col2:\n'
                ]
                # Remplacer "search_term = st.text_input"
                for k in range(j+1, min(j+5, len(lines))):
                    if 'search_term = st.text_input' in lines[k]:
                        lines[j+1:k] = new_lines
                        print(f"✅ Ajouté filtre problème à la ligne {j+2}")
                        break
                break
        break

# Trouver et modifier "with col3:" en "with col4:"
for i, line in enumerate(lines):
    if 'with col3:' in line and 'prix_max_filter' in lines[i+1] if i+1 < len(lines) else False:
        lines[i] = '        with col4:\n'
        print(f"✅ Ligne {i+1}: Changé col3 en col4")
        break

# Ajouter la logique de filtrage
for i, line in enumerate(lines):
    if 'query = "SELECT * FROM produits WHERE 1=1"' in line:
        # Trouver la ligne "if search_term:"
        for j in range(i+1, min(i+10, len(lines))):
            if 'if search_term:' in lines[j]:
                # Insérer la logique de filtrage avant
                filter_logic = '''            
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
            
'''
                lines.insert(j, filter_logic)
                print(f"✅ Ajouté logique de filtrage à la ligne {j+1}")
                break
        break

# Écrire le fichier
with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n🎉 Modifications terminées!")
