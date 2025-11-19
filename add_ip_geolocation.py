#!/usr/bin/env python3
"""Add IP-based geolocation"""

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver où ajouter l'import
for i, line in enumerate(lines):
    if 'import numpy as np' in line:
        # Ajouter après numpy
        lines.insert(i+1, 'import geocoder\n')
        print(f"✅ Import geocoder ajouté à la ligne {i+2}")
        break

# Trouver la section de géolocalisation et ajouter le bouton automatique
for i, line in enumerate(lines):
    if 'st.header("📍 Localisation")' in line:
        # Trouver la ligne après et insérer le code
        insert_pos = i + 2
        
        new_code = '''        
        # Détection automatique via IP
        col_auto, col_manual = st.columns([2, 1])
        
        with col_auto:
            if st.button("🌍 Détecter ma position automatiquement", type="primary", use_container_width=True):
                with st.spinner("🔄 Détection de votre position..."):
                    try:
                        g = geocoder.ip('me')
                        if g.ok and g.latlng:
                            lat, lon = g.latlng
                            st.session_state.user_location = (lat, lon)
                            st.session_state.detected_city = g.city or "Position détectée"
                            st.success(f"✅ Position détectée: {lat:.4f}, {lon:.4f}")
                            if g.city:
                                st.info(f"📍 Ville: {g.city}, {g.country}")
                            st.rerun()
                        else:
                            st.warning("⚠️ Impossible de détecter votre position. Utilisez la sélection manuelle.")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
                        st.info("💡 Utilisez la sélection par ville ci-dessous")
        
        with col_manual:
            if st.button("🔄 Réinitialiser", use_container_width=True):
                if 'user_location' in st.session_state:
                    del st.session_state.user_location
                if 'detected_city' in st.session_state:
                    del st.session_state.detected_city
                st.rerun()
        
        # Afficher la position actuelle
        if 'user_location' in st.session_state and st.session_state.user_location:
            lat, lon = st.session_state.user_location
            city_info = st.session_state.get('detected_city', 'Position enregistrée')
            st.success(f"📍 {city_info}: {lat:.4f}, {lon:.4f}")
        
        st.markdown("---")
        
'''
        
        lines.insert(insert_pos, new_code)
        print(f"✅ Code de détection automatique ajouté à la ligne {insert_pos}")
        break

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n🎉 Géolocalisation automatique par IP ajoutée!")
print("\n📝 Comment ça marche:")
print("1. Cliquer sur '🌍 Détecter ma position automatiquement'")
print("2. L'application détecte votre position via votre adresse IP")
print("3. Position enregistrée automatiquement")
print("4. Aller dans 'Pharmacies' pour voir les distances réelles!")
