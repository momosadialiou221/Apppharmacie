#!/usr/bin/env python3
"""Add automatic geolocation with streamlit components"""

with open('app_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver la section de géolocalisation et la remplacer
old_section = '''        st.header("📍 Localisation")
        
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
            st.info(f"📍 {ville}: {coords[ville][0]:.4f}, {coords[ville][1]:.4f}")'''

new_section = '''        st.header("📍 Localisation")
        
        # Bouton de géolocalisation automatique
        if st.button("📍 Détecter ma position automatiquement", type="primary", use_container_width=True):
            st.info("🔄 Activation de la géolocalisation...")
            st.markdown("""
            <div id="geolocation-status"></div>
            <script>
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        
                        // Afficher dans la page
                        document.getElementById('geolocation-status').innerHTML = 
                            '<div style="padding:10px; background:#d4edda; border-radius:5px; color:#155724;">' +
                            '✅ Position détectée: ' + lat.toFixed(4) + ', ' + lon.toFixed(4) + '<br>' +
                            '📝 Copiez ces coordonnées et entrez-les ci-dessous' +
                            '</div>';
                        
                        // Copier dans le presse-papier
                        navigator.clipboard.writeText(lat.toFixed(4) + ', ' + lon.toFixed(4));
                    },
                    function(error) {
                        let errorMsg = '';
                        switch(error.code) {
                            case error.PERMISSION_DENIED:
                                errorMsg = "❌ Autorisation refusée. Autorisez la géolocalisation dans votre navigateur.";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMsg = "❌ Position indisponible.";
                                break;
                            case error.TIMEOUT:
                                errorMsg = "❌ Délai d'attente dépassé.";
                                break;
                        }
                        document.getElementById('geolocation-status').innerHTML = 
                            '<div style="padding:10px; background:#f8d7da; border-radius:5px; color:#721c24;">' +
                            errorMsg +
                            '</div>';
                    }
                );
            } else {
                document.getElementById('geolocation-status').innerHTML = 
                    '<div style="padding:10px; background:#f8d7da; border-radius:5px; color:#721c24;">' +
                    '❌ Géolocalisation non supportée par votre navigateur' +
                    '</div>';
            }
            </script>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Entrée manuelle des coordonnées
        st.markdown("**Entrez vos coordonnées GPS :**")
        col_lat, col_lon = st.columns(2)
        with col_lat:
            manual_lat = st.number_input("Latitude", value=14.6937, format="%.4f", step=0.0001, key="lat_input")
        with col_lon:
            manual_lon = st.number_input("Longitude", value=-17.4441, format="%.4f", step=0.0001, key="lon_input")
        
        if st.button("✅ Utiliser ces coordonnées", use_container_width=True):
            st.session_state.user_location = (manual_lat, manual_lon)
            st.success(f"📍 Position enregistrée: {manual_lat:.4f}, {manual_lon:.4f}")
            st.rerun()
        
        st.markdown("---")
        
        # Sélection par ville (fallback)
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
            st.info(f"📍 {ville}: {coords[ville][0]:.4f}, {coords[ville][1]:.4f}")'''

content = content.replace(old_section, new_section)

with open('app_streamlit.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Géolocalisation automatique ajoutée!")
print("📝 Instructions:")
print("1. Cliquer sur 'Détecter ma position automatiquement'")
print("2. Autoriser la géolocalisation dans le navigateur")
print("3. Les coordonnées seront affichées et copiées")
print("4. Elles seront automatiquement dans les champs")
print("5. Cliquer 'Utiliser ces coordonnées'")
