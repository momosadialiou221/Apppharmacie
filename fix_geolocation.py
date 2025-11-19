#!/usr/bin/env python3
"""Fix geolocation section"""

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_geo = '''        st.header("📍 Localisation")
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
        
        h24_only = st.checkbox("Pharmacies 24h/24 seulement")'''

new_geo = '''        st.header("📍 Localisation")
        
        # Option 1: Coordonnées manuelles (GPS)
        with st.expander("🌐 Entrer coordonnées GPS"):
            st.markdown("**Obtenez vos coordonnées GPS :**")
            st.markdown("- Google Maps : Clic droit sur votre position → Coordonnées")
            st.markdown("- Smartphone : Applications GPS")
            
            col_lat, col_lon = st.columns(2)
            with col_lat:
                manual_lat = st.number_input("Latitude", value=14.6937, format="%.4f", step=0.0001)
            with col_lon:
                manual_lon = st.number_input("Longitude", value=-17.4441, format="%.4f", step=0.0001)
            
            if st.button("✅ Utiliser ces coordonnées"):
                st.session_state.user_location = (manual_lat, manual_lon)
                st.success(f"📍 Position GPS: {manual_lat:.4f}, {manual_lon:.4f}")
        
        # Option 2: Sélection par ville
        st.markdown("**Ou sélectionnez votre ville :**")
        ville = st.selectbox(
            "Ville",
            ["Dakar", "Thiès", "Saint-Louis", "Kaolack"],
            label_visibility="collapsed"
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
            st.info(f"📍 {ville}: {coords[ville][0]:.4f}, {coords[ville][1]:.4f}")
        
        h24_only = st.checkbox("Pharmacies 24h/24 seulement")'''

content = content.replace(old_geo, new_geo)

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Géolocalisation corrigée!")
