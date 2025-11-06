#!/usr/bin/env python3
"""
Script de Déploiement Streamlit - Assistant Pharmacien Sénégal
Préparation et lancement de l'application web
"""

import subprocess
import sys
import os
import sqlite3

def check_dependencies():
    """Vérifie et installe les dépendances Streamlit"""
    print("📦 Vérification des dépendances Streamlit...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installé")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} manquant")
    
    if missing_packages:
        print(f"\n📥 Installation des packages manquants: {missing_packages}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "streamlit", "pandas", "plotly"
            ])
            print("✅ Dépendances installées avec succès!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des dépendances")
            return False
    
    return True

def check_database():
    """Vérifie que la base de données existe et contient des données"""
    print("\n🗄️  Vérification de la base de données...")
    
    if not os.path.exists('pharmacy_assistant.db'):
        print("❌ Base de données non trouvée")
        print("💡 Initialisation de la base de données...")
        
        try:
            subprocess.run([sys.executable, "data_init.py"], check=True)
            print("✅ Base de données initialisée")
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'initialisation")
            return False
    
    # Vérifier le contenu
    try:
        conn = sqlite3.connect('pharmacy_assistant.db')
        
        produits_count = conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0]
        pharmacies_count = conn.execute('SELECT COUNT(*) FROM pharmacies').fetchone()[0]
        
        conn.close()
        
        print(f"✅ Base de données OK:")
        print(f"   • {produits_count} produits")
        print(f"   • {pharmacies_count} pharmacies")
        
        if produits_count > 0 and pharmacies_count > 0:
            return True
        else:
            print("⚠️  Base de données vide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def create_streamlit_config():
    """Crée le fichier de configuration Streamlit"""
    print("\n⚙️  Configuration Streamlit...")
    
    config_dir = ".streamlit"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_content = """
[general]
dataFrameSerialization = "legacy"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#28a745"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    with open(os.path.join(config_dir, "config.toml"), "w") as f:
        f.write(config_content.strip())
    
    print("✅ Configuration Streamlit créée")

def launch_streamlit():
    """Lance l'application Streamlit"""
    print("\n🚀 Lancement de l'application Streamlit...")
    print("📱 L'application sera disponible sur: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_streamlit.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement: {e}")

def create_deployment_guide():
    """Crée un guide de déploiement"""
    guide_content = """
# 🚀 Guide de Déploiement Streamlit

## Déploiement Local

### 1. Installation des dépendances
```bash
pip install streamlit pandas plotly
```

### 2. Lancement de l'application
```bash
streamlit run app_streamlit.py
```

### 3. Accès à l'application
- URL locale: http://localhost:8501
- L'application se lance automatiquement dans votre navigateur

## Déploiement en Ligne

### Option 1: Streamlit Cloud (Gratuit)
1. Créer un compte sur https://streamlit.io/cloud
2. Connecter votre repository GitHub
3. Sélectionner le fichier `app_streamlit.py`
4. Déploiement automatique

### Option 2: Heroku
1. Créer un fichier `Procfile`:
```
web: streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0
```

2. Déployer sur Heroku:
```bash
heroku create assistant-pharmacien-senegal
git push heroku main
```

### Option 3: Railway
1. Connecter votre repository sur https://railway.app
2. Déploiement automatique avec détection Streamlit

## Fichiers Nécessaires pour le Déploiement
- `app_streamlit.py` (application principale)
- `requirements_streamlit.txt` (dépendances)
- `pharmacy_assistant.db` (base de données)
- `.streamlit/config.toml` (configuration)

## Variables d'Environnement (si nécessaire)
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

## Optimisations pour la Production
1. Mise en cache des données avec `@st.cache_data`
2. Optimisation des requêtes SQL
3. Compression des images
4. Configuration HTTPS
"""
    
    with open("DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Guide de déploiement créé: DEPLOYMENT_GUIDE.md")

def main():
    """Fonction principale de déploiement"""
    print("🚀 DÉPLOIEMENT STREAMLIT - Assistant Pharmacien Sénégal")
    print("=" * 60)
    
    # Vérifications préalables
    if not check_dependencies():
        print("❌ Échec de l'installation des dépendances")
        return
    
    if not check_database():
        print("❌ Problème avec la base de données")
        return
    
    # Configuration
    create_streamlit_config()
    create_deployment_guide()
    
    print("\n✅ Préparation terminée avec succès!")
    print("\n🎯 Options de lancement:")
    print("   1. Automatique: python deploy_streamlit.py")
    print("   2. Manuel: streamlit run app_streamlit.py")
    print("   3. Avec port: streamlit run app_streamlit.py --server.port 8501")
    
    # Demander si on veut lancer maintenant
    try:
        choice = input("\n🚀 Lancer l'application maintenant ? (o/n): ").lower().strip()
        if choice in ['o', 'oui', 'y', 'yes']:
            launch_streamlit()
        else:
            print("👍 Application prête à être lancée manuellement")
    except KeyboardInterrupt:
        print("\n👋 Au revoir!")

if __name__ == "__main__":
    main()