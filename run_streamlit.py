#!/usr/bin/env python3
"""
Script de Lancement Streamlit - Assistant Pharmacien Sénégal
Lancement rapide de l'application web
"""

import subprocess
import sys
import os

def install_streamlit():
    """Installe Streamlit si nécessaire"""
    try:
        import streamlit
        print("✅ Streamlit déjà installé")
        return True
    except ImportError:
        print("📦 Installation de Streamlit...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "streamlit", "pandas", "plotly"
            ])
            print("✅ Streamlit installé avec succès!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation de Streamlit")
            return False

def check_database():
    """Vérifie la base de données"""
    if not os.path.exists('pharmacy_assistant.db'):
        print("🗄️  Initialisation de la base de données...")
        try:
            subprocess.run([sys.executable, "data_init.py"], check=True)
            print("✅ Base de données créée")
        except:
            print("❌ Erreur création base de données")
            return False
    else:
        print("✅ Base de données trouvée")
    return True

def launch_streamlit():
    """Lance l'application Streamlit"""
    print("\n🚀 Lancement de l'Assistant Pharmacien Sénégal")
    print("=" * 55)
    print("📱 Interface Streamlit moderne")
    print("🤖 Chat intelligent avec IA")
    print("🌍 Produits africains authentiques")
    print("🏥 100+ pharmacies géolocalisées")
    print("\n🌐 L'application va s'ouvrir dans votre navigateur...")
    print("📍 URL locale : http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        # Lancer Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_streamlit.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")

def main():
    """Fonction principale"""
    print("🏥 ASSISTANT PHARMACIEN SÉNÉGAL - STREAMLIT")
    print("=" * 50)
    
    # Vérifications
    if not install_streamlit():
        return
    
    if not check_database():
        return
    
    # Lancement
    launch_streamlit()

if __name__ == "__main__":
    main()