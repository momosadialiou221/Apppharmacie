#!/usr/bin/env python3
"""
Script de démarrage intelligent pour l'Assistant Pharmacien Sénégal
Détecte automatiquement les dépendances et lance la version appropriée
"""

import os
import sys
import subprocess

def check_dependencies():
    """Vérifie si les dépendances Flask sont disponibles"""
    try:
        import flask
        import geopy
        return True
    except ImportError:
        return False

def install_dependencies():
    """Tente d'installer les dépendances"""
    print("📦 Installation des dépendances...")
    
    commands = [
        [sys.executable, "-m", "pip", "install", "flask", "flask-cors", "geopy", "python-dotenv"],
        ["pip", "install", "flask", "flask-cors", "geopy", "python-dotenv"],
        ["pip3", "install", "flask", "flask-cors", "geopy", "python-dotenv"]
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ Dépendances installées avec succès!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    return False

def init_database():
    """Initialise la base de données si nécessaire"""
    if not os.path.exists('pharmacy_assistant.db'):
        print("🔧 Initialisation de la base de données...")
        try:
            from data_init import init_sample_data
            init_sample_data()
            print("✅ Base de données créée!")
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            return False
    return True

def start_flask_app():
    """Lance l'application Flask complète"""
    print("🚀 Lancement de l'application Flask...")
    
    # Vérifier si les dépendances NLP sont disponibles
    try:
        import nltk, sklearn, textblob
        print("🤖 Version avancée avec IA/NLP disponible")
        print("📱 Interface IA disponible sur: http://localhost:5000")
        
        try:
            from app_advanced import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Erreur version avancée: {e}")
            print("🔄 Basculement vers version standard...")
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("📱 Version standard disponible sur: http://localhost:5000")
        try:
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Erreur Flask: {e}")
            return False
    return True

def start_simple_app():
    """Lance l'application simple sans dépendances"""
    print("🚀 Lancement de l'application simple...")
    print("📱 Interface disponible sur: http://localhost:8000")
    
    try:
        from app_simple import main
        main()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    return True

def main():
    """Fonction principale"""
    print("🏥 Assistant Pharmacien Sénégal - Cosmétiques")
    print("=" * 50)
    
    # Initialiser la base de données
    if not init_database():
        print("❌ Impossible d'initialiser la base de données")
        sys.exit(1)
    
    # Vérifier les dépendances
    if check_dependencies():
        print("✅ Dépendances Flask détectées")
        start_flask_app()
    else:
        print("⚠️  Dépendances Flask non trouvées")
        
        # Demander si on veut installer
        try:
            choice = input("Voulez-vous installer Flask? (o/n): ").lower().strip()
            if choice in ['o', 'oui', 'y', 'yes']:
                if install_dependencies() and check_dependencies():
                    start_flask_app()
                else:
                    print("❌ Installation échouée, utilisation de la version simple")
                    start_simple_app()
            else:
                print("📱 Utilisation de la version simple")
                start_simple_app()
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
            sys.exit(0)

if __name__ == '__main__':
    main()